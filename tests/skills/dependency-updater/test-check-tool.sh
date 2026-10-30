#!/bin/bash
# Tests check-tool.sh's documented installed/missing/tool-usage behavior using PATH shims.
HERE=$(cd "$(dirname "$0")" && pwd)
SCRIPT=$HERE/../../../skills/dependency-updater/scripts/check-tool.sh
FAILS=0; ROOT=$(mktemp -d); trap 'rm -rf "$ROOT"' EXIT
check() { if [ "$2" != "$3" ]; then echo "FAIL $1: got [$2] want [$3]"; FAILS=$((FAILS+1)); fi; }
mkdir -p "$ROOT/bin"
cat > "$ROOT/bin/fake-tool" <<'EOF'
#!/bin/sh
[ "$1" = --version ] && echo "fake-tool 1.2.3"
EOF
chmod +x "$ROOT/bin/fake-tool"
PATH="$ROOT/bin:$PATH" bash "$SCRIPT" fake-tool >"$ROOT/installed.out" 2>"$ROOT/installed.err"; rc=$?
check installed_rc "$rc" 0; check installed_json "$(grep -c '^{\"status\":\"ok\",\"tool\":\"fake-tool\"}$' "$ROOT/installed.out")" 1; check version "$(grep -c '^fake-tool 1.2.3$' "$ROOT/installed.err")" 1
PATH="$ROOT/bin:$PATH" bash "$SCRIPT" missing-tool 'install missing-tool' >"$ROOT/missing.out" 2>"$ROOT/missing.err"; rc=$?
check missing_rc "$rc" 1; check missing_json "$(grep -c '^{\"status\":\"missing\",\"tool\":\"missing-tool\",\"install\":\"install missing-tool\"}$' "$ROOT/missing.out")" 1
PATH="$ROOT/bin:$PATH" bash "$SCRIPT" missing-tool >"$ROOT/no-hint.out" 2>"$ROOT/no-hint.err"; rc=$?
check missing_without_hint_rc "$rc" 1; check no_hint_json "$(grep -c '^{\"status\":\"missing\",\"tool\":\"missing-tool\",\"install\":\"\"}$' "$ROOT/no-hint.out")" 1
PATH="$ROOT/bin:$PATH" bash "$SCRIPT" >"$ROOT/usage.out" 2>"$ROOT/usage.err"; rc=$?
check no_arg_rc "$rc" 1; check usage_json "$(grep -c '^{\"status\":\"error\",\"diagnostic\":\"tool name is required\"}$' "$ROOT/usage.out")" 1
PATH="$ROOT/bin:$PATH" bash "$SCRIPT" --help >"$ROOT/help.out" 2>"$ROOT/help.err"; rc=$?
check help_rc "$rc" 0; check help_usage "$(grep -c '^Usage: check-tool.sh' "$ROOT/help.err")" 1
[ "$FAILS" = 0 ] || exit 1
echo 'PASS test_check_tool_documented_paths'
