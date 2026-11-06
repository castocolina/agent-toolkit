#!/bin/bash
# Tests for skills/draw-io/scripts/convert-drawio-to-png.sh.
HERE=$(cd "$(dirname "$0")" && pwd)
CONV=$HERE/../../../skills/draw-io/scripts/convert-drawio-to-png.sh
FAILS=0 TMPS=()
trap 'rm -rf "${TMPS[@]}"' EXIT

check() {
  if [ "$2" != "$3" ]; then echo "  FAIL: $1: got [$2] want [$3]"; FAILS=$((FAILS + 1)); TESTFAIL=1; fi
}
t() {
  TESTFAIL=0; "$1"
  if [ $TESTFAIL = 0 ]; then echo "PASS $1"; else echo "FAIL $1"; fi
}

# Writes a PNG like drawio -e does: IHDR, a zTXt "mxGraphModel" chunk holding the
# URL-encoded source, IDAT, IEND. Modes: ok, trunc (cut mid-file), nodata (no zTXt),
# noidat (CRC-valid but no image data), notdrawio (embedded XML is not a draw.io document),
# zerodim (IHDR width 0).
write_png_maker() {
  cat > "$1/mkpng.py" << 'EOF'
import struct, sys, urllib.parse, zlib
out, mode, src = sys.argv[1:4]
def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
body = "<svg/>" if mode == "notdrawio" else open(src, encoding="utf-8").read()
xml = urllib.parse.quote(body, safe="").encode()
png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 0 if mode == "zerodim" else 1, 1, 8, 2, 0, 0, 0))
if mode != "nodata":
    png += chunk(b"zTXt", b"mxGraphModel\0\0" + zlib.compress(xml))
if mode != "noidat":
    png += chunk(b"IDAT", zlib.compress(b"\0\0\0\0"))
png += chunk(b"IEND", b"")
open(out, "wb").write(png[: len(png) // 2] if mode == "trunc" else png)
EOF
}

# Stub drawio: logs argv and the exported source. Input name picks the outcome:
# *bad* exits 1, *empty* writes 0 bytes, *trunc*/*nodata* write a broken PNG,
# *slow* sleeps past the timeout, anything else writes a valid embedded PNG.
write_drawio_stub() {
  mkdir -p "$1/bin"
  write_png_maker "$1"
  cat > "$1/bin/drawio" << 'EOF'
#!/bin/bash
printf '%s\n' "$*" >> "$ROOT/argv"
out="" src=""
args=("$@")
i=0
while [ $i -lt ${#args[@]} ]; do
  case "${args[$i]}" in
    -o) i=$((i + 1)); out=${args[$i]} ;;
    *.drawio) src=${args[$i]} ;;
  esac
  i=$((i + 1))
done
cat "$src" > "$ROOT/src"
case "$src" in
  *bad*) echo "bad input" >&2; exit 1 ;;
  *empty*) : > "$out"; exit 0 ;;
  *trunc*) exec python3 "$ROOT/mkpng.py" "$out" trunc "$src" ;;
  *nodata*) exec python3 "$ROOT/mkpng.py" "$out" nodata "$src" ;;
  *noidat*) exec python3 "$ROOT/mkpng.py" "$out" noidat "$src" ;;
  *notdrawio*) exec python3 "$ROOT/mkpng.py" "$out" notdrawio "$src" ;;
  *zerodim*) exec python3 "$ROOT/mkpng.py" "$out" zerodim "$src" ;;
  *slow*) sleep 10 ;;
esac
python3 "$ROOT/mkpng.py" "$out" ok "$src"
EOF
  chmod +x "$1/bin/drawio"
}

setup() { # work dir with flow.drawio and a drawio stub; sets ROOT. $1=git to init a repo
  ROOT=$(mktemp -d); TMPS+=("$ROOT")
  mkdir -p "$ROOT/work"
  printf '<mxfile><diagram><mxGraphModel background="#123456"><root/></mxGraphModel></diagram></mxfile>\n' > "$ROOT/work/flow.drawio"
  write_drawio_stub "$ROOT"
  if [ "${1:-}" = git ]; then
    git init -q "$ROOT/work"
    git -C "$ROOT/work" config user.email t@example.com
    git -C "$ROOT/work" config user.name t
  fi
}

run() { # run the converter in $ROOT/work; sets CODE
  (cd "$ROOT/work" && PATH="$ROOT/bin:$PATH" ROOT="$ROOT" bash "$CONV" "$@") > "$ROOT/out" 2> "$ROOT/err" && CODE=0 || CODE=$?
}

staged() { git -C "$ROOT/work" diff --cached --name-only | tr '\n' ' ' | sed 's/ $//'; }
exists() { [ -e "$1" ] && echo yes || echo no; }

test_help_exits_zero() {
  setup
  run --help
  check exit "$CODE" 0
  check usage "$(grep -c '^Usage: convert-drawio-to-png.sh' "$ROOT/out")" 1
  check no_drawio_call "$(exists "$ROOT/argv")" no
}

test_usage_errors_exit_2() {
  setup
  run
  check no_args "$CODE" 2
  run --bogus flow.drawio
  check unknown_option "$CODE" 2
  check no_drawio_call "$(exists "$ROOT/argv")" no
}

test_passes_embed_and_disable_update_flags() {
  setup
  run flow.drawio
  check exit "$CODE" 0
  check embed "$(grep -c -- ' -e ' "$ROOT/argv")" 1
  check disable_update "$(grep -c -- '--disable-update' "$ROOT/argv")" 1
  check wrote "$(head -c 4 "$ROOT/work/flow.drawio.png" | tail -c 3)" PNG
}

test_prints_json_results_on_stdout() {
  setup
  printf '<mxfile/>\n' > "$ROOT/work/bad.drawio"
  run flow.drawio bad.drawio
  check exit "$CODE" 1
  check json "$(cat "$ROOT/out")" '[{"drawio":"flow.drawio","png":"flow.drawio.png","ok":true},{"drawio":"bad.drawio","png":"bad.drawio.png","ok":false}]'
  check status_on_stderr "$(grep -c 'Generated flow.drawio.png' "$ROOT/err")" 1
}

test_works_outside_git_and_does_not_stage_by_default() {
  setup
  run flow.drawio
  check exit_outside_git "$CODE" 0
  setup git
  run flow.drawio
  check exit "$CODE" 0
  check no_staging "$(staged)" ""
  check no_staged_msg "$(grep -c Staged "$ROOT/err")" 0
}

test_stage_flag_stages_successes_but_exits_nonzero_on_failure() {
  setup git
  printf '<mxfile/>\n' > "$ROOT/work/bad.drawio"
  run --stage flow.drawio bad.drawio
  check exit "$CODE" 1
  check reports "$(grep -c 'drawio PNG export failed for bad.drawio' "$ROOT/err")" 1
  check staged "$(staged)" flow.drawio.png
  check staged_msg "$(grep -c 'Staged 1 file(s)' "$ROOT/err")" 1
  check bad_png_absent "$(exists "$ROOT/work/bad.drawio.png")" no
}

test_failed_export_keeps_previous_png() {
  setup
  printf '<mxfile/>\n' > "$ROOT/work/bad.drawio"
  printf 'OLD' > "$ROOT/work/bad.drawio.png"
  run bad.drawio
  check exit "$CODE" 1
  check previous_png_kept "$(cat "$ROOT/work/bad.drawio.png")" OLD
  check no_temp_left "$(find "$ROOT/work" -name '.drawio-export.*' | wc -l | tr -d ' ')" 0
}

test_empty_output_is_rejected_and_previous_png_kept() {
  setup
  printf '<mxfile/>\n' > "$ROOT/work/empty.drawio"
  printf 'OLD' > "$ROOT/work/empty.drawio.png"
  run empty.drawio
  check exit "$CODE" 1
  check reports "$(grep -c 'output is not a PNG with embedded draw.io data' "$ROOT/err")" 1
  check previous_png_kept "$(cat "$ROOT/work/empty.drawio.png")" OLD
}

test_missing_input_fails_without_calling_drawio() {
  setup
  run nope.drawio
  check exit "$CODE" 1
  check reports "$(grep -c 'nope.drawio: no such file' "$ROOT/err")" 1
  check no_drawio_call "$(exists "$ROOT/argv")" no
}

test_background_modes() {
  local mode want_t want_bg
  while read -r mode want_t want_bg; do
    setup
    if [ "$mode" = unset ]; then run flow.drawio; else DRAWIO_BACKGROUND=$mode run flow.drawio; fi
    check "exit[$mode]" "$CODE" 0
    check "t_flag[$mode]" "$(grep -c -- ' -t ' "$ROOT/argv")" "$want_t"
    check "background[$mode]" "$(grep -o 'background="[^"]*"' "$ROOT/src")" "background=\"$want_bg\""
  done << 'EOF'
unset 0 #123456
file 0 #123456
transparent 1 #123456
light 0 #ffffff
dark 0 #1e1e1e
#a0b1c2 0 #a0b1c2
EOF
  setup
  printf '<mxfile><diagram><mxGraphModel><root/></mxGraphModel></diagram></mxfile>\n' > "$ROOT/work/flow.drawio"
  DRAWIO_BACKGROUND=dark run flow.drawio
  check inserted_background "$(grep -o 'background="[^"]*"' "$ROOT/src")" 'background="#1e1e1e"'
  check source_untouched "$(grep -c background "$ROOT/work/flow.drawio")" 0
  for mode in blue '#12345' '#12345g|x'; do
    setup
    DRAWIO_BACKGROUND=$mode run flow.drawio
    check "invalid[$mode]" "$CODE" 2
    check "no_drawio_call[$mode]" "$(exists "$ROOT/argv")" no
  done
}

test_broken_png_is_a_failure_and_keeps_previous_png() {
  local name
  for name in trunc nodata noidat notdrawio zerodim; do
    setup
    # valid source XML: each fixture would pass in ok mode without its targeted PNG corruption
    cp "$ROOT/work/flow.drawio" "$ROOT/work/$name.drawio"
    printf 'OLD' > "$ROOT/work/$name.drawio.png"
    run "$name.drawio" flow.drawio
    check "exit[$name]" "$CODE" 1
    check "reports[$name]" "$(grep -c "$name.drawio output is not a PNG with embedded draw.io data" "$ROOT/err")" 1
    check "previous_png_kept[$name]" "$(cat "$ROOT/work/$name.drawio.png")" OLD
    check "continues[$name]" "$(exists "$ROOT/work/flow.drawio.png")" yes
    check "no_temp_left[$name]" "$(find "$ROOT/work" -name '.drawio-export.*' | wc -l | tr -d ' ')" 0
  done
}

test_timeout_is_a_per_file_failure() {
  setup
  printf '<mxfile/>\n' > "$ROOT/work/slow.drawio"
  printf 'OLD' > "$ROOT/work/slow.drawio.png"
  local start=$SECONDS
  DRAWIO_TIMEOUT=1 run slow.drawio flow.drawio
  check exit "$CODE" 1
  check bounded "$([ $((SECONDS - start)) -lt 8 ] && echo yes || echo no)" yes
  check reports "$(grep -c 'drawio timed out after 1s on slow.drawio' "$ROOT/err")" 1
  check hint "$(grep -c "pgrep -af '\[d\]rawio'" "$ROOT/err")" 1
  check previous_png_kept "$(cat "$ROOT/work/slow.drawio.png")" OLD
  check continues "$(exists "$ROOT/work/flow.drawio.png")" yes
  check no_temp_left "$(find "$ROOT/work" -name '.drawio-export.*' | wc -l | tr -d ' ')" 0
  local bad
  for bad in -1 abc; do
    DRAWIO_TIMEOUT=$bad run flow.drawio
    check "invalid_timeout[$bad]" "$CODE" 2
  done
}

test_background_rewrite_parses_xml() {
  setup
  cat > "$ROOT/work/flow.drawio" << 'EOF'
<mxfile><diagram id='a'><mxGraphModel background='#123456' grid='1'><root/></mxGraphModel></diagram><diagram id="b"><mxGraphModel><root/></mxGraphModel></diagram></mxfile>
EOF
  cp "$ROOT/work/flow.drawio" "$ROOT/orig"
  DRAWIO_BACKGROUND=dark run flow.drawio
  check exit "$CODE" 0
  check every_page_dark "$(python3 -c 'import sys,xml.etree.ElementTree as E; m=list(E.parse(sys.argv[1]).iter("mxGraphModel")); print(sorted({x.get("background") for x in m}), len(m))' "$ROOT/src")" "['#1e1e1e'] 2"
  check source_untouched "$(cmp -s "$ROOT/work/flow.drawio" "$ROOT/orig" && echo same || echo changed)" same
  setup
  printf '<mxfile><diagram id="c">jZBNC4MwDIZ/Td5L</diagram></mxfile>\n' > "$ROOT/work/flow.drawio"
  printf 'OLD' > "$ROOT/work/flow.drawio.png"
  DRAWIO_BACKGROUND=light run flow.drawio
  check compressed_fails "$CODE" 1
  check compressed_reports "$(grep -c 'no <mxGraphModel> to set background on (compressed? decode it first)' "$ROOT/err")" 1
  check compressed_no_drawio_call "$(exists "$ROOT/argv")" no
  check compressed_previous_png_kept "$(cat "$ROOT/work/flow.drawio.png")" OLD
}

test_json_round_trips_tabs_and_newlines_in_names() {
  setup
  local tab=$'tab\there' nl=$'new\nline'
  cp "$ROOT/work/flow.drawio" "$ROOT/work/$tab.drawio"
  cp "$ROOT/work/flow.drawio" "$ROOT/work/$nl.drawio"
  run "$tab.drawio" "$nl.drawio" 'q"uote\.drawio'
  check exit "$CODE" 1
  check parsed "$(python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin)))' < "$ROOT/out")" \
    '[{"drawio": "tab\there.drawio", "png": "tab\there.drawio.png", "ok": true}, {"drawio": "new\nline.drawio", "png": "new\nline.drawio.png", "ok": true}, {"drawio": "q\"uote\\.drawio", "png": "q\"uote\\.drawio.png", "ok": false}]'
}

test_missing_timeout_fails_before_drawio() {
  setup
  printf 'OLD' > "$ROOT/work/flow.drawio.png"
  mkdir -p "$ROOT/tools"
  local tool
  for tool in python3 mktemp dirname rm mv cat; do ln -s "$(command -v "$tool")" "$ROOT/tools/$tool"; done
  (cd "$ROOT/work" && PATH="$ROOT/bin:$ROOT/tools" ROOT="$ROOT" "$BASH" "$CONV" flow.drawio) > "$ROOT/out" 2> "$ROOT/err" && CODE=0 || CODE=$?
  check exit "$CODE" 1
  check reports "$(grep -c 'timeout(1) not found' "$ROOT/err")" 1
  check no_drawio_call "$(exists "$ROOT/argv")" no
  check previous_png_kept "$(cat "$ROOT/work/flow.drawio.png")" OLD
  (cd "$ROOT/work" && PATH="$ROOT/bin:$ROOT/tools" ROOT="$ROOT" DRAWIO_TIMEOUT=0 "$BASH" "$CONV" flow.drawio) > "$ROOT/out" 2> "$ROOT/err" && CODE=0 || CODE=$?
  check opt_out_exit "$CODE" 0
  check opt_out_exported "$(head -c 4 "$ROOT/work/flow.drawio.png" | tail -c 3)" PNG
}

test_gtimeout_is_used_when_timeout_is_missing() {
  setup
  mkdir -p "$ROOT/tools"
  local tool
  for tool in python3 mktemp dirname rm mv cat; do ln -s "$(command -v "$tool")" "$ROOT/tools/$tool"; done
  cat > "$ROOT/bin/gtimeout" << 'EOF'
#!/bin/bash
printf '%s\n' "$*" > "$ROOT/gtimeout-argv"
shift 3
exec "$@"
EOF
  chmod +x "$ROOT/bin/gtimeout"
  (cd "$ROOT/work" && PATH="$ROOT/bin:$ROOT/tools" ROOT="$ROOT" DRAWIO_TIMEOUT=7 "$BASH" "$CONV" flow.drawio) > "$ROOT/out" 2> "$ROOT/err" && CODE=0 || CODE=$?
  check exit "$CODE" 0
  check gtimeout_used "$(cut -d' ' -f1-4 "$ROOT/gtimeout-argv" 2> /dev/null)" "-k 5 7 drawio"
  check exported "$(head -c 4 "$ROOT/work/flow.drawio.png" | tail -c 3)" PNG
}

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
