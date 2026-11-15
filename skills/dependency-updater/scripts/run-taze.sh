#!/bin/bash
# Run taze in the current Node project. stdout is JSON status/output.
set -e

usage() {
    echo 'Usage: run-taze.sh [-r] [taze arguments]' >&2
    echo 'Pass --write only for an approved target set. Exit codes: 0 success/help, 1 missing taze, 2 missing package.json, 3 missing python3, delegated taze code otherwise.' >&2
    echo 'Accepted arguments: long options pass through to taze; a single-letter short option (-r, -h) is a scan flag; --write, -w, --interactive, -i and any short cluster containing w (-rw, -wr) are a write; any other combined short cluster (two or more letters after one dash) is treated as a write, so a potentially mutating call is never run as a scan.' >&2
    echo 'stdout shape: a candidate scan (no write argument) passes taze --json and prints {"status":"ok","candidates":<taze JSON>}; a write run, or taze output that is not valid JSON, prints {"status":"ok","output":"<text report>"}; a failure prints {"status":"error",...}.' >&2
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

if ! command -v python3 >/dev/null 2>&1; then
    echo 'python3 is required to build the JSON result' >&2
    printf '{"status":"error","diagnostic":"python3 is not installed"}\n'
    exit 3
fi

# A potentially mutating call is never a scan: --write, --interactive and -i (interactive mode can write after
# confirmation), any single-dash argument containing w (-w, -rw, -wr), and any other combined short cluster
# (single dash, two or more letters) count as a write.
mode=scan
has_json=0
for arg in "$@"; do
    case "$arg" in
        --write|--interactive) mode=write ;;
        --json) has_json=1 ;;
        --*) ;;
        -*w*|-i) mode=write ;;
        -?) ;;
        -*) mode=write ;;
    esac
done
if [ "$mode" = scan ] && [ "$has_json" = 0 ]; then
    set -- "$@" --json
fi

output=$(taze "$@") || { rc=$?; printf '{"status":"error","exit_code":%s}\n' "$rc"; printf '%s\n' "$output" >&2; exit "$rc"; }
printf '%s\n' "$output" | python3 -c 'import json,sys
mode=sys.argv[1]
text=sys.stdin.read()
result={"status":"ok"}
try:
    if mode!="scan":
        raise ValueError("write run keeps the text report")
    result["candidates"]=json.loads(text)
except ValueError:
    result["output"]=text
print(json.dumps(result))' "$mode"
