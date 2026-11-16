# Framework constructs per rule

Styling-stack facts the rules turn on and that no other file holds; standard constructs (`Button` variants, `:hover`, `aria-label`, utility scales) are left to the model. Stack traps that decide a verdict live in `SKILL.md` (MUI `sx` strings, Tailwind arbitrary values, `hover:` wrapping, `dark:` patches, `Skeleton` ARIA) or in the rule file named. Entries marked UNVERIFIED were not confirmed against the framework docs on 2026-10-30.

## MUI v7

- responsive: `Grid` takes `size={{ xs: 12, md: 6 }}`, not the old `xs`/`md` item props.
- a11y: native input attributes go through `TextField` `slotProps.htmlInput`.
- loading: only `Skeleton` was read (wrapping and sizing in `rules/loading.md`); `CircularProgress` and `LinearProgress` were not.
- states: `Snackbar` `role` handling UNVERIFIED.
- interaction: `.Mui-disabled` as the disabled class name in `sx` is UNVERIFIED; ripple and focus-visible in `rules/interaction.md`.
- consistency: `colorSchemes` and `palette` precedence in `rules/consistency.md`.

## Tailwind

- responsive: unprefixed classes are the base (phone) style; `sm:` 40rem, `md:` 48rem, `lg:` 64rem, `xl:` 80rem, `2xl:` 96rem are min-width; `max-*` variants target below a width.
- a11y, states: `aria-*:` variants exist for state styling; `sr-only` and the exact `aria-invalid:` variant are UNVERIFIED.
- loading: `animate-pulse`; pairing it with `motion-reduce:` is UNVERIFIED.

## Plain CSS

- responsive: `@container` needs `container-type: inline-size` on the ancestor; `cqi` units size against it.
- consistency: `color-scheme` on `:root` is UNVERIFIED (route in `rules/consistency.md`).
- states: `[aria-invalid="true"]` styles a field in error; `:invalid` is UNVERIFIED for error timing.
