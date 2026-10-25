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
printf 'PNG\n' > "$out"
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

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
