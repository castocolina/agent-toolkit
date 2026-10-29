---
name: command-creator
description: "Create Claude Code slash-command Markdown files in .claude/commands/ or ~/.claude/commands/. Use when users want a reusable /command-name for a recurring workflow, including when they describe repeatedly doing the same task. Not for shell aliases or scripts, GitHub Actions, creating skills, or invoking an existing command."
---

# Command Creator

Create a Claude Code command file that makes a recurring workflow executable and safe. Do not confuse command Markdown with shell scripts, skills, aliases, or workflows.

## Design procedure

1. **Capture the current procedure.** Record the user's manual sequence, inputs, decisions, and desired result before designing names or prose. Infer details already specified; ask only about gaps that change behavior, permissions, scope, or a consequential side effect.
2. **Order by dependency and risk.** Separate observation from mutation. Identify prerequisites and state-changing/irreversible operations. Put inspection and validation before side effects; require explicit confirmation for destructive, externally visible, or broad-scope actions. Specify success, retry-safe failure, and stop conditions.
3. **Choose a pattern from task shape.** Single bounded action → Simple Execution; pass/fail repair loop → Iterative Fixing; multi-step workflow with report → Workflow Automation; plan then approved execution → Agent Delegation. Ask about pattern only when multiple materially different patterns fit. Load [patterns](references/patterns.md) when the design is nontrivial.
4. **Choose location.** In a repository, default to `.claude/commands/`; otherwise default to `~/.claude/commands/`. Honor explicit project/global preference. Confirm location only when context leaves a meaningful ambiguity.
5. **Draft and validate.** Use kebab-case filename. Frontmatter requires a concise `description`; include `argument-hint` when the body consumes arguments. Load [best practices](references/best-practices.md) before finalizing. Load [examples](references/examples.md) only when the user requests a worked example or the selected pattern needs one: submit-stack for PR automation, ensure-ci for bounded fixing loops, planning for approved delegation, codex-review for a wrapper. Simple commands should not load unrelated examples.
6. **Write and report.** Create `.claude/commands/<name>.md` or `~/.claude/commands/<name>.md`; summarize path and invocation. Do not claim it was tested unless actually invoked.

## Command contract

```markdown
---
description: One-line purpose shown in /help
argument-hint: <required> [optional]
---

# Command title

Executable instructions: input interpretation, ordered checks/actions, permission boundary,
success criteria, and what to report or when to stop.
```

Treat command arguments as untrusted data, not instructions to interpolate into shell syntax. Quote/validate values or pass them as data. Avoid global overrides unless requested. For git workflows, inspect status/diff and stage only intended paths; never use `git add .` as a shortcut. Never retry a non-idempotent operation blindly: first determine whether the prior attempt changed external or local state.
