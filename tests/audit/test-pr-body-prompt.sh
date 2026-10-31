#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HELPER="$ROOT/.github/audit/pr-body-prompt.py"
TEMPLATE="$ROOT/.github/audit/pr-body-prompt.md"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

REPO="$TMP/repo"
git init -q "$REPO"
git -C "$REPO" config user.email test@example.com
git -C "$REPO" config user.name Test
mkdir -p "$REPO/skills/x/references"
printf 'first\n' > "$REPO/skills/x/SKILL.md"
git -C "$REPO" add skills
GIT_AUTHOR_DATE='2026-01-01T00:00:00+00:00' GIT_COMMITTER_DATE='2026-01-01T00:00:00+00:00' \
  git -C "$REPO" commit -qm base
printf 'changed\n' > "$REPO/skills/x/SKILL.md"
printf 'new\n' > "$REPO/skills/x/references/new.md"
git -C "$REPO" add -A
GIT_AUTHOR_DATE='2026-01-02T00:00:00+00:00' GIT_COMMITTER_DATE='2026-01-02T00:00:00+00:00' \
  git -C "$REPO" commit -qm 'fix(audit): apply scheduled skill audit'

cat > "$TMP/decision.json" <<'JSON'
{"update": true, "type": "fix", "title": "Apply judged audit fixes",
 "targets": ["x"], "rationale": "Judges agreed the skill drifted from the rubric."}
JSON

cd "$REPO"

# The rendered prompt carries the title, the rationale, the stat, the diff and the format.
python3 "$HELPER" prompt --template "$TEMPLATE" --decision "$TMP/decision.json" \
  --diagrams mermaid --diff-cap 61440 --out "$TMP/prompt.md"
for marker in 'PR Summary' 'Apply judged audit fixes' 'Judges agreed the skill drifted' 'skills/x/SKILL.md' 'skills/x/references/new.md' 'commit ' 'mermaid' '{{'; do
  if [ "$marker" = '{{' ]; then
    grep -qF "$marker" "$TMP/prompt.md" && { echo 'prompt left placeholders' >&2; exit 1; }
  else
    grep -qF "$marker" "$TMP/prompt.md" || { echo "prompt lost marker: $marker" >&2; exit 1; }
  fi
done

# none mode is carried into the prompt so the model omits the diagram section.
python3 "$HELPER" prompt --template "$TEMPLATE" --decision "$TMP/decision.json" \
  --diagrams none --diff-cap 61440 --out "$TMP/prompt-none.md"
grep -qF 'Diagram format' "$TMP/prompt-none.md"
tail -n 1 "$TMP/prompt-none.md" | grep -qF 'none' || { echo 'none format not carried into prompt' >&2; exit 1; }

# Literal placeholder markers inside the diff and rationale survive substitution:
# one pass over the template only, evidence text is never re-scanned or aborted on.
printf 'probe with {{EXAMPLE}} marker\n' > "$REPO/marker.txt"
git -C "$REPO" add marker.txt
GIT_AUTHOR_DATE='2026-01-03T00:00:00+00:00' GIT_COMMITTER_DATE='2026-01-03T00:00:00+00:00' \
  git -C "$REPO" commit -qm 'add marker fixture'
cat > "$TMP/decision-marker.json" <<'JSON'
{"update": true, "type": "fix", "title": "Marker decision",
 "targets": ["x"], "rationale": "Rationale cites {{EXAMPLE}} verbatim."}
JSON
python3 "$HELPER" prompt --template "$TEMPLATE" --decision "$TMP/decision-marker.json" \
  --diagrams mermaid --diff-cap 61440 --out "$TMP/prompt-marker.md"
marker_count=$(grep -cF '{{EXAMPLE}}' "$TMP/prompt-marker.md" || true)
[ "$marker_count" -ge 2 ] || { echo "literal evidence markers destroyed: $marker_count" >&2; exit 1; }

# An oversized diff is trimmed at the cap with an explicit marker.
python3 - "$REPO" <<'PY'
import sys
with open(sys.argv[1] + '/big.txt', 'w') as f:
    for i in range(20000):
        f.write(f'line {i}: some audit content to pad the diff beyond the cap\n')
PY
git -C "$REPO" add big.txt
git -C "$REPO" commit -qm 'add large fixture'
python3 "$HELPER" prompt --template "$TEMPLATE" --decision "$TMP/decision.json" \
  --diagrams mermaid --diff-cap 4096 --out "$TMP/prompt-capped.md"
size=$(wc -c < "$TMP/prompt-capped.md")
[ "$size" -lt 9000 ] || { echo "capped prompt too large: $size bytes" >&2; exit 1; }
grep -q 'diff truncated at 4096 bytes' "$TMP/prompt-capped.md" || { echo 'truncation marker missing' >&2; exit 1; }

# The fallback body is a plain summary and needs no template.
python3 "$HELPER" fallback --decision "$TMP/decision.json" --out "$TMP/fallback.md"
for marker in 'PR Summary: Apply judged audit fixes' 'Targets: x' 'Judges agreed the skill drifted' 'Diff stat'; do
  grep -qF "$marker" "$TMP/fallback.md" || { echo "fallback lost marker: $marker" >&2; exit 1; }
done
[ -s "$TMP/fallback.md" ] || { echo 'fallback body empty' >&2; exit 1; }

# Missing decision fields fail loudly.
printf '{"update":true,"type":"fix","title":"t","targets":["x"]}' > "$TMP/bad-decision.json"
if python3 "$HELPER" fallback --decision "$TMP/bad-decision.json" --out "$TMP/f2.md" 2>"$TMP/err"; then
  echo 'fallback accepted a decision without rationale' >&2
  exit 1
fi
grep -q 'missing rationale' "$TMP/err" || { echo 'decision error not surfaced' >&2; exit 1; }

# The workflow must use the body-only helpers, keep AUDIT_PR_DIAGRAMS from env,
# validate the body, and no longer install xvfb or feed the whole command file.
WF="$ROOT/.github/workflows/skill-audit.yaml"
grep -Fq '.github/audit/pr-body-prompt.py prompt' "$WF" || { echo 'workflow does not render the body prompt' >&2; exit 1; }
grep -Fq '.github/audit/pr-body-prompt.py fallback' "$WF" || { echo 'workflow lacks the fallback path' >&2; exit 1; }
grep -Fq 'AUDIT_PR_DIAGRAMS:-mermaid' "$WF" || { echo 'AUDIT_PR_DIAGRAMS no longer read from env' >&2; exit 1; }
grep -Fq 'cannot be installed reliably on a hosted runner yet (UNVERIFIED)' "$WF" || { echo 'drawio fallback warning missing' >&2; exit 1; }
grep -qF 'xvfb' "$WF" && { echo 'workflow still installs xvfb' >&2; exit 1; }
grep -qF 'explain-pr-changes.md) --diagrams' "$WF" && { echo 'workflow still feeds the command file to copilot' >&2; exit 1; }
grep -qF '[ ! -s "$RUNNER_TEMP/pr-body.md" ]' "$WF" || { echo 'workflow does not validate a non-empty body' >&2; exit 1; }

printf 'PASS PR body prompt is body-only, diff-capped, validated and falls back cleanly\n'
