#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HELPER="$ROOT/.github/audit/upstream-evidence.py"
FIXTURES="$ROOT/tests/audit/fixtures/upstream-evidence"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/bin"
# Override fetcher: reads the row as JSON on stdin, prints change text.
cat > "$TMP/bin/fetch-stub" <<'STUB'
#!/usr/bin/env bash
python3 -c 'import json,sys; row=json.load(sys.stdin); print("stub change text for", row["source"])'
STUB
# Failing override fetcher: nonzero exit with a stderr reason.
cat > "$TMP/bin/fetch-fail" <<'STUB'
#!/usr/bin/env bash
cat >/dev/null
echo "stub fetch down" >&2
exit 1
STUB
# Stub gh for the default github fetcher (no network): logs every call so the
# test can assert which rows are dispatched and with which query.
cat > "$TMP/bin/gh" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "${GH_CALL_LOG:?GH_CALL_LOG must be set}"
cat <<'JSON'
[
 {"sha": "0123456789abcdef0123456789abcdef01234567",
  "commit": {"committer": {"date": "2026-01-04T12:00:00Z"}, "message": "Fix typo\n\nbody"}},
 {"sha": "fedcba9876543210fedcba9876543210fedcba98",
  "commit": {"committer": {"date": "2026-01-03T09:00:00Z"}, "message": "Add guide"}}
]
JSON
STUB
# Wikipedia transport override: receives the API URL as argv[1] and prints the
# raw response body, so tests never hit the network.
cat > "$TMP/bin/wiki-transport" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$1" > "${WIKI_TRANSPORT_LOG:?WIKI_TRANSPORT_LOG must be set}"
cat <<'JSON'
{"query": {"pages": {"1389573": {"revisions": [
  {"timestamp": "2026-01-06T00:00:00Z", "user": "WikiEditor", "comment": "copyedit pass"}
]}}}}
JSON
STUB
chmod +x "$TMP/bin/fetch-stub" "$TMP/bin/fetch-fail" "$TMP/bin/gh" "$TMP/bin/wiki-transport"
export PATH="$TMP/bin:$PATH"

# --- evidence: all kinds, dates from the snapshot, links by ref/kind ---
AUDIT_UPSTREAM_FETCH="$TMP/bin/fetch-stub" python3 "$HELPER" evidence \
  --upstreams "$FIXTURES/rows.json" --registry "$FIXTURES/registry.json" \
  --evidence-dir "$TMP/evidence" > "$TMP/written.json"
count=$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$TMP/written.json")
[ "$count" -eq 9 ] || { echo "expected 9 evidence files, got $count" >&2; exit 1; }

repo_file=$(grep -rlE 'Stale upstream key: \|o/r$' "$TMP/evidence")
grep -q 'Kind: repo' "$repo_file" || { echo 'repo evidence lost kind' >&2; exit 1; }
grep -qF 'Source last update: 2026-01-05T00:00:00Z' "$repo_file" || { echo 'evidence lost source_updated as display text' >&2; exit 1; }
grep -qF 'Our last update: 2026-01-01T00:00:00Z' "$repo_file" || { echo 'evidence lost ours_updated' >&2; exit 1; }
grep -qF 'Ref: main' "$repo_file" || { echo 'evidence lost registry ref' >&2; exit 1; }
grep -qF 'Diff link: https://github.com/o/r/compare/abc123def4567890abc123def4567890abc12345...main' "$repo_file" \
  || { echo 'repo compare link wrong'; exit 1; }
grep -q 'stub change text for o/r' "$repo_file" || { echo 'override fetch text missing' >&2; exit 1; }
if grep -q 'upstream_updated\|Upstream update' "$repo_file" "$TMP/evidence"/*; then
  echo 'evidence still references the nonexistent upstream_updated field' >&2
  exit 1
fi

repo2_file=$(grep -rlE 'Stale upstream key: \|o/r2$' "$TMP/evidence")
grep -qF 'Diff link: https://github.com/o/r2/commits/main' "$repo2_file" \
  || { echo 'repo without merge base must link commits/<ref>' >&2; exit 1; }

github_file=$(grep -rlE 'Stale upstream key: humanizer\|blader/humanizer' "$TMP/evidence")
grep -qF 'Diff link: https://github.com/blader/humanizer/commits/main' "$github_file" \
  || { echo 'github link wrong' >&2; exit 1; }

path_file=$(grep -rlE 'Stale upstream key: react-useeffect\|reactjs/react.dev' "$TMP/evidence")
grep -qF 'Diff link: https://github.com/reactjs/react.dev/commits/main/src/content/learn/you-might-not-need-an-effect.md' "$path_file" \
  || { echo 'github-path link wrong' >&2; exit 1; }

wiki_file=$(grep -rlE 'Stale upstream key: humanizer\|Wikipedia:Signs of AI writing' "$TMP/evidence")
grep -qF 'Diff link: https://en.wikipedia.org/w/index.php?title=Wikipedia%3ASigns%20of%20AI%20writing&action=history' "$wiki_file" \
  || { echo 'wikipedia link not url-quoted' >&2; exit 1; }

# Refs and paths with spaces, '#', '?' and non-ASCII are percent-encoded while
# the structural '/' separators survive.
ref_file=$(grep -rlE 'Stale upstream key: weird-ref\|o/r4$' "$TMP/evidence")
grep -qF 'Diff link: https://github.com/o/r4/commits/feat%2Fx%231' "$ref_file" \
  || { echo 'ref with slash and hash not url-encoded' >&2; exit 1; }
path2_file=$(grep -rlE 'Stale upstream key: weird-path\|o/r3:folder' "$TMP/evidence")
grep -qF 'Diff link: https://github.com/o/r3/commits/feat%2Fx%231/folder/a%20file-%C3%A9.md' "$path2_file" \
  || { echo 'path components not url-encoded' >&2; exit 1; }

# --- evidence: default fetchers are fully offline through stubbed gh and wiki ---
gh_file="$TMP/evidence-gh"
GH_CALL_LOG="$TMP/gh-calls.log" AUDIT_UPSTREAM_FETCH="" \
  AUDIT_UPSTREAM_WIKI_FETCH="$TMP/bin/wiki-transport" WIKI_TRANSPORT_LOG="$TMP/wiki-url.log" \
  python3 "$HELPER" evidence \
  --upstreams "$FIXTURES/rows.json" --registry "$FIXTURES/registry.json" \
  --evidence-dir "$gh_file" > /dev/null
# repo rows are dispatched to the commits fetcher with the registry ref, limit 20.
grep -qF 'repos/o/r/commits?sha=main&per_page=20' "$TMP/gh-calls.log" \
  || { echo 'repo kind not dispatched to the commits fetcher' >&2; exit 1; }
repo_gh=$(grep -rlE 'Stale upstream key: \|o/r$' "$gh_file")
grep -qF '0123456789ab 2026-01-04T12:00:00Z Fix typo' "$repo_gh" \
  || { echo 'repo evidence missing commits fetch text' >&2; exit 1; }
if grep -rqF 'no fetch for kind repo' "$gh_file"; then
  echo 'repo kind still skipped by the default fetcher' >&2
  exit 1
fi
humanizer_gh=$(grep -rlE 'Stale upstream key: humanizer\|blader/humanizer' "$gh_file")
grep -qF '0123456789ab 2026-01-04T12:00:00Z Fix typo' "$humanizer_gh" \
  || { echo 'default github fetch formatting wrong' >&2; exit 1; }
grep -qF 'fedcba987654 fedcba9876543210fedcba9876543210fedcba98' "$humanizer_gh" && \
  { echo 'truncated sha wrong' >&2; exit 1; }
grep -qF 'fedcba987654 2026-01-03T09:00:00Z Add guide' "$humanizer_gh" \
  || { echo 'second commit line missing' >&2; exit 1; }
# The wikipedia row goes through the redirected transport, offline.
wiki_gh=$(grep -rlE 'Stale upstream key: humanizer\|Wikipedia:Signs of AI writing' "$gh_file")
grep -qF '2026-01-06T00:00:00Z WikiEditor copyedit pass' "$wiki_gh" \
  || { echo 'wikipedia transport text missing' >&2; exit 1; }
grep -qF 'titles=Wikipedia%3ASigns%20of%20AI%20writing' "$TMP/wiki-url.log" \
  || { echo 'wikipedia transport did not receive the quoted URL' >&2; exit 1; }
# The unversioned and fresh rows stay out of the evidence set.
[ "$(ls "$gh_file" | wc -l)" -eq 9 ] || { echo 'non-stale rows produced evidence' >&2; exit 1; }

# --- evidence: fetch failures never abort and are recorded verbatim ---
fail_dir="$TMP/evidence-fail"
if ! AUDIT_UPSTREAM_FETCH="$TMP/bin/fetch-fail" python3 "$HELPER" evidence \
    --upstreams "$FIXTURES/rows.json" --registry "$FIXTURES/registry.json" \
    --evidence-dir "$fail_dir" > /dev/null; then
  echo 'fetch failure aborted the evidence run' >&2
  exit 1
fi
[ "$(ls "$fail_dir" | wc -l)" -eq 9 ] || { echo 'failed fetches dropped evidence files' >&2; exit 1; }
grep -rq 'evidence unavailable: stub fetch down' "$fail_dir" \
  || { echo 'failure reason not recorded' >&2; exit 1; }

# --- evidence: wikipedia degraded paths through the redirected transport ---
printf '%s\n' '[{"skill":"humanizer","source":"Wikipedia:Signs of AI writing","kind":"wikipedia","source_updated":"2026-01-05T00:00:00Z","ours_updated":"2026-01-01T00:00:00Z","stale":true,"error":null,"merge_base":null}]' > "$TMP/wiki-rows.json"
printf '%s\n' '[{"skill":"humanizer","kind":"wikipedia","source":"Wikipedia:Signs of AI writing","ref":null}]' > "$TMP/wiki-registry.json"
cat > "$TMP/bin/wiki-down" <<'STUB'
#!/usr/bin/env bash
cat >/dev/null
echo "wiki transport down" >&2
exit 1
STUB
cat > "$TMP/bin/wiki-garbage" <<'STUB'
#!/usr/bin/env bash
printf 'not json at all\n'
STUB
chmod +x "$TMP/bin/wiki-down" "$TMP/bin/wiki-garbage"
AUDIT_UPSTREAM_WIKI_FETCH="$TMP/bin/wiki-down" python3 "$HELPER" evidence \
  --upstreams "$TMP/wiki-rows.json" --registry "$TMP/wiki-registry.json" \
  --evidence-dir "$TMP/wiki-degraded" > /dev/null
grep -qF 'evidence unavailable: wiki transport down' "$TMP/wiki-degraded"/* \
  || { echo 'wikipedia transport failure not recorded' >&2; exit 1; }
AUDIT_UPSTREAM_WIKI_FETCH="$TMP/bin/wiki-garbage" python3 "$HELPER" evidence \
  --upstreams "$TMP/wiki-rows.json" --registry "$TMP/wiki-registry.json" \
  --evidence-dir "$TMP/wiki-garbage-dir" > /dev/null
grep -qF 'evidence unavailable: malformed Wikipedia payload' "$TMP/wiki-garbage-dir"/* \
  || { echo 'wikipedia malformed payload not degraded' >&2; exit 1; }

# --- issue: escaped cells, both dates, links, no non-stale rows ---
python3 "$HELPER" issue --upstreams "$FIXTURES/rows.json" --registry "$FIXTURES/registry.json" \
  --recommendations "$FIXTURES/recommendations.json" --issue-file "$TMP/issue.md"
grep -qF '| Key | Kind | Source | Our last update | Source last update | Diff | Recommendation | Reason |' "$TMP/issue.md" \
  || { echo 'issue header lost the date columns' >&2; exit 1; }
grep -qF '| humanizer\|blader/humanizer | github | blader/humanizer | 2026-01-01T00:00:00Z | 2026-01-05T00:00:00Z |' "$TMP/issue.md" \
  || { echo 'issue row missing escaped key or both dates' >&2; exit 1; }
grep -qF 'guide gained a rule \| worth porting' "$TMP/issue.md" \
  || { echo 'reason pipe not escaped' >&2; exit 1; }
grep -qF '| piped\|o/r\|weird | github | o/r\|weird |' "$TMP/issue.md" \
  || { echo 'literal skill|source key cells not escaped' >&2; exit 1; }
grep -qF '[diff](https://github.com/o/r/compare/abc123def4567890abc123def4567890abc12345...main)' "$TMP/issue.md" \
  || { echo 'issue lost the repo compare link' >&2; exit 1; }
grep -qF '[diff](https://github.com/o/r4/commits/feat%2Fx%231)' "$TMP/issue.md" \
  || { echo 'issue link not url-encoded' >&2; exit 1; }
grep -qF '| n/a |' "$TMP/issue.md" || { echo 'non-linked rows need n/a' >&2; exit 1; }
grep -q 'domain-name-brainstormer\|o/fresh' "$TMP/issue.md" && \
  { echo 'non-stale rows leaked into the issue' >&2; exit 1; }
grep -qF 'To apply approved updates dispatch skill-audit.yaml with approved_upstreams=<keys>' "$TMP/issue.md" \
  || { echo 'issue lost the approval instruction' >&2; exit 1; }

# --- issue: incomplete or malformed recommendations fail closed ---
printf '[{"key":"|o/r","recommendation":"update","reason":"x"}]' > "$TMP/partial-recs.json"
if python3 "$HELPER" issue --upstreams "$FIXTURES/rows.json" --registry "$FIXTURES/registry.json" \
    --recommendations "$TMP/partial-recs.json" --issue-file "$TMP/issue2.md" 2>"$TMP/err"; then
  echo 'partial recommendations unexpectedly accepted' >&2
  exit 1
fi
grep -q 'do not cover the stale rows exactly' "$TMP/err" || { echo 'coverage error not surfaced' >&2; exit 1; }

# --- workflow sync: detect ships the snapshot, the report consumes it ---
WF="$ROOT/.github/workflows/skill-audit.yaml"
grep -Fq '.github/audit/upstream-evidence.py evidence' "$WF" || { echo 'workflow lacks evidence subcommand' >&2; exit 1; }
grep -Fq '.github/audit/upstream-evidence.py issue' "$WF" || { echo 'workflow lacks issue subcommand' >&2; exit 1; }
grep -Fq 'spec/content/upstreams.json' "$WF" || { echo 'upstream-report does not consume the detect snapshot' >&2; exit 1; }
if grep -qE 'audit.py upstreams --registry' <(sed -n '/^  upstream-report:/,/^  state:/p' "$WF"); then
  echo 'upstream-report still recomputes upstreams' >&2
  exit 1
fi

printf 'PASS upstream evidence and issue consume the snapshot with per-kind links and escaped cells\n'
