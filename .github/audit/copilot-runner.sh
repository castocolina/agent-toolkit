#!/usr/bin/env bash
set -euo pipefail
: "${AUDIT_MERGER_MODEL:?AUDIT_MERGER_MODEL must be set}"
exec copilot -p "$(</dev/stdin)" -s --no-ask-user --model "$AUDIT_MERGER_MODEL" --available-tools ''
