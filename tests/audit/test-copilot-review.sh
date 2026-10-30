#!/usr/bin/env bash
# Offline tests for .github/audit/copilot-review.sh (the read-only PR reviewer wrapper).
# A stub copilot on PATH records its argv, its environment and its stdin. The
# checks pin the reviewer's containment (read tool only, no shell, no write tool)
# and that no GitHub token reaches the model process.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WRAPPER="$ROOT/.github/audit/copilot-review.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"
DEFAULT_ANSWER=$(printf '%s' '{"verdict":"approve","findings":[]}')
export DEFAULT_ANSWER
cat > "$TMP/bin/copilot" <<'STUB'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\0' "$@" > "$COPILOT_ARGS"
env | sort > "$COPILOT_ENV"
cat > "$COPILOT_STDIN"
printf '%s' "${COPILOT_STDOUT:-$DEFAULT_ANSWER}"
exit "${COPILOT_EXIT:-0}"
STUB
chmod +x "$TMP/bin/copilot"
export PATH="$TMP/bin:$PATH"
export COPILOT_ARGS="$TMP/args" COPILOT_ENV="$TMP/env" COPILOT_STDIN="$TMP/stdin"
export AUDIT_REVIEW_MODEL='review-model' AUDIT_REVIEW_EFFORT='high'
prompt='review this pull request'

fail() { printf 'FAIL %s\n' "$*" >&2; exit 1; }

assert_argv() {
  local label=$1
  shift
  local -a actual=() expected=("$@")
  mapfile -d '' -t actual < "$COPILOT_ARGS"
  if ((${#actual[@]} != ${#expected[@]})); then
    fail "$label argv length mismatch: got ${#actual[@]}, expected ${#expected[@]}: $(printf '%q ' "${actual[@]}")"
  fi
  local i
  for ((i = 0; i < ${#expected[@]}; i++)); do
    if [[ "${actual[i]}" != "${expected[i]}" ]]; then
      fail "$label argv mismatch at $i: got ${actual[i]@Q}, expected ${expected[i]@Q}"
    fi
  done
}

# The reviewer runs with the model, the effort, the read tool and no shell, and
# the prompt on stdin becomes -p.
printf '%s' "$prompt" | GH_TOKEN=must-not-leak GITHUB_TOKEN=must-not-leak "$WRAPPER" > "$TMP/out"
# Containment: the shell, the write and the URL-fetch tools are all excluded by name. The tool names
# are UNVERIFIED until the containment drill (docs/audit/ci-spike.md item 11) lists them in Actions.
assert_argv reviewer -p "$prompt" -s --no-ask-user --model review-model --reasoning-effort high --allow-tool=read --excluded-tools shell write web_fetch
[[ "$(cat "$COPILOT_STDIN")" == "" ]] || fail "stdin was forwarded to copilot instead of the prompt argument"
grep -q '^GH_TOKEN=' "$COPILOT_ENV" && fail "GH_TOKEN reached the model process"
grep -q '^GITHUB_TOKEN=' "$COPILOT_ENV" && fail "GITHUB_TOKEN reached the model process"
[[ "$(cat "$TMP/out")" == '{"verdict":"approve","findings":[]}' ]] || fail "stdout was not passed through: $(cat "$TMP/out")"
echo "PASS reviewer argv: read tool only, no shell, effort and model, no GitHub token"

# The write tool and the shell are never granted; the argv differs from copilot-agent.sh.
if grep -q -- '--allow-tool=write' "$COPILOT_ARGS" 2>/dev/null; then fail "reviewer granted write"; fi
if printf '%s' "$(tr '\0' ' ' < "$COPILOT_ARGS")" | grep -q -- 'allow-tool=shell\|allow-all\|--yolo'; then
  fail "reviewer granted shell or all tools"
fi
if [[ "$(tr '\0' ' ' < "$COPILOT_ARGS")" == *"--allow-tool=write"* ]]; then fail "reviewer argv matches the writer"; fi
echo "PASS reviewer grants no write and no shell"

# A failing copilot run makes the wrapper fail (the reviewer step then fails and the outcome is needs-human).
if printf '%s' "$prompt" | COPILOT_EXIT=7 "$WRAPPER" > "$TMP/out" 2> "$TMP/err"; then
  fail "wrapper succeeded when copilot exited 7"
fi
echo "PASS a failing reviewer exits non-zero"

# Missing knobs fail closed before any model runs.
rm -f "$COPILOT_ARGS"
if printf '%s' "$prompt" | env -u AUDIT_REVIEW_MODEL "$WRAPPER" > "$TMP/out" 2> "$TMP/err"; then
  fail "wrapper ran without AUDIT_REVIEW_MODEL"
fi
[[ ! -e "$COPILOT_ARGS" ]] || fail "copilot ran without AUDIT_REVIEW_MODEL"
if printf '%s' "$prompt" | env -u AUDIT_REVIEW_EFFORT "$WRAPPER" > "$TMP/out" 2> "$TMP/err"; then
  fail "wrapper ran without AUDIT_REVIEW_EFFORT"
fi
[[ ! -e "$COPILOT_ARGS" ]] || fail "copilot ran without AUDIT_REVIEW_EFFORT"
echo "PASS missing knobs fail before copilot runs"

echo 'PASS copilot-review.sh'
