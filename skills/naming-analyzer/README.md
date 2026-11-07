# Naming Analyzer Skill

A skill for Claude Code that reviews code identifiers and suggests clearer names. It reads the implementation and call sites before proposing a rename, and rates each suggestion by confidence and compatibility risk, so a rename that would break a JSON key, a database column, or a string-keyed lookup is flagged instead of recommended blindly.

The review rules, decision table, hidden-consumer list and report format live in [SKILL.md](SKILL.md); this file only covers what the skill is for and how to install it.

## What it does

- Flags names whose behavior contradicts their promise (a getter that writes, a duration called `expiresAt`).
- Surfaces hidden units, time bases, nullability and boolean polarity problems.
- Checks names against the project's own conventions, falling back to the language's dominant convention when the project has none.
- Returns a prioritized rename table, including rows where keeping a name is the right call.

It never edits files. Apply the approved renames with your IDE's rename feature or a codemod tool such as LibCST.

## Example prompts

- "Review the naming in `src/services` before I open the PR."
- "Is `getAccount` misleading if it also saves?"
- "Is it safe to rename `usr_nm` to `user_name` in this model?"

## Installation

**Claude Code:**

```bash
cp -r skills/naming-analyzer ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste the contents of `SKILL.md` into the conversation.

## Evals

`evals/evals.json` holds output evals (fixtures in `evals/files/`), and `evals/trigger-queries.json` holds trigger queries, including near-miss requests that should go to a rename or migration tool instead.

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Framework and language facts (PEP 8, Effective Go, TypeScript style guides, Protocol Buffers, Django, SQLAlchemy, Spring, pytest, Celery, RQ, NestJS, Angular and others) were checked against their official documentation.

Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-07): Python Software Foundation, Python Packaging Authority, The Go Authors, Microsoft, Django Software Foundation, SQLAlchemy authors, Broadcom (Spring), pytest-dev, Vercel, Rails contributors, Celery Project, Google (Angular), Pydantic Services, FasterXML, Instagram (Meta).
