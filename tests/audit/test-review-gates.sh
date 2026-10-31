#!/usr/bin/env bash
# Offline tests for .github/audit/review-gates.sh: the CI and evals gates of the
# PR review. A stub gh answers the check-runs and commit-status reads; the poll
# clock is injected (REVIEW_CI_SLEEP, REVIEW_CI_MAX_POLLS) so no test waits.
# Gate codes: 0 pass, 1 fail, 2 needs-human (see review-combine.py).
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
GATES="$ROOT/.github/audit/review-gates.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"

# Stub gh: answers the two reads with fixtures chosen by env vars.
cat > "$TMP/bin/gh" <<'STUB'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$GH_LOG"
case "$*" in
  *"/check-runs"*)
    if [[ -n "${CHECK_RUNS_EXIT:-}" ]]; then exit "$CHECK_RUNS_EXIT"; fi
    # FLIP_FILE / FLIP_AFTER: serve the pending answer until the Nth call, then the completed one.
    src=$CHECK_RUNS_FILE
    if [[ -n "${FLIP_AFTER:-}" ]]; then
      calls=$(grep -c '/check-runs' "$GH_LOG")
      if (( calls > FLIP_AFTER )); then src=$FLIP_FILE; fi
    fi
    # The gate reads the raw pages (no --jq) and validates them itself, so the stub serves them as they are.
    cat "$src" ;;
  *"/statuses"*)
    if [[ -n "${STATUS_EXIT:-}" ]]; then exit "$STATUS_EXIT"; fi
    # The real call is gh api --paginate .../statuses --jq '.[]': one object per line.
    jq -c '.[]' "$STATUS_FILE" ;;
  *) echo "unexpected gh call: $*" >&2; exit 90 ;;
esac
STUB
chmod +x "$TMP/bin/gh"
export PATH="$TMP/bin:$PATH"
export GH_LOG="$TMP/gh.log" GH_TOKEN=test GH_REPO=acme/repo
export HEAD_SHA=0123456789abcdef0123456789abcdef01234567
export REVIEW_CI_SLEEP=0 REVIEW_CI_MAX_POLLS=3 EXPECTED_CHECKS_FILE="$TMP/expected.txt"
export CHECK_RUNS_FILE="$TMP/check-runs.txt" STATUS_FILE="$TMP/status.json"
printf 'Validate Plugin Structure\n' > "$EXPECTED_CHECKS_FILE"

fail() { printf 'FAIL %s\n' "$*" >&2; exit 1; }

# run_ci: runs only the CI gate and prints its exit code.
run_ci() {
  : > "$GH_LOG"
  bash "$GATES" ci > "$TMP/ci.out" 2> "$TMP/ci.err" || fail "ci gate exited non-zero: $(cat "$TMP/ci.err")"
  cat "$TMP/ci.out"
}

# A check-runs fixture is one raw page as the API returns it: {"total_count":N,"check_runs":[...]}.
# page reads one check object per line on stdin and wraps them into one raw page.
page() { jq -cn '[inputs] as $r | {total_count: ($r | length), check_runs: $r}'; }
run() { printf '{"name":"%s","status":"%s","conclusion":"%s"}\n' "$1" "$2" "$3" | page; }

# test_failed_check_run_is_changes: a failed expected check is a gate failure (1).
run "Validate Plugin Structure" completed failure > "$CHECK_RUNS_FILE"
got=$(run_ci)
[[ "$got" == 1 ]] || fail "failed check_run gave $got, expected 1"
echo "PASS test_failed_check_run_is_changes"

# cancelled and timed_out are gate failures too.
for conclusion in cancelled timed_out; do
  run "Validate Plugin Structure" completed "$conclusion" > "$CHECK_RUNS_FILE"
  got=$(run_ci)
  [[ "$got" == 1 ]] || fail "$conclusion gave $got, expected 1"
done
echo "PASS cancelled and timed_out check runs are changes"

# success, skipped and neutral pass.
for conclusion in success skipped neutral; do
  run "Validate Plugin Structure" completed "$conclusion" > "$CHECK_RUNS_FILE"
  got=$(run_ci)
  [[ "$got" == 0 ]] || fail "$conclusion gave $got, expected 0"
done
echo "PASS success, skipped and neutral pass"

# An empty expected-checks list (or a missing file) names nothing to wait for: needs-human, never a pass.
printf '\n\n' > "$EXPECTED_CHECKS_FILE"
run "Validate Plugin Structure" completed success > "$CHECK_RUNS_FILE"
got=$(run_ci)
[[ "$got" == 2 ]] || fail "expected-checks with no names gave $got, expected 2"
: > "$EXPECTED_CHECKS_FILE"
got=$(run_ci)
[[ "$got" == 2 ]] || fail "empty expected-checks file gave $got, expected 2"
EXPECTED_CHECKS_FILE="$TMP/missing.txt" run_ci >/dev/null 2>&1 || true
got=$(EXPECTED_CHECKS_FILE="$TMP/missing.txt" run_ci)
[[ "$got" == 2 ]] || fail "missing expected-checks file gave $got, expected 2"
printf 'Validate Plugin Structure\n' > "$EXPECTED_CHECKS_FILE"
echo "PASS an empty or missing expected-checks list is needs-human"

# An empty check_runs array is a real answer (no runs yet): the gate polls, then needs-human on the timeout.
# The stub's raw page is an object with a check_runs array; it is the empty object that must poll, not give up.
printf '{"total_count":0,"check_runs":[]}\n' > "$CHECK_RUNS_FILE"
: > "$GH_LOG"
got=$(run_ci)
[[ "$got" == 2 ]] || fail "empty check_runs array gave $got, expected 2 after polling"
[[ "$(grep -c '/check-runs' "$GH_LOG")" == 3 ]] || fail "empty check_runs array did not poll (got $(grep -c '/check-runs' "$GH_LOG") reads)"
# An empty body (no JSON at all) is unreadable: needs-human at once, not a wait.
: > "$CHECK_RUNS_FILE"
: > "$GH_LOG"
got=$(run_ci)
[[ "$got" == 2 ]] || fail "empty answer gave $got, expected 2"
[[ "$(grep -c '/check-runs' "$GH_LOG")" == 1 ]] || fail "unreadable answer was polled instead of failing at once"
printf 'not json\n' > "$CHECK_RUNS_FILE"
got=$(run_ci)
[[ "$got" == 2 ]] || fail "unreadable check-runs gave $got, expected 2"
got=$(CHECK_RUNS_EXIT=1 run_ci)
[[ "$got" == 2 ]] || fail "failing gh gave $got, expected 2"
echo "PASS test_empty_or_unreadable_check_runs_is_needs_human"

# test_missing_expected_check_times_out_to_needs_human: a check that never appears is needs-human after the polls.
run "Some other check" completed success > "$CHECK_RUNS_FILE"
got=$(run_ci)
[[ "$got" == 2 ]] || fail "missing expected check gave $got, expected 2"
polls=$(grep -c '/check-runs' "$GH_LOG")
[[ "$polls" == 3 ]] || fail "expected 3 polls before the timeout, got $polls"
echo "PASS test_missing_expected_check_times_out_to_needs_human"

# A check still in progress is polled again, then passes when it completes.
# The stub serves the in-progress answer on its first call and the completed one afterwards.
printf '%s\n' '{"name":"Validate Plugin Structure","status":"in_progress","conclusion":null}' | page > "$TMP/pending.txt"
printf '%s\n' '{"name":"Validate Plugin Structure","status":"completed","conclusion":"success"}' | page > "$TMP/done.txt"
cp "$TMP/pending.txt" "$CHECK_RUNS_FILE"
: > "$GH_LOG"
set +e
FLIP_AFTER=1 FLIP_FILE="$TMP/done.txt" bash "$GATES" ci >/dev/null 2>"$TMP/flip.err"
flip=$?
set -e
[[ "$flip" == 0 ]] || fail "in-progress then completed gave $flip, expected 0 ($(cat "$TMP/flip.err"))"
[[ "$(grep -c '/check-runs' "$GH_LOG")" -ge 2 ]] || fail "in-progress check was not polled again"
echo "PASS an in-progress check is polled until it completes"

# A later re-run of the same check supersedes an earlier failed run: the latest by id decides.
printf '%s\n' '{"name":"Validate Plugin Structure","id":1,"started_at":"2026-10-30T10:00:00Z","status":"completed","conclusion":"failure"}' \
  '{"name":"Validate Plugin Structure","id":2,"started_at":"2026-10-30T11:00:00Z","status":"completed","conclusion":"success"}' | page > "$CHECK_RUNS_FILE"
got=$(run_ci)
[[ "$got" == 0 ]] || fail "a later success after an earlier failure gave $got, expected 0"
# The reverse order: a later failure still fails the gate.
printf '%s\n' '{"name":"Validate Plugin Structure","id":3,"started_at":"2026-10-30T12:00:00Z","status":"completed","conclusion":"success"}' \
  '{"name":"Validate Plugin Structure","id":4,"started_at":"2026-10-30T13:00:00Z","status":"completed","conclusion":"failure"}' | page > "$CHECK_RUNS_FILE"
got=$(run_ci)
[[ "$got" == 1 ]] || fail "a later failure after an earlier success gave $got, expected 1"
echo "PASS the latest run of an expected check decides"

# test_paginated_later_page_failure_is_caught: the poll reads every page, so a failure on a later page counts.
# Two raw pages: the first is all green, the second (a later page) holds the failure.
{ printf '%s\n' '{"name":"Validate Plugin Structure","status":"completed","conclusion":"success"}' | page
  printf '%s\n' '{"name":"Validate Plugin Structure","status":"completed","conclusion":"failure"}' | page; } > "$CHECK_RUNS_FILE"
got=$(run_ci)
[[ "$got" == 1 ]] || fail "later-page failure gave $got, expected 1"
grep -q -- '--paginate' "$GH_LOG" || fail "check-runs read is not paginated"
echo "PASS test_paginated_later_page_failure_is_caught"

# The CI read uses the step token and the commit's check runs, never a bot token.
run "Validate Plugin Structure" completed success > "$CHECK_RUNS_FILE"
run_ci >/dev/null
grep -q "repos/acme/repo/commits/$HEAD_SHA/check-runs" "$GH_LOG" || fail "check-runs read is not bound to the head"
echo "PASS the check-runs read is bound to head_sha"

# test_missing_eval_status_is_needs_human: the evals gate requires skill-audit/evals success on the head.
run_evals() {
  : > "$GH_LOG"
  bash "$GATES" evals > "$TMP/evals.out" 2> "$TMP/evals.err" || fail "evals gate exited non-zero: $(cat "$TMP/evals.err")"
  cat "$TMP/evals.out"
}
printf '%s\n' '[{"context":"skill-audit/evals","state":"success"}]' > "$STATUS_FILE"
got=$(run_evals)
[[ "$got" == 0 ]] || fail "success eval status gave $got, expected 0"
printf '%s\n' '[{"context":"skill-audit/evals","state":"failure"}]' > "$STATUS_FILE"
got=$(run_evals)
[[ "$got" == 1 ]] || fail "failure eval status gave $got, expected 1"
printf '%s\n' '[{"context":"other","state":"success"}]' > "$STATUS_FILE"
got=$(run_evals)
[[ "$got" == 2 ]] || fail "missing eval status gave $got, expected 2"
printf '%s\n' '[]' > "$STATUS_FILE"
got=$(run_evals)
[[ "$got" == 2 ]] || fail "empty statuses gave $got, expected 2"
printf 'junk' > "$STATUS_FILE"
got=$(run_evals)
[[ "$got" == 2 ]] || fail "unreadable statuses gave $got, expected 2"
got=$(STATUS_EXIT=1 run_evals)
[[ "$got" == 2 ]] || fail "failing status read gave $got, expected 2"
printf '%s\n' '[{"context":"skill-audit/evals","state":"success"}]' > "$STATUS_FILE"
run_evals >/dev/null
grep -q "repos/acme/repo/commits/$HEAD_SHA/statuses" "$GH_LOG" || fail "eval status read is not bound to head_sha"
echo "PASS test_missing_eval_status_is_needs_human"

# test_truncated_diff_is_never_positive: the diff-size gate is needs-human when the diff is cut.
export REVIEW_DIFF_CAP=20
printf 'x%.0s' $(seq 1 100) > "$TMP/big.diff"
size_code=$(bash "$GATES" diff-size "$TMP/big.diff" 2> "$TMP/size.err")
[[ "$size_code" == 2 ]] || fail "truncated diff gave $size_code, expected 2"
printf 'small\n' > "$TMP/small.diff"
[[ "$(bash "$GATES" diff-size "$TMP/small.diff" 2>/dev/null)" == 0 ]] || fail "small diff rejected"
echo "PASS test_truncated_diff_is_never_positive"

echo 'PASS review-gates.sh'
