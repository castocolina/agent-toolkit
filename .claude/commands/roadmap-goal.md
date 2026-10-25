---
description: Drive a multi-plan roadmap end to end - two-lane plan review, execution, two-lane code review, skill grading toward 90%, stacked PRs
argument-hint: <roadmap.md> [--plans N[,M...]] [--lanes opus,pi:router-env/my-referee-one]
---

# Roadmap Goal

Take a roadmap that lists ordered plans and carry each plan from reviewed document to an open, reviewed PR, autonomously. This file is the process; plans and skills never encode it (lanes and models are chosen here, at run time).

## Usage

```bash
/roadmap-goal docs/plans/2026-10-24-00-roadmap.md
/roadmap-goal docs/plans/2026-10-24-00-roadmap.md --plans 3,4
/roadmap-goal docs/plans/2026-10-24-00-roadmap.md --lanes opus
```

- `<roadmap.md>`: the roadmap; its "Plans, in execution order" table is the work list.
- `--plans`: only these plan numbers (default: every plan without a merged PR, in order).
- `--lanes`: judging/review lanes. Default `opus,pi:router-env/my-referee-one` (one native Claude Code Opus subagent, one pi model). `opus` alone means a single unbiased native subagent.

## Operating rules (apply to every step)

- **Autonomy.** Run without check-ins. Stop and ask only for: a destructive or irreversible action, an outward action the user has not approved in this run (merging, touching `main`, force-pushing anything but a PR branch), a decision only the user can make (it changes a recorded user decision), or a loop that hit its cap without converging. Settle simple decisions and classify doubts with the `jev-fast-decision` skill; when it returns `needs_fallback`, decide yourself. Record every decision in the plan's ledger as `Ruling: <what> — <why> — <cost if wrong>`.
- **Language.** All artifacts in English (see `AGENTS.local.md`).
- **Process vs artifacts.** Never write lane names, judge counts or this process into plans or skills; they carry only their own rules.
- **Workspace.** One worktree per plan under `.claude/worktrees/<branch-slug>/` (gitignored). Plan N+1's branch starts from plan N's branch (stacked PRs). Never commit to or force-push `main`.
- **Subagent output.** Save every reviewer/judge report to disk VERBATIM before merging; `merge-reports` parses `- **title** — Location: … . Required: … Why: …` and silently drops reports whose separators were rewritten.

## Polling pi and other CLI lanes

- Always pass the prompt on **stdin** (`pi -p … < prompt.txt`), never as an argument: `pi -p` also reads a non-TTY stdin and blocks forever on an inherited pipe or socket.
- Restricted lanes: judges `--tools read,grep,find,ls --no-mcp --no-extensions --no-skills --no-context-files`; eval runners `--no-tools` plus the same flags (in this repo, take them from `python3 scripts/audit/audit.py pi-cmd judge|runner --print0`).
- Run long CLI calls in the background and wait for their completion (exit file or process exit), never short polling loops. A run with no output, ~0 CPU (`ps -o time`) for 10+ minutes and fd 0 on a socket is hung: kill it and re-run with the prompt on stdin.
- `ai-kit`'s supervised runner `cross-ai.mjs` (timeouts, stall detection, retry ladder, `AIKIT-XAI` status line) is preferred once it can express the restricted flags; check its current contract (ai-kit Phase 25.1) before relying on it.
- Sessions you start yourself in Herdr: monitor with `herdr agent wait <name> --until working` then `herdr agent wait <name>`; read with `herdr agent read <name> --source recent-unwrapped`.

## Implementation Steps

### 1. Load the roadmap

Read the roadmap's order table, Decisions, Global Constraints and interface-ownership table. Build the work list from `--plans` or the first plan without a merged PR. Expected: an ordered list of plan files.

### 2. Review each plan before implementing (repeat per plan)

1. Use the `ai-kit-spec-review` skill on the plan (archetype `plan`, framework profile superpowers, grounding doc = the roadmap). Configure the lanes from `--lanes`: the native lane is the `Agent` tool with `model: opus`; a `pi:<model>` lane is a project-local `.aikit/review-spec.toml` custom entry `pi -p --model <model> --tools read,grep,find,ls {prompt}` in `double` mode (trust it with `ai-kit-spec.py trust-local` when its content is unchanged from a config the user already trusted).
2. Merge both reports, revise through `superpowers:writing-plans`, and iterate while CRITICAL + HIGH (deduplicated across lanes) is 3 or more. Past the skill's iteration cap, keep iterating under this rule; if the count stops falling for two rounds, stop and ask.
3. When only MEDIUM/MINOR remain, apply them with one direct revise and no re-review. Commit the plan (`docs(plan): …`) on the plan's branch.

### 3. Execute the plan

1. Create the plan's worktree and branch (stacked on the previous plan's branch).
2. Use the `ai-kit-spec-execute` skill (it routes a superpowers plan to `superpowers:subagent-driven-development`): sonnet implementers, one task review each, the 5-round fix loop, the ledger in `.superpowers/sdd/<plan>/progress.md`.
3. If a task needs a fresh session (for example a new `.claude/agents/*.md` must load), use the `herdr` skill: split a pane with `--cwd <worktree> --no-focus`, `herdr agent start <name> --kind claude --pane <id>`, answer its trust prompt for the user's own files, and prompt it with a resume instruction naming the plan, the ledger and the resume step. Keep monitoring it until it reports.

### 4. Grade every skill the plan ships

Judge each shipped skill with `skill-judge` through every lane in `--lanes`, validate and merge the verdicts with the repo tooling (`audit.py validate-verdict` / `merge`), and run its evals. Target: merged score close to 90% (Grade A); 80% is only the floor. Run fix rounds (max 3) aimed at the lowest-scoring dimensions until the target is reached; stop and report what blocks a skill that stays below 90 after 3 rounds.

### 5. Review the code

Use `superpowers:requesting-code-review` with every lane on the same prompt file (native subagent on the most capable model, pi with read-only flags and the prompt on stdin). Dispatch ONE fix wave for all findings, then one scoped re-review. Park residual minors in the ledger with rulings.

### 6. Ship as a stacked PR

1. `git push -u origin <branch>`.
2. Use `commands/explain-pr-changes.md` only to write the PR body to a file; it must not create the PR.
3. `gh pr create --repo castocolina/agent-toolkit --base <previous plan's branch, or main for the first> --head <branch> --title "<conventional title>" --body-file <file>`. Expected: a URL under `https://github.com/castocolina/agent-toolkit/pull/`.
4. Never merge. The user squash-merges bottom-up; after a squash, rebase the next branch with `git rebase --onto main <old-base> <branch>` and force-push only that PR branch.

### 7. Report

Per plan, report in one short message: PR URL, merged grades per skill, eval results, review outcome, the ledger's `Ruling:` lines, and anything still open. Then continue with the next plan.

## Error Handling

- A lane fails or returns no `### Status:` line: re-run it once; still failing → continue with the remaining lane and say so in the report.
- A verdict fails `validate-verdict` (wrong totals, stale rubric): delete it and re-run that judge once.
- The fix loop hits its cap with open CRITICAL/IMPORTANT findings that later tasks build on: rule on the smallest unblocking change and ledger it; stop only if every path forward is a guess.
