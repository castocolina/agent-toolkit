#!/bin/bash
# Pointer checks: explain-pr-changes must point at the mermaid-diagrams rules, and the plugin must ship them.
set -e
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
cd "$ROOT"
RULES=skills/mermaid-diagrams/references/authoring-rules.md

n=$(grep -o -F "$RULES" commands/explain-pr-changes.md | wc -l)  # grep, not rg: CI runners lack rg
[ "$n" -eq 2 ] || { echo "FAIL: expected 2 pointers in commands/explain-pr-changes.md, got $n"; exit 1; }
[ -f "$RULES" ] || { echo "FAIL: missing $RULES"; exit 1; }
DIST=dist/plugins/command-explain-pr-changes/$RULES
[ -f "$DIST" ] || { echo "FAIL: missing $DIST (run scripts/build_plugins.py)"; exit 1; }
echo "PASS test-pointers"
