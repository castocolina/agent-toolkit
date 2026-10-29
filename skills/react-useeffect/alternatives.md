# Alternatives to useEffect

| Need | Prefer | Boundary to preserve |
|---|---|---|
| Derive a value from props/state | Compute during render | Add memoization only for measured cost or required identity stability; do not mirror derivable values in state. |
| Expensive pure calculation | `useMemo` or compiler optimization | Memoization is not a correctness or lifetime guarantee. |
| Reset state for a new identity | `key` on the smallest subtree that owns the reset | A key resets all descendant state. For a partial reset, keep the changing identity with the local state and adjust during render only when the stored identity differs; do not clear unrelated state or flash stale UI in an Effect. |
| Respond to a user action | Event/action handler | Keep the action tied to the event; share a function when multiple events genuinely share work. |
| Subscribe to mutable external data | `useSyncExternalStore` | `subscribe` must clean up and remain stable; snapshots must preserve identity while unchanged, and the server snapshot must match hydration. |
| Synchronize with an external system | `useEffect` with cleanup | Effects are for external synchronization, not state-to-state orchestration. Cleanup must undo the specific setup instance. |
| Share state between components | Lift state to the common owner | Avoid sibling Effects that race to synchronize duplicate state. |
| Fetch route or server data | Framework/router loader or a cache | Component Effects need stale-result protection and explicit loading/error semantics; abort where supported, but cancellation does not prove the server stopped work. |

## Difficult boundaries

- **Partial identity reset:** Use a key only when all state below that boundary belongs to the new identity. If only a subset changes, associate that subset with its identity and derive the reset synchronously, or move ownership to the identity-specific child. Avoid an Effect that renders one frame of stale data before resetting.
- **External snapshots:** `getSnapshot` must return a cached/stable value until the underlying store changes. Returning a fresh object each call can produce repeated renders. Keep subscription identity stable and make server and initial client snapshots hydration-compatible.
- **Initialization lifetime:** “Once” must mean once per page, root, component, or auth session. Do not assume an Effect with `[]` is once globally: Strict Mode may replay it in development, roots/remounts have separate lifetimes, and failures need retry semantics. Prefer idempotent work and a lifetime-scoped cache with explicit failure handling.
- **Async cleanup:** Cleanup can mark a request obsolete or abort client work, but cannot undo an already committed server-side mutation. Guard every post-await state write against stale identity; mutations should use operation identity/idempotency rather than relying on unmount cancellation.
