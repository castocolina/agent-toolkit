---
description: Prepare prompt_to_codex.md so the user can run Codex themselves and get an implementation plan in codex-plan.md. Use when the user wants Codex to write a plan, or a plan handed off to another agent, for a feature, API, auth change, migration, refactor or test strategy, including underspecified requests. Gathers repo context, asks only blocking questions, shows the manual `codex exec` command. Not for in-session planning without a Codex handoff, not for implementing changes; never runs Codex.
argument-hint: "<what to plan> [--model <id>]"
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# Codex Plan

Build a self-contained prompt that a user-run Codex session turns into `codex-plan.md`. You write the prompt and show the command; you never run Codex.

Request: `$ARGUMENTS`

If the request is empty or only `--model <id>`, ask for the planning topic with AskUserQuestion before step 1; never build a prompt with no objective.

If it contains `--model <id>` (if no id follows, or the next token reads like part of the topic, ask for the id with AskUserQuestion, and drop the flag only if the user declines; never pass `-m` empty or guessed), strip it from the topic and pass it to Codex with `-m <id>`. Without it, Codex uses its configured default model (a hard-coded id goes stale).

## Workflow

1. **Context first.** Read what the plan depends on. Start with the manifest (`package.json`, `pyproject.toml`), the schema or models, type definitions, existing tests (to show the testing pattern), the entry points and middleware the topic touches, and `.env.example`; stop after about 10 files, preferring files a task would edit over files that only document. `## Files to Read for Context` lists ONLY existing paths verified with `ls`/Read; a planned or new path (for example a file the plan would create) goes in the task list, never in that section.
2. **Readiness gate.** Sort what you know into confirmed requirements, blocking decisions (they change the plan's shape: stack, scope, auth method) and non-blocking assumptions. Test for blocking: would Codex produce a structurally different phase list under each answer? If not, it is an assumption.
   - Ask the blocking decisions with AskUserQuestion, one batch, only what the request and repo do not already answer. Three to six is an upper range, not a quota; zero is fine.
   - Record each remaining assumption explicitly in the prompt.
   - If a blocking question goes unanswered or is declined, pick the most conservative option, record it as an assumption in the prompt, and say so in your reply.
3. **Name the files.** Default `prompt_to_codex.md` and `codex-plan.md`. If either exists, ask whether to overwrite or use a numeric suffix (`-2`, `-3`, ... until both names are free); never overwrite silently. Use the chosen names in the prompt, the command and the request below. Also fix the exact exclusion pathspec for the chosen plan file now (for example `':(exclude)codex-plan-2.md'`) and use it unchanged in steps 5 and 7.
4. **Write the prompt** (below) and confirm the file exists (`test -s`). On failure report the exact error, give the prompt inline or ask for a writable directory, and do not present the command as ready.
5. **Record a baseline.** Inside a git repo, in the directory the command will run in (each Bash call is a new shell: no variables survive), run `B=$(mktemp); echo "$B"`, tell the user that path and record it as a literal. Then run this one line with the literal path:

```bash
set -o pipefail; { git status --porcelain=v1 -uall -- . ":(exclude)<plan file>" && git diff HEAD -- . ":(exclude)<plan file>" | sha256sum && git ls-files -o --exclude-standard -z -- . ":(exclude)<plan file>" | xargs -0 -r sha256sum; } > "<literal path>" || echo "baseline failed: change verification unavailable"
```

   It is content-aware for tracked and non-ignored untracked files; ignored files are not covered. The chosen plan file is excluded so its creation is not flagged. Outside git, or if the line prints the failure message, say change verification is unavailable. Run `git rev-parse --verify -q HEAD` first:
   - Unborn repo (it prints nothing): skip the line above and run this reduced line instead, with the same literal path and the same `<plan file>` exclusion (without it the new plan file is always flagged as a change), saying verification is limited to it; step 7 then runs this same reduced line. A printed failure message always means verification is unavailable.

```bash
git status --porcelain=v1 -uall -- . ":(exclude)<plan file>" > "<literal path>" || echo "baseline failed: change verification unavailable"
```

   - Fix the exact pathspec once in step 3 (for example `':(exclude)codex-plan-2.md'`) and reuse it unchanged here and in step 7, so both runs are byte-identical.
6. **Show the command, then stop.**

```bash
codex exec -s workspace-write -c model_reasoning_effort=high [-m <id>] "$(cat prompt_to_codex.md)"
```

`-c model_reasoning_effort=high` is a config override (https://learn.chatgpt.com/docs/config-file/config-reference, checked 2026-11-08); the accepted values depend on the model, so if `high` is rejected read the live list with `codex exec --help` and `codex debug models`.

Add `--skip-git-repo-check` (https://learn.chatgpt.com/docs/non-interactive-mode, checked 2026-11-08) only when `git rev-parse --is-inside-work-tree` fails. `-s workspace-write` lets Codex create the plan file but also write anywhere in the workspace, so the planning-only instruction is the only guard against source edits.

State the directory the command must run from (it uses relative paths).

Ask the user to send you the content of `codex-plan.md` when Codex finishes. Do nothing else until they do, and never guess what the plan says. If Codex fails or wrote no file, ask for its output; do not rerun it yourself.
7. **Review the plan.** When it arrives, run the same line from step 5 (same `<plan file>` exclusion) into a second `mktemp` file (literal path again, same directory): copy the completed baseline line verbatim from your step-5 Bash call and change only the output path, so both runs are byte-identical; then `diff` the two literal paths (or ask the user to). Flag any difference. Then review the plan: every task Location path exists or is marked new; Dependencies form no cycle; every confirmed requirement maps to a task with acceptance criteria. List gaps; do not implement unless asked.

## Prompt contents

- Objective, confirmed requirements, exclusions, constraints, stated assumptions.
- `## Files to Read for Context`: verified paths only, each with a one-line reason; Codex reads them first.
- Plan structure: Overview, Prerequisites, Phases with tasks, Testing Strategy, Dependency Graph, Risks, Rollback (drop sections that do not apply, e.g. Rollback for a test-strategy plan). Every task carries Location (file paths), Description, Dependencies (task IDs, so work can run in parallel), Complexity 1-10, Test-First Approach and testable Acceptance Criteria.
- Instructions: write the prompt and plan in English unless the user asks otherwise; write the full plan to the chosen plan file in the current directory; do NOT ask clarifying questions; put code snippets only where they help; begin immediately. State: "This is planning only. Do not implement changes or modify source, configuration, dependencies or data. Write only the chosen plan file; describe implementation and validation steps without executing them."

Put this skeleton in the prompt's plan-structure part, filling the brackets from the request:

```
# Plan: [Task name]
**Generated**: [date]   **Estimated Complexity**: [Low/Medium/High]
## Overview
[Summary and general approach, including recommended libraries and tools]
## Prerequisites
[Dependencies, tools or access needed first]
## Phase 1: [Phase name]
**Goal**: [What this phase accomplishes]
### Task 1.1: [Task name]
- **Location**: [file paths or components]
- **Description**: [what to do]
- **Dependencies**: [task IDs, e.g. "None" or "1.2, 2.1"]
- **Complexity**: [1-10]
- **Test-First Approach**: [tests to write before implementation, and what each verifies]
- **Acceptance Criteria**: [specific, testable criteria]
## Testing Strategy
- **Unit Tests**: [what to unit test, frameworks]
- **Integration Tests**: [API and service integrations]
- **E2E Tests**: [critical user flows]
- **Test Coverage Goals**: [target percentage per level]
## Dependency Graph
- Tasks with no dependencies (can start in parallel): [list]
- Dependency chains and the critical path: [show]
## Potential Risks
[What could go wrong, with a mitigation each]
## Rollback Plan
[How to undo the changes]
```

Add these task guidelines to the prompt: each task is specific and actionable, has clear inputs and outputs, is independently testable, names file paths and code locations, lists its dependencies so work can run in parallel, and carries a complexity score; specify the tests to write before implementation (test-driven). Break large tasks down, for example:

- Bad: "Implement Google OAuth"
- Good: "Add the Google OAuth settings to the environment variables", "Install and configure the OAuth library chosen in the plan", "Create the OAuth callback route handler", "Add a Google sign-in button to the login UI", "Write integration tests for the OAuth flow"

Illustrative excerpt for `/codex-plan help me implement auth` (paths are examples: replace them with verified ones):

```
## Files to Read for Context
- `package.json` - framework and dependencies
- `prisma/schema.prisma` - existing models
- `src/middleware.ts` - current request handling
```

## Gotchas

- Never add `--full-auto` or `-s danger-full-access`: they widen the sandbox or skip approvals. `--full-auto` also errors now on codex-cli 0.162.1 ("unexpected argument '--full-auto' found"); the Codex docs say to use `--sandbox workspace-write` (https://learn.chatgpt.com/docs/non-interactive-mode, checked 2026-11-07).
- Do not run `codex`: the user chose manual execution, and an unattended run could write files and spend quota unreviewed.
- `--output-last-message` (`codex exec --help`; https://learn.chatgpt.com/docs/non-interactive-mode, checked 2026-11-08) saves Codex's final reply, not `codex-plan.md`; do not use it to claim the plan exists.
- Copy environment key names (from `.env.example`) into the prompt, never live secret values: the prompt file is plain text on disk.
- A planning run reads context and writes only the plan: no package installs, external calls or test runs. Network access depends on Codex configuration, so do not rely on the sandbox to block execution.
- The command uses relative paths: run it from the directory holding `prompt_to_codex.md`, or `$(cat ...)` fails and the plan lands elsewhere.
