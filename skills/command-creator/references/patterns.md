# Command Body Skeletons

Read the one skeleton for the pattern chosen in SKILL.md, then replace every `<...>` with the user's own tools, paths and numbers. What each pattern must define, and the gotchas, live in SKILL.md; these are only body shapes.

## Simple execution

````markdown
---
description: <what it does, in one line>
argument-hint: [base-branch]
arguments: base
---

1. If `$base` is empty, use `main` if `git rev-parse -q --verify --end-of-options refs/heads/main` succeeds, else `master`
   if the same check on `refs/heads/master` succeeds; if neither exists, stop and ask for an explicit base branch.
2. If `$base` is not empty, encode `refs/heads/$base` as one single-quoted shell word: wrap it in `'...'` and write each `'` inside
   it as `'\''` (a branch `it's` gives `'refs/heads/it'\''s'`). Run `git rev-parse -q --verify --end-of-options <encoded ref>`;
   if it fails, stop and say the branch was not found.
3. Run `<tool> -- <encoded value>` (same encoding; use the tool's own end-of-options form if it has one) and show its output unchanged.
4. On a non-zero exit, show the error output and the command that failed. Do not retry.
````

## Iterative fixing

````markdown
---
description: Run <check> and fix failures until it passes
---

1. Baseline: run `<check command>`. Exit code 0: report SUCCESS (no fixes needed) and stop.
   Otherwise record each failure as check + file + first error line.

Then make at most <N> attempts. Each attempt is:

2. Fix the recorded failures you can fix from the code alone; read each file before editing it.
3. Run `<check command>` again. Exit code 0: report SUCCESS with the attempt count and stop.
4. Record the new failures. If a failure from the previous record survived two fix attempts unchanged, stop:
   report STUCK with that failure, what you tried, and what a human needs to decide.

If the check after attempt <N> still fails, report STUCK with the remaining failures.
Never weaken a test, skip a check, or add an ignore comment to make it pass unless the user said so.
````

The last line matters: the cheapest way for a loop to "pass" is to delete the evidence.

## Workflow with side effects

````markdown
---
description: <what it publishes or changes>
argument-hint: <required-argument>
arguments: <name>
disable-model-invocation: true
---

Context: !`git status --short 2>/dev/null || true`

1. Validate `$<name>` against <allowed values or pattern>; on anything else stop and ask. Any free text that reaches the shell
   (a message, a title, a path) is encoded as one single-quoted word, each `'` written as `'\''`.
2. Read-only prerequisites, in order, stopping on the first failure: <branch>, <clean tree>, <up to date>, <tests pass>,
   <the target does not exist yet (tag, version, release)>.
3. <Local change, for example the version bump or commit>. Stage named paths only (`git add -- <encoded path>`), and pass any
   message or title as an encoded value attached to its option (`git commit -m <encoded message>`), same encoding as step 1.
4. <Remote change, for example push or publish>.
5. If step 4 fails or times out, run <state check> and act on what it shows; never retry on any other outcome:
   - Confirmed done (the remote state matches what step 4 meant to create): continue to step 6 and say so.
   - Confirmed absent (the check succeeded and shows nothing): show the error and ask before one retry.
   - Unknown (the check fails or times out): stop and report that the state is unknown, with what to check by hand.
   - Conflicting or partial (another value is there, or only some of the changes landed): stop and report
     exactly what is there and what is missing; do not retry or overwrite.
6. Report what changed, where, and any step left for the user (for example an announcement in a tool you do not have).
````

Order the remote changes so the hardest one to undo comes last: a pushed tag can be deleted, a published package version usually cannot be reused.

## Plan, approve, execute

````markdown
---
description: Draft a plan for <goal>, wait for approval, then carry it out
argument-hint: [goal]
---

Phase 1, plan only. Do not edit or write any file in this phase.
1. If `$ARGUMENTS` is empty, ask what to plan.
2. Inspect what the plan needs. Read-only searches scoped to the goal are allowed without asking: find the
   implementation the goal names, its callers and the tests that cover it. Ask before going further (unrelated
   modules, whole-repo audits) or past any inspection limit the user set.
3. Show the plan in the conversation: steps, files to change, how each step is verified.

Phase 2 starts only when the user approves in their own words ("approved", "go ahead", "looks good").
Any other reply is feedback: revise the plan and show it again.
4. Save the approved plan to <path> and carry it out step by step, verifying each one.
````

Keep the approval wait in the main conversation. A `context: fork` subagent runs the body as one task and returns; it cannot pause for the user's reply, so a forked plan step must end by returning the plan, and the approval step stays in a command that runs in the main thread.
