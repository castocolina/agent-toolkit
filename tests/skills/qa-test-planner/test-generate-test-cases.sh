#!/bin/bash
# Tests for skills/qa-test-planner/scripts/generate_test_cases.sh.
#
# Pins the behavior documented in the qa-test-planner SKILL.md/README: the
# interactive generator produces a readable Markdown test case with its
# priority, type, objective, preconditions, action/expected steps, test data,
# edge cases, related tests and notes. UI tests with a Figma URL also include
# the visual-validation section.
HERE=$(cd "$(dirname "$0")" && pwd)
SCRIPT=$HERE/../../../skills/qa-test-planner/scripts/generate_test_cases.sh
FAILS=0 TMPS=()
trap 'rm -rf "${TMPS[@]}"' EXIT

check() {
  if [ "$2" != "$3" ]; then echo "  FAIL: $1: got [$2] want [$3]"; FAILS=$((FAILS + 1)); TESTFAIL=1; fi
}
t() {
  TESTFAIL=0; "$1"
  if [ $TESTFAIL = 0 ]; then echo "PASS $1"; else echo "FAIL $1"; fi
}

new_sandbox() { # tmp dir with a fixed `date` shim on PATH
  root=$(mktemp -d); TMPS+=("$root")
  mkdir -p "$root/bin"
  cat > "$root/bin/date" << 'EOF'
#!/bin/bash
case "$1" in
  +%Y-%m-%d) echo "2026-01-20" ;;
  *) command -p date "$@" ;;
esac
EOF
  chmod +x "$root/bin/date"
  printf '%s' "$root"
}

run_case() { # run_case <sandbox> <stdin-file> [output-dir]
  local root=$1 stdin_file=$2 out_dir=${3:-$1/out}
  mkdir -p "$out_dir"
  (cd "$root" && PATH="$root/bin:$PATH" bash "$SCRIPT" "$out_dir") \
    <"$stdin_file" >"$root/stdout" 2>"$root/stderr"
}

test_functional_test_case_markdown() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
TC-LOGIN-001
Login flow works
2
1
30
Verify the login page
Guards against login regressions
User has an account
User is on the login page

Open the login page
Login page loads
Submit valid credentials
Dashboard appears
done
sample user
Boundary: empty password
TC-000-9
Created during sprint review
EOF
  run_case "$root" "$root/stdin"
  check exit "$?" 0
  check file_name "$([ -f "$root/out/TC-LOGIN-001.md" ] && echo yes || echo no)" yes
  local report="$root/out/TC-LOGIN-001.md"
  check title "$(grep -c '# TC-LOGIN-001: Login flow works' "$report")" 1
  check priority "$(grep -c '^\*\*Priority:\*\* P1 (High)$' "$report")" 1
  check type "$(grep -c '^\*\*Type:\*\* Functional$' "$report")" 1
  check status "$(grep -c '^\*\*Status:\*\* Not Run$' "$report")" 1
  check est_time "$(grep -c '^\*\*Estimated Time:\*\* 30 minutes$' "$report")" 1
  check created "$(grep -c '^\*\*Created:\*\* 2026-01-20$' "$report")" 1
  check objective "$(grep -c '^Verify the login page$' "$report")" 1
  check why "$(grep -c '^\*\*Why this matters:\*\* Guards against login regressions$' "$report")" 1
  check precondition1_own_line "$(grep -c '^- User has an account$' "$report")" 1
  check precondition2_own_line "$(grep -c '^- User is on the login page$' "$report")" 1
  check step1_own_line "$(grep -c '^1\. Open the login page$' "$report")" 1
  check step1_expected "$(grep -c '^   \*\*Expected:\*\* Login page loads$' "$report")" 1
  check step2_own_line "$(grep -c '^2\. Submit valid credentials$' "$report")" 1
  check step2_expected "$(grep -c '^   \*\*Expected:\*\* Dashboard appears$' "$report")" 1
  check test_data "$(grep -c '^sample user$' "$report")" 1
  check edge_cases "$(grep -c '^Boundary: empty password$' "$report")" 1
  check related "$(grep -c '^TC-000-9$' "$report")" 1
  check notes "$(grep -c '^Created during sprint review$' "$report")" 1
  check no_figma_section "$(grep -c '^## Visual Validation (Figma)$' "$report")" 0
  check success_msg "$(grep -c 'Test case generated successfully' "$root/stdout")" 1
}

test_ui_test_case_gets_figma_section() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
TC-UI-002
Login page visuals
1
2
45
Pixel-check the login page
Match the Figma design

Open the login page
Page renders
done

https://figma.example.com/file/login
Buttons, inputs, spacing



EOF
  run_case "$root" "$root/stdin"
  check exit "$?" 0
  check file_name "$([ -f "$root/out/TC-UI-002.md" ] && echo yes || echo no)" yes
  local report="$root/out/TC-UI-002.md"
  check priority "$(grep -c '^\*\*Priority:\*\* P0 (Critical)$' "$report")" 1
  check type "$(grep -c '^\*\*Type:\*\* UI/Visual$' "$report")" 1
  check figma_section "$(grep -c '^## Visual Validation (Figma)$' "$report")" 1
  check figma_url "$(grep -c '^\*\*Design Reference:\*\* https://figma.example.com/file/login$' "$report")" 1
  check visual_checks "$(grep -c '^Buttons, inputs, spacing$' "$report")" 1
  check checklist "$(grep -c '^- \[ \] Layout matches Figma design$' "$report")" 1
  check figma_hint "$(grep -c 'Validate against Figma design' "$root/stdout")" 1
}

test_id_is_sanitized_but_extension_kept() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
TC LOGIN 002
Sanitized ID case
3
1

Verify sanitization


Step one
Works
done





EOF
  run_case "$root" "$root/stdin"
  check exit "$?" 0
  check sanitized_file "$([ -f "$root/out/TCLOGIN002.md" ] && echo yes || echo no)" yes
  check markdown_extension "$([ -f "$root/out/TCLOGIN002md" ] && echo yes || echo no)" no
  check title "$(grep -c '# TC LOGIN 002: Sanitized ID case' "$root/out/TCLOGIN002.md")" 1
}

test_rerun_preserves_existing_case_unless_overwrite_requested() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
TC-COLLIDE-001
Original title
2
1

Original objective



done






EOF
  run_case "$root" "$root/stdin"
  local report="$root/out/TC-COLLIDE-001.md"
  check initial_exit "$?" 0
  printf 'original sentinel\n' >> "$report"
  run_case "$root" "$root/stdin"
  check collision_exit "$?" 1
  check preserved "$(grep -c '^original sentinel$' "$report")" 1
  check actionable "$(grep -c -- '--overwrite to replace it' "$root/stderr")" 1
}

test_output_defaults_to_current_directory() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
TC-LOGIN-003
Default dir case
2
1

Verify default output dir


Step one
Works
done





EOF
  (cd "$root" && PATH="$root/bin:$PATH" bash "$SCRIPT") \
    <"$root/stdin" >"$root/stdout" 2>"$root/stderr"
  check exit "$?" 0
  check file "$([ -f "$root/TC-LOGIN-003.md" ] && echo yes || echo no)" yes
}

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
