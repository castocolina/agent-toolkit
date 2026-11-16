# Framework constructs per rule

Styling-stack facts the rules turn on and that no other file holds; standard constructs (`Button` variants, `:hover`, `aria-label`, utility scales) are left to the model. Stack traps that decide a verdict live in `SKILL.md` (MUI `sx` strings, Tailwind arbitrary values, `hover:` wrapping, `dark:` patches, `Skeleton` ARIA) or in the rule file named. Entries marked UNVERIFIED were not confirmed against the framework docs (entries re-checked on 2026-11-15 cite their page).

## MUI (current major: check the installed version)

The MUI claims below were checked on 2026-11-15 against v9.5.0 (npm `@mui/material` 9.5.0, release v9.5.0 of 2026-10-09: https://registry.npmjs.org/@mui/material/latest). Read the version from `package.json` before relying on a version-bound line.

- responsive: `Grid` takes `size={{ xs: 12, md: 6 }}`, not the old `xs`/`md` item props.
- a11y: native input attributes go through `TextField` `slotProps.htmlInput`.
- loading: only `Skeleton` was read (wrapping and sizing in `rules/loading.md`); `CircularProgress` and `LinearProgress` were not.
- states: `Snackbar` root is `role="presentation"`; its content (`SnackbarContent`) announces as `alert` by default (https://mui.com/material-ui/api/snackbar-content/, checked 2026-11-15). Pass `role="status"` for a confirmation.
- interaction: `.Mui-disabled` is the documented global class applied when `disabled={true}` (https://mui.com/material-ui/api/button-base/, checked 2026-11-15); ripple and focus-visible in `rules/interaction.md`. MUI v9 adds a theme key `theme.focusVisible` that `Button` spreads under `.Mui-focusVisible`: version-bound, so re-read the installed source before a verdict that depends on it.
- consistency: `colorSchemes` and `palette` precedence in `rules/consistency.md`.

## Tailwind

- responsive: unprefixed classes are the base (phone) style; `sm:` 40rem, `md:` 48rem, `lg:` 64rem, `xl:` 80rem, `2xl:` 96rem are min-width; `max-*` variants target below a width.
- a11y, states: `aria-*:` variants exist for state styling; `sr-only` is documented (https://tailwindcss.com/docs/display, checked 2026-11-15). `aria-invalid:` is not a built-in variant: use `aria-[invalid=true]:` or `@custom-variant aria-invalid (&[aria-invalid="true"]);` (https://tailwindcss.com/docs/hover-focus-and-other-states, checked 2026-11-15).
- loading: `animate-pulse`; `motion-safe:` and `motion-reduce:` apply to any animation utility (they compile to `@media (prefers-reduced-motion: ...)`; https://tailwindcss.com/docs/animation, checked 2026-11-15).

## Plain CSS

- responsive: `@container` needs `container-type: inline-size` on the ancestor; `cqi` units size against it. Container queries are Baseline Widely available since February 2023 (https://developer.mozilla.org/en-US/docs/Web/CSS/@container, checked 2026-11-15).
- consistency: `color-scheme: light dark` on `:root` opts the page in so the UA adapts canvas, scrollbars and form controls (Baseline Widely available since January 2022; https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme, checked 2026-11-15); route in `rules/consistency.md`.
- states: `[aria-invalid="true"]` styles a field in error; `:invalid` is UNVERIFIED for error timing.
