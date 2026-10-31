#!/usr/bin/env bash
# Snapshot and verify the git control state a model step could tamper with:
# .git/config, everything under .git/info (excludes, attributes) and .git/hooks.
# The index (.git/index entries) is covered by the `verify` mode only: a forged
# index would make edits look staged, which --skip-staged then ignores.
#
#   git-state.sh snapshot DIR     record the state into DIR (trusted step, before a model)
#   git-state.sh verify DIR       files AND index unchanged (right after a model step)
#   git-state.sh verify-files DIR files unchanged (before push; commit legitimately changes the index)
#
# Order matters: file state is compared BEFORE git runs at all, so a tampered
# .git/config can never make git execute code (core.fsmonitor, hooks, filters)
# before the check fails. The index is only read once the files match.
set -euo pipefail

usage() { echo "usage: git-state.sh snapshot|verify|verify-files DIR" >&2; exit 2; }
[ "$#" -eq 2 ] || usage
MODE=$1
DIR=$2
GIT_DIR=.git

if [ ! -d "$GIT_DIR" ] || [ -L "$GIT_DIR" ]; then
  echo "git-state: $GIT_DIR must be a real directory in the checkout" >&2
  exit 1
fi

# One line per path under .git: a sha256 for regular files, or the kind of
# entry for anything else. Missing entries are part of the state.
entry() {
  local rel=$1 path="$GIT_DIR/$1"
  if [ -L "$path" ]; then echo "symlink $rel"
  elif [ -f "$path" ]; then echo "file $(sha256sum "$path" | cut -d' ' -f1) $rel"
  elif [ -d "$path" ]; then echo "dir $rel"
  elif [ -e "$path" ]; then echo "other $rel"
  else echo "absent $rel"
  fi
}

file_state() {
  local dir rel
  entry config
  for dir in info hooks; do
    entry "$dir"
    if [ -d "$GIT_DIR/$dir" ] && [ ! -L "$GIT_DIR/$dir" ]; then
      find "$GIT_DIR/$dir" -mindepth 1 -printf '%P\n' | LC_ALL=C sort | while IFS= read -r rel; do
        entry "$dir/$rel"
      done
    fi
  done
}

# Runs git: only called after file_state matched. Under set -o pipefail a failing
# git makes the assignment fail, which stops the script (fail closed).
index_digest() {
  # Entries plus per-file index flags (assume-unchanged, skip-worktree): flipping a flag hides
  # a worktree edit from git status without touching the entry itself.
  { git ls-files --stage; git ls-files -v; } | sha256sum | cut -d' ' -f1
}

case "$MODE" in
  snapshot)
    mkdir -p "$DIR"
    file_state > "$DIR/files"
    index_digest > "$DIR/index" ;;
  verify|verify-files)
    [ -f "$DIR/files" ] && [ -f "$DIR/index" ] || { echo "git-state: no snapshot in $DIR" >&2; exit 1; }
    actual=$(file_state)
    if [ "$actual" != "$(cat "$DIR/files")" ]; then
      echo "git-state: .git config, info or hooks changed since the trusted snapshot" >&2
      diff "$DIR/files" <(printf '%s\n' "$actual") >&2 || true
      exit 1
    fi
    if [ "$MODE" = verify ]; then
      actual=$(index_digest)
      if [ "$actual" != "$(cat "$DIR/index")" ]; then
        echo "git-state: the git index changed since the trusted snapshot" >&2
        exit 1
      fi
    fi
    ;;
  *) usage ;;
esac
