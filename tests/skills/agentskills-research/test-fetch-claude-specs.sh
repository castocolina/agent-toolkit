#!/bin/bash
# Tests for fetch-claude-specs.sh; synthetic pages are served through file:// URLs.
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
FETCH=$REPO/skills/agentskills-research/scripts/fetch-claude-specs.sh
FAILS=0 TMPS=()
trap 'rm -rf "${TMPS[@]}"' EXIT
cd "$REPO" || exit 1 # the script needs a git repository as cwd

setup() { # sets T; pages live in $T/fx, pin in $T/cc, profiles in $T/profiles
  T=$(mktemp -d); TMPS+=("$T"); mkdir "$T/fx" "$T/profiles"
  for p in skills sub-agents plugins-reference; do printf '# Synthetic %s\n\nbody of %s\n' "$p" "$p" > "$T/fx/$p.md"; done
  for k in command agent; do printf 'profile_version: 1\nsource_digest: %s\n\n# %s\n' "$(printf 0%.0s {1..64})" "$k" > "$T/profiles/$k.md"; done
}
run() { # run [extra args]; stdout -> $OUT, exit -> $CODE
  OUT=$(bash "$FETCH" --dest "$T/cc" --profiles "$T/profiles" --base "file://$T/fx" "$@" 2>"$T/err") && CODE=0 || CODE=$?
}
j() { jq -c "$1" <<<"$OUT"; }
adopt() { # profiles take the digests of the last run
  for k in command agent; do printf 'profile_version: 1\nsource_digest: %s\n\n# %s\n' "$(jq -r ".digests.$k" <<<"$OUT")" "$k" > "$T/profiles/$k.md"; done
}
check() {
  if [ "$2" != "$3" ]; then echo "  FAIL: $1: got [$2] want [$3]"; FAILS=$((FAILS + 1)); TESTFAIL=1; fi
}
t() { TESTFAIL=0; "$1"; if [ $TESTFAIL = 0 ]; then echo "PASS $1"; else echo "FAIL $1"; fi; }

test_first_run_writes_pin() {
  setup; run
  check exit "$CODE" 0
  check changed "$(j .changed)" '["skills","sub-agents","plugins-reference"]'
  check unchanged "$(j .unchanged)" '[]'
  check stale "$(j .profiles_stale)" '["command","agent"]'
  check url "$(jq -r .pages.skills.url "$T/cc/SOURCE.json")" "file://$T/fx/skills.md"
  check keys "$(jq -c 'keys' "$T/cc/SOURCE.json")" '["base","digests","fetched_at","pages"]'
  local sk pr exp
  sk=$(sha256sum < "$T/fx/skills.md" | cut -d' ' -f1); pr=$(sha256sum < "$T/fx/plugins-reference.md" | cut -d' ' -f1)
  exp=$(printf 'plugins-reference %s\nskills %s\n' "$pr" "$sk" | sha256sum | cut -d' ' -f1)
  check command-digest "$(j .digests.command)" "\"$exp\""
}
test_second_run_is_untouched() {
  setup; run; adopt; local before; before=$(sha256sum < "$T/cc/SOURCE.json"); sleep 1; run
  check exit "$CODE" 0
  check changed "$(j .changed)" '[]'
  check unchanged "$(j .unchanged)" '["skills","sub-agents","plugins-reference"]'
  check stale "$(j .profiles_stale)" '[]'
  check pin "$(sha256sum < "$T/cc/SOURCE.json")" "$before"
}
test_one_page_changes_one_kind() {
  setup; run; adopt; local c; c=$(j .digests.command); echo more >> "$T/fx/sub-agents.md"; run
  check changed "$(j .changed)" '["sub-agents"]'
  check command-digest "$(j .digests.command)" "$c"
  check stale "$(j .profiles_stale)" '["agent"]'
}
test_empty_page_keeps_pin() {
  setup; run; local before; before=$(sha256sum < "$T/cc/SOURCE.json"); : > "$T/fx/skills.md"; run
  check exit "$CODE" 1
  check pin "$(sha256sum < "$T/cc/SOURCE.json")" "$before"
}
test_html_page_keeps_pin() {
  setup; run; local before; before=$(sha256sum < "$T/cc/SOURCE.json")
  printf '\n  <!DOCTYPE html>\n<p>x</p>\n' > "$T/fx/sub-agents.md"; run
  check exit "$CODE" 1
  check pin "$(sha256sum < "$T/cc/SOURCE.json")" "$before"
  printf '<HTML><body>x</body></HTML>\n' > "$T/fx/sub-agents.md"; run
  check html-tag "$CODE" 1
}
test_comment_or_mdx_first_is_accepted() {
  setup; printf '<!-- note -->\n# T\n' > "$T/fx/skills.md"; printf '<Note>hi</Note>\n# T\n' > "$T/fx/sub-agents.md"; run
  check exit "$CODE" 0
}
test_keep() {
  setup; run --keep
  local kept; kept=$(jq -r .kept <<<"$OUT")
  check exit "$CODE" 0
  check pages "$(ls "$kept" | sort | tr '\n' ' ')" 'plugins-reference.md skills.md sub-agents.md '
  rm -rf "$kept"
  setup; run
  check nokept "$(j 'has("kept")')" false
}
test_no_page_files_remain() {
  setup; mkdir "$T/tmpdir"; OUT=$(TMPDIR=$T/tmpdir bash "$FETCH" --dest "$T/cc" --profiles "$T/profiles" --base "file://$T/fx" 2>/dev/null) && CODE=0 || CODE=$?
  check exit "$CODE" 0
  check left "$(ls -A "$T/tmpdir" | wc -l)" 0
}
test_tmpdir_inside_repo_refused() {
  setup; mkdir -p "$REPO/.tmp-fcs-test"; TMPS+=("$REPO/.tmp-fcs-test")
  OUT=$(TMPDIR=$REPO/.tmp-fcs-test bash "$FETCH" --dest "$T/cc" --profiles "$T/profiles" --base "file://$T/fx" 2>"$T/err") && CODE=0 || CODE=$?
  check exit "$CODE" 1
  check nopin "$(test -e "$T/cc/SOURCE.json" && echo yes || echo no)" no
  check leftover "$(ls -A "$REPO/.tmp-fcs-test" | wc -l)" 0
  ln -s "$REPO/.tmp-fcs-test" "$T/link"
  OUT=$(TMPDIR=$T/link bash "$FETCH" --dest "$T/cc" --profiles "$T/profiles" --base "file://$T/fx" 2>"$T/err") && CODE=0 || CODE=$?
  check symlink-exit "$CODE" 1
  check symlink-msg "$(grep -c 'inside the repository' "$T/err")" 1
}
test_failure_after_publish_restores_pin() {
  setup; run; local before; before=$(sha256sum < "$T/cc/SOURCE.json"); echo more >> "$T/fx/skills.md"
  bash "$FETCH" --dest "$T/cc" --profiles "$T/profiles" --base "file://$T/fx" >/dev/full 2>"$T/err" && CODE=0 || CODE=$?
  check exit-nonzero "$([ "$CODE" != 0 ] && echo yes)" yes
  check pin "$(sha256sum < "$T/cc/SOURCE.json")" "$before"
  check restored "$(grep -c 'restored previous pin' "$T/err")" 1
  check nostray "$(ls -A "$T/cc" | tr '\n' ' ')" 'SOURCE.json '
  setup; bash "$FETCH" --dest "$T/cc" --profiles "$T/profiles" --base "file://$T/fx" >/dev/full 2>/dev/null || true
  check first-run-no-pin "$(ls -A "$T/cc" | wc -l)" 0
}
test_tmpdir_inside_other_worktree_refused() {
  setup; git worktree add -q --detach "$T/wt" HEAD || { check worktree-add 1 0; return; }
  mkdir "$T/wt/tmp"
  OUT=$(TMPDIR=$T/wt/tmp bash "$FETCH" --dest "$T/cc" --profiles "$T/profiles" --base "file://$T/fx" 2>"$T/err") && CODE=0 || CODE=$?
  check exit "$CODE" 1
  check msg "$(grep -c 'inside the repository' "$T/err")" 1
  check nopin "$(test -e "$T/cc/SOURCE.json" && echo yes || echo no)" no
  git worktree remove --force "$T/wt"
}
test_tmpdir_inside_newline_worktree_refused() {
  setup; local nl=$'\n'
  git worktree add -q --detach "$T/wt${nl}x" HEAD || { check worktree-add 1 0; return; }
  git worktree add -q --detach "$T/wt2" HEAD || { check worktree-add2 1 0; return; }
  mkdir "$T/wt${nl}x/tmp"
  OUT=$(TMPDIR="$T/wt${nl}x/tmp" bash "$FETCH" --dest "$T/cc" --profiles "$T/profiles" --base "file://$T/fx" 2>"$T/err") && CODE=0 || CODE=$?
  check exit "$CODE" 1
  check msg "$(grep -c 'inside the repository' "$T/err")" 1
  git worktree remove --force "$T/wt${nl}x"; git worktree remove --force "$T/wt2"
}
test_bad_usage() {
  setup; run --keep extra
  check exit "$CODE" 2
}

for f in test_first_run_writes_pin test_second_run_is_untouched test_one_page_changes_one_kind test_empty_page_keeps_pin \
  test_html_page_keeps_pin test_comment_or_mdx_first_is_accepted test_keep test_no_page_files_remain \
  test_tmpdir_inside_repo_refused test_failure_after_publish_restores_pin test_tmpdir_inside_other_worktree_refused test_tmpdir_inside_newline_worktree_refused test_bad_usage; do t $f; done
[ $FAILS = 0 ]
