#!/bin/bash
# Tests for skills/pr-diagrams/scripts/pr-diagrams.sh.
# Origin is a local bare repo. GH and DRAWIO_CONVERTER are stubs.
HERE=$(cd "$(dirname "$0")" && pwd)
SCRIPT=$HERE/../../../skills/pr-diagrams/scripts/pr-diagrams.sh
FIXTURE=$HERE/fixtures/flow.drawio
REAL_GIT=$(command -v git)
FAILS=0 TMPS=()
trap 'rm -rf "${TMPS[@]}"' EXIT

check() { # check DESC ACTUAL EXPECTED
  if [ "$2" != "$3" ]; then echo "  FAIL: $1: got [$2] want [$3]"; FAILS=$((FAILS + 1)); TESTFAIL=1; fi
}
t() {
  TESTFAIL=0; "$1"
  if [ $TESTFAIL = 0 ]; then echo "PASS $1"; else echo "FAIL $1"; fi
}

# Bare origin plus a work clone. Sets REPO (work tree), BARE, SHA_A, SHA_B, SHA_C.
init_repo() {
  local root
  root=$(mktemp -d); TMPS+=("$root")
  BARE=$root/origin.git
  REPO=$root/work
  "$REAL_GIT" init --bare -q "$BARE"
  "$REAL_GIT" init -q -b main "$REPO"
  "$REAL_GIT" -C "$REPO" config user.email t@example.com
  "$REAL_GIT" -C "$REPO" config user.name t
  "$REAL_GIT" -C "$REPO" remote add origin "$BARE"
  printf 'a\n' > "$REPO/f.txt"
  "$REAL_GIT" -C "$REPO" add f.txt
  "$REAL_GIT" -C "$REPO" commit -q -m base
  "$REAL_GIT" -C "$REPO" push -q origin main
  "$REAL_GIT" -C "$REPO" checkout -q -b feature
  printf 'b\n' > "$REPO/f.txt"
  "$REAL_GIT" -C "$REPO" commit -q -am one
  SHA_A=$("$REAL_GIT" -C "$REPO" rev-parse HEAD)
  printf 'c\n' > "$REPO/f.txt"
  "$REAL_GIT" -C "$REPO" commit -q -am two
  SHA_B=$("$REAL_GIT" -C "$REPO" rev-parse HEAD)
  printf 'd\n' > "$REPO/f.txt"
  "$REAL_GIT" -C "$REPO" commit -q -am three
  SHA_C=$("$REAL_GIT" -C "$REPO" rev-parse HEAD)
  "$REAL_GIT" -C "$REPO" push -q origin feature
  STUB=$(mktemp -d); TMPS+=("$STUB")
}

# Stub gh: logs every invocation, serves scripted JSON per endpoint, and on an
# HTTP error writes the body to stdout and "gh: <message> (HTTP NNN)" to stderr.
# Failure is env-only (GH_STUB_FAIL_CODE/MSG/BODY) so the shipping script never
# grows test flags that real gh would reject.
write_gh_stub() {
  local root=$1
  mkdir -p "$root/bin" "$root/fixtures"
  cat > "$root/bin/gh" << 'EOF'
#!/bin/bash
printf '%s\n' "$*" >> "$GH_LOG"
code=${GH_STUB_FAIL_CODE:-} msg=${GH_STUB_FAIL_MSG:-} body=${GH_STUB_FAIL_BODY:-}
if [ -n "$code" ]; then
  printf '%s\n' "$body"
  printf 'gh: %s (HTTP %s)\n' "$msg" "$code" >&2
  exit 1
fi
endpoint=""
for a in "$@"; do
  case "$a" in
    repos/*) endpoint=$a ;;
  esac
done
file=${GH_FIXTURES}/${endpoint//\//__}
if [ -f "$file" ]; then cat "$file"; exit 0; fi
echo "stub: no fixture for $endpoint" >&2
exit 1
EOF
  chmod +x "$root/bin/gh"
}

# Converter stub: status lines on stdout, writes a PNG, git-adds it in CWD.
write_converter_stub() {
  local path=$1 mode=${2:-png}
  cat > "$path" << EOF
#!/bin/bash
echo "Converting inputs..."
mode=$mode
generated=()
for src in "\$@"; do
  case "\$src" in
    *.drawio) out="\${src%.drawio}.drawio.png" ;;
    *) continue ;;
  esac
  case "\$mode" in
    png) printf '\211PNG\r\n\032\nembedded' > "\$out"; echo "Generated \$out"; generated+=("\$out") ;;
    none) echo "no output for \$src" ;;
    bad) printf 'not a png' > "\$out"; echo "Generated \$out"; generated+=("\$out") ;;
  esac
done
if [ \${#generated[@]} -gt 0 ]; then git add -- "\${generated[@]}"; fi
exit 0
EOF
  chmod +x "$path"
}

run_in() { # run_in DIR [env...] -- args; sets OUT CODE ERR
  local dir=$1; shift
  local envargs=()
  while [ $# -gt 0 ] && [ "$1" != -- ]; do envargs+=("$1"); shift; done
  shift
  OUT=$(cd "$dir" && env "${envargs[@]}" bash "$SCRIPT" "$@" 2>"$dir/err") && CODE=0 || CODE=$?
  ERR=$(cat "$dir/err" 2>/dev/null || true)
}

gh_env() { # GH stub dir already has bin/gh and fixtures/
  printf 'GH=%s/bin/gh GH_LOG=%s/gh.log GH_FIXTURES=%s/fixtures PR_DIAGRAMS_REPO=acme/widgets' "$1" "$1" "$1"
}

test_repo_from_origin() {
  local root; root=$(mktemp -d); TMPS+=("$root")
  "$REAL_GIT" init -q "$root"
  for url in \
    'https://github.com/acme/widgets' \
    'https://github.com/acme/widgets.git' \
    'git@github.com:acme/widgets.git' \
    'ssh://git@github.com/acme/widgets.git' \
    'ssh://git@github.com/acme/widgets'; do
    "$REAL_GIT" -C "$root" remote remove origin 2>/dev/null || true
    "$REAL_GIT" -C "$root" remote add origin "$url"
    run_in "$root" -- repo
    check "parse $url" "$CODE:$OUT" "0:acme/widgets"
  done
  "$REAL_GIT" -C "$root" remote remove origin
  "$REAL_GIT" -C "$root" remote add origin 'https://gitlab.com/acme/widgets.git'
  run_in "$root" -- repo
  check exit "$CODE" 1
  check names_url "$(grep -c 'https://gitlab.com/acme/widgets.git' "$root/err")" 1
  check no_stdout "$OUT" ""
}

test_repo_override_ignored_without_gh_stub() {
  local root; root=$(mktemp -d); TMPS+=("$root")
  "$REAL_GIT" init -q "$root"
  "$REAL_GIT" -C "$root" remote add origin 'https://github.com/real/origin.git'
  run_in "$root" PR_DIAGRAMS_REPO=acme/widgets -- repo
  check unset "$CODE:$OUT" "0:real/origin"
  check note "$(grep -c 'PR_DIAGRAMS_REPO' "$root/err")" 1
  run_in "$root" PR_DIAGRAMS_REPO=acme/widgets GH=gh -- repo
  check gh_literal "$CODE:$OUT" "0:real/origin"
  local stub=$root/stub
  write_gh_stub "$stub"
  run_in "$root" PR_DIAGRAMS_REPO=acme/widgets GH="$stub/gh" -- repo
  check stub "$CODE:$OUT" "0:acme/widgets"
}

test_related_dedupes_prs() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; mkdir -p "$s/fixtures"
  local pr='{"number":7,"title":"Add widgets","merged_at":"2026-01-02T00:00:00Z","head":{"ref":"feature"},"base":{"ref":"main"}}'
  printf '%s\n' "$pr" > "$s/fixtures/repos__acme__widgets__commits__${SHA_A}__pulls"
  printf '%s\n' "$pr" > "$s/fixtures/repos__acme__widgets__commits__${SHA_B}__pulls"
  printf '%s\n' "$pr" > "$s/fixtures/repos__acme__widgets__commits__${SHA_C}__pulls"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- related main feature
  check exit "$CODE" 0
  check count "$(jq 'length' <<<"$OUT")" 1
  check pr "$(jq -r '.[0].pr' <<<"$OUT")" 7
}

test_related_reports_head_and_base_ref() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; mkdir -p "$s/fixtures"
  printf '%s\n' '{"number":7,"title":"Add widgets","merged_at":"2026-01-02T00:00:00Z","head":{"ref":"feature"},"base":{"ref":"develop"}}' \
    > "$s/fixtures/repos__acme__widgets__commits__${SHA_A}__pulls"
  printf '\n' > "$s/fixtures/repos__acme__widgets__commits__${SHA_B}__pulls"
  printf '\n' > "$s/fixtures/repos__acme__widgets__commits__${SHA_C}__pulls"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- related main feature
  check exit "$CODE" 0
  check head "$(jq -r '.[0].head_ref' <<<"$OUT")" feature
  check base "$(jq -r '.[0].base_ref' <<<"$OUT")" develop
  check title "$(jq -r '.[0].title' <<<"$OUT")" "Add widgets"
  check merged "$(jq -r '.[0].merged_at' <<<"$OUT")" "2026-01-02T00:00:00Z"
}

test_related_excludes_open_and_current_pr() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; mkdir -p "$s/fixtures"
  printf '%s\n%s\n' \
    '{"number":9,"title":"Open","merged_at":null,"head":{"ref":"feature"},"base":{"ref":"main"}}' \
    '{"number":8,"title":"Current","merged_at":"2026-01-03T00:00:00Z","head":{"ref":"feature"},"base":{"ref":"main"}}' \
    > "$s/fixtures/repos__acme__widgets__commits__${SHA_A}__pulls"
  printf '%s\n' '{"number":7,"title":"Kept","merged_at":"2026-01-01T00:00:00Z","head":{"ref":"topic"},"base":{"ref":"main"}}' \
    > "$s/fixtures/repos__acme__widgets__commits__${SHA_B}__pulls"
  printf '\n' > "$s/fixtures/repos__acme__widgets__commits__${SHA_C}__pulls"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- related main feature --exclude-pr 8
  check exit "$CODE" 0
  check prs "$(jq -c '[.[].pr]' <<<"$OUT")" '[7]'
}

test_related_paginates() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; mkdir -p "$s/fixtures"
  printf '%s\n%s\n' \
    '{"number":1,"title":"Page one","merged_at":"2026-01-01T00:00:00Z","head":{"ref":"a"},"base":{"ref":"main"}}' \
    '{"number":2,"title":"Page two","merged_at":"2026-01-02T00:00:00Z","head":{"ref":"b"},"base":{"ref":"main"}}' \
    > "$s/fixtures/repos__acme__widgets__commits__${SHA_A}__pulls"
  printf '\n' > "$s/fixtures/repos__acme__widgets__commits__${SHA_B}__pulls"
  printf '\n' > "$s/fixtures/repos__acme__widgets__commits__${SHA_C}__pulls"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- related main feature
  check exit "$CODE" 0
  check page2 "$(jq -c '[.[].pr] | sort' <<<"$OUT")" '[1,2]'
  check paginate "$(grep -c -- '--paginate' "$s/gh.log")" 3
  check jqflag "$(grep -F -c -- '--jq .[]' "$s/gh.log")" 3
}

test_related_rate_limited() {
  init_repo
  local s=$STUB; write_gh_stub "$s"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") GH_STUB_FAIL_CODE=429 GH_STUB_FAIL_MSG='rate limit' GH_STUB_FAIL_BODY='{"message":"rate"}' -- related main feature
  check exit429 "$CODE" 1
  check stderr429 "$(grep -c 'rate limited' "$REPO/err")" 1
  check names429 "$(grep -c "$SHA_A" "$REPO/err")" 1
  check stdout429 "$OUT" ""
  : > "$s/gh.log"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") GH_STUB_FAIL_CODE=403 GH_STUB_FAIL_MSG='forbidden' GH_STUB_FAIL_BODY='{"message":"nope"}' -- related main feature
  check exit403 "$CODE" 1
  check stderr403 "$(grep -c 'rate limited' "$REPO/err")" 1
  check stdout403 "$OUT" ""
}

test_related_other_failure_names_commit() {
  init_repo
  local s=$STUB; write_gh_stub "$s"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") GH_STUB_FAIL_CODE=500 GH_STUB_FAIL_MSG='boom' GH_STUB_FAIL_BODY='{"message":"boom"}' -- related main feature
  check exit "$CODE" 1
  check names "$(grep -c "$SHA_A" "$REPO/err")" 1
  check no_rate "$(grep -c 'rate limited' "$REPO/err")" 0
  check stdout "$OUT" ""
}

test_related_fetch_failure() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; : > "$s/gh.log"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- related main missing-head
  check exit "$CODE" 1
  check git_stderr "$(grep -c "couldn't find remote ref" "$REPO/err")" 1
  check stdout "$OUT" ""
  check no_gh "$(wc -l < "$s/gh.log" | tr -d ' ')" 0
}

test_related_orders_by_merged_at() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; mkdir -p "$s/fixtures"
  printf '%s\n' '{"number":3,"title":"Old","merged_at":"2026-01-01T00:00:00Z","head":{"ref":"a"},"base":{"ref":"main"}}' \
    > "$s/fixtures/repos__acme__widgets__commits__${SHA_A}__pulls"
  printf '%s\n%s\n' \
    '{"number":4,"title":"Tie low","merged_at":"2026-02-01T00:00:00Z","head":{"ref":"b"},"base":{"ref":"main"}}' \
    '{"number":9,"title":"Tie high","merged_at":"2026-02-01T00:00:00Z","head":{"ref":"c"},"base":{"ref":"main"}}' \
    > "$s/fixtures/repos__acme__widgets__commits__${SHA_B}__pulls"
  printf '%s\n' '{"number":5,"title":"Newest","merged_at":"2026-03-01T00:00:00Z","head":{"ref":"d"},"base":{"ref":"main"}}' \
    > "$s/fixtures/repos__acme__widgets__commits__${SHA_C}__pulls"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- related main feature
  check exit "$CODE" 0
  check order "$(jq -c '[.[].pr]' <<<"$OUT")" '[5,9,4,3]'
}

test_related_empty_when_no_prs() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; mkdir -p "$s/fixtures"
  for sha in "$SHA_A" "$SHA_B" "$SHA_C"; do
    printf '\n' > "$s/fixtures/repos__acme__widgets__commits__${sha}__pulls"
  done
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- related main feature
  check exit "$CODE" 0
  check empty "$OUT" '[]'
}

review_fixtures() {
  local s=$1
  mkdir -p "$s/fixtures"
  printf '%s\n%s\n' \
    '{"user":{"login":"Alice","type":"User"}}' \
    '{"user":{"login":"bob","type":"User"}}' \
    > "$s/fixtures/repos__acme__widgets__pulls__10__reviews"
  printf '%s\n%s\n' '{"login":"carol","type":"User"}' '{"login":"alice","type":"User"}' \
    > "$s/fixtures/repos__acme__widgets__pulls__10__requested_reviewers"
  printf '%s\n' '{"user":{"login":"BOB","type":"User"}}' \
    > "$s/fixtures/repos__acme__widgets__pulls__11__reviews"
  printf '%s\n' '{"login":"dave","type":"User"}' \
    > "$s/fixtures/repos__acme__widgets__pulls__11__requested_reviewers"
}

test_reviewers_union_dedupes() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; review_fixtures "$s"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- reviewers 10 11
  check exit "$CODE" 0
  check logins "$(jq -c '.' <<<"$OUT")" '["Alice","bob","carol","dave"]'
  check pages "$(grep -c 'pulls/10/reviews' "$s/gh.log")" 1
  check paginate "$(grep 'pulls/10/reviews' "$s/gh.log" | grep -c -- '--paginate')" 1
  check req "$(grep -c 'pulls/10/requested_reviewers' "$s/gh.log")" 1
}

test_reviewers_exclude_is_case_insensitive() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; review_fixtures "$s"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- reviewers 10 11 --exclude Alice
  check exit "$CODE" 0
  check logins "$(jq -c '.' <<<"$OUT")" '["bob","carol","dave"]'
}

test_reviewers_keeps_only_users_and_excludes_given_login() {
  init_repo
  local s=$STUB; write_gh_stub "$s"; mkdir -p "$s/fixtures"
  printf '%s\n%s\n%s\n' \
    '{"user":{"login":"copilot-pull-request-reviewer","type":"Bot"}}' \
    '{"user":null}' \
    '{"user":{"login":"alice","type":"User"}}' \
    > "$s/fixtures/repos__acme__widgets__pulls__12__reviews"
  printf '%s\n%s\n' '{"login":"dependabot","type":"Bot"}' '{"login":"erin","type":"User"}' \
    > "$s/fixtures/repos__acme__widgets__pulls__12__requested_reviewers"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- reviewers 12 --exclude erin
  check exit "$CODE" 0
  check kept "$(jq -c '.' <<<"$OUT")" '["alice"]'
  : > "$s/gh.log"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") -- reviewers 99
  check fail_exit "$CODE" 1
  check names_pr "$(grep -c 'PR 99' "$REPO/err")" 1
  check stdout "$OUT" ""
}

limited_path() { # symlinks for the tools the script needs, no drawio
  local bin=$1
  mkdir -p "$bin"
  local tool
  for tool in bash git jq mktemp cp mkdir cat printf; do
    ln -s "$(command -v "$tool")" "$bin/$tool"
  done
  # bash builtins cover printf; git/jq/cp come from PATH of the test runner
  ln -sf "$(command -v git)" "$bin/git"
  ln -sf "$(command -v jq)" "$bin/jq"
  ln -sf "$(command -v cp)" "$bin/cp"
  ln -sf "$(command -v mkdir)" "$bin/mkdir"
  ln -sf "$(command -v cat)" "$bin/cat"
  ln -sf "$(command -v mktemp)" "$bin/mktemp"
  ln -sf "$(command -v rm)" "$bin/rm"
  ln -sf "$(command -v chmod)" "$bin/chmod"
  ln -sf "$(command -v touch)" "$bin/touch"
}

test_render_reports_missing_cli() {
  local root; root=$(mktemp -d); TMPS+=("$root")
  limited_path "$root/bin"
  cp "$FIXTURE" "$root/flow.drawio"
  OUT=$(cd "$root" && PATH="$root/bin" bash "$SCRIPT" render "$root/flow.drawio" 2>"$root/err") && CODE=0 || CODE=$?
  check exit "$CODE" 1
  check msg "$(grep -c 'drawio CLI not found' "$root/err")" 1
  check nothing "$([ -e "$root/flow.drawio.png" ] && echo yes || echo no)" no
  check stdout "$OUT" ""
}

test_render_rejects_duplicate_basenames() {
  local root; root=$(mktemp -d); TMPS+=("$root")
  mkdir -p "$root/a" "$root/b"
  cp "$FIXTURE" "$root/a/flow.drawio"
  cp "$FIXTURE" "$root/b/flow.drawio"
  write_converter_stub "$root/conv.sh"
  run_in "$root" DRAWIO_CONVERTER="$root/conv.sh" -- render "$root/a/flow.drawio" "$root/b/flow.drawio"
  check exit "$CODE" 1
  check names_a "$(grep -c "$root/a/flow.drawio" "$root/err")" 1
  check names_b "$(grep -c "$root/b/flow.drawio" "$root/err")" 1
  check never "$(grep -c Converting "$root/err")" 0
  check nothing "$([ -e "$root/a/flow.drawio.png" ] || [ -e "$root/b/flow.drawio.png" ] && echo yes || echo no)" no
}

test_render_returns_png_next_to_source() {
  local root; root=$(mktemp -d); TMPS+=("$root")
  cp "$FIXTURE" "$root/flow.drawio"
  write_converter_stub "$root/conv.sh"
  run_in "$root" DRAWIO_CONVERTER="$root/conv.sh" -- render "$root/flow.drawio"
  check exit "$CODE" 0
  check json "$(jq -c '.' <<<"$OUT")" "[{\"drawio\":\"$root/flow.drawio\",\"png\":\"$root/flow.drawio.png\"}]"
  check status_not_stdout "$(grep -c Converting <<<"$OUT")" 0
  check png "$([ -s "$root/flow.drawio.png" ] && echo yes || echo no)" yes
}

test_render_rejects_missing_or_invalid_png() {
  local root; root=$(mktemp -d); TMPS+=("$root")
  cp "$FIXTURE" "$root/flow.drawio"
  write_converter_stub "$root/conv.sh" none
  run_in "$root" DRAWIO_CONVERTER="$root/conv.sh" -- render "$root/flow.drawio"
  check exit_none "$CODE" 1
  check names "$(grep -c 'no valid PNG' "$root/err" || true)" 1
  check nothing_none "$([ -e "$root/flow.drawio.png" ] && echo yes || echo no)" no
  check stdout_none "$OUT" ""
  write_converter_stub "$root/conv.sh" bad
  run_in "$root" DRAWIO_CONVERTER="$root/conv.sh" -- render "$root/flow.drawio"
  check exit_bad "$CODE" 1
  check nothing_bad "$([ -e "$root/flow.drawio.png" ] && echo yes || echo no)" no
  check stdout_bad "$OUT" ""
}

test_render_leaves_caller_index_untouched() {
  init_repo
  cp "$FIXTURE" "$REPO/flow.drawio"
  write_converter_stub "$REPO/conv.sh"
  "$REAL_GIT" -C "$REPO" add f.txt
  # shellcheck disable=SC2046
  run_in "$REPO" DRAWIO_CONVERTER="$REPO/conv.sh" -- render "$REPO/flow.drawio"
  check exit "$CODE" 0
  check clean "$("$REAL_GIT" -C "$REPO" diff --cached --quiet && echo yes || echo no)" yes
  "$REAL_GIT" -C "$REPO" add f.txt
  write_converter_stub "$REPO/conv.sh" none
  # shellcheck disable=SC2046
  run_in "$REPO" DRAWIO_CONVERTER="$REPO/conv.sh" -- render "$REPO/flow.drawio"
  check exit_fail "$CODE" 1
  check clean_fail "$("$REAL_GIT" -C "$REPO" diff --cached --quiet && echo yes || echo no)" yes
}

test_render_embeds_diagram_in_real_png() {
  if ! command -v drawio >/dev/null 2>&1; then
    echo "  SKIP drawio CLI not on PATH"
    return 0
  fi
  local root; root=$(mktemp -d); TMPS+=("$root")
  cp "$FIXTURE" "$root/flow.drawio"
  run_in "$root" -- render "$root/flow.drawio"
  check exit "$CODE" 0
  check marker "$(grep -a -c zTXtmxGraphModel "$root/flow.drawio.png" || true)" 1
}

test_stdout_clean_on_http_errors() {
  init_repo
  local s=$STUB; write_gh_stub "$s"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") GH_STUB_FAIL_CODE=429 GH_STUB_FAIL_MSG='rate limit' GH_STUB_FAIL_BODY='{"message":"API rate limit exceeded"}' -- related main feature
  check related_exit "$CODE" 1
  check related_stdout "$OUT" ""
  : > "$s/gh.log"
  # shellcheck disable=SC2046
  run_in "$REPO" $(gh_env "$s") GH_STUB_FAIL_CODE=404 GH_STUB_FAIL_MSG='not found' GH_STUB_FAIL_BODY='{"message":"Not Found"}' -- reviewers 404
  check reviewers_exit "$CODE" 1
  check reviewers_stdout "$OUT" ""
}

for f in $(declare -F | awk '{print $3}' | grep '^test_'); do t "$f"; done
[ $FAILS = 0 ] || { echo "$FAILS assertion(s) failed"; exit 1; }
echo "all passed"
