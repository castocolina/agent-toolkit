# consistency

## Decisions

- Compare variants on the same axes: height, padding, radius, type size, border and state styles. A screen that needs something different extends the shared component with a prop.
- One word per action across the app ("Delete", not "Remove" here and "Trash" there), and platform conventions where users expect them (NN/g heuristic 4, Consistency and standards).
- Dark mode routes, one per stack:
  - Plain CSS: switch the custom properties under `@media (prefers-color-scheme: dark)` or on `[data-theme]` at the root.
  - Tailwind: `dark:` maps to `prefers-color-scheme`; put it on the theme variables, not on each component.
  - MUI: `createTheme({ colorSchemes: { dark: true } })` is the recommended route.
- `color-scheme: light dark` on `:root` so native controls follow the theme (MDN: declare `color-scheme` on `:root` to opt the page in; your own elements still need `prefers-color-scheme` or `light-dark()`; Baseline Widely available since January 2022; https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme, checked 2026-11-15).

## Gotchas

- MUI: if both `palette` and `colorSchemes` are set, `palette` wins, so the dark scheme you added is ignored. `useColorScheme` returns an undefined mode on the first render, so a toggle that reads it then shows the wrong state. SSR needs CSS variables with `InitColorSchemeScript`.
