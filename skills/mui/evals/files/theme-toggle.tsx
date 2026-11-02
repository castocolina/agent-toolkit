import { useMemo, useState } from 'react';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import { createTheme, ThemeProvider, useTheme } from '@mui/material/styles';

export function ThemeToggle() {
  const outerTheme = useTheme();
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  const innerTheme = useMemo(
    () =>
      createTheme({
        ...outerTheme,
        palette: { ...outerTheme.palette, mode: 'dark' },
      }),
    [outerTheme],
  );

  return (
    <ThemeProvider theme={innerTheme}>
      <Box sx={{ bgcolor: 'background.default', color: 'text.primary', p: 2 }}>
        <IconButton onClick={() => setMode((m) => (m === 'light' ? 'dark' : 'light'))}>
          {mode === 'light' ? <DarkModeIcon /> : <LightModeIcon />}
        </IconButton>
      </Box>
    </ThemeProvider>
  );
}
