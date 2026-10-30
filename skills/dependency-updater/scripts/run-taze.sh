#!/bin/bash
# Run taze in the current Node project. stdout is JSON status/output.
set -e

usage() {
    echo 'Usage: run-taze.sh [-r] [taze arguments]' >&2
    echo 'Pass --write only for an approved target set. Exit codes: 0 success/help, 1 missing taze, 2 missing package.json, delegated taze code otherwise.' >&2
}

if [ "${1:-}" = --help ] || [ "${1:-}" = -h ]; then
    usage
    exit 0
fi

if ! command -v taze >/dev/null 2>&1; then
    echo 'taze is not installed (install with npm install -g taze or use npx taze)' >&2
    printf '{"status":"error","diagnostic":"taze is not installed"}\n'
    exit 1
fi
if [ ! -f package.json ]; then
    echo 'No package.json found in current directory' >&2
    printf '{"status":"error","diagnostic":"No package.json found in current directory"}\n'
    exit 2
fi

output=$(taze "$@") || { rc=$?; printf '{"status":"error","exit_code":%s}\n' "$rc"; printf '%s\n' "$output" >&2; exit "$rc"; }
python3 -c 'import json,sys; print(json.dumps({"status":"ok","output":sys.stdin.read()}))' <<< "$output"
