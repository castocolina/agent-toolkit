#!/bin/bash
# Run taze in the current Node project. stdout is JSON status/output.
set -e

usage() {
    echo 'Usage: run-taze.sh [-r] [taze arguments]' >&2
    echo 'Pass --write only for an approved target set. Exit codes: 0 success/help, 1 missing taze, 2 missing package.json or rejected global mode (--global, -g), 3 missing python3, delegated taze code otherwise.' >&2
    echo 'Accepted arguments: long options pass through to taze; a single-letter short option (-r, -h) is a scan flag; --write, -w, --update, -u, --install, -i, --interactive, -I (the long four also as --flag=value, for example --write=true) and any short cluster containing w (-rw, -wr) are a write (per taze src/cli.ts: -u updates directly after bumping, -i installs after bumping, -I is interactive mode); any other combined short cluster (two or more letters after one dash) is treated as a write, so a potentially mutating call is never run as a scan.' >&2
    echo 'Rejected: --global, --global=<value> and -g (also inside a short cluster such as -rg) select taze global-package mode (checkGlobal in src/cli.ts); this wrapper scans a project, so it prints {"status":"error","diagnostic":...} and exits 2 without running taze.' >&2
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

# A potentially mutating call is never a scan: --write/-w, --update/-u (update directly after bumping),
# --install/-i (install after bumping), --interactive/-I (interactive mode can write after confirmation; taze
# source: https://github.com/antfu-collective/taze/blob/main/src/cli.ts, checked 2026-11-15), any single-dash
# argument containing w (-rw, -wr), and any other combined short cluster (single dash, two or more letters)
# count as a write; the long write options also count with a value (--write=true). --global and -g (also inside
# a cluster such as -rg) select taze's global-package mode (checkGlobal in src/cli.ts) and are rejected with a
# JSON error and exit 2, because this wrapper scans a project.
reject_global() {
    echo 'taze global mode (--global, -g, also inside a short cluster such as -rg) is out of scope: this wrapper scans a project' >&2
    printf '{"status":"error","diagnostic":"taze global mode (--global, -g) is out of scope for this wrapper, which scans a project"}\n'
    exit 2
}
mode=scan
has_json=0
for arg in "$@"; do
    case "$arg" in
        --global|--global=*) reject_global ;;
        --write|--write=*|--update|--update=*|--install|--install=*|--interactive|--interactive=*|-u|-i|-I) mode=write ;;
        --json) has_json=1 ;;
        --*) ;;
        -*g*) reject_global ;;
        -*w*) mode=write ;;
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
