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
if [ -n "$TAZE_OUT" ]; then printf '%s\n' "$TAZE_OUT"; fi
EOF
chmod +x "$ROOT/bin/taze"
printf '{"name":"fixture"}\n' > "$ROOT/work/package.json"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" "$BASH" "$SCRIPT" -r --write) >"$ROOT/success.out" 2>&1; rc=$?
check success_rc "$rc" 0; check success_json "$(grep -Fc '"status": "ok"' "$ROOT/success.out")" 1; check args "$(cat "$ROOT/argv")" '-r --write'
python3 -c 'import json,sys; json.load(sys.stdin)' < "$ROOT/success.out"; check success_valid_json "$?" 0
check no_here_string "$(grep -c '<<<' "$SCRIPT")" 0
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='{"packages":[{"name":"left-pad"}]}' "$BASH" "$SCRIPT" -r) >"$ROOT/scan.out" 2>&1; rc=$?
check scan_rc "$rc" 0; check scan_args "$(cat "$ROOT/argv")" '-r --json'
check scan_candidates "$(python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["candidates"]["packages"][0]["name"], "output" in d)' < "$ROOT/scan.out")" 'left-pad False'
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='left-pad 1.0.0 -> 1.1.0' "$BASH" "$SCRIPT") >"$ROOT/text.out" 2>&1; rc=$?
check text_rc "$rc" 0
check text_fallback "$(python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["output"].strip(), "candidates" in d)' < "$ROOT/text.out")" 'left-pad 1.0.0 -> 1.1.0 False'
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='{"a":1}' "$BASH" "$SCRIPT" --json) >"$ROOT/json-flag.out" 2>&1; rc=$?
check json_flag_args "$(cat "$ROOT/argv")" '--json'
check json_flag_candidates "$(python3 -c 'import json,sys; print(json.load(sys.stdin)["candidates"]["a"])' < "$ROOT/json-flag.out")" 1
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='{"a":1}' "$BASH" "$SCRIPT" -w) >"$ROOT/write.out" 2>&1; rc=$?
check write_short_args "$(cat "$ROOT/argv")" '-w'
check write_keeps_text "$(python3 -c 'import json,sys; d=json.load(sys.stdin); print("candidates" in d, "output" in d)' < "$ROOT/write.out")" 'False True'
for combo in -i -I -u --install --update --interactive; do
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='{"a":1}' "$BASH" "$SCRIPT" "$combo") >"$ROOT/write$combo.out" 2>&1; rc=$?
check "write_interactive_${combo}_args" "$(cat "$ROOT/argv")" "$combo"
check "write_interactive_${combo}_keeps_text" "$(python3 -c 'import json,sys; d=json.load(sys.stdin); print("candidates" in d, "output" in d)' < "$ROOT/write$combo.out")" 'False True'
done
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='{"a":1}' "$BASH" "$SCRIPT" -u --json) >"$ROOT/update-json.out" 2>&1; rc=$?
check update_json_args "$(cat "$ROOT/argv")" '-u --json'
check update_json_keeps_text "$(python3 -c 'import json,sys; d=json.load(sys.stdin); print("candidates" in d, "output" in d)' < "$ROOT/update-json.out")" 'False True'
for combo in -rw -wr; do
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='{"a":1}' "$BASH" "$SCRIPT" "$combo") >"$ROOT/write$combo.out" 2>&1; rc=$?
check "write_cluster_${combo}_args" "$(cat "$ROOT/argv")" "$combo"
check "write_cluster_${combo}_keeps_text" "$(python3 -c 'import json,sys; d=json.load(sys.stdin); print("candidates" in d, "output" in d)' < "$ROOT/write$combo.out")" 'False True'
done
for combo in --write=true --update=true --install=true --interactive=true; do
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='{"a":1}' "$BASH" "$SCRIPT" "$combo") >"$ROOT/write$combo.out" 2>&1; rc=$?
check "write_equals_${combo}_rc" "$rc" 0
check "write_equals_${combo}_args" "$(cat "$ROOT/argv")" "$combo"
check "write_equals_${combo}_keeps_text" "$(python3 -c 'import json,sys; d=json.load(sys.stdin); print("candidates" in d, "output" in d)' < "$ROOT/write$combo.out")" 'False True'
done
for combo in --global --global=true -g -rg -gr; do
: > "$ROOT/argv"
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" TAZE_OUT='{"a":1}' "$BASH" "$SCRIPT" "$combo") >"$ROOT/global$combo.out" 2>"$ROOT/global$combo.err"; rc=$?
check "global_${combo}_rc" "$rc" 2
check "global_${combo}_taze_not_run" "$(cat "$ROOT/argv")" ""
check "global_${combo}_json" "$(python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["status"], "out of scope" in d["diagnostic"])' < "$ROOT/global$combo.out")" 'error True'
done
check help_documents_global "$(PATH="$ROOT/bin:/usr/bin:/bin" "$BASH" "$SCRIPT" --help 2>&1 | grep -c '^Rejected: --global')" 1
(cd "$ROOT/work" && PATH="$ROOT/bin" TAZE_LOG="$ROOT/argv" "$BASH" "$SCRIPT") >"$ROOT/no-python.out" 2>"$ROOT/no-python.err"; rc=$?
check missing_python_rc "$rc" 3; check missing_python_json "$(grep -Foc '"diagnostic":"python3 is not installed"' "$ROOT/no-python.out")" 1
python3 -c 'import json,sys; json.load(sys.stdin)' < "$ROOT/no-python.out"; check missing_python_valid_json "$?" 0
(cd "$ROOT/no-package" && PATH="$ROOT/bin:/usr/bin:/bin" TAZE_LOG="$ROOT/argv" "$BASH" "$SCRIPT") >"$ROOT/no-package.out" 2>"$ROOT/no-package.err"; rc=$?
check missing_package_rc "$rc" 2; check missing_package_json "$(grep -Foc '"diagnostic":"No package.json found in current directory"' "$ROOT/no-package.out")" 1
mv "$ROOT/bin/taze" "$ROOT/bin/taze.disabled"
(cd "$ROOT/work" && PATH="$ROOT/bin" TAZE_LOG="$ROOT/argv" "$BASH" "$SCRIPT") >"$ROOT/no-taze.out" 2>"$ROOT/no-taze.err"; rc=$?
check missing_taze_rc "$rc" 1; check missing_taze_json "$(grep -Foc '"diagnostic":"taze is not installed"' "$ROOT/no-taze.out")" 1
(cd "$ROOT/work" && PATH="$ROOT/bin:/usr/bin:/bin" "$BASH" "$SCRIPT" --help) >"$ROOT/help.out" 2>"$ROOT/help.err"; rc=$?
check help_rc "$rc" 0; check help_usage "$(grep -c '^Usage: run-taze.sh' "$ROOT/help.err")" 1
[ "$FAILS" = 0 ] || exit 1
echo 'PASS test_run_taze_documented_paths'
