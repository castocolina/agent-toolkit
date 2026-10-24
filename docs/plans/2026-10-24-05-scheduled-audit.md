# Plan 5 — Scheduled Audit Workflow

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every ~15 days GitHub Actions refreshes the Agent Skills spec and the rubric, judges the skills that changed with several Copilot models, merges the verdicts, re-checks upstream sources, and — only when something needs updating — opens a fix PR whose merge mode is a repo knob.

**Architecture:** One scheduled workflow with LLM-free gating (`detect`) in front of Copilot jobs, all reusing `scripts/audit/audit.py` and the skills from plans 2-4; a second workflow gates `agent` merges on a Copilot review of the current head. State advances only after a durable outcome.

**Tech Stack:** GitHub Actions, GitHub Copilot CLI (`copilot -p`), pi (GLM 5.3 Flash fixer), `gh`, `uv`, `actionlint`.

**Spec:** [Roadmap](2026-10-24-00-roadmap.md) — Decisions 4, 5, 6, 8, 9, 11; planner calls C6, C7, C9; Global Constraints apply.

Branch: `feat/<yy-mm-dd>-scheduled-skill-audit`. Depends on plans 2, 3 and 4.

## Review Focus

1. Scheduled run with no spec change and no skill change → zero Copilot calls. Pinned in Task 2.
2. A run that judges only the changed skills → merge is scoped to them and can complete. Pinned in Task 3 job 4.
3. A run fails after research → `AUDIT_LAST_STATE` untouched, the next run retries. Pinned in Task 3 job 7 and Step 8.
4. An audit PR is closed without merging after a spec change → the next run still sees the spec as changed (comparison is against the committed references, not stored state). Pinned in Task 2.
5. Required status checks are enabled for `auto`/`agent` → the existing direct-push bots (`auto-bump`, `sync-*`) keep working. Pinned in Task 1 Step 5.

---

### Task 1: Spike — Copilot CLI, pi and repo settings in Actions

Results go to `docs/audit/ci-spike.md`, which Task 3 consumes. `workflow_dispatch` and `schedule` only run from the default branch, so the spike workflow uses a `push` trigger on its own branch.

- [ ] **Step 1: Smoke workflow.** `.github/workflows/copilot-smoke.yaml` with `on: push: branches: [spike/copilot-smoke]`. Install Copilot CLI (package name from GitHub docs), auth via secret `COPILOT_GITHUB_TOKEN` (fine-grained PAT, "Copilot Requests"), list models, run `copilot -p "Reply with OK" -s --no-ask-user --model=<each>`. Also confirm: passing a multi-KB prompt (`-p "$(</dev/stdin)"`), `--allow-tool` / `--deny-tool` syntax, and a no-tools mode for the eval runner.
- [ ] **Step 2: pi in Actions.** Same workflow: install pi; `pi -p --provider zai-coding-cn --model glm-5.3-flash "Reply with OK"`; record the install command and the provider secret name. If it cannot run, STOP and ask the user for a replacement fixer (Decision 9).
- [ ] **Step 3: Copilot review bot.** Record: reviewer handle for `gh pr edit --add-reviewer`, the bot login in `pull_request_review` events, that it only submits `COMMENTED`, its exact "nothing to report" body, and whether bot reviews trigger workflows without approval.
- [ ] **Step 4: Run the spike.** `git push origin HEAD:spike/copilot-smoke`; read the run log with `gh run view --log`; write `docs/audit/ci-spike.md`; delete the branch and the workflow file.
- [ ] **Step 5: Repo prerequisites for `auto|agent`** (skip if the user keeps `manual`). Check `gh api repos/{owner}/{repo} --jq .allow_auto_merge` and the `main` ruleset's required `CI` checks. Required checks would reject the direct pushes of `auto-bump.yaml`, `sync-gepetto.yaml`, `sync-datadog-cli.yaml`; present the options (ruleset bypass for the token those workflows use, or switching them to `AUDIT_BOT_TOKEN` with a bypass actor) and apply the user's choice; verify by dispatching `sync-gepetto.yaml` once.
- [ ] **Step 6: Choose models.** Present available models; the user picks; set repo variables `AUDIT_RESEARCH_MODELS`, `AUDIT_MERGER_MODEL`, `AUDIT_MERGE_MODE=manual`, `AUDIT_ENABLED=false`.

### Task 2: `audit.py` — detect, branch-name, validate-decision

**Files:** Modify `scripts/audit/audit.py`, `scripts/audit/test_audit.py`.

**Interfaces:**
- `audit.py detect --state JSON --spec-changed true|false [--force]` → `{"run_needed":bool,"spec_changed":bool,"skills":[names],"eval_skills":[names],"state":{"judge_sha","skills":{name: tree_sha}}}`. `--spec-changed` is `true` when `fetch-spec.sh` printed a non-empty `changed` (docs differ from the committed references). Tree sha = `git rev-parse HEAD:skills/<name>`; `judge_sha` = `git rev-parse HEAD:skills/skill-judge`. `skills` = changed skills, or all skills when `spec_changed`, `judge_sha` differs, the state is empty/invalid, or `--force`. `eval_skills` = `skills` minus `SYNCED`.
- `audit.py branch-name --type feat|fix --title TEXT [--date YY-MM-DD]` → e.g. `feat/26-10-24-refresh-skill-judge-rubric` (ASCII-folded, lowercase, `[a-z0-9-]`, slug ≤ 50 chars, UTC date default).
- `audit.py validate-decision FILE [--spec-changed]` → exit 1 with reasons unless `type` ∈ `feat|fix`, `title` non-empty, `update` bool, every target is `skill-judge` or an existing non-synced `skills/` dir, `targets` non-empty when `update`; with `--spec-changed`, `update` is true and `targets` includes `skill-judge`.

- [ ] **Step 1: Write failing tests** (temp git repo): `test_detect_no_change_no_run`, `test_detect_spec_change_runs_all`, `test_detect_judge_change_runs_all`, `test_detect_single_skill_change`, `test_detect_bad_state_runs_all`, `test_detect_force`, `test_detect_eval_skills_excludes_synced`, `test_branch_name_slug` (`"Refresh: skill-judge rubric ✨ für v2"` → `feat/26-10-24-refresh-skill-judge-rubric-fur-v2`), `test_branch_name_truncates`, `test_validate_decision_rejects_unknown_target`, `test_validate_decision_rejects_synced_target`, `test_validate_decision_spec_changed_requires_skill_judge`.
- [ ] **Step 2: Run the tests to verify they fail**

  Run: `python3 -m unittest discover -s scripts/audit -v`
  Expected: new tests FAIL.
- [ ] **Step 3: Implement `detect(state, spec_changed, force) -> dict`, `branch_name(type, title, date) -> str`, `validate_decision(data, spec_changed) -> list[str]`** and their subcommands.
- [ ] **Step 4: Run the tests to verify they pass**

  Run: `python3 -m unittest discover -s scripts/audit -v`
  Expected: PASS.
- [ ] **Step 5: Commit**

  `git add scripts/audit && git commit -m "feat(audit): detect changes, name branches, validate decisions"`.

### Task 3: Workflows, prompts and runner

**Files:**
- Create: `.github/workflows/skill-audit.yaml`, `.github/workflows/skill-audit-gate.yaml`
- Create: `.github/audit/{research,rubric,merge,fix}-prompt.md`, `.github/audit/copilot-runner.sh` (stdin prompt → `copilot -p "$(</dev/stdin)" -s --no-ask-user --model "$AUDIT_RUNNER_MODEL"` with the no-tools flags recorded in `ci-spike.md`)
- Modify: `README.md` ("Automated audits": knobs and the Task 1 Step 5 prerequisites)

Workflow-level `env`: `AUDIT_RUNNER_MODEL: ${{ vars.AUDIT_MERGER_MODEL }}`; every job that runs `audit.py check` installs `uv` (`astral-sh/setup-uv`). The schedule job runs only when `vars.AUDIT_ENABLED == 'true'`.

Jobs of `skill-audit.yaml` (LLM jobs download the named artifacts and overlay them onto their checkout):

1. `detect` (no LLM): if an open PR labeled `skill-audit` exists, stop (`run_needed=false`, state untouched). Else run `fetch-spec.sh` into the checkout; `spec_changed` = its `changed` is non-empty; `git diff -- skills/skill-judge/references/agentskills > spec.diff`; `audit.py detect --state "$AUDIT_LAST_STATE" --spec-changed <bool>`; `audit.py upstreams --registry docs/audit/upstream-sources.json > upstreams.json`; `audit.py check > check.json`. Outputs `run_needed`, `spec_changed`, `skills`, `eval_skills`, `state`. Artifact `spec` (references incl. `SOURCE.json`, `spec.diff`, `upstreams.json`, `check.json`).
2. `rubric` (if `spec_changed`): merger model via `copilot-runner.sh` with `rubric-prompt.md` (the `agentskills-research` workflow) updates `rubric.md`; `audit.py rubric-check` must exit 0. Artifact `rubric`.
3. `research` (matrix over `AUDIT_RESEARCH_MODELS`, `fail-fast: false`; `if: needs.detect.outputs.run_needed == 'true' && needs.rubric.result != 'failure'`): fill `judge-prompt.md` with `{JUDGE}=<model>` and `{SKILLS}=<skills>`; `copilot -p "$(<prompt)" -s --no-ask-user --model=<model> --allow-tool=read | audit.py split-verdicts --judge <model> --out verdicts`; `audit.py validate-verdict verdicts/<slug>/*.json`; on failure retry once, then upload whatever valid verdicts exist and end the leg red. Artifact `verdicts-<slug>`.
   `evals` (parallel): `audit.py run-evals --skills <eval_skills> --runner "$GITHUB_WORKSPACE/.github/audit/copilot-runner.sh" --out evals-out` and again with `--triggers`; exit 1 tolerated (evidence), exit 2 fails the job. Artifact `evals-results`.
4. `merge` (`if: always() && needs.detect.outputs.run_needed == 'true'`): `audit.py merge --in verdicts --out out --judges "$AUDIT_RESEARCH_MODELS" --skills <skills> --check check.json` (exit 2 = incomplete coverage fails the job); merger model reads `merged.json`, `spec.diff`, `upstreams.json`, `evals-results` → `decision.json` `{"update","type","title","targets","rationale"}`; `audit.py validate-decision decision.json [--spec-changed]` must pass. Artifact `decision`.
5. `apply` (if `update`): preflight the Task 1 Step 5 prerequisites when `AUDIT_MERGE_MODE` is `auto|agent`; overlay `spec` + `rubric`; branch via `audit.py branch-name`; fixer `pi -p --provider zai-coding-cn --model glm-5.3-flash` with `fix-prompt.md` applies `targets`; `audit.py check --strict`; `audit.py run-evals --skills <targets> --runner "$GITHUB_WORKSPACE/.github/audit/copilot-runner.sh" --fail-under 0.8` (failure aborts before the PR); `python3 scripts/build_plugins.py`; push with `AUDIT_BOT_TOKEN`; open the PR labeled `skill-audit`, body via `copilot -p` following `commands/explain-pr-changes.md --diagrams=${AUDIT_PR_DIAGRAMS:-mermaid}` (drawio + xvfb installed only for `drawio`).
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
| pi provider key (name from `ci-spike.md`) | secret | pi fixer access to GLM 5.3 Flash |
| `AUDIT_RESEARCH_MODELS` | variable | Comma list of Copilot model IDs (judges) |
| `AUDIT_MERGER_MODEL` | variable | Rubric refresh, decision, eval runner (`AUDIT_RUNNER_MODEL`) |
| `AUDIT_MERGE_MODE` | variable | `manual` (default) / `auto` / `agent` |
| `AUDIT_PR_DIAGRAMS` | variable | `none` / `mermaid` (default) / `drawio` |
| `AUDIT_ENABLED` | variable | `true` turns the schedule on (Task 3 Step 10) |
| `AUDIT_LAST_STATE` | variable | Written only by the `state` job (C6) |
