#!/bin/bash
# Test double for an eval runner: records each call under $STUB_STATE/calls and answers from $STUB_ANSWERS.
set -e
[ -n "$STUB_SLEEP" ] && sleep "$STUB_SLEEP"
calls="$STUB_STATE/calls"
mkdir -p "$calls"
n=$(find "$calls" -name '*.stdin' | wc -l)
cat > "$calls/$n.stdin"
pwd > "$calls/$n.pwd"
printf '%s\n' "$@" > "$calls/$n.argv"
ls -A > "$calls/$n.ls"
mode=$(sed -n '1s/^MODE: //p' "$calls/$n.stdin")
key=$(sed -n '2s/^KEY: //p' "$calls/$n.stdin")
file="$STUB_ANSWERS/$mode-${key//\//__}.txt"
[ -f "${file%.txt}.raw" ] && { cat "${file%.txt}.raw"; exit 0; }  # multi-line answer, returned whole
[ -f "$file" ] || { echo "stub-runner: no answer file $file" >&2; exit 1; }
counter="$STUB_STATE/counter-$(basename "$file")"
k=$(cat "$counter" 2>/dev/null || echo 0)
echo $((k + 1)) > "$counter"
lines=$(wc -l < "$file")
[ "$lines" -gt 0 ] || lines=1
sed -n "$((k % lines + 1))p" "$file"
