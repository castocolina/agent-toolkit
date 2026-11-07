# MUI sx and styled recipes: v7 code

Load this when the user asks for an example of the `sx` array form, a reusable `styled()` component, or how to debug or merge `sx`. The sx-versus-styled choice and the sx multipliers are in `SKILL.md`; state-class specificity and color-mode styling are in `resources/styling-guide.md`; theme-level defaults are in `references/theme-recipes.md`. Checked against mui.com on 2026-11-07 (https://mui.com/system/getting-started/the-sx-prop/ and https://mui.com/material-ui/customization/how-to-customize/).

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

`theme.palette.*` is fixed at the default color scheme when `cssVariables` and `colorSchemes` are on; for styles that must follow the color mode use `theme.vars` and `theme.applyStyles` (`resources/styling-guide.md`).
