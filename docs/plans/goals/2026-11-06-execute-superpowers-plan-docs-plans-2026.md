# Goal prompt: Execute superpowers plan docs/plans/2026-11-06-13-judge-preservation.md, then docs/plans/2026-11-06-14-content-recovery.md (14 depends on 13 merged)

The recommended block is one /goal condition that stops when DONE WHEN holds. Paste one block between the markers into a fresh session in this repository.

▼▼▼ COPY FROM HERE ▼▼▼

## Strategy 1 (recommended): goal

````
/goal read document `docs/plans/goals/2026-11-06-execute-superpowers-plan-docs-plans-2026.md` at section `Full goal` and finish only when that section's DONE WHEN conditions hold
````

▲▲▲ COPY TO HERE ▲▲▲

## Rails

OBJECTIVE
- Finish Execute superpowers plan docs/plans/2026-11-06-13-judge-preservation.md, then docs/plans/2026-11-06-14-content-recovery.md (14 depends on 1..., each verified. Then leave the repository clean.
- PRECEDENCE: where the generic Rails sections conflict with this objective, this objecti... (full text: docs/plans/goals/2026-11-06-execute-superpowers-plan-docs-plans-2026.md section Full objective)

ROLE
- You are the orchestrator: the session that received this prompt. Dispatch plan work to subagents, reusing one or starting a fresh one, as you judge best.
- Verify every result yourself; never accept a reported pass.

RULES FOR EVERY PLAN
- Work the task in order and verify each step yourself; never accept a reported pass.
- You own AGENTS.md compliance; read AGENTS.md first.
- Read a skill only when the task needs it. Candidate skills: ai-kit-cross-ai, ai-kit-gsd-spec-discuss, ai-kit-session-wake, ai-kit-spec-execute-superpowers, skill-judge, skill-updater.
- Pre-commit hooks always run on every commit; fix a real failure at its root, never skip it.

QUOTA
- A. This session (its own quota): before the first plan, arm the ai-kit-session-wake skill, a self-resume by session id at the host-reported reset when known, else hourly.
   Run its done step when the run ends. Only this orchestrator arms or disarms it.
   Wake primitive on this host: systemd user timer.
- B. Cross-AI children (a child CLI hits its limit): follow the ai-kit-cross-ai skill. The runner cross-ai.mjs owns the retry ladder and never switches CLI, provider or model.
   Read its last AIKIT-XAI status line before acting.
   A quota stop whose AIKIT-XAI line has a whole-number retry_after_s: wait that exact time once (one one-shot job, never a fixed-interval re-check), then re-invoke the same lane.
   Check the working tree and resume only the unfinished work. After stopped=hard-waits or stopped=cap schedule nothing more.
   A quota stop without retry_after_s is an owner stop: report the evidence and stop. Whether this host can run a one-shot job is unverified.

DECISIONS
- Verifiable questions: check and fix them directly; do not ask.
- Gray areas: ask the jev-fast-decision skill and follow its SKILL.md. Advisory only: on needs_fallback or no answer you decide; verify before acting. Prefer the best design over the easiest.
- Never pause for questions or UAT. Put a blocking item in the ledger and continue.
- Never remove existing features.

SAFETY
- Never touch the real ~/.claude, ~/.cursor, ~/.config/opencode, ~/.codex, ~/.pi or ~/.gsd; use a scratch HOME.
- Never print secrets. Never push. Never stage everything blindly.
- Pre-commit hooks and every test tier always run; no step may skip one.

DONE WHEN
- No e2e suite exists. The first task, before any feature plan, creates one that launches the real app (a PTY drive for a terminal UI, a browser for a web UI) and make it pass.
- Print each command with its exact exit code, its count line and the last 20 lines of output, ANSI codes stripped.
- Gates first: the project's lint and unit commands (none detected: find them).
- Print the paths of the screenshots or TUI text snapshots the e2e run produced.
- Start each long-lived e2e process in its own process group and record its group id in tmp/. After the run kill those groups and print a process listing (ps) that shows none remain.
- Phase status: VERIFICATION shows passed for every phase in scope, or the item is listed as human verification with its reason.
- Unit tests alone never count as done.

CLEANUP
- Leave no stray files: commit, ignore or remove each.
- Act only on worktrees, branches and tags this run created and recorded in a run ledger under tmp/.
- Anything older or not owned by this run is reported, never removed.
- Finished work means the backlog entries and the directories of work items finished in this run. Remove those; list the rest.
- Before any merge or removal, the porcelain form of git status must be empty in that worktree and in the main checkout.
- Never force a merge, removal or branch delete. On a conflict or a dirty tree, stop and report.
- Merge the working branch into the main checkout; never push.
- Archive the unmerged work of each worktree this run created as a tag, then remove that worktree and its branch; remove this worktree last.

STOP IF
- The same failure repeats 3 times with no progress.
- Stop after 60 turns and report.
- A decision blocks other work and nothing resolves it.
- A step needs a real config write, a login or sudo.
- In each case park the item, continue independent work, then report.

REPORT
- Per item: status, verification, the evidence printed, the cross-AI CLI used.
- The ledger of your decisions, the commits made, nothing pushed.
- Advisory (not a gate): ask the jev-fast-decision skill one choice item (follow its SKILL.md), objectives all, mostly, partly or not met, from text summaries only.
- Report jev's advisory answer under that heading; needs_fallback or no answer means you judge it yourself.

## Full objective

PRECEDENCE: where the generic Rails sections conflict with this objective, this objective wins.
Never merge anything into main or the main checkout. Pushing feature branches and opening PRs is
required. This repo has no app: do not create an e2e suite; the DONE WHEN gates below are the
end-to-end checks. Use the real HOME, because the pi lanes need it, but never write ~/.claude. The
60-turn cap does not apply; the other STOP IF items do. Ignore GSD phase VERIFICATION and cross-AI
runner steps. Execute plan 13 (docs/plans/2026-11-06-13-judge-preservation.md), then plan 14
(docs/plans/2026-11-06-14-content-recovery.md), task by task with
superpowers:subagent-driven-development. The intent file
docs/plans/2026-11-06-13-content-recovery-intent.md (rulings R1-R6 and the standing rulings) is
binding. Resolve each finding in docs/plans/2026-11-06-13-14-review-notes.md when its task runs. The
goal is not a higher score. Every skill, command and agent keeps the expert guidance it had at
baseline dbff837f unless a recorded decision moved or dropped it. Its sources are found and its
version-sensitive facts are checked against official docs. It still grades 90 or more under rubric
v5, with passing evals. Rails (lessons from plans 4, 8, 12 and 13): 1. Never cut to fit the judge.
Every removed rule, step, fact, template, example, line or file gets a record row (fate, value,
decision, reason). After every edit, read the lines and paragraphs next to it to catch collateral
deletions. Never remove, shorten or reword a credit, attribution or license line. 2. Only
section-level presence checks count as evidence. A whole-artifact 'guidance lost' answer does not
(skill-judge read 65% lost at confidence 0.31; the section check found 74% present). Restore content
by rewriting it in the current style, into references/ unless the procedure depends on it. Never
paste it back wholesale. 3. Facts: point, do not pin. Prefer instructions that read the live value
(the CLI's --help, its model list, the API catalog). A value that must be written carries its
official source URL and the date checked. Example: codex still defaults to the deprecated gpt-5.2.
4. Batches hold at most 3 artifacts. Use one native sonnet implementer per artifact (Agent tool,
model sonnet, effort medium), with docs/audit/fixer-rules.md in its prompt. router-env/my-coding is
not used. Judging and review run only on pi referee lanes (router-env/my-referee-one, -two, -three),
never on native Opus. Two lanes are ideal and one is enough. A lane that answers 404, 503,
'unavailable' or out of quota is not a blocker: switch to another lane or wait, never stop. 5. After
every ai-kit-spec-review merge-reports, compare the finding titles in each lane's report against the
merged file, because it drops findings that contain nested bullets. Send any missing finding to the
fixer. 6. jev is advisory only, never a gate. Its ladder escalates to a remote backend even with
JEV_BACKEND=laya, so call a backend directly. Send artifact text off this machine only to a backend
with recorded consent. Never send secrets or .env values. 7. Calibration: when a band drops, fix the
rubric wording, never a fixture or expected.json. 8. gepetto and datadog-cli are report-only and
never edited. skills/skill-judge/references/agentskills/ is a vendored mirror and is excluded. 9.
Git: plan 13 gets one branch and one PR. Plan 14 gets the PR groups it defines. While an earlier PR
is unmerged, stack each new PR on the previous open one, starting from PR #17
(docs/26-11-06-content-recovery-plan). Never merge, and never push to main. Before review, fold
fix-on-fix commits into 3 to 6 logical commits per PR. Commit with git -C <wt> commit -F <file>,
with no attribution trailers. Every commit that touches skill-judge or skill-updater runs python3
scripts/build_plugins.py first and includes dist/. 10. Shell: no cd chains, no heredocs, no
multi-statement one-liners. Write .sh scripts with the Write tool and run them with bash
/abs/path.sh. Pass rails 1 to 12 to every subagent. 11. Before a plan ends, close every process,
pane and subagent you started. 12. Collect user decisions in one form per PR and never block a batch
waiting for one. An artifact still failing after round 3 goes on the user's list. DONE WHEN all of
these hold: - Every plan 13 and plan 14 checkbox is checked or carries a recorded user decision. -
On each PR branch, bash scripts/audit/run-script-tests.sh and python3 scripts/audit/audit.py check
--strict pass, with the test count printed. - python3 scripts/build_plugins.py leaves dist/
unchanged. - bash tests/skills/skill-judge/calibrate.sh holds every band. - python3
scripts/audit/audit.py recovery check is clean for every closed batch. - Every PR is open with green
CI and a final review with fewer than 3 critical or high findings. - A final report table lists, per
artifact: lost items found, restored, moved, dropped with reason, facts updated with source, and
final grade.

## Full goal

Finish Execute superpowers plan docs/plans/2026-11-06-13-judge-preservation.md, then
docs/plans/2026-11-06-14-content-recovery.md (14 depends on 13 merged), each verified. Then leave
the repository clean. PRECEDENCE: where the generic Rails sections conflict with this objective,
this objective wins. Never merge anything into main or the main checkout. Pushing feature branches
and opening PRs is required. This repo has no app: do not create an e2e suite; the DONE WHEN gates
below are the end-to-end checks. Use the real HOME, because the pi lanes need it, but never write
~/.claude. The 60-turn cap does not apply; the other STOP IF items do. Ignore GSD phase VERIFICATION
and cross-AI runner steps. Execute plan 13 (docs/plans/2026-11-06-13-judge-preservation.md), then
plan 14 (docs/plans/2026-11-06-14-content-recovery.md), task by task with
superpowers:subagent-driven-development. The intent file
docs/plans/2026-11-06-13-content-recovery-intent.md (rulings R1-R6 and the standing rulings) is
binding. Resolve each finding in docs/plans/2026-11-06-13-14-review-notes.md when its task runs. The
goal is not a higher score. Every skill, command and agent keeps the expert guidance it had at
baseline dbff837f unless a recorded decision moved or dropped it. Its sources are found and its
version-sensitive facts are checked against official docs. It still grades 90 or more under rubric
v5, with passing evals. Rails (lessons from plans 4, 8, 12 and 13): 1. Never cut to fit the judge.
Every removed rule, step, fact, template, example, line or file gets a record row (fate, value,
decision, reason). After every edit, read the lines and paragraphs next to it to catch collateral
deletions. Never remove, shorten or reword a credit, attribution or license line. 2. Only
section-level presence checks count as evidence. A whole-artifact 'guidance lost' answer does not
(skill-judge read 65% lost at confidence 0.31; the section check found 74% present). Restore content
by rewriting it in the current style, into references/ unless the procedure depends on it. Never
paste it back wholesale. 3. Facts: point, do not pin. Prefer instructions that read the live value
(the CLI's --help, its model list, the API catalog). A value that must be written carries its
official source URL and the date checked. Example: codex still defaults to the deprecated gpt-5.2.
4. Batches hold at most 3 artifacts. Use one native sonnet implementer per artifact (Agent tool,
model sonnet, effort medium), with docs/audit/fixer-rules.md in its prompt. router-env/my-coding is
not used. Judging and review run only on pi referee lanes (router-env/my-referee-one, -two, -three),
never on native Opus. Two lanes are ideal and one is enough. A lane that answers 404, 503,
'unavailable' or out of quota is not a blocker: switch to another lane or wait, never stop. 5. After
every ai-kit-spec-review merge-reports, compare the finding titles in each lane's report against the
merged file, because it drops findings that contain nested bullets. Send any missing finding to the
fixer. 6. jev is advisory only, never a gate. Its ladder escalates to a remote backend even with
JEV_BACKEND=laya, so call a backend directly. Send artifact text off this machine only to a backend
with recorded consent. Never send secrets or .env values. 7. Calibration: when a band drops, fix the
rubric wording, never a fixture or expected.json. 8. gepetto and datadog-cli are report-only and
never edited. skills/skill-judge/references/agentskills/ is a vendored mirror and is excluded. 9.
Git: plan 13 gets one branch and one PR. Plan 14 gets the PR groups it defines. While an earlier PR
is unmerged, stack each new PR on the previous open one, starting from PR #17
(docs/26-11-06-content-recovery-plan). Never merge, and never push to main. Before review, fold
fix-on-fix commits into 3 to 6 logical commits per PR. Commit with git -C <wt> commit -F <file>,
with no attribution trailers. Every commit that touches skill-judge or skill-updater runs python3
scripts/build_plugins.py first and includes dist/. 10. Shell: no cd chains, no heredocs, no
multi-statement one-liners. Write .sh scripts with the Write tool and run them with bash
/abs/path.sh. Pass rails 1 to 12 to every subagent. 11. Before a plan ends, close every process,
pane and subagent you started. 12. Collect user decisions in one form per PR and never block a batch
waiting for one. An artifact still failing after round 3 goes on the user's list. DONE WHEN all of
these hold: - Every plan 13 and plan 14 checkbox is checked or carries a recorded user decision. -
On each PR branch, bash scripts/audit/run-script-tests.sh and python3 scripts/audit/audit.py check
--strict pass, with the test count printed. - python3 scripts/build_plugins.py leaves dist/
unchanged. - bash tests/skills/skill-judge/calibrate.sh holds every band. - python3
scripts/audit/audit.py recovery check is clean for every closed batch. - Every PR is open with green
CI and a final review with fewer than 3 critical or high findings. - A final report table lists, per
artifact: lost items found, restored, moved, dropped with reason, facts updated with source, and
final grade. Done when every DONE WHEN item in
docs/plans/goals/2026-11-06-execute-superpowers-plan-docs-plans-2026.md section Rails holds, with
the exit code and count line of every command printed. Unit tests alone never count as done. If it
does not hold, stop and report after 60 turns.
