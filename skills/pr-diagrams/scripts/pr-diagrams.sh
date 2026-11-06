#!/bin/bash
# Render draw.io PR diagrams and look up promotion sources and reviewers.
# Status goes to stderr. stdout is JSON only, and empty on failure.
set -euo pipefail

GH=${GH:-gh}
TMPS=()
WT=""
cleanup() {
  [ -z "$WT" ] || git worktree remove --force "$WT" >/dev/null 2>&1 || true
  [ ${#TMPS[@]} -gt 0 ] && rm -rf "${TMPS[@]}"
  return 0
}
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
  path=${path%/}
  path=${path%.git}
  if [[ "$path" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$ ]]; then
    printf '%s\n' "$path"
  else
    die "origin is not a GitHub URL: $url"
  fi
}

cmd_related() {
  local base="" head="" exclude=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --exclude-pr)
        shift
        [ $# -gt 0 ] || die "--exclude-pr requires a value"
        exclude=$1
        ;;
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
  if ! git fetch origin "+refs/heads/$base:refs/remotes/origin/$base" "+refs/heads/$head:refs/remotes/origin/$head" >"$fetch_err" 2>&1; then
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
    if ! out=$("$GH" api --paginate --jq '.[]' "repos/$repo/commits/$sha/pulls" 2>"$err"); then
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
      --exclude)
        shift
        [ $# -gt 0 ] || die "--exclude requires a value"
        exclude=$1
        ;;
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
  local pr out err
  for pr in "${prs[@]}"; do
    err=$(mktemp); TMPS+=("$err")
    if ! out=$("$GH" api --paginate --jq '.[]' "repos/$repo/pulls/$pr/reviews" 2>"$err"); then
      cat "$err" >&2
      die "PR $pr: reviews lookup failed"
    fi
    printf '%s\n' "$out" | jq -c 'select(.user != null and .user.type == "User") | {login: .user.login, type: .user.type}' >> "$acc"
    err=$(mktemp); TMPS+=("$err")
    if ! out=$("$GH" api --jq '.users[]' "repos/$repo/pulls/$pr/requested_reviewers" 2>"$err"); then
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
  local seen=() f base i n
  for f in "$@"; do
    base=$(basename "$f")
    n=${#seen[@]}
    for ((i = 0; i < n; i++)); do
      [ "${seen[i]}" = "$base" ] && die "duplicate basename $base: $*"
    done
    seen+=("$base")
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
  local f png dest dest_dir tmp
  for f in "$@"; do
    png=$scratch/$(basename "$f" .drawio).drawio.png
    dest_dir=$(dirname "$f")
    dest=$dest_dir/$(basename "$png")
    # Never write through an existing destination symlink: refuse instead of
    # following it, and copy through a temp file in the destination directory
    # so the final rename replaces the entry itself.
    if [ -L "$dest" ]; then
      die "refusing to overwrite a symlinked destination: $dest"
    fi
    tmp=$(mktemp "$dest_dir/.pr-diagrams.XXXXXX") || die "cannot create a temp file in $dest_dir"
    cp "$png" "$tmp"
    chmod 644 "$tmp"
    mv -f "$tmp" "$dest"
    jq -nc --arg drawio "$f" --arg png "$dest" '{drawio: $drawio, png: $png}' >> "$manifest"
  done
  jq -s '.' "$manifest"
}

usage_err() { echo "pr-diagrams: $*" >&2; exit 2; }

# Host of a URL per the host rule: text after scheme:// up to the first /, lowercased.
url_host() {
  local u=$1 rest
  case "$u" in *://*) ;; *) return 0 ;; esac
  rest=${u#*://}
  printf '%s\n' "${rest%%/*}" | tr '[:upper:]' '[:lower:]'
}

# Sets O_HOST (lowercased), O_PATH (<owner>/<repo> of origin) and O_ARG (what to hand gh repo view). Fails if origin is unparsable.
# The test hook may carry a host as <host>/<owner>/<repo>; without one the host is not compared.
# shortcut: a URL with a port or a nested group path is taken verbatim, upgrade if such a host appears.
origin_target() {
  local url rest host path
  O_HOST=""; O_PATH=""; O_ARG=""
  if [ -n "${PR_DIAGRAMS_REPO:-}" ] && [ -n "${GH:-}" ] && [ "$GH" != "gh" ]; then
    O_PATH=$PR_DIAGRAMS_REPO; O_ARG=$PR_DIAGRAMS_REPO
    if [[ "$O_PATH" == */*/* ]]; then O_HOST=${O_PATH%%/*}; O_HOST=${O_HOST,,}; O_PATH=${O_PATH#*/}; fi
    return 0
  fi
  url=$(git remote get-url origin 2>/dev/null) || return 1
  case "$url" in
    *://*) rest=${url#*://}; rest=${rest#*@}; host=${rest%%/*}; path=${rest#*/} ;;
    *@*:*) rest=${url#*@}; host=${rest%%:*}; path=${rest#*:} ;;
    *) return 1 ;;
  esac
  path=${path%/}; path=${path%.git}
  [ -n "$host" ] && [[ "$path" == */* ]] || return 1
  O_HOST=${host,,}; O_PATH=$path; O_ARG=https://$host/$path
}

cmd_capability() {
  [ $# -eq 0 ] || usage_err "usage: pr-diagrams.sh capability"
  case "${PR_DIAGRAMS_MODE:-}" in
    attach|branch) printf '%s\n' "$PR_DIAGRAMS_MODE"; return 0 ;;
    "") ;;
    *) usage_err "PR_DIAGRAMS_MODE must be attach or branch, got: $PR_DIAGRAMS_MODE" ;;
  esac
  local t=${PR_DIAGRAMS_PROBE_TIMEOUT:-10} out rc=0 ver url host bound=()
  if command -v timeout >/dev/null 2>&1; then bound=(timeout -k 1 "$t")
  elif command -v gtimeout >/dev/null 2>&1; then bound=(gtimeout -k 1 "$t")
  # shortcut: with no timeout/gtimeout a hung gh hangs capability; add a portable bound if that is ever reported.
  else echo "pr-diagrams: timeout(1) not found (nor gtimeout), running gh probes unbounded" >&2
  fi
  out=$(${bound[@]+"${bound[@]}"} "$GH" --version 2>/dev/null) || rc=$?
  if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then echo "pr-diagrams: gh --version timed out after ${t}s, using branch" >&2; echo branch; return 0; fi
  if [ "$rc" -ne 0 ]; then echo "pr-diagrams: gh --version failed, using branch" >&2; echo branch; return 0; fi
  ver=$(printf '%s\n' "$out" | head -n 1)
  if [[ ! "$ver" =~ ^gh\ version\ ([0-9]+)\.([0-9]+) ]]; then
    echo "pr-diagrams: cannot parse gh version [$ver], using branch" >&2; echo branch; return 0
  fi
  if [ "${BASH_REMATCH[1]}" -lt 2 ] || { [ "${BASH_REMATCH[1]}" -eq 2 ] && [ "${BASH_REMATCH[2]}" -lt 101 ]; }; then
    echo "pr-diagrams: gh ${BASH_REMATCH[1]}.${BASH_REMATCH[2]} has no --attach, using branch" >&2; echo branch; return 0
  fi
  rc=0
  origin_target || O_ARG=""  # no parsable origin: fall back to gh's own repository
  url=$(${bound[@]+"${bound[@]}"} "$GH" repo view ${O_ARG:+"$O_ARG"} --json url --jq .url 2>/dev/null) || rc=$?
  if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then echo "pr-diagrams: gh repo view timed out after ${t}s, using branch" >&2; echo branch; return 0; fi
  if [ "$rc" -ne 0 ]; then echo "pr-diagrams: gh repo view failed, using branch" >&2; echo branch; return 0; fi
  host=$(url_host "$url")
  if [ -z "$host" ]; then echo "pr-diagrams: no host in repository URL [$url], using branch" >&2; echo branch; return 0; fi
  if [ "$host" = github.com ]; then echo attach; else echo "pr-diagrams: host $host is not github.com, using branch" >&2; echo branch; fi
}

# Build one commit of <N>/<basename> files on top of $1 (empty = orphan) in worktree $WT.
publish_commit() {
  local parent=$1 n=$2 f tree commit; shift 2
  if [ -n "$parent" ]; then git -C "$WT" read-tree "$parent"; else git -C "$WT" read-tree --empty; fi
  mkdir -p "$WT/$n"  # keep images published earlier for this PR; only the given basenames are replaced
  # The worktree is --no-checkout, so add each file by path: -A would drop earlier ones from the index.
  for f in "$@"; do cp "$f" "$WT/$n/$(basename "$f")"; git -C "$WT" add -- "$n/$(basename "$f")"; done
  tree=$(git -C "$WT" write-tree)
  if [ -n "$parent" ]; then commit=$(git -C "$WT" commit-tree "$tree" -p "$parent" -m "docs: diagrams for PR $n")
  else commit=$(git -C "$WT" commit-tree "$tree" -m "docs: diagrams for PR $n"); fi
  git -C "$WT" update-ref HEAD "$commit"
}

cmd_publish() {
  [ $# -ge 2 ] || usage_err "usage: pr-diagrams.sh publish <N> <png>..."
  local n=$1 f base i seen=(); shift
  [[ "$n" =~ ^[0-9]+$ ]] || usage_err "PR number must be digits only: $n"
  for f in "$@"; do
    base=$(basename "$f")
    case "$base" in .|..) usage_err "bad PNG path: $f" ;; esac
    if [ ! -f "$f" ] || ! png_ok "$f"; then usage_err "not a PNG file: $f"; fi
    for ((i = 0; i < ${#seen[@]}; i++)); do
      [ "${seen[i]}" = "$base" ] && usage_err "duplicate basename $base"
    done
    seen+=("$base")
  done
  local stray
  stray=$( { git for-each-ref --format='%(refname:short)' 'refs/heads/pr-diagrams-*' 'refs/heads/pr-diagrams/*'
             git ls-remote --heads origin 'pr-diagrams-*' 'pr-diagrams/*' | sed 's|.*refs/heads/||'; } | tr '\n' ' ')
  [ -z "$stray" ] || usage_err "stray branch(es), only 'pr-diagrams' is allowed: $stray"
  local rurl
  origin_target || usage_err "cannot determine origin's repository from its URL"
  rurl=$("$GH" repo view "$O_ARG" --json url --jq .url) || die "gh repo view failed"
  rurl=${rurl%/}
  local gpath=${rurl#*://} ghost; ghost=$(url_host "$rurl"); gpath=${gpath#*/}
  if [ "${gpath,,}" != "${O_PATH,,}" ] || { [ -n "$O_HOST" ] && [ "$ghost" != "$O_HOST" ]; }; then
    usage_err "gh resolves ${ghost:+$ghost/}$gpath but origin is ${O_HOST:+$O_HOST/}$O_PATH; refusing to publish"
  fi
  local dir parent="" attempt
  dir=$(mktemp -d); TMPS+=("$dir")
  git worktree add -q --detach --no-checkout "$dir/wt" HEAD || die "cannot create worktree"
  WT=$dir/wt
  for attempt in 1 2; do
    if [ -n "$(git ls-remote --heads origin refs/heads/pr-diagrams)" ]; then
      git fetch -q origin refs/heads/pr-diagrams || die "fetch of pr-diagrams failed"
      parent=$(git rev-parse FETCH_HEAD)
    fi
    publish_commit "$parent" "$n" "$@"
    if git -C "$WT" push -q origin HEAD:refs/heads/pr-diagrams; then break; fi
    [ "$attempt" -eq 1 ] || die "push of pr-diagrams failed after retry"
    echo "pr-diagrams: push rejected, fetching and retrying once" >&2
  done
  for f in "$@"; do
    base=$(basename "$f")
    jq -nc --arg png "$f" --arg url "$rurl/blob/pr-diagrams/$n/$(jq -rn --arg s "$base" '$s|@uri')?raw=true" '{png: $png, url: $url}'
  done
}

cmd_help() {
  printf '%s\n' \
    'usage: pr-diagrams.sh <subcommand> [args]' \
    '' \
    '  capability                              print attach or branch, always exit 0' \
    '  render <file.drawio>...                 stdout [{"drawio","png"}]; each PNG embeds its diagram, next to its source' \
    '  publish <N> <png>...                    commit <N>/<name> on branch pr-diagrams; stdout one {"png","url"} line per file' \
    '  related <base> <head> [--exclude-pr N]  stdout [{"pr","title","head_ref","base_ref","merged_at"}], merged PRs, newest first' \
    '  reviewers <PR>... [--exclude LOGIN]     stdout sorted JSON array of human reviewer logins' \
    '  repo                                    stdout <owner>/<repo> parsed from origin' \
    '  help | --help | -h                      this text' \
    '' \
    'env: GH (gh binary), DRAWIO_CONVERTER (converter script), PR_DIAGRAMS_MODE=attach|branch (forces capability),' \
    '     PR_DIAGRAMS_PROBE_TIMEOUT (capability probe seconds, default 10)' \
    'exit: 0 ok; 1 failure (gh, git or converter error, bad arguments to repo/related/reviewers/render, unknown subcommand);' \
    '      2 usage error of capability or publish, or a publish refusal (stray branch, gh and origin name different repositories)' \
    'Status goes to stderr; stdout is empty on any failure.'
}

main() {
  local cmd=${1:-}
  [ $# -gt 0 ] && shift
  case "$cmd" in
    help|--help|-h) cmd_help ;;
    repo) repo_of ;;
    related) cmd_related "$@" ;;
    reviewers) cmd_reviewers "$@" ;;
    render) cmd_render "$@" ;;
    capability) cmd_capability "$@" ;;
    publish) cmd_publish "$@" ;;
    *) die "usage: pr-diagrams.sh repo|related|reviewers|render|capability|publish|help ..." ;;
  esac
}

main "$@"
