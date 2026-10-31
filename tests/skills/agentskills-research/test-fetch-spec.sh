#!/bin/bash
# Tests for scripts/fetch-spec.sh; fixtures are served through file:// URLs.
HERE=$(cd "$(dirname "$0")" && pwd)
FETCH=$HERE/../../../skills/agentskills-research/scripts/fetch-spec.sh
A=$(printf 'a%.0s' {1..40})
B=$(printf 'b%.0s' {1..40})
C=$(printf 'c%.0s' {1..40})
HEADER='<!-- Source: https://github.com/agentskills/agentskills (CC-BY-4.0), verbatim copy, see SOURCE.json -->'
REAL_GIT=$(command -v git)
FAILS=0 TMPS=()
trap 'rm -rf "${TMPS[@]}"' EXIT

setup() { # sets T and CODE/OUT; mutates only $T
  T=$(mktemp -d); TMPS+=("$T"); mkdir "$T/fx"; cp -a "$HERE/fixtures/upstream" "$T/fx/$A"; ln -s "$A" "$T/fx/$B"
  export AGENTSKILLS_RAW_BASE=file://$T/fx
  unset AGENTSKILLS_SHA FETCH_SPEC_FAIL_AT
}
run() { # run SHA [extra env assignments via env]; stdout -> $OUT, exit -> $CODE
  local sha=$1; shift
  OUT=$(AGENTSKILLS_SHA=$sha "$@" bash "$FETCH" --dest "$T/dest" --rubric "$T/rubric.md" ${FETCH_ARGS:-} 2>"$T/err") && CODE=0 || CODE=$?
}
copy_sha() { cp -r "$T/fx/$A" "$T/fx/$1"; } # fresh upstream commit based on A
snap() { (cd "$T" && find dest -type f 2>/dev/null | sort | xargs -r sha256sum); }
j() { jq -c "$1" <<<"$OUT"; }
check() { # check DESC ACTUAL EXPECTED
  if [ "$2" != "$3" ]; then echo "  FAIL: $1: got [$2] want [$3]"; FAILS=$((FAILS + 1)); TESTFAIL=1; fi
}
t() {
  TESTFAIL=0; "$1"
  if [ $TESTFAIL = 0 ]; then echo "PASS $1"; else echo "FAIL $1"; fi
}
count_files() { find "$T/dest" -type f 2>/dev/null | wc -l; }

test_docs_json_tracked() {
  setup; run $A
  check exit "$CODE" 0
  check header "$(head -1 "$T/dest/docs-navigation.json.txt")" "# Source: https://github.com/agentskills/agentskills (CC-BY-4.0), verbatim copy, see SOURCE.json"
  check structure "$(j .structure_changed)" false
}
test_new_nav_page_reported() {
  setup; copy_sha $C
  jq '.navigation.pages += ["skill-creation/new-guide"]' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  run $C
  check exit "$CODE" 0
  check structure "$(j .structure_changed)" true
  check new_pages "$(j .new_pages)" '["skill-creation/new-guide"]'
}
test_removed_nav_page_reported_and_kept() {
  setup; run $A; local before; before=$(sha256sum < "$T/dest/using-scripts.md"); copy_sha $C
  jq '.navigation.pages |= map(if type == "object" then .pages |= map(select(. != "skill-creation/using-scripts")) else . end)' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  run $C
  check exit "$CODE" 0
  check removed "$(j .removed_pages)" '["skill-creation/using-scripts"]'
  check kept "$(sha256sum < "$T/dest/using-scripts.md")" "$before"
}
test_out_of_scope_nav_page_ignored() {
  setup; run $A; local before; before="$(j .new_pages)|$(j .removed_pages)"; copy_sha $C
  jq '.navigation.pages += ["client-implementation/new"]' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  run $C
  check exit "$CODE" 0
  check structure "$(j .structure_changed)" false
  check sets "$(j .new_pages)|$(j .removed_pages)" "$before"
}

test_removed_upstream_file_is_not_downloaded() {
  setup; run $A; local before; before=$(sha256sum < "$T/dest/using-scripts.md"); copy_sha $C
  jq '.navigation.pages |= map(if type == "object" then .pages |= map(select(. != "skill-creation/using-scripts")) else . end)' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  rm "$T/fx/$C/docs/skill-creation/using-scripts.mdx"
  run $C
  check exit "$CODE" 0
  check removed "$(j .removed_pages)" '["skill-creation/using-scripts"]'
  check kept "$(sha256sum < "$T/dest/using-scripts.md")" "$before"
}

test_empty_navigation_groups_are_supported() {
  setup; copy_sha $C
  jq '.navigation.pages += [{group:"empty",pages:[]},{group:"nested",pages:[{group:"deeper",pages:[]}]}]' \
    "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  run $C
  check exit "$CODE" 0
  check structure "$(j .structure_changed)" false
}

test_pages_dir_rejects_symlink_escape() {
  setup; copy_sha $C
  jq '.navigation.pages += ["skill-creation/new-guide"]' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  printf '# New guide\n' > "$T/fx/$C/docs/skill-creation/new-guide.mdx"
  mkdir -p "$T/pages/skill-creation" "$T/outside"
  printf 'sentinel\n' > "$T/outside/sentinel.txt"
  ln -s "$T/outside/sentinel.txt" "$T/pages/skill-creation/new-guide.mdx"
  FETCH_ARGS="--pages-dir $T/pages" run $C; unset FETCH_ARGS
  check exit "$CODE" 1
  check message "$(grep -c 'not a regular file' "$T/err" || true)" 1
  check sentinel "$(cat "$T/outside/sentinel.txt")" sentinel
  check still-link "$([ -L "$T/pages/skill-creation/new-guide.mdx" ] && echo yes || echo no)" yes
}
test_pages_json_symlink_is_rejected() {
  setup; copy_sha $C
  jq '.navigation.pages += ["skill-creation/new-guide"]' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  printf '# New guide\n' > "$T/fx/$C/docs/skill-creation/new-guide.mdx"
  mkdir -p "$T/pages" "$T/outside"
  printf 'sentinel\n' > "$T/outside/pages.txt"
  ln -s "$T/outside/pages.txt" "$T/pages/pages.json"
  FETCH_ARGS="--pages-dir $T/pages" run $C; unset FETCH_ARGS
  check exit "$CODE" 1
  check sentinel "$(cat "$T/outside/pages.txt")" sentinel
}

test_malformed_navigation_path_is_rejected() {
  setup; copy_sha $C
  jq '.navigation.pages += ["skill-creation/../../escape"]' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  run $C
  check exit "$CODE" 1
  check message "$(grep -c 'invalid navigation page path' "$T/err")" 1
  check no_escape "$( [ ! -e "$T/fx/escape.mdx" ] && echo yes)" yes
}

test_mapping_is_derived_from_source_map() {
  setup; run $A; copy_sha $C
  jq '.navigation.pages |= map(if type == "object" then .pages |= map(select(. != "skill-creation/using-scripts")) else . end)' \
    "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  run $C
  check removed_page "$(j .removed_pages)" '["skill-creation/using-scripts"]'
  cp "$FETCH" "$T/fetch-spec.sh"
  sed -i '/using-scripts.md|docs\/skill-creation\/using-scripts.mdx/d' "$T/fetch-spec.sh"
  local old_fetch=$FETCH
  FETCH=$T/fetch-spec.sh
  run $C
  check removed_after_unmap "$(j .removed_pages)" '[]'
  check new_after_unmap "$(j .new_pages)" '[]'
  # With the map entry absent, putting the page back in navigation makes it new.
  jq '.navigation.pages |= map(if type == "object" then .pages += ["skill-creation/using-scripts"] else . end)' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  run $C
  check new_without_mapping "$(j .new_pages)" '["skill-creation/using-scripts"]'
  sed -i '/^FILES=(/a\  "using-scripts.md|docs/skill-creation/using-scripts.mdx"' "$T/fetch-spec.sh"
  run $C
  check no_longer_new "$(j .new_pages)" '[]'
  check no_longer_removed "$(j .removed_pages)" '[]'
  FETCH=$old_fetch
}
test_bad_docs_json_exits_1() {
  setup; run $A; local before; before=$(snap); copy_sha $C
  printf '{invalid' > "$T/fx/$C/docs/docs.json"
  run $C
  check exit "$CODE" 1
  check unchanged "$(snap)" "$before"
}
test_pages_dir_downloads_new_page() {
  setup; copy_sha $C
  jq '.navigation.pages += ["skill-creation/new-guide"]' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  mkdir -p "$T/fx/$C/docs/skill-creation"
  printf 'new page body\n' > "$T/fx/$C/docs/skill-creation/new-guide.mdx"
  local pages="$T/pages"; FETCH_ARGS="--pages-dir $pages" run $C; unset FETCH_ARGS
  check exit "$CODE" 0
  check byte_copy "$(cmp -s "$pages/skill-creation/new-guide.mdx" "$T/fx/$C/docs/skill-creation/new-guide.mdx" && echo yes)" yes
  check page_map "$(jq -c '[.[]|select(.page=="skill-creation/new-guide")|.mapped]' "$pages/pages.json")" '[false]'
  check mapped_count "$(jq '[.[]|select(.mapped)]|length' "$pages/pages.json")" 6
  check no_reference "$( [ ! -e "$T/dest/new-guide.md" ] && echo yes)" yes
}
test_pages_dir_skips_removed_page() {
  setup; run $A; copy_sha $C
  jq '.navigation.pages |= map(if type == "object" then .pages |= map(select(. != "skill-creation/using-scripts")) else . end)' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  local pages="$T/pages"; FETCH_ARGS="--pages-dir $pages" run $C; unset FETCH_ARGS
  check absent "$( [ ! -e "$pages/skill-creation/using-scripts.mdx" ] && echo yes)" yes
  check absent_map "$(jq -e 'all(.[]; .page != "skill-creation/using-scripts")' "$pages/pages.json" >/dev/null && echo yes)" yes
}
test_pages_dir_reuses_regular_targets_on_next_run() {
  setup; copy_sha $C
  local pages="$T/pages"
  FETCH_ARGS="--pages-dir $pages" run $C; unset FETCH_ARGS
  check first_exit "$CODE" 0
  # Change a mapped document's actual source file.
  printf 'changed upstream content\n' > "$T/fx/$C/docs/skill-creation/using-scripts.mdx"
  FETCH_ARGS="--pages-dir $pages" run $C; unset FETCH_ARGS
  check second_exit "$CODE" 0
  check updated "$(cat "$pages/skill-creation/using-scripts.mdx")" "changed upstream content"
}
test_pages_dir_rejects_escaping_ancestor_before_mkdir() {
  setup; copy_sha $C
  jq '.navigation.pages += ["skill-creation/new-guide"]' "$T/fx/$C/docs/docs.json" > "$T/docs.json"
  mv "$T/docs.json" "$T/fx/$C/docs/docs.json"
  local pages="$T/pages"; mkdir "$T/outside"; ln -s "$T/outside" "$pages"
  FETCH_ARGS="--pages-dir $pages" run $C; unset FETCH_ARGS
  check exit "$CODE" 1
  check no_outside_directory "$( [ ! -e "$T/outside/skill-creation" ] && echo yes)" yes
}
test_first_run_all_changed() {
  setup; run $A
  check exit "$CODE" 0
  check changed_len "$(j '.changed|length')" 8
  check files "$(count_files)" 9
  check sha "$(j .sha)" "\"$A\""
  check stale "$(j .rubric_stale)" true
  check header "$(head -1 "$T/dest/best-practices.md")" "$HEADER"
  check txt_header "$(head -1 "$T/dest/skills-ref-validator.py.txt" | cut -c1-9)" "# Source:"
  check blank "$(sed -n 2p "$T/dest/best-practices.md")" ""
}
test_second_run_unchanged() {
  setup; run $A; local before; before=$(snap)
  run $B
  check exit "$CODE" 0
  check changed "$(j .changed)" '[]'
  check same "$(snap)" "$before"
  check sha "$(j .sha)" "\"$A\""
  check resolved "$(j .resolved)" "\"$B\""
  check stale "$(j .rubric_stale)" true
  check unchanged_len "$(j '.unchanged|length')" 8
}
test_one_file_changed() {
  setup; run $A; copy_sha $C
  echo extra >> "$T/fx/$C/docs/skill-creation/best-practices.mdx"
  run $C
  check changed "$(j .changed)" '["best-practices.md"]'
  check pin "$(jq -r .sha "$T/dest/SOURCE.json")" "$C"
}
test_validator_only_change_advances_pin() {
  setup; run $A; local docs; docs=$(cd "$T/dest" && sha256sum *.md); copy_sha $C
  echo '# extra' >> "$T/fx/$C/skills-ref/src/skills_ref/validator.py"
  run $C
  check changed "$(j .changed)" '["skills-ref-validator.py.txt"]'
  check pin "$(jq -r .sha "$T/dest/SOURCE.json")" "$C"
  check docs "$(cd "$T/dest" && sha256sum *.md)" "$docs"
}
test_missing_source_keeps_dest() {
  setup; run $A; local before; before=$(snap); copy_sha $C
  rm "$T/fx/$C/docs/skill-creation/quickstart.mdx"
  run $C
  check exit "$CODE" 1
  check same "$(snap)" "$before"
}
test_publish_failure_rolls_back() {
  setup; run $A; local before; before=$(snap); copy_sha $C
  echo extra >> "$T/fx/$C/docs/specification.mdx"
  run $C env FETCH_SPEC_FAIL_AT=metadata
  check exit "$CODE" 1
  check same "$(snap)" "$before"
}
test_backup_failure_leaves_dest_untouched() {
  setup; run $A; local before; before=$(snap); copy_sha $C
  echo extra >> "$T/fx/$C/docs/specification.mdx"
  echo extra >> "$T/fx/$C/docs/skill-creation/quickstart.mdx"
  run $C env FETCH_SPEC_FAIL_AT=backup
  check exit "$CODE" 1
  check same "$(snap)" "$before"
  check message "$(grep -c 'backup failed, references untouched' "$T/err")" 1
  check no_restore_claim "$(grep -c 'restored' "$T/err")" 0
}
test_term_during_publish_restores() {
  setup; run $A; local before; before=$(snap); copy_sha $C
  echo extra >> "$T/fx/$C/docs/specification.mdx"
  echo extra >> "$T/fx/$C/docs/skill-creation/quickstart.mdx"
  run $C env FETCH_SPEC_FAIL_AT=term
  check exit "$CODE" 1
  check same "$(snap)" "$before"
}
test_failed_restore_keeps_backups() {
  setup; run $A; local before; before=$(snap); copy_sha $C
  echo extra >> "$T/fx/$C/docs/specification.mdx"
  mkdir "$T/bin" # cp fails only when restoring from a backup
  printf '#!/bin/bash\ncase "$*" in */backup/*" '"$T"'/dest/"*) exit 1 ;; esac\nexec %s "$@"\n' "$(command -v cp)" > "$T/bin/cp"
  chmod +x "$T/bin/cp"
  run $C env PATH="$T/bin:$PATH" FETCH_SPEC_FAIL_AT=metadata
  check exit "$CODE" 1
  local kept; kept=$(sed -n 's/.*recovery failed.* kept in \([^ ]*\)$/\1/p' "$T/err")
  [ -n "$kept" ] && TMPS+=("${kept%/backup}")
  check kept_dir "$([ -n "$kept" ] && [ -f "$kept/SOURCE.json" ] && [ -f "$kept/specification.md" ] && echo yes)" yes
}
test_corrupt_source_json_exits_1() {
  setup; run $A
  echo '{bad' > "$T/dest/SOURCE.json"; local before; before=$(snap)
  run $B
  check exit "$CODE" 1
  check same "$(snap)" "$before"
  echo '"str"' > "$T/dest/SOURCE.json"
  run $B
  check exit_str "$CODE" 1
}
test_interrupted_refresh_reports_stale_rubric() {
  setup; run $A
  echo "spec_sha: 0000" > "$T/rubric.md"
  run $B
  check changed "$(j .changed)" '[]'
  check stale "$(j .rubric_stale)" true
  echo "spec_sha: $A" > "$T/rubric.md"
  run $B
  check stale2 "$(j .rubric_stale)" false
}
test_http_error_exits_1() {
  setup; run $A; local before; before=$(snap); copy_sha $C
  mkdir "$T/bin"
  printf '#!/bin/bash\necho 404 >&2\nexit 22\n' > "$T/bin/curl"; chmod +x "$T/bin/curl"
  run $C env PATH="$T/bin:$PATH"
  check exit "$CODE" 1
  check same "$(snap)" "$before"
}
test_empty_ls_remote_exits_1() {
  setup; mkdir "$T/bin"
  printf '#!/bin/bash\n[ "$1" = ls-remote ] && exit 0\nexec %s "$@"\n' "$REAL_GIT" > "$T/bin/git"; chmod +x "$T/bin/git"
  OUT=$(PATH="$T/bin:$PATH" bash "$FETCH" --dest "$T/dest" --rubric "$T/rubric.md" 2>/dev/null) && CODE=0 || CODE=$?
  check exit_empty "$CODE" 1
  check nothing_empty "$(count_files)" 0
  printf '#!/bin/bash\n[ "$1" = ls-remote ] && { printf "nothex\\trefs/heads/main\\n"; exit 0; }\nexec %s "$@"\n' "$REAL_GIT" > "$T/bin/git"
  OUT=$(PATH="$T/bin:$PATH" bash "$FETCH" --dest "$T/dest" --rubric "$T/rubric.md" 2>/dev/null) && CODE=0 || CODE=$?
  check exit_nothex "$CODE" 1
  check nothing_nothex "$(count_files)" 0
}
test_ls_remote_failure_exits_1() {
  setup; mkdir "$T/bin"
  printf '#!/bin/bash\n[ "$1" = ls-remote ] && exit 128\nexec %s "$@"\n' "$REAL_GIT" > "$T/bin/git"; chmod +x "$T/bin/git"
  OUT=$(PATH="$T/bin:$PATH" bash "$FETCH" --dest "$T/dest" --rubric "$T/rubric.md" 2>/dev/null) && CODE=0 || CODE=$?
  check exit "$CODE" 1
  check nothing "$(count_files)" 0
}
test_short_sha_rejected() {
  setup; run deadbeef
  check exit "$CODE" 1
  check nothing "$(count_files)" 0
}
test_deleted_dest_file_is_repaired() {
  setup; run $A; local h; h=$(sha256sum < "$T/dest/quickstart.md")
  rm "$T/dest/quickstart.md"
  run $B
  check exit "$CODE" 0
  check changed "$(j .changed)" '["quickstart.md"]'
  check hash "$(sha256sum < "$T/dest/quickstart.md")" "$h"
}
test_edited_dest_file_is_repaired() {
  setup; run $A
  echo local edit >> "$T/dest/specification.md"
  run $B
  check changed "$(j .changed)" '["specification.md"]'
  check hash "$(sha256sum < "$T/dest/specification.md" | cut -d' ' -f1)" "$(jq -r '.files["specification.md"]' "$T/dest/SOURCE.json")"
}

test_help_prints_usage_and_exits_0() {
  setup
  OUT=$(bash "$FETCH" --help 2>"$T/err") && CODE=0 || CODE=$?
  check exit "$CODE" 0
  check no_stderr "$(wc -c < "$T/err" | tr -d ' ')" 0
  for w in AGENTSKILLS_SHA AGENTSKILLS_RAW_BASE rubric_stale resolved unchanged --dest --ref --rubric 'bash 4' sha256sum; do
    check "mentions $w" "$(grep -c -- "$w" <<<"$OUT" | sed 's/^[1-9].*/ok/')" ok
  done
  OUT=$(bash "$FETCH" -h 2>/dev/null) && CODE=0 || CODE=$?
  check exit_h "$CODE" 0
  OUT=$(bash "$FETCH" --bogus 2>/dev/null) && CODE=0 || CODE=$?
  check exit_bogus "$CODE" 1
}
test_post_publish_jq_failure_exits_1() {
  setup; run $A; mkdir "$T/bin"
  printf '#!/bin/bash\n[ "$1" = -R ] && [ "$2" = select\(length\>0\) ] && exit 5\nexec %s "$@"\n' "$(command -v jq)" > "$T/bin/jq"; chmod +x "$T/bin/jq"
  run $B env PATH="$T/bin:$PATH"
  check exit "$CODE" 1
  check stdout_empty "$OUT" ""
}

test_default_dest_requires_repo_root() {
  setup; mkdir "$T/elsewhere"
  OUT=$(cd "$T/elsewhere" && AGENTSKILLS_SHA=$A bash "$FETCH" 2>"$T/err") && CODE=0 || CODE=$?
  check exit "$CODE" 1
  check stdout_empty "$OUT" ""
  check mentions_root "$(grep -c 'repo root' "$T/err" | sed 's/^[1-9].*/ok/')" ok
  check no_tree "$(find "$T/elsewhere" | wc -l | tr -d ' ')" 1
  OUT=$(cd "$T/elsewhere" && bash "$FETCH" -h 2>/dev/null) && CODE=0 || CODE=$?
  check help_exit "$CODE" 0
}

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
