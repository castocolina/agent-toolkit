#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
RENDER="$ROOT/.github/audit/render-prompt.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
WS="$TMP/workspace"
mkdir -p "$WS/merged" "$WS/.audit-evidence/evals-results" "$WS/audit-pages" "$TMP/outside"
printf 'spec diff' > "$WS/.audit-evidence/spec.diff"
printf '[]' > "$WS/.audit-evidence/upstreams.json"
printf '{}' > "$WS/.audit-evidence/check.json"
printf 'results' > "$WS/.audit-evidence/evals-results/summary.json"
printf '{"update":false}' > "$WS/merged/merged.json"
# apply restores the evidence bundle flat into .audit-evidence/ (merged.json, check.json, ...).
printf '{"update":false}' > "$WS/.audit-evidence/merged.json"
printf '{"changed":[],"removed_pages":["skill-creation/old-page"],"new_pages":[],"rubric_stale":false,"structure_changed":true}' > "$WS/.audit-evidence/fetch-result.json"
printf '[{"page":"skill-creation/new-page","raw":"skill-creation/new-page.mdx","mapped":false}]' > "$WS/audit-pages/pages.json"
printf 'secret' > "$TMP/outside/evidence.txt"

# upload-artifact skips empty directories, so a run without approvals restores the
# evidence bundle WITHOUT .audit-evidence/approved-evidence. The fixture starts that
# way; the workflow recreates the directory with mkdir before any --path render.
cd "$WS"
if [ -e "$WS/.audit-evidence/approved-evidence" ]; then
  echo 'fixture must start without approved-evidence (artifact round trip)' >&2
  exit 1
fi

# Render the real merge prompt exactly like the workflow does (--path, which requires
# the directory). Without the recreated directory the render must fail: that is the bug.
if python3 "$RENDER" "$ROOT/.github/audit/merge-prompt.md" "$TMP/merge-missing.md" \
    --path MERGED_JSON=merged/merged.json \
    --path SPEC_DIFF=.audit-evidence/spec.diff \
    --path UPSTREAMS_JSON=.audit-evidence/upstreams.json \
    --path EVALS_RESULTS=.audit-evidence/evals-results \
    --path CHECK_JSON=.audit-evidence/check.json \
    --path APPROVED_EVIDENCE=.audit-evidence/approved-evidence \
    --out-path DECISION_JSON=decision.json \
    --text QUALITY_FAILED=false \
    --text APPROVED_UPSTREAMS='' 2>"$TMP/missing-err"; then
  echo 'merge render succeeded without the recreated approved-evidence directory' >&2
  exit 1
fi
grep -q 'approved-evidence' "$TMP/missing-err" || { echo 'missing approved-evidence error not surfaced' >&2; exit 1; }

# The workflow recreates the directory, then renders.
mkdir -p .audit-evidence/approved-evidence
if python3 "$RENDER" "$ROOT/.github/audit/merge-prompt.md" "$TMP/merge-rendered.md" \
    --path MERGED_JSON=merged/merged.json \
    --path SPEC_DIFF=.audit-evidence/spec.diff \
    --path UPSTREAMS_JSON=.audit-evidence/upstreams.json \
    --path EVALS_RESULTS=.audit-evidence/evals-results \
    --path CHECK_JSON=.audit-evidence/check.json \
    --path APPROVED_EVIDENCE=.audit-evidence/approved-evidence \
    --out-path DECISION_JSON=decision.json \
    --text QUALITY_FAILED=false \
    --text APPROVED_UPSTREAMS=''; then
  :
else
  echo 'merge prompt render unexpectedly failed' >&2
  exit 1
fi
grep -q '{{' "$TMP/merge-rendered.md" && { echo 'merge render left placeholders' >&2; exit 1; }
for marker in '.audit-evidence/evals-results' '.audit-evidence/spec.diff' '.audit-evidence/upstreams.json' '.audit-evidence/check.json' 'merged/merged.json' '.audit-evidence/approved-evidence'; do
  grep -qF "$marker" "$TMP/merge-rendered.md" || { echo "merge render lost $marker" >&2; exit 1; }
done
# Every absolute path in the rendered prompt must stay inside the workspace.
python3 - "$TMP/merge-rendered.md" "$WS" <<'PY'
import re, sys
text = open(sys.argv[1], encoding='utf-8').read()
workspace = sys.argv[2].rstrip('/') + '/'
tokens = re.findall(r'(?<![\w.:])/[A-Za-z0-9_./-]+', re.sub(r'https?://\S+', ' ', text))
outside = [t for t in tokens if not t.startswith(workspace)]
if outside:
    print('paths outside the workspace: %s' % sorted(set(outside)), file=sys.stderr)
    raise SystemExit(1)
PY
if grep -qF "$TMP/outside" "$TMP/merge-rendered.md"; then
  echo 'merge render referenced the outside fixture' >&2
  exit 1
fi


# The fix prompt must reference the decision inside the workspace, not $RUNNER_TEMP.
printf '{"update":true,"targets":["skill-judge"]}' > "$WS/.audit-evidence/decision.json"
if python3 "$RENDER" "$ROOT/.github/audit/fix-prompt.md" "$TMP/fix-rendered.md" \
    --path DECISION_JSON=.audit-evidence/decision.json \
    --path MERGED_JSON=.audit-evidence/merged.json \
    --path CHECK_JSON=.audit-evidence/check.json \
    --path SPEC_DIFF=.audit-evidence/spec.diff \
    --path APPROVED_EVIDENCE=.audit-evidence/approved-evidence \
    --text TARGETS='skill-judge'; then
  :
else
  echo 'fix prompt render unexpectedly failed' >&2
  exit 1
fi
for marker in '.audit-evidence/decision.json' '.audit-evidence/merged.json' '.audit-evidence/check.json' '.audit-evidence/spec.diff' '.audit-evidence/approved-evidence'; do
  grep -qF "$marker" "$TMP/fix-rendered.md" || { echo "fix render lost $marker" >&2; exit 1; }
done

# The rubric prompt is rendered exactly like the workflow renders it, with the
# structure flag, the new/removed page lists and the excluded evidence paths.
if python3 "$RENDER" "$ROOT/.github/audit/rubric-prompt.md" "$TMP/rubric-rendered.md" \
    --path PAGES_JSON=audit-pages/pages.json \
    --path FETCH_RESULT=.audit-evidence/fetch-result.json \
    --path SPEC_DIFF=.audit-evidence/spec.diff \
    --text STRUCTURE_CHANGED=true \
    --text NEW_PAGES='["skill-creation/new-page"]' \
    --text REMOVED_PAGES='["skill-creation/old-page"]'; then
  :
else
  echo 'rubric prompt render unexpectedly failed' >&2
  exit 1
fi
grep -q '{{' "$TMP/rubric-rendered.md" && { echo 'rubric render left placeholders' >&2; exit 1; }
for marker in 'STRUCTURE_CHANGED=true' '["skill-creation/new-page"]' '["skill-creation/old-page"]'; do
  grep -qF "$marker" "$TMP/rubric-rendered.md" || { echo "rubric render lost $marker" >&2; exit 1; }
done
# Every absolute path in the rendered rubric prompt must stay inside the workspace.
python3 - "$TMP/rubric-rendered.md" "$WS" <<'PY'
import re, sys
text = open(sys.argv[1], encoding='utf-8').read()
workspace = sys.argv[2].rstrip('/') + '/'
tokens = re.findall(r'(?<![\w.:])/[A-Za-z0-9_./-]+', re.sub(r'https?://\S+', ' ', text))
outside = [t for t in tokens if not t.startswith(workspace)]
if outside:
    print('rubric paths outside the workspace: %s' % sorted(set(outside)), file=sys.stderr)
    raise SystemExit(1)
PY

expect_fail() {
  local label=$1
  shift
  if python3 "$RENDER" "$@" >"$TMP/out" 2>"$TMP/err"; then
    printf '%s: render unexpectedly succeeded\n' "$label" >&2
    exit 1
  fi
}

# Missing evidence file fails.
rm "$WS/.audit-evidence/upstreams.json"
expect_fail 'missing evidence path' "$ROOT/.github/audit/merge-prompt.md" "$TMP/o.md" \
  --path UPSTREAMS_JSON=.audit-evidence/upstreams.json --text QUALITY_FAILED=false
grep -q 'does not exist' "$TMP/err" || { echo 'missing-path error not surfaced' >&2; exit 1; }
printf '[]' > "$WS/.audit-evidence/upstreams.json"

# Paths outside the workspace fail even when they exist.
expect_fail 'evidence outside workspace' "$ROOT/.github/audit/merge-prompt.md" "$TMP/o.md" \
  --path UPSTREAMS_JSON="$TMP/outside/evidence.txt"
grep -q 'outside the workspace' "$TMP/err" || { echo 'outside-workspace error not surfaced' >&2; exit 1; }

# Unresolvable placeholders fail closed.
printf 'use {{UNKNOWN}} now' > "$WS/broken.md"
expect_fail 'unknown placeholder' "$WS/broken.md" "$TMP/o.md"
grep -q 'unresolved placeholders' "$TMP/err" || { echo 'placeholder error not surfaced' >&2; exit 1; }

# Output paths may not exist yet but must stay inside the workspace.
printf 'write to {{TARGET}}' > "$WS/ok.md"
python3 "$RENDER" "$WS/ok.md" "$TMP/o.md" --out-path TARGET=decision.json
grep -qF "$WS/decision.json" "$TMP/o.md" || { echo 'out-path not absolutized' >&2; exit 1; }
if python3 "$RENDER" "$WS/ok.md" "$TMP/o.md" --out-path TARGET="$TMP/outside/evidence.txt" 2>"$TMP/err"; then
  echo 'out-path outside workspace unexpectedly succeeded' >&2
  exit 1
fi


# The workflow must render both prompts through the helper with evidence copied
# into the excluded workspace directory, never from $RUNNER_TEMP.
WF="$ROOT/.github/workflows/skill-audit.yaml"
grep -Fq 'render-prompt.py" .github/audit/merge-prompt.md' "$WF" || { echo 'merge render not via helper' >&2; exit 1; }
grep -Fq 'render-prompt.py" .github/audit/fix-prompt.md' "$WF" || { echo 'fix render not via helper' >&2; exit 1; }
grep -Fq 'render-prompt.py" .github/audit/rubric-prompt.md' "$WF" || { echo 'rubric render not via helper' >&2; exit 1; }
if grep -qE 'python3 \.github/audit/render-prompt\.py' "$WF"; then echo 'a render still runs the checkout render-prompt.py' >&2; exit 1; fi
grep -Fq '.audit-evidence/evals-results' "$WF" || { echo 'evals results not copied into workspace evidence' >&2; exit 1; }
grep -Fq '.audit-evidence/decision.json' "$WF" || { echo 'decision not copied into workspace evidence' >&2; exit 1; }
grep -Fq 'echo .audit-evidence/ >> .git/info/exclude' "$WF" || { echo 'evidence dir not git-excluded' >&2; exit 1; }
if grep -qE 'EVALS_RESULTS=.*RUNNER_TEMP' "$WF" || grep -qE 'DECISION_JSON=.*RUNNER_TEMP' "$WF"; then
  echo 'prompt paths still rendered from RUNNER_TEMP' >&2
  exit 1
fi

printf 'PASS prompt rendering keeps every evidence path existing and inside the workspace\n'
