#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HELPER="$ROOT/.github/audit/eval-status.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# expect LABEL LEFT RIGHT WANT_STATUS WANT_STDOUT
expect() {
  local label=$1 left=$2 right=$3 want_status=$4 want_output=$5
  local status output
  set +e
  output=$(bash "$HELPER" "$left" "$right" 2>"$TMP/err")
  status=$?
  set -e
  if [ "$status" -ne "$want_status" ]; then
    printf '%s: expected exit %d, got %d (stderr: %s)\n' "$label" "$want_status" "$status" "$(cat "$TMP/err")" >&2
    exit 1
  fi
  if [ "$output" != "$want_output" ]; then
    printf '%s: expected stdout %q, got %q\n' "$label" "$want_output" "$output" >&2
    exit 1
  fi
}

expect 'both clean' 0 0 0 'quality_failed=false'
expect 'first leg quality failure' 1 0 0 'quality_failed=true'
expect 'second leg quality failure' 0 1 0 'quality_failed=true'
expect 'both legs quality failure' 1 1 0 'quality_failed=true'

expect 'first leg harness error' 2 0 2 ''
expect 'second leg harness error' 0 2 2 ''
expect 'both legs harness error' 2 2 2 ''

expect 'first leg crash' 3 0 3 ''
expect 'second leg command not found' 0 127 127 ''
expect 'first leg killed' 137 0 137 ''
expect 'crash dominates quality failure' 137 1 137 ''
expect 'permission failure' 126 0 126 ''
expect 'harness error dominates crash' 2 139 2 ''

# Bad invocations fail loudly instead of guessing.
set +e
bash "$HELPER" >/dev/null 2>&1; [ $? -ne 0 ] || { echo 'missing args unexpectedly succeeded' >&2; exit 1; }
bash "$HELPER" 0 >/dev/null 2>&1; [ $? -ne 0 ] || { echo 'one arg unexpectedly succeeded' >&2; exit 1; }
bash "$HELPER" x 0 >/dev/null 2>&1; [ $? -ne 0 ] || { echo 'non-numeric arg unexpectedly succeeded' >&2; exit 1; }
set -e

# The workflow must delegate the combining decision to this helper and no longer
# treat unknown statuses as success.
WF="$ROOT/.github/workflows/skill-audit.yaml"
grep -Fq '.github/audit/eval-status.sh' "$WF" || { echo 'workflow does not call eval-status.sh' >&2; exit 1; }
if grep -qE "quality_failed=true' >> \"\\\$GITHUB_OUTPUT\"" "$WF"; then
  echo 'workflow still inlines quality_failed handling' >&2
  exit 1
fi

printf 'PASS eval exit-code combining tolerates only 0 and 1, fails on 2 and crashes\n'
