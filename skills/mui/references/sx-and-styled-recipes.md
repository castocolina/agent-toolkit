# MUI sx and styled recipes: v7 code

Load this when the user asks for an example of conditional or dynamic `sx`, global styles, a reusable `styled()` component, a card hover effect, a gradient, a sticky header, or how to debug or merge `sx`. The sx-versus-styled choice and the sx multipliers are in `SKILL.md`; state-class specificity and color-mode styling are in `styling-guide.md`; theme-level defaults are in `theme-recipes.md`. Checked against mui.com on 2026-11-07 (https://mui.com/system/getting-started/the-sx-prop/ and https://mui.com/material-ui/customization/how-to-customize/).

## Dynamic styles from props

Conditional values map straight into `sx`; palette strings and the spacing and border shorthands resolve through the theme:

```tsx
interface StatusCardProps {
  isActive: boolean;
  priority: 'low' | 'medium' | 'high';
}

function StatusCard({ isActive, priority }: StatusCardProps) {
  return (
    <Paper
      sx={{
        borderLeft: 4,
        borderColor: isActive ? 'success.main' : 'grey.300',
        bgcolor: priority === 'high' ? 'error.light' : 'background.paper',
        opacity: isActive ? 1 : 0.7,
      }}
    />
  );
}
```

For several conditional blocks, prefer the array form below over a chain of ternaries.

## The sx array form, merging and debugging

An `sx` array applies its entries in order, and a falsy entry (`false`, `undefined`) is skipped, so later entries override earlier ones. Each entry is an object or a callback:

```tsx
<Box
  sx={[
    { p: 2, '&:hover': { color: 'primary.main' } },
    isActive && { bgcolor: 'primary.main' },
    isDisabled && { opacity: 0.5 },
  ]}
/>
```

A custom component that accepts `sx` and forwards it to a MUI component must keep a caller's array working. The sx docs flatten it:

```tsx
function Tag({ sx, ...other }: BoxProps) {
  return <Box sx={[{ px: 1, textDecoration: 'underline' }, ...[sx].flat()]} {...other} />;
}
```

To see which theme values a callback receives, log inside it and return the style object:

```tsx
<Box
  sx={(theme) => {
    console.log('theme', theme);
    return { p: 2 };
  }}
/>
```

Remove the log before committing. The sx page marks a callback used as a single property value (`color: (theme) => ...`) as deprecated; pass the callback as the whole `sx` value, as in the examples on this page. To find which rule wins, inspect the element in devtools: `sx` styles carry a generated `css-<hash>` class, and the `Mui*` classes show the component's own rules.

## Global styles with GlobalStyles

```tsx
import GlobalStyles from '@mui/material/GlobalStyles';

const globalStyles = {
  body: { margin: 0 },
  '.custom-scrollbar::-webkit-scrollbar': { width: 8 },
};

<GlobalStyles styles={globalStyles} />;
```

`styles` takes an object, a string or a function of the theme. Mount it once near the root, inside `ThemeProvider`, and keep a static object at module scope so it is not rebuilt on every render. `CssBaseline` already sets `box-sizing: border-box` on every element and the body background (https://mui.com/material-ui/react-css-baseline/), so do not repeat that reset here. The import above also works as `import { GlobalStyles } from '@mui/material'`; the layer-order use of `GlobalStyles` is in `theme-customization.md`.

## Reusable styled components

```tsx
import { styled } from '@mui/material/styles';

const StyledCard = styled(Card)(({ theme }) => ({
  padding: theme.spacing(2),
  borderRadius: theme.shape.borderRadius * 2,
  backgroundColor: theme.palette.background.paper,
  transition: theme.transitions.create(['transform', 'box-shadow']),
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[8],
  },
}));
```

With a custom prop, type it by extending the base props and filter it out so it does not reach the DOM or the wrapped component. Do not name it `variant`: `Button` already has a `variant` prop (`text`, `outlined`, `contained`) with its own type, so a second `variant` collides with it and changes how `Button` renders. Use a name the component does not own, here `tone`:

```tsx
import Button, { type ButtonProps } from '@mui/material/Button';
import { styled } from '@mui/material/styles';

interface ToneButtonProps extends ButtonProps {
  tone?: 'primary' | 'secondary';
}

const ToneButton = styled(Button, {
  shouldForwardProp: (prop) => prop !== 'tone',
})<ToneButtonProps>(({ theme, tone = 'primary' }) => ({
  backgroundColor: theme.palette[tone].main,
  color: theme.palette[tone].contrastText,
  '&:hover': { backgroundColor: theme.palette[tone].dark },
}));
```

`theme.palette.*` is fixed at the default color scheme when `cssVariables` and `colorSchemes` are on; for styles that must follow the color mode use `theme.vars` and `theme.applyStyles` (`styling-guide.md`).

## Card with a hover effect

```tsx
<Card
  sx={(theme) => ({
    p: 3,
    transition: theme.transitions.create(['transform', 'box-shadow']),
    '&:hover': { transform: 'scale(1.02)', boxShadow: 4 },
    '@media (prefers-reduced-motion: reduce)': { transition: 'none', '&:hover': { transform: 'none' } },
  })}
/>
```

List the properties that change instead of `all`, and `boxShadow: 4` reads `theme.shadows[4]`. The motion rule keeps the effect off for users who ask for less motion.

## Gradient background

```tsx
<Box
  sx={(theme) => ({
    background: `linear-gradient(45deg, ${theme.palette.primary.main} 30%, ${theme.palette.secondary.main} 90%)`,
    color: theme.palette.primary.contrastText,
  })}
/>
```

Text over a gradient has to pass contrast at both ends of it; check the pair, not one stop.

## Sticky header

```tsx
<AppBar
  position="sticky"
  sx={(theme) => ({ top: 0, zIndex: theme.zIndex.drawer + 1 })}
/>
```

`position="sticky"` keeps the bar in the page flow, so content is not hidden behind it; with `position="fixed"` the bar leaves the flow and you must offset the content with a second `<Toolbar />` (https://mui.com/material-ui/react-app-bar/). The default stack order is app bar 1100, drawer 1200, modal 1300, snackbar 1400, tooltip 1500 (https://mui.com/material-ui/customization/z-index/); `drawer + 1` puts the bar above a permanent drawer. Read `theme.zIndex` rather than hardcoding the numbers; the docs discourage changing individual values.
