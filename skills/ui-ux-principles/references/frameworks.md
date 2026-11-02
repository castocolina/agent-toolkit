# Framework constructs per rule

Rule ids mapped to constructs; no rule text. Entries marked UNVERIFIED were not confirmed against the framework docs on 2026-10-30.

| rule | MUI v7 | Tailwind | plain CSS |
|------|--------|----------|-----------|
| loading | `Skeleton` (`variant` text/circular/rectangular/rounded, `animation` pulse/wave/false; wrap a component to infer size), `CircularProgress`, `LinearProgress` (only Skeleton was read) | `animate-pulse`; `motion-safe:` / `motion-reduce:` variants exist (pairing UNVERIFIED) | `@keyframes` plus `prefers-reduced-motion`; `aspect-ratio`, `min-height` to reserve space |
| responsive | `Grid` with `size={{ xs: 12, md: 6 }}`, responsive `sx` values, `useMediaQuery` | unprefixed = base, `sm:` 40rem, `md:` 48rem, `lg:` 64rem, `xl:` 80rem, `2xl:` 96rem (min-width); `max-*` variants for below-width | `@media (min-width)`, `@container` with `container-type: inline-size`, `clamp()`, `cqi` units |
| hierarchy | `Button` `variant` contained/outlined/text, `Typography` `variant` scale, `Stack` spacing | `font-*`, `text-*`, `space-y-*`, `gap-*` utilities on a defined scale | type scale custom properties; spacing and heading margins |
| tokens | `createTheme` (`palette`, `spacing`, `shape`, `typography`), `sx` theme keys | theme variables / config; arbitrary values `[...]` are the escape hatch to avoid | `:root { --token: value }` custom properties; optional DTCG `.tokens.json` as source |
| consistency | one `ThemeProvider`; `components` overrides in the theme; `colorSchemes` for dark mode (`palette` wins if both set); `useColorScheme` | `dark:` maps to `prefers-color-scheme`; shared component classes via `@apply` or a component | variables switched in `@media (prefers-color-scheme: dark)` or on `[data-theme]`; `color-scheme` (UNVERIFIED) |
| a11y | `IconButton aria-label`, `TextField` `slotProps.htmlInput` for native attributes, visible `label` | `sr-only` for visually hidden text (UNVERIFIED), `aria-*:` variants for state styling | `aria-label`, `aria-labelledby`, `alt`, `min-width/min-height` for targets |
| states | `Alert`, `Snackbar` (`role` handling UNVERIFIED), `FormHelperText` with `error` | `aria-invalid:` variant (an `aria-*` family exists; this exact one UNVERIFIED), `disabled:` | `[aria-invalid="true"]`, `:invalid` (UNVERIFIED for UX timing); `role="alert"` / `role="status"` |
| interaction | `Button` has built-in states; custom `sx` needs `'&:focus-visible'`, `'&:hover'`, `'&.Mui-disabled'` (UNVERIFIED class name) | `hover:` (wrapped in `@media (hover: hover)`), `focus-visible:`, `active:`, `disabled:`, `enabled:` | `:hover`, `:focus-visible`, `:active`, `:disabled`, `@media (hover: hover)`, `scroll-margin` for sticky headers |
