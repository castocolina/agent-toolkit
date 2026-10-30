#!/usr/bin/env bash
# Read-only PR reviewer wrapper for .github/workflows/skill-audit-review.yaml.
#
# The prompt arrives on stdin and the answer leaves on stdout. The model may read
# files and nothing else: no write tool, no shell, and no GitHub token in its
# environment. The answer is validated by review-combine.py before it is trusted.
#
# UNVERIFIED: that --allow-tool=read confines the agent in a hosted Actions
# run is not verified offline. The model knob AUDIT_REVIEW_MODEL stays empty
# until the containment drill (Phase 1 Task A3 Step 2) has passed.
set -euo pipefail
: "${AUDIT_REVIEW_MODEL:?AUDIT_REVIEW_MODEL must be set}"
: "${AUDIT_REVIEW_EFFORT:?AUDIT_REVIEW_EFFORT must be set}"
# Drop any GitHub credential the caller left in the environment: the model never gets one.
unset GH_TOKEN GITHUB_TOKEN
# Only the read tool is allowed. The shell, write and URL-fetch tools are also excluded by name, so the
# containment does not rest on the allow-list alone. UNVERIFIED: the tool names (write, web_fetch) are
# not listed by the CLI help; the containment drill (docs/audit/ci-spike.md item 11) must confirm them.
exec copilot -p "$(</dev/stdin)" -s --no-ask-user --model "$AUDIT_REVIEW_MODEL" \
  --reasoning-effort "$AUDIT_REVIEW_EFFORT" --allow-tool=read --excluded-tools shell write web_fetch
