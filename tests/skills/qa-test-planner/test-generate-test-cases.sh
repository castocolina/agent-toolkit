#!/bin/bash
# Tests for skills/qa-test-planner/scripts/generate_test_cases.sh.
#
# Pins the behavior documented in SKILL.md and --help: interactively (no field
# flag) or from flags (never prompts), the generator writes a Markdown test case
# with its priority, type, objective, preconditions, action/expected steps, test
# data, edge cases, related tests and notes, and prints one JSON manifest line on
# stdout. UI tests with a Figma URL also include the visual-validation section.
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
  check success_msg "$(grep -c 'Test case generated successfully' "$root/stderr")" 1
  check manifest "$(cat "$root/stdout")" "{\"status\":\"created\",\"id\":\"TC-LOGIN-001\",\"file\":\"$root/out/TC-LOGIN-001.md\"}"
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
  check figma_hint "$(grep -c 'Validate against Figma design' "$root/stderr")" 1
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

test_out_of_range_priority_and_type_are_not_guessed() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
TC-OOR-001
Out of range answers
9
9

Verify unrecognized answers

Step one
Works
done





EOF
  run_case "$root" "$root/stdin"
  check exit "$?" 0
  local report="$root/out/TC-OOR-001.md"
  check priority "$(grep -c '^\*\*Priority:\*\* Untriaged$' "$report")" 1
  check type "$(grep -c '^\*\*Type:\*\* Unknown$' "$report")" 1
  check no_guessed_priority "$(grep -c 'P2 (Medium)' "$report")" 0
  check no_guessed_type "$(grep -c '^\*\*Type:\*\* Functional$' "$report")" 0
  check oq_priority "$(grep -c '^- Priority: Untriaged$' "$report")" 1
  check oq_type "$(grep -c '^- Type: Unknown$' "$report")" 1
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

run_flags() { # run_flags <sandbox> <args...>; never reads stdin
  local root=$1; shift
  mkdir -p "$root/out"
  (cd "$root" && PATH="$root/bin:$PATH" bash "$SCRIPT" "$@") \
    </dev/null >"$root/stdout" 2>"$root/stderr"
}

test_help_documents_flags() {
  local root; new_sandbox; root=$root
  run_flags "$root" --help
  check exit "$?" 0
  check usage "$(grep -c '^Usage: generate_test_cases.sh' "$root/stdout")" 1
  check no_file "$(find "$root/out" -type f | wc -l | tr -d " ")" 0
}

test_flag_mode_writes_case() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id TC-CHK-002 --title "Declined card keeps cart" --priority p0 \
    --type functional --objective "A declined card creates no order" \
    --precondition "Cart holds 1 item" --step "Pay with the decline card | Decline shown; no order ID" \
    --step "Reload the cart|Same item still in cart" "$root/out"
  check exit "$?" 0
  local report="$root/out/TC-CHK-002.md"
  check manifest "$(cat "$root/stdout")" "{\"status\":\"created\",\"id\":\"TC-CHK-002\",\"file\":\"$root/out/TC-CHK-002.md\"}"
  check no_prompt "$(grep -c 'Test Case ID' "$root/stderr")" 0
  check priority "$(grep -c '^\*\*Priority:\*\* P0 (Critical)$' "$report")" 1
  check precondition "$(grep -c '^- Cart holds 1 item$' "$report")" 1
  check step1 "$(grep -c '^1\. Pay with the decline card$' "$report")" 1
  check step1_expected "$(grep -c '^   \*\*Expected:\*\* Decline shown; no order ID$' "$report")" 1
  check step2_trimmed "$(grep -c '^2\. Reload the cart$' "$report")" 1
  check step2_expected "$(grep -c '^   \*\*Expected:\*\* Same item still in cart$' "$report")" 1
}

test_flag_mode_missing_and_bad_fields() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id TC-1 --title T --priority P1 --type ui --objective O "$root/out"
  check missing_step "$?" 2
  check manifest "$(cat "$root/stdout")" '{"status":"error","missing":["--step"]}'
  run_flags "$root" --id TC-1 --title T --priority P1 --type ui --objective O --step "no expected" "$root/out"
  check step_without_bar "$?" 2
  run_flags "$root" --id TC-1 --title T --priority P1 --type ui --objective O --step "Act | " "$root/out"
  check step_empty_expected "$?" 2
  run_flags "$root" --id TC-1 --title T --priority P1 --type smoke --objective O --step "a | b" "$root/out"
  check bad_type "$?" 2
  check no_file "$(find "$root/out" -type f | wc -l | tr -d " ")" 0
}

test_flag_mode_traceability_and_cleanup() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id TC-CHK-004 --title "Declined card creates no order" --priority P0 \
    --type functional --objective "A declined card leaves no order" \
    --requirement REQ-PAY-7 --risk "Declined payment still creates an order" \
    --precondition "Seeded account qa+decline@example.test with 1 item in cart" \
    --data "Decline test card from the provider sandbox" \
    --step "Pay with the decline card | Decline message; order list unchanged" \
    --cleanup "Empty the cart of qa+decline@example.test" --cleanup "Delete any order it created" --time 10 "$root/out"
  check exit "$?" 0
  local report="$root/out/TC-CHK-004.md"
  check requirement "$(grep -c '^\*\*Requirement:\*\* REQ-PAY-7$' "$report")" 1
  check risk "$(grep -c '^\*\*Risk:\*\* Declined payment still creates an order$' "$report")" 1
  check cleanup_section "$(grep -c '^## Cleanup$' "$report")" 1
  check cleanup1 "$(grep -c '^- Empty the cart of qa+decline@example.test$' "$report")" 1
  check cleanup2 "$(grep -c '^- Delete any order it created$' "$report")" 1
  check no_placeholder "$(grep -c 'Describe system state' "$report")" 0
  check no_open_questions "$(grep -c '^None: every listed fact was supplied.$' "$report")" 1
}

test_missing_trace_fields_are_unknown() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id TC-5 --title T --priority P2 --type functional --objective O \
    --step "a | b" "$root/out"
  check exit "$?" 0
  local report="$root/out/TC-5.md"
  check requirement "$(grep -c '^\*\*Requirement:\*\* Unknown$' "$report")" 1
  check risk "$(grep -c '^\*\*Risk:\*\* Unknown$' "$report")" 1
  check data_unknown "$(grep -c '^Unknown (not recorded)$' "$report")" 2
  check no_none_required "$(grep -c 'No specific test data required' "$report")" 0
  check cleanup_unknown "$(grep -c '^Unknown (cleanup not recorded)$' "$report")" 1
  check open_questions "$(grep -c '^## Open Questions$' "$report")" 1
  for f in Requirement Risk Preconditions 'Test data' Cleanup; do
    check "oq_$f" "$(grep -c "^- $f: Unknown$" "$report")" 1
  done
}

test_unspecified_duration_is_unknown_and_asked() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id TC-D --title T --priority P2 --type functional --objective O \
    --step "a | b" "$root/out"
  local report="$root/out/TC-D.md"
  check duration "$(grep -c '^\*\*Estimated Time:\*\* Unknown$' "$report")" 1
  check no_tbd "$(grep -c 'TBD' "$report")" 0
  check oq_time "$(grep -c '^- Estimated time: Unknown$' "$report")" 1
  local shown asked
  shown=$(sed '/^## Open Questions$/,$d' "$report" | grep -ci 'unknown')
  asked=$(sed -n '/^## Open Questions$/,$p' "$report" | grep -c '^- .*: Unknown$')
  check shown_equals_asked "$shown" "$asked"
}

ctl_chars() { # U+0001..U+001F; printf -v keeps the newline a $(...) would strip
  local c='' ch i; for i in $(seq 1 31); do printf -v ch "\\$(printf '%03o' "$i")"; c+=$ch; done; printf '%s' "$c"; }
json_field() { # json_field <file> <key>: prints the parsed value, or PARSE_ERROR
  python3 -c 'import json,sys
try: print(json.loads(open(sys.argv[1]).read())[sys.argv[2]], end="")
except Exception: print("PARSE_ERROR", end="")' "$1" "$2"
}

test_manifests_escape_control_characters() {
  local root; new_sandbox; root=$root
  local ctl dir; ctl=$(ctl_chars)
  check ctl_len "${#ctl}" 31
  dir="$root/out-$ctl-end"
  mkdir -p "$dir"
  run_flags "$root" --id TC-J --title T --priority P1 --type functional --objective O --step 'a | b' "$dir"
  check exit "$?" 0
  check one_line "$(wc -l < "$root/stdout" | tr -d ' ')" 1
  check status "$(json_field "$root/stdout" status)" created
  check file_roundtrip "$(json_field "$root/stdout" file)" "$dir/TC-J.md"
  run_flags "$root" --id TC-J --title T --priority P1 --type functional --objective O --step 'a | b' "$root/missing-$ctl-end"
  check error_exit "$?" 3
  check error_status "$(json_field "$root/stdout" status)" error
  check error_roundtrip "$(json_field "$root/stdout" error)" "output directory $root/missing-$ctl-end does not exist or is not a directory"
  run_flags "$root" --title T "$root/out"
  check missing_status "$(json_field "$root/stdout" status)" error
}

test_io_failures_are_exit_3_not_exists() {
  local root; new_sandbox; root=$root
  mkdir -p "$root/out"
  : > "$root/plainfile"
  run_flags "$root" --id TC-IO --title T --priority P1 --type functional --objective O --step 'a | b' "$root/plainfile"
  check not_a_dir_exit "$?" 3
  check not_a_dir_status "$(json_field "$root/stdout" status)" error
  check not_a_dir_msg "$(json_field "$root/stdout" error)" "output directory $root/plainfile does not exist or is not a directory"
  if [ "$(id -u)" != 0 ]; then # root ignores directory permissions
    mkdir -p "$root/locked"; chmod 555 "$root/locked"
    run_flags "$root" --id TC-IO --title T --priority P1 --type functional --objective O --step 'a | b' "$root/locked"
    check locked_exit "$?" 3
    check locked_status "$(json_field "$root/stdout" status)" error
    check locked_msg "$(json_field "$root/stdout" error | grep -c '^cannot create ')" 1
    check locked_not_exists_msg "$(grep -c 'already exists' "$root/stderr")" 0
    check locked_no_file "$([ -e "$root/locked/TC-IO.md" ] && echo yes || echo no)" no
    chmod 755 "$root/locked"
  fi
  run_flags "$root" --id TC-IO --title T --priority P1 --type functional --objective O --step 'a | b' "$root/out"
  check first "$?" 0
  run_flags "$root" --id TC-IO --title T --priority P1 --type functional --objective O --step 'a | b' "$root/out"
  check exists_exit "$?" 1
  check exists_msg "$(json_field "$root/stdout" error | grep -c 'already exists')" 1
}

test_failed_write_is_exit_3() {
  local root; new_sandbox; root=$root
  [ -w /dev/full ] || { echo "  skip: no /dev/full"; return; }
  mkdir -p "$root/out"; ln -s /dev/full "$root/out/TC-IO.md"
  run_flags "$root" --id TC-IO --title T --priority P1 --type functional --objective O --step 'a | b' --overwrite "$root/out"
  check exit "$?" 3
  check status "$(json_field "$root/stdout" status)" error
  check msg "$(json_field "$root/stdout" error | grep -c 'may be incomplete')" 1
}

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
