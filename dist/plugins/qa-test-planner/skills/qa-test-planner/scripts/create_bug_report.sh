#!/bin/bash
# Bug report generator: writes one Markdown bug report, prints a JSON manifest on stdout.
set -e

usage() {
    cat << 'EOF'
Usage: create_bug_report.sh [FIELD FLAGS] [--overwrite] [OUTPUT_DIR]

Writes <ID>.md into OUTPUT_DIR (default: current directory) and prints one JSON
line on stdout: {"status":"created","id":"BUG-...","file":"..."}
Prompts, progress and errors go to stderr; stdout carries only the JSON line.
Needs bash and python3 (python3 builds the JSON line).

Modes:
  no field flag    asks for each field, one answer per stdin line
  any field flag   never prompts; unset optional fields are written as Unknown

Required: --title --description --expected --actual
Optional:
  --id ID            default BUG-<YYYYmmddHHMMSS>; characters outside [A-Za-z0-9_-] are dropped
  --severity S       critical|high|medium|low (default Untriaged)
  --priority P       P0|P1|P2|P3 (default Untriaged)
  --type T           e.g. Functional, UI, Crash, Performance (default Unknown)
  --os --browser --device --build --url
  --step TEXT        repeat once per reproduction step, in order
  --rate R           reproduction rate as observed, e.g. 2/10 (default Unknown)
  --console TEXT  --impact TEXT  --workaround TEXT
  --test-case ID  --figma URL  --first-noticed TEXT  --reporter NAME
  --regression TEXT  e.g. 'No' or 'Yes, since 2.3.0' (default Unknown)
  --overwrite        replace an existing <ID>.md (otherwise exit 1)

Every unset environment field, type, reporter, steps, rate, console errors,
user impact, workaround and regression status is written as Unknown and listed under the report's Open Questions.

Exit: 0 created; 1 the file already exists (rerun with --overwrite only if
replacing it is intended); 3 OUTPUT_DIR missing or not a directory, or the file
cannot be created or written (permission, disk): pick a writable directory;
2 usage error or missing required field ({"status":"error","missing":[...]}).
Every error also prints {"status":"error","error":"..."} or the missing list on stdout.

Example:
  create_bug_report.sh --title "[Checkout] Submit does nothing on second click" \
    --description "Pay button stays enabled, no request sent" \
    --step "Add any item to the cart" --step "Click Pay twice" \
    --expected "One order is created" --actual "No request; button unchanged" \
    --rate "3/10" --severity high --priority P1 ./bugs
EOF
}

say() { printf '%s\n' "$*" >&2; }
json_obj() { # json_obj KEY VALUE ...: one compact JSON line on stdout
    python3 -c 'import json, sys
a = sys.argv[1:]
print(json.dumps(dict(zip(a[::2], a[1::2])), ensure_ascii=False, separators=(",", ":")))' "$@"
}
json_missing() { # json_missing FLAG ...: the missing-fields error line
    python3 -c 'import json, sys
print(json.dumps({"status": "error", "missing": sys.argv[1:]}, separators=(",", ":")))' "$@"
}
fail() { # fail <exit-code> <message>
    json_obj status error error "$2"
    say "Error: $2"
    exit "$1"
}

prompt_input() {
    local prompt_text="$1" var_name="$2" required="$3" input
    while true; do
        say "$prompt_text"
        if ! read -r input; then # EOF: optional fields stay empty, required ones stop
            [ "$required" != "true" ] || fail 2 "stdin ended before: $prompt_text"
            input=""
        fi
        if [ -n "$input" ]; then
            printf -v "$var_name" '%s' "$input"
            break
        elif [ "$required" != "true" ]; then
            printf -v "$var_name" '%s' ''
            break
        else
            say "This field is required."
        fi
    done
}

# Start every field empty so inherited environment variables (OS, URL, ...) never leak in.
BUG_ID='' BUG_TITLE='' SEVERITY_IN='' PRIORITY_IN='' BUG_TYPE='' OS='' BROWSER='' DEVICE='' BUILD='' URL=''
DESCRIPTION='' EXPECTED='' ACTUAL='' CONSOLE_ERRORS='' FREQUENCY='' USER_IMPACT='' WORKAROUND=''
TEST_CASE='' FIGMA_LINK='' FIRST_NOTICED='' REPORTER='' REGRESSION=''
FLAGS=0 OVERWRITE=false OUTPUT_DIR="." REPRO_STEPS="" STEP_NUM=1
while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        --overwrite) OVERWRITE=true; shift; continue ;;
        --*)
            [ $# -ge 2 ] || fail 2 "$1 needs a value"
            FLAGS=1
            case "$1" in
                --id) BUG_ID=$2 ;;
                --title) BUG_TITLE=$2 ;;
                --severity) SEVERITY_IN=$2 ;;
                --priority) PRIORITY_IN=$2 ;;
                --type) BUG_TYPE=$2 ;;
                --os) OS=$2 ;;
                --browser) BROWSER=$2 ;;
                --device) DEVICE=$2 ;;
                --build) BUILD=$2 ;;
                --url) URL=$2 ;;
                --description) DESCRIPTION=$2 ;;
                --step) REPRO_STEPS+="${STEP_NUM}. $2"$'\n'; STEP_NUM=$((STEP_NUM + 1)) ;;
                --expected) EXPECTED=$2 ;;
                --actual) ACTUAL=$2 ;;
                --console) CONSOLE_ERRORS=$2 ;;
                --rate) FREQUENCY=$2 ;;
                --impact) USER_IMPACT=$2 ;;
                --workaround) WORKAROUND=$2 ;;
                --test-case) TEST_CASE=$2 ;;
                --figma) FIGMA_LINK=$2 ;;
                --first-noticed) FIRST_NOTICED=$2 ;;
                --reporter) REPORTER=$2 ;;
                --regression) REGRESSION=$2 ;;
                *) fail 2 "unknown option $1 (see --help)" ;;
            esac
            shift 2 ;;
        *) OUTPUT_DIR=$1; shift ;;
    esac
done

if [ "$FLAGS" = 1 ]; then
    missing=()
    [ -n "$BUG_TITLE" ] || missing+=(--title)
    [ -n "$DESCRIPTION" ] || missing+=(--description)
    [ -n "$EXPECTED" ] || missing+=(--expected)
    [ -n "$ACTUAL" ] || missing+=(--actual)
    if [ ${#missing[@]} -gt 0 ]; then
        json_missing "${missing[@]}"
        say "Error: missing required field(s): ${missing[*]}"
        exit 2
    fi
    case "$(printf '%s' "$SEVERITY_IN" | tr '[:upper:]' '[:lower:]')" in
        critical) SEVERITY=Critical ;; high) SEVERITY=High ;;
        medium) SEVERITY=Medium ;; low) SEVERITY=Low ;;
        "") SEVERITY=Untriaged ;;
        *) fail 2 "--severity must be critical, high, medium or low" ;;
    esac
    PRIORITY_IN=$(printf '%s' "$PRIORITY_IN" | tr '[:lower:]' '[:upper:]')
    case "$PRIORITY_IN" in
        P0|P1|P2|P3) PRIORITY=$PRIORITY_IN ;;
        "") PRIORITY=Untriaged ;;
        *) fail 2 "--priority must be P0, P1, P2 or P3" ;;
    esac
else
    say "Bug Report Generator (answer one field per line)"
    prompt_input "Bug title (clear, specific):" BUG_TITLE true
    say "Severity: 1) Critical - data loss, security breach, crash with no recovery"
    say "          2) High - core flow blocked, no workaround"
    say "          3) Medium - workaround exists"
    say "          4) Low - cosmetic, no functional effect"
    prompt_input "Select severity (1-4):" SEVERITY_NUM true
    case $SEVERITY_NUM in
        1) SEVERITY="Critical" ;; 2) SEVERITY="High" ;;
        3) SEVERITY="Medium" ;; 4) SEVERITY="Low" ;;
        *) SEVERITY="Untriaged" ;;
    esac
    say "Priority: 1) P0 - blocks release  2) P1 - fix before release"
    say "          3) P2 - next release     4) P3 - when possible"
    prompt_input "Select priority (1-4):" PRIORITY_NUM true
    case $PRIORITY_NUM in
        1) PRIORITY="P0" ;; 2) PRIORITY="P1" ;;
        3) PRIORITY="P2" ;; 4) PRIORITY="P3" ;;
        *) PRIORITY="Untriaged" ;;
    esac
    say "Environment (leave blank when unknown; it is written as Unknown)"
    prompt_input "Operating System (e.g., Windows 11, macOS 14):" OS false
    prompt_input "Browser & Version (e.g., Chrome 120, Firefox 121):" BROWSER false
    prompt_input "Device (e.g., Desktop, iPhone 15):" DEVICE false
    prompt_input "Build/Version number:" BUILD false
    prompt_input "URL or page where bug occurs:" URL false
    prompt_input "Brief description of the issue:" DESCRIPTION true
    say "Enter reproduction steps (one per line, empty line when done):"
    while read -r line && [ -n "$line" ]; do
        REPRO_STEPS+="${STEP_NUM}. ${line}"$'\n'
        STEP_NUM=$((STEP_NUM + 1))
    done
    prompt_input "Expected behavior:" EXPECTED true
    prompt_input "Actual behavior:" ACTUAL true
    prompt_input "Console errors (paste if any):" CONSOLE_ERRORS false
    prompt_input "Reproduction rate as observed (e.g., 2/10):" FREQUENCY false
    prompt_input "How many users affected (estimate):" USER_IMPACT false
    prompt_input "Workaround available? (describe if yes):" WORKAROUND false
    prompt_input "Related test case ID:" TEST_CASE false
    prompt_input "Figma design link (if UI bug):" FIGMA_LINK false
    prompt_input "First noticed (date/build):" FIRST_NOTICED false
    prompt_input "Reporter name:" REPORTER false
    prompt_input "Bug type (Functional, UI, Crash, Performance, Security, Data):" BUG_TYPE false
    prompt_input "Is this a regression? (No / Yes, since <build>):" REGRESSION false
fi

BUG_ID=${BUG_ID:-BUG-$(date +%Y%m%d%H%M%S)}
SAFE_ID="${BUG_ID//[^a-zA-Z0-9_-]/}"
[ -n "$SAFE_ID" ] || fail 2 "--id has no usable characters"
[ -d "$OUTPUT_DIR" ] || fail 3 "output directory $OUTPUT_DIR does not exist or is not a directory"
OUTPUT_FILE="$OUTPUT_DIR/${SAFE_ID}.md"

if [ "$OVERWRITE" != true ] && { [ -e "$OUTPUT_FILE" ] || [ -L "$OUTPUT_FILE" ]; }; then
    fail 1 "$OUTPUT_FILE already exists. Use --overwrite to replace it."
fi
if [ "$OVERWRITE" = true ]; then
    create_err=$( { : > "$OUTPUT_FILE"; } 2>&1 ) || fail 3 "cannot create $OUTPUT_FILE: ${create_err##*: }"
elif ! create_err=$( { set -o noclobber; : > "$OUTPUT_FILE"; } 2>&1 ); then
    [ ! -e "$OUTPUT_FILE" ] || fail 1 "$OUTPUT_FILE already exists. Use --overwrite to replace it."
    fail 3 "cannot create $OUTPUT_FILE: ${create_err##*: }"
fi
write_fail() { fail 3 "writing $OUTPUT_FILE failed; the file may be incomplete"; }

OPEN_QUESTIONS=""
ask() { [ -n "$2" ] || OPEN_QUESTIONS+="- $1: Unknown"$'\n'; } # ask <label> <value>
ask Type "$BUG_TYPE"; ask Reporter "$REPORTER"; ask OS "$OS"; ask Browser "$BROWSER"; ask Device "$DEVICE"; ask Build "$BUILD"; ask URL "$URL"
ask "Steps to reproduce" "$REPRO_STEPS"; ask "Reproduction rate" "$FREQUENCY"
ask "Console errors" "$CONSOLE_ERRORS"; ask "User impact" "$USER_IMPACT"; ask Workaround "$WORKAROUND"; ask Regression "$REGRESSION"

cat > "$OUTPUT_FILE" << EOF || write_fail
# ${BUG_ID}: ${BUG_TITLE}

**Severity:** ${SEVERITY}
**Priority:** ${PRIORITY}
**Type:** ${BUG_TYPE:-Unknown}
**Status:** Open
**Reported:** $(date +%Y-%m-%d)
**Reporter:** ${REPORTER:-Unknown}

---

## Environment

- **OS:** ${OS:-Unknown}
- **Browser:** ${BROWSER:-Unknown}
- **Device:** ${DEVICE:-Unknown}
- **Build:** ${BUILD:-Unknown}
- **URL:** ${URL:-Unknown}

---

## Description

${DESCRIPTION}

---

## Steps to Reproduce

${REPRO_STEPS:-Unknown (not yet reproduced; steps not recorded)}

---

## Expected Behavior

${EXPECTED}

---

## Actual Behavior

${ACTUAL}

---

## Visual Evidence

- [ ] Screenshot attached
- [ ] Screen recording attached
- [ ] Console logs attached

**Console Errors:**
\`\`\`
${CONSOLE_ERRORS:-Unknown (whether console errors were observed)}
\`\`\`

---

## Impact

- **Reproduction rate:** ${FREQUENCY:-Unknown}
- **User Impact:** ${USER_IMPACT:-Unknown}
- **Workaround:** ${WORKAROUND:-Unknown (whether a workaround exists)}

---

## Additional Context

${FIGMA_LINK:+**Figma Design:** ${FIGMA_LINK}}

${TEST_CASE:+**Related Test Case:** ${TEST_CASE}}

${FIRST_NOTICED:+**First Noticed:** ${FIRST_NOTICED}}

**Is this a regression?** ${REGRESSION:-Unknown}

---

## Root Cause

[To be filled by developer]

---

## Fix

[To be filled by developer]

---

## Verification

- [ ] Bug fix verified in dev environment
- [ ] Regression testing completed
- [ ] Related test cases passing

**Verified By:** ___________
**Date:** ___________

---

## Open Questions

${OPEN_QUESTIONS:-None: every listed fact was supplied.}
EOF

say "Bug report generated successfully: $OUTPUT_FILE"
say "Next: attach evidence, then confirm the steps reproduce on a clean account."
[ -z "$FIGMA_LINK" ] || say "Verify against Figma design before filing."
json_obj status created id "$BUG_ID" file "$OUTPUT_FILE"
