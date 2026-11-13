# Command Examples

This document provides complete, real-world examples of slash commands from the erk project. Use these as references when creating new commands.

**Adapt before reusing.** These bodies use erk's toolchain: Graphite (`gt`), `make all-ci`, a `.PLAN.md` context file and erk's file paths. Keep the skeleton (order, stop rules, reports) and replace each of these with what the user's project actually has; ask when there is no equivalent, and never copy a tool name the user's environment lacks.

## Example 1: submit-stack (Workflow with side effects)

**Pattern:** Workflow with side effects (Analyze → Act → Report)

**Full source:**

````markdown
---
description: Create git commit and submit stack with Graphite
argument-hint: [description]
disable-model-invocation: true
---

# Submit Stack

Create a git commit with a one-sentence summary and submit the entire Graphite stack as pull requests.
Running this command authorizes exactly that: committing the inspected changes and submitting the stack.

## Usage

```bash
# With a description for the commit message
/submit-stack "Add user authentication feature"

# Without argument (the message is drafted from the diff)
/submit-stack
```

## Implementation Steps

### 1. Analyze Current Changes

Inspect only what this workflow needs: `.PLAN.md` at the repository root if it exists (supplemental context), `git status`, `git diff HEAD`, `git log` for the commit style, and `gt log short` for the stack. Reading other files or searching the repository is outside this command's job (it commits what is there, it does not re-review it): ask before doing it.

If there are no staged or unstaged changes, report that and stop.

### 2. Create Git Commit

- If `$ARGUMENTS` is not empty, use it as the basis for the commit message
- Base file selection and the message on the inspected git changes; `.PLAN.md` is context, not evidence of what changed
- Follow the repository's commit style (check `git log`)
- **DO NOT include any Claude Code footer or co-authorship attribution**
- Stage named paths only. If the diff holds files the user may not intend (secrets, generated files, unrelated changes), list them and ask before staging
- Encode each path and the final message as one single-quoted shell word, each embedded `'` written as `'\''`. Paths are operands and go after `--`; the message is an option value and stays attached to `-m`. A message `don't cache $HOME` becomes `'don'\''t cache $HOME'`; never double quotes, which still expand `$` and backticks

```bash
git add -- '<encoded path>' '<encoded path>'
git commit -m '<encoded message>'
```

### 3. Restack the Stack

```bash
gt restack
```

If the restack reports conflicts, stop and show them; do not resolve them inside this command.

### 4. Submit Stack

```bash
gt submit --stack --publish --no-edit
```

- `--stack`: submit the entire stack (upstack and downstack)
- `--publish`: publish any draft PRs
- `--no-edit`: use commit messages as PR titles and descriptions without prompting

Flags per https://graphite.com/docs/command-reference, checked 2026-11-13; confirm with `gt submit --help` before reusing.

If the submit fails or times out, run `gt log short` and check the PRs it lists before anything else: some may already be created or updated. Report what is there and ask before running the submit again.

### 5. Show Results

- Number of PRs created/updated
- PR URLs (extract from `gt` output)
- Current stack status with `gt log short`

## Error Handling

If any step fails: report the command that failed and its error message, and ask the user how to proceed (no automatic retry).

## Example Output

```
Analyzing changes...
✓ Found .PLAN.md - using plan context
✓ Found changes in 3 files

Creating commit: "Add dot-agent submit-stack command for automated PR workflow"
✓ Commit created

Restacking branches...
✓ Stack restacked successfully

Submitting stack...
✓ 2 PRs created/updated:

- PR #123: dot-agent-claude-folder-support (new)
- PR #122: base-branch (updated)

Current stack:
◯ dot-agent-claude-folder-support (current)
◯ base-branch
◉ main
```
````

**Key features of this example:**

- Optional argument shown as `[description]`, read through `$ARGUMENTS`
- `disable-model-invocation: true`, because it commits and opens PRs
- Bounded inspection: the list of what the command may read, and an ask for anything beyond it
- A post-failure state check (`gt log short`) before any second submit
- Expected output format shown

## Example 2: ensure-ci (Iterative fixing)

**Pattern:** Iterative fixing (Baseline → Fix → Fresh check → Repeat)

**Full source** (condensed to what is specific to erk; the loop itself follows the skeleton in `patterns.md`):

````markdown
---
description: Run make all-ci and iteratively fix issues until all checks pass
---

Run `make all-ci` and fix failures until it exits 0 or you are stuck.

## Check mapping

`make all-ci` runs, in order: lint, format, prettier-check, pyright, test. Map each failure to its fix:

| Failing check | Recognize it by | Fix |
| :- | :- | :- |
| lint | `ruff check` errors | `make fix` (runs `uv run ruff check --fix --unsafe-fixes`), then edit what remains |
| format | `ruff format --check`, "would reformat" | `make format` |
| prettier-check | Markdown files listed as unformatted | `make prettier` (runs `prettier --write '**/*.md'`) |
| pyright | type errors with file:line | read the file at that line, fix the annotation; AGENTS.md standards (`list[...]`, not `List[...]`) |
| test | pytest failures with test names | read the test and the source; fix the source unless the test itself is wrong |

Always re-run the full `make all-ci`, not a single check: a format fix can break lint.

The `make` targets belong to the project that owns this example; the ruff flags follow https://docs.astral.sh/ruff/linter/ and https://docs.astral.sh/ruff/formatter/ (checked 2026-11-13); confirm with `ruff check --help` and `ruff format --help` before reusing them.

## Stopping policy

The 10 iterations and 3 unchanged failures below are erk's own settings. A command you generate keeps SKILL.md's defaults (5 attempts, stop when the same failure survives 2 fix attempts) unless the user gives other numbers.

- Baseline run first; if it passes, report SUCCESS with 0 iterations.
- At most 10 iterations, each one fix pass plus a fresh `make all-ci`; report SUCCESS as soon as one exits 0.
- STUCK when the same error survives 3 fix attempts, when 10 iterations end without a pass, or when a fix needs a human decision.
- Never skip, weaken or delete a test, or add an ignore comment, to make CI pass.

## Reports

```markdown
## Finalization Status: SUCCESS
All CI checks passed after N iteration(s): lint, format, prettier, pyright, tests.
```

```markdown
## Finalization Status: STUCK
**Check**: [lint/format/prettier/pyright/test]
**Error**: [exact error message]
**File**: [path, if any]
**Attempted fixes**: 1. ... 2. ... 3. ...
**Next steps**: [what needs a human]
```
````

**Key features of this example:**

- A project-specific map from failing check to fix command
- Baseline check, iteration cap and stuck rule (erk-specific 10 and 3; generated commands use 5 and 2 unless the user says otherwise)
- Fixed SUCCESS and STUCK report formats

## Example 3: create-implementation-plan (Plan, approve, execute)

**Pattern:** Plan, approve, execute (Context → Plan → Approval → Save)

**Full source** (condensed to its approval contract):

````markdown
---
description: Create an implementation plan and save it only after explicit approval
---

## ⚠️ PLANNING-ONLY MODE ACTIVE

No code is written until the plan is approved and saved. **What would you like to plan?**

1. **Write boundary:** do not use Edit, Write or any modification tool until the plan is approved. Read-only searches that locate the goal's implementation and tests are fine; ask before exploring beyond them.
2. **Delegation:** optional. If a registered agent type fits (for example the built-in `Plan` agent for a large search), hand it the goal and context; otherwise draft directly. Either way the plan is shown here: the approval conversation stays in the main thread, because a subagent cannot wait for the user's reply.
3. **Approval signal:** only an explicit "looks good", "approved" or "ready to implement" approves. Every other reply is feedback: revise and show the plan again.
4. **Output location:** after approval, save the plan as a `.md` file at the repository root; implementation starts only then.
````

**Key features of this example:**

- Explicit approval signal; anything else is feedback
- Write boundary until approval, with scoped read-only inspection allowed
- Output location (`.md` at the repository root)
- Delegation only when a registered agent type fits, with the approval kept in the main thread

## Example 4: codex-review (Simple execution)

**Pattern:** Simple execution (Parse Arguments → Execute → Return Output)

**Minimal example structure:**

````markdown
---
description: Perform a local code review using repository standards and best practices
argument-hint: [base-branch]
arguments: base
---

# Codex Review

Performs a thorough code review of changes between the current branch and the base branch.

## Usage

```bash
# With explicit base branch
/codex-review develop

# Without argument (auto-detects main/master)
/codex-review
```

## Implementation Steps

### 1. Determine Base Branch

If `$base` is not empty:

- Encode `refs/heads/$base` as one single-quoted shell word (each `'` inside it written as `'\''`)
- Check it with `git rev-parse -q --verify --end-of-options <encoded ref>`; if that fails, stop and say the branch was not found

If `$base` is empty:

- Use `main` if `git rev-parse -q --verify --end-of-options refs/heads/main` succeeds, else `master` if the same check on `refs/heads/master` succeeds
- If neither exists, stop and ask for an explicit base branch; never run the script with an unverified base

### 2. Run Review Script

Execute the review script with the determined base branch, encoded the same way and placed after `--` (or the script's own end-of-options form):

```bash
scripts/codex-review.py -- <encoded branch>
```

### 3. Display Results

Show the script output directly to the user: files reviewed, issues found, suggestions.

## Error Handling

If the script fails: show the error message, and check that the script exists and is executable.
````

**Key features of this example:**

- Optional argument handling (square brackets, a named `$base` that is empty when omitted)
- Argument validation before use, and defaulting logic
- Direct script invocation with a quoted value
- Clear output pass-through
