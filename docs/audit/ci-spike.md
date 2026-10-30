# CI spike: Copilot CLI and repository settings (partial)

Status: **partial, Actions behavior not yet verified.** Task 1 of plan 5 needs a push of `spike/copilot-smoke`, a `COPILOT_GITHUB_TOKEN` secret and repository settings that are not configured yet (`gh secret list` and `gh variable list` were empty when this was written; `allow_auto_merge` is `false`). Everything below marked VERIFIED comes from `copilot --help` of GitHub Copilot CLI 1.0.103 on a workstation. Everything marked UNVERIFIED must be confirmed by running the spike before `AUDIT_ENABLED` is set to `true`.

## Copilot CLI flags (VERIFIED from `--help`, 1.0.103)

| Need | Flags |
|---|---|
| Non-interactive prompt, response only | `-p, --prompt <text>` with `-s, --silent` |
| No questions to a human | `--no-ask-user` |
| Pick the model | `--model <model>` |
| Allow or deny tools | `--allow-tool [tools...]`, `--deny-tool [tools...]` |
| Restrict the tool set | `--available-tools [tools...]`, `--excluded-tools [tools...]` |
| Redact secrets from tool environments | `--secret-env-vars [vars...]` |

Wrapper contract used by Task 3 (assumed tool names, UNVERIFIED until the spike lists them):

- `copilot-runner.sh` (evals, no tools): `copilot -p "$(</dev/stdin)" -s --no-ask-user --model "$AUDIT_MERGER_MODEL" --available-tools ''`
- `copilot-agent.sh` (edits files in the checkout, no shell): same call with `--allow-tool=read --allow-tool=write` and `--excluded-tools shell`.

## Items the spike must still record (UNVERIFIED)

1. Step 1: the CLI installs and authenticates in Actions with `COPILOT_GITHUB_TOKEN`; the exact install step.
2. Step 2: with the flags above Copilot edits a scratch file and cannot run a shell.
4. Step 5: default workflow-token permissions (`gh api repos/{owner}/{repo}/actions/permissions/workflow --jq .default_workflow_permissions`), so the audit behaves the same under `read` and `write`.
5. Step 6: which models the account offers for `AUDIT_RESEARCH_MODELS` and `AUDIT_MERGER_MODEL` (the owner picks).
7. apply: that `copilot -p ... --allow-tool=read` returns a usable Markdown PR body on stdout from the body-only prompt (diff stat, trimmed diff, rationale passed in; no git/gh available).
8. apply: drawio CLI installation on hosted runners (xvfb) is assumed unreliable; `AUDIT_PR_DIAGRAMS=drawio` logs a warning and uses mermaid until this is verified.
9. Supply-chain pins: the exact `@github/copilot` CLI version the spike installs (so the unversioned `npm install -g @github/copilot` steps can be pinned to it) and the commit SHA of the `astral-sh/setup-uv` release matching tag `v5.4.1` (the tag is mutable), for all four `setup-uv` uses. The `setup-uv` pin is now `0c5e2b8115b80b4c7c5ddf6ffdd634974642d182 # v5.4.1` in every use (resolved from the tag, not yet confirmed on Actions); the Copilot install still needs its exact version recorded here and written into each install step.
10. apply: the audit branch probe is anonymous (`git ls-remote` on the credentialless checkout). Confirm the repository is readable without credentials; on a private repository the probe fails and the run stops (UNVERIFIED). If that is the case, pass the PAT only to a dedicated probe step, never to a model step.

### Phase 1 spike additions (plan 5, Amendment A, Task A3 Step 2)

Every item below is UNVERIFIED until the spike runs it in Actions. The local CLI help does not establish any of them.

11. **Containment drill for the reviewer (gate for `AUDIT_REVIEW_MODEL`).** UNVERIFIED. Run `.github/audit/copilot-review.sh` in Actions with its exact flags (`--allow-tool=read --excluded-tools shell write web_fetch`; the names `write` and `web_fetch` are UNVERIFIED, so the drill must confirm the tool names are real), `--model`, `--reasoning-effort`, prompt on stdin, no `GH_TOKEN` or `GITHUB_TOKEN` in the environment). Ask it three things: run a shell command, write a file, and fetch a URL. All three must be refused or unavailable. Only then may `AUDIT_REVIEW_MODEL` be set. If any of the three succeeds, or the result is unclear, the variable stays empty and the review stays off (the `audit-review:skipped` path).
12. **Free-tier request quota and exhaustion (UNVERIFIED).** Measure how many requests the review and the judge lanes use on the Free tier, and what the account reports when the quota runs out. Exhaustion must yield a failed or `needs-human` outcome, never a positive.
13. **`--model auto` headless on Free (UNVERIFIED).** Confirm that `copilot -p ... --model auto` runs non-interactively on the Free tier, and which concrete model it resolves to. `AUDIT_RESEARCH_MODELS=auto` and `AUDIT_MERGER_MODEL=auto` depend on this.
14. **Commit statuses with the workflow token (UNVERIFIED).** Confirm that `GITHUB_TOKEN` with `statuses: write` can `POST repos/{owner}/{repo}/statuses/{sha}` for the head of a PR created by `AUDIT_BOT_TOKEN`, and that the status shows as the `skill-audit/review` or `skill-audit/evals` check on that PR.
15. **Called-workflow `statuses: write` ceiling (UNVERIFIED).** Confirm that `skill-audit-review.yaml` (called by `skill-audit.yaml`'s `review` job) receives no more than the caller's `statuses: write` grant, and that the `review` and `publish` steps can write the status with it.
16. **`--reasoning-effort` in Actions.** VERIFIED locally: `copilot --help` (CLI 1.0.103) lists `--reasoning-effort <level>` with the values `none, minimal, low, medium, high, xhigh, max`, which `audit.py` pins. UNVERIFIED in Actions: that the flag is accepted headless and that the effort reaches the model.

### Phase 2 open issues (plan 5, "Phase 2 open issues", items 1-10)

Not implemented. Each item stays UNVERIFIED and blocks Phase 2 (automerge, jev and the judge decisions) until it is resolved and the plan review is re-run:

- 18. Skill install and key isolation (plan item 1).
- 19. Required check and bypass actors for `skill-audit/review` (plan item 2).
- 20. Cheap model orchestrating the research skill, and the owner's sign-off on that deviation (plan items 3 and 10).
- 21. `rubric_stale` distinguishing a pre-existing incomplete refresh from this run's candidate (plan item 4).
- 22. The `re_review=no` rubric-only route and pending versus committed judge state (plan item 5).
- 23. The upstream `pr` mode DAG, with a post-triage planning job (plan item 6).
- 24. Model roles and the `models` data contract, including family resolution and `models_seen` (plan item 7).
- 25. The per-decision failure table and injection defenses in the key-holding step (plan item 8).
- 26. Triage wiring and the `rubric-check` placement (plan item 9).
- 27. The A7-style configuration of the Phase 2 knobs (plan item 10).
