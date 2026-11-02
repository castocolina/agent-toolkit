#!/bin/bash
# Pin the Claude Code docs pages that define commands and agents (url + sha256 only,
# never a copy of the pages). stdout: one JSON object; status/errors: stderr.
set -euo pipefail

usage() {
  cat <<'USAGE'
usage: fetch-claude-specs.sh [--dest DIR] [--profiles DIR] [--base URL] [--keep] [-h|--help]

Download the Claude Code pages skills, sub-agents and plugins-reference into a
temporary directory outside every checkout of this repository, hash them and
update DEST/SOURCE.json (default skills/skill-judge/references/claude-code).
Run from the repo root. Normally run with no options.

Options:
  --dest DIR      directory holding SOURCE.json (tests only)
  --profiles DIR  judge profiles to compare with the digests (default DEST/../profiles)
  --base URL      page base URL (default https://code.claude.com/docs/en)
  --keep          keep the downloaded pages and print their directory as "kept"

stdout: one JSON object with these fields
  changed          pages whose sha256 differs from the pin (all of them on a first run)
  unchanged        pages that match the pin
  digests          per-kind digest: command (skills, plugins-reference), agent (sub-agents, plugins-reference)
  profiles_stale   kinds whose profile source_digest differs from digests[kind]
  kept             only with --keep
SOURCE.json is rewritten only when a page hash changed (fetched_at moves with it).
The raw pages are Claude Code documentation without a license grant: never commit them.

Exit codes: 0 success; 1 any failure (the previous SOURCE.json survives); 2 bad usage.
USAGE
}

DEST=skills/skill-judge/references/claude-code
PROFILES=
BASE=https://code.claude.com/docs/en
KEEP=false
DEST_SET=false
while [ $# -gt 0 ]; do
  case $1 in
    --dest) [ $# -ge 2 ] || { usage >&2; exit 2; }; DEST=$2; DEST_SET=true; shift 2 ;;
    --profiles) [ $# -ge 2 ] || { usage >&2; exit 2; }; PROFILES=$2; shift 2 ;;
    --base) [ $# -ge 2 ] || { usage >&2; exit 2; }; BASE=${2%/}; shift 2 ;;
    --keep) KEEP=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done
if ! $DEST_SET; then # the default is cwd-relative: refuse to write a fresh tree elsewhere
  [ -f scripts/build_plugins.py ] || { echo "fetch-claude-specs: run from the repo root (or pass --dest)" >&2; exit 1; }
fi
PROFILES=${PROFILES:-$DEST/../profiles}

die() { echo "fetch-claude-specs: $*" >&2; exit 1; }
PAGES=(skills sub-agents plugins-reference)
PIN=$DEST/SOURCE.json

TMP=$(mktemp -d)
NEWPIN= BACKUP= PUBLISHED=false DONE=false KEEP_BACKUP=false
restore_pin() { # undo a published pin that was never reported
  $PUBLISHED && ! $DONE || return 0
  if [ -z "$BACKUP" ]; then rm -f "$PIN"; echo "fetch-claude-specs: removed the unreported new pin" >&2
  elif mv -f "$BACKUP" "$PIN"; then BACKUP=; echo "fetch-claude-specs: restored previous pin" >&2
  else KEEP_BACKUP=true; echo "fetch-claude-specs: restore failed; old pin is kept at $BACKUP" >&2; fi
}
on_exit() {
  trap '' INT TERM
  restore_pin
  rm -f "$NEWPIN"; $KEEP_BACKUP || rm -f ${BACKUP:+"$BACKUP"}
  if $KEEP && $DONE; then return; fi
  rm -rf "$TMP"
}
trap on_exit EXIT
trap 'echo "fetch-claude-specs: interrupted" >&2; exit 1' INT TERM

# The raw pages must never land inside any worktree or the main checkout of this repo.
REAL=$(realpath "$TMP")
TOP=$(realpath "$(git rev-parse --show-toplevel)") || die "not inside a git repository"
MAIN=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
ROOTS=("$TOP" "$(realpath "$MAIN")")
git worktree list --porcelain -z > "$TMP/worktrees" || die "cannot list worktrees"
mapfile -d '' -t WTREC < "$TMP/worktrees"
for rec in "${WTREC[@]}"; do
  [[ $rec == "worktree "* && -d ${rec#worktree } ]] && ROOTS+=("$(realpath "${rec#worktree }")")
done
rm -f "$TMP/worktrees"
for root in "${ROOTS[@]}"; do
  case $REAL/ in "$root"/*) die "temp directory $REAL is inside the repository $root; set TMPDIR elsewhere" ;; esac
done

for page in "${PAGES[@]}"; do
  f=$TMP/$page.md
  echo "fetching $BASE/$page.md" >&2
  curl -fsSL --max-time 60 --retry 2 "$BASE/$page.md" -o "$f" || die "download failed: $BASE/$page.md"
  first=$(grep -m1 -v '^[[:space:]]*$' "$f" || true)
  [ -n "$first" ] || die "empty page: $page"
  shopt -s nocasematch
  first=${first#"${first%%[![:space:]]*}"}
  [[ $first == "<!doctype"* || $first == "<html"* ]] && die "page is HTML, not Markdown: $page"
  shopt -u nocasematch
done

declare -A HASH
for page in "${PAGES[@]}"; do HASH[$page]=$(sha256sum < "$TMP/$page.md" | cut -d' ' -f1); done
digest() { # digest PAGE...
  local p
  for p in "$@"; do printf '%s %s\n' "$p" "${HASH[$p]}"; done | LC_ALL=C sort | sha256sum | cut -d' ' -f1
}
DIG_COMMAND=$(digest skills plugins-reference)
DIG_AGENT=$(digest sub-agents plugins-reference)

CHANGED=() UNCHANGED=()
for page in "${PAGES[@]}"; do
  old=$(jq -r --arg p "$page" '.pages[$p].sha256 // empty' "$PIN" 2>/dev/null || true)
  if [ "$old" = "${HASH[$page]}" ]; then UNCHANGED+=("$page"); else CHANGED+=("$page"); fi
done

WRITE=false
{ [ ${#CHANGED[@]} -gt 0 ] || [ ! -f "$PIN" ]; } && WRITE=true
if $WRITE; then
  pages_json='{}'
  for page in "${PAGES[@]}"; do
    pages_json=$(jq -c --arg p "$page" --arg u "$BASE/$page.md" --arg h "${HASH[$page]}" '.[$p] = {url: $u, sha256: $h}' <<<"$pages_json")
  done
  mkdir -p "$DEST"
  NEWPIN=$(mktemp "$DEST/.SOURCE.XXXXXX")
  jq -n --arg base "$BASE" --arg at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --argjson pages "$pages_json" \
    --arg c "$DIG_COMMAND" --arg a "$DIG_AGENT" \
    '{base: $base, fetched_at: $at, pages: $pages, digests: {command: $c, agent: $a}}' > "$NEWPIN"
fi

STALE=()
for kind in command agent; do
  want=DIG_${kind^^}
  have=$(sed -n '2s/^source_digest: //p' "$PROFILES/$kind.md" 2>/dev/null || true)
  [ "$have" = "${!want}" ] || STALE+=("$kind")
done

arr() { if [ $# -eq 0 ]; then echo '[]'; else printf '%s\n' "$@" | jq -R . | jq -sc .; fi; }
KEPT=; $KEEP && KEPT=$REAL
RESULT=$(jq -n --argjson changed "$(arr "${CHANGED[@]}")" --argjson unchanged "$(arr "${UNCHANGED[@]}")" \
  --argjson stale "$(arr "${STALE[@]}")" --arg c "$DIG_COMMAND" --arg a "$DIG_AGENT" --arg kept "$KEPT" \
  '{changed: $changed, unchanged: $unchanged, digests: {command: $c, agent: $a}, profiles_stale: $stale}
   + (if $kept == "" then {} else {kept: $kept} end)')

# Publish last: the old pin comes back on any failure until the result is printed.
if $WRITE; then
  if [ -f "$PIN" ]; then BACKUP=$(mktemp "$DEST/.SOURCE.bak.XXXXXX"); cp -p "$PIN" "$BACKUP"; fi
  PUBLISHED=true
  mv "$NEWPIN" "$PIN"; NEWPIN=
  echo "wrote $PIN" >&2
else
  echo "pins unchanged" >&2
fi
printf '%s\n' "$RESULT"
DONE=true
