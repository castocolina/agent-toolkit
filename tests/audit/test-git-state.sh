#!/usr/bin/env bash
# Tamper regression for git-state.sh: any change to the git configuration a
# model could use to hide edits or run code (config, excludes, attributes,
# hooks, index) must fail verification. Runs entirely in a scratch repository.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
STATE="$ROOT/.github/audit/git-state.sh"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
REPO="$T/repo"
git init -q "$REPO"
cd "$REPO"
printf 'x\n' > tracked.txt
git add tracked.txt
mkdir -p .git/hooks
printf '#!/bin/sh\n' > .git/hooks/pre-commit.sample

expect_ok() {
  bash "$STATE" verify "$T/snap" || { echo "verify rejected an unchanged state: $1" >&2; exit 1; }
}
expect_tamper() {
  local mode=${2:-verify}
  if bash "$STATE" "$mode" "$T/snap" 2>"$T/err"; then
    echo "$mode accepted a tampered state: $1" >&2
    exit 1
  fi
  grep -q 'changed since the trusted snapshot' "$T/err" || { echo "no tamper message for: $1" >&2; cat "$T/err" >&2; exit 1; }
}
fresh_snapshot() {
  bash "$STATE" snapshot "$T/snap"
}

fresh_snapshot
expect_ok 'untouched repository'
bash "$STATE" verify-files "$T/snap" || { echo 'verify-files rejected an unchanged state' >&2; exit 1; }

printf '[alias]\n\tx = !sh -c evil\n' >> .git/config
expect_tamper '.git/config edited'
expect_tamper '.git/config edited (verify-files)' verify-files
fresh_snapshot

printf 'skills/x/\n' >> .git/info/exclude
expect_tamper '.git/info/exclude extended to hide model edits'
fresh_snapshot

printf '[core]\n\tattributesfile = /tmp/x\n' > .git/info/attributes
expect_tamper '.git/info/attributes created'
fresh_snapshot

printf '#!/bin/sh\nexit 0\n' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
expect_tamper 'hook planted'
fresh_snapshot

rm .git/hooks/pre-commit.sample
expect_tamper 'sample hook removed'
fresh_snapshot

rm .git/config
ln -s /dev/null .git/config
expect_tamper '.git/config replaced by a symlink'
rm .git/config
printf '[core]\n\trepositoryformatversion = 0\n' > .git/config
fresh_snapshot

# A forged index entry (a model write to .git/index) is caught by verify, not by
# the file comparison alone.
printf 'changed\n' > tracked.txt
git add tracked.txt
fresh_snapshot
git update-index --cacheinfo 100644,"$(git hash-object -w /dev/null)",tracked.txt
expect_tamper 'index entry forged'
fresh_snapshot

# Index flags that hide a worktree edit from git status are tampering as well.
fresh_snapshot
git update-index --assume-unchanged tracked.txt
expect_tamper 'assume-unchanged flag set'
git update-index --no-assume-unchanged tracked.txt
fresh_snapshot
git update-index --skip-worktree tracked.txt
expect_tamper 'skip-worktree flag set'
git update-index --no-skip-worktree tracked.txt
fresh_snapshot

if bash "$STATE" verify "$T/missing" 2>/dev/null; then
  echo 'verify without a snapshot unexpectedly succeeded' >&2
  exit 1
fi
if bash "$STATE" bogus "$T/snap" 2>/dev/null; then
  echo 'unknown subcommand unexpectedly succeeded' >&2
  exit 1
fi

printf 'PASS git-state detects tampering with config, excludes, attributes, hooks and the index\n'
