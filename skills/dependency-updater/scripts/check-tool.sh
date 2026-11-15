#!/bin/bash
# Check a prerequisite. stdout is one JSON result; diagnostics go to stderr.
set -e

usage() {
    echo 'Usage: check-tool.sh <tool-name> [install-command]' >&2
}

if [ "${1:-}" = --help ] || [ "${1:-}" = -h ]; then
    usage
    echo 'Exit codes: 0 installed, 1 missing/invalid arguments.' >&2
    exit 0
fi

TOOL_NAME="${1:-}"
INSTALL_CMD="${2:-}"
if [ -z "$TOOL_NAME" ]; then
    usage
    printf '{"status":"error","diagnostic":"tool name is required"}\n'
    exit 1
fi

# Escape backslash, quote and the common control characters; drop the other control bytes (JSON forbids them raw).
json_string() {
    local value=${1//\\/\\\\}
    value=${value//\"/\\\"}
    value=${value//$'\n'/\\n}
    value=${value//$'\r'/\\r}
    value=${value//$'\t'/\\t}
    value=${value//$'\b'/\\b}
    value=${value//$'\f'/\\f}
    printf '%s' "$value" | tr -d '\000-\037'
}
if command -v "$TOOL_NAME" >/dev/null 2>&1; then
    printf '{"status":"ok","tool":"%s"}\n' "$(json_string "$TOOL_NAME")"
    "$TOOL_NAME" --version >&2 2>/dev/null || true
    exit 0
fi
printf '{"status":"missing","tool":"%s","install":"%s"}\n' "$(json_string "$TOOL_NAME")" "$(json_string "$INSTALL_CMD")"
exit 1
