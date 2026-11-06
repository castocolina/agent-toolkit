// app/components/ThemeToggle.tsx (Next.js 15 App Router, React 19)
'use client';

import { useEffect, useState } from 'react';

type Theme = 'light' | 'dark';

export function ThemeToggle({ userId }: { userId: string }) {
  const storageKey = `theme:${userId}`;
  const [theme, setTheme] = useState<Theme>(() => (localStorage.getItem(storageKey) as Theme) ?? 'light');

  useEffect(() => {
    localStorage.setItem(storageKey, theme);
  }, [storageKey, theme]);

  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>{theme}</button>;
}

// Reports:
// 1. Server logs: ReferenceError: localStorage is not defined
// 2. "Hydration failed because the server rendered text didn't match the client"
// 3. After switching accounts in the header (userId changes without a remount), the new user gets the previous user's theme saved under their key.
