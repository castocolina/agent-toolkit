---
name: mui
description: "Use when writing, fixing or migrating React code on Material UI v7 (@mui/material, @mui/icons-material, @mui/material/styles): sx styling and its spacing and borderRadius multipliers, Grid size layouts, slots/slotProps, createTheme palettes and color augmentation, CSS variables, colorSchemes dark mode, CSS layers, Dialog onClose, Skeleton loading and IconButton names. Trigger when upgrading v5 or v6 code (onBackdropClick, Grid item/xs/md, components/componentsProps, deep imports) or editing an existing MUI screen, even when the user does not say v7. Not for Joy UI, MUI X data grids or pickers, Chakra UI, Vuetify, Radix, a native <dialog>, Tailwind-only or plain CSS styling, or general React setup."
---

# MUI v7

Only the v7 facts a model gets wrong are here. Keep the repository's own styling conventions.

## Decision order

1. **Confirm the installed API.** Read the version in `package.json` and the component's `node_modules/@mui/material/<Component>/<Component>.d.ts` before relying on a prop. No `node_modules`: use the v7 upgrade guide and say which source you used.
2. **Pick the layer.** `sx` for one instance, `styled` for a reused component, theme `components` overrides for an app-wide default. Extract styles when reuse or readability asks for it, not at a line count.
3. **Apply the matching trap** from v7 facts and Gotchas.
4. **Verify.** Run the repo's typecheck script; if it has none, run `npx tsc --noEmit`. Then exercise what the change touches: each breakpoint, keyboard focus, every dialog close path.

## Worked branch: a v6 dialog

A private deep import, `onBackdropClick` and `components` become a public import, `onClose(event, reason)` and `slots`:

```tsx
// v6
import Dialog from '@mui/material/Dialog/Dialog';
<Dialog open={open} onBackdropClick={onCancel} components={{ Backdrop: MyBackdrop }}>

// v7
import Dialog from '@mui/material/Dialog';
<Dialog
  open={open}
  onClose={(event, reason) => {
    if (reason === 'backdropClick' && deleting) return; // reason is 'backdropClick' or 'escapeKeyDown'
    onCancel();
  }}
  slots={{ backdrop: MyBackdrop }}
>
  <DialogTitle>Delete {name}?</DialogTitle>
```

Keep `open` controlled by the parent. `DialogTitle` gives the dialog its accessible name; keep it. Legacy Grid inside becomes `<Grid size={{ xs: 12, md: 6 }}>`.

## v7 facts

- **Imports.** v7's package `exports` resolve one level only: `@mui/material/Dialog` works, `@mui/material/Dialog/Dialog` fails to resolve.
- **Grid.** v7 `Grid` is the former Grid2: `<Grid size={{ xs: 12, md: 6 }}>`, `offset` for gaps, no `item`. The old API is `GridLegacy`; import it only for code you deliberately leave unmigrated, and say so. `Hidden` is removed: use `sx={{ display: { xs: 'none', md: 'block' } }}` or `useMediaQuery`.
- **Slots.** `components` becomes `slots` and `componentsProps` becomes `slotProps`, with lowercase keys (`Backdrop` becomes `backdrop`). TextField: `inputProps` becomes `slotProps.htmlInput` (the native `<input>`, for `aria-label` and other attributes), `InputProps` becomes `slotProps.input` (the MUI Input component), `InputLabelProps` becomes `slotProps.inputLabel`. Dialog: `PaperProps` becomes `slotProps.paper`, `TransitionComponent` becomes `slots.transition`. Any other component: take the slot names from its `.d.ts`.
- **sx multipliers.** Spacing keys multiply by `theme.spacing`; a numeric `borderRadius` multiplies by `theme.shape.borderRadius`, so `borderRadius: 1` is one theme unit. Pass a resolved radius as a string: `` `${theme.shape.borderRadius}px` ``.
- **Palette color.** A new palette color needs three augmentations: `Palette`, `PaletteOptions`, and each consuming component's `*PropsColorOverrides` (`ButtonPropsColorOverrides` for `<Button color="tertiary">`), plus the entry in `createTheme({ palette })`. Then typecheck the consumer.
- **CSS variables.** `cssVariables: true` emits `--mui-palette-*`, `--mui-spacing` and the like; there is no numbered `--mui-spacing-2`. Check the generated stylesheet before using a variable name.
- **Loading.** While the title and body are not rendered yet, show `Skeleton` in their shape (`variant="text"` for a title, `variant="rectangular"` or `"rounded"` for a body), not a lone `CircularProgress`.
- **Icon-only buttons.** An `IconButton` has no accessible name of its own: set `aria-label` to the action (`Switch to dark mode`), not to the icon.

## Gotchas

- Legacy Grid props are silently ignored: `item`, `xs` and `md` raise no runtime error and the item renders full width.
- The wrong slot typechecks: an attribute in `slotProps.input` lands on the wrapper div, not on the `<input>`, so the textbox stays unnamed. Check the name with a role-based query.
- When the installed `.d.ts` and the upgrade guide disagree, the `.d.ts` wins for the version in `package.json`; say which version you read.
- Never spread a resolved `useTheme()` into `createTheme`: `borderRadius` is multiplied again and flipping `palette.mode` does not derive the dark palette. Build both themes from shared source `ThemeOptions`.
- `enableCssLayer` is not a `createTheme` key: in 7.3 it is a `StyledEngineProvider` prop (`AppRouterCacheProvider options` in Next.js). Grep the installed `.d.ts` for it, then confirm the generated CSS contains `@layer mui`.

## Load only what the task needs

This file covers every prop or import migration; load nothing for one.

- `resources/theme-customization.md`: when writing `createTheme` or provider setup: the full augmentation code, `cssVariables` with `colorSchemes`, the CSS layer setup, a nested theme. Not for an `sx` edit.
- `resources/styling-guide.md`: when a `styled` component or a theme `styleOverrides` must beat a state class (`Mui-focused`, `Mui-error`) or style by color mode (`theme.applyStyles`, `theme.vars`). Not for theme setup; theme-customization.md owns that.
- For a new or redesigned screen's loading, responsive, hierarchy, tokens, consistency, a11y, states or interaction work: load the `ui-ux-principles` skill first, then `resources/ui-ux-mapping.md` for the MUI construct per rule. Load neither for a migration or a single-prop fix.
