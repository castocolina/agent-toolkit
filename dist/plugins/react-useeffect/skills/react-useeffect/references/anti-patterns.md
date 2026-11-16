# Auditing existing Effects

Each smell links to the react.dev section with the full before/after. Section names are from [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) (YMNNAE).

## Smell catalog

| Smell in the code | Fix | react.dev |
|---|---|---|
| `useEffect(() => setX(f(a, b)), [a, b])` | `const x = f(a, b)` in render; `useMemo` if measured slow | YMNNAE, Updating state based on props or state; Caching expensive calculations |
| Effect clears all form state when `userId` changes | `key={userId}` on the component that owns the state | YMNNAE, Resetting all state when a prop changes |
| Effect resets one field (`selection`) when `items` changes | Store `selectedId`, derive `items.find(...) ?? null`; else the previous-value check in [alternatives](alternatives.md#partial-identity-reset) | YMNNAE, Adjusting some state when a prop changes |
| Effect watches `product.isInCart` to show a toast | Show it in the click handler (the Effect also fires on reload when the item is already in the cart) | YMNNAE, Sharing logic between event handlers |
| Effect sends a POST because a `submitted` flag flipped | Send it in the submit handler; keep analytics-on-display in an Effect | YMNNAE, Sending a POST request |
| Effects that set state that triggers the next Effect | Compute all next state in the one event handler; derive what can be derived (`isGameOver = round > 5`) | YMNNAE, Chains of computations |
| Effect calls `onChange(isOn)` after local state changes | Call `onChange` in the same handler that sets state, or make the component controlled | YMNNAE, Notifying parent components about state changes |
| Child fetches, then an Effect passes data up to the parent | Parent fetches and passes data down | YMNNAE, Passing data to the parent |
| Effect copies `navigator.onLine` or a store value into state | `useSyncExternalStore` ([alternatives](alternatives.md#external-store-snapshots)) | YMNNAE, Subscribing to an external store |
| Fetch Effect with no cleanup | The complete hook below | YMNNAE, Fetching data |
| `[]` Effect in `App` that must run once per app load | The initialization cache below | YMNNAE, Initializing the application |

Keep an Effect when the code runs because the component is displayed (connections, widgets, analytics on view). A doubled analytics call in development is expected; react.dev recommends leaving it.

## Fetch in an Effect: complete version

Use this only when the project has no data layer. The result is stored with the request generation it belongs to (an id that is bumped whenever the URL or `reloadCount` changes, including A to B to A), so loading is derived during render instead of set inside the Effect: an earlier result for the same URL is never shown as current while a new request for it is pending, and there is no unguarded `finally`.

```tsx
import { useEffect, useState } from 'react';

class HttpError extends Error {
  readonly status: number;
  constructor(status: number, url: string) {
    super(`HTTP ${status} for ${url}`);
    this.status = status;
  }
}

async function fetchJson<T>(url: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(url, { signal }); // rejects only on network failure or abort
  if (!response.ok) throw new HttpError(response.status, url);
  return (await response.json()) as T;
}

type Result<T> =
  | { status: 'success'; id: number; data: T }
  | { status: 'error'; id: number; error: unknown };

// reloadCount: increment from a retry button to re-request the same url
export function useJson<T>(url: string, reloadCount = 0): { status: 'loading' } | Result<T> {
  const key = `${reloadCount}:${url}`;
  const [result, setResult] = useState<Result<T> | null>(null);
  // Request generation: bumped during render whenever the key changes, so A -> B -> A gives
  // the second A a new id and the stored result of the first A can no longer match it.
  const [request, setRequest] = useState({ key, id: 0 });
  let id = request.id;
  if (request.key !== key) {
    id = request.id + 1;
    setRequest({ key, id }); // adjusting state during render; React re-renders at once
  }

  useEffect(() => {
    let ignore = false;
    const controller = new AbortController();
    fetchJson<T>(url, controller.signal).then(
      (data) => { if (!ignore) setResult({ status: 'success', id, data }); },
      (error) => { if (!ignore) setResult({ status: 'error', id, error }); },
    );
    return () => {
      ignore = true;
      controller.abort();
    };
  }, [url, id]);

  if (result === null || result.id !== id) return { status: 'loading' };
  return result;
}
```

How it holds up:

- Out-of-order responses: an older request's cleanup has set its own `ignore`, so neither its data nor its error is written.
- Strict Mode: the first setup is cleaned up at once, its abort rejects with `AbortError`, and the `ignore` check drops it; only the second request writes.
- HTTP errors: `error instanceof HttpError` separates a 404 or 500 from a network failure (a `TypeError` from `fetch`).
- Separate `isLoading`/`error` state instead of the derived status: put `if (!ignore)` on the `finally` write as well.
- Retry of the same URL: the caller increments `reloadCount`; it changes the key, which bumps the request id used by the stored result, the dependencies and the loading check, so a retry shows loading instead of the previous result.
- A to B to A: navigating back to A before B has answered gives A a new request id, so the first A result (still stored) does not match and loading shows until the new A request writes. A test for it: resolve A, switch to B, switch back to A without resolving anything, and assert the hook returns loading, not A's old data; then resolve the new A request and assert its data. Alternatively, reset at a keyed boundary (`key={url}` on the component that calls the hook) so each URL gets a fresh hook state.
- Caching, deduplication, server rendering and waterfalls are not solved here; that is the reason to prefer the project's data layer.

## Initialization that must run once

A module-level `didInit` flag (react.dev's example) is correct only for synchronous work that cannot fail and must run once per page load. For anything else, first name the lifetime: page load, React root, component instance or auth session. Then cache the work for that lifetime and clear the cache on failure:

```ts
let initPromise: Promise<void> | null = null; // lifetime: one page load

export function ensureAppInit(): Promise<void> {
  initPromise ??= runInit().catch((error) => {
    initPromise = null; // a failed attempt must not count as done
    throw error;
  });
  return initPromise;
}
```

Call it from an `App` Effect and catch the rejection, or it surfaces as an unhandled rejection: `useEffect(() => { ensureAppInit().catch(setInitError); }, []);`. This is safe under the Strict Mode replay and remounts. The cleared cache does not retry by itself: render `initError` with a retry button whose handler calls `ensureAppInit()` again. For a per-session lifetime, key the cache by session ID and drop it on sign-out. Calling it at module top level runs it on import, even when the component never renders; do that only in the app entry module. Test: a failed first attempt followed by a retry, a remount, and a session change.
