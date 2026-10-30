#!/usr/bin/env bash
# Gates of the PR review that read GitHub state or the PR diff
# (.github/workflows/skill-audit-review.yaml). Trusted code: it runs from the
# default-branch copy in $RUNNER_TEMP/trusted, never from the PR checkout.
#
# Usage:
#   review-gates.sh ci                 poll the expected CI check runs on HEAD_SHA
#   review-gates.sh evals              require the skill-audit/evals status on HEAD_SHA
#   review-gates.sh diff-size DIFF     pass when DIFF is within REVIEW_DIFF_CAP bytes
# Environment: GH_TOKEN (step-scoped), GH_REPO, HEAD_SHA, EXPECTED_CHECKS_FILE,
#   REVIEW_CI_SLEEP (seconds, default 60), REVIEW_CI_MAX_POLLS (default 30),
#   REVIEW_DIFF_CAP (bytes, default 61440).
# Exit codes (the gate code written to gates.json): 0 pass, 1 fail, 2 needs-human.
set -uo pipefail

PASS=0
FAIL=1
HUMAN=2

log() { printf 'review-gates: %s\n' "$*" >&2; }

# A check conclusion is a gate pass when it is success, skipped or neutral.
conclusion_pass() {
  case "$1" in
    success|skipped|neutral) return 0 ;;
    *) return 1 ;;
  esac
}

# fetch_check_runs: every page of the commit's check runs, one JSON object per line.
# The raw pages are validated first: each must be JSON with a check_runs array. An empty array
# is a real answer (no runs yet) and prints nothing, so the caller polls. An unreadable page
# fails here, and the caller treats that as needs-human.
fetch_check_runs() {
  local raw
  raw=$(gh api --paginate "repos/$GH_REPO/commits/$HEAD_SHA/check-runs" 2>/dev/null) || return 1
  [[ -n "$raw" ]] || return 1
  jq -e -s 'all(.[]; (.check_runs | type) == "array")' <<<"$raw" >/dev/null 2>&1 || return 1
  jq -c '.check_runs[]' <<<"$raw" 2>/dev/null
}

# evaluate_checks TEXT: print one of pass (0), fail (1), pending or needs-human (2).
# pending means an expected check is missing or not completed yet; the caller polls
# again. A failed conclusion is fail at once. An empty TEXT is a valid answer with no runs
# yet (fetch_check_runs rejects unreadable pages before this), so it is pending, not human.
evaluate_checks() {
  local text=$1 name line parsed status conclusion pending=0 seen named=0
  # No expected names (missing or blank file) is needs-human: nothing to check must never pass.
  [[ -r "$EXPECTED_CHECKS_FILE" ]] || { echo human; return 0; }
  while IFS= read -r name; do
    [[ -n "$name" ]] && named=1
    [[ -n "$name" ]] || continue
    # Only the latest run of the name decides: a later re-run supersedes an earlier failure.
    if ! parsed=$(jq -rs --arg name "$name" \
        'map(select(.name == $name)) | sort_by([(.started_at // ""), (.id // 0)]) | last | if . == null then "" else [.status, (.conclusion // "")] | @tsv end' <<<"$text" 2>/dev/null); then
      echo human; return 0
    fi
    if [[ -z "$parsed" ]]; then pending=1; continue; fi
    status=${parsed%%$'\t'*}
    conclusion=${parsed#*$'\t'}
    if [[ "$status" == completed ]]; then
      if ! conclusion_pass "$conclusion"; then
        echo fail; return 0
      fi
    else
      pending=1
    fi
  done < "$EXPECTED_CHECKS_FILE"
  if ((named == 0)); then echo human; return 0; fi
  if ((pending)); then echo pending; else echo pass; fi
}

gate_ci() {
  local polls=0 max=${REVIEW_CI_MAX_POLLS:-30} sleep_for=${REVIEW_CI_SLEEP:-60} text verdict
  while :; do
    polls=$((polls + 1))
    if ! text=$(fetch_check_runs); then
      log "check-runs read failed"; echo "$HUMAN"; return 0
    fi
    verdict=$(evaluate_checks "$text")
    case "$verdict" in
      pass) echo "$PASS"; return 0 ;;
      fail) echo "$FAIL"; return 0 ;;
      human) log "check-runs answer is empty or unreadable"; echo "$HUMAN"; return 0 ;;
    esac
    if ((polls >= max)); then
      log "expected checks not complete after $polls polls"
      echo "$HUMAN"; return 0
    fi
    log "waiting for expected checks (poll $polls of $max)"
    sleep "$sleep_for"
  done
}

gate_evals() {
  local statuses state
  statuses=$(gh api --paginate "repos/$GH_REPO/commits/$HEAD_SHA/statuses" --jq '.[]' 2>/dev/null) || { echo "$HUMAN"; return 0; }
  if [[ -z "$statuses" ]]; then
    log "no commit statuses on $HEAD_SHA"
    echo "$HUMAN"; return 0
  fi
  state=$(jq -rs 'map(select(.context == "skill-audit/evals")) | sort_by(.created_at // "") | last | .state // ""' <<<"$statuses" 2>/dev/null) || { echo "$HUMAN"; return 0; }
  case "$state" in
    success) echo "$PASS" ;;
    failure|error) echo "$FAIL" ;;
    *) log "skill-audit/evals status is missing or not decided ($state)"; echo "$HUMAN" ;;
  esac
}

gate_diff_size() {
  local file=$1 cap=${REVIEW_DIFF_CAP:-61440} size
  size=$(wc -c < "$file") || { echo "$HUMAN"; return 0; }
  if ((size > cap)); then
    log "diff is $size bytes, over the $cap byte cap: needs-human"
    echo "$HUMAN"
  else
    echo "$PASS"
  fi
}

case "${1:-}" in
  ci)
    : "${GH_TOKEN:?GH_TOKEN is required}" "${GH_REPO:?GH_REPO is required}" "${HEAD_SHA:?HEAD_SHA is required}"
    : "${EXPECTED_CHECKS_FILE:?EXPECTED_CHECKS_FILE is required}"
    gate_ci
    ;;
  evals)
    : "${GH_TOKEN:?GH_TOKEN is required}" "${GH_REPO:?GH_REPO is required}" "${HEAD_SHA:?HEAD_SHA is required}"
    gate_evals
    ;;
  diff-size)
    [[ -n "${2:-}" ]] || { echo "usage: review-gates.sh diff-size DIFF" >&2; exit 64; }
    gate_diff_size "$2"
    ;;
  *)
    echo "usage: review-gates.sh ci|evals|diff-size DIFF" >&2
    exit 64
    ;;
esac
