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

test_converter_passes_embed_flag() {
  local root; root=$(mktemp -d); TMPS+=("$root")
  mkdir -p "$root/bin" "$root/work"
  cat > "$root/bin/drawio" << 'EOF'
#!/bin/bash
printf '%s\n' "$*" > "$DRAWIO_ARGV_LOG"
out=""
args=("$@")
i=0
while [ $i -lt ${#args[@]} ]; do
  if [ "${args[$i]}" = -o ]; then i=$((i + 1)); out=${args[$i]}; fi
  i=$((i + 1))
done
printf '\211PNG\r\n\032\n' > "$out"
EOF
  chmod +x "$root/bin/drawio"
  printf '<mxfile></mxfile>\n' > "$root/work/flow.drawio"
  git init -q "$root/work"
  git -C "$root/work" config user.email t@example.com
  git -C "$root/work" config user.name t
  (cd "$root/work" && PATH="$root/bin:$PATH" DRAWIO_ARGV_LOG="$root/argv" bash "$CONV" flow.drawio) >"$root/out" 2>"$root/err" && CODE=0 || CODE=$?
  check exit "$CODE" 0
  check embed "$(grep -c -- ' -e ' "$root/argv" || true)" 1
  check wrote "$([ -s "$root/work/flow.drawio.png" ] && echo yes || echo no)" yes
}

write_failing_drawio_stub() { # exits 1 without writing an output
  local root=$1
  mkdir -p "$root/bin"
  cat > "$root/bin/drawio" << 'EOF'
#!/bin/bash
echo "drawio exploded" >&2
exit 1
EOF
  chmod +x "$root/bin/drawio"
}

write_empty_drawio_stub() { # succeeds but writes a zero-byte PNG
  local root=$1
  mkdir -p "$root/bin"
  cat > "$root/bin/drawio" << 'EOF'
#!/bin/bash
out=""
args=("$@")
i=0
while [ $i -lt ${#args[@]} ]; do
  if [ "${args[$i]}" = -o ]; then i=$((i + 1)); out=${args[$i]}; fi
  i=$((i + 1))
done
: > "$out"
EOF
  chmod +x "$root/bin/drawio"
}

init_conv_repo() { # git repo with flow.drawio; sets ROOT
  ROOT=$(mktemp -d); TMPS+=("$ROOT")
  mkdir -p "$ROOT/work"
  printf '<mxfile></mxfile>\n' > "$ROOT/work/flow.drawio"
  git init -q "$ROOT/work"
  git -C "$ROOT/work" config user.email t@example.com
  git -C "$ROOT/work" config user.name t
}

test_converter_exits_nonzero_when_export_fails() {
  init_conv_repo
  write_failing_drawio_stub "$ROOT"
  (cd "$ROOT/work" && PATH="$ROOT/bin:$PATH" bash "$CONV" flow.drawio) >"$ROOT/out" 2>"$ROOT/err" && CODE=0 || CODE=$?
  check exit "$([ "$CODE" -ne 0 ] && echo nonzero || echo zero)" nonzero
  check reports "$(grep -c 'drawio PNG export failed' "$ROOT/err")" 1
  check no_png "$([ -e "$ROOT/work/flow.drawio.png" ] && echo yes || echo no)" no
  check no_staging "$(git -C "$ROOT/work" diff --cached --name-only | wc -l | tr -d ' ')" 0
  check no_staged_msg "$(grep -c Staged "$ROOT/out")" 0
}

test_converter_rejects_empty_png() {
  init_conv_repo
  write_empty_drawio_stub "$ROOT"
  (cd "$ROOT/work" && PATH="$ROOT/bin:$PATH" bash "$CONV" flow.drawio) >"$ROOT/out" 2>"$ROOT/err" && CODE=0 || CODE=$?
  check exit "$([ "$CODE" -ne 0 ] && echo nonzero || echo zero)" nonzero
  check reports "$(grep -c 'not a non-empty PNG' "$ROOT/err")" 1
  check png_removed "$([ -e "$ROOT/work/flow.drawio.png" ] && echo yes || echo no)" no
  check no_staging "$(git -C "$ROOT/work" diff --cached --name-only | wc -l | tr -d ' ')" 0
}

test_converter_stages_successes_but_exits_nonzero_on_failure() {
  init_conv_repo
  mkdir -p "$ROOT/bin"
  cat > "$ROOT/bin/drawio" << 'EOF'
#!/bin/bash
out=""
src=""
args=("$@")
i=0
while [ $i -lt ${#args[@]} ]; do
  case "${args[$i]}" in
    -o) i=$((i + 1)); out=${args[$i]} ;;
    *.drawio) src=${args[$i]} ;;
  esac
  i=$((i + 1))
done
case "$src" in
  *bad*) echo "bad input" >&2; exit 1 ;;
esac
printf '\211PNG\r\n\032\n' > "$out"
EOF
  chmod +x "$ROOT/bin/drawio"
  printf '<mxfile></mxfile>\n' > "$ROOT/work/bad.drawio"
  (cd "$ROOT/work" && PATH="$ROOT/bin:$PATH" bash "$CONV" flow.drawio bad.drawio) >"$ROOT/out" 2>"$ROOT/err" && CODE=0 || CODE=$?
  check exit "$([ "$CODE" -ne 0 ] && echo nonzero || echo zero)" nonzero
  check reports "$(grep -c 'drawio PNG export failed' "$ROOT/err")" 1
  check good_png "$([ -s "$ROOT/work/flow.drawio.png" ] && echo yes || echo no)" yes
  check staged "$(git -C "$ROOT/work" diff --cached --name-only)" flow.drawio.png
  check staged_msg "$(grep -c 'Staged 1 file(s)' "$ROOT/out")" 1
  check bad_png_absent "$([ -e "$ROOT/work/bad.drawio.png" ] && echo yes || echo no)" no
}

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
