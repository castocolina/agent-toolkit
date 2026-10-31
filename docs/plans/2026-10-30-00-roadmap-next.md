# Next Roadmap — Artifact Quality, Updater and CI Flow

**Date:** 2026-10-30 (continues [the 2026-10-24 roadmap](2026-10-24-00-roadmap.md); its Decisions and Global Constraints still apply except where this file says otherwise)
**Handoff (read first in a clean session):** [2026-10-30-00-handoff.md](2026-10-30-00-handoff.md)
**Status:** Plans 1-4 merged or in review (#7 open, mergeable); plan 5 Phase 1 open as #8; plans 6, 7, 8 and 10 under spec review, not executed; plans 9 and 11 are drafts split out of that review.

**Goal:** Every skill, command and agent is judged and fixed in small batches; a `skill-updater` keeps them current against sources and models; the scheduled CI reviews them in rotation; and `pr-diagrams` works on servers without `gh --attach`.

## Plans, in execution order

| # | Plan | Depends on | Ships |
|---|---|---|---|
| 5 | [Scheduled audit](2026-10-24-05-scheduled-audit.md), Phase 1 | 4 | PR #8 (open). Phase 2 stays blocked on the Copilot spike and your inputs |
| 6 | [New skills](2026-10-30-06-new-skills.md) | 4 merged, plan 5 merged (registry validator) | `ui-ux-principles`, `skill-updater`, `audit.py track`, judge profiles for commands and agents |
| 7 | [Artifact audit](2026-10-30-07-artifact-audit.md) | 6 | verdicts and a disposition table for 7 commands, 6 agents and 2 new skills |
| 8 | [Artifact fixes](2026-10-30-08-artifact-fixes.md) | 7 | the 26 high findings and every other finding, in batches of at most 3 artifacts; Mermaid rules moved into the diagram skills |
| 10 | [pr-diagrams branch and CI triggers](2026-10-30-10-pr-diagrams-branch.md) | 8 Task 4 | single `pr-diagrams` branch fallback, CI on any PR base |
| 11 | [Scheduled audit Phase 2](2026-10-30-11-scheduled-audit-phase2.md) | 5 merged, tokens set by the user | draft, own review after #8 merges. Copilot spike, Phase 2 cut to the keyless decision protocol, first real run |
| 9 | [CI artifact flow](2026-10-30-09-ci-artifact-flow.md) | 5 merged, 6, 7, 11 | draft, own review after #8 merges. Two-stage CI: refresh the judge, then review every artifact in rotation |

PRs are stacked as in the first roadmap. The ledger of problems is [2026-10-30-00-known-issues.md](2026-10-30-00-known-issues.md): the 26 high findings are skill content issues, so they belong to plan 8, not to plan 5.

## The flow, for every plan

plan → review (`/ai-kit-spec-review`, two lanes) → commit, push, PR → execute (`/ai-kit-spec-execute`) → code review (two lanes) plus skill judge → compact to 3-6 commits → push (`--force-with-lease` if already pushed) → PR stacked on the previous one. Chain as far as possible without stopping. Plans 6, 7, 8 and 10 go through the review gate first; plans 9 and 11 get their own review once plan 5 (PR #8) merges, because they integrate with its unmerged workflow code.

- **Lanes:** three referees exist (`router-env/my-referee-one|two|three`). Two per round is ideal; one is enough when the others are down; use the third to replace an unavailable one. Never native Opus for review. `my-coding` only implements. Probe a lane with a one-line prompt before a long run.
- **Judge scope:** `skill-judge` and `audit.py` cover `skills/` only until plan 6 Task 4 adds command and agent profiles. Any refactored skill is judged after its change (two lanes, 90 or more); a command or agent is judged only after those profiles exist, before that it gets its eval file and a code review.
- **CI:** deterministic checks run on every PR push (plan 10 Task 4); a retarget does not trigger `pull_request`, so close and reopen the PR to start a run. Inference and update workflows run on their schedule only.

## One-shot goal

Paste into a session opened at the repo root, or run `/goal Follow the "One-shot goal" section of docs/plans/2026-10-30-00-roadmap-next.md`.

```text
/goal
OBJECTIVE
Deliver plans 6, 7, 8 and 10 of docs/plans/2026-10-30-00-roadmap-next.md for castocolina/agent-toolkit, in that order, each as a reviewed, executed, tested, judged and code-reviewed PR stacked on the previous one. Plans 9 and 11 are drafts: review them only after plan 5 (PR #8) is merged. Do not execute plan 5 Phase 2.

DONE MEANS
- Each plan passed /ai-kit-spec-review (two lanes, one is enough if the others are down) before its code, then was executed with /ai-kit-spec-execute, code-reviewed, judged (skills now; commands and agents once plan 6 Task 4 exists), compacted to 3-6 commits, pushed and opened as a PR. Never merge.
- Every skill, command and agent the plans touch grades 90 or more, with passing evals. No findings are left over: plan 8 works in batches and re-queues instead of leaving a tail.
- Nothing of yours is left running; one short report per plan, in English.

RULES
- You are the controller: delegate implementation to pi router-env/my-coding, reviews to read-only referees. Park out-of-scope findings in the ledger.
- Reply in English, write every artifact in English, no attribution lines in commits or PRs.
- Use gh yourself for variables, secrets and settings; ask only for web-only auth or secret values.
- Stop and ask only for destructive or outward actions not listed here, or user gates: Copilot spike and tokens (COPILOT_GITHUB_TOKEN, AUDIT_BOT_TOKEN), dispositions of commands and agents (plan 7 Task 3), upstream proposals, the Orwell port.
- Pid files and background watchers live outside the workspace; tell fixers to ignore any pid file or pi process and never wait on one.
- After a compaction, re-read this section, the current plan and its ledger; resume from git log, not memory.
```

## What we learned (apply to every plan)

1. **Verify names against the real branch.** Plan reviews caught interfaces that no plan produced; check each cited file, flag and job in the worktree that owns it.
2. **Reusable workflows:** inside a called workflow `github.event_name` is the caller's event; detect "called" by an input such as `head_sha`.
3. **Batch the fixes.** Small batches (3 artifacts, 15 findings), one dispatch per artifact, three rounds then re-queue; plan 4 left 359 findings by doing it in one wave.
4. **Fixers:** a fixer deadlocked on a pid file it found in the workspace and waited for itself; keep pid files in `/tmp`, tell the fixer to ignore them, and wait by PID, never `pgrep -f` (it matches itself).
5. **Plan patching scripts** must tolerate a missing anchor; an aborted script left plans half patched.
6. **History:** compact with a tree-identity check and a backup branch; force-push only with `--lease` and only your own branch. A git ref cannot be both `x` and `x/y`.
7. **Registry, not new files:** review dates extend `docs/audit/upstream-sources.json`; relax its validator once, in one place.
8. **Plugin bundling:** a command's plugin only ships the skills listed in `marketplace.json`; a command that points at another skill's file must bundle that skill.
9. **Third-party sources:** unreachable is not "no change"; a moved path is its own status.

## Open for the user

Dispositions for commands and agents (after plan 7); upstream proposals; Orwell port; Copilot spike and tokens; whether to run plan 5 Phase 2 once the spike inputs exist; `skill-audit-plan` worktree (unmerged old plan drafts, kept).
