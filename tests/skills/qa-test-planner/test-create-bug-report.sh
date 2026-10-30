#!/bin/bash
# Tests for skills/qa-test-planner/scripts/create_bug_report.sh.
#
# Pins the behavior documented in the qa-test-planner SKILL.md/README: the
# script interviews the user (title, severity, priority, environment,
# description, reproduction steps, expected vs actual) and writes a Markdown
# bug report named <BUG-ID>.md into the requested output directory. A fixed
# `date` shim makes the generated bug ID and report date deterministic.
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
  printf '%s' "$root"
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
  check url_default "$(grep -c '^- \*\*URL:\*\* N/A$' "$report")" 1
  check description "$(grep -c '^App crashes on login click$' "$report")" 1
  check step1_own_line "$(grep -c '^1\. Click the Login button$' "$report")" 1
  check step2_own_line "$(grep -c '^2\. App stays open$' "$report")" 1
  check expected "$(grep -c '^The user logs in$' "$report")" 1
  check actual "$(grep -c '^The app crashes$' "$report")" 1
  check console_default "$(grep -c '^Not provided (whether console errors were observed is unknown)$' "$report")" 1
  check workaround_default "$(grep -c '^- \*\*Workaround:\*\* Not provided (availability is unknown)$' "$report")" 1
  check success_msg "$(grep -c 'Bug report generated successfully' "$root/stdout")" 1
  check location_msg "$(grep -c "$root/out/BUG-20260120101112.md" "$root/stdout")" 1
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
Always
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
  check frequency "$(grep -c '^- \*\*Frequency:\*\* Always$' "$report")" 1
  check impact "$(grep -c '^- \*\*User Impact:\*\* ~500 users$' "$report")" 1
  check workaround "$(grep -c '^- \*\*Workaround:\*\* Use the mobile site$' "$report")" 1
  check related_tc "$(grep -c '^\*\*Related Test Case:\*\* TC-SEARCH-001$' "$report")" 1
  check figma "$(grep -c '^\*\*Figma Design:\*\* https://figma.example.com/file/search$' "$report")" 1
  check first_noticed "$(grep -c '^\*\*First Noticed:\*\* build-98$' "$report")" 1
  check figma_hint "$(grep -c 'Verify against Figma design' "$root/stdout")" 1
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
  check reprompt "$(grep -c 'This field is required.' "$root/stdout")" 1
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

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
