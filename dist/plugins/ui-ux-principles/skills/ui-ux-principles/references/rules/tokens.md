# tokens

## Decisions

- Where a value goes, in order: the role already in the theme; a new role added to that theme (CSS custom properties, MUI `createTheme`, Tailwind theme); a flag to the user when the repo has no theme. Never the component.
- A role name (`color-danger`) survives a rebrand and a dark theme; a value name (`red-500`) in a component is a literal with extra steps.
- A z-index, duration or breakpoint used twice becomes a role in the same theme; a one-off is flagged, not inlined.
- Check contrast once per role pair per theme (`color-text` on `color-surface`), not once per component.

## Gotchas

- MUI `sx` spacing keys multiply `theme.spacing` when given a number (`p: 2`), so that is a token read; a string (`p: '9px'`) bypasses the scale and is a literal.
- A Tailwind arbitrary value (`bg-[#3b82f6]`, `p-[9px]`) is a literal in the component even though it is a utility class.
- The DTCG format is a draft community group report, not a W3C standard; follow it only when the repo already keeps `.tokens.json` files.

## Fix pattern

```css
:root { --color-primary: #1d4ed8; --space-2: 0.5rem; }
.btn { background: var(--color-primary); padding: var(--space-2); }
```
