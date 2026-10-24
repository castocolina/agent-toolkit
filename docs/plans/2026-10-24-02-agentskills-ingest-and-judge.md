# Plan 2 — agentskills Ingest Skill and Spec-Aligned skill-judge

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A new `agentskills-research` skill ingests the Agent Skills docs and reference validator from `agentskills/agentskills`, and `skill-judge` is rebuilt on them, with deterministic tooling that validates the judge's output and runs skill evals.

**Architecture:** A bash fetcher copies the upstream docs verbatim into `skills/skill-judge/references/agentskills/`, pinned by commit SHA. `skill-judge` reads a machine-parseable `rubric.md` that cites those docs. Judges emit JSON lines; `scripts/audit/audit.py` splits, validates (against the rubric, never against the judge's own numbers), merges with coverage accounting, and runs output and trigger evals through a pluggable stdin/stdout runner.

**Tech Stack:** Bash, Python 3.12 stdlib, `uvx` + `skills-ref` (pinned to the fetched SHA), pi (local runner).

**Spec:** [Roadmap](2026-10-24-00-roadmap.md) — Decisions 1, 3, 7, 13, 16, 17; planner calls C3, C4, C5, C9; Global Constraints apply.

Branch: `feat/<yy-mm-dd>-agentskills-ingest-judge`. Depends on nothing; plans 3, 4 and 5 depend on it.

## Review Focus

1. Spec fetch fails mid-way (network, missing file) → previously stored references stay byte-identical. Pinned in Task 1.
2. A judge emits malformed JSON, NaN, scores outside the rubric's `max`, an inflated `max`, a wrong total/percent/grade, or a stale `rubric_version`/`spec_sha` → verdict rejected, never merged. Pinned in Task 4.
3. A skill ends up with no valid verdict → reported `UNJUDGED`, merge exits 2 unless explicitly allowed. Pinned in Task 4.
4. An eval prompt for an action-taking skill (jira, codex, gemini, commit-work) → the runner has no tools and runs in a sandbox cwd, so nothing real happens. Pinned in Task 5.
5. A synced skill (`gepetto`, `datadog-cli`) is passed to `run-evals` → skipped and reported, not an error. Pinned in Task 5.

---

### Task 1: `agentskills-research` skill with tested spec fetcher

**Files:**
- Create: `skills/agentskills-research/{SKILL.md,README.md}`, `skills/agentskills-research/scripts/fetch-spec.sh`
- Create: `skills/agentskills-research/evals/test-fetch-spec.sh`, fixtures `skills/agentskills-research/evals/fixtures/deadbeef/docs/{specification.mdx,skill-creation/{quickstart,best-practices,evaluating-skills,optimizing-descriptions,using-scripts}.mdx}` and symlink `evals/fixtures/cafebabe -> deadbeef`
- Create (first real run): `skills/skill-judge/references/agentskills/{specification,quickstart,best-practices,evaluating-skills,optimizing-descriptions,using-scripts}.md` + `SOURCE.json`
- Modify: `.claude-plugin/marketplace.json` (new plugin entry), `README.md` (skills table)

**Interfaces:**
- `fetch-spec.sh [--dest DIR] [--ref REF]` (default dest `skills/skill-judge/references/agentskills`, ref `main`) → stdout `{"ref","sha":"<resolved>","changed":[names],"unchanged":[names]}`; exit 0 on success, 1 on any failure.
- Resolution: `sha` = `AGENTSKILLS_SHA` if set, else `git ls-remote https://github.com/agentskills/agentskills refs/heads/<ref>`. Every file is downloaded from `$AGENTSKILLS_RAW_BASE/<sha>/docs/<path>` (default base `https://raw.githubusercontent.com/agentskills/agentskills`), so content and recorded SHA always match.
- Source map: `docs/specification.mdx` → `specification.md`; `docs/skill-creation/<page>.mdx` → `<page>.md`.
- `SOURCE.json`: `{"repo":"agentskills/agentskills","ref","sha","fetched_at":"<ISO8601>","license":"CC-BY-4.0","files":{"<name>.md":"<sha256>"}}`, rewritten only when `changed` is non-empty (so `sha` is stable while the docs are stable).

- [ ] **Step 1: Write failing tests** in `evals/test-fetch-spec.sh` (plain bash asserts; `AGENTSKILLS_RAW_BASE=file://$FIXTURES`):
  - `test_first_run_all_changed` (`AGENTSKILLS_SHA=deadbeef`, empty dest → 6 `changed`, 6 files + `SOURCE.json`).
  - `test_second_run_unchanged` (`AGENTSKILLS_SHA=cafebabe` → `changed == []`, files and `SOURCE.json` byte-identical, stdout `sha` == `deadbeef`).
  - `test_one_file_changed` (edit one fixture → `changed == ["best-practices.md"]`).
  - `test_missing_source_keeps_dest` (delete one fixture → exit 1, dest `sha256sum` unchanged).
- [ ] **Step 2: Run the tests to verify they fail**

  Run: `bash skills/agentskills-research/evals/test-fetch-spec.sh`
  Expected: FAIL (script missing).
- [ ] **Step 3: Implement `fetch-spec.sh`**: download all six into a `mktemp -d` staging dir (trap cleanup); only when all six succeed compare sha256 against `SOURCE.json`, move changed files into dest, rewrite `SOURCE.json`. Content is copied verbatim with a one-line attribution header.
- [ ] **Step 4: Run the tests to verify they pass**

  Run: `bash skills/agentskills-research/evals/test-fetch-spec.sh`
  Expected: all four PASS.
- [ ] **Step 5: Write `SKILL.md` and `README.md`** (use superpowers:writing-skills; follow the fetched `best-practices.md` and `optimizing-descriptions.md`). Workflow: run `fetch-spec.sh`; if `changed` is empty report "spec unchanged at <sha>" and stop; else read `git diff -- skills/skill-judge/references/agentskills`, list rule additions/removals, update `skills/skill-judge/references/rubric.md` (Task 2) with `rubric_version` +1 and `spec_sha` = `SOURCE.json` sha, and also check whether the `skills-ref` validator changed at that SHA (`skills-ref/src/skills_ref/validator.py`); finish with `python3 scripts/audit/audit.py rubric-check` exiting 0. Description triggers: "refresh agent skills spec", "update skill-judge from agentskills.io".
- [ ] **Step 6: Fetch the real spec**

  Run: `bash skills/agentskills-research/scripts/fetch-spec.sh`
  Expected: JSON with 6 `changed`; six references + `SOURCE.json` exist.
- [ ] **Step 7: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/`, `.claude-plugin/marketplace.json`, new files; `git commit -m "feat(agentskills-research): ingest and track Agent Skills spec"`.

### Task 2: Rebuild `skill-judge` on the fetched spec

**Files:**
- Modify: `skills/skill-judge/SKILL.md` (752 → < 500 lines)
- Create: `skills/skill-judge/references/{rubric.md,verdict.schema.json,judge-prompt.md}`
- Create: `skills/skill-judge/evals/{evals.json,trigger-queries.json}`

**Interfaces:**
- `rubric.md` (parsed by `audit.py load_rubric`): first two lines `rubric_version: <int>` and `spec_sha: <40 hex>`; then ONE table `| id | name | max | source |` with rows `D1`..`D8` (`max` int > 0; `source` = `references/agentskills/<file>.md#<heading>`); prose criteria follow.
- Required criteria (Decisions 16, 17): D1 Knowledge Delta flags content current harnesses (Claude Code, Codex, Cursor, opencode, pi, Copilot CLI) already do natively or current models already know, judged from the judge's own knowledge; one dimension scores tests (output evals, trigger queries, and a runnable test when `scripts/` exists), citing `evaluating-skills.md`, `optimizing-descriptions.md`, `using-scripts.md`.
- Verdict (one JSON object per line on the judge's stdout): `{"skill","judge","rubric_version","spec_sha","scores":{"D1":int…"D8":int},"max":{"D1":int…},"total":int,"max_total":int,"percent":float,"grade":"A|B|C|D|F","findings":[{"id","dimension","severity":"critical|high|medium|low","file","line","evidence","fix"}]}`. `percent = round(total/max_total*100, 1)`; A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, else F.
- `judge-prompt.md`: template with placeholders `{JUDGE}` (judge slug, Task 3 `slug`), `{SKILLS}` (comma list of skill dirs) and `{ROOT}`; tells the judge to print exactly one verdict line per listed skill and nothing else.

- [ ] **Step 1: Write `references/rubric.md`** in the shape above; keep the current 8 dimensions where the spec supports them; `rubric_version: 1`; `spec_sha` from `SOURCE.json`.
- [ ] **Step 2: Rewrite `SKILL.md`**: protocol step 1 is MANDATORY `Read` of `rubric.md` and each spec file it cites (whole sections); verdicts copy `rubric_version`, `spec_sha` and every `max` from the rubric; output contract = JSON lines per `judge-prompt.md`. Replace the Chinese bad-description example (lines ~267-271) with an English one (`"Handles document stuff"`).
- [ ] **Step 3: Write `references/verdict.schema.json` and `references/judge-prompt.md`** per the Interfaces block.
- [ ] **Step 4: Write the evals.** `evals.json`: ≥ 3 evals (a strong skill, a vague-description skill, an over-500-line skill) with assertions like `"Every output line is one JSON object"`, `"D4 score is below half of max for the vague-description skill"`. `trigger-queries.json`: `[{"query","should_trigger"}]` sized per the fetched `optimizing-descriptions.md` (currently ~20 queries, 8–10 per class, near-misses such as "write me a new skill from scratch").
- [ ] **Step 5: Verify**

  Run: `wc -l skills/skill-judge/SKILL.md` → Expected: < 500.
  Run: `uvx --from "git+https://github.com/agentskills/agentskills@$(jq -r .sha skills/skill-judge/references/agentskills/SOURCE.json)#subdirectory=skills-ref" skills-ref validate skills/skill-judge` → Expected: exit 0.
- [ ] **Step 6: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/` and changes; `git commit -m "refactor(skill-judge): derive rubric from Agent Skills spec"`.

### Task 3: `audit.py` — check, rubric-check, slug, split-verdicts

**Files:**
- Create: `scripts/audit/audit.py`, `scripts/audit/test_audit.py`, `scripts/audit/non_latin_allowlist.txt`
- Test: `python3 -m unittest discover -s scripts/audit -v`

**Interfaces:**
- Constants: `SYNCED = {"gepetto","datadog-cli"}`; `C5_FIELDS = {"user-invocable","disable-model-invocation","argument-hint"}`.
- `run_skills_ref(skill_dir: Path) -> tuple[int, str]` — `uvx --from git+https://github.com/agentskills/agentskills@<SOURCE.json sha>#subdirectory=skills-ref skills-ref validate <dir>`; tests inject a stub.
- `audit.py check [--strict] [--skills a,b] [--ignore CODE,…]` → `{"skills":[{"name","ok","synced","issues":[{"code","detail"}]}]}`. Codes: `skills_ref`, `lines_over_500`, `description_too_long`, `name_mismatch`, `missing_readme`, `non_latin`, `missing_evals` (`evals/evals.json` or `evals/trigger-queries.json` absent/invalid JSON), `missing_script_tests` (`scripts/` has files but no `evals/test-*.sh` or `evals/test_*.py`). `missing_*` never apply to synced skills. `--ignore` drops codes from `ok`/exit (still printed). `--strict` exits 1 when any non-synced skill has a non-ignored issue.
- C5 handling: in `skills-ref` output, drop the line `Unexpected fields in frontmatter: <list>.` when every listed field is in `C5_FIELDS`; `skills_ref` is an issue only if other error lines remain.
- Non-Latin: any char in the Han, Hiragana, Katakana, Hangul, Cyrillic, Arabic, Hebrew, Thai, Devanagari or Greek script ranges (embedded constant; `unicodedata` has no script property) is an issue unless `path:line-text` is in `non_latin_allowlist.txt` (seed: the kaomoji lines of `skills/meme-factory/references/markdown-memes-guide.md`).
- `audit.py rubric-check [--rubric FILE]` → exit 0 when the front block parses, `D1`..`D8` present with int `max` > 0 and `spec_sha` equals `SOURCE.json` sha; else exit 1 with one reason per line. Exposes `load_rubric(path) -> {"version":int,"spec_sha":str,"max":{"D1":int,…}}`.
- `slug(model: str) -> str` and `audit.py slug MODEL`: lowercase, every run of non `[a-z0-9]` → `-`, trimmed (`router-env/my-referee-one` → `router-env-my-referee-one`, `opus` → `opus`).
- `audit.py split-verdicts --judge MODEL --out DIR < judge_stdout` → writes each JSON line to `DIR/<slug(MODEL)>/<skill>.json`; non-JSON lines are reported on stderr and skipped; exit 0.

- [ ] **Step 1: Write failing tests** in `scripts/audit/test_audit.py` (tmp skill dirs, stubbed `run_skills_ref`):
  - `test_check_flags_over_500_lines`, `test_check_flags_non_latin`, `test_check_allowlist_suppresses`, `test_check_name_mismatch`, `test_check_flags_missing_evals`, `test_check_flags_missing_script_tests`, `test_check_script_tests_present_ok`.
  - `test_check_ignores_c5_fields` (stub `Unexpected fields in frontmatter: user-invocable.` → ok), `test_check_keeps_non_c5_unexpected_fields` (`version` → issue).
  - `test_check_strict_ignores_synced`, `test_check_ignore_flag`.
  - `test_rubric_check_ok`, `test_rubric_check_rejects_missing_dimension`, `test_rubric_check_rejects_stale_spec_sha`.
  - `test_slug`, `test_split_verdicts_writes_per_skill_files`, `test_split_verdicts_skips_non_json`.
- [ ] **Step 2: Run the tests to verify they fail**

  Run: `python3 -m unittest discover -s scripts/audit -v`
  Expected: FAIL (`audit` module missing).
- [ ] **Step 3: Implement `check_skills(skills, strict, ignore) -> dict`, `load_rubric`, `rubric_check`, `slug`, `split_verdicts`** and their argparse subcommands in `scripts/audit/audit.py`; seed `non_latin_allowlist.txt`.
- [ ] **Step 4: Run the tests to verify they pass**

  Run: `python3 -m unittest discover -s scripts/audit -v`
  Expected: PASS.
- [ ] **Step 5: Record the baseline for plan 4**

  Run: `python3 scripts/audit/audit.py check > docs/audit/baseline-check.json`
  Expected: `skills_ref` for 4 skills (`design-system-starter`, `humanizer`, `qa-test-planner`, `react-dev`); `lines_over_500` for 4 (`database-schema-designer` 687, `design-system-starter` 603, `mui` 504, `qa-test-planner` 757); `non_latin` for marp-slide (`SKILL.md`, `README.md`, `assets/template-*.md`, `assets/theme-*.css`) and draw-io (`scripts/find_aws_icon.py`, `references/aws-icons.md`); `missing_evals` for every non-synced skill except `skill-judge`; `missing_script_tests` for skills with `scripts/` and no tests.
- [ ] **Step 6: Commit**

  `git add scripts/audit docs/audit/baseline-check.json && git commit -m "feat(audit): add skill check, rubric check and verdict splitting"`.

### Task 4: `audit.py` — validate-verdict and merge

**Files:** Modify `scripts/audit/audit.py`, `scripts/audit/test_audit.py`.

**Interfaces:**
- Consumes: `load_rubric`, `slug`, `SYNCED`, `check` output (Task 3).
- `validate_verdict(data: dict, path: Path, rubric: dict) -> list[str]` and `audit.py validate-verdict [--rubric FILE] FILE...` (exit 1, one `FILE: reason` per problem). Valid only if: JSON with NaN/Infinity rejected; every key of the Task 2 shape; `scores`/`max` have exactly `D1`..`D8`; each `max[Dn]` equals the rubric; each score int in `0..max[Dn]`; `total`, `max_total`, `percent`, `grade` recomputed and equal; `rubric_version`/`spec_sha` equal the rubric; `skill`/`judge` equal the `<judge>/<skill>.json` path parts; findings have valid keys and `severity`.
- `audit.py merge --in DIR --out DIR --judges m1,m2 [--skills x,y] [--check FILE] [--waivers FILE] [--min-judges N] [--allow-incomplete] [--rubric FILE]`. `--judges` takes model IDs and slugs them; `--skills` defaults to every `skills/*/`; `--min-judges` defaults to 1. Writes `merged.json` `{"rubric_version","spec_sha","complete":bool,"skills":[{"name","percent":float|null,"grade":"A|B|C|D|F|UNJUDGED","judges":{slug:percent},"missing_judges":[…],"disagreement":bool,"synced":bool,"waived":bool,"skills_ref_valid":bool|null,"check_issues":[…],"findings":[…]}],"needs_update":bool}` and `report.md` (summary table, Disagreements, Missing verdicts, Below target, Waived, Synced). Rules: percent = mean of valid verdicts; no valid verdict → `UNJUDGED`; `disagreement` when percents differ by > 10; findings deduped on `(dimension, file, fix lowercased)`; synced findings excluded from the fix list; `skills_ref_valid`/`check_issues` copied from `--check` output; `waived` from `--waivers` (`[{"skill","percent","reason","date"}]`); `needs_update` = any non-synced, non-waived skill below 80, any critical/high finding, or any `check_issues` entry on a non-synced skill. Exit 2 when not `complete` unless `--allow-incomplete`.

- [ ] **Step 1: Write failing tests**:
  - Validation: `test_validate_accepts_valid`, `test_validate_rejects_non_json`, `test_validate_rejects_nan`, `test_validate_rejects_missing_dimension`, `test_validate_rejects_score_over_max`, `test_validate_rejects_inflated_max`, `test_validate_rejects_wrong_total`, `test_validate_rejects_wrong_percent_or_grade`, `test_validate_rejects_stale_rubric_version`, `test_validate_rejects_stale_spec_sha`, `test_validate_rejects_path_mismatch`.
  - Merge: `test_merge_means_and_disagreement` (92 and 78 → 85, `disagreement`), `test_merge_skips_invalid_verdict`, `test_merge_marks_synced_skills`, `test_merge_needs_update_on_high_finding`, `test_merge_reports_unjudged_skill`, `test_merge_lists_missing_judges`, `test_merge_exit2_when_below_min_judges`, `test_merge_allow_incomplete_exits_0`, `test_merge_subset_skills_complete` (`--skills a` with verdicts only for `a` → `complete`), `test_merge_judges_are_slugged`, `test_merge_copies_check_results`, `test_merge_waived_skill_not_needs_update`.
- [ ] **Step 2: Run the tests to verify they fail**

  Run: `python3 -m unittest discover -s scripts/audit -v`
  Expected: new tests FAIL, Task 3 tests PASS.
- [ ] **Step 3: Implement `validate_verdict`** and the `validate-verdict` subcommand.
- [ ] **Step 4: Implement `merge_verdicts(in_dir, out_dir, judges, skills, check, waivers, min_judges, allow_incomplete, rubric) -> int`** and the `merge` subcommand.
- [ ] **Step 5: Run the tests to verify they pass**

  Run: `python3 -m unittest discover -s scripts/audit -v`
  Expected: PASS.
- [ ] **Step 6: Commit**

  `git add scripts/audit && git commit -m "feat(audit): validate verdicts against the rubric and merge with coverage"`.

### Task 5: `audit.py run-evals`

**Files:** Modify `scripts/audit/audit.py`, `scripts/audit/test_audit.py`; create `scripts/audit/fixtures/stub-runner.sh`.

**Interfaces:**
- Runner contract: `--runner CMD` reads the full prompt on stdin, writes the answer to stdout, exits 0. `run-evals` resolves the runner's first word to an absolute path against the invocation cwd BEFORE changing directory, then runs it with cwd = a fresh temp sandbox holding a copy of the skill (`skills/<name>/`) and the eval's `files`. Prompts are prefixed with `SANDBOX_PREAMBLE` ("You have no tools, network or shell. Do not try to run anything; show the exact commands, calls and file contents you would use instead."). The local runner is `pi -p --no-tools --model router-env/my-referee-one`.
- `audit.py run-evals --skills a,b --runner CMD [--triggers] [--runs N] [--out DIR] [--fail-under 0.8]`:
  - Output mode (default): for each eval in `evals/evals.json` (`{skill_name, evals:[{id, prompt, expected_output, files, assertions}]}`): save `DIR/<s>/output/<id>/output.txt`; grade with a second runner call returning `{"results":[{"assertion","passed","evidence"}]}` saved as `grading.json`; write `DIR/<s>/summary-output.json`.
  - Trigger mode (`--triggers`, `--runs` default 3): for each `{query, should_trigger}` in `evals/trigger-queries.json`, ask the runner `N` times to pick from a catalog of every non-synced skill's `name` + `description` and return `{"skill":"<name>|none"}`; trigger rate = share of runs answering `<s>`; a query passes when `(rate >= 0.5) == should_trigger` (threshold per the fetched `optimizing-descriptions.md`); write `DIR/<s>/summary-triggers.json`.
  - Summary shape: `{"skill","mode","pass_rate","passed","total","failures":[…]}`; synced skills are skipped with `{"skill","skipped":"synced"}`; stdout = JSON list.
  - Exit 0 when every pass_rate ≥ `--fail-under`; 1 when any is below; 2 on harness errors (runner non-zero, invalid grader JSON, missing/invalid eval file for a non-synced skill).

- [ ] **Step 1: Write failing tests** with `stub-runner.sh` (canned answers keyed on prompt text): `test_run_evals_grades_assertions`, `test_run_evals_fail_under_exits_1`, `test_run_evals_harness_error_exits_2`, `test_run_evals_missing_file_exits_2`, `test_run_evals_runs_in_sandbox_cwd` (stub records `pwd` ≠ repo root, sees the copied skill), `test_run_evals_relative_runner_resolves`, `test_run_evals_output_and_triggers_keep_separate_summaries`, `test_run_evals_skips_synced`, `test_triggers_rate_over_runs`, `test_triggers_catalog_excludes_synced`.
- [ ] **Step 2: Run the tests to verify they fail**

  Run: `python3 -m unittest discover -s scripts/audit -v`
  Expected: new tests FAIL.
- [ ] **Step 3: Implement `run_evals(skills, runner, triggers, runs, out, fail_under) -> int`** and the subcommand.
- [ ] **Step 4: Run the tests to verify they pass**

  Run: `python3 -m unittest discover -s scripts/audit -v`
  Expected: PASS.
- [ ] **Step 5: Commit**

  `git add scripts/audit && git commit -m "feat(audit): add sandboxed runner for output and trigger evals"`.

### Task 6: Judge the two skills this plan ships

**Files:** Create `docs/audit/<yyyy-mm-dd>-plan2/{judgements/,merged.json,report.md,evals/}`.

- [ ] **Step 1: Judge with both local judges.** Opus: a Claude Code subagent (`model: opus`) given `judge-prompt.md` with `{JUDGE}=opus`, `{SKILLS}=agentskills-research,skill-judge`; pipe its answer to `python3 scripts/audit/audit.py split-verdicts --judge opus --out docs/audit/<date>-plan2/judgements`. pi: `pi -p --tools read,grep,find,ls --model router-env/my-referee-one "<filled judge-prompt.md>" | python3 scripts/audit/audit.py split-verdicts --judge router-env/my-referee-one --out docs/audit/<date>-plan2/judgements`.
- [ ] **Step 2: Validate, check and merge**

  Run: `python3 scripts/audit/audit.py check --skills agentskills-research,skill-judge > /tmp/check.json && python3 scripts/audit/audit.py merge --in docs/audit/<date>-plan2/judgements --out docs/audit/<date>-plan2 --judges opus,router-env/my-referee-one --skills agentskills-research,skill-judge --check /tmp/check.json`
  Expected: exit 0, both skills grade ≥ B. Below B → fix and re-run (max 2 rounds), then present to the user.
- [ ] **Step 3: Run their evals**

  Run: `python3 scripts/audit/audit.py run-evals --skills agentskills-research,skill-judge --runner "pi -p --no-tools --model router-env/my-referee-one" --out docs/audit/<date>-plan2/evals` and again with `--triggers`.
  Expected: exit 0.
- [ ] **Step 4: Commit and open the PR**

  `git add docs/audit && git commit -m "docs(audit): judge agentskills-research and skill-judge"`; open the PR with `/explain-pr-changes`.
