---
name: mui
description: "Use when building or migrating React UI with Material UI v7 (@mui/material and @mui/icons-material): sx styling, responsive Grid/Stack layouts, palette/theme overrides, forms, and dialogs. Trigger for adapting v6-era props/imports or an existing MUI screen. Not for Chakra UI, Vuetify, MUI X, raw CSS/Tailwind-only styling, or general React setup."
---

# MUI v7: migration and troubleshooting

Inspect installed `@mui/material` version and existing theme before changing code. Keep the repository's styling conventions; choose `sx` for one-off instance styling, `styled` for reusable component-level styles, and theme overrides for system-wide defaults. Extract colocated styles when reuse or readability warrants it, not at a fixed line count.

## v7 migration checks

- Use package exports, not private deep imports. Replace removed `onBackdropClick` with `onClose` and inspect the component's current callback reason semantics.
- Current Grid API: `import Grid from '@mui/material/Grid'` and `<Grid size={{ xs: 12, md: 6 }}>…</Grid>`; do not pass legacy `item`, `xs`, or `md` props. For other components, use responsive `sx` values where appropriate (for example `sx={{ width: { xs: '100%', md: 320 } }}`). For an intentionally unmigrated app, import and label `GridLegacy` explicitly.
- MUI supports `slots`/`slotProps` on components that expose them; use these APIs instead of deprecated component-specific replacement props when supported. Do not assume all components share identical slots: inspect the target component's v7 prop type/docs before choosing. For TextField, `slotProps.input` targets the MUI Input component, while `slotProps.htmlInput` targets the native `<input>`: prefer a visible `label`, or use `<TextField slotProps={{ htmlInput: { 'aria-label': 'Search' } }} />` for a native attribute. Verify the rendered textbox's accessible name in the accessibility tree or a role-based test.
- `sx` transforms values: numeric `borderRadius: 1` means one theme-radius unit. To use already-resolved `theme.shape.borderRadius`, pass an explicit CSS string (for example, `${theme.shape.borderRadius}px`) rather than feeding the number back through the multiplier.
- Palette augmentation does not automatically add a component's `color` prop. Augment `Palette`, `PaletteOptions`, and each consuming component's `*PropsColorOverrides` as needed; typecheck the actual consumer.
- CSS variable mode does not imply numbered variables such as `--mui-spacing-2`; use defined variables and verify the generated CSS contract.

## Verify changes

1. Check installed package types/docs and local theme overrides before assuming a prop exists.
2. Make the smallest relevant migration; preserve behavior and controlled state.
3. Run TypeScript/build checks. Exercise breakpoints, focus/keyboard behavior, and dialog close paths where affected.
4. For dialogs, replace `onBackdropClick` with `onClose(event, reason)` and check `reason === 'backdropClick'`; customize inner parts through `slots` and `slotProps` instead of legacy `components`/`componentsProps` or `*Props` overrides.

## Load the relevant reference only

- `resources/styling-guide.md` for selector nesting, `styled`, prop forwarding, or CSS variable transformations.
- `resources/component-library.md` for the specific component/API and v7 Grid patterns.
- `resources/theme-customization.md` for provider setup, palette augmentation, CSS variables, or global overrides.
