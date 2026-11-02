#!/bin/bash
# Structure test for the skill-updater skill: layout files and frontmatter name.
set -e
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
S="$ROOT/skills/skill-updater"
fail=0
need() { [ -e "$1" ] || { echo "FAIL missing: ${1#$ROOT/}" >&2; fail=1; }; }

need "$S/SKILL.md"
need "$S/README.md"
need "$S/evals/evals.json"
need "$S/evals/trigger-queries.json"
need "$S/evals/files/registry-moved-path.json"
need "$S/evals/files/registry-current.json"
need "$S/evals/files/registry-deleted-path.json"
need "$S/evals/files/registry-several-candidates.json"
if [ -f "$S/SKILL.md" ]; then
  name="$(sed -n '2,/^---$/p' "$S/SKILL.md" | sed -n 's/^name: *//p' | head -1 | tr -d '"')"
  [ "$name" = "skill-updater" ] || { echo "FAIL frontmatter name is '$name'" >&2; fail=1; }
  grep -qi 'jev' "$S/SKILL.md" && { echo "FAIL SKILL.md mentions jev" >&2; fail=1; }
fi
[ "$fail" = 0 ] && echo "PASS skill-updater structure"
exit "$fail"
