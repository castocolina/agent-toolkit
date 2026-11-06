#!/bin/bash
# Tests for skills/qa-test-planner/scripts/create_bug_report.sh.
#
# Pins the behavior documented in SKILL.md and --help: with no field flag the
# script interviews the user on stdin; with field flags it never prompts. Either
# way it writes <BUG-ID>.md into the output directory, keeps prompts and errors
# on stderr and prints one JSON manifest line on stdout. A fixed `date` shim
# makes the generated bug ID and report date deterministic.
HERE=$(cd "$(dirname "$0")" && pwd)
SCRIPT=$HERE/../../../skills/qa-test-planner/scripts/create_bug_report.sh
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
  +%Y%m%d%H%M%S) echo "20260120101112" ;;
  +%Y-%m-%d) echo "2026-01-20" ;;
  *) command -p date "$@" ;;
esac
EOF
  chmod +x "$root/bin/date"
}

run_report() { # run_report <sandbox> <stdin-file> [output-dir]; leaves rc in $?
  local root=$1 stdin_file=$2 out_dir=${3:-$1/out}
  mkdir -p "$out_dir"
  (cd "$root" && PATH="$root/bin:$PATH" bash "$SCRIPT" "$out_dir") \
    <"$stdin_file" >"$root/stdout" 2>"$root/stderr"
}

test_report_from_minimal_input() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
Login button crashes app
2
1
Windows 11
Chrome 120

build-42

App crashes on login click
Click the Login button
App stays open

The user logs in
The app crashes













EOF
  run_report "$root" "$root/stdin"
  check exit "$?" 0
  check file "$([ -f "$root/out/BUG-20260120101112.md" ] && echo yes || echo no)" yes
  local report="$root/out/BUG-20260120101112.md"
  check title "$(grep -c '# BUG-20260120101112: Login button crashes app' "$report")" 1
  check severity "$(grep -c '^\*\*Severity:\*\* High$' "$report")" 1
  check priority "$(grep -c '^\*\*Priority:\*\* P0$' "$report")" 1
  check reported "$(grep -c '^\*\*Reported:\*\* 2026-01-20$' "$report")" 1
  check status "$(grep -c '^\*\*Status:\*\* Open$' "$report")" 1
  check device_default "$(grep -c '^- \*\*Device:\*\* Unknown$' "$report")" 1
  check url_default "$(grep -c '^- \*\*URL:\*\* Unknown$' "$report")" 1
  check reporter_default "$(grep -c '^\*\*Reporter:\*\* Unknown$' "$report")" 1
  check oq_os_known "$(grep -c '^- OS: Unknown$' "$report")" 0
  check oq_device "$(grep -c '^- Device: Unknown$' "$report")" 1
  check oq_url "$(grep -c '^- URL: Unknown$' "$report")" 1
  check oq_build_known "$(grep -c '^- Build: Unknown$' "$report")" 0
  check description "$(grep -c '^App crashes on login click$' "$report")" 1
  check step1_own_line "$(grep -c '^1\. Click the Login button$' "$report")" 1
  check step2_own_line "$(grep -c '^2\. App stays open$' "$report")" 1
  check expected "$(grep -c '^The user logs in$' "$report")" 1
  check actual "$(grep -c '^The app crashes$' "$report")" 1
  check console_default "$(grep -c '^Not provided (whether console errors were observed is unknown)$' "$report")" 1
  check workaround_default "$(grep -c '^- \*\*Workaround:\*\* Not provided (availability is unknown)$' "$report")" 1
  check success_msg "$(grep -c 'Bug report generated successfully' "$root/stderr")" 1
  check manifest "$(cat "$root/stdout")" "{\"status\":\"created\",\"id\":\"BUG-20260120101112\",\"file\":\"$root/out/BUG-20260120101112.md\"}"
  check no_ansi_stdout "$(grep -c $'\033' "$root/stdout")" 0
}

test_report_records_optional_fields() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
Search results flicker
1
3
macOS 14
Firefox 121
iPhone 15
build-99
https://app.example.com/search
Results flicker while typing
Type in the search box
Watch the results list

Results stay stable
Results flicker every keystroke
TypeError: cannot read property of undefined
3/10
~500 users
Use the mobile site
TC-SEARCH-001
https://figma.example.com/file/search
build-98
EOF
  run_report "$root" "$root/stdin"
  check exit "$?" 0
  local report="$root/out/BUG-20260120101112.md"
  check file "$([ -f "$report" ] && echo yes || echo no)" yes
  check severity "$(grep -c '^\*\*Severity:\*\* Critical$' "$report")" 1
  check priority "$(grep -c '^\*\*Priority:\*\* P2$' "$report")" 1
  check device "$(grep -c '^- \*\*Device:\*\* iPhone 15$' "$report")" 1
  check url "$(grep -c '^- \*\*URL:\*\* https://app.example.com/search$' "$report")" 1
  check console "$(grep -c 'TypeError: cannot read property of undefined' "$report")" 1
  check rate "$(grep -c '^- \*\*Reproduction rate:\*\* 3/10$' "$report")" 1
  check impact "$(grep -c '^- \*\*User Impact:\*\* ~500 users$' "$report")" 1
  check workaround "$(grep -c '^- \*\*Workaround:\*\* Use the mobile site$' "$report")" 1
  check related_tc "$(grep -c '^\*\*Related Test Case:\*\* TC-SEARCH-001$' "$report")" 1
  check figma "$(grep -c '^\*\*Figma Design:\*\* https://figma.example.com/file/search$' "$report")" 1
  check first_noticed "$(grep -c '^\*\*First Noticed:\*\* build-98$' "$report")" 1
  check figma_hint "$(grep -c 'Verify against Figma design' "$root/stderr")" 1
}

test_required_field_reprompts_until_answered() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'

Login button crashes app
4
4
Ubuntu 24.04
Chrome 120

build-7

Description text
Step one

Expected text
Actual text













EOF
  run_report "$root" "$root/stdin"
  check exit "$?" 0
  check reprompt "$(grep -c 'This field is required.' "$root/stderr")" 1
  local report="$root/out/BUG-20260120101112.md"
  check file "$([ -f "$report" ] && echo yes || echo no)" yes
  check severity "$(grep -c '^\*\*Severity:\*\* Low$' "$report")" 1
  check priority "$(grep -c '^\*\*Priority:\*\* P3$' "$report")" 1
  check title "$(grep -c '# BUG-20260120101112: Login button crashes app' "$report")" 1
}

test_output_defaults_to_current_directory() {
  local root; new_sandbox; root=$root
  cat > "$root/stdin" << 'EOF'
Login button crashes app
2
1
Windows 11
Chrome 120

build-42

App crashes on login click
Click the Login button

The user logs in
The app crashes













EOF
  (cd "$root" && PATH="$root/bin:$PATH" bash "$SCRIPT") \
    <"$root/stdin" >"$root/stdout" 2>"$root/stderr"
  check exit "$?" 0
  check file "$([ -f "$root/BUG-20260120101112.md" ] && echo yes || echo no)" yes
}

run_flags() { # run_flags <sandbox> <args...>; never reads stdin
  local root=$1; shift
  mkdir -p "$root/out"
  (cd "$root" && PATH="$root/bin:$PATH" OS=Leaked bash "$SCRIPT" "$@") \
    </dev/null >"$root/stdout" 2>"$root/stderr"
}

test_help_documents_flags() {
  local root; new_sandbox; root=$root
  run_flags "$root" --help
  check exit "$?" 0
  check usage "$(grep -c '^Usage: create_bug_report.sh' "$root/stdout")" 1
  check required_line "$(grep -c -- '^Required: --title --description --expected --actual$' "$root/stdout")" 1
  check no_file "$(find "$root/out" -type f | wc -l | tr -d " ")" 0
}

test_flag_mode_marks_unknown_facts() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id BUG-CHK-1 --title "[Checkout] Submit does nothing" \
    --description "Pay click sends no request" --expected "Order created" \
    --actual "Nothing happens" --rate 2/10 "$root/out"
  check exit "$?" 0
  local report="$root/out/BUG-CHK-1.md"
  check manifest "$(cat "$root/stdout")" "{\"status\":\"created\",\"id\":\"BUG-CHK-1\",\"file\":\"$root/out/BUG-CHK-1.md\"}"
  check no_prompt "$(grep -c 'Bug title' "$root/stderr")" 0
  check os_unknown_not_env "$(grep -c '^- \*\*OS:\*\* Unknown$' "$report")" 1
  check browser_unknown "$(grep -c '^- \*\*Browser:\*\* Unknown$' "$report")" 1
  check build_unknown "$(grep -c '^- \*\*Build:\*\* Unknown$' "$report")" 1
  check steps_unknown "$(grep -c '^Unknown (not yet reproduced; steps not recorded)$' "$report")" 1
  check severity_untriaged "$(grep -c '^\*\*Severity:\*\* Untriaged$' "$report")" 1
  check type_unknown "$(grep -c '^\*\*Type:\*\* Unknown$' "$report")" 1
  check rate "$(grep -c '^- \*\*Reproduction rate:\*\* 2/10$' "$report")" 1
}

test_flag_mode_steps_and_triage() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id BUG-2 --title T --description D --expected E --actual A \
    --step "Add an item" --step "Click Pay twice" --severity HIGH --priority p1 "$root/out"
  check exit "$?" 0
  local report="$root/out/BUG-2.md"
  check step1 "$(grep -c '^1\. Add an item$' "$report")" 1
  check step2 "$(grep -c '^2\. Click Pay twice$' "$report")" 1
  check severity "$(grep -c '^\*\*Severity:\*\* High$' "$report")" 1
  check priority "$(grep -c '^\*\*Priority:\*\* P1$' "$report")" 1
}

test_flag_mode_missing_required_fields() {
  local root; new_sandbox; root=$root
  run_flags "$root" --title "Only a title" "$root/out"
  check exit "$?" 2
  check manifest "$(cat "$root/stdout")" '{"status":"error","missing":["--description","--expected","--actual"]}'
  check no_file "$(find "$root/out" -type f | wc -l | tr -d " ")" 0
}

test_flag_mode_rejects_bad_values() {
  local root; new_sandbox; root=$root
  run_flags "$root" --title T --description D --expected E --actual A --severity urgent "$root/out"
  check bad_severity "$?" 2
  run_flags "$root" --title T --bogus x "$root/out"
  check unknown_flag "$?" 2
  run_flags "$root" --title T --description D --expected E --actual A "$root/missing-dir"
  check missing_dir "$?" 3
}

test_existing_report_kept_unless_overwrite() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id BUG-3 --title First --description D --expected E --actual A "$root/out"
  check first "$?" 0
  run_flags "$root" --id BUG-3 --title Second --description D --expected E --actual A "$root/out"
  check collision "$?" 1
  check kept "$(grep -c '^# BUG-3: First$' "$root/out/BUG-3.md")" 1
  run_flags "$root" --id BUG-3 --title Second --description D --expected E --actual A --overwrite "$root/out"
  check overwrite "$?" 0
  check replaced "$(grep -c '^# BUG-3: Second$' "$root/out/BUG-3.md")" 1
}

test_open_questions_list_every_missing_fact() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id BUG-OQ --title T --description D --expected E --actual A \
    --build 2.4.0-rc2 --rate 2/10 --step "Click Pay twice" --reporter "QA Ana" "$root/out"
  check exit "$?" 0
  local report="$root/out/BUG-OQ.md"
  check section "$(grep -c '^## Open Questions$' "$report")" 1
  for f in OS Browser Device URL 'Console errors' 'User impact' Workaround; do
    check "oq_$f" "$(grep -c "^- $f: Unknown$" "$report")" 1
  done
  check build_supplied "$(grep -c '^- \*\*Build:\*\* 2.4.0-rc2$' "$report")" 1
  check build_not_asked "$(grep -c '^- Build: Unknown$' "$report")" 0
  check rate_not_asked "$(grep -c '^- Reproduction rate: Unknown$' "$report")" 0
  check steps_not_asked "$(grep -c '^- Steps to reproduce: Unknown$' "$report")" 0
  check reporter "$(grep -c '^\*\*Reporter:\*\* QA Ana$' "$report")" 1
}

test_open_questions_ask_for_steps_and_rate() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id BUG-OQ2 --title T --description D --expected E --actual A "$root/out"
  local report="$root/out/BUG-OQ2.md"
  check steps_asked "$(grep -c '^- Steps to reproduce: Unknown$' "$report")" 1
  check rate_asked "$(grep -c '^- Reproduction rate: Unknown$' "$report")" 1
}

test_no_open_questions_when_all_known() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id BUG-ALL --title T --description D --expected E --actual A \
    --os 'macOS 14' --browser 'Safari 17' --device Desktop --build b1 --url https://x.test \
    --step s1 --rate 1/1 --console none --impact 'all users' --workaround none \
    --type UI --reporter 'QA Ana' --regression No "$root/out"
  check none_open "$(grep -c '^None: every listed fact was supplied.$' "$root/out/BUG-ALL.md")" 1
}

test_every_displayed_unknown_is_asked() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id BUG-U --title T --description D --expected E --actual A "$root/out"
  local report="$root/out/BUG-U.md"
  check type_shown "$(grep -c '^\*\*Type:\*\* Unknown$' "$report")" 1
  check reporter_shown "$(grep -c '^\*\*Reporter:\*\* Unknown$' "$report")" 1
  check regression_shown "$(grep -c '^\*\*Is this a regression?\*\* Unknown$' "$report")" 1
  for f in Type Reporter Regression; do
    check "oq_$f" "$(grep -c "^- $f: Unknown$" "$report")" 1
  done
  # every "Unknown" value displayed above the questions has a matching question
  local shown asked
  shown=$(sed '/^## Open Questions$/,$d' "$report" | grep -ci 'unknown')
  asked=$(sed -n '/^## Open Questions$/,$p' "$report" | grep -c '^- .*: Unknown$')
  check shown_equals_asked "$shown" "$asked"
}

test_supplied_type_reporter_regression_not_asked() {
  local root; new_sandbox; root=$root
  run_flags "$root" --id BUG-K --title T --description D --expected E --actual A \
    --type Functional --reporter 'QA Ana' --regression 'Yes, since 2.3.0' "$root/out"
  local report="$root/out/BUG-K.md"
  check regression "$(grep -c '^\*\*Is this a regression?\*\* Yes, since 2.3.0$' "$report")" 1
  check type_not_asked "$(grep -c '^- Type: Unknown$' "$report")" 0
  check reporter_not_asked "$(grep -c '^- Reporter: Unknown$' "$report")" 0
  check regression_not_asked "$(grep -c '^- Regression: Unknown$' "$report")" 0
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
  run_flags "$root" --id BUG-J --title T --description D --expected E --actual A "$dir"
  check exit "$?" 0
  check one_line "$(wc -l < "$root/stdout" | tr -d ' ')" 1
  check status "$(json_field "$root/stdout" status)" created
  check file_roundtrip "$(json_field "$root/stdout" file)" "$dir/BUG-J.md"
  run_flags "$root" --id BUG-J --title T --description D --expected E --actual A "$root/missing-$ctl-end"
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
  run_flags "$root" --id BUG-IO --title T --description D --expected E --actual A "$root/plainfile"
  check not_a_dir_exit "$?" 3
  check not_a_dir_status "$(json_field "$root/stdout" status)" error
  check not_a_dir_msg "$(json_field "$root/stdout" error)" "output directory $root/plainfile does not exist or is not a directory"
  if [ "$(id -u)" != 0 ]; then # root ignores directory permissions
    mkdir -p "$root/locked"; chmod 555 "$root/locked"
    run_flags "$root" --id BUG-IO --title T --description D --expected E --actual A "$root/locked"
    check locked_exit "$?" 3
    check locked_status "$(json_field "$root/stdout" status)" error
    check locked_msg "$(json_field "$root/stdout" error | grep -c '^cannot create ')" 1
    check locked_not_exists_msg "$(grep -c 'already exists' "$root/stderr")" 0
    check locked_no_file "$([ -e "$root/locked/BUG-IO.md" ] && echo yes || echo no)" no
    chmod 755 "$root/locked"
  fi
  run_flags "$root" --id BUG-IO --title T --description D --expected E --actual A "$root/out"
  check first "$?" 0
  run_flags "$root" --id BUG-IO --title T --description D --expected E --actual A "$root/out"
  check exists_exit "$?" 1
  check exists_msg "$(json_field "$root/stdout" error | grep -c 'already exists')" 1
}

test_failed_write_is_exit_3() {
  local root; new_sandbox; root=$root
  [ -w /dev/full ] || { echo "  skip: no /dev/full"; return; }
  mkdir -p "$root/out"; ln -s /dev/full "$root/out/BUG-IO.md"
  run_flags "$root" --id BUG-IO --title T --description D --expected E --actual A --overwrite "$root/out"
  check exit "$?" 3
  check status "$(json_field "$root/stdout" status)" error
  check msg "$(json_field "$root/stdout" error | grep -c 'may be incomplete')" 1
}

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
