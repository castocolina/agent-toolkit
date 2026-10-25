# Plan 4 — Judge and Fix Every Skill

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every editable skill passes `audit.py check --strict`, ships output evals, trigger queries and script tests, and grades B or better under the plan 2 judge; upstream inspiration sources are tracked and reviewed once.

**Architecture:** Deterministic fixes first (non-Latin, frontmatter), then tests for every skill, then the upstream-source registry, then two independent judges, a mechanical merge, `my-coding` fixers and re-judging. CI tightens one `--ignore` at a time so `main` never goes red.

**Tech Stack:** `scripts/audit/audit.py` (plan 2), pi, Claude Code subagents, `jev-fast-decision` (classification only), GitHub Actions (`main.yaml`).

**Spec:** [Roadmap](2026-10-24-00-roadmap.md) — Decisions 2, 3, 7, 9, 11, 13, 16, 17; planner calls C5, C9, C10, C11; Global Constraints apply.

Branch: `fix/<yy-mm-dd>-skill-audit-fixes` (may split by category into several PRs). Depends on plan 2.

## Review Focus

1. A strict gate runs before the fix it needs has landed → CI uses `--ignore` for exactly the codes not yet fixed. Pinned in Tasks 1, 2, 5.
2. A skill stays below 80 after the fix rounds → the PR cannot merge until the user approves more rounds or records a waiver. Pinned in Task 5.
3. A translated script changes behavior → before/after output compared. Pinned in Task 1.
4. A repository-level source (the fork's own upstream) has no skill directory → registry has a `repo` kind. Pinned in Task 4.
5. An eval prompt asks an action-taking skill to act → the runner has no tools. Pinned in Tasks 2, 5 (runner command).

Local eval runner everywhere in this plan: `RUNNER="$(python3 scripts/audit/audit.py pi-cmd runner)"`.

---

### Task 1: Deterministic fixes and CI gate

**Files:** `skills/marp-slide/{SKILL.md,README.md,assets/template-*.md,assets/theme-*.css}`, `skills/draw-io/{scripts/find_aws_icon.py,references/aws-icons.md}`, frontmatter of `skills/{design-system-starter,humanizer,qa-test-planner,react-dev}/SKILL.md`, `scripts/audit/non_latin_allowlist.txt`, `.github/workflows/main.yaml`.

- [ ] **Step 1: Classify non-Latin hits.** `jev-fast-decision` classifies each `non_latin` hit in `docs/audit/baseline-check.json` as `translate` / `allowlist`; present the table; apply after the user approves.
- [ ] **Step 2: Capture draw-io behavior before translating**

  Run: `python3 skills/draw-io/scripts/find_aws_icon.py lambda > /tmp/aws-before.txt`
- [ ] **Step 3: Translate to English.** marp trigger phrases become English equivalents ("make it look nice", "make it cool"); comments, templates, docs and `aws-icons.md` translated.
- [ ] **Step 4: Verify draw-io behavior is unchanged**

  Run: `python3 skills/draw-io/scripts/find_aws_icon.py lambda | diff - /tmp/aws-before.txt`
  Expected: no output (translated table headers may change; if they do, the data rows must be identical).
- [ ] **Step 5: Fix frontmatter** (`skills-ref` allows `name`, `description`, `license`, `allowed-tools`, `compatibility`, `metadata`; `metadata` is string→string):
  - `design-system-starter`: `tags: "design-system, ui, components, design-tokens, accessibility, frontend"` (plain string, not a flow list) and `version: "1.0.0"`.
  - `humanizer`, `react-dev`: top-level `version` → `metadata.version` (quoted).
  - `qa-test-planner`: top-level `trigger` → `metadata.trigger`.
- [ ] **Step 6: Verify the touched skills**

  Run: `python3 scripts/audit/audit.py check --strict --ignore lines_over_500,missing_evals,missing_script_tests --skills marp-slide,draw-io,meme-factory,design-system-starter,humanizer,qa-test-planner,react-dev`
  Expected: exit 0.
- [ ] **Step 7: Add the CI gate.** In `.github/workflows/main.yaml` add a `Validate skills` step: `astral-sh/setup-uv`, then `python3 scripts/audit/audit.py check --strict --ignore lines_over_500,missing_evals,missing_script_tests`.
- [ ] **Step 8: Run the full check**

  Run: `python3 scripts/audit/audit.py check --strict --ignore lines_over_500,missing_evals,missing_script_tests`
  Expected: exit 0.
- [ ] **Step 9: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/` and changes; `git commit -m "fix(skills): translate non-Latin text and normalize frontmatter"`.

### Task 2: Output evals and trigger queries for every skill

**Files:** Create `skills/<name>/evals/{evals.json,trigger-queries.json}` for every non-synced skill without them (`session-handoff` already has an `evals/` that predates the layout convention: move its test-support files, such as `setup_test_env.py` and the eval docs (`model-expectations.md`, `results-opus-baseline.md`, `test-scenarios.md`), to `tests/skills/session-handoff/`, keep only actual eval inputs in `skills/session-handoff/evals/files/`, and fix the links in `skills/session-handoff/README.md` (~line 184) that point at files no longer shipped in `dist/`). Modify `.github/workflows/main.yaml`.

- [ ] **Step 1: Write the evals** in batches of ~9 skills via subagents. `evals.json`: ≥ 3 evals per `evaluating-skills.md` (casual and precise phrasing, realistic context, objective assertions; for action-taking skills assertions check the commands/files the agent would produce). `trigger-queries.json`: sized per `optimizing-descriptions.md` (currently ~20 queries, 8–10 per class, near-misses included).
- [ ] **Step 2: Verify presence**

  Run: `python3 scripts/audit/audit.py check --strict --ignore lines_over_500,missing_script_tests`
  Expected: exit 0.
- [ ] **Step 3: Smoke-run one skill**

  Run: `python3 scripts/audit/audit.py run-evals --skills humanizer --runner "$RUNNER" --out /tmp/eval-smoke` and again with `--triggers`.
  Expected: exit 0 or 1 with summaries written (not 2).
- [ ] **Step 4: Tighten CI** to `--ignore lines_over_500,missing_script_tests`.
- [ ] **Step 5: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/` and changes; `git commit -m "test(skills): add output evals and trigger queries for every skill"`.

### Task 3: Script tests for every skill that ships scripts

**Files:** Create `tests/skills/<name>/test-*.sh` or `test_*.py` (fixtures in `tests/skills/<name>/fixtures/`; never inside the skill) for each skill flagged `missing_script_tests` in the baseline (today: `daily-meeting-update`, `dependency-updater`, `draw-io`, `meme-factory`, `plugin-forge`, `qa-test-planner`, `session-handoff`); create `scripts/audit/run-script-tests.sh`; modify `.github/workflows/main.yaml`.

- [ ] **Step 1: Write one test file per flagged skill** that runs each script with a fixture input and asserts its output (bash asserts, or `unittest` for Python scripts). Network-dependent scripts are tested with a stubbed command or a `--dry-run` path; no test calls a real external service.
- [ ] **Step 2: Write `scripts/audit/run-script-tests.sh`**: runs every `tests/skills/*/test-*.sh` with `bash`, and `python3 -m unittest discover -s <dir> -p 'test_*.py'` for every `tests/skills/*` dir that has `test_*.py`; prints one `PASS|FAIL <file>` line each; exits 1 if any failed (no `|| true` masking).
- [ ] **Step 3: Run every script test**

  Run: `bash scripts/audit/run-script-tests.sh`
  Expected: exit 0, every line `PASS`.
- [ ] **Step 4: Add a `Skill script tests` step** to `.github/workflows/main.yaml` running `bash scripts/audit/run-script-tests.sh`, and tighten `Validate skills` to `--ignore lines_over_500`.
- [ ] **Step 5: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/` and changes; `git commit -m "test(skills): add script tests for every skill with scripts"`.

### Task 4: Upstream inspiration sources (first pass)

**Files:** Create `docs/audit/upstream-sources.json`, `docs/audit/upstream-sources.md`; modify `scripts/audit/audit.py`, `tests/audit/test_audit.py`.

**Interfaces:**
- Registry entry: `{"skill":<name>|null,"kind":"github|github-path|wikipedia|repo|unversioned","source","ref"}`; `github-path` = `owner/repo:path`; `repo` = a source for the whole repository (`skill: null`).
- `fetch_source_updated(entry) -> str | None` (GitHub: `gh api repos/<o>/<r>/commits?path=<p>&per_page=1`; Wikipedia: `https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=<t>&rvprop=timestamp&format=json`; `unversioned` → `None`). Tests stub it.
- `audit.py upstreams --registry FILE` → `[{"skill","source","kind","source_updated","ours_updated","stale":bool}]`; `ours_updated` = `git log -1 --format=%cI -- skills/<skill>` (repo root for `repo`); `stale` = source newer than ours.

- [ ] **Step 1: Seed and confirm sources.** Confirm each with `rg -n "<url or credit>" skills/<skill>/` before adding: `humanizer` ← `blader/humanizer` and `Wikipedia:Signs_of_AI_writing`; `react-useeffect` ← `reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md`; `agent-md-refactor` ← Matt Pocock post (unversioned); `domain-name-brainstormer` ← Lenny's Newsletter (unversioned); repository ← `softaworks/agent-toolkit` (`kind: repo`).
- [ ] **Step 2: Scan for further sources.** Scan `skills/*/{SKILL,README}.md` for URLs/credits; `jev-fast-decision` classifies each as `inspiration-source` / `incidental-link` (e.g. `writing-clearly-and-concisely` cites Strunk's book, candidate `obra/the-elements-of-style`); present; add approved ones.
- [ ] **Step 3: Write failing tests** `test_upstreams_stale_when_source_newer`, `test_upstreams_unversioned_never_stale`, `test_upstreams_repo_kind_uses_repo_log`.
- [ ] **Step 4: Run the tests to verify they fail**

  Run: `python3 -m unittest discover -s tests/audit -v`
  Expected: the three new tests FAIL.
- [ ] **Step 5: Implement `fetch_source_updated`, `upstreams`** and the subcommand.
- [ ] **Step 6: Run the tests to verify they pass**

  Run: `python3 -m unittest discover -s tests/audit -v`
  Expected: PASS.
- [ ] **Step 7: Review stale sources.** Run `python3 scripts/audit/audit.py upstreams --registry docs/audit/upstream-sources.json`; for each stale source diff upstream changes since our last change (for `repo`: `gh api repos/softaworks/agent-toolkit/compare/<merge-base>...main`) and write `update` / `ignore` + one-line reason per entry to `upstream-sources.md`. The user decides; approved updates feed Task 5's fix list.
- [ ] **Step 8: Commit**

  `git add scripts/audit tests/audit docs/audit && git commit -m "docs(audit): track and review upstream inspiration sources"`.

### Task 5: Judge, merge, fix, re-judge

**Files:** Create `docs/audit/<yyyy-mm-dd>/{judgements/{opus,router-env-my-referee-one}/<skill>.json,check.json,merged.json,report.md,evals/}`, optional `docs/audit/waivers.json`; modify skills per the merged fix list; modify `.github/workflows/main.yaml`.

- [ ] **Step 1: Judge A (Opus).** Batches of ~9 skills; per batch dispatch a read-only native judge lane chosen at run time (for example the ai-kit read-only judge agent, or a native Opus subagent told to stay read-only) with `skills/skill-judge/references/judge-prompt.md` filled `{ROOT}=<absolute repo root>`, `{JUDGE}=opus`, `{SKILLS}=<batch>`; pipe the answer to `python3 scripts/audit/audit.py split-verdicts --judge opus --out docs/audit/<date>/judgements`.
- [ ] **Step 2: Judge B (pi).** Same batches: the `python3 scripts/audit/audit.py pi-cmd judge --print0` array of plan 2 Task 6 Step 3 (`mapfile -d '' -t JUDGE_CMD < <(...)`), with `{JUDGE}=$(python3 scripts/audit/audit.py slug router-env/my-referee-one)` and `{ROOT}`/`{SKILLS}` filled as in Step 1: `"${JUDGE_CMD[@]}" < <filled prompt file> | python3 scripts/audit/audit.py split-verdicts --judge router-env/my-referee-one --out docs/audit/<date>/judgements`, in the background. The prompt goes on stdin, never as an argument: `pi -p` also reads stdin when it is not a TTY and blocks forever on an inherited one.
- [ ] **Step 3: Validate the verdicts**

  Run: `python3 scripts/audit/audit.py validate-verdict docs/audit/<date>/judgements/*/*.json`
  Expected: exit 0; re-run the judge for a rejected skill (max 2 retries, then leave it missing).
- [ ] **Step 4: Check and merge**

  Run: `python3 scripts/audit/audit.py check > docs/audit/<date>/check.json && python3 scripts/audit/audit.py merge --in docs/audit/<date>/judgements --out docs/audit/<date> --judges opus,router-env/my-referee-one --check docs/audit/<date>/check.json --allow-incomplete`
  Expected: `merged.json`, `report.md`; missing verdicts listed. Present Disagreements and Missing verdicts to the user before fixing.
- [ ] **Step 5: Fix.** `pi -p --model router-env/my-coding` (tools enabled; outside `pi-cmd`, which only builds the restricted runner/judge commands) per batch, applying ONLY the merged fix list plus approved upstream updates (synced skills excluded); split the > 500-line bodies (`database-schema-designer`, `design-system-starter`, `mui`, `qa-test-planner`) into `references/`.
- [ ] **Step 6: Verify without ignores**

  Run: `python3 scripts/audit/audit.py check --strict`; review `git diff --stat` per skill.
  Expected: exit 0.
- [ ] **Step 7: Re-judge and run evals.** Before re-judging, delete `docs/audit/<date>/judgements/*/<skill>.json` for each re-judged skill, so a judge that drops a skill shows it as missing, not stale. Repeat Steps 1-4 for fixed skills; any skill < 80 gets up to 2 more fix rounds. Run `run-evals --runner "$RUNNER"` (output and `--triggers`) for every fixed skill into `docs/audit/<date>/evals/`.
- [ ] **Step 8: Grade gate.** If any non-synced skill is still < 80 (or `UNJUDGED`), stop and present them; the user either approves another round or adds a waiver to `docs/audit/waivers.json` (`[{"skill","percent","reason","date"}]`). Re-run Step 4 with `--waivers docs/audit/waivers.json` and WITHOUT `--allow-incomplete`.
  Expected: exit 0 and `needs_update: false`.
- [ ] **Step 9: Remove the last CI ignore.** `Validate skills` becomes `python3 scripts/audit/audit.py check --strict`; run it locally → exit 0.
- [ ] **Step 10: Commit** per category (`python3 scripts/build_plugins.py` and stage `dist/` first each time); final `git commit -m "docs(audit): <date> skill audit report"`; open the PR(s) with `/explain-pr-changes`.
