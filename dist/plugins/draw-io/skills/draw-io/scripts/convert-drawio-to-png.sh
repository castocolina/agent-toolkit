#!/bin/bash
set -e

# Convert .drawio files to .drawio.png
generated_files=()

for drawio in "$@"; do
  png="${drawio%.drawio}.drawio.png"
  echo "Converting $drawio to $png..."

  # DRAWIO_BACKGROUND=transparent|light|dark|#rrggbb|file
  # transparent: pass -t. light/dark/#rrggbb: rewrite background on a temp copy, no -t.
  # file (default): export the file as stored, no -t.
  mode="${DRAWIO_BACKGROUND:-file}"
  src="$drawio"
  tmp=""
  bg=""
  extra=()
  case "$mode" in
    transparent) extra+=(-t) ;;
    file) ;;
    light) bg="#ffffff" ;;
    dark) bg="#1e1e1e" ;;
    \#*) bg="$mode" ;;
    *) echo "DRAWIO_BACKGROUND must be transparent, light, dark, file, or #rrggbb" >&2; exit 1 ;;
  esac
  if [ -n "${bg:-}" ]; then
    tmp="$(mktemp "${TMPDIR:-/tmp}/drawio.XXXXXX")"
    if grep -q 'background="' "$drawio"; then
      sed "s|background=\"[^\"]*\"|background=\"${bg}\"|" "$drawio" > "$tmp"
    else
      sed "s|<mxGraphModel|<mxGraphModel background=\"${bg}\"|" "$drawio" > "$tmp"
    fi
    src="$tmp"
  fi
  if ! drawio -x -f png -s 2 "${extra[@]}" -o "$png" "$src" 2>/dev/null; then
    [ -n "$tmp" ] && rm -f "$tmp"
    echo "✗ drawio PNG export failed for $drawio" >&2
    continue
  fi

  generated_files+=("$png")
  [ -n "${tmp:-}" ] && rm -f "$tmp"
  echo "✓ Generated $png"
done

# Stage all generated files at once to avoid index.lock conflicts
if [ ${#generated_files[@]} -gt 0 ]; then
  git add "${generated_files[@]}"
  echo "Staged ${#generated_files[@]} file(s)"
fi
