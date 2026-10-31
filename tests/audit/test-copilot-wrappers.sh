#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"
cat > "$TMP/bin/copilot" <<'STUB'
#!/usr/bin/env bash
printf '%s\0' "$@" > "$COPILOT_ARGS"
STUB
chmod +x "$TMP/bin/copilot"
export PATH="$TMP/bin:$PATH"
export COPILOT_ARGS="$TMP/args"
export AUDIT_MERGER_MODEL='test-model'
prompt='prompt from stdin'

assert_argv() {
  local label=$1
  shift
  local -a actual=() expected=("$@")
  mapfile -d '' -t actual < "$COPILOT_ARGS"
  if ((${#actual[@]} != ${#expected[@]})); then
    printf '%s argv length mismatch: got %d, expected %d\n' "$label" "${#actual[@]}" "${#expected[@]}" >&2
    exit 1
  fi
  local i
  for ((i = 0; i < ${#expected[@]}; i++)); do
    if [[ "${actual[i]}" != "${expected[i]}" ]]; then
      printf '%s argv mismatch at %d: got %q, expected %q\n' "$label" "$i" "${actual[i]}" "${expected[i]}" >&2
      exit 1
    fi
  done
}

printf '%s' "$prompt" | "$ROOT/.github/audit/copilot-runner.sh" > "$TMP/out"
assert_argv runner -p "$prompt" -s --no-ask-user --model test-model --available-tools ''
[[ ! -s "$TMP/out" ]]

printf '%s' "$prompt" | "$ROOT/.github/audit/copilot-agent.sh" > "$TMP/out"
assert_argv agent -p "$prompt" -s --no-ask-user --model test-model --allow-tool=read --allow-tool=write --excluded-tools shell
[[ ! -s "$TMP/out" ]]

unset AUDIT_MERGER_MODEL
if printf '%s' "$prompt" | "$ROOT/.github/audit/copilot-runner.sh" > "$TMP/out" 2> "$TMP/err"; then
  printf 'runner unexpectedly succeeded without AUDIT_MERGER_MODEL\n' >&2
  exit 1
fi
if printf '%s' "$prompt" | "$ROOT/.github/audit/copilot-agent.sh" > "$TMP/out" 2> "$TMP/err"; then
  printf 'agent unexpectedly succeeded without AUDIT_MERGER_MODEL\n' >&2
  exit 1
fi
printf 'PASS Copilot wrappers preserve argv, stdin prompt, and required model\n'
