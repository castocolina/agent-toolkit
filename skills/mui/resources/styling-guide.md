# MUI styling: specificity and color mode

Load this for a `styled` component or a theme `styleOverrides` that must beat a state class, or that styles by color mode. The sx-versus-styled choice and the sx multipliers are in `SKILL.md`; theme setup is in `theme-customization.md`.

## Beat a state class at its own specificity

MUI's default state rules live on the component root and include the state class, so a slot override with one class loses to them.

```tsx
// Loses: `.MuiOutlinedInput-notchedOutline` is 0,1,0. MUI's default
// `.root:hover .notchedOutline` and `.root.Mui-focused .notchedOutline`
// are 0,3,0, so hover and focus keep MUI's colors.
MuiOutlinedInput: {
  styleOverrides: {
    notchedOutline: ({ theme }) => ({ borderColor: theme.palette.divider }),
  },
},

// Wins: the same 0,3,0 selectors on `root`. Theme overrides are emitted after
// the defaults, so the tie goes to them.
import { outlinedInputClasses } from '@mui/material/OutlinedInput';

MuiOutlinedInput: {
  styleOverrides: {
    root: ({ theme }) => ({
      [`& .${outlinedInputClasses.notchedOutline}`]: { borderColor: theme.palette.divider },
      [`&:hover .${outlinedInputClasses.notchedOutline}`]: { borderColor: theme.palette.text.primary },
      [`&.${outlinedInputClasses.focused} .${outlinedInputClasses.notchedOutline}`]: {
        borderColor: theme.palette.primary.main,
      },
    }),
  },
},
```

Copy the state selector from the component's source rather than guessing it, use the exported `*Classes` objects instead of string class names, and never target the generated `css-<hash>` classes: they change between builds. Check the result in devtools with the input hovered and focused.

## Style by color mode

With `cssVariables` and `colorSchemes`, `theme.palette.mode` inside a `styled` or `styleOverrides` callback is fixed at the default scheme, so a `mode === 'dark'` branch never switches. Use `theme.applyStyles`:

```tsx
const Panel = styled('div')(({ theme }) => ({
  backgroundColor: theme.vars.palette.background.paper,
  ...theme.applyStyles('dark', { borderColor: theme.vars.palette.divider }),
}));
```

- `theme.vars.palette.*` resolves to `var(--mui-palette-*)`. The `alpha()` helper cannot parse a `var()`: use `theme.alpha(theme.vars.palette.primary.main, 0.12)` where the installed theme type declares `alpha`, else `` `rgba(${theme.vars.palette.primary.mainChannel} / 0.12)` ``.
- `theme.vars` exists only when `cssVariables` is on; without it, read `theme.palette` and keep `applyStyles`.
