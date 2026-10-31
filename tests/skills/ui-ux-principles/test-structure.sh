#!/bin/bash
# Structure test for the ui-ux-principles skill: layout files, frontmatter name, rule headings.
set -e
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
S="$ROOT/skills/ui-ux-principles"
IDS="loading responsive hierarchy tokens consistency a11y states interaction"
fail=0
need() { [ -e "$1" ] || { echo "FAIL missing: ${1#$ROOT/}" >&2; fail=1; }; }

need "$S/SKILL.md"; need "$S/README.md"
need "$S/references/frameworks.md"; need "$S/references/sources.md"
need "$S/evals/evals.json"; need "$S/evals/trigger-queries.json"
need "$S/evals/files/dashboard.tsx"; need "$S/evals/files/form.tsx"
for id in $IDS; do
  need "$S/references/rules/$id.md"
  grep -qx "## $id" "$S/SKILL.md" 2>/dev/null || { echo "FAIL SKILL.md lacks heading '## $id'" >&2; fail=1; }
  grep -q "references/rules/$id.md" "$S/SKILL.md" 2>/dev/null || { echo "FAIL SKILL.md does not link rules/$id.md" >&2; fail=1; }
done
if [ -f "$S/SKILL.md" ]; then
  name="$(sed -n '2,/^---$/p' "$S/SKILL.md" | sed -n 's/^name: *//p' | head -1 | tr -d '"')"
  [ "$name" = "ui-ux-principles" ] || { echo "FAIL frontmatter name is '$name'" >&2; fail=1; }
  [ "$(wc -l < "$S/SKILL.md")" -lt 500 ] || { echo "FAIL SKILL.md is 500 lines or more" >&2; fail=1; }
  grep -qi 'jev' "$S/SKILL.md" && { echo "FAIL SKILL.md mentions jev" >&2; fail=1; }
fi
for id in $IDS; do
  [ -f "$S/references/rules/$id.md" ] && ! grep -q "$id" "$S/references/sources.md" 2>/dev/null && { echo "FAIL sources.md has no row for $id" >&2; fail=1; }
done
[ "$fail" = 0 ] && echo "PASS ui-ux-principles structure"
exit "$fail"
