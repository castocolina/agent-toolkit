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
- `references/component-examples.md` - semantic CSS roles, accessible field composition, browser theme-state check, additive variants, props conventions, compound Card, polymorphic component, native dialog Modal, skip link, theme toggle, responsive navigation
- `references/token-scales.md` - DTCG object-form typography, spacing, radius, shadow, duration, easing and layer scales, plus warning and info roles with measured contrast
- `references/component-specs.md` - per-component variants, states and accessibility, layout primitives, feedback patterns and target sizes (AA 24x24, AAA 44x44 CSS px)
- `references/process-and-tooling.md` - theming alternatives (Tailwind variants, a ThemeProvider)
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

## Credits

Adapted from [ArieGoldkin/ai-agent-hub](https://github.com/ArieGoldkin/ai-agent-hub/tree/main/skills/design-system-starter) by Arie Goldkin (MIT), through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit).

Scale values follow the Tailwind CSS default theme (MIT): https://tailwindcss.com/docs/theme.

Sources: @ArieGoldkin (original skill), [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Design Tokens Community Group format 2025.10](https://www.designtokens.org/tr/2025.10/format/), [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog), [WHATWG HTML Standard](https://html.spec.whatwg.org/multipage/form-elements.html#the-button-element), [React team](https://react.dev/blog/2024/12/05/react-19), [Tailwind Labs](https://tailwindcss.com/docs/box-shadow), [Style Dictionary maintainers](https://github.com/style-dictionary/style-dictionary), [Google Chrome DevTools](https://developer.chrome.com/docs/devtools/accessibility/reference).

## Version

1.0.0
