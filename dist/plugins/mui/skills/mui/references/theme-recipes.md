# MUI theme recipes: v7 code

Load this when the user asks for an example of component `styleOverrides` or `defaultProps`, custom breakpoints or custom shadows. Palette augmentation, `colorSchemes`, CSS layers and nested themes are in `resources/theme-customization.md`; beating a state class is in `resources/styling-guide.md`. Checked against mui.com on 2026-11-07 (pages under https://mui.com/material-ui/customization/); each recipe names its source.

## Component defaults and style overrides

```tsx
const theme = createTheme({
  components: {
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          // Variant plus color rules go in `variants` under `root` (see below).
          variants: [
            {
              props: { variant: 'contained', color: 'primary' },
              style: { boxShadow: 'none', '&:hover': { boxShadow: 'none' } },
            },
          ],
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: { borderRadius: 12, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' },
      },
    },
    MuiTextField: {
      defaultProps: { variant: 'outlined' },
    },
    MuiOutlinedInput: {
      styleOverrides: { root: { borderRadius: 8 } },
    },
    MuiChip: {
      styleOverrides: { root: { borderRadius: 6, fontWeight: 500 } },
    },
  },
});
```

- `styleOverrides` needs a slot name as the key (`root` is the outermost element); `defaultProps` sets a prop on every instance, for example `disableRipple` on `MuiButtonBase` to remove ripples everywhere.
- A `TextField` is a wrapper: the border radius belongs to the `OutlinedInput` it renders, hence `MuiOutlinedInput` above. For hover and focus colors of that input, see `resources/styling-guide.md` (state-class specificity).
- `variants` entries (`props` plus `style`) target one prop combination inside a slot and replace the old per-combination class keys. The `styleOverrides` keys named after a variant and color (`containedPrimary` and similar on `Button`, with matching keys on `Chip` and `Alert`) work on v7 but are removed in v9, where the same override is a `variants` entry under `root`. Read the upgrade guide for the installed major (https://mui.com/material-ui/migration/upgrade-to-v9/, sections "Button CSS classes", "Chip CSS classes", "Alert CSS classes") before writing a class key.
- Where `variants` goes: the docs document one form, `variants` inside a slot of `styleOverrides` (`components.MuiButton.styleOverrides.root.variants`), not as a sibling of `styleOverrides` and `defaultProps`; the example above uses that form (https://mui.com/material-ui/customization/theme-components/, "Variants" under "Theme style overrides", and the v9 guide's "Button CSS classes" section, both checked 2026-11-07).
- Put overrides that must win last when you write them as an array, and note that the `sx` prop on an instance still beats the theme (higher specificity). Sources: https://mui.com/material-ui/customization/theme-components/.

## Breakpoints

Defaults: `xs` 0, `sm` 600, `md` 900, `lg` 1200, `xl` 1536 px. Overriding `values` replaces the whole set, so list every key you keep:

```tsx
const theme = createTheme({
  breakpoints: {
    values: { xs: 0, sm: 600, md: 960, lg: 1280, xl: 1920 },
  },
});

<Box sx={{ width: { xs: '100%', sm: '80%', md: '60%', lg: '50%' } }} />
```

Each key is a minimum width, so `md: '60%'` applies from 960 px up. Custom names (`mobile`, `tablet`, ...) need a `BreakpointOverrides` module augmentation (`mobile: true`, and `xs: false` to remove a default). Helpers for use in `styled` or an `sx` callback: `theme.breakpoints.up('md')` (md and wider), `down('md')` (below md) and `between('sm', 'md')`. Source: https://mui.com/material-ui/customization/breakpoints/.

## Shadows

`theme.shadows` is a tuple of 25 entries: `'none'` at index 0 and 24 strings. A shorter literal fails the `Shadows` type, so start from the default and replace the entries you want:

```tsx
const base = createTheme();
const shadows = [...base.shadows] as typeof base.shadows;
shadows[1] = '0 2px 4px rgba(0,0,0,0.10)';
shadows[2] = '0 4px 8px rgba(0,0,0,0.12)';
shadows[3] = '0 8px 16px rgba(0,0,0,0.14)';

const theme = createTheme({ shadows });

<Paper elevation={2} /> // uses shadows[2]
```

Sources: `Shadows` in `@mui/material/styles/shadows.d.ts` (7.3.11, unpkg.com) and the default theme viewer, https://mui.com/material-ui/customization/default-theme/ (`shadows: Array(25)`), both checked 2026-11-07. `boxShadow: 4` in `sx` reads `shadows[4]`.
