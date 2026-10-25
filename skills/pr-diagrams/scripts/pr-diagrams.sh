#!/bin/bash
# Render draw.io PR diagrams and look up promotion sources and reviewers.
# Status goes to stderr. stdout is JSON only, and empty on failure.
set -euo pipefail

GH=${GH:-gh}
TMPS=()
cleanup() { rm -rf "${TMPS[@]}"; }
trap cleanup EXIT

die() { echo "pr-diagrams: $*" >&2; exit 1; }

note_override_ignored() {
  if [ -n "${PR_DIAGRAMS_REPO:-}" ]; then
    echo "pr-diagrams: ignoring PR_DIAGRAMS_REPO (set only for tests, and only with a stub GH)" >&2
  fi
}

repo_of() {
  if [ -n "${PR_DIAGRAMS_REPO:-}" ] && [ -n "${GH:-}" ] && [ "$GH" != "gh" ]; then
    printf '%s\n' "$PR_DIAGRAMS_REPO"
    return 0
  fi
  note_override_ignored
  local url
  url=$(git remote get-url origin 2>/dev/null) || die "no origin remote"
  local path=""
  case "$url" in
    https://github.com/*) path=${url#https://github.com/} ;;
    ssh://git@github.com/*) path=${url#ssh://git@github.com/} ;;
    git@github.com:*) path=${url#git@github.com:} ;;
    *) die "origin is not a GitHub URL: $url" ;;
  esac
  path=${path%.git}
  path=${path%/}
  case "$path" in
    */*) printf '%s\n' "$path" ;;
    *) die "origin is not a GitHub URL: $url" ;;
  esac
}

cmd_related() {
  local base="" head="" exclude=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --exclude-pr) shift; exclude=$1 ;;
      --fail-code) shift; FAIL_CODE=$1 ;;
      --fail-msg) shift; FAIL_MSG=$1 ;;
      --fail-body) shift; FAIL_BODY=$1 ;;
      *)
        if [ -z "$base" ]; then base=$1
        elif [ -z "$head" ]; then head=$1
        else die "unexpected argument: $1"; fi
        ;;
    esac
    shift
  done
  [ -n "$base" ] && [ -n "$head" ] || die "usage: pr-diagrams.sh related <base> <head> [--exclude-pr N]"
  local repo
  repo=$(repo_of)
  local fetch_err
  fetch_err=$(mktemp); TMPS+=("$fetch_err")
  if ! git fetch origin "$base" "$head" >"$fetch_err" 2>&1; then
    cat "$fetch_err" >&2
    exit 1
  fi
  local shas sha out err
  shas=$(git rev-list --reverse "origin/$base..origin/$head")
  local acc
  acc=$(mktemp); TMPS+=("$acc")
  : > "$acc"
  for sha in $shas; do
    err=$(mktemp); TMPS+=("$err")
    local extra=()
    [ -n "${FAIL_CODE:-}" ] && extra+=(--fail-code "$FAIL_CODE" --fail-msg "${FAIL_MSG:-}" --fail-body "${FAIL_BODY:-}")
    if ! out=$("$GH" api --paginate --jq '.[]' "${extra[@]}" "repos/$repo/commits/$sha/pulls" 2>"$err"); then
      cat "$err" >&2
      if grep -q -E '\(HTTP (403|429)\)' "$err"; then
        die "rate limited on commit $sha"
      fi
      die "lookup failed for commit $sha"
    fi
    printf '%s\n' "$out" >> "$acc"
  done
  jq -s --argjson exclude "${exclude:-0}" '
    map(select(.merged_at != null and .number != $exclude))
    | unique_by(.number)
    | sort_by(.merged_at, .number) | reverse
    | map({pr: .number, title, head_ref: .head.ref, base_ref: .base.ref, merged_at})
  ' "$acc"
}

cmd_reviewers() {
  local exclude="" prs=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --exclude) shift; exclude=$1 ;;
      --fail-code) shift; FAIL_CODE=$1 ;;
      --fail-msg) shift; FAIL_MSG=$1 ;;
      --fail-body) shift; FAIL_BODY=$1 ;;
      *) prs+=("$1") ;;
    esac
    shift
  done
  [ ${#prs[@]} -gt 0 ] || die "usage: pr-diagrams.sh reviewers <PR>... [--exclude LOGIN]"
  local repo
  repo=$(repo_of)
  local acc
  acc=$(mktemp); TMPS+=("$acc")
  : > "$acc"
  local pr out err extra
  for pr in "${prs[@]}"; do
    err=$(mktemp); TMPS+=("$err")
    extra=()
    [ -n "${FAIL_CODE:-}" ] && extra+=(--fail-code "$FAIL_CODE" --fail-msg "${FAIL_MSG:-}" --fail-body "${FAIL_BODY:-}")
    if ! out=$("$GH" api --paginate --jq '.[]' "${extra[@]}" "repos/$repo/pulls/$pr/reviews" 2>"$err"); then
      cat "$err" >&2
      die "PR $pr: reviews lookup failed"
    fi
    printf '%s\n' "$out" | jq -c 'select(.user != null and .user.type == "User") | {login: .user.login, type: .user.type}' >> "$acc"
    err=$(mktemp); TMPS+=("$err")
    if ! out=$("$GH" api --jq '.users[]' "${extra[@]}" "repos/$repo/pulls/$pr/requested_reviewers" 2>"$err"); then
      cat "$err" >&2
      die "PR $pr: requested reviewers lookup failed"
    fi
    if [ -n "$out" ]; then
      printf '%s\n' "$out" | jq -c 'select(.type == "User") | {login, type}' >> "$acc"
    fi
  done
  jq -s --arg exclude "$exclude" '
    map(select(.type == "User"))
    | map(. + {key: (.login | ascii_downcase)})
    | if $exclude != "" then map(select(.key != ($exclude | ascii_downcase))) else . end
    | unique_by(.key)
    | sort_by(.key)
    | map(.login)
  ' "$acc"
}

png_ok() {
  local f=$1
  [ -s "$f" ] || return 1
  local sig
  sig=$(od -An -t x1 -N 8 "$f" | tr -d ' \n')
  [ "$sig" = "89504e470d0a1a0a" ]
}

cmd_render() {
  [ $# -gt 0 ] || die "usage: pr-diagrams.sh render <file.drawio>..."
  local converter=${DRAWIO_CONVERTER:-}
  if [ -z "$converter" ]; then
    command -v drawio >/dev/null 2>&1 || die "drawio CLI not found"
    converter=$(cd "$(dirname "$0")" && pwd)/../../draw-io/scripts/convert-drawio-to-png.sh
  fi
  local seen="" f base
  for f in "$@"; do
    base=$(basename "$f")
    case " $seen " in
      *" $base "*) die "duplicate basename $base: $*" ;;
    esac
    seen="$seen $base"
  done
  local scratch
  scratch=$(mktemp -d); TMPS+=("$scratch")
  git -C "$scratch" init -q
  local inputs=() src
  for f in "$@"; do
    src=$scratch/$(basename "$f")
    cp "$f" "$src"
    inputs+=("$src")
  done
  local conv_err
  conv_err=$(mktemp); TMPS+=("$conv_err")
  if ! (cd "$scratch" && bash "$converter" "${inputs[@]}") >"$conv_err" 2>&1; then
    echo "pr-diagrams: converter failed" >&2
    cat "$conv_err" >&2
    exit 1
  fi
  local missing=0 f png
  for f in "$@"; do
    png=$scratch/$(basename "$f" .drawio).drawio.png
    if ! png_ok "$png"; then
      echo "pr-diagrams: $f: no valid PNG (missing, empty, or not a PNG)" >&2
      missing=1
    fi
  done
  if [ "$missing" -ne 0 ]; then
    cat "$conv_err" >&2
    exit 1
  fi
  local manifest
  manifest=$(mktemp); TMPS+=("$manifest")
  : > "$manifest"
  local f png dest
  for f in "$@"; do
    png=$scratch/$(basename "$f" .drawio).drawio.png
    dest=$(dirname "$f")/$(basename "$png")
    cp "$png" "$dest"
    jq -nc --arg drawio "$f" --arg png "$dest" '{drawio: $drawio, png: $png}' >> "$manifest"
  done
  jq -s '.' "$manifest"
}

main() {
  local cmd=${1:-}
  [ $# -gt 0 ] && shift
  case "$cmd" in
    repo) repo_of ;;
    related) cmd_related "$@" ;;
    reviewers) cmd_reviewers "$@" ;;
    render) cmd_render "$@" ;;
    *) die "usage: pr-diagrams.sh repo|related|reviewers|render ..." ;;
  esac
}

main "$@"
