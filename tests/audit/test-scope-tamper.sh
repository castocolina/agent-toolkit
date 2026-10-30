#!/usr/bin/env bash
# Tamper regression for the model-tampering guard: the scope gate must come from a
# trusted copy, so a model that replaces the checkout's scope-check.py with an
# always-success script cannot widen the scope. Also covers the decision: a model
# that rewrites the workspace decision.json cannot widen the fixer allowlist when
# the gate reads the untouched downloaded decision.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
SCOPE="$ROOT/.github/audit/scope-check.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# A scratch checkout: the trusted copy is taken from the real tooling, then the
# checkout is attacked, exactly as the workflow's job sequence allows.
CHECKOUT="$TMP/checkout"
TRUSTED="$TMP/runner-temp/trusted"
DECISION_DIR="$TMP/runner-temp/decision"
mkdir -p "$CHECKOUT/.github/audit" "$TRUSTED" "$DECISION_DIR" "$CHECKOUT/skills/alpha"
cp "$SCOPE" "$TRUSTED/scope-check.py"
printf '{"update":true,"type":"fix","title":"t","targets":["alpha"],"rationale":"r"}' > "$DECISION_DIR/decision.json"
cp "$DECISION_DIR/decision.json" "$TMP/decision-untouched.json"

cd "$CHECKOUT"
git init -q .
git -c user.email=a@b -c user.name=n commit -q --allow-empty -m init
cp "$SCOPE" .github/audit/scope-check.py
printf 'x\n' > skills/alpha/SKILL.md
git add -A && git -c user.email=a@b -c user.name=n commit -q -m base
# An out-of-scope edit the model is not allowed to make.
mkdir -p scripts && printf 'evil\n' > scripts/evil.sh

# 1. The model replaces the checkout's gate with an always-success script.
printf '#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n' > .github/audit/scope-check.py

# The trusted copy is what the workflow invokes, and it must still reject the edit.
if git -c core.quotePath=false status --porcelain=v2 --untracked-files=all \
    | python3 "$TRUSTED/scope-check.py" fixer --decision "$DECISION_DIR/decision.json" --format porcelain-v2 --skip-staged 2>"$TMP/err"; then
  echo 'trusted scope gate accepted an out-of-scope edit made after a tampered checkout' >&2
  exit 1
fi
grep -q 'scripts/evil.sh' "$TMP/err" || { echo 'trusted gate did not name the out-of-scope path' >&2; exit 1; }

# 2. The model rewrites the workspace decision to widen the allowlist. The gate
#    reads the untouched download, so the out-of-scope edit is still rejected.
mkdir -p "$CHECKOUT/.audit-evidence"
echo .audit-evidence/ >> "$CHECKOUT/.git/info/exclude"
printf '{"update":true,"type":"fix","title":"t","targets":["alpha","scripts"],"rationale":"r"}' > "$CHECKOUT/.audit-evidence/decision.json"
if git -c core.quotePath=false status --porcelain=v2 --untracked-files=all \
    | python3 "$TRUSTED/scope-check.py" fixer --decision "$DECISION_DIR/decision.json" --format porcelain-v2 --skip-staged 2>"$TMP/err2"; then
  echo 'a workspace decision that widens the allowlist was trusted' >&2
  exit 1
fi
cmp -s "$DECISION_DIR/decision.json" "$TMP/decision-untouched.json" || { echo 'the untouched decision was modified' >&2; exit 1; }

# 3. Only a genuinely in-scope edit passes the trusted gate: clean up the attack first.
rm -f scripts/evil.sh
git checkout -q -- .github/audit/scope-check.py
printf 'edit\n' > skills/alpha/SKILL.md
git -c core.quotePath=false status --porcelain=v2 --untracked-files=all \
  | python3 "$TRUSTED/scope-check.py" fixer --decision "$DECISION_DIR/decision.json" --format porcelain-v2 --skip-staged 2>/dev/null \
  || { echo 'the trusted gate rejected an in-scope target edit' >&2; exit 1; }

printf 'PASS scope gate from the trusted copy rejects tampered-checkout and widened-decision edits\n'
