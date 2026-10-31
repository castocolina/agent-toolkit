# Plan 11 — Scheduled Audit Phase 2 (spike, scope cuts, triage)

Status: DRAFT, split out of the first plans PR. Not spec-reviewed. Re-run /ai-kit-spec-review after plan 5 (PR #8) merges. Open review findings: tmp/docs/spec-review-iter7-report.md (main checkout, untracked) and the handoff.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run the Copilot spike, turn plan 5's Phase 2 (tasks B1-B5 and ten open issues) into a smaller, executable Phase 2, and implement it, so the scheduled audit can be switched on.

**Architecture:** Phase 1 (PR #8) already gates, judges, opens fix PRs and reviews them. Phase 2 adds only what needs a model decision between steps: spec-change triage and model recording (upstream triage, issue only, is Phase 1's `upstream-report` as it stands). It stays keyless: no jev key, no automerge, no skill install on secret-bearing runners. Those are cut here and can return as a later plan. Task 3's Interfaces block is the Phase 2 spec; plan 5's Phase 2 text stays only as the record of the jev design.

**Tech Stack:** GitHub Actions, Copilot CLI, `scripts/audit/audit.py`, `.github/audit/*`.

**Spec:** [Plan 5](2026-10-24-05-scheduled-audit.md) Phase 2 and its open issues; [next roadmap](2026-10-30-00-roadmap-next.md). Roadmap Global Constraints apply.

Branch: `feat/<yy-mm-dd>-audit-phase2`, stacked on plan 5 (PR #8). Blocked until the user sets `COPILOT_GITHUB_TOKEN` and `AUDIT_BOT_TOKEN` (instructions: `tmp/docs/tokens-setup.md` in the main checkout).

## Global Constraints

- Phase 1 guarantees stay: keyless gates that run no PR code, trusted tooling copies, step-scoped tokens, state written only by `attempt`, `checkpoint` and `state`.
- No step may hold both a model with a network tool and any secret other than the Copilot token.
- `AUDIT_ENABLED` is switched on by the user's go-ahead, last.

## Scope decision (needs the user's yes before Task 2)

| Plan 5 Phase 2 item | Recommendation | Why |
|---|---|---|
| jev decisions, `JEV_API_KEY`, skill install (open issue 1) | **Cut.** Decisions are made by the agent; the keyless path is already the fail-safe | Removes the HIGH key-isolation and install risks |
| Automerge and required check `skill-audit/review` (issue 2) | **Cut.** Phase 1 already accepts `AUDIT_AUTOMERGE` without acting on it | A bypass actor defeats the required status; needs its own design |
| `re_review=no` (issue 5) | **Cut.** Phase 1 keeps its rule: a spec change re-judges every non-synced skill (`detect()` `full`, pinned by `test_detect_spec_change_runs_all`) | The user approves that cost, bounded by the interval gate; no executable opt-out path today |
| Upstream `pr` mode (issue 6) | **Cut.** `AUDIT_UPSTREAM_ACTION=issue` only (roadmap Decision 11) | Needs a post-triage job and DAG changes |
| `family:<name>` model resolution (issue 7) | **Cut to** explicit IDs or `auto`, recorded in the PR | Matches Phase 1 knob |
| B3 spec triage, B4 upstream triage (issue only), B2 minimal model recording, B1 agent-only decision protocol | **Keep**, as Task 3 Interfaces specifies them | The remaining value of Phase 2 |
| Owner sign-off on the fetch-script deviation (issue 3, 10) | Needs one line from the user | Cheap model stays keyless; a script fetches evidence and triage sees only validated enums |

If the user declines a cut, that item returns as its own plan with the open issue resolved first.

## Review Focus

1. A triage answer injects text into a later step → the spec triage answer is the closed enum checked by `audit.py validate-triage`, its evidence is whitelisted (Task 3 Interfaces, B1), and free text never reaches the fixer prompt. Pinned in Task 3.
2. `rubric_stale` blocks every `ignore` (issue 4) → two booleans (Task 3 Interfaces, B3): `spec_changed_this_run` and `rubric_incomplete`. Triage runs only when `rubric_incomplete` and `structure_changed` are both false, so only those two override `ignore`; a failing `rubric-check` fails the `rubric` job, which blocks `merge` and needs no override. Pinned in Task 3.
3. A triage failure advances state → it fails the run without touching state (Phase 1 rule). Pinned in Task 3.
4. A skipped decision point is silent → one failure rule for every decision point (issue 8): a model error, an invalid enum or a timeout fails the job, so the run fails without touching state (Focus 3), never "no change". Ruling: a failed run, because it is Phase 1's tested fail-safe path (an invalid `recommendations.json` already fails `upstream-report`) and the next due run retries; a failed triage has no PR to label `needs-human`. Pinned in Task 3.
5. The spike result contradicts an assumption → Task 1 records it, and Task 2 re-reads this table before editing anything.

---

### Task 1: Run the spike (needs the tokens)

**Files:** Create `.github/workflows/copilot-smoke.yaml` (temporary), `docs/audit/ci-spike.md` (extend).

- [ ] **Step 1:** Confirm `gh secret list -R castocolina/agent-toolkit` shows `COPILOT_GITHUB_TOKEN` and `AUDIT_BOT_TOKEN`; if not, stop and point the user to `tmp/docs/tokens-setup.md`.
- [ ] **Step 2:** Execute plan 5 Task 1 Steps 1, 2 and 4, Step 3 for the reviewer-bot facts only (its `skill-audit-gate.yaml` schedule consequence is superseded), and the containment drill of plan 5 Task A3 Step 2: smoke workflow on branch `spike/copilot-smoke`, model list, a several-KB prompt on stdin, `--allow-tool` / `--deny-tool` syntax, a no-tools mode (the exact flags, which Task 3's `copilot-decide.sh` uses), write confinement, reviewer bot behavior, and whether `--usage-output-file` names the model behind `auto`. Record every answer in `docs/audit/ci-spike.md`; replace each UNVERIFIED mark with the observed result or leave it. No no-tools mode: stop and report (Task 3's decision step needs one).
- [ ] **Step 3:** Delete the spike branch and the workflow file; confirm with `git ls-remote --heads origin spike/*`.
- [ ] **Step 4:** Update the reviewer wrapper and README where the spike changed a tool name (`copilot-review.sh`), with tests first. Commit `docs(audit): record the Copilot spike` and `fix(audit): align the reviewer wrapper with the spike`.
- [ ] **Step 5 (user gate):** present the observed model list; the user picks `AUDIT_RESEARCH_MODELS`, `AUDIT_MERGER_MODEL` and optionally `AUDIT_REVIEW_MODEL`, and states the account's monthly Copilot premium-request allowance (Task 4 Step 1 checks the first run against it); set the models with `gh variable set`.

### Task 2: Mark plan 5 Phase 2 as superseded

**Files:** Modify `docs/plans/2026-10-24-05-scheduled-audit.md` (Phase 2 status paragraph, open issues, required secrets).

- [ ] **Step 1:** After the user's yes on the scope table, replace the `Status:` paragraph under plan 5's `## Phase 2` with one paragraph: Phase 2 is re-specified, keyless, by plan 11; plan 11 Task 3 Interfaces is the spec that gets implemented; Tasks B1-B5, the design resolutions and the Phase 2 Review Focus additions stay below unchanged as the record of the jev design and are not implemented. Mark each open issue in one line: 1, 2, 5, 6 and 7 `cut (plan 11 scope table)`; 3 and 10 `owner sign-off: <the user's line>` (issue 10's knobs are cut); 4, 8 and 9 `resolved: plan 11 Task 3`. In `## Required secrets and variables` mark the `JEV_API_KEY` row `cut (plan 11)`. Ruling: mark, not delete, because the spec now lives in plan 11 Task 3, so no edit to plan 5 can strand text Task 3 needs.
- [ ] **Step 2:** Run `/ai-kit-spec-review` on the amended plan (two lanes, one is enough) until approved. Commit `docs(plan): reduce Phase 2 to the keyless decision protocol`.

### Task 3: Implement the keyless Phase 2

**Files:** Modify `scripts/audit/audit.py` (`validate-triage`, `spec-ignored`), `.github/audit/write-state.sh`, `.github/workflows/skill-audit.yaml`, `tests/audit/test_audit.py`, `tests/audit/test-workflow.sh` (`expected_jobs` gains `triage`), the `write-state.sh` stub-`gh` tests; create `.github/audit/{decision-evidence.py,copilot-decide.sh,triage-prompt.md}`, `tests/audit/{test_decision_evidence.py,test-copilot-decide.sh}`.

**Interfaces** (the Phase 2 spec, defined only here; plan 9 points to it):
- **B1 decision step.** `decision-evidence.py --fetch-result FILE --spec-diff FILE` prints one JSON object with exactly `changed` (file names), `new_pages`, `removed_pages` (page slugs), `structure_changed` (boolean) and `lines` (`{file: [added, removed]}` counted from the diff); every string matches `^[A-Za-z0-9./-]{1,128}$` (no `_`, so no GitHub token prefix such as `ghp_` or `github_pat_` passes) and the output fits 2 KB, else exit 2 with nothing on stdout. `copilot-decide.sh PROMPT EVIDENCE` runs `copilot -p` on PROMPT's text followed by the evidence, with `-s --no-ask-user --model "$AUDIT_MERGER_MODEL"` and the no-tools flags `docs/audit/ci-spike.md` records (never `--allow-tool`), under `env -i` keeping only `PATH`, `HOME` and `COPILOT_GITHUB_TOKEN`, and prints the answer. `triage-prompt.md` asks one question, whether this spec change needs a rubric update, and requires exactly `{"rubric": "update-rubric"}` or `{"rubric": "ignore"}`. `audit.py validate-triage FILE` exits 0 for exactly one of those two objects, else 1. Ruling: no decision trail and no `{{DECISION_PROTOCOL}}` placeholder, because both exist only to record jev calls (cut); the cheap role is `AUDIT_MERGER_MODEL`, so no new knob.
- **B3 `detect` outputs**, replacing Phase 1's `spec_changed` (`structure_changed` stays): `spec_sha` = the fetch result's `sha`; `rubric_incomplete` = the committed pin (`git show HEAD:skills/skill-judge/references/agentskills/SOURCE.json`, key `sha`) differs from the committed `rubric.md` `spec_sha` (not the fetch's `rubric_stale`, true on every ordinary change); `spec_changed_this_run` = the fetch result's `changed` list is non-empty and `audit.py spec-ignored` prints `false`. `audit.py spec-ignored --state JSON --sha SHA [--now ISO]` prints `true` only when `state.ignored` is `{spec_sha: SHA, until: YYYY-MM-DD}` with `until` on or after the UTC date of `--now` (default: now), else `false`. `audit.py detect --spec-changed` gets the unpublished `spec_changed_this_run OR rubric_incomplete OR structure_changed`, Phase 1's value except under an active ignore (`test_detect_spec_change_runs_all` stays green).
- **B3 `triage` job** (`needs: [detect, attempt]`; `if`: `upstream-report`'s guard with its `upstream_new != '[]'` term replaced by `spec_changed_this_run == 'true' && rubric_incomplete == 'false' && structure_changed == 'false'`; `timeout-minutes: 10`): runs `decision-evidence.py` on the `spec` artifact's `fetch-result.json` and `spec.diff`, `copilot-decide.sh .github/audit/triage-prompt.md`, `validate-triage`, and outputs `rubric`. Readers:
  - `rubric` job: `needs` gains `triage`; its `if` starts with `!cancelled()` (a skipped `triage` must not skip it), keeps Phase 1's guards, replaces `spec_changed == 'true'` with `(spec_changed_this_run == 'true' || rubric_incomplete == 'true' || structure_changed == 'true')`, and requires `needs.triage.result` success or skipped and `needs.triage.outputs.rubric != 'ignore'`.
  - the `rubric` `download-artifact` steps in `research`, `evals`, `merge` and `apply`: `if: needs.rubric.result == 'success'` (`apply` gains `rubric` in `needs`).
  - `merge`'s `validate-decision`: `--spec-changed` when `needs.rubric.result == 'success'`; `--structure-changed` unchanged. Ruling: `rubric` success means a non-ignored spec change, an incomplete rubric or structure drift, Phase 1's meaning of the flag.
  - `state` job: `needs` gains `triage`; its `if` adds `(needs.triage.result == 'success' || needs.triage.result == 'skipped')`; when `needs.triage.outputs.rubric == 'ignore'` it calls `write-state.sh state --ignore-spec "$SPEC_SHA"` (job env from `needs.detect.outputs.spec_sha`) `--until <UTC today + 2 × AUDIT_INTERVAL_DAYS days>` (two intervals, plan 5 Design resolution 5).
- **`write-state.sh state [--ignore-spec SHA --until YYYY-MM-DD]`**: both or neither, SHA 40 lowercase hex, a real date, else exit 2 before any write; sets `.ignored = {spec_sha, until}` in the same jq merge; `read`, `checkpoint`, `attempt` and a `state` call without the options keep a live `ignored`. Plan 9 adds `--review-cursor N` to this parser.
- **B2 recording**: the trusted PR step of `apply` appends `## Models` to `pr-body.md` before `gh pr create`: each lane of `needs.detect.outputs.models` and `AUDIT_MERGER_MODEL` as requested; for `auto`, the actual model only when `ci-spike.md` records how to read it, else `auto (actual model not reported)`.
- **B4 upstream triage**: Phase 1's `upstream-report` already answers a closed `update|ignore` per stale row, fails on an invalid answer and writes only the issue. Ruling: no new code, because issue-only mode is exactly that job; it only gains `timeout-minutes: 10` (Focus 4).

- [ ] **Step 1: Failing tests.** `test_decision_evidence.py`: `test_whitelist_rejects_free_text` (a slug with a space or a backtick), `test_summary_cap_2kb`, `test_token_pattern_rejected` (each exit 2, empty stdout); a valid fetch result gives exactly the five keys. `test_audit.py`: `validate-triage` accepts the two objects and rejects an extra key, another value, a non-object and invalid JSON; `test_ignored_sha_not_retriggered_until_expiry` (`spec-ignored` true on `until`, false the day after), `test_new_sha_retriggers` (another sha), and `false` for an absent or malformed `ignored`. Stub-`gh` tests: `state --ignore-spec <sha> --until 2026-12-01` sets `ignored` and keeps every other live key; one option alone, a short sha or `2026-02-30` exits 2 and writes nothing; `checkpoint`, `attempt` and plain `state` keep a live `ignored`. `test-copilot-decide.sh` (stub `copilot` on `PATH` recording argv and env): argv holds `--no-ask-user`, the model and the recorded no-tools flags and no `--allow-tool`; the prompt contains the evidence; `JEV_API_KEY` and `AUDIT_BOT_TOKEN` set by the caller are absent from the stub's env. `test-workflow.sh`, one case per Interfaces item that edits the workflow (each `if`, `needs`, the `--ignore-spec` call, both `timeout-minutes`, the `## Models` append), and `rg -nw 'needs.detect.outputs.spec_changed' .github/workflows/skill-audit.yaml` printing nothing (`-w`, so `spec_changed_this_run` does not match).
- [ ] **Step 2: Implement** the Interfaces above; run `python3 -m unittest discover -s tests/audit`, `bash scripts/audit/run-script-tests.sh`, `actionlint` → green; one commit per B item.
- [ ] **Step 3:** Dual-lane code review, one fix wave, scoped re-review, compact to 3-6 commits, push, PR stacked on #8.

### Task 4: First real run (user gate)

- [ ] **Step 1:** After #8 and this PR merge, `gh workflow run skill-audit.yaml` from `main` (schedule and dispatch run only from the default branch). It is a full run whatever `force` says: with `AUDIT_LAST_STATE` absent or invalid, `detect()` sets `full` (`not old_valid`) and selects every non-synced skill (pass `-f force=true` only if a valid state exists). Before dispatching, recount on `main` (synced skills excluded) and get the user's yes on the cost; today: 43 skills, one judge call per lane, 149 quality evals plus 857 trigger queries × 3 runs (`run-evals --runs` default) = 2,720 runner calls in `evals`, plus merge, fixer, PR-body and `apply` eval calls. Over the allowance stated in Task 1 Step 5: stop and ask. Ruling: no cap, because plan 9's `AUDIT_MAX_ARTIFACTS` bounds only the rotation, never `detect`'s full set (plan 9 Review Focus 3), so waiting for plan 9 would not bound this run. Read the logs; fix what fails.
- [ ] **Step 2:** Failure drills (bad token, empty model list, hung reviewer) and then `gh variable set AUDIT_ENABLED --body true`.
