#!/bin/bash
# Text checks (no YAML library) that the CI workflow triggers on PRs of any base.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
FILE=${1:-$ROOT/.github/workflows/main.yaml}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

fail=0

# block_match KEY RE FILE -> 0 if a line inside the `  KEY:` block (blank or indented 4+) matches RE.
# grep and awk only: CI runners lack rg.
block_match() {
  awk -v k="$1" -v re="$2" '
    $0 ~ "^  " k ":[ ]*$" { inb = 1; next }
    inb && /^(    .*)?$/ { if ($0 ~ re) found = 1; next }
    { inb = 0 }
    END { exit !found }' "$3"
}

# check_all FILE -> prints one line per failed check; returns 1 if any failed
check_all() {
  local f=$1 bad=0
  grep -q -E '^  pull_request:[ ]*$' "$f" || { echo "(1) pull_request must be block form"; bad=1; }
  if block_match pull_request '^    branches(-ignore)?:' "$f"; then
    echo "(2) pull_request must not filter branches"; bad=1
  fi
  block_match push '^    branches: [[]main[]]' "$f" || { echo "(3) push must stay on branches: [main]"; bad=1; }
  grep -q -E '^  workflow_dispatch:' "$f" || { echo "(4) workflow_dispatch missing"; bad=1; }
  return $bad
}

# expect LABEL FILE WANT(pass|fail)
expect() {
  local label=$1 f=$2 want=$3 out got=pass
  out=$(check_all "$f") || got=fail
  if [ "$got" = "$want" ]; then
    echo "PASS: $label" >&2
  else
    echo "FAIL: $label (wanted $want, got $got)" >&2
    [ -z "$out" ] || echo "$out" >&2
    fail=1
  fi
}

printf 'on:\n  push:\n    branches: [main]\n  pull_request:\n    branches: [main]\n' >"$TMP/old.yaml"
printf 'on:\n  push:\n    branches: [main]\n\n  pull_request:\n\n  workflow_dispatch:\n' >"$TMP/new.yaml"

expect 'fixture: branch-filtered pull_request is rejected' "$TMP/old.yaml" fail
expect 'fixture: unfiltered pull_request passes' "$TMP/new.yaml" pass
expect "$FILE" "$FILE" pass

exit $fail
