# Requirements Clarity

A skill that turns a vague feature request ("add login", "improve onboarding") into a Product Requirements Document through short, scored question rounds, so that every acceptance criterion traces to a decision someone owns.

The routing rule, workflow, scoring rubric, conflict rule and gotchas live in [SKILL.md](SKILL.md); this file only covers what the skill is for and how to install it.

## What it does

- Decides whether a request needs clarification at all; a named file is context, not a spec.
- Reads the repository for technical facts and asks the user only for product decisions.
- Scores clarity per category, asks 2–3 high-impact questions per round, and keeps a decision log with sources.
- Surfaces contradictions between rounds and stakeholder disagreements instead of silently resolving them.
- Writes the PRD to `./docs/prds/{feature-name}-v{version}-prd.md`, or into chat when saving is not possible or not wanted.

## Files

- `SKILL.md`: routing, workflow, pre-save check, rubric with anchors, gotchas.
- `references/prd-template.md`: PRD layout, read only when generating the document.

## Example prompts

- "We need a login feature. Help me figure out what to build before anyone codes."
- "Leadership wants better onboarding by Q3 and eng keeps asking me what that means. Help me pin down scope."
- "Here are our notes from three rounds on the CSV export; write the PRD."

## Related skills

- `game-changing-features`: deciding what to build next.
- `gepetto`: implementation plans once requirements are clear.
- `frontend-to-backend-requirements`: data needs a frontend has from a backend.

## Installation

**Claude Code:**

```bash
cp -r skills/requirements-clarity ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste the contents of `SKILL.md` into the conversation.

## Evals

`evals/evals.json` holds output evals (session-note fixtures in `evals/files/`), and `evals/trigger-queries.json` holds trigger queries, including requests that name a file but are fully specified and should not load this skill.
