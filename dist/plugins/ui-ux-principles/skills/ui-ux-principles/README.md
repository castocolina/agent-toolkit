# ui-ux-principles

Eight UI/UX rules to apply while building a screen and to run as a review checklist. Works in any framework (React, Vue, Svelte, plain HTML/CSS, MUI, Tailwind). Not for backend work, copywriting or brand design.

## Install

```bash
cp -r skills/ui-ux-principles ~/.claude/skills/
```

## Rules

| id | in one line |
|----|-------------|
| `loading` | Skeletons that match the final layout; spinners only inside one module; submits disable while pending |
| `responsive` | Mobile-first, verified at 360, 768, 1280 and 1920 px |
| `hierarchy` | At most one filled button per view; outlined and text never count; destructive never filled |
| `tokens` | Colors, type, spacing, radii and shadows defined once and consumed everywhere |
| `consistency` | One visual language; dark mode through the same tokens |
| `a11y` | Alt text, accessible names, contrast, target size, keyboard operation (WCAG 2.2 figures) |
| `states` | Empty, error with recovery, and success states |
| `interaction` | Hover, focus-visible, active and disabled states |

Ask for a review and the output is a `rule | pass/fail/na | evidence file:line | fix` table.

## Layout

- `SKILL.md`: the workflow, and the pass line and trap of each rule.
- `references/rules/<id>.md`: per-rule decisions, exceptions, gotchas and a fix pattern.
- `references/frameworks.md`: MUI, Tailwind and plain-CSS constructs per rule.
- `references/sources.md`: where each figure comes from, with fetch dates and what is unverified.
- `evals/`: output evals, trigger queries and the fixtures they use.

## Related skills

- `mui`: MUI v7 API migration and `sx` usage. Use it for how to write MUI; use this skill for whether the screen is good.
- `design-system-starter`: creating a design system and token pipeline. This skill checks that a screen consumes the tokens that exist; it does not create the system.
