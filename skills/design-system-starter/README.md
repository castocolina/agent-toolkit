# Design System Starter

A Claude Code skill for creating and evolving shared design-system contracts: semantic tokens, light/dark token themes, component APIs, contrast-checked token pairs, and adoption without breaking consumers. `SKILL.md` holds the workflow and rules; this file only describes the package.

## When to use

- Create a design system or a first token file, with or without an existing repository
- Convert raw values (`blue-500`, `16px`) into semantic tokens with one value set per theme
- Standardize UI patterns across apps or teams, starting from one pilot pattern
- Version, deprecate and migrate shared tokens and components

Reviewing or fixing a single screen against UI rules belongs to the `ui-ux-principles` skill.

## Bundled resources

- `templates/design-tokens-template.json` - token file in the DTCG 2025.10 format, validated against the official schema
- `templates/component-template.tsx` - React `Button` contract: semantic props, focusable loading/aria-disabled state, no root `className`
- `references/token-checks.md` - runnable alias resolver, contrast script (alpha, translucent backgrounds) and wide-gamut conversion
- `references/component-examples.md` - semantic CSS roles, accessible field composition, browser theme-state check, additive variants
- `checklists/design-system-checklist.md` - scope-dependent audit and release gate
- `evals/` - output evals, trigger queries and their input files

## Usage examples

```
Create a design system for my React app with dark mode support
Turn this token file into semantic tokens with light and dark values
Here's our legacy settings page; plan an incremental migration to shared tokens
```

## License

MIT

## Version

1.0.0
