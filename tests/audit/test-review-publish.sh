#!/usr/bin/env bash
# Offline tests for .github/audit/review-publish.sh with a stub gh on PATH.
# Covers the publish contract of the PR review (Phase 1 brief, Task A2): head
# binding, one COMMENT review bound to commit_id, the skill-audit/review status,
# the mutually exclusive audit-review:* labels, sanitizing, the automerge notice
# (never a merge call) and no partial publish when a call fails.
#
# Usage of the publisher: review-publish.sh OUTCOME.json REVIEW.json GATES.json
# Environment: GH_REPO, PR_NUMBER, HEAD_SHA, GH_TOKEN, optional AUDIT_AUTOMERGE.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
PUBLISH="$ROOT/.github/audit/review-publish.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin" "$TMP/payloads"

# Stub gh: logs every call, copies --input payloads, and answers the reads the
# publisher makes. GH_FAIL_PATTERN makes matching calls fail.
cat > "$TMP/bin/gh" <<'STUB'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$GH_LOG"
if [[ -n "${GH_FAIL_PATTERN:-}" && "$*" == *"$GH_FAIL_PATTERN"* ]]; then
  echo "stub failure: $*" >&2
  exit 1
fi
prev=""
for arg in "$@"; do
  if [[ "$prev" == --input ]]; then
    n=$(wc -l < "$GH_LOG")
    cp "$arg" "$PAYLOAD_DIR/call-$n.json"
  fi
  prev=$arg
done
case "$*" in
  *"pr view "*"--json headRefOid"*) printf '%s\n' "$LIVE_HEAD" ;;
  *"pr view "*"--json labels"*) printf '%s' "$LABELS" ;;
  *"--paginate"*"/issues/"*"/comments"*) printf '%s' "$COMMENT_BODIES" ;;
  *) ;;
esac
STUB
chmod +x "$TMP/bin/gh"
export PATH="$TMP/bin:$PATH"
export GH_LOG="$TMP/gh.log" PAYLOAD_DIR="$TMP/payloads"
export GH_REPO=acme/repo PR_NUMBER=42 GH_TOKEN=test-token
export HEAD_SHA=0123456789abcdef0123456789abcdef01234567

fail() { printf 'FAIL %s\n' "$*" >&2; exit 1; }

reset() {
  : > "$GH_LOG"
  rm -f "$PAYLOAD_DIR"/call-*.json
  export LIVE_HEAD="$HEAD_SHA" LABELS="" COMMENT_BODIES="" GH_FAIL_PATTERN=""
  unset AUDIT_AUTOMERGE || true
}

# log_has FRAGMENT: some gh call contains FRAGMENT (exact text, not a regex).
log_has() { grep -qF -- "$1" "$GH_LOG" || fail "expected gh call containing: $1 (log: $(tr '\n' '|' < "$GH_LOG"))"; }
log_lacks() { if grep -qF -- "$1" "$GH_LOG"; then fail "unexpected gh call containing: $1"; fi; }

write_outcome() { printf '{"outcome":"%s","status":"%s","label":"%s"}\n' "$1" "$2" "$3" > "$TMP/outcome.json"; }
write_review() { printf '%s\n' "$1" > "$TMP/review.json"; }
write_gates() { printf '{"scope":0,"check":0,"evals":0,"ci":0,"diff-size":0}\n' > "$TMP/gates.json"; }
publish() { "$PUBLISH" "$TMP/outcome.json" "$TMP/review.json" "$TMP/gates.json"; }

# payload_with KEY VALUE: the JSON posted as a review body (one of call-*.json).
review_payload() {
  local file
  file=$(grep -l '"event"' "$PAYLOAD_DIR"/call-*.json | head -1) || fail "no review payload was posted"
  cat "$file"
}

APPROVE='{"verdict":"approve","findings":[]}'
CHANGES_ONE='{"verdict":"changes","findings":[{"id":"f1","file":"skills/a/SKILL.md","line":3,"severity":"high","summary":"Missing frontmatter field."}]}'
write_gates

# Positive: the review is bound to head_sha, the status is set on head_sha, the label is added.
reset
write_outcome positive success audit-review:positive
write_review "$APPROVE"
publish || fail "publish positive"
review_payload | python3 -c '
import json, sys
body = json.load(sys.stdin)
assert body["event"] == "COMMENT", body
assert body["commit_id"] == "'"$HEAD_SHA"'", body
assert body["body"].strip(), body
'
log_has "repos/acme/repo/statuses/$HEAD_SHA"
log_has "context=skill-audit/review"
log_has "state=success"
log_has "pr edit 42 --add-label audit-review:positive"
echo "PASS test_comment_posted_with_commit_id (positive: COMMENT bound to head, status on head)"

# Labels are created with --force before they are applied.
reset
write_outcome positive success audit-review:positive
write_review "$APPROVE"
publish || fail "publish labels"
log_has "label create audit-review:positive --force"
log_has "label create audit-review:changes --force"
log_has "label create audit-review:needs-human --force"
echo "PASS labels are created with --force first"

# test_label_reconciliation: positive to needs-human removes the old label and adds the new one.
reset
LABELS=$'audit-review:positive\nbug'
write_outcome needs-human failure audit-review:needs-human
write_review '{"verdict":"unsure","findings":[]}'
publish || fail "publish needs-human"
log_has "pr edit 42 --remove-label audit-review:positive"
log_has "pr edit 42 --add-label audit-review:needs-human"
log_lacks "--remove-label bug"
log_lacks "--remove-label audit-review:needs-human"
echo "PASS test_label_reconciliation (positive to needs-human)"

# positive to changes.
reset
LABELS="audit-review:positive"
write_outcome changes failure audit-review:changes
write_review "$CHANGES_ONE"
publish || fail "publish changes"
log_has "pr edit 42 --remove-label audit-review:positive"
log_has "pr edit 42 --add-label audit-review:changes"
log_lacks "--add-label audit-review:positive"
echo "PASS test_label_reconciliation (positive to changes)"

# A label to none: the outcome is needs-human with no positive label in the add list, and changes are removed.
reset
LABELS="audit-review:changes"
write_outcome needs-human failure audit-review:needs-human
write_review '{"verdict":"unsure","findings":[]}'
publish || fail "publish label to none"
log_has "pr edit 42 --remove-label audit-review:changes"
echo "PASS test_label_reconciliation (changes to needs-human)"

# AUDIT_ON_POSITIVE=none: a positive outcome adds no label and removes an existing positive label.
reset
LABELS="audit-review:positive"
write_outcome positive success ""
write_review "$APPROVE"
publish || fail "publish positive with none"
log_has "pr edit 42 --remove-label audit-review:positive"
log_lacks "--add-label audit-review:positive"
log_has "state=success"
echo "PASS test_on_positive_none_adds_no_label"

# test_stale_head_sets_no_status: the live head moved, so only a comment is posted.
reset
LIVE_HEAD=ffffffffffffffffffffffffffffffffffffffff
write_outcome changes failure audit-review:changes
write_review "$CHANGES_ONE"
publish || fail "publish stale"
log_lacks "statuses/"
log_lacks "pr edit"
log_lacks "label create"
review_payload | python3 -c '
import json, sys
body = json.load(sys.stdin)
assert body["event"] == "COMMENT", body
assert body["commit_id"] == "'"$HEAD_SHA"'", body
'
echo "PASS test_stale_head_sets_no_status"

# test_comment_sanitized: reviewer text cannot inject HTML, images, links, mentions, references or tokens.
reset
write_outcome changes failure audit-review:changes
python3 - "$TMP/review.json" <<'PY'
import json, sys
hostile = (
    '<script>alert(1)</script> <img src="https://evil.example/x.png"> ![x](https://evil.example/i) '
    '[click](https://evil.example/login) https://evil.example/steal see www.evil.example '
    '#123 owner/repo#456 @acme/security-team @someone '
    'ghp_0123456789abcdefghijABCDEFGHIJ0123 github_pat_0123456789abcdefghijABCDEFGHIJ '
    'x-access-token:abcdef123456 Bearer abc.def.ghi'
)
review = {"verdict": "changes", "findings": [
    {"id": "f1", "file": "skills/a/SKILL.md", "line": 3, "severity": "high", "summary": hostile},
]}
json.dump(review, open(sys.argv[1], "w"))
PY
publish || fail "publish sanitized"
review_payload | python3 -c '
import json, sys
body = json.load(sys.stdin)["body"]
# Only the reviewer-controlled lines are scanned: the publisher writes its own heading and head line.
reviewed = body.split("Findings:", 1)[1]
for banned in ("<", ">", "![", "](", "http", "www.", "#", "@", "`", "ghp_", "github_pat_",
               "x-access-token", "Bearer abc", "evil.example", "owner/repo", "script", "img"):
    assert banned not in reviewed, f"sanitizer let {banned!r} through: {reviewed!r}"
assert "f1" in body and "skills/a/SKILL.md" in body, body
'
echo "PASS test_comment_sanitized"

# test_finding_id_sanitized: the reviewer id is free text in the schema, so it gets the same sanitizer as the summary.
reset
write_outcome changes failure audit-review:changes
python3 - "$TMP/review.json" <<'PY'
import json, sys
review = {"verdict": "changes", "findings": [
    {"id": "@acme/security-team [click](https://evil.example/x) #7 <b>f1</b>", "file": "skills/a/SKILL.md", "line": 3, "severity": "high", "summary": "Missing field."},
]}
json.dump(review, open(sys.argv[1], "w"))
PY
publish || fail "publish with a hostile finding id"
review_payload | python3 -c '
import json, sys
body = json.load(sys.stdin)["body"]
reviewed = body.split("Findings:", 1)[1]
for banned in ("<", ">", "](", "http", "#", "@", "evil.example", "security-team", "[click]"):
    assert banned not in reviewed, f"finding id let {banned!r} through: {reviewed!r}"
assert "Missing field." in reviewed, reviewed
'
echo "PASS test_finding_id_sanitized"

# A finding's file path survives sanitizing: underscores and dotted names are real path characters.
reset
write_outcome changes failure audit-review:changes
python3 - "$TMP/review.json" <<'PY'
import json, sys
review = {"verdict": "changes", "findings": [
    {"id": "f1", "file": "tests/audit/test_foo.py", "line": 3, "severity": "low", "summary": "Keep the name."},
    {"id": "f2", "file": "skills/my_skill/tools.io/SKILL.md", "line": 9, "severity": "low", "summary": "Path check."},
]}
json.dump(review, open(sys.argv[1], "w"))
PY
publish || fail "publish with path findings"
review_payload | python3 -c '
import json, sys
body = json.load(sys.stdin)["body"]
for kept in ("tests/audit/test_foo.py", "skills/my_skill/tools.io/SKILL.md"):
    assert kept in body, f"path {kept!r} was mangled: {body!r}"
'
echo "PASS finding paths keep their underscores and dots"

# test_automerge_true_is_not_acted_on: a notice once, never a merge or --auto.
reset
export AUDIT_AUTOMERGE=true
write_outcome positive success audit-review:positive
write_review "$APPROVE"
publish || fail "publish automerge"
log_lacks "pr merge"
log_lacks "--auto"
log_has "repos/acme/repo/issues/42/comments"
log_has "skill-audit-automerge-notice"
reset
export AUDIT_AUTOMERGE=true
COMMENT_BODIES='<!-- skill-audit-automerge-notice --> already posted'
write_outcome positive success audit-review:positive
write_review "$APPROVE"
publish || fail "publish automerge again"
log_lacks "skill-audit-automerge-notice"
log_lacks "pr merge"
unset AUDIT_AUTOMERGE
echo "PASS test_automerge_true_is_not_acted_on"

# No partial publish: a failed review POST sets no status and no label.
reset
GH_FAIL_PATTERN="pulls/42/reviews"
write_outcome positive success audit-review:positive
write_review "$APPROVE"
if publish; then fail "publish should fail when the review POST fails"; fi
log_lacks "statuses/"
log_lacks "pr edit"
echo "PASS a failed review POST publishes nothing else"

# A missing or unreadable outcome is needs-human, published as a failure (never an aborted run with no comment).
reset
rm -f "$TMP/outcome.json"
write_review '{"verdict":"unsure","findings":[]}'
publish || fail "publish with a missing outcome.json must still publish needs-human"
log_has "pr edit 42 --add-label audit-review:needs-human"
log_has "state=failure"
reset
printf 'not json' > "$TMP/outcome.json"
write_review '{"verdict":"unsure","findings":[]}'
publish || fail "publish with an unreadable outcome.json must still publish needs-human"
log_has "pr edit 42 --add-label audit-review:needs-human"
echo "PASS a missing or unreadable outcome is published as needs-human"

# A skipped outcome never touches GitHub.
reset
write_outcome skipped none ""
write_review ""
publish || fail "publish skipped"
[[ ! -s "$GH_LOG" ]] || fail "skipped outcome made gh calls"
echo "PASS skipped outcome makes no calls"

# Invalid environment fails before any call.
reset
if GH_REPO="" publish 2>/dev/null; then fail "missing GH_REPO accepted"; fi
if PR_NUMBER=abc publish 2>/dev/null; then fail "non-numeric PR accepted"; fi
if HEAD_SHA=short publish 2>/dev/null; then fail "malformed HEAD_SHA accepted"; fi
[[ ! -s "$GH_LOG" ]] || fail "gh called despite an invalid environment"
echo "PASS invalid inputs make no calls"

echo 'PASS review-publish.sh'
