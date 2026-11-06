#!/bin/bash
# Convert .drawio files to .drawio.png (2x, diagram embedded).
# Status lines go to stderr; stdout is one JSON array, one object per input.
set -e

usage() {
  cat << 'EOF'
Usage: convert-drawio-to-png.sh [--stage] [--] FILE.drawio...

Writes FILE.drawio.png next to each input (2x scale, diagram embedded with -e).
Each export goes to a temp file and replaces the PNG only after it parses as a
complete PNG with decodable embedded draw.io XML; a failed, truncated or timed-out
export leaves the previous PNG as it was and the run continues with the next file.

  --stage     git add the generated PNGs (for a pre-commit hook). Off by default.
  -h, --help  Show this help.

DRAWIO_BACKGROUND (default file):
  file         export the page background as stored, no -t
  transparent  pass -t (it overrides any stored background)
  light|dark   export a temp copy with background #ffffff|#1e1e1e, no -t
  #rrggbb      export a temp copy with that background, no -t
  (the copy sets background on every page's <mxGraphModel>; the source is untouched)

DRAWIO_TIMEOUT (default 120): seconds allowed per drawio call. Needs timeout(1)
  or gtimeout (Homebrew coreutils); with neither, the script stops before running drawio. 0 runs drawio unbounded.

Stdout: [{"drawio":"a.drawio","png":"a.drawio.png","ok":true}, ...]
Exit: 0 all exported, 1 any export (or --stage) failed, 2 usage error.
EOF
}

stage=0
files=()
opts_done=0
for arg in "$@"; do
  if [ "$opts_done" = 1 ]; then files+=("$arg"); continue; fi
  case "$arg" in
    -h | --help) usage; exit 0 ;;
    --stage) stage=1 ;;
    --) opts_done=1 ;;
    -*) echo "unknown option: $arg" >&2; usage >&2; exit 2 ;;
    *) files+=("$arg") ;;
  esac
done
[ ${#files[@]} -gt 0 ] || { usage >&2; exit 2; }

mode="${DRAWIO_BACKGROUND:-file}"
bg=""
extra=()
case "$mode" in
  file) ;;
  transparent) extra=(-t) ;;
  light) bg="#ffffff" ;;
  dark) bg="#1e1e1e" ;;
  *)
    if [[ "$mode" =~ ^#[0-9A-Fa-f]{6}$ ]]; then bg="$mode"; else
      echo "DRAWIO_BACKGROUND must be transparent, light, dark, file, or #rrggbb (got: $mode)" >&2
      exit 2
    fi
    ;;
esac

timeout_s="${DRAWIO_TIMEOUT:-120}"
if ! [[ "$timeout_s" =~ ^[0-9]+$ ]]; then
  echo "DRAWIO_TIMEOUT must be a whole number of seconds, 0 for no bound (got: $timeout_s)" >&2
  exit 2
fi

command -v drawio > /dev/null 2>&1 || { echo "drawio CLI not found on PATH" >&2; exit 1; }
bounded=()
if [ "$timeout_s" != 0 ]; then
  # gtimeout is GNU timeout as installed by Homebrew coreutils on macOS.
  tbin=$(command -v timeout || command -v gtimeout) || {
    echo "timeout(1) not found (nor gtimeout): install GNU coreutils (macOS: brew install coreutils), or set DRAWIO_TIMEOUT=0 to run drawio unbounded" >&2
    exit 1
  }
  bounded=("$tbin" -k 5 "$timeout_s")
fi

TMPS=()
cleanup() { [ ${#TMPS[@]} -eq 0 ] || rm -rf "${TMPS[@]}"; }
trap cleanup EXIT

# Sets background on every <mxGraphModel> of a temp copy; parses XML, so quoting and page count do not matter.
SET_BG_PY='
import sys, xml.etree.ElementTree as ET
src, dst, bg = sys.argv[1:4]
try:
    tree = ET.parse(src)
except ET.ParseError as e:
    sys.exit(f"not valid XML: {e}")
pages = list(tree.iter("diagram"))
models = list(tree.iter("mxGraphModel"))
if not models or any(d.find("mxGraphModel") is None for d in pages):
    sys.exit("no <mxGraphModel> to set background on (compressed? decode it first)")
for m in models:
    m.set("background", bg)
tree.write(dst, encoding="unicode")
'
# Accepts only a complete PNG (CRC-checked chunks; a 13-byte IHDR first with nonzero
# size; at least one IDAT; an empty IEND last) whose zTXt "mxGraphModel" chunk
# (drawio -e) decodes to a draw.io document: <mxfile> with a <diagram>, or <mxGraphModel>.
CHECK_PNG_PY='
import struct, sys, urllib.parse, zlib, xml.etree.ElementTree as ET
b = open(sys.argv[1], "rb").read()
if b[:8] != b"\x89PNG\r\n\x1a\n":
    sys.exit(1)
i, kinds, xml = 8, [], None
while i < len(b):
    if i + 12 > len(b):
        sys.exit(1)
    (n,) = struct.unpack(">I", b[i:i + 4])
    kind, data, crc = b[i + 4:i + 8], b[i + 8:i + 8 + n], b[i + 8 + n:i + 12 + n]
    if len(data) != n or len(crc) != 4 or struct.unpack(">I", crc)[0] != zlib.crc32(kind + data):
        sys.exit(1)
    kinds.append(kind)
    if kind == b"zTXt" and data.startswith(b"mxGraphModel\0\0"):
        xml = urllib.parse.unquote(zlib.decompress(data[14:]).decode("utf-8"))
    i += 12 + n
if len(b) < 33 or b[8:16] != b"\x00\x00\x00\x0dIHDR" or 0 in struct.unpack(">II", b[16:24]):
    sys.exit(1)
if b"IDAT" not in kinds or kinds[-1] != b"IEND" or b[-12:-8] != b"\x00\x00\x00\x00" or not xml:
    sys.exit(1)
doc = ET.fromstring(xml)
sys.exit(not (doc.tag == "mxGraphModel" or (doc.tag == "mxfile" and doc.find("diagram") is not None)))
'

generated=()
failures=0
results=() # drawio, png, ok triplets; serialized by json.dumps at the end
for drawio in "${files[@]}"; do
  png="${drawio%.drawio}.drawio.png"
  echo "Converting $drawio to $png..." >&2
  ok=false
  work=""
  if [ ! -f "$drawio" ]; then
    echo "✗ $drawio: no such file" >&2
  elif ! work=$(mktemp -d "$(dirname "$png")/.drawio-export.XXXXXX"); then
    echo "✗ cannot create a temp directory next to $png" >&2
  else
    TMPS+=("$work")
    src="$drawio"
    rc=0
    if [ -n "$bg" ]; then
      src="$work/src.drawio"
      python3 -c "$SET_BG_PY" "$drawio" "$src" "$bg" || rc=$?
    fi
    # --disable-update: the AppImage build can hang an export while it auto-updates.
    [ "$rc" -ne 0 ] || "${bounded[@]}" drawio --disable-update -x -f png -e -s 2 "${extra[@]}" -o "$work/out.png" "$src" >&2 || rc=$?
    if [ -n "$bg" ] && [ ! -f "$src" ]; then
      echo "✗ $drawio: background not set" >&2
    elif [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then
      echo "✗ drawio timed out after ${timeout_s}s on $drawio" >&2
      echo "  hint: a drawio instance left hung by an earlier run (check: pgrep -af '[d]rawio'), or an AppImage auto-update in progress" >&2
    elif [ "$rc" -ne 0 ]; then
      echo "✗ drawio PNG export failed for $drawio" >&2
    elif ! python3 -c "$CHECK_PNG_PY" "$work/out.png" 2> /dev/null; then
      echo "✗ $drawio output is not a PNG with embedded draw.io data" >&2
    else
      mv -f "$work/out.png" "$png"
      ok=true
      generated+=("$png")
      echo "✓ Generated $png" >&2
    fi
    rm -rf "$work"
  fi
  [ "$ok" = true ] || failures=1
  results+=("$drawio" "$png" "$ok")
done

if [ "$stage" = 1 ] && [ ${#generated[@]} -gt 0 ]; then
  # One git add for all files avoids index.lock races between parallel hook runs.
  if git add -- "${generated[@]}"; then
    echo "Staged ${#generated[@]} file(s)" >&2
  else
    echo "✗ git add failed" >&2
    failures=1
  fi
fi

python3 -c 'import json, sys
a = sys.argv[1:]
print(json.dumps([{"drawio": a[i], "png": a[i + 1], "ok": a[i + 2] == "true"} for i in range(0, len(a), 3)], separators=(",", ":")))' "${results[@]}"
[ "$failures" -eq 0 ]
