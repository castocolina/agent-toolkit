# Designing without an Effect: the hard boundaries

The routing table in SKILL.md covers the common cases. This file covers the three boundaries where the obvious answer is wrong.

## Partial identity reset

A `key` resets every piece of state under it. When only some state belongs to the new identity, pick the first option that fits:

1. Store the identity, not the object, and derive during render. Nothing needs resetting, and a selection survives when the item is still in the new list:

   ```tsx
   const [selectedId, setSelectedId] = useState<string | null>(null);
   const selection = items.find((item) => item.id === selectedId) ?? null;
   ```

2. Move the identity-specific state into a child and key only that child (`<Comments key={postId} />`), so sibling state such as a sort order survives.

3. Adjust during render by comparing a stored previous value:

   ```tsx
   const [prevItems, setPrevItems] = useState(items);
   if (items !== prevItems) {
     setPrevItems(items);
     setSelection(null);
   }
   ```

   React discards this render's output and re-renders the same component before its children render, so no child sees the stale selection. The comparison is required to avoid a loop. Only the component's own state may be set this way; setting another component's state during render is an error, and side effects (DOM, timers) still belong in handlers or Effects.

## External store snapshots

```tsx
import { useSyncExternalStore } from 'react';

function subscribe(onChange: () => void) { // module level: one identity, no resubscribe per render
  window.addEventListener('online', onChange);
  window.addEventListener('offline', onChange);
  return () => {
    window.removeEventListener('online', onChange);
    window.removeEventListener('offline', onChange);
  };
}

export function useOnlineStatus() {
  return useSyncExternalStore(
    subscribe,
    () => navigator.onLine, // primitive: stable while unchanged
    () => true,             // server and hydration snapshot
  );
}
```

- An inline `subscribe` has a new identity every render, so React resubscribes on every render. Hoist it, or wrap it in `useCallback` keyed by its real arguments.
- For a mutable store that returns objects, keep the last snapshot with the store version it was built from, and rebuild it only when the version changes.
- The third argument is required for server rendering. It must return what the server rendered; returning the live client value there causes a hydration mismatch.
- A store with no change event needs an observation mechanism first: write an adapter that notifies subscribers, for example one `setInterval` poll (choose the interval; clear it when the last subscriber leaves) that reads the value and notifies only when it changed, and pass that adapter's `subscribe` and a cheap cached `getSnapshot` to `useSyncExternalStore`. Without any such mechanism, live synchronization cannot be guaranteed: read once on mount and say it can go stale.
- When reading is too costly to repeat every render, cache the snapshot in the adapter (see the version rule above).

## Non-reactive reads

An Effect sometimes needs the latest value of something (the theme for a notification, the cart for a log) without re-running when it changes.

React 19.2 and later: wrap that logic in `useEffectEvent`, call it only from inside the Effect, and leave it out of the dependency array:

```tsx
const onConnected = useEffectEvent(() => showNotification('Connected!', theme));

useEffect(() => {
  const connection = createConnection(roomId);
  connection.on('connected', () => onConnected());
  connection.connect();
  return () => connection.disconnect();
}, [roomId]);
```

Before React 19.2, `useEffectEvent` exists only as `experimental_useEffectEvent` in experimental and canary builds; do not ship that. Use a ref updated after each commit instead, and call `latest.current()` inside the Effect:

```tsx
const latest = useRef(handler);
useLayoutEffect(() => {
  latest.current = handler; // never write ref.current during render
});
```

Check first that the value really is non-reactive. If the Effect should re-synchronize when it changes (a `roomId`, a URL), it is a dependency, and neither tool applies.
