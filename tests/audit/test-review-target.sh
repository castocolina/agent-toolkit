#!/usr/bin/env bash
# Runtime tests of the review workflow's target job. The resolve step is taken
# out of .github/workflows/skill-audit-review.yaml and run against a stub gh, so
# the validations the brief requires (closed, unlabeled, fork head, stale head,
# dispatch on the live head, skipped model) are checked as behaviour, not text.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WF="$ROOT/.github/workflows/skill-audit-review.yaml"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"

cat > "$TMP/bin/gh" <<'STUB'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$GH_LOG"
# GH_FAIL_REMOVE makes every --remove-label call fail (a transient API error, not a missing label).
if [[ -n "${GH_FAIL_REMOVE:-}" && "$*" == *--remove-label* ]]; then
  echo "stub failure: $*" >&2
  exit 1
fi
case "$*" in
  "pr view "*) cat "${LIVE_JSON:-$PR_JSON}" ;;
  "api repos/"*) echo main ;;
  *) exit 0 ;;
esac
STUB
chmod +x "$TMP/bin/gh"

# Extract the resolve step's shell body from the workflow (ten spaces of indent removed).
python3 - "$WF" "$TMP/resolve.sh" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(
    r"      - name: Resolve and validate the audit pull request\n        id: resolve\n        run: \|\n"
    r"((?:          .*\n|\n)+?)(?=      - |  review:)",
    text,
)
if not match:
    raise SystemExit("resolve step not found in the review workflow")
lines = [line[10:] if line.startswith("          ") else line for line in match.group(1).splitlines()]
Path(sys.argv[2]).write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

HEAD=0123456789abcdef0123456789abcdef01234567
OPEN="{\"state\":\"OPEN\",\"labels\":[{\"name\":\"skill-audit\"}],\"headRefOid\":\"$HEAD\",\"baseRefOid\":\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"headRepositoryOwner\":{\"login\":\"acme\"},\"isCrossRepository\":false}"

# run_resolve PR_JSON CALLER_HEAD EVENT MODEL: runs the step; its exit code is returned.
run_resolve() {
  printf '%s\n' "$1" > "$TMP/pr.json"
  : > "$TMP/gh.log"
  : > "$TMP/out"
  local rc=0
  PATH="$TMP/bin:$PATH" GH_LOG="$TMP/gh.log" PR_JSON="$TMP/pr.json" GH_REPO=acme/repo PR_NUMBER=42 \
    CALLER_HEAD="$2" GITHUB_EVENT_NAME="$3" AUDIT_REVIEW_MODEL="$4" GITHUB_OUTPUT="$TMP/out" RUNNER_TEMP="$TMP" \
    bash "$TMP/resolve.sh" >"$TMP/stdout" 2>"$TMP/stderr" || rc=$?
  return "$rc"
}

expect_rc() {
  local label=$1 want=$2
  shift 2
  local rc=0
  "$@" || rc=$?
  if [[ "$rc" != "$want" ]]; then
    printf 'FAIL %s: exited %s, expected %s (stderr: %s)\n' "$label" "$rc" "$want" "$(cat "$TMP/stderr")" >&2
    exit 1
  fi
  printf 'PASS %s\n' "$label"
}

# Inside a reusable workflow GITHUB_EVENT_NAME is the CALLER's event (schedule or workflow_dispatch),
# never workflow_call. A called run is therefore identified by a non-empty CALLER_HEAD (inputs.head_sha).
expect_rc "a valid open audit PR resolves when called" 0 run_resolve "$OPEN" "$HEAD" schedule m
grep -q "head_sha=$HEAD" "$TMP/out" || { echo "FAIL outputs head_sha" >&2; exit 1; }

expect_rc "a closed PR is rejected" 1 run_resolve "${OPEN/OPEN/CLOSED}" "$HEAD" schedule m
expect_rc "an unlabeled PR is rejected" 1 run_resolve "${OPEN/\"skill-audit\"/\"other\"}" "$HEAD" schedule m
expect_rc "a fork head is rejected" 1 run_resolve "${OPEN/\"isCrossRepository\":false/\"isCrossRepository\":true}" "$HEAD" schedule m

expect_rc "a stale head_sha on a called run is rejected" 1 run_resolve "$OPEN" ffffffffffffffffffffffffffffffffffffffff schedule m
grep -q "is not the live head" "$TMP/stderr" || { echo "FAIL stale head rejected for the wrong reason" >&2; exit 1; }
echo "PASS the stale head is rejected for the right reason"

# A dispatch passes no head_sha input, so CALLER_HEAD is empty and the live head is resolved.
expect_rc "a dispatch resolves the live head" 0 run_resolve "$OPEN" "" workflow_dispatch m
grep -q "head_sha=$HEAD" "$TMP/out" || { echo "FAIL dispatch did not resolve the live head" >&2; exit 1; }

expect_rc "an empty model is skipped and labeled" 0 run_resolve "$OPEN" "$HEAD" schedule ""
grep -q 'add-label audit-review:skipped' "$TMP/gh.log" || { echo "FAIL the skipped path does not label audit-review:skipped" >&2; exit 1; }
grep -q 'model_empty=true' "$TMP/out" || { echo "FAIL the skipped path does not set model_empty" >&2; exit 1; }

# The skipped path removes only the audit-review:* labels the PR carries, and any remove failure fails the step.
WITH_POSITIVE=$(python3 -c 'import json, sys; pr = json.loads(sys.argv[1]); pr["labels"].append({"name": "audit-review:positive"}); print(json.dumps(pr))' "$OPEN")
expect_rc "the skipped path removes a carried audit-review label" 0 run_resolve "$WITH_POSITIVE" "$HEAD" schedule ""
grep -q 'pr edit 42 --remove-label audit-review:positive' "$TMP/gh.log" || { echo "FAIL the carried positive label was not removed" >&2; exit 1; }
if grep -q -- '--remove-label audit-review:changes' "$TMP/gh.log"; then echo "FAIL an absent label was removed" >&2; exit 1; fi
echo "PASS the skipped path removes only the labels the PR carries"

export GH_FAIL_REMOVE=1
expect_rc "a failed label removal fails the skipped path" 1 run_resolve "$WITH_POSITIVE" "$HEAD" schedule ""
if grep -q 'add-label audit-review:skipped' "$TMP/gh.log"; then echo "FAIL the skipped label was added after a failed removal" >&2; exit 1; fi
# A removal that fails only because the label vanished in the meantime is tolerated: the fresh read no longer has it.
export LIVE_JSON="$TMP/live.json"
printf '%s\n' "$OPEN" > "$LIVE_JSON"
expect_rc "a removal of a label already gone is tolerated" 0 run_resolve "$WITH_POSITIVE" "$HEAD" schedule ""
grep -q 'add-label audit-review:skipped' "$TMP/gh.log" || { echo "FAIL the skipped label was not added after a tolerated removal" >&2; exit 1; }
unset LIVE_JSON GH_FAIL_REMOVE

echo 'PASS test-review-target.sh'
