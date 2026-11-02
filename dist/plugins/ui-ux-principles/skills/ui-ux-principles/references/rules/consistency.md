# consistency

## Decisions

- Compare variants on the same axes: height, padding, radius, type size, border and state styles. A screen that needs something different extends the shared component with a prop.
- One word per action across the app ("Delete", not "Remove" here and "Trash" there), and platform conventions where users expect them (NN/g heuristic 4, Consistency and standards).
- Dark mode routes, one per stack:
  - Plain CSS: switch the custom properties under `@media (prefers-color-scheme: dark)` or on `[data-theme]` at the root.
  - Tailwind: `dark:` maps to `prefers-color-scheme`; put it on the theme variables, not on each component.
  - MUI: `createTheme({ colorSchemes: { dark: true } })` is the recommended route.
- `color-scheme: light dark` on `:root` so native controls follow the theme (UNVERIFIED: general CSS practice, not on the pages read).

## Gotchas

- A `<style>` element rendered by a component is not scoped: `input, button { ... }` in one form restyles every input and button in the document.
- MUI: if both `palette` and `colorSchemes` are set, `palette` wins, so the dark scheme you added is ignored. `useColorScheme` returns an undefined mode on the first render, so a toggle that reads it then shows the wrong state. SSR needs CSS variables with `InitColorSchemeScript`.
- A dark theme made by inverting the light values often drops input borders and focus rings under 3:1 (the a11y row).

## Fix pattern

```css
:root { --color-primary: #1d4ed8; --color-on-primary: #fff; }
@media (prefers-color-scheme: dark) { :root { --color-primary: #93b4ff; --color-on-primary: #0b1b4d; } }
.btn { background: var(--color-primary); color: var(--color-on-primary); }
```
