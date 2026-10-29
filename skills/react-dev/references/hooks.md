# Hook TypeScript Contracts

## Inference and state shape

- Let `useState` infer from a meaningful initializer. Explicitly type empty collections, nullable values, and finite status unions so the setter cannot widen the state accidentally.
- Reducer actions should be discriminated unions; keep state transitions exhaustive. A reducer returning `State | undefined` from a missing branch breaks the state contract.
- Context without a real default should be `Context<T | null>` with a consumer hook that throws outside its provider. A fabricated default hides missing providers.
- Tuple-returning custom hooks need an explicit tuple type or `as const`; otherwise TypeScript infers an array and loses positional types.

## Generic correlation

A generic hook that accepts a key and a value must preserve the relationship between them in its signature. Do not widen correlated keys, values, or callbacks into independent unions; inference can then accept a key paired with another key's value. Prefer a discriminated union or a generic parameter tied to the key, and keep callback variance visible in the API.

## React-version boundaries

- React 19 makes refs mutable and permits `ref` as a component prop; do not apply those assumptions to React 18 typings/runtime. React 18 components need `forwardRef` and may expose readonly nullable ref behavior based on their type declarations.
- `useImperativeHandle` should expose the smallest deliberate imperative surface, not a duplicate DOM API.
- `useCallback`/`useMemo` stabilize identity only while dependencies are stable; they do not repair stale closures or make a value semantically persistent. Prefer correct dependency contracts over suppressions.

## External state and SSR

Use `useSyncExternalStore` for mutable external stores. Its `subscribe` function must have stable identity, unsubscribe correctly, and notify after every relevant change. `getSnapshot` must return the same reference/value while the store is unchanged; allocating a new object each call can cause repeated renders. The server snapshot must agree with the initial hydration snapshot.

Browser globals are unavailable during server rendering, including lazy state initializers in Client Components. For storage-backed state, initialize to a hydration-stable value, then read after mount; guard storage access (it can throw when blocked) and parse/validate unknown JSON before treating it as `T`:

```tsx
function useStoredValue<T>(key: string, initial: T, isT: (value: unknown) => value is T) {
  const [value, setValue] = useState(initial);

  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(key);
      if (raw === null) return;
      const parsed: unknown = JSON.parse(raw);
      if (isT(parsed)) setValue(parsed);
    } catch {
      // Storage can be unavailable and stored data can be malformed.
    }
  }, [key]);

  return [value, setValue] as const;
}
```

Do not persist the initial value before the post-mount read completes; otherwise it can overwrite valid stored data. For external subscriptions, provide an SSR-safe snapshot rather than reading `window` from `getServerSnapshot`.

## Async data and stable resources

Effects that fetch must abort or ignore stale results at cleanup; cancellation is about preventing obsolete writes, not guaranteeing the server stopped processing. For React 19 `use(promise)`, pass a stable promise from a server component or cache keyed by resource identity. Creating a fresh uncached promise during client render can suspend indefinitely. `use` may be conditional/iterative; ordinary hooks may not.

## Router integration

When route state owns data or navigation, use the router's loader/action/search-parameter APIs rather than mirroring route values in component state. Preserve router-provided generic relationships at boundaries; casting route params or loader results merely hides invalid route assumptions.
