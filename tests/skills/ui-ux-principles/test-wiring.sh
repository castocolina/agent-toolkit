#!/bin/bash
# Wiring test: mui and design-system-starter each name ui-ux-principles once and copy no rule text.
set -e
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
COPIED="one primary action per view"
fail=0

check() { # check REL
  local f="$ROOT/$1" n
  if [ ! -f "$f" ]; then echo "FAIL missing: $1" >&2; fail=1; return; fi
  n="$(grep -o 'ui-ux-principles' "$f" | wc -l)"
  [ "$n" = 1 ] || { echo "FAIL $1 names ui-ux-principles $n times, want 1" >&2; fail=1; }
  if grep -qF "$COPIED" "$f"; then echo "FAIL $1 copies rule text" >&2; fail=1; fi
}

check skills/mui/SKILL.md
check skills/design-system-starter/SKILL.md
[ "$fail" = 0 ] && echo "PASS ui-ux-principles wiring"
exit "$fail"
