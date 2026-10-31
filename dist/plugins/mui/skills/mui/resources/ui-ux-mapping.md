# MUI constructs for the UI/UX rules

The rules live in the `ui-ux-principles` skill; load it first. This file names only the MUI construct per rule where the choice is not obvious. Loading (Skeleton) and icon-button names are in `SKILL.md`.

| rule | MUI construct |
|------|---------------|
| responsive | `sx` breakpoint objects for a CSS-only change; `useMediaQuery(theme.breakpoints.up('md'))` only when the markup differs, and pass `{ noSsr: true }` or expect a first render at the default value. |
| hierarchy | The filled button is `variant="contained"`; a destructive action is `variant="outlined" color="error"`, not contained. |
| tokens | Add a missing role to `createTheme` (palette entry with the augmentation in `SKILL.md`, or a `shape`/`spacing` value), then read it as `'primary.main'` or a numeric spacing key in `sx`. |
| consistency | `colorSchemes` on the one theme and `useColorScheme().setMode` at the root; a shared look goes in `components.<Name>.defaultProps` or `styleOverrides`, not a one-off `styled` copy. |
| states | `Alert severity="error"` with a retry button in `action` for a failure. `Alert` defaults to `role="alert"`, which interrupts the screen reader: pass `role="status"` for a success confirmation. |
| interaction | MUI puts `.Mui-focusVisible` on keyboard focus; `disableRipple` also removes the visible focus ripple, so add a `&.Mui-focusVisible` outline whenever you disable it. |
