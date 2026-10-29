# Plan 4 — Judge and Fix Every Skill

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every editable skill passes `audit.py check --strict`, ships output evals, trigger queries and script tests, and is fixed toward Grade A (close to 90%) under the plan 2 judge, with 80% as the floor; upstream inspiration sources are tracked and reviewed once.

**Architecture:** Deterministic fixes first (non-Latin, frontmatter), then tests for every skill, then the upstream-source registry, then independent judge lanes chosen at run time, a mechanical merge, `my-coding` fixers, re-judging and an eval gate. CI tightens one `--ignore` at a time so `main` never goes red.

**Tech Stack:** `scripts/audit/audit.py` (plan 2), pi, GitHub Actions (`main.yaml`).

**Spec:** [Roadmap](2026-10-24-00-roadmap.md) — Decisions 2, 3, 7, 9, 11, 13, 16, 17, 19; planner calls C5, C9, C10, C11; Global Constraints apply.

Branch: `fix/<yy-mm-dd>-skill-audit-fixes`, started from plan 3's branch (`feat/26-10-25-pr-diagrams`; `main` if plan 3 has merged), and its PR uses that branch as base. May split by category into several stacked PRs. Depends on plans 2 and 3.

## Review Focus

1. A strict gate runs before the fix it needs has landed → CI uses `--ignore` for exactly the codes not yet fixed. Pinned in Tasks 1, 2, 5.
2. A skill stops short of 90% → fix rounds work from its lowest-scoring dimension, up to 3; a skill at 80-90 ships with its remaining findings reported; a skill below 80, `UNJUDGED`, or at 80+ with `needs_update: true` (critical/high finding or non-ignored check issue) is fixed or goes to the user (more rounds or, for a score below 80 only, a waiver). Pinned in Task 5.
3. A translated script changes behavior → `find_aws_icon.py` keeps only the last row per lowercase service name, so its output is not the whole table (475 table rows / 464 unique names in `aws-icons.md`). The test parses `aws-icons.md` directly and compares every `(service, resIcon)` row before and after, with the four deliberately renamed rows listed; the script output is a secondary check. Pinned in Task 1.
4. A repository-level source (the fork's own upstream) has no skill directory → registry has a `repo` kind. An unreachable or malformed source is an error row, never `stale: false`; adding evals to a skill never makes it look freshly synced. Pinned in Task 4.
5. An eval prompt asks an action-taking skill to act → the runner has no tools. Pinned in Tasks 2, 5 (runner command).
6. New or fixed evals fail or the harness breaks → every in-scope skill with evals is run (output and triggers), pass rate >= 0.9 each; exit 1 is classified and fixed in at most 3 rounds, exit 2 is a harness error. Pinned in Task 5.
7. A script test exposes an existing script defect (e.g. `meme-factory` discarding its URL) → the test is written first, fails, and the script is fixed minimally in the same task. Pinned in Task 3.

Local eval runner everywhere in this plan: `RUNNER="$(python3 scripts/audit/audit.py pi-cmd runner)"`. The shell keeps no variables between calls, so a command that needs it computes it inline; Task 5 records it once in its state file.

---

### Task 1: Deterministic fixes and CI gate

**Files:** `skills/marp-slide/{SKILL.md,README.md,assets/template-*.md,assets/theme-*.css}`, `skills/draw-io/{scripts/find_aws_icon.py,references/aws-icons.md}`, frontmatter of `skills/{design-system-starter,humanizer,qa-test-planner,react-dev}/SKILL.md`, `scripts/audit/non_latin_allowlist.txt`, `.github/workflows/main.yaml`; create `tests/skills/draw-io/{test_find_aws_icon.py,fixtures/aws-icon-rows.before.txt}`.

**Interfaces:**
- Produces: `tests/skills/draw-io/test_find_aws_icon.py` (`unittest`), the draw-io script test that Task 3's `run-script-tests.sh` picks up.

- [ ] **Step 1: Classify non-Latin hits.** Run `python3 scripts/audit/audit.py check > ${TMPDIR:-/tmp}/check-fresh.json` on this branch (`docs/audit/baseline-check.json` predates plan 3 and is not the input). Each `non_latin` hit in it is classified (fast triage) as `translate` / `allowlist`; present the table to the user; apply after the user approves.
- [ ] **Step 2: Capture the table rows before translating.** `find_aws_icon.py` keeps only the last row per lowercase service name, so its output is NOT the whole table: `aws-icons.md` has 475 table rows but 464 unique names (11 duplicated names, e.g. `auto scaling`, `nice dcv`, `amazon qldb`, `generic database`, `amazon api gateway`, `aws cloud`, `aws step functions workflow`). The before/after check therefore parses `skills/draw-io/references/aws-icons.md` directly, with the script's own regex `\|\s*([^|]+?)\s*\|\s*(mxgraph\.aws4\.[a-z0-9_]+)\s*\|`, for every row.

  Run: `python3 -c "import re;p=r'\|\s*([^|]+?)\s*\|\s*(mxgraph\.aws4\.[a-z0-9_]+)\s*\|';[print(a+'\t'+b) for a,b in re.findall(p,open('skills/draw-io/references/aws-icons.md',encoding='utf-8').read())]" > tests/skills/draw-io/fixtures/aws-icon-rows.before.txt` (one `service<TAB>resIcon` line per row, 475 lines today). `rg -c -P '[^\x00-\x7F]' tests/skills/draw-io/fixtures/aws-icon-rows.before.txt` prints `4` (the rows `ELB`, `IAM`, `Elasticsearch`, `Machine Learning`, each with a Japanese suffix). Then replace the service name of exactly those rows by the token `<renamed>`: `LC_ALL=C sed -E -i '/[\x80-\xFF]/ s/^[^\t]*/<renamed>/' tests/skills/draw-io/fixtures/aws-icon-rows.before.txt`, so the committed fixture is Latin-only (the `rg` count now prints nothing).
- [ ] **Step 3: Write the test `tests/skills/draw-io/test_find_aws_icon.py`.** `EXPECTED_RENAMES` = the four resIcons whose service name is translated on purpose: `mxgraph.aws4.elb`, `mxgraph.aws4.iam`, `mxgraph.aws4.elasticsearch_service`, `mxgraph.aws4.machine_learning`. The test keeps its own copy of the script's regex and reads `aws-icons.md` and the fixture directly. Tests:
  - `test_all_rows_survive_translation`: the file yields 475 `(service, resIcon)` rows; the fixture has the same count; the ordered resIcon lists are identical; the fixture's `<renamed>` rows are exactly the `EXPECTED_RENAMES`; every other row has an identical service name.
  - `test_expected_renames_are_english`: each of the four rows exists in the file with a changed, ASCII-only service name.
  - `test_no_non_latin_in_table_rows`: no character matching the audit's `NON_LATIN_RE` (`scripts/audit/audit.py`) in any table row (any line starting with `|`) of `aws-icons.md`.
  - `test_script_output_matches_table_rows` (secondary): the `Service:`/`resIcon:` pairs of `find_aws_icon.py mxgraph` equal the file's rows reduced to the last row per lowercase service name (464 blocks), ignoring the four renamed names.
  - `test_no_non_latin_in_output` (secondary): no `NON_LATIN_RE` match in the whole script output.

  Run: `python3 -m unittest discover -s tests/skills/draw-io -p 'test_*.py' -v`
  Expected: `test_expected_renames_are_english`, `test_no_non_latin_in_table_rows` and `test_no_non_latin_in_output` FAIL before the translation (the other two pass).
- [ ] **Step 4: Translate to English.** marp trigger phrases become English equivalents ("make it look nice", "make it cool"); comments, templates, docs, `find_aws_icon.py` strings and `aws-icons.md` translated (the four renamed rows keep their resIcon values).
  Run: the Step 3 command. Expected: all five tests PASS.
- [ ] **Step 5: Fix frontmatter** (`skills-ref` allows `name`, `description`, `license`, `allowed-tools`, `compatibility`, `metadata`; plain-string `metadata` values are this repo's convention (roadmap C5) and what the pinned parser was observed to accept, not a rule verified against `skills-ref`):
  - `design-system-starter`: its recorded baseline error is `Invalid YAML in frontmatter: While scanning` (the flow-list `tags: [...]` is invalid YAML there). Fix: `tags: "design-system, ui, components, design-tokens, accessibility, frontend"` (plain string, not a flow list) and `version: "1.0.0"`.
  - `humanizer`, `react-dev`: top-level `version` → `metadata.version` (quoted).
  - `qa-test-planner`: top-level `trigger` → `metadata.trigger`.
- [ ] **Step 6: Verify the touched skills**

  Run: `python3 scripts/audit/audit.py check --strict --ignore lines_over_500,missing_evals,missing_script_tests --skills marp-slide,draw-io,design-system-starter,humanizer,qa-test-planner,react-dev`
  Expected: exit 0.
- [ ] **Step 7: Add the CI gate.** `check` runs the pinned `skills-ref` validator through `uvx`, which CI does not have yet. In the `validate` job of `.github/workflows/main.yaml`, right after the `Set up Python` step (`actions/setup-python@v5`, the version already used there), add:

  ```yaml
      - name: Install uv
        run: python3 -m pip install uv
      - name: Validate skills
        run: python3 scripts/audit/audit.py check --strict --ignore lines_over_500,missing_evals,missing_script_tests
  ```
- [ ] **Step 8: Run the full check**

  Run: `python3 scripts/audit/audit.py check --strict --ignore lines_over_500,missing_evals,missing_script_tests`
  Expected: exit 0.
- [ ] **Step 9: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/` and changes; `git commit -m "fix(skills): translate non-Latin text and normalize frontmatter"`.

### Task 2: Output evals and trigger queries for every skill

**Files:** Create `skills/<name>/evals/{evals.json,trigger-queries.json}` for every non-synced skill without them (today 40, `draw-io` included). `session-handoff` already has an `evals/` that predates the layout convention: move its test-support files (`setup_test_env.py`, `model-expectations.md`, `results-opus-baseline.md`, `test-scenarios.md`) to `tests/skills/session-handoff/`, keep only actual eval inputs in `skills/session-handoff/evals/files/`, and in `skills/session-handoff/README.md` (lines 184-185) replace the two `evals/…` bullets with one link to `https://github.com/castocolina/agent-toolkit/tree/main/tests/skills/session-handoff` (files no longer ship in `dist/`). Modify `.github/workflows/main.yaml`.

- [ ] **Step 1: Write the evals** in batches of about 9 skills. `evals.json`: ≥ 3 evals per `skills/skill-judge/references/agentskills/evaluating-skills.md` (casual and precise phrasing, realistic context, objective assertions; for action-taking skills assertions check the commands/files the agent would produce). `trigger-queries.json`: sized per `skills/skill-judge/references/agentskills/optimizing-descriptions.md` (currently ~20 queries, 8–10 per class, near-misses included).
- [ ] **Step 2: Verify presence**

  Run: `python3 scripts/audit/audit.py check --strict --ignore lines_over_500,missing_script_tests`
  Expected: exit 0.
- [ ] **Step 3: Smoke-run one skill** (a smoke run only; the pass gate for every skill is Task 5 Step 7)

  Run: `RUNNER="$(python3 scripts/audit/audit.py pi-cmd runner)"; python3 scripts/audit/audit.py run-evals --skills humanizer --runner "$RUNNER" --out ${TMPDIR:-/tmp}/eval-smoke` and again with `--triggers` (same inline `RUNNER=`).
  Expected: exit 0 or 1 with summaries written (not 2).
- [ ] **Step 4: Tighten CI** to `--ignore lines_over_500,missing_script_tests`.
- [ ] **Step 5: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/` and changes; `git commit -m "test(skills): add output evals and trigger queries for every skill"`.

### Task 3: Script tests for every skill that ships scripts

**Files:** Create `tests/skills/<name>/test-*.sh` or `test_*.py` (fixtures in `tests/skills/<name>/fixtures/`; never inside the skill) for each skill still flagged `missing_script_tests` by a fresh `audit.py check`, one test file per script listed: `daily-meeting-update` (`claude_digest.py`), `dependency-updater` (`check-tool.sh`, `run-taze.sh`), `meme-factory` (`meme_generator.py`), `plugin-forge` (`bump_version.py`, `create_plugin.py`), `qa-test-planner` (`create_bug_report.sh`, `generate_test_cases.sh`), `session-handoff` (`check_staleness.py`, `create_handoff.py`, `list_handoffs.py`, `validate_handoff.py`). Already covered and not redone: `draw-io` (`convert-drawio-to-png.sh` by plan 3's test, `find_aws_icon.py` by Task 1's), `pr-diagrams`, `agentskills-research`. Create `scripts/audit/run-script-tests.sh`; modify `.github/workflows/main.yaml`; modify a skill script only to fix a defect one of these tests exposes (Step 1).

- [ ] **Step 1: Write one test file per flagged skill** that runs each of its scripts with a fixture input and asserts the intended behavior documented in the skill's `SKILL.md`/script docstring (bash asserts, or `unittest` for Python scripts). Tests may stub external commands (a `PATH` shim in a `mktemp -d` directory); no test calls a real external service (no `--dry-run` path is added).
  - Test-first repair path: when a test pins intended behavior that the script does not deliver, run it, see it FAIL for that reason, then fix the script minimally in this same task, commit that fix on its own (one commit per skill, English-only, `fix(<skill>): <defect>`), and see the test PASS. Never weaken a test to fit a defect.
  - Known case, `meme-factory`: `meme_generator.py` discards the generated URL and the suggested template, and its template-list loop body is only `pass`. Tests `test_generate_prints_memegen_url`, `test_suggest_prints_template_for_context` and `test_list_templates_prints_every_template` run `generate buzz "memes" "memes everywhere"`, `suggest "deployment success"` and `list-templates`, and assert the printed memegen URL, a template name from `CONTEXT_MAP["deployment"]`, and all `TEMPLATES` keys. They fail first; the script is then fixed so the CLI prints them.
- [ ] **Step 2: Write `scripts/audit/run-script-tests.sh`**: runs every `tests/skills/*/test-*.sh` with `bash`, and `python3 -m unittest discover -s <dir> -p 'test_*.py'` for every `tests/skills/*` dir that has `test_*.py`; prints one `PASS|FAIL <file>` line each; exits 1 if any failed (no `|| true` masking).
- [ ] **Step 3: Run every script test**

  Run: `bash scripts/audit/run-script-tests.sh`
  Expected: exit 0, every line `PASS` (any script defect a test exposed is fixed per Step 1 first).
- [ ] **Step 4: Add a `Skill script tests` step** to `.github/workflows/main.yaml` running `bash scripts/audit/run-script-tests.sh`, and tighten `Validate skills` to `--ignore lines_over_500`.
- [ ] **Step 5: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/` and changes; `git commit -m "test(skills): add script tests for every skill with scripts"` (script fixes from Step 1 are their own earlier commits).

### Task 4: Upstream inspiration sources (first pass)

**Files:** Create `docs/audit/upstream-sources.json`, `docs/audit/upstream-sources.md`; modify `scripts/audit/audit.py`, `tests/audit/test_audit.py`.

**Interfaces:**
- Registry entry: `{"skill":<name>|null,"kind":"github|github-path|wikipedia|repo|unversioned","source","ref"}`.
  - `github`: `source` = `owner/repo`; `github-path`: `owner/repo:path`; `repo`: `owner/repo` of the whole-repository upstream (`skill: null`); `wikipedia`: the page title; `unversioned`: a free-text citation.
  - `ref`: the branch, tag or sha read for `github`, `github-path` and `repo` (default branch name, e.g. `main`); `null` for `wikipedia` and `unversioned`.
- `validate_entry(root, entry) -> str | None`: returns the reason an entry is malformed, else `None`; run on every entry before any fetch. Rules: all four keys present; `kind` in the five supported kinds; `skill` a name matching `^[a-z0-9][a-z0-9-]*$` whose directory `skills/<skill>/` exists under `root` (resolved path stays inside `skills/`) for every kind except `repo`, where `skill` must be `null`; `source` syntax per kind (`github`/`repo`: `owner/repo`; `github-path`: `owner/repo:path` with a non-empty relative `path` containing no `..` segment; `wikipedia`: non-empty single-line title; `unversioned`: non-empty text); `ref` a non-empty string for `github`, `github-path`, `repo` and `null` for `wikipedia`, `unversioned`.
- `class SourceUnavailable(Exception)`. `source_query(entry) -> str | None` builds the request per kind and is the unit the query test checks: `github-path` → `repos/<o>/<r>/commits?path=<p>&sha=<ref>&per_page=1`; `github` → `repos/<o>/<r>/commits?sha=<ref>&per_page=1` (no `path`); `repo` → the same query as `github` (never a path: the latest commit on the upstream repo's default branch `ref`); `wikipedia` → `https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=<t>&rvprop=timestamp&format=json` (title URL-quoted); `unversioned` → `None`. `fetch_source_updated(entry) -> str | None` returns an ISO timestamp (GitHub kinds: `gh api "<source_query>"`; Wikipedia: a GET with `urllib.request` from the standard library, `timeout=10` seconds), `None` for `unversioned`, and raises `SourceUnavailable(reason)` on a `gh` non-zero exit (auth, rate limit), a network error or timeout, an empty commit list or a response without the timestamp field. Tests stub it.
- `ours_updated(root, entry) -> str | None`: the date of the last commit touching `skills/<skill>/SKILL.md` or `skills/<skill>/references/` (`git log -1 --format=%cI -- <those paths>`), never `evals/`, `tests/` or `dist/`; `None` when there is no such commit. For `kind: repo`: `git fetch --quiet https://github.com/<source>.git <ref>`, then the committer date of `git merge-base HEAD FETCH_HEAD`, or of the earliest local commit when the histories are unrelated (a fetch failure raises `SourceUnavailable`). Tests point the repo URL at a local fixture repository.
- `audit.py upstreams --registry FILE` → `[{"skill","source","kind","source_updated","ours_updated","stale":bool|null,"error":str|null}]`. `stale` = source newer than ours; `unversioned` → `stale: false`, `source_updated: null`. A malformed entry (`validate_entry` reason), a `SourceUnavailable` or a `None` `ours_updated` gives `stale: null` and `error: <reason>` (`invalid entry: <reason>` for a malformed one, which is never fetched). Exit 1 when any row has an error, so a failure is never read as "not stale"; else exit 0. A registry file that is unreadable, not JSON or not a list exits 2 with a message on stderr.

- [ ] **Step 1: Seed and confirm sources.** Confirm each with `rg -n "<url or credit>" skills/<skill>/` before adding: `humanizer` ← `blader/humanizer` and `Wikipedia:Signs_of_AI_writing`; `react-useeffect` ← `reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md`; `agent-md-refactor` ← Matt Pocock post (unversioned); `domain-name-brainstormer` ← Lenny's Newsletter (unversioned); repository ← `softaworks/agent-toolkit` (`kind: repo`, `ref: main`).
- [ ] **Step 2: Scan for further sources.** Scan `skills/*/{SKILL,README}.md` for URLs/credits; each is classified (fast triage) as `inspiration-source` / `incidental-link` (e.g. `writing-clearly-and-concisely` cites Strunk's book, candidate `obra/the-elements-of-style`); present the table to the user; add approved ones.
- [ ] **Step 3: Write failing tests** in `tests/audit/test_audit.py`: `test_upstreams_stale_when_source_newer`, `test_upstreams_unversioned_never_stale`, `test_upstreams_repo_kind_uses_merge_base`, `test_upstreams_fetch_failure_is_error_not_stale` (stub raises `SourceUnavailable`: row has `stale: null`, an `error`, and the command exits 1), `test_upstreams_evals_only_commit_does_not_reset_staleness` (temp git repo: a later commit touching only `evals/` leaves `ours_updated` at the SKILL.md commit), `test_upstreams_empty_local_history_is_error`, `test_fetch_source_updated_malformed_response_raises`, `test_source_query_per_kind` (subTests: `github` has no `path`, `github-path` has `path` and `sha`, `repo` has no `path`, `wikipedia` has the quoted title, `unversioned` is `None`), `test_upstreams_invalid_entries_are_error_rows` (subTests: missing key, unknown kind, skill directory absent, `skill` `../x`, bad `source` per kind, `github-path` with a `..` segment, `repo` with a non-null `skill`, `github` with `ref: null`, `wikipedia` with a non-null `ref`; each yields `error` starting `invalid entry`, `stale: null`, the fetch stub is never called, a valid sibling row is still processed, exit 1), `test_upstreams_unreadable_registry_exits_2` (missing file, non-JSON, JSON object instead of list).
- [ ] **Step 4: Run the tests to verify they fail**

  Run: `python3 -m unittest discover -s tests/audit -v`
  Expected: the ten new tests FAIL.
- [ ] **Step 5: Implement `validate_entry`, `SourceUnavailable`, `source_query`, `fetch_source_updated`, `ours_updated`, `upstreams`** and the subcommand.
- [ ] **Step 6: Run the tests to verify they pass**

  Run: `python3 -m unittest discover -s tests/audit -v`
  Expected: PASS.
- [ ] **Step 7: Review stale sources.** Run `python3 scripts/audit/audit.py upstreams --registry docs/audit/upstream-sources.json`; an error row (exit 1) is investigated and re-run, never skipped. For each stale source diff upstream changes since our last change (for `repo`: `gh api repos/softaworks/agent-toolkit/compare/<merge-base>...main`) and write `update` / `ignore` + one-line reason per entry to `upstream-sources.md`. The user decides (user gate); approved updates feed Task 5's fix list.
- [ ] **Step 8: Commit**

  `git add scripts/audit tests/audit docs/audit && git commit -m "docs(audit): track and review upstream inspiration sources"`.

### Task 5: Judge, merge, fix, re-judge

**Files:** Create `docs/audit/<yyyy-mm-dd>/{judgements/<lane slug>/<skill>.json,check.json,merged.json,report.md,remaining-findings.md,evals/}`, optional `docs/audit/waivers.json`; modify skills per the merged fix list; modify `.github/workflows/main.yaml`.

**Interfaces:**
- State (shell keeps no variables between calls): Step 1 writes `${TMPDIR:-/tmp}/plan4/state.env` once with `RUNNER`, `S`, `D` (the date directory `docs/audit/<yyyy-mm-dd>`, date taken once), `T` (scratch dir `${TMPDIR:-/tmp}/plan4-judge`, outside `docs/audit/`), `LANES` (space-separated `<slug>=<model>`), `JUDGES` (comma-joined slugs), `N` (lane count), `JUDGED_AT` (the commit the verdicts describe), `S_TODO` (comma list) and `BATCHES` (space-separated comma-joined batches). EVERY later command in this task runs as `( set -euo pipefail; . "${TMPDIR:-/tmp}/plan4/state.env"; : "${RUNNER:?}" "${S:?}" "${D:?}" "${T:?}" "${JUDGES:?}" "${N:?}"; <command> )`, written below as `<guard>; <command>`; a step that uses `LANES`, `S_TODO`, `BATCHES` or `JUDGED_AT` adds them to the `:?` list. An empty `S` therefore stops the step and never widens scope.
- Scope `S` (Roadmap PLAN 4): every skill directory except `gepetto` and `datadog-cli`: `S=$(ls -1 skills | rg -v -x 'gepetto|datadog-cli' | paste -sd, -)`. Judging, `check --skills` and `merge --skills` all use this one list. Batches of about 9: `echo "$S_TODO" | tr , '\n' | xargs -n 9 | tr ' ' ,` prints one comma-joined batch per line.
- Judging follows Decisions 2, 9 and 19: run `skill-judge` with the lanes chosen at run time, never hard-coded here (examples: `router-env/my-referee-one`, `router-env/my-referee-three`). Every lane is a read-only `pi` judge built by `audit.py pi-cmd judge --print0 --model <model>`. `J` = a lane's slug (`audit.py slug <model>`).
- Fix ordering, `ORDER <skill>` (merged.json carries no per-dimension scores; every validated verdict does): `jq -s -r 'map(. as $v | .scores | to_entries[] | {d:.key, r:(.value / $v.max[.key])}) | group_by(.d) | map({d:.[0].d, r:(map(.r)|add/length)}) | sort_by(.r)[] | "\(.d) \(.r*100|round)%"' $D/judgements/*/<skill>.json` prints `D<n> <percent>%`, the mean over lanes of score/max per dimension, lowest first.

- [ ] **Step 1: Reuse, batch and record state.** One command, in one call, after `export MODELS="<space-separated pi models the user chose as lanes>"` (the only run-time input; `REUSE=0` in the environment disables reuse). It computes `RUNNER`, `S`, `D` (date taken once), `T`, `JUDGED_AT`, `LANES` (slugs via `audit.py slug`), `JUDGES`, `N`, the reuse check and `S_TODO`, the `BATCHES` list (about 9 skills each), and writes `${TMPDIR:-/tmp}/plan4/state.env` in the same call:

  ```bash
  ( set -euo pipefail; shopt -s nullglob; : "${MODELS:?export MODELS (space-separated pi models) first}"
    RUNNER="$(python3 scripts/audit/audit.py pi-cmd runner)"
    S=$(ls -1 skills | rg -v -x 'gepetto|datadog-cli' | paste -sd, -)
    D=docs/audit/$(date +%F); T=${TMPDIR:-/tmp}/plan4-judge; JUDGED_AT=$(git rev-parse HEAD)
    LANES=""; JUDGES=""; N=0
    for m in $MODELS; do j=$(python3 scripts/audit/audit.py slug "$m"); LANES="${LANES:+$LANES }$j=$m"; JUDGES="${JUDGES:+$JUDGES,}$j"; N=$((N+1)); done
    mkdir -p "$T" "$D/judgements" "${TMPDIR:-/tmp}/plan4"
    S_TODO=""
    for s in ${S//,/ }; do
      ok=1
      for l in $LANES; do
        j=${l%%=*}; got=0
        if [ "${REUSE:-1}" = 1 ]; then
          for f in docs/audit/*-plan2/judgements/$j/$s.json docs/audit/*-plan3/judgements/$j/$s.json; do
            c=$(git log -1 --format=%H -- "$f"); [ -n "$c" ] || continue
            if git diff --quiet "$c" HEAD -- skills/$s tests/skills/$s skills/skill-judge; then mkdir -p "$D/judgements/$j"; cp "$f" "$D/judgements/$j/"; got=1; fi
          done
        fi
        [ $got = 1 ] || ok=0
      done
      [ $ok = 1 ] || S_TODO="${S_TODO:+$S_TODO,}$s"
    done
    BATCHES=$(echo "$S_TODO" | tr , '\n' | xargs -r -n 9 | tr ' ' , | paste -sd' ' -)
    for v in RUNNER S D T LANES JUDGES N JUDGED_AT S_TODO BATCHES; do printf '%s=%q\n' $v "${!v}"; done > "${TMPDIR:-/tmp}/plan4/state.env"
  )
  ```

  - Reuse rule the command implements: a verdict from an earlier run (`docs/audit/*-plan2`, plan 3's `docs/audit/*-plan3`) is copied into `$D/judgements/<J>/` only for a chosen lane's slug and only when `git diff --quiet $(git log -1 --format=%H -- <verdict path>) HEAD -- skills/<skill> tests/skills/<skill> skills/skill-judge` exits 0: the skill, its tests (scored by D7) and the shared judging inputs (rubric, judge prompt, schema) are all unchanged since the verdict's commit. A skill is in `S_TODO` unless every lane has a reused verdict. `scripts/audit/audit.py` is not in that diff: it counts as a shared input only if its diff since the verdict's commit touches rubric parsing, `validate_verdict` or grading (Task 4 adds only `upstreams`, which does not); the executor checks this by hand and sets `REUSE=0` if it does. Expected reuse: `agentskills-research`, `skill-judge`, possibly `pr-diagrams`; `draw-io` changed in Task 1 and every skill that gained a Task 3 test is re-judged.

  Expected: `. "${TMPDIR:-/tmp}/plan4/state.env"; echo "$S $D $N"` prints non-empty values.
- [ ] **Step 2: Fill prompts and run every lane.** One command, in one call. It sources the state file, and per batch fills the judge prompt for every lane (`sd`, under `$T/<lane slug>/prompt-<batch number>.txt`), builds the lane's read-only `pi-cmd judge` command and starts one background job per lane, waits for that batch's jobs inside the same guarded subshell (a failed job is reported on stderr and handled by Step 3's retry), then runs `split-verdicts` on every saved output file. The prompt goes on stdin, never as an argument: `pi -p` also reads stdin when it is not a TTY and blocks forever on an inherited one.

  ```bash
  ( set -euo pipefail; . "${TMPDIR:-/tmp}/plan4/state.env"; : "${RUNNER:?}" "${S:?}" "${D:?}" "${T:?}" "${JUDGES:?}" "${N:?}" "${LANES:?}"
    n=0
    for batch in $BATCHES; do
      n=$((n+1)); JOBS=()
      for l in $LANES; do
        j=${l%%=*}; m=${l#*=}; mkdir -p "$T/$j"
        sd -F '{ROOT}' "$(pwd)" < skills/skill-judge/references/judge-prompt.md | sd -F '{SKILLS}' "$batch" | sd -F '{JUDGE}' "$j" > "$T/$j/prompt-$n.txt"
        ( mapfile -d '' -t PI < <(python3 scripts/audit/audit.py pi-cmd judge --print0 --model "$m"); "${PI[@]}" < "$T/$j/prompt-$n.txt" > "$T/$j/$n.out" ) &
        JOBS+=("$!:$j-$n")
      done
      for x in "${JOBS[@]}"; do wait "${x%%:*}" || echo "FAILED job ${x#*:}" >&2; done
    done
    for l in $LANES; do
      j=${l%%=*}; m=${l#*=}
      for f in "$T/$j"/*.out; do python3 scripts/audit/audit.py split-verdicts --judge "$m" --out "$D/judgements" < "$f"; done
    done
  )
  ```

- [ ] **Step 3: Validate the verdicts**

  Run: `<guard>; python3 scripts/audit/audit.py validate-verdict $D/judgements/*/*.json`
  Expected: exit 0; re-run the lane for a rejected skill (max 2 retries). A skill still missing a verdict is `UNJUDGED`: it cannot be waived, so it stops at the Step 8 user gate.
- [ ] **Step 4: Check and merge**

  Run: `<guard>; python3 scripts/audit/audit.py check --skills "$S" > $D/check.json; python3 scripts/audit/audit.py merge --in $D/judgements --out $D --judges "$JUDGES" --min-judges "$N" --skills "$S" --check $D/check.json --allow-incomplete`
  Expected: `merged.json`, `report.md`; missing verdicts listed. Present Disagreements and Missing verdicts to the user before fixing (user gate).
- [ ] **Step 5: Fix, one batch at a time.** The fixer is `pi` with tools enabled, outside `pi-cmd` (which only builds the restricted runner/judge commands). Per batch (under `<guard>` with `BATCHES`) write the prompt file `$T/fix-<n>.txt` with: the batch's skills; per skill, the `ORDER <skill>` output (lowest dimensions first, the fixer works from the top) followed by its merged findings, all severities (`jq --arg s <skill> '.skills[] | select(.name==$s) | .findings' $D/merged.json`); the approved upstream updates for them from `upstream-sources.md`; and the rails: English only, no attribution trailers, layout per `AGENTS.md` and `docs/conventions/skill-layout.md`, never edit `gepetto`/`datadog-cli`, never make an eval easier, leave `skills/skill-judge/` rubric, prompt and schema alone unless a finding requires it (such an edit forces a full re-judge, Step 7), `SKILL.md` under 500 lines (split `database-schema-designer`, `design-system-starter`, `mui`, `qa-test-planner` into `references/`). Run `pi -p --model router-env/my-coding < $T/fix-<n>.txt > $T/fix-<n>.out` (prompt on stdin). Then, before any re-judging: `bash scripts/audit/run-script-tests.sh`, `python3 scripts/build_plugins.py`, review `git diff --stat` per skill, and commit (`git commit -m "fix(skills): apply judged fixes, batch <n>"`, `dist/` staged), so the reports describe a tree that is in git.
- [ ] **Step 6: Verify without ignores**

  Run: `python3 scripts/audit/audit.py check --strict`
  Expected: exit 0.
- [ ] **Step 7: Re-judge and run evals.**
  - Re-judge: under `<guard>` with `JUDGED_AT`, the changed set is `git diff --name-only $JUDGED_AT HEAD -- skills tests/skills scripts/audit/audit.py`, mapped to skills. If it touches `skills/skill-judge/` (rubric, judge prompt or schema) or the rubric/scoring/verdict-validation code of `audit.py`, every verdict is stale: re-judge EVERY skill of `S` (`S_TODO=$S`). Otherwise `S_TODO` = the skills whose `skills/<skill>/` or `tests/skills/<skill>/` changed. Delete `$D/judgements/*/<skill>.json` for every skill in `S_TODO` (a lane that drops a skill must show it as missing, not stale), rewrite `S_TODO`, `BATCHES` and `JUDGED_AT=$(git rev-parse HEAD)` in the state file, repeat Steps 2-4 for them (Step 4 merges the whole `$S`), then Step 5 on what is still below about 90%, up to 3 fix rounds in all.
  - Evals (under `<guard>`): for every skill of `S` that has `evals/evals.json` (`E=$(for s in ${S//,/ }; do [ -f skills/$s/evals/evals.json ] && echo $s; done | paste -sd, -)`; not only fixed skills): `python3 scripts/audit/audit.py run-evals --skills "$E" --runner "$RUNNER" --fail-under 0.9 --out $D/evals` and again with `--triggers`.
  - Gate (under `<guard>`): `for f in $D/evals/*/summary-*.json; do jq -e '.total > 0 and (.passed / .total) >= 0.9' "$f" > /dev/null || echo "FAIL $f"; done` prints nothing. Exit 2 is a harness error: fix the cause and re-run. Exit 1 or a FAIL line: classify each failure as skill defect / eval defect / grader noise (present the table to the user), fix, re-run (a changed skill returns to the re-judge bullet), at most 3 rounds, then the user gate.
- [ ] **Step 8: Grade gate.** Under `<guard>`, merge once more without `--allow-incomplete`, passing `--waivers docs/audit/waivers.json` only if that file exists: `python3 scripts/audit/audit.py merge --in $D/judgements --out $D --judges "$JUDGES" --min-judges "$N" --skills "$S" --check $D/check.json` (`check.json` regenerated as in Step 4), then `jq -e '.complete == true and .needs_update == false and all(.skills[]; .grade != "UNJUDGED" and ((.percent // 0) >= 80 or .waived))' $D/merged.json`.
  Expected: both exit 0. Skills at 80-90 ship with their remaining findings written by Step 9 (and put in the PR body). Otherwise stop and present the failing skills to the user: a skill below 80 gets another round or a waiver in `docs/audit/waivers.json` (`[{"skill","percent","reason","date"}]`, which only lowers the score bar); a skill at 80+ with `needs_update: true` has its critical/high finding or check issue fixed (a waiver does not clear it); an `UNJUDGED` skill gets its judge re-run, and if still missing the user decides how to proceed (it cannot be waived).
- [ ] **Step 9: Write the remaining findings.** `merge`'s `report.md` is not enough: it holds scores and the Disagreements/Missing/Below target/Waived/Synced sections only, no findings, and "Below target" lists just skills under 80 (`TARGET`). So, from the Step 8 `merged.json` and under `<guard>`: `jq -r '.skills[] | select((.synced|not) and (.percent==null or .percent<90)) | "## \(.name): \(if .percent == null then "UNJUDGED" else "\(.percent)%" end)", "", (.findings[] | "- [\(.severity)] \(.dimension) \(.file):\(.line // "-"): \(.fix)"), "- Reason it ships: TBD", ""' $D/merged.json > $D/remaining-findings.md`. Then replace each `TBD` with a one-line reason that skill ships below 90 (finding judged `ignore` with why, fix rejected as out of scope, waived, rounds exhausted), written by the controller from the Step 5 fix outputs.
  Run: `<guard>; ! rg -n 'TBD' $D/remaining-findings.md`
  Expected: exit 0 (no placeholder left). Re-run this step after any later Step 8 round.
- [ ] **Step 10: Remove the last CI ignore and re-verify.** `Validate skills` becomes `python3 scripts/audit/audit.py check --strict`; run it locally → exit 0. After the final fixes also run `bash scripts/audit/run-script-tests.sh` (exit 0), and, under `<guard>`, when `skills/pr-diagrams/SKILL.md` changed since plan 3, plan 3's command-eval gate: `python3 scripts/audit/audit.py run-evals --eval-file commands/evals/explain-pr-changes.json --runner "$RUNNER" --fail-under 1.0 --out $D/evals-command`, then `jq -e '.total > 0 and .passed == .total and (.failures | length == 0)' $D/evals-command/explain-pr-changes/summary-output.json` (exit 0; failures classified and fixed as in plan 3 Task 3 Step 12).
- [ ] **Step 11: Commit and write the PR body.** The skill fixes were already committed per batch in Step 5 (and in Step 7 fix rounds), so they are not committed again. Run `python3 scripts/build_plugins.py` (no `dist/` change is expected after Step 5), then commit only: (a) the audit reports under `docs/audit/<date>/`, plus `docs/audit/waivers.json` if it exists: `git add docs/audit && git commit -m "docs(audit): <date> skill audit report"`; (b) the final CI change from Step 10: `git add .github/workflows/main.yaml && git commit -m "ci: run strict skill validation without ignores"`. Include `$D/remaining-findings.md` in the body (its content under a "Remaining findings" heading). Follow `commands/explain-pr-changes.md` with `--base=feat/26-10-25-pr-diagrams` (plan 3's branch; `main` if it has merged) **only to compose the PR body text**, saved to `${TMPDIR:-/tmp}/pr-body-skill-audit-fixes.md` (not a registered slash command in this checkout; run none of its push, `gh pr create` or `gh pr edit` steps). Pushing and opening the PR(s) belong to the roadmap ship step, after the final code review and history compaction.
  Expected: the body file exists and is non-empty, every `## <skill>` heading of `$D/remaining-findings.md` appears in it (`rg -c` equals the heading count); `git status --porcelain` prints nothing.
