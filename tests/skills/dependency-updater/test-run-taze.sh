#!/bin/bash
# Tests run-taze.sh with a PATH shim; never invokes a real package manager/service.
HERE=$(cd "$(dirname "$0")" && pwd)
SCRIPT=$HERE/../../../skills/dependency-updater/scripts/run-taze.sh
BASH=$(command -v bash)
READLINK=$(command -v readlink)
MKDIR=$(command -v mkdir)
GREP=$(command -v grep)
CAT=$(command -v cat)
BASENAME=$(command -v basename)
FAILS=0; ROOT=$(mktemp -d); trap 'rm -rf "$ROOT"' EXIT
check() { if [ "$2" != "$3" ]; then echo "FAIL $1: got [$2] want [$3]"; FAILS=$((FAILS+1)); fi; }
mkdir -p "$ROOT/bin" "$ROOT/work" "$ROOT/no-package"
for tool in "$BASH" "$READLINK" "$MKDIR" "$GREP" "$CAT" "$BASENAME"; do ln -s "$tool" "$ROOT/bin/$(basename "$tool")"; done
cat > "$ROOT/bin/taze" <<'EOF'
#!/bin/bash
printf '%s\n' "$*" >> "$TAZE_LOG"
EOF
chmod +x "$ROOT/bin/taze"
printf '{"name":"fixture"}\n' > "$ROOT/work/package.json"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" "$BASH" "$SCRIPT" -r --write) >"$ROOT/success.out" 2>&1; rc=$?
check success_rc "$rc" 0; check success_json "$(grep -Fc '"status": "ok"' "$ROOT/success.out")" 1; check args "$(cat "$ROOT/argv")" '-r --write'
(cd "$ROOT/no-package" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" "$BASH" "$SCRIPT") >"$ROOT/no-package.out" 2>"$ROOT/no-package.err"; rc=$?
check missing_package_rc "$rc" 2; check missing_package_json "$(grep -Foc '"diagnostic":"No package.json found in current directory"' "$ROOT/no-package.out")" 1
mv "$ROOT/bin/taze" "$ROOT/bin/taze.disabled"
(cd "$ROOT/work" && PATH="$ROOT/bin" TAZE_LOG="$ROOT/argv" "$BASH" "$SCRIPT") >"$ROOT/no-taze.out" 2>"$ROOT/no-taze.err"; rc=$?
check missing_taze_rc "$rc" 1; check missing_taze_json "$(grep -Foc '"diagnostic":"taze is not installed"' "$ROOT/no-taze.out")" 1
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" "$BASH" "$SCRIPT" --help) >"$ROOT/help.out" 2>"$ROOT/help.err"; rc=$?
check help_rc "$rc" 0; check help_usage "$(grep -c '^Usage: run-taze.sh' "$ROOT/help.err")" 1
[ "$FAILS" = 0 ] || exit 1
echo 'PASS test_run_taze_documented_paths'
