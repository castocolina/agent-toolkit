#!/usr/bin/env bash
# Read and write the AUDIT_LAST_STATE repository variable.
#
#   write-state.sh read        print the live state object ({} when absent or unusable)
#   write-state.sh checkpoint  stamp checked_at = now (a clean run that needed no judging)
#   write-state.sh attempt     stamp last_attempt_at = now (a run that is about to start judging)
#   write-state.sh state       replace the detect-owned keys with DETECT_STATE, stamp checked_at
#
# Every write reads the live variable first (never a workflow-level snapshot), merges with jq
# and writes with gh variable set. Only a 404 ("HTTP 404" in gh's stderr: the variable is absent)
# or a successfully read value that is not one JSON object starts from {}. Any other read failure
# (authentication, authorization, transport) aborts without writing: a stale or wrong baseline
# must never be stamped as the newest state.
#
# Environment: GH_REPO (owner/name, required), GH_TOKEN (the caller's token, read by gh),
# DETECT_STATE (state mode only: the detect output's state object).
set -euo pipefail

usage() { echo "usage: write-state.sh read|checkpoint|attempt|state" >&2; exit 2; }
[ "$#" -eq 1 ] || usage
MODE=$1
case "$MODE" in read|checkpoint|attempt|state) ;; *) usage ;; esac
: "${GH_REPO:?GH_REPO must name the repository}"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
NAME=AUDIT_LAST_STATE
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# read_live: prints the variable's JSON object on stdout, or {} with a notice.
read_live() {
  local value
  if value=$(gh api "repos/$GH_REPO/actions/variables/$NAME" --jq .value 2>"$TMP/read.err"); then
    :
  elif grep -q 'HTTP 404' "$TMP/read.err"; then
    echo "notice: $NAME is absent; starting from {}" >&2
    printf '{}'
    return 0
  else
    cat "$TMP/read.err" >&2
    echo "error: cannot read $NAME; no state was written" >&2
    return 1
  fi
  # Slurp: exactly one JSON object is accepted; '{} {}', arrays, scalars and garbage are unusable.
  if ! jq -cse 'if length == 1 and (.[0] | type) == "object" then .[0] else error("not an object") end' \
      <<<"$value" 2>/dev/null; then
    echo "notice: $NAME is not one JSON object; starting from {}" >&2
    printf '{}'
  fi
}

if [ "$MODE" = read ]; then
  read_live
  exit 0
fi

if [ "$MODE" = state ]; then
  # The detect state must be a complete object with the three detect-owned keys of the right shape,
  # or the write would replace a valid baseline with garbage.
  if ! DETECT_JSON=$(jq -cse 'if length == 1 and (.[0] | type) == "object" and (.[0].judge_sha | type) == "string"
        and (.[0].skills | type) == "object" and (.[0].upstreams | type) == "object"
      then .[0] else error("not a detect state") end' <<<"${DETECT_STATE:-}" 2>/dev/null); then
    echo "error: DETECT_STATE is not a detect state object; no state was written" >&2
    exit 1
  fi
fi

LIVE=$(read_live)
if [ "$MODE" = state ]; then
  JSON=$(jq -c --argjson d "$DETECT_JSON" --arg now "$NOW" \
    '. + {judge_sha: $d.judge_sha, skills: $d.skills, upstreams: $d.upstreams} | .checked_at = $now' <<<"$LIVE")
else
  STAMP=checked_at
  [ "$MODE" = attempt ] && STAMP=last_attempt_at
  JSON=$(jq -c --arg k "$STAMP" --arg now "$NOW" '.[$k] = $now' <<<"$LIVE")
fi

gh variable set "$NAME" --body "$JSON"
