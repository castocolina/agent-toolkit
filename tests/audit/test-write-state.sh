#!/usr/bin/env bash
# Offline tests for .github/audit/write-state.sh. A stub gh (REST read and variable set) and a stub
# date are put first on PATH, so nothing reaches GitHub and every run is deterministic.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WS="$ROOT/.github/audit/write-state.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
BIN="$TMP/bin"
mkdir -p "$BIN"
NOW=2026-10-30T06:00:00Z
export STUB_LOG="$TMP/gh.log" STUB_WRITES="$TMP/writes" STUB_LIVE_FILE="$TMP/live" STUB_NOW="$NOW"
LIVE_MODE=value

cat > "$BIN/gh" <<'STUB'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$STUB_LOG"
if [ "$1" = api ] && [ "$2" = "repos/acme/repo/actions/variables/AUDIT_LAST_STATE" ] && [ "$3" = --jq ] && [ "$4" = .value ]; then
  case "${STUB_LIVE:-value}" in
    value) cat "$STUB_LIVE_FILE"; echo ;;
    absent) echo "gh: Not Found (HTTP 404)" >&2; exit 1 ;;
    forbidden) echo "gh: Resource not accessible by integration (HTTP 403)" >&2; exit 1 ;;
    auth) echo "gh: Bad credentials (HTTP 401)" >&2; exit 1 ;;
    transport) echo "Get https://api.github.com/: dial tcp: lookup api.github.com: no such host" >&2; exit 1 ;;
  esac
  exit 0
fi
if [ "$#" = 5 ] && [ "$1 $2 $3 $4" = "variable set AUDIT_LAST_STATE --body" ]; then
  [ -z "${STUB_SET_FAIL:-}" ] || { echo "gh: set failed" >&2; exit 1; }
  printf '%s\n' "$5" >> "$STUB_WRITES"
  exit 0
fi
echo "unexpected gh call: $*" >&2
exit 90
STUB
cat > "$BIN/date" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$STUB_NOW"
STUB
chmod +x "$BIN/gh" "$BIN/date"

fail() { echo "test-write-state: $*" >&2; exit 1; }

# run MODE [VAR=value ...]: runs write-state.sh with a clean environment; sets RC, OUT and ERR.
run_ws() {
  local mode=$1
  shift
  : > "$STUB_LOG"
  : > "$STUB_WRITES"
  set +e
  OUT=$(env -i PATH="$BIN:$PATH" GH_REPO=acme/repo STUB_LOG="$STUB_LOG" STUB_WRITES="$STUB_WRITES" \
    STUB_LIVE_FILE="$STUB_LIVE_FILE" STUB_NOW="$STUB_NOW" STUB_LIVE="$LIVE_MODE" "$@" \
    bash "$WS" "$mode" 2>"$TMP/err")
  RC=$?
  set -e
  ERR=$(cat "$TMP/err")
}

live() { # live MODE [VALUE]: configure the stub's live AUDIT_LAST_STATE
  LIVE_MODE=$1
  printf '%s' "${2:-}" > "$STUB_LIVE_FILE"
}

same_json() { # same_json NAME ACTUAL EXPECTED: compare canonical JSON
  local a e
  a=$(jq -cS . <<<"$2") || fail "$1: output is not JSON: $2"
  e=$(jq -cS . <<<"$3")
  [ "$a" = "$e" ] || fail "$1: got $a, expected $e"
}

expect_rc() { [ "$RC" = "$1" ] || fail "$2: exit $RC, expected $1 (stderr: $ERR)"; }
no_write() { [ ! -s "$STUB_WRITES" ] || fail "$1: a write happened: $(cat "$STUB_WRITES")"; }
one_write() { [ "$(wc -l < "$STUB_WRITES")" = 1 ] || fail "$1: expected exactly one write, got: $(cat "$STUB_WRITES")"; }
written() { tail -n 1 "$STUB_WRITES"; }

# --- read: the live object, {} when absent or unusable, never a write ---------------------------
live value '{"judge_sha":"j","skills":{"alpha":"s"},"upstreams":{},"checked_at":"2026-10-01T06:00:00Z","future":[1]}'
run_ws read
expect_rc 0 "read existing"
same_json "read keeps every key" "$OUT" '{"judge_sha":"j","skills":{"alpha":"s"},"upstreams":{},"checked_at":"2026-10-01T06:00:00Z","future":[1]}'
no_write "read"

live absent
run_ws read
expect_rc 0 "read absent"
same_json "read absent gives {}" "$OUT" '{}'
grep -q 'absent' <<<"$ERR" || fail "read absent gives no notice: $ERR"
no_write "read absent"

for value in '[1,2]' '"text"' '42' 'null' '{bad' '' '{} {}'; do
  live value "$value"
  run_ws read
  expect_rc 0 "read unusable value [$value]"
  same_json "read unusable [$value] gives {}" "$OUT" '{}'
  grep -q 'not one JSON object' <<<"$ERR" || fail "read unusable [$value] gives no notice: $ERR"
done

# --- checkpoint: stamps checked_at and keeps the rest ----------------------------------------------
live absent
run_ws checkpoint
expect_rc 0 "checkpoint absent"
one_write "checkpoint absent"
same_json "checkpoint absent starts from {}" "$(written)" "{\"checked_at\":\"$NOW\"}"
grep -q 'absent' <<<"$ERR" || fail "checkpoint absent gives no notice: $ERR"

live value '{"judge_sha":"j","skills":{"alpha":"s"},"upstreams":{"alpha|o/r":"2026-01-01T00:00:00Z"},"last_attempt_at":"2026-10-20T06:00:00Z","checked_at":"2026-09-01T06:00:00Z","future_field":{"k":[1,2]}}'
run_ws checkpoint
expect_rc 0 "checkpoint preserves"
one_write "checkpoint preserves"
same_json "checkpoint keeps unknown keys" "$(written)" '{"judge_sha":"j","skills":{"alpha":"s"},"upstreams":{"alpha|o/r":"2026-01-01T00:00:00Z"},"last_attempt_at":"2026-10-20T06:00:00Z","checked_at":"2026-10-30T06:00:00Z","future_field":{"k":[1,2]}}'
case "$(written)" in *$'\n'*) fail "checkpoint write is not compact one-line JSON" ;; esac

for value in '[1,2]' '"text"' '42' 'null' '{bad' '' '{} {}'; do
  live value "$value"
  run_ws checkpoint
  expect_rc 0 "checkpoint unusable [$value]"
  one_write "checkpoint unusable [$value]"
  same_json "checkpoint unusable [$value] starts from {}" "$(written)" "{\"checked_at\":\"$NOW\"}"
done

# --- attempt: stamps last_attempt_at, keeps checked_at -------------------------------------------
live value '{"checked_at":"2026-10-01T06:00:00Z","judge_sha":"j"}'
run_ws attempt
expect_rc 0 "attempt"
one_write "attempt"
same_json "attempt stamps last_attempt_at" "$(written)" "{\"checked_at\":\"2026-10-01T06:00:00Z\",\"judge_sha\":\"j\",\"last_attempt_at\":\"$NOW\"}"

# --- state: detect-owned keys are replaced, the rest kept, checked_at stamped -----------------------
DETECT='{"judge_sha":"new","skills":{"alpha":"n1"},"upstreams":{"alpha|o/r":"d2"}}'
live value '{"judge_sha":"old","skills":{"alpha":"o1","gone":"g"},"upstreams":{"gone|x":"d"},"last_attempt_at":"2026-10-20T06:00:00Z","future_field":"keep"}'
run_ws state DETECT_STATE="$DETECT"
expect_rc 0 "state"
one_write "state"
same_json "state replaces detect-owned keys" "$(written)" "{\"judge_sha\":\"new\",\"skills\":{\"alpha\":\"n1\"},\"upstreams\":{\"alpha|o/r\":\"d2\"},\"last_attempt_at\":\"2026-10-20T06:00:00Z\",\"future_field\":\"keep\",\"checked_at\":\"$NOW\"}"

live absent
run_ws state DETECT_STATE="$DETECT"
expect_rc 0 "state absent"
same_json "state absent starts from {}" "$(written)" "{\"judge_sha\":\"new\",\"skills\":{\"alpha\":\"n1\"},\"upstreams\":{\"alpha|o/r\":\"d2\"},\"checked_at\":\"$NOW\"}"

for detect in '' '{"skills":{},"upstreams":{}}' '{"judge_sha":"x","skills":[],"upstreams":{}}' \
  '{"judge_sha":"x","skills":{},"upstreams":[]}' '[1]' '{} {}' 'not json'; do
  live value '{"judge_sha":"old"}'
  run_ws state DETECT_STATE="$detect"
  expect_rc 1 "state malformed DETECT_STATE [$detect]"
  no_write "state malformed DETECT_STATE [$detect]"
done
run_ws state
expect_rc 1 "state without DETECT_STATE"
no_write "state without DETECT_STATE"

# --- failures: a read error aborts without writing, for every mode -------------------------------
for failure in forbidden auth transport; do
  for mode in read checkpoint attempt; do
    live "$failure"
    run_ws "$mode"
    expect_rc 1 "$mode with $failure read"
    no_write "$mode with $failure read"
  done
  live "$failure"
  run_ws state DETECT_STATE="$DETECT"
  expect_rc 1 "state with $failure read"
  no_write "state with $failure read"
done
live forbidden
run_ws checkpoint
grep -q 'HTTP 403' <<<"$ERR" || fail "read error text is not passed through: $ERR"

# A failed write leaves the script failed (the caller marks the job as failed).
live value '{}'
run_ws checkpoint STUB_SET_FAIL=1
expect_rc 1 "checkpoint with failing set"

# --- contract: the read happens in the same run, before the write; the mode is validated ---------
live value '{"judge_sha":"j"}'
run_ws attempt
[ "$(sed -n 1p "$STUB_LOG")" = "api repos/acme/repo/actions/variables/AUDIT_LAST_STATE --jq .value" ] || fail "first gh call is not the live read: $(cat "$STUB_LOG")"
[ "$(sed -n 2p "$STUB_LOG")" = "variable set AUDIT_LAST_STATE --body $(written)" ] || fail "second gh call is not the write: $(cat "$STUB_LOG")"

run_ws bogus
expect_rc 2 "unknown mode"
[ ! -s "$STUB_LOG" ] || fail "unknown mode called gh: $(cat "$STUB_LOG")"

: > "$STUB_LOG"
set +e
env -i PATH="$BIN:$PATH" STUB_LOG="$STUB_LOG" STUB_WRITES="$STUB_WRITES" STUB_LIVE_FILE="$STUB_LIVE_FILE" \
  STUB_NOW="$STUB_NOW" STUB_LIVE=value bash "$WS" checkpoint >/dev/null 2>"$TMP/err"
rc=$?
set -e
[ "$rc" != 0 ] || fail "missing GH_REPO did not fail"
[ ! -s "$STUB_LOG" ] || fail "missing GH_REPO still called gh"

echo "PASS tests/audit/test-write-state.sh"
