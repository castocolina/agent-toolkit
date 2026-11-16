# How each harness loads instruction files

Read this before choosing where a topic file lives or how the root links to it. Loading rules change between releases, so verify on the live page before relying on a detail; the values below were checked 2026-11-15.

Sources: Claude Code, "How Claude remembers your project" (https://code.claude.com/docs/en/memory); GitHub Docs, "Support for different types of custom instructions" (https://docs.github.com/en/copilot/reference/custom-instructions-support).

## Claude Code

- `.claude/rules/*.md` (recursive): a file without `paths:` frontmatter loads at launch, like `.claude/CLAUDE.md`. A conditional topic file placed there loses progressive disclosure. A rule with `paths:` frontmatter (a glob list) loads on demand, when Claude reads a matching file, so it suits file-type topics such as testing rules for test files.
- Other files under `.claude/` (for example `.claude/testing.md`) load only when the agent reads them, so the root link must state the read condition.
- `@path` imports load eagerly with the importing file, so they organise a file but do not cut its context cost. A plain Markdown link with a read condition does cut it. The docs page states the import depth limit.
- `AGENTS.md` is read by Claude Code only when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the working directory or above (v2.1.277 or later per the page https://code.claude.com/docs/en/memory, checked 2026-11-15; verify on the live page). A `CLAUDE.md` that contains `@AGENTS.md` shares one file across tools.
- The docs page also gives the size guidance (a target per CLAUDE.md file) and the startup warning for long files; read the live value there.

## GitHub Copilot

Per the support table on the docs page above, Copilot reads `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md` and, depending on the product (cloud agent, code review, CLI, VS Code Chat), `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (and `REVIEW.md` for code review). Copilot does not read a `COPILOT.md`. Check the table for the product the user targets.
