import { createTheme } from '@mui/material/styles';

// Divider-colored border for every outlined input. Hover and focus still show MUI's
// default colors, and the dark scheme branch below never switches.
export const theme = createTheme({
  cssVariables: { colorSchemeSelector: 'class' },
  colorSchemes: { light: true, dark: true },
  components: {
    MuiOutlinedInput: {
      styleOverrides: {
        notchedOutline: ({ theme }) => ({
          borderColor: theme.palette.divider,
          ...(theme.palette.mode === 'dark' && { borderColor: 'rgba(255, 255, 255, 0.4)' }),
        }),
      },
    },
  },
});
