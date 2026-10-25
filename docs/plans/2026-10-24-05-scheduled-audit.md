# Plan 5 — Scheduled Audit Workflow

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every ~15 days GitHub Actions refreshes the Agent Skills spec and the rubric, judges the skills that changed with several Copilot models, merges the verdicts, re-checks upstream sources, and — only when something needs updating — opens a fix PR whose merge mode is a repo knob.

**Architecture:** One scheduled workflow with LLM-free gating (`detect`) in front of Copilot jobs, all reusing `scripts/audit/audit.py` and the skills from plans 2-4; a second workflow gates `agent` merges on a Copilot review of the current head. State advances only after a durable outcome.

**Tech Stack:** GitHub Actions, GitHub Copilot CLI (`copilot -p`), `gh`, `uv`, `actionlint`.

**Spec:** [Roadmap](2026-10-24-00-roadmap.md) — Decisions 4, 5, 6, 8, 9, 11, 18; planner calls C6, C7, C9; Global Constraints apply.

Branch: `feat/<yy-mm-dd>-scheduled-skill-audit`. Depends on plans 2, 3 and 4.

## Review Focus

1. Scheduled run with no spec change and no skill change → zero Copilot calls. Pinned in Task 2.
2. A run that judges only the changed skills → merge is scoped to them and can complete. Pinned in Task 3 job 4.
3. A run fails after research → `AUDIT_LAST_STATE` untouched, the next run retries. Pinned in Task 3 job 7 and Step 8.
4. An audit PR is closed without merging after a spec change → the next run still sees the spec as changed (comparison is against the committed references, not stored state). Pinned in Task 2.
5. Required status checks are enabled for `auto`/`agent` → the existing direct-push bots (`auto-bump`, `sync-*`) keep working. Pinned in Task 1 Step 5.
6. Upstream adds, removes or renames a skill-creation page, or renames/removes a heading the rubric cites → detected (`structure_changed`, or `rubric-check` failing on a broken `source` anchor), treated as a spec change, and the audit PR updates the research skill (file list, fixtures, tests) and the judge (rubric sources, criteria, eval file lists); never silently ignored. Pinned in Task 2a and Task 3 job 1.
7. An interrupted refresh (references committed, rubric not updated) → `rubric_stale` counts as a spec change, so the next run refreshes the rubric. Pinned in Task 2 (`--spec-changed` definition) and Task 3 job 1.

---

### Task 1: Spike — Copilot CLI, pi and repo settings in Actions

Results go to `docs/audit/ci-spike.md`, which Task 3 consumes. `workflow_dispatch` and `schedule` only run from the default branch, so the spike workflow uses a `push` trigger on its own branch.

- [ ] **Step 1: Smoke workflow.** `.github/workflows/copilot-smoke.yaml` with `on: push: branches: [spike/copilot-smoke]`. Install Copilot CLI (package name from GitHub docs), auth via secret `COPILOT_GITHUB_TOKEN` (fine-grained PAT, "Copilot Requests"), list models, run `copilot -p "Reply with OK" -s --no-ask-user --model=<each>`. Also confirm: passing a multi-KB prompt (`-p "$(</dev/stdin)"`), `--allow-tool` / `--deny-tool` syntax, and a no-tools mode for the eval runner.
- [ ] **Step 2: Copilot as fixer.** Same workflow: on a scratch file, `copilot -p "Append the line OK to scratch.txt" -s --no-ask-user --model=<merger model> --allow-tool=read,write` must edit the file and nothing else; record the exact flags. The fixer in Actions is a Copilot model (roadmap Decision 9); if Copilot cannot edit files non-interactively, STOP and ask the user.
- [ ] **Step 3: Copilot review bot.** Record: reviewer handle for `gh pr edit --add-reviewer`, the bot login in `pull_request_review` events, that it only submits `COMMENTED`, its exact "nothing to report" body, and whether bot reviews trigger workflows without approval.
- [ ] **Step 4: Run the spike.** `git push origin HEAD:spike/copilot-smoke`; read the run log with `gh run view --log`; write `docs/audit/ci-spike.md`; delete the branch and the workflow file.
- [ ] **Step 5: Repo prerequisites for `auto|agent`** (skip if the user keeps `manual`). Check `gh api repos/{owner}/{repo} --jq .allow_auto_merge` and the `main` ruleset's required `CI` checks. Required checks would reject the direct pushes of `auto-bump.yaml`, `sync-gepetto.yaml`, `sync-datadog-cli.yaml`; present the options (ruleset bypass for the token those workflows use, or switching them to `AUDIT_BOT_TOKEN` with a bypass actor) and apply the user's choice; verify by dispatching `sync-gepetto.yaml` once.
- [ ] **Step 6: Choose models.** Present available models; the user picks; set repo variables `AUDIT_RESEARCH_MODELS`, `AUDIT_MERGER_MODEL`, `AUDIT_MERGE_MODE=manual`, `AUDIT_ENABLED=false`.

### Task 2: `audit.py` — detect, branch-name, validate-decision

**Files:** Modify `scripts/audit/audit.py`, `tests/audit/test_audit.py`.

**Interfaces:**
- `audit.py detect --state JSON --spec-changed true|false [--force]` → `{"run_needed":bool,"spec_changed":bool,"skills":[names],"eval_skills":[names],"state":{"judge_sha","skills":{name: tree_sha}}}`. `--spec-changed` is `true` when `fetch-spec.sh` printed a non-empty `changed` (docs differ from the committed references), `rubric_stale: true`, or `structure_changed: true` (Task 2a). Tree sha = `git rev-parse HEAD:skills/<name>`; `judge_sha` = `git rev-parse HEAD:skills/skill-judge`. `skills` = changed skills, or all skills when `spec_changed`, `judge_sha` differs, the state is empty/invalid, or `--force`. `eval_skills` = `skills` minus `SYNCED`.
- `audit.py branch-name --type feat|fix --title TEXT [--date YY-MM-DD]` → e.g. `feat/26-10-24-refresh-skill-judge-rubric` (ASCII-folded, lowercase, `[a-z0-9-]`, slug ≤ 50 chars, UTC date default).
- `audit.py validate-decision FILE [--spec-changed] [--structure-changed]` → exit 1 with reasons unless `type` ∈ `feat|fix`, `title` non-empty, `update` bool, every target is `skill-judge` or an existing non-synced `skills/` dir, `targets` non-empty when `update`; with `--spec-changed`, `update` is true and `targets` includes `skill-judge`; with `--structure-changed`, `update` is true and `targets` includes both `agentskills-research` and `skill-judge` (the fetcher's file list and the rubric must both change).

- [ ] **Step 1: Write failing tests** (temp git repo): `test_detect_no_change_no_run`, `test_detect_spec_change_runs_all`, `test_detect_judge_change_runs_all`, `test_detect_single_skill_change`, `test_detect_bad_state_runs_all`, `test_detect_force`, `test_detect_eval_skills_excludes_synced`, `test_branch_name_slug` (`"Refresh: skill-judge rubric ✨ für v2"` → `feat/26-10-24-refresh-skill-judge-rubric-fur-v2`), `test_branch_name_truncates`, `test_validate_decision_rejects_unknown_target`, `test_validate_decision_rejects_synced_target`, `test_validate_decision_spec_changed_requires_skill_judge`, `test_validate_decision_structure_changed_requires_research_and_judge`.
- [ ] **Step 2: Run the tests to verify they fail**

  Run: `python3 -m unittest discover -s tests/audit -v`
  Expected: new tests FAIL.
- [ ] **Step 3: Implement `detect(state, spec_changed, force) -> dict`, `branch_name(type, title, date) -> str`, `validate_decision(data, spec_changed) -> list[str]`** and their subcommands.
- [ ] **Step 4: Run the tests to verify they pass**

  Run: `python3 -m unittest discover -s tests/audit -v`
  Expected: PASS.
- [ ] **Step 5: Commit**

  `git add scripts/audit tests/audit && git commit -m "feat(audit): detect changes, name branches, validate decisions"`.

### Task 2a: Upstream structure drift (roadmap Decision 18)

Today `fetch-spec.sh` tracks a hardcoded list of 7 upstream files (plan 2 Task 1): a page upstream adds is never noticed, a removed or renamed page only fails the fetch (exit 1) with no recovery path, and a renamed heading silently breaks the rubric's `source` anchors (`rubric-check` does not verify them). The agentskills.io navigation is `docs/docs.json` in `agentskills/agentskills`; this task makes the fetcher and the checker detect structural drift so the audit PR can update the research skill and the judge.

**Files:** Modify `skills/agentskills-research/scripts/fetch-spec.sh`, `tests/skills/agentskills-research/test-fetch-spec.sh`, its fixtures in `tests/skills/agentskills-research/fixtures/` (add `docs/docs.json` to `tests/skills/agentskills-research/fixtures/upstream/`; SHA dirs are created at run time), `skills/agentskills-research/{SKILL.md,README.md}`, `scripts/audit/audit.py`, `tests/audit/test_audit.py`; create (first real run) `skills/skill-judge/references/agentskills/docs-navigation.json.txt` and its `SOURCE.json` entry.

**Interfaces:**
- Consumes: plan 2's `fetch-spec.sh` contract (stdout JSON, publish/rollback, `SOURCE.json`), `audit.py rubric-check`, `load_rubric`.
- `fetch-spec.sh` downloads `docs/docs.json` first and tracks it as an 8th file, `docs-navigation.json.txt` (first line `# Source: https://github.com/agentskills/agentskills (CC-BY-4.0), verbatim copy, see SOURCE.json`, then a blank line). In-scope pages = every navigation page path (pages are strings or nested `{group, pages}` objects, at any depth) equal to `specification` or starting with `skill-creation/`; other pages (`home`, `clients`, `client-implementation/*`) are out of scope and ignored. Stdout gains `"structure_changed":bool,"new_pages":[page paths],"removed_pages":[page paths]`: `new_pages` = in-scope pages with no entry in the source map, `removed_pages` = mapped doc pages (not the validator) absent from the in-scope set. A removed page is not downloaded (no 404 abort); its committed copy is kept until the research skill drops it from the source map, so rubric citations stay readable during the update. `docs.json` failing to download or parse is a fetch failure (exit 1, nothing published).
- `audit.py rubric-check` additionally verifies every `source` anchor: for each `references/agentskills/<file>.md#<anchor>` the file exists under the rubric's directory and `<anchor>` equals the GitHub-style slug (lowercase; drop characters other than letters, digits, spaces and `-`; spaces → `-`) of one of that file's Markdown headings; each broken anchor prints one `broken source anchor: <source>` line and the command exits 1.
- `agentskills-research` `SKILL.md` gains a section "When upstream structure changes", run when `structure_changed` is true or `rubric-check` reports a broken anchor: add or remove the page in `fetch-spec.sh`'s source map (and its test fixtures and tests), add or delete the reference copy, re-map every affected rubric `source`, review the rubric criteria a new page adds or a removed page took away, bump `rubric_version`, keep `skill-judge`'s eval `files` lists in sync with the sources the rubric cites (plan 2 Task 2 Step 6 invariant), and finish with `rubric-check` and `test-fetch-spec.sh` passing. All of it lands in the audit PR.

- [ ] **Step 1: Write failing tests.** In `test-fetch-spec.sh` (fixtures copied to `mktemp -d`, as in plan 2): `test_docs_json_tracked` (first run → `docs-navigation.json.txt` exists with the header, `structure_changed == false`), `test_new_nav_page_reported` (a copy of the SHA fixture whose `docs.json` adds `skill-creation/new-guide` → `structure_changed == true`, `new_pages == ["skill-creation/new-guide"]`, exit 0), `test_removed_nav_page_reported_and_kept` (`docs.json` without `skill-creation/using-scripts` → `removed_pages == ["skill-creation/using-scripts"]`, exit 0, the committed `using-scripts.md` unchanged), `test_out_of_scope_nav_page_ignored` (adds `client-implementation/other` → `structure_changed == false`), `test_bad_docs_json_exits_1` (invalid JSON → exit 1, dest unchanged). In `test_audit.py`: `test_rubric_check_accepts_slug_anchor`, `test_rubric_check_rejects_broken_anchor` (heading renamed → exit 1 naming the source), `test_rubric_check_rejects_missing_reference_file`.
- [ ] **Step 2: Run the tests to verify they fail**

  Run: `bash tests/skills/agentskills-research/test-fetch-spec.sh; python3 -m unittest discover -s tests/audit -v`
  Expected: the new tests FAIL, existing tests PASS.
- [ ] **Step 3: Implement** the `docs.json` tracking and structure fields in `fetch-spec.sh` (parse with `jq`, recursive over `pages`), and `check_source_anchors(rubric_path, ref_dir) -> list[str]` called by `rubric_check`; write the `SKILL.md` section and a matching README line.
- [ ] **Step 4: Run the tests to verify they pass**

  Run: `bash tests/skills/agentskills-research/test-fetch-spec.sh && python3 -m unittest discover -s tests/audit -v`
  Expected: PASS.
- [ ] **Step 5: Real run**

  Run: `bash skills/agentskills-research/scripts/fetch-spec.sh && python3 scripts/audit/audit.py rubric-check`
  Expected: `structure_changed: false` against today's upstream (its in-scope pages are exactly the six tracked docs), `changed` lists only `docs-navigation.json.txt`, and `rubric-check` exits 0 (every current anchor resolves). Any broken anchor found here is a real defect: fix the rubric's `source` in this task.
- [ ] **Step 6: Commit**

  `python3 scripts/build_plugins.py`; stage `dist/`, the skill, the new reference and `SOURCE.json`, `scripts/audit`, `tests/audit`, `tests/skills/agentskills-research`; `git commit -m "feat(agentskills-research): detect upstream structure drift"`.

### Task 3: Workflows, prompts and runner

**Files:**
- Create: `.github/workflows/skill-audit.yaml`, `.github/workflows/skill-audit-gate.yaml`
- Create: `.github/audit/{research,rubric,merge,fix}-prompt.md`, `.github/audit/copilot-runner.sh` (stdin prompt → `copilot -p "$(</dev/stdin)" -s --no-ask-user --model "$AUDIT_RUNNER_MODEL"` with the no-tools flags recorded in `ci-spike.md`)
- Modify: `README.md` ("Automated audits": knobs and the Task 1 Step 5 prerequisites)

Workflow-level `env`: `AUDIT_RUNNER_MODEL: ${{ vars.AUDIT_MERGER_MODEL }}`; every job that runs `audit.py check` installs `uv` (`astral-sh/setup-uv`). The schedule job runs only when `vars.AUDIT_ENABLED == 'true'`.

Jobs of `skill-audit.yaml` (LLM jobs download the named artifacts and overlay them onto their checkout):

1. `detect` (no LLM): if an open PR labeled `skill-audit` exists, stop (`run_needed=false`, state untouched). Else run `fetch-spec.sh` into the checkout; `spec_changed` = its `changed` is non-empty OR `rubric_stale` is true OR `structure_changed` is true; `structure_changed` is also an output (it adds `--structure-changed` to job 4's `validate-decision` and makes the `rubric` job follow the research skill's "When upstream structure changes" section); `git diff -- skills/skill-judge/references/agentskills > spec.diff`; `audit.py detect --state "$AUDIT_LAST_STATE" --spec-changed <bool>`; `audit.py upstreams --registry docs/audit/upstream-sources.json > upstreams.json`; `audit.py check > check.json`. Outputs `run_needed`, `spec_changed`, `skills`, `eval_skills`, `state`. Artifact `spec` (references incl. `SOURCE.json`, `spec.diff`, `upstreams.json`, `check.json`).
2. `rubric` (if `spec_changed`): merger model via `copilot-runner.sh` with `rubric-prompt.md` (the `agentskills-research` workflow) updates `rubric.md`; `audit.py rubric-check` must exit 0. Artifact `rubric`.
3. `research` (matrix over `AUDIT_RESEARCH_MODELS`, `fail-fast: false`; `if: needs.detect.outputs.run_needed == 'true' && needs.rubric.result != 'failure'`): fill `judge-prompt.md` with `{ROOT}=$GITHUB_WORKSPACE`, `{JUDGE}=$(python3 scripts/audit/audit.py slug <model>)` and `{SKILLS}=<skills>` (`split-verdicts --judge <model>` and `verdicts-<slug>` below already slug the same value); `copilot -p "$(<prompt)" -s --no-ask-user --model=<model> --allow-tool=read | audit.py split-verdicts --judge <model> --out verdicts`; `audit.py validate-verdict verdicts/<slug>/*.json`; on failure retry once, then upload whatever valid verdicts exist and end the leg red. Artifact `verdicts-<slug>`.
   `evals` (parallel): `audit.py run-evals --skills <eval_skills> --runner "$GITHUB_WORKSPACE/.github/audit/copilot-runner.sh" --out evals-out` and again with `--triggers`; exit 1 tolerated (evidence), exit 2 fails the job. Artifact `evals-results`.
4. `merge` (`if: always() && needs.detect.outputs.run_needed == 'true'`): `audit.py merge --in verdicts --out out --judges "$AUDIT_RESEARCH_MODELS" --skills <skills> --check check.json` (exit 2 = incomplete coverage fails the job); merger model reads `merged.json`, `spec.diff`, `upstreams.json`, `evals-results` → `decision.json` `{"update","type","title","targets","rationale"}`; `audit.py validate-decision decision.json [--spec-changed] [--structure-changed]` must pass. Artifact `decision`.
5. `apply` (if `update`): preflight the Task 1 Step 5 prerequisites when `AUDIT_MERGE_MODE` is `auto|agent`; overlay `spec` + `rubric`; branch via `audit.py branch-name`; fixer `copilot -p "$(<.github/audit/fix-prompt.md)" -s --no-ask-user --model=$AUDIT_MERGER_MODEL` with the write-tool flags recorded in `ci-spike.md` applies `targets`; `audit.py check --strict`; `audit.py run-evals --skills <targets> --runner "$GITHUB_WORKSPACE/.github/audit/copilot-runner.sh" --fail-under 0.8` (failure aborts before the PR); `python3 scripts/build_plugins.py`; push with `AUDIT_BOT_TOKEN`; open the PR labeled `skill-audit`, body via `copilot -p` following `commands/explain-pr-changes.md --diagrams=${AUDIT_PR_DIAGRAMS:-mermaid}` (drawio + xvfb installed only for `drawio`).
6. `merge-knob` (after `apply`, using `AUDIT_BOT_TOKEN`): `manual` → nothing; `auto` → `gh pr merge --auto --squash`; `agent` → request Copilot review. `skill-audit-gate.yaml` (`pull_request_review: submitted`, `AUDIT_BOT_TOKEN`) acts only if the PR has label `skill-audit` and head `^(feat|fix)/`, `review.user.login` is the bot login from `ci-spike.md`, `review.commit_id == pull_request.head.sha`, and `review.state == COMMENTED`; it enables auto-merge only with zero inline comments AND a body that is empty or exactly the recorded "nothing to report" text; anything else → label `needs-human`.
7. `state` (`needs: [detect, merge, apply]`, `if: always() && needs.detect.outputs.run_needed == 'true'`): `gh variable set AUDIT_LAST_STATE` with `detect`'s `state` ONLY when `merge` succeeded AND `apply` succeeded or was skipped because `update` is false. Otherwise untouched.

- Schedule `0 6 1,16 * *` plus `workflow_dispatch` inputs `force` (bool) and `merge_mode`.
- Publishing = merging the PR; `auto-bump.yaml` bumps the version and rebuilds `dist/`.

- [ ] **Step 1: Write the four prompt files and `copilot-runner.sh`** (each prompt names its exact output and JSON shape; research and rubric prompts say "copy `rubric_version`, `spec_sha` and every `max` from `rubric.md`").
- [ ] **Step 2: Write `.github/workflows/skill-audit.yaml`** implementing jobs 1-7 with the `needs`/`if` conditions above.
- [ ] **Step 3: Write `.github/workflows/skill-audit-gate.yaml`** implementing the job 6 conditions.
- [ ] **Step 4: Lint**

  Run: `actionlint .github/workflows/skill-audit.yaml .github/workflows/skill-audit-gate.yaml` (actionlint via its official download script).
  Expected: 0 errors.
- [ ] **Step 5: Land on `main` disabled.** Open the PR with `/explain-pr-changes`; after merge, `AUDIT_ENABLED` is still `false`, so the schedule does nothing.
- [ ] **Step 6: Forced run** on `main`: `gh workflow run skill-audit.yaml -f force=true -f merge_mode=manual`.
  Expected: a `skill-audit` PR on `feat|fix/<yy-mm-dd>-…` whose CI runs, or a validated "no update" decision and an updated `AUDIT_LAST_STATE`.
- [ ] **Step 7: Unchanged run.** Close or merge that PR, then dispatch without `force`.
  Expected: with nothing changed since, `detect` stops with `run_needed=false` and zero Copilot calls (a merged PR's skills are re-judged once, by design); while a `skill-audit` PR is open, `detect` stops and the state is untouched.
- [ ] **Step 8: Failure drill.** Dispatch `force=true` with a temporary invalid entry in `AUDIT_RESEARCH_MODELS`.
  Expected: that research leg red, `merge` runs and exits 2, `state` does not update. Restore the variable.
- [ ] **Step 9: Gate drill** (only if `agent` mode is wanted): on a scratch `skill-audit` PR, a review of an old head SHA does not enable auto-merge; one with inline comments labels `needs-human`.
- [ ] **Step 10: Enable.** With the user's go-ahead set `AUDIT_ENABLED=true`.

## Required secrets and variables

| Name | Kind | Purpose |
|---|---|---|
| `COPILOT_GITHUB_TOKEN` | secret | Fine-grained PAT with "Copilot Requests" |
| `AUDIT_BOT_TOKEN` | secret | Fine-grained PAT: contents, pull-requests, variables write (its events trigger CI and auto-bump) |
| `AUDIT_RESEARCH_MODELS` | variable | Comma list of Copilot model IDs (judges) |
| `AUDIT_MERGER_MODEL` | variable | Rubric refresh, decision, eval runner (`AUDIT_RUNNER_MODEL`) |
| `AUDIT_MERGE_MODE` | variable | `manual` (default) / `auto` / `agent` |
| `AUDIT_PR_DIAGRAMS` | variable | `none` / `mermaid` (default) / `drawio` |
| `AUDIT_ENABLED` | variable | `true` turns the schedule on (Task 3 Step 10) |
| `AUDIT_LAST_STATE` | variable | Written only by the `state` job (C6) |
