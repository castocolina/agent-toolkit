# Hook Typing

Only what differs by `@types/react` version or is easy to get subtly wrong. Effect design (whether an Effect should exist, dependencies, cleanup) belongs to the react-useeffect skill.

## Refs by `@types/react` major

| Call | `@types/react` 18 | `@types/react` 19 |
|---|---|---|
| `useRef<HTMLDivElement>(null)` | `RefObject<HTMLDivElement>`, `current` readonly | `RefObject<HTMLDivElement \| null>`, `current` mutable |
| `useRef<number>()` | allowed, `MutableRefObject<number \| undefined>` | type error: an argument is required |
| Timer ref | `useRef<ReturnType<typeof setTimeout>>()` | `useRef<ReturnType<typeof setTimeout> \| undefined>(undefined)` |

Source: React 19 upgrade guide, "TypeScript changes" (useRef requires an argument; all refs mutable), https://react.dev/blog/2024/04/25/react-19-upgrade-guide, checked 2026-11-08.

Code that must compile against both majors passes an explicit initial value everywhere and never assigns to a DOM ref's `current`.

## Reducers and context

- `@types/react` 19: do not pass type arguments to `useReducer`; annotate the reducer (`(s: State, a: Action): State`) and let the hook infer. An action union then rejects `dispatch({ type: 'typo' })` at the call site.
- Context with no meaningful default: `createContext<T | null>(null)` plus a `useX()` hook that throws outside the provider; a fake default object hides a missing provider.
- `useImperativeHandle` exposes the smallest deliberate surface (`{ focus(): void }`), not the DOM node again.

## External state and SSR

Use `useSyncExternalStore` for mutable external stores. Its `subscribe` function must have stable identity, unsubscribe correctly, and notify after every relevant change. `getSnapshot` must return the same reference/value while the store is unchanged; allocating a new object each call can cause repeated renders. The server snapshot must agree with the initial hydration snapshot.

Storage-backed state follows the SKILL.md rule (hydration-stable start, read after mount, validate, never write before the current key is read). This hook keeps the value tagged with the key it was read for, so a key change can never show or persist another key's value:

```tsx
function useStoredValue<T>(key: string, fallback: T, isT: (value: unknown) => value is T) {
  const [entry, setEntry] = useState<{ key: string; value: T } | null>(null);

  useEffect(() => {
    let value = fallback; // missing, blocked or invalid: use the fallback and write nothing
    try {
      const raw = window.localStorage.getItem(key);
      if (raw !== null) {
        const parsed: unknown = JSON.parse(raw);
        if (isT(parsed)) value = parsed;
      }
    } catch {
      // Storage can throw (blocked, private mode) and stored JSON can be malformed.
    }
    setEntry({ key, value });
    // eslint-disable-next-line react-hooks/exhaustive-deps -- read once per key
  }, [key]);

  const ready = entry?.key === key; // false on the server, on first client render, and right after a key change
  const setValue = (next: T) => {
    setEntry({ key, value: next });
    try {
      window.localStorage.setItem(key, JSON.stringify(next)); // writes happen only on an explicit set
    } catch {
      // Quota exceeded or blocked: keep the in-memory value.
    }
  };

  return [ready ? entry.value : fallback, setValue, ready] as const;
}
```

Switching `key` from `a` to `b`: the render after the change has `ready === false` and shows `fallback`, the effect reads `b`, and nothing is written to either key. For a store shared across tabs or components, use `useSyncExternalStore` with a `getServerSnapshot` that returns the fallback instead of reading `window`.
