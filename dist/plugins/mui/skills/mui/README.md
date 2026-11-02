# MUI v7 Patterns Skill

A comprehensive skill for working with Material-UI v7 components, styling, and best practices in React applications.

## Purpose

This skill provides guidance and patterns for building React applications with Material-UI v7 (released March 2025). It covers component usage, the sx prop styling system, theme integration, responsive design, and MUI-specific utilities.

MUI is one of the most popular React UI libraries, and v7 introduced several breaking changes from v6. This skill helps developers navigate these changes while following consistent, type-safe patterns.

## When to Use

Use this skill when you are:

- **Styling components with the sx prop** - Need guidance on MUI's styling approach
- **Working with MUI components** - Using Box, Grid, Paper, Typography, Button, Card, Dialog, and other MUI components
- **Customizing themes** - Setting up or modifying MUI themes
- **Building responsive layouts** - Using MUI's breakpoint system for mobile-first design
- **Using MUI utilities and hooks** - Working with useTheme, useMediaQuery, or custom MUI hooks
- **Migrating from MUI v6** - Understanding v7 breaking changes

**Trigger phrases:**
- "style with sx prop"
- "MUI component"
- "Material-UI"
- "theme customization"
- "MUI responsive design"
- "MUI Grid layout"

## How It Works

1. **Identify the MUI task** - Recognize when MUI patterns are relevant to the current work
2. **Apply appropriate patterns** - Choose `sx`, `styled`, or theme overrides by how widely the style is reused
3. **Leverage theme tokens** - Use MUI's built-in theme values instead of hardcoded styles
4. **Ensure type safety** - Apply proper TypeScript types for sx props
5. **Build responsively** - Use MUI's breakpoint system for adaptive layouts

## Key Features

### MUI v7 Breaking Changes Awareness

The skill includes guidance on v7-specific changes:
- Deep imports no longer work (use package exports)
- `onBackdropClick` removed from Modal (use `onClose` instead)
- Use `slots` and `slotProps` where the target component supports them; check its v7 API

### Styling Patterns

Choose `sx` for one-off styling, `styled` for reusable component-level styles, and theme overrides for system-wide defaults. Extract colocated styles when reuse or readability warrants it; there is no fixed line-count rule.

### Component Guidance

The skill provides migration and styling guidance for MUI v7. Check the target component's current prop types or documentation before relying on a specific API.

### Theme Integration

- Direct theme value access in sx prop
- useTheme hook for programmatic access
- Callback syntax for complex theme-dependent styles

### Responsive Design

- Mobile-first breakpoint system (xs, sm, md, lg, xl)
- Responsive prop values for any CSS property
- Conditional display based on screen size

## Usage Examples

### Basic Component with sx Prop

```typescript
import { Box, Typography, Button, Paper } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';

const styles: Record<string, SxProps<Theme>> = {
  container: {
    p: 2,
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
  },
  header: {
    mb: 3,
    fontSize: '1.5rem',
    fontWeight: 600,
  },
};

function MyComponent() {
  return (
    <Paper sx={styles.container}>
      <Typography sx={styles.header}>Title</Typography>
      <Button variant="contained">Action</Button>
    </Paper>
  );
}
```

### Responsive Layout

```typescript
<Box
  sx={{
    width: {
      xs: '100%',  // 0-600px
      sm: '80%',   // 600-900px
      md: '60%',   // 900-1200px
      lg: '40%',   // 1200px+
    },
    display: {
      xs: 'none',  // Hidden on mobile
      md: 'block', // Visible on desktop
    },
  }}
>
  Responsive content
</Box>
```

### Grid System

```typescript
import { Grid } from '@mui/material';

<Grid container spacing={3}>
  <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
    <Card>...</Card>
  </Grid>
  <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
    <Card>...</Card>
  </Grid>
</Grid>
```

### Theme-Aware Styling

```typescript
<Box
  sx={(theme) => ({
    color: theme.palette.primary.main,
    bgcolor: 'background.paper',
    p: 2,
    '&:hover': {
      color: theme.palette.primary.dark,
    },
  })}
>
  Theme-integrated content
</Box>
```

## Prerequisites

- React 18 or later
- Material-UI v7 packages installed:
  - `@mui/material`
  - `@mui/icons-material` (for icons)
- TypeScript (recommended for type safety)

## Output

This skill produces:
- Type-safe component code using MUI patterns
- Properly structured style definitions
- Responsive, theme-integrated layouts
- Accessible UI components following MUI conventions

## Best Practices

### 1. Always Type Your sx Props

```typescript
import type { SxProps, Theme } from '@mui/material';

const styles: Record<string, SxProps<Theme>> = {
  container: { p: 2 },
};
```

### 2. Use Theme Tokens Over Hardcoded Values

```typescript
// Good
<Box sx={{ color: 'primary.main', p: 2 }} />

// Avoid
<Box sx={{ color: '#1976d2', padding: '16px' }} />
```

### 3. Use MUI Spacing Scale

```typescript
// Good - Uses theme.spacing()
<Box sx={{ p: 2, mb: 3, mt: 1 }} />

// Avoid - Random pixel values
<Box sx={{ padding: '17px', marginBottom: '25px' }} />
```

### 4. Choose Style Organization by Need

Keep styles colocated when that suits the component. Extract them when reuse or readability warrants it.

### 5. Use Semantic Color Names

Access palette colors by their semantic names:
- `primary.main`, `primary.light`, `primary.dark`
- `secondary.main`, `error.main`, `warning.main`
- `text.primary`, `text.secondary`
- `background.paper`, `background.default`

## Additional Resources

The skill includes supplementary documentation:
- `resources/styling-guide.md` - Beating MUI state-class specificity and styling by color mode
- `resources/theme-customization.md` - Palette augmentation, colorSchemes, nested themes and CSS layers
- `resources/ui-ux-mapping.md` - MUI constructs for the ui-ux rules skill

## Related Documentation

- [MUI Official Documentation](https://mui.com/material-ui/)
- [MUI v7 Migration Guide](https://mui.com/material-ui/migration/upgrade-to-v7/)
- [MUI System (sx prop)](https://mui.com/system/getting-started/)
