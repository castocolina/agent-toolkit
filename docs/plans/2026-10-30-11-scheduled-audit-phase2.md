# Plan 11 — Scheduled Audit Phase 2 (spike, scope cuts, triage)

Status: DRAFT, split out of the first plans PR. Not spec-reviewed. Re-run /ai-kit-spec-review after plan 5 (PR #8) merges. Open review findings: tmp/docs/spec-review-iter7-report.md (main checkout, untracked) and the handoff.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run the Copilot spike, turn plan 5's Phase 2 (tasks B1-B5 and ten open issues) into a smaller, executable Phase 2, and implement it, so the scheduled audit can be switched on.

**Architecture:** Phase 1 (PR #8) already gates, judges, opens fix PRs and reviews them. Phase 2 adds only what needs a model decision between steps: spec-change triage, upstream triage (issue only) and model resolution. It stays keyless: no jev key, no automerge, no skill install on secret-bearing runners. Those are cut here and can return as a later plan.

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
| B3 spec triage, B4 upstream triage (issue only), B2 minimal model recording, B1 agent-only decision protocol | **Keep** | The remaining value of Phase 2 |
| Owner sign-off on the fetch-script deviation (issue 3, 10) | Needs one line from the user | Cheap model stays keyless; a script fetches evidence and triage sees only validated enums |

If the user declines a cut, that item returns as its own plan with the open issue resolved first.

## Review Focus

1. A triage answer injects text into a later step → triage output is a closed enum set validated by `validate-decision`; free text never reaches the fixer prompt. Pinned in Task 3.
2. `rubric_stale` blocks every `ignore` (issue 4) → two booleans: `spec_changed_this_run` (this run's fetch changed the pin) and `rubric_incomplete` (the pin differs from the committed rubric before this run). Only `rubric_incomplete` and `structure_changed` override `ignore`; a failing `rubric-check` fails the `rubric` job, and every downstream `if` requires `rubric` success or skipped, so it blocks `merge` and needs no override. Pinned in Task 3.
3. A triage failure advances state → it fails the run without touching state (Phase 1 rule). Pinned in Task 3.
4. A skipped decision point is silent → one failure rule for every decision point (issue 8): a model error, an invalid enum or a timeout fails the job, so the run fails without touching state (Focus 3), never "no change". Ruling: a failed run for all three, because it is Phase 1's tested fail-safe path (an invalid `recommendations.json` already fails `upstream-report`, which blocks `state`) and the next due run retries; `needs-human` stays the outcome of the PR review only, since a failed triage has no PR to label. Pinned in Task 3.
5. The spike result contradicts an assumption → Task 1 records it, and Task 2 re-reads this table before editing anything.

---

### Task 1: Run the spike (needs the tokens)

**Files:** Create `.github/workflows/copilot-smoke.yaml` (temporary), `docs/audit/ci-spike.md` (extend).

- [ ] **Step 1:** Confirm `gh secret list -R castocolina/agent-toolkit` shows `COPILOT_GITHUB_TOKEN` and `AUDIT_BOT_TOKEN`; if not, stop and point the user to `tmp/docs/tokens-setup.md`.
- [ ] **Step 2:** Execute plan 5 Task 1 Steps 1, 2 and 4, Step 3 for the reviewer-bot facts only (its `skill-audit-gate.yaml` schedule consequence is superseded), and the containment drill of plan 5 Task A3 Step 2: smoke workflow on branch `spike/copilot-smoke`, model list, a several-KB prompt on stdin, `--allow-tool` / `--deny-tool` syntax, a no-tools mode, write confinement, reviewer bot behavior. Record every answer in `docs/audit/ci-spike.md`; replace each UNVERIFIED mark with the observed result or leave it.
- [ ] **Step 3:** Delete the spike branch and the workflow file; confirm with `git ls-remote --heads origin spike/*`.
- [ ] **Step 4:** Update the reviewer wrapper and README where the spike changed a tool name (`copilot-review.sh`), with tests first. Commit `docs(audit): record the Copilot spike` and `fix(audit): align the reviewer wrapper with the spike`.
- [ ] **Step 5 (user gate):** present the observed model list; the user picks `AUDIT_RESEARCH_MODELS`, `AUDIT_MERGER_MODEL` and optionally `AUDIT_REVIEW_MODEL`; set them with `gh variable set`.

### Task 2: Amend plan 5 Phase 2 with the cuts

**Files:** Modify `docs/plans/2026-10-24-05-scheduled-audit.md` (Phase 2 section, open issues, knobs, required secrets).

- [ ] **Step 1:** After the user's yes on the scope table, edit plan 5's `## Phase 2` section by deletion and substitution only, so B1-B4 stay written down as the spec Task 3 implements. Delete every sentence that serves only a cut item of the scope table (jev and `JEV_API_KEY`, skill install, automerge and the required check, `re_review=no`, upstream `pr` mode and `approved_keys`, `family:` resolution); this removes Task B5 and Design resolutions 2, 4 and 6 whole. Substitute: each remaining jev call becomes "the agent decides from the evidence file and answers with a closed enum"; in B3 `rubric_stale` becomes `rubric_incomplete` and `spec_changed` becomes `spec_changed_this_run` (Focus 2). Mark each open issue `resolved`, `cut` or `moved to plan 11` in one line; issue 8 points to Focus 4. In `## Required secrets and variables` delete only the `JEV_API_KEY` row and the jev wording. Ruling: deletion only, because a rewrite would drop text Task 3 implements.
- [ ] **Step 2:** Run `/ai-kit-spec-review` on the amended plan (two lanes, one is enough) until approved. Commit `docs(plan): reduce Phase 2 to the keyless decision protocol`.

### Task 3: Implement B1-B4

**Files:** `scripts/audit/audit.py` (`validate-decision` enums, triage outputs), `.github/audit/{decision-evidence.py,copilot-decide.sh,render-prompt.py}`, `.github/workflows/skill-audit.yaml`, `tests/audit/*`.

- [ ] **Step 1: Failing tests** for the Review Focus items above: enum validation, the two booleans, evidence built from a character whitelist only (page paths charset-checked), state untouched on a triage failure, the Focus 4 rule at each decision point (model error, invalid enum and timeout each fail the job and leave state untouched), and the Step 2a reader rewiring (case table in `test-workflow.sh`).
- [ ] **Step 2:** Implement B1-B4 as Task 2 left them in plan 5, with the Focus 4 failure rule at each decision point; B3 emits `spec_changed_this_run` and `rubric_incomplete` as `detect` job outputs, replacing Phase 1's single `spec_changed` (`structure_changed` stays), and these exact names are what plan 9 Task 1 consumes (Step 2a does the rewiring); one commit per task; run `python3 -m unittest discover -s tests/audit`, `bash scripts/audit/run-script-tests.sh`, `actionlint`.
- [ ] **Step 2a: Rewire every reader of `needs.detect.outputs.spec_changed`.** Phase 1's `spec_changed` is `changed OR rubric_stale OR structure_changed` (the `Fetch specification and detect changes` step in `skill-audit.yaml`), so a plain rename would change behavior. In the `detect` job's `publish` step write `spec_changed_this_run` from the fetch result's `changed` and `rubric_incomplete` from its `rubric_stale`, and drop the `spec_changed` output. Then edit each reader, with a test per row in `tests/audit/test-workflow.sh` (a case table over both booleans and `structure_changed`):
  - the `detect` step's own `audit.py detect --spec-changed "$SPEC_CHANGED"` call keeps the Phase 1 value through a private variable `this_run OR incomplete OR structure_changed` (not published), so `run_needed`, `full` and the reasons stay as pinned by `test_detect_spec_change_runs_all`;
  - the `rubric` job `if` (and the `spec` artifact download and unpack steps it runs) and the four `download-artifact` steps that fetch the `rubric` artifact in the `research`, `evals`, `merge` and `apply` jobs: the condition is `spec_changed_this_run == 'true' || rubric_incomplete == 'true' || structure_changed == 'true'`, written once as a comment-labelled expression, so the `rubric` job also runs and uploads when only `rubric_incomplete` is true (plan 9 Task 1 depends on this);
  - the `merge` job's `validate-decision` call (`[ ... spec_changed ... ] || ARGS+=(--spec-changed)`): pass `--spec-changed` when `rubric_incomplete` is true, or when `spec_changed_this_run` is true and the B3 triage result is not `ignore`; `--structure-changed` stays as is. Ruling: only `rubric_incomplete` and `structure_changed` override `ignore` (Review Focus 2; a failing `rubric-check` blocks `merge` through the `rubric` job result instead), so `spec_changed_this_run` alone must not force `update=true`.
  Add a final workflow test: `rg -nw 'needs.detect.outputs.spec_changed' .github/workflows/skill-audit.yaml` prints nothing (`-w`, so the new `spec_changed_this_run` does not match), and every `if:` that mentioned it now names the new booleans.
- [ ] **Step 3:** Dual-lane code review, one fix wave, scoped re-review, compact to 3-6 commits, push, PR stacked on #8.

### Task 4: First real run (user gate)

- [ ] **Step 1:** With the user's go-ahead: `gh workflow run skill-audit.yaml` from `main` after #8 and this PR merge (schedule and dispatch run only from the default branch); run it as a full run with `gh workflow run skill-audit.yaml -f force=true` and no `approved_upstreams` (`force` selects every non-synced skill in `detect()`; the default is `false`, so a bare dispatch would select nothing unless something changed, and Phase 1 has no knob that narrows the judged set; `AUDIT_MAX_ARTIFACTS` arrives with plan 9). Ruling: a full run, because this plan adds no limiting mechanism and the user gate precedes it. Read the logs; fix what fails.
- [ ] **Step 2:** Failure drills (bad token, empty model list, hung reviewer) and then `gh variable set AUDIT_ENABLED --body true`.
