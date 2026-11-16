#!/bin/bash
# Converter stub: status lines on stdout, writes a PNG, git-adds it in CWD.
# Like the real converter it records its working directory and lets a failed
# git add fail the stub, so a wrong-working-directory regression surfaces
# instead of being masked by a canned exit 0.
# The mode (png|none|bad|big) is read from the file "$0.mode" next to the copy.
set -e
echo "Converting inputs..."
mode=$(cat "$0.mode" 2>/dev/null || echo png)
generated=()
for src in "$@"; do
  case "$src" in
    *.drawio) out="${src%.drawio}.drawio.png" ;;
    *) continue ;;
  esac
  case "$mode" in
    png) printf '\211PNG\r\n\032\nembedded' > "$out"; echo "Generated $out"; generated+=("$out") ;;
    big) printf '\211PNG\r\n\032\nembedded' > "$out"; head -c 10485761 /dev/zero >> "$out"; echo "Generated $out"; generated+=("$out") ;;
    none) echo "no output for $src" ;;
    bad) printf 'not a png' > "$out"; echo "Generated $out"; generated+=("$out") ;;
  esac
done
if [ -n "${STUB_CWD_LOG:-}" ]; then
  printf '%s git=%s\n' "$PWD" "$(git rev-parse --is-inside-work-tree 2>/dev/null || echo false)" >> "$STUB_CWD_LOG"
fi
if [ ${#generated[@]} -gt 0 ]; then git add -- "${generated[@]}"; fi
