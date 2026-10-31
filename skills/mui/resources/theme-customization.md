# MUI theme setup: v7 code

Load this when writing `createTheme` or provider setup. The rules (the three augmentations, no numbered spacing variable, never spreading `useTheme()`, where `enableCssLayer` lives) are in `SKILL.md`; this file is the code that applies them.

## Palette color augmentation

```tsx
declare module '@mui/material/styles' {
  interface Palette { tertiary: Palette['primary']; }
  interface PaletteOptions { tertiary?: PaletteOptions['primary']; }
}
declare module '@mui/material/Button' {
  interface ButtonPropsColorOverrides { tertiary: true; }
}

const theme = createTheme({
  palette: { tertiary: { main: '#ff9800', contrastText: '#000' } },
});
```

Without `ButtonPropsColorOverrides`, `theme.palette.tertiary` typechecks and `<Button color="tertiary">` is still rejected. Repeat the override block for every component that takes the color (`Chip`, `IconButton`, ...).

## Light and dark on one theme

Prefer one theme with both schemes over a second nested theme:

```tsx
const theme = createTheme({
  cssVariables: { colorSchemeSelector: 'class' },
  colorSchemes: {
    light: { palette: { primary: { main: '#1976d2' } } },
    dark: { palette: { primary: { main: '#90caf9' } } },
  },
});

// Anywhere below <ThemeProvider theme={theme}>:
const { mode, setMode } = useColorScheme(); // from '@mui/material/styles'; mode is undefined on the first render
```

For the stock dark palette write `colorSchemes: { dark: true }` in place of the explicit `dark` object; keep the object when you override colors. CSS reads `var(--mui-palette-background-paper)` and `calc(2 * var(--mui-spacing))`.

## A nested region with its own theme

When a region really needs a separate theme, build it from the same source options, never from the resolved outer theme:

```tsx
const base: ThemeOptions = { shape: { borderRadius: 8 }, typography: { fontFamily: 'Inter' } };
const darkTheme = createTheme({ ...base, palette: { mode: 'dark' } }); // module scope, not per render

function NestedRegion({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ bgcolor: 'background.default', color: 'text.primary' }}>{children}</Box>
    </ThemeProvider>
  );
}
```

`palette: { mode: 'dark' }` in options, not in a resolved theme, is what derives the dark background and text. Check the computed `background-color` and `color` in the region; the mode flag alone proves nothing.

## CSS layers

Installed 7.3 types declare `enableCssLayer` on `StyledEngineProvider` and `modularCssLayers` on `ThemeOptions`. Check yours first: `grep -rn --include='*.d.ts' -e enableCssLayer -e modularCssLayers node_modules/@mui`. Default setup with those types:

```tsx
import { StyledEngineProvider } from '@mui/material/styles';
import GlobalStyles from '@mui/material/GlobalStyles';

<StyledEngineProvider enableCssLayer>
  <GlobalStyles styles="@layer theme, base, mui, components, utilities;" />
  <ThemeProvider theme={theme}>{app}</ThemeProvider>
</StyledEngineProvider>
```

In the Next.js App Router, pass it as `<AppRouterCacheProvider options={{ enableCssLayer: true }}>` instead. The `GlobalStyles` line fixes the layer order for Tailwind v4; drop it without Tailwind. Unlayered app CSS now beats MUI regardless of specificity, so rules that relied on load order change. Verify: the generated `<style>` tags contain `@layer mui`. If neither key is in the installed types, the version predates layers: stop and say so.
