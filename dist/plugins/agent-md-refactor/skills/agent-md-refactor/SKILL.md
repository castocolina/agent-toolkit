---
name: agent-md-refactor
description: Refactor existing bloated, conflicting, or repetitive AGENTS.md, CLAUDE.md, COPILOT.md, and similar coding-agent instruction files into a minimal root plus focused, conditionally loaded topic documents. Use when instructions are too long, inconsistent, hard to maintain, or need progressive disclosure, even when asked to clean up agent config. Not for READMEs, general developer documentation, or creating a new instruction system from scratch.
license: MIT
---

# Agent instruction refactor

Reduce context cost without changing instruction meaning, precedence, or scope. Resolve contradictions before extracting anything: a contradiction changes what counts as essential. Preserve unresolved rules verbatim with their original scopes, report the conflict, and defer affected extraction. Introduce conditional scopes only when supported by existing instructions or an explicit user decision.

## Procedure

If instruction files or repository evidence are unavailable, do not stop at a request for them. State the assumption that the current instructions are unknown, then give the concrete refactor checklist or candidate commands/topics to review without claiming they are obsolete or inventing their contents. When the user says the file has obsolete setup commands, list the setup, install, build and run commands under a “Review for removal” heading as candidates, name the evidence that confirms each (package scripts, CI config, lockfiles), and do not propose replacements.

1. Read every relevant instruction file, including scoped/ancestor files. Inventory each rule with source file, directory scope, exceptions, and precedence.
2. Identify contradictions and ask for a decision when precedence cannot be derived from existing instructions. Do not silently choose a preferred rule.
3. Keep in the root only instructions that truly apply to nearly every task: project identity, critical overrides/safety constraints, and essential commands. Preserve universal constraints even if the result exceeds a suggested length. A concise guide may need no split.
4. Group remaining actionable rules by topic while preserving their source scope and exceptions. Create focused files under `.claude/` by default; use `docs/agent-instructions/` only if the repository has no `.claude/` directory. Avoid unnecessary file counts and generic template scaffolding.
5. Add links with explicit read conditions, e.g. “Read `.claude/testing.md` before changing or writing tests.” Plain Markdown links are not automatic imports: confirm the target harness follows links when applicable. Claude Code auto-loads the root instruction file; linked files require the agent to follow the stated condition.
6. Remove only rules proven redundant, obsolete, or non-actionable. Do not delete project-specific safety overrides as presumed defaults.
7. Verify every moved rule against the inventory (source, scope, precedence, exception), check every Markdown link resolves to an existing target, and confirm the target harness will load conditional guidance when relevant. Identify obsolete commands or instructions for review/removal only when repository evidence shows they are obsolete; do not guess replacements. Report removed rules and unresolved decisions.

## Gotchas

- Flattening a directory-specific exception into global guidance changes behavior in other directories.
- A project-specific safety override may be essential even if another environment treats it as default; verify before pruning.
- Moving text without preserving precedence can reverse which instruction wins.
- Claude Code does not automatically load arbitrary files under `.claude/`; links must say when the agent must read them.

## Templates

Read `references/templates.md` only when a compact root/linked-file example is useful for the refactor.
