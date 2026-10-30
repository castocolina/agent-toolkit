# MUI Component Library

## v7 decisions and migration traps

- **Grid:** v7's `Grid` uses `size`, not legacy `item`, `xs`, or `md` props. Example: `<Grid size={{ xs: 12, md: 6 }}>…</Grid>`. Keep `GridLegacy` only in intentionally unmigrated code and label that choice explicitly.
- **TextField accessibility:** Prefer a visible `label`. `slotProps.input` configures the MUI Input component; `slotProps.htmlInput` configures the native input. Verify the rendered textbox's accessible name, not just TypeScript acceptance.
- **Slots:** Slot names and responsibilities vary by component. Check that component's v7 types/docs before migrating deprecated replacement props; do not infer one component's slot contract from another.
- **Selectors and overrides:** Prefer public component classes and theme overrides for shared behavior. Avoid generated hash selectors, which can change between builds. Check selector specificity against default state classes such as `Mui-focused` and `Mui-error`.
- **Responsive values:** Use responsive `sx` values for one-off layout changes; use Grid/Stack when the relationship between children is structural. Preserve existing project conventions and responsive breakpoints.
- **Component choice:** Use the smallest component that satisfies interaction and accessibility requirements. For example, use `IconButton` for an icon-only action only when it has an accessible name; use `Tooltip` as supplementary help, not as the sole accessible name.

## Example: v7 responsive Grid

```tsx
import Grid from '@mui/material/Grid';

<Grid container spacing={2}>
  <Grid size={{ xs: 12, md: 6 }}>First panel</Grid>
  <Grid size={{ xs: 12, md: 6 }}>Second panel</Grid>
</Grid>
```
