#!/usr/bin/env bash
# Publish the PR review outcome (trusted step of .github/workflows/skill-audit-review.yaml).
#
# Usage: review-publish.sh OUTCOME.json REVIEW.json GATES.json
#   OUTCOME.json  the result of review-combine.py outcome: {outcome, status, label}
#   REVIEW.json   the validated reviewer answer (may be empty for skipped/needs-human)
#   GATES.json    the gate codes (used only for the comment's gate lines)
# Environment (step-scoped GH_TOKEN only):
#   GH_TOKEN, GH_REPO, PR_NUMBER, HEAD_SHA (the head the review and status bind to)
#   AUDIT_AUTOMERGE (true is accepted but not acted on in Phase 1)
#
# It posts one COMMENT review bound to HEAD_SHA (commit_id), sets the commit
# status skill-audit/review on HEAD_SHA, and keeps the four audit-review:* labels
# mutually exclusive. When the live head is not HEAD_SHA the outcome is stale:
# a comment only, no status and no label change. It never merges and never calls
# any merge command or auto-merge option.
set -euo pipefail

LABEL_POSITIVE='audit-review:positive'
LABEL_CHANGES='audit-review:changes'
LABEL_HUMAN='audit-review:needs-human'
CONTEXT='skill-audit/review'
NOTICE_MARK='<!-- skill-audit-automerge-notice -->'

die() { printf 'review-publish: %s\n' "$*" >&2; exit 1; }

[[ $# -eq 3 ]] || die 'usage: review-publish.sh OUTCOME.json REVIEW.json GATES.json'
OUTCOME_FILE=$1
REVIEW_FILE=$2
GATES_FILE=$3
: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GH_REPO:?GH_REPO is required}"
[[ "${GH_REPO}" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || die "GH_REPO must be owner/name"
[[ "${PR_NUMBER:-}" =~ ^[0-9]+$ ]] || die 'PR_NUMBER must be a number'
[[ "${HEAD_SHA:-}" =~ ^[0-9a-f]{40}$ ]] || die 'HEAD_SHA must be a 40-character commit SHA'

# A missing or unreadable outcome is needs-human (failure): the review must still publish a result.
OUTCOME_JSON='{"outcome":"needs-human","status":"failure","label":"audit-review:needs-human"}'
if jq -e 'type == "object" and (.outcome | type == "string")' "$OUTCOME_FILE" >/dev/null 2>&1; then
  OUTCOME_JSON=$(cat "$OUTCOME_FILE")
else
  echo 'review-publish: outcome.json is missing or unreadable; publishing needs-human' >&2
fi
OUTCOME=$(jq -r '.outcome' <<<"$OUTCOME_JSON")
STATUS_STATE=$(jq -r '.status' <<<"$OUTCOME_JSON")
LABEL=$(jq -r '.label' <<<"$OUTCOME_JSON")

case "$OUTCOME" in
  skipped) exit 0 ;;
  positive|changes|needs-human) ;;
  *) die "unknown outcome: $OUTCOME" ;;
esac

LIVE_HEAD=$(gh pr view "$PR_NUMBER" --json headRefOid --jq .headRefOid)
STALE=false
if [[ "$LIVE_HEAD" != "$HEAD_SHA" ]]; then
  STALE=true
  OUTCOME=stale
fi

# safe_path PATH: a repository path is printed as is when it is a plain relative path (letters, digits,
# '_', '.', '-', '/'; no '..', no leading '/'); anything else is replaced, so it cannot carry markup.
safe_path() {
  local path=$1
  if [[ -n "$path" && "$path" =~ ^[A-Za-z0-9_./-]+$ && "$path" != *..* && "$path" != /* ]]; then
    printf '%s' "$path"
  else
    printf '%s' '(invalid path)'
  fi
}

sanitize() {
  # Reviewer text is untrusted: keep plain words and the characters a finding needs.
  # Strips HTML, Markdown images and links, URLs, '#' references, team and user
  # mentions, token-shaped strings and any '@' or backtick.
  python3 -c '
import re, sys
text = sys.stdin.read()
text = re.sub(r"<[^>]*>", " ", text)
text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
text = re.sub(r"(?i)(https?://|www\.)\S+", " ", text)
text = re.sub(r"\S+\.(com|org|net|io|dev|example)\S*", " ", text)
text = re.sub(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#\d+", " ", text)
text = re.sub(r"#\d+", " ", text)
text = re.sub(r"@\S+", " ", text)
text = re.sub(r"(?i)(gh[pousr]_|github_pat_)[A-Za-z0-9_]+", " ", text)
text = re.sub(r"(?i)x-access-token\S*", " ", text)
text = re.sub(r"(?i)bearer\s+\S+", " ", text)
text = re.sub(r"[`*_~|\\]", "", text)
text = re.sub(r"[ \t]+", " ", text)
sys.stdout.write(text.strip())
'
}

render_body() {
  local gates finding_lines
  gates=$(jq -r 'to_entries | map("- \(.key): \(if .value == 0 then "pass" elif .value == 1 then "fail" else "needs-human" end)") | .[]' "$GATES_FILE" 2>/dev/null || true)
  printf '### Skill audit review: %s\n\n' "$OUTCOME"
  # shellcheck disable=SC2016 # the backticks are literal Markdown code marks
  printf 'Head: `%s`\n\n' "$HEAD_SHA"
  printf 'Gates:\n%s\n\n' "$gates"
  if [[ -s "$REVIEW_FILE" ]] && jq -e . "$REVIEW_FILE" >/dev/null 2>&1; then
    printf 'Reviewer verdict: %s\n\n' "$(jq -r '.verdict' "$REVIEW_FILE" | sanitize)"
    # The file field is a repository path, not prose: it keeps its underscores and dots and is checked
    # against a path allowlist. The id and the summary are reviewer prose and go through the sanitizer.
    finding_lines=$(jq -r '.findings[] | [.severity, (.file // ""), (.line | tostring), .id, (.summary // "")] | @tsv' "$REVIEW_FILE" \
      | while IFS=$'\t' read -r severity file line id summary; do
          printf -- '- [%s] %s:%s %s: %s\n' "$severity" "$(safe_path "$file")" "$line" "$(sanitize <<<"$id")" "$(sanitize <<<"$summary")"
        done)
    if [[ -n "$finding_lines" ]]; then
      printf 'Findings:\n%s\n' "$finding_lines"
    fi
  else
    printf 'The reviewer produced no valid answer for this head.\n'
  fi
}

BODY_FILE=$(mktemp)
trap 'rm -f "$BODY_FILE"' EXIT
render_body > "$BODY_FILE"

# One COMMENT review, bound to the reviewed commit.
python3 - "$BODY_FILE" "$HEAD_SHA" > "$BODY_FILE.json" <<'PY'
import json, sys
body = open(sys.argv[1], encoding="utf-8").read().strip()
print(json.dumps({"event": "COMMENT", "commit_id": sys.argv[2], "body": body}))
PY
gh api --method POST "repos/$GH_REPO/pulls/$PR_NUMBER/reviews" --input "$BODY_FILE.json" >/dev/null
rm -f "$BODY_FILE.json"

if [[ "${AUDIT_AUTOMERGE:-false}" == true ]]; then
  PRIOR=$(gh api --paginate "repos/$GH_REPO/issues/$PR_NUMBER/comments" --jq '.[].body' 2>/dev/null || true)
  if ! grep -qF -- "$NOTICE_MARK" <<<"$PRIOR"; then
    NOTICE=$(printf '%s\nAUDIT_AUTOMERGE=true is accepted but not acted on in Phase 1. Automerge arrives with Phase 2, after the spike verifies how auto-merge binds to a head SHA. This PR is not merged by the audit.' "$NOTICE_MARK")
    gh api --method POST "repos/$GH_REPO/issues/$PR_NUMBER/comments" -f "body=$NOTICE" >/dev/null
  fi
fi

if [[ "$STALE" == true ]]; then
  exit 0
fi

# Labels: create them, then keep the three audit-review:* labels mutually exclusive.
for name in "$LABEL_POSITIVE" "$LABEL_CHANGES" "$LABEL_HUMAN"; do
  gh label create "$name" --force --color 0e8a16 --description 'Skill audit review' >/dev/null
done
CURRENT=$(gh pr view "$PR_NUMBER" --json labels --jq '[.labels[].name | select(startswith("audit-review:"))] | join("\n")')
REMOVE=()
while IFS= read -r existing; do
  # Only the audit-review:* family is ever removed; every other label is untouched.
  [[ "$existing" == audit-review:* ]] || continue
  if [[ "$existing" != "$LABEL" ]]; then
    REMOVE+=("$existing")
  fi
done <<<"$CURRENT"
if ((${#REMOVE[@]})); then
  for name in "${REMOVE[@]}"; do
    gh pr edit "$PR_NUMBER" --remove-label "$name" >/dev/null
  done
fi
if [[ -n "$LABEL" ]]; then
  gh pr edit "$PR_NUMBER" --add-label "$LABEL" >/dev/null
fi

gh api --method POST "repos/$GH_REPO/statuses/$HEAD_SHA" \
  -f "state=$STATUS_STATE" -f "context=$CONTEXT" \
  -f "description=Skill audit review: $OUTCOME" >/dev/null
