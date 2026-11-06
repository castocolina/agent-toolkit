#!/bin/bash
# Manual test case generator: writes one Markdown test case, prints a JSON manifest on stdout.
set -e

usage() {
    cat << 'EOF'
Usage: generate_test_cases.sh [FIELD FLAGS] [--overwrite] [OUTPUT_DIR]

Writes <ID>.md (one case per run) into OUTPUT_DIR (default: current directory)
and prints one JSON line on stdout: {"status":"created","id":"TC-...","file":"..."}
Prompts, progress and errors go to stderr; stdout carries only the JSON line.
Needs bash and python3 (python3 builds the JSON line).

Modes:
  no field flag    asks for each field, one answer per stdin line
  any field flag   never prompts

Required: --id --title --priority --type --objective, and at least one --step
Traceability (written as Unknown and listed under Open Questions when unset):
  --requirement ID   --risk TEXT   --precondition TEXT   --data TEXT   --cleanup TEXT
  --time MINUTES
Optional:
  --priority P       P0|P1|P2|P3
  --type T           functional|ui|integration|regression|performance|security
  --step "ACTION | EXPECTED"   repeat once per step, in order; both halves required
  --precondition TEXT          repeat once per seeded precondition
  --cleanup TEXT               repeat once per cleanup action, so a rerun starts clean
  --why TEXT  --edge TEXT  --related IDS  --notes TEXT
  --figma URL  --visual TEXT   (written only for --type ui with --figma)
  --overwrite        replace an existing <ID>.md (otherwise exit 1)

The file name is the ID with characters outside [A-Za-z0-9_-] dropped.
Exit: 0 created; 1 the file already exists (rerun with --overwrite only if
replacing it is intended); 3 OUTPUT_DIR missing or not a directory, or the file
cannot be created or written (permission, disk): pick a writable directory;
2 usage error or missing required field ({"status":"error","missing":[...]}).
Every error also prints {"status":"error","error":"..."} or the missing list on stdout.

Example:
  generate_test_cases.sh --id TC-CHK-002 --title "Declined card keeps cart" \
    --priority P0 --type functional --objective "A declined card creates no order" \
    --requirement REQ-PAY-7 --risk "A declined payment still creates an order" \
    --precondition "Seeded account qa+decline@example.test with 1 item in cart" \
    --data "The payment sandbox's decline test card" \
    --step "Pay with the decline card | Decline message shown; no order ID" \
    --step "Reload the cart | Same item still in cart" \
    --cleanup "Empty the cart of qa+decline@example.test" ./cases
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
trim() { local s=$1; s=${s#"${s%%[![:space:]]*}"}; printf '%s' "${s%"${s##*[![:space:]]}"}"; }

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

add_step() { # add_step <action> <expected>
    TEST_STEPS+="${STEP_NUM}. $1"$'\n'"   **Expected:** $2"$'\n\n'
    STEP_NUM=$((STEP_NUM + 1))
}

# Start every field empty so inherited environment variables never leak in.
TC_ID='' TC_TITLE='' PRIORITY_IN='' TYPE_IN='' EST_TIME='' OBJECTIVE='' WHY_IMPORTANT='' TEST_DATA=''
FIGMA_URL='' VISUAL_CHECKS='' EDGE_CASES='' RELATED_TCS='' NOTES='' REQUIREMENT='' RISK=''
FLAGS=0 OVERWRITE=false OUTPUT_DIR="." PRECONDITIONS="" CLEANUP="" TEST_STEPS="" STEP_NUM=1
while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        --overwrite) OVERWRITE=true; shift; continue ;;
        --*)
            [ $# -ge 2 ] || fail 2 "$1 needs a value"
            FLAGS=1
            case "$1" in
                --id) TC_ID=$2 ;;
                --title) TC_TITLE=$2 ;;
                --priority) PRIORITY_IN=$2 ;;
                --type) TYPE_IN=$2 ;;
                --time) EST_TIME=$2 ;;
                --objective) OBJECTIVE=$2 ;;
                --why) WHY_IMPORTANT=$2 ;;
                --precondition) PRECONDITIONS+="- $2"$'\n' ;;
                --cleanup) CLEANUP+="- $2"$'\n' ;;
                --requirement) REQUIREMENT=$2 ;;
                --risk) RISK=$2 ;;
                --step)
                    case "$2" in *"|"*) ;; *) fail 2 "--step needs \"ACTION | EXPECTED\": $2" ;; esac
                    action=$(trim "${2%%|*}") expected=$(trim "${2#*|}")
                    [ -n "$action" ] && [ -n "$expected" ] || fail 2 "--step needs both ACTION and EXPECTED: $2"
                    add_step "$action" "$expected" ;;
                --data) TEST_DATA=$2 ;;
                --figma) FIGMA_URL=$2 ;;
                --visual) VISUAL_CHECKS=$2 ;;
                --edge) EDGE_CASES=$2 ;;
                --related) RELATED_TCS=$2 ;;
                --notes) NOTES=$2 ;;
                *) fail 2 "unknown option $1 (see --help)" ;;
            esac
            shift 2 ;;
        *) OUTPUT_DIR=$1; shift ;;
    esac
done

if [ "$FLAGS" = 1 ]; then
    missing=()
    [ -n "$TC_ID" ] || missing+=(--id)
    [ -n "$TC_TITLE" ] || missing+=(--title)
    [ -n "$PRIORITY_IN" ] || missing+=(--priority)
    [ -n "$TYPE_IN" ] || missing+=(--type)
    [ -n "$OBJECTIVE" ] || missing+=(--objective)
    [ -n "$TEST_STEPS" ] || missing+=(--step)
    if [ ${#missing[@]} -gt 0 ]; then
        json_missing "${missing[@]}"
        say "Error: missing required field(s): ${missing[*]}"
        exit 2
    fi
    case "$(printf '%s' "$PRIORITY_IN" | tr '[:lower:]' '[:upper:]')" in
        P0) PRIORITY="P0 (Critical)" ;; P1) PRIORITY="P1 (High)" ;;
        P2) PRIORITY="P2 (Medium)" ;; P3) PRIORITY="P3 (Low)" ;;
        *) fail 2 "--priority must be P0, P1, P2 or P3" ;;
    esac
    case "$(printf '%s' "$TYPE_IN" | tr '[:upper:]' '[:lower:]')" in
        functional) TEST_TYPE="Functional" ;; ui) TEST_TYPE="UI/Visual" ;;
        integration) TEST_TYPE="Integration" ;; regression) TEST_TYPE="Regression" ;;
        performance) TEST_TYPE="Performance" ;; security) TEST_TYPE="Security" ;;
        *) fail 2 "--type must be functional, ui, integration, regression, performance or security" ;;
    esac
else
    say "Manual Test Case Generator (answer one field per line)"
    prompt_input "Test Case ID (e.g., TC-LOGIN-001):" TC_ID true
    prompt_input "Test Case Title:" TC_TITLE true
    say "Priority: 1) P0 - Critical (blocks release)  2) P1 - High"
    say "          3) P2 - Medium                     4) P3 - Low"
    prompt_input "Select priority (1-4):" PRIORITY_NUM true
    case $PRIORITY_NUM in
        1) PRIORITY="P0 (Critical)" ;; 2) PRIORITY="P1 (High)" ;;
        3) PRIORITY="P2 (Medium)" ;; 4) PRIORITY="P3 (Low)" ;;
        *) PRIORITY="P2 (Medium)" ;;
    esac
    say "Test type: 1) Functional 2) UI/Visual 3) Integration"
    say "           4) Regression 5) Performance 6) Security"
    prompt_input "Select test type (1-6):" TYPE_NUM true
    case $TYPE_NUM in
        1) TEST_TYPE="Functional" ;; 2) TEST_TYPE="UI/Visual" ;;
        3) TEST_TYPE="Integration" ;; 4) TEST_TYPE="Regression" ;;
        5) TEST_TYPE="Performance" ;; 6) TEST_TYPE="Security" ;;
        *) TEST_TYPE="Functional" ;;
    esac
    prompt_input "Estimated test time (minutes):" EST_TIME false
    prompt_input "What are you testing? (objective):" OBJECTIVE true
    prompt_input "Why is this test important?" WHY_IMPORTANT false
    say "Enter preconditions (one per line, empty line when done):"
    while read -r line && [ -n "$line" ]; do
        PRECONDITIONS+="- ${line}"$'\n'
    done
    say "Enter test steps: an action, then its expected result. Type 'done' or leave the action empty to finish."
    while true; do
        say "Step $STEP_NUM:"
        prompt_input "Action:" STEP_ACTION false
        if [ "$STEP_ACTION" = "done" ] || [ -z "$STEP_ACTION" ]; then
            break
        fi
        prompt_input "Expected result:" STEP_EXPECTED true
        add_step "$STEP_ACTION" "$STEP_EXPECTED"
    done
    prompt_input "Test data required (e.g., user credentials, sample data):" TEST_DATA false
    if [ "$TEST_TYPE" = "UI/Visual" ]; then
        prompt_input "Figma design URL (if applicable):" FIGMA_URL false
        prompt_input "Visual elements to validate:" VISUAL_CHECKS false
    fi
    prompt_input "Edge cases or variations to consider:" EDGE_CASES false
    prompt_input "Related test cases (IDs):" RELATED_TCS false
    prompt_input "Notes or comments:" NOTES false
    prompt_input "Requirement ID this case covers:" REQUIREMENT false
    prompt_input "Risk (failure mode) this case catches:" RISK false
    prompt_input "Cleanup after the run:" CLEANUP_LINE false
    [ -z "$CLEANUP_LINE" ] || CLEANUP="- ${CLEANUP_LINE}"$'\n'
fi

EST_DISPLAY="Unknown"; [ -z "$EST_TIME" ] || EST_DISPLAY="$EST_TIME minutes"
OPEN_QUESTIONS=""
ask() { [ -n "$2" ] || OPEN_QUESTIONS+="- $1: Unknown"$'\n'; } # ask <label> <value>
ask "Estimated time" "$EST_TIME"; ask Requirement "$REQUIREMENT"; ask Risk "$RISK"; ask Preconditions "$PRECONDITIONS"
ask "Test data" "$TEST_DATA"; ask Cleanup "$CLEANUP"

SAFE_TC_ID="${TC_ID//[^a-zA-Z0-9_-]/}"
[ -n "$SAFE_TC_ID" ] || fail 2 "the ID has no usable characters"
[ -d "$OUTPUT_DIR" ] || fail 3 "output directory $OUTPUT_DIR does not exist or is not a directory"
OUTPUT_FILE="$OUTPUT_DIR/${SAFE_TC_ID}.md"

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

cat > "$OUTPUT_FILE" << EOF || write_fail
# ${TC_ID}: ${TC_TITLE}

**Priority:** ${PRIORITY}
**Type:** ${TEST_TYPE}
**Requirement:** ${REQUIREMENT:-Unknown}
**Risk:** ${RISK:-Unknown}
**Status:** Not Run
**Estimated Time:** ${EST_DISPLAY}
**Created:** $(date +%Y-%m-%d)

---

## Objective

${OBJECTIVE}

${WHY_IMPORTANT:+**Why this matters:** ${WHY_IMPORTANT}}

---

## Preconditions

${PRECONDITIONS:-Unknown (not recorded)}

---

## Test Steps

${TEST_STEPS:-None recorded (add steps before execution)}

---

## Test Data

${TEST_DATA:-Unknown (not recorded)}

---

EOF

if [ "$TEST_TYPE" = "UI/Visual" ] && [ -n "$FIGMA_URL" ]; then
    cat >> "$OUTPUT_FILE" << EOF || write_fail
## Visual Validation (Figma)

**Design Reference:** ${FIGMA_URL}

**Elements to validate:**
${VISUAL_CHECKS}

**Verification checklist:**
- [ ] Layout matches Figma design
- [ ] Spacing (padding/margins) accurate
- [ ] Typography (font, size, weight, color) correct
- [ ] Colors match design system
- [ ] Component states (hover, active, disabled) implemented
- [ ] Responsive behavior as designed

---

EOF
fi

cat >> "$OUTPUT_FILE" << EOF || write_fail
## Cleanup

${CLEANUP:-Unknown (cleanup not recorded)}

---

## Edge Cases & Variations

${EDGE_CASES:-None recorded}

---

## Related Test Cases

${RELATED_TCS:-None}

---

## Execution History

| Date | Tester | Build | Result | Notes |
|------|--------|-------|--------|-------|
| | | | Not Run | |

---

## Notes

${NOTES}

---

## Open Questions

${OPEN_QUESTIONS:-None: every listed fact was supplied.}
EOF

say "Test case generated successfully: $OUTPUT_FILE"
if [ "$TEST_TYPE" = "UI/Visual" ] && [ -n "$FIGMA_URL" ]; then
    say "Validate against Figma design before marking it Pass."
fi
json_obj status created id "$TC_ID" file "$OUTPUT_FILE"
