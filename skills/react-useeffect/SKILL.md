---
name: react-useeffect
description: "Decide whether React logic belongs in render, an event handler, a key reset, useSyncExternalStore or useEffect, and fix Effects that misbehave: missing or suppressed dependencies, asymmetric cleanup, Effect chains, state copied from props, stale or out-of-order fetch responses, Strict Mode double runs and once-per-app initialization. Use when writing, reviewing or testing a component that uses useEffect or useLayoutEffect, derived or reset state, browser or store subscriptions, or useEffectEvent, even when the user only says the UI flashes old data, runs twice in development, or shows a previous search's results. Not for networking outside a React component, data-library configuration (React Query or SWR caching), routing, Server Actions, reducer design, re-render questions with no Effect involved, generic component features such as keyboard navigation, TypeScript-only typing, accessibility, or test mocking unrelated to Effects."
---

# React Effects: synchronize, then validate

An Effect synchronizes a component with a system outside React. Before keeping or writing one, name that external system. If there is none, the logic belongs in render or in an event handler.

## 1. Route the logic

| Situation | Put it in |
|---|---|
| Derived value, or work a user action caused (submit, buy, notify parent) | Render (`useMemo` only for measured cost), or that event handler |
| New identity resets all state below a boundary | `key` on that subtree |
| New identity resets one field, other state survives | Selection that should survive list updates: store the ID and derive the object during render. State that must reset when the identity changes: `key` only the identity-specific child, or adjust this component's own state during render by comparing a stored previous identity. Never key the whole subtree |
| Subscription to mutable external data | `useSyncExternalStore` when you can give a cached `getSnapshot` and a stable `subscribe`; otherwise an Effect that subscribes, reads the current value once, and unsubscribes in cleanup |
| Widget, browser API, connection, analytics on display | `useEffect`. When setup creates a reversible resource (instance, listener, connection, timer), cleanup undoes exactly that setup. Display analytics has no undo: do not invent one, and expect the setup to run twice in development (Strict Mode replay) |
| Data fetch | The project's data layer (framework loader, React Query, SWR) if one exists; a hand-rolled Effect only otherwise |
| Effect must read a latest value without re-running on it | `useEffectEvent` (stable in React 19.2+); older React: see [alternatives](references/alternatives.md#non-reactive-reads) |

An ID shared by two identities, or an earlier identity returning, does not reset a stored ID. Example: a selected message `m7` in inbox A, then inbox B also has a message `m7`; the derived selection still finds `m7`, and the same happens when A returns. If the selection must not carry over, key the identity-specific child (`<MessageView key={inboxId} />`) or compare a stored previous `inboxId` during render and reset the selection there.

Mixed logic: split it. User-caused work stays in the handler; prop-driven values are derived in render; only real synchronization stays in the Effect.

Two handlers need the same logic (a toast for Buy and for Checkout): extract one function that both handlers call; do not watch a flag in an Effect. Memoize with `useMemo` only after `console.time` around the calculation shows about 1ms or more per interaction, measured on a throttled CPU in a production build; `useMemo` does not speed up the first render.

## 2. Correctness loop

1. Write the invariant in one sentence: "while mounted with X, external system Y is in state Z."
2. Dependencies equal the reactive values read. If one re-runs the Effect too often, change its identity (move it inside, depend on a primitive) or use an Effect Event. Put create-once setup and per-prop syncs in separate Effects, so a prop change does not destroy the instance.
3. Cleanup reverses exactly this setup instance (same listener, connection, timer id). For a reversible resource, setup, cleanup, setup (the Strict Mode replay) looks the same as one setup. An irreversible effect such as display analytics has no undo: expect its setup to run twice in development and add no compensating event.
4. For async work: every write after an `await` or in `.then`, `.catch` and `.finally` checks that its run is still current.
5. Test it: render inside `<StrictMode>`, `rerender` with a new dependency, and branch by what the Effect does; `unmount` comes after the branch's assertions (for async work, after the requests are resolved and the rendered result is asserted):
   - Async request: resolve the new request and then the old one (deferred promises inside `act`) and assert the rendered result before unmounting: the newest result wins and no error from the obsolete run shows; then `unmount` and assert cleanup ran once per setup.
   - Async request, rejection case (a separate test): resolve the new request and reject the old one (deferred promises inside `act`), then assert the current result is still visible and no stale error shows, before `unmount`.
   - Widget whose lifetime is independent of the changed prop: assert the prop change reaches the existing instance, that exactly one instance is live after the Strict Mode replay (setup, cleanup, setup leaves nothing behind), and that `unmount` runs cleanup once per setup.
   - Subscription keyed by the changed prop (listener, socket or store subscription for an id or topic): after `rerender` with the new key, assert the old subscription was cleaned up and exactly one new subscription is live, and that `unmount` runs cleanup once per setup.
   - Analytics on display (no undo): assert the replay in a development build with `<StrictMode>` enabled at the root, that is two `track` calls on mount (when a configuration does not enable the initial replay, expect a single call instead of universally expecting two), one more call when the dependency changes, and no compensating event sent from cleanup.

If step 1 names no external system, stop: delete the Effect and route the logic with the table above. Otherwise fix the failing step and repeat from step 2.

## 3. NEVER

- NEVER suppress `react-hooks/exhaustive-deps`. The Effect keeps a stale closure, and the linter can no longer flag the next dependency someone adds. Fix the identity or use an Effect Event.
- NEVER use `useEffectEvent` to drop a dependency the Effect should react to, list it in a dependency array, call it during render, or pass it to another component or Hook. Its identity changes every render on purpose.
- NEVER set state in an Effect only to mirror props or other state. Every child renders once with the stale value first, and chained Effects add one render per link.
- NEVER put a purchase, POST or notification that a click caused into an Effect. It also fires on mount, on remount, and twice in Strict Mode development.
- NEVER block the Strict Mode replay with a `useRef` "already ran" flag or by disabling Strict Mode. Components remount in production too, so the flag only hides the missing cleanup the replay exposed.
- NEVER guard only the success write of a fetch. When cleanup aborts, the Strict Mode replay's first request rejects with `AbortError`; that rejection, or any obsolete request's `catch` or `finally`, overwrites the current request's state unless every write checks the same `ignore` flag.
- NEVER rely on `AbortController` alone for stale responses: async steps after the `fetch` that do not take the signal still resolve. Keep the `ignore` flag; abort only saves bandwidth, and it does not undo server-side work.
- NEVER treat a resolved `fetch` as success: it resolves for 404 and 500. Check `response.ok` and give HTTP errors their own state, distinct from network rejection.
- NEVER return a new object or array from `getSnapshot` on each call. React compares snapshots with `Object.is`, so it re-renders without end ("The result of getSnapshot should be cached").
- NEVER set a module-level "initialized" flag before async or fallible work succeeds. A failed first attempt then looks complete forever. Name the lifetime first (page load, React root, auth session) and cache the work for that lifetime, cleared on failure.
- NEVER run browser-only initialization at module top level of a server-rendered app without `if (typeof window !== 'undefined')`: top-level code runs on import, on the server too. Keep it in a module guaranteed to execute in the client, or use a client component's Effect with the cached initialization promise.

## 4. Load only what the task needs

- Auditing existing Effects, a fetch race, a stale write, or "runs once" initialization: read [anti-patterns](references/anti-patterns.md). It has the smell catalog, a complete fetch hook and the initialization cache.
- Designing state ownership, a partial reset, a `useSyncExternalStore` store, or a non-reactive read on React before 19.2: read [alternatives](references/alternatives.md).
- Deciding whether a calculation needs `useMemo` (measuring steps, React Compiler), two handlers that share logic, or module-level initialization in a server-rendered app: read [restored-patterns](references/restored-patterns.md).
- A simple routing question (derived value, event handler, `key`): the table above is enough; load neither file.

Based on react.dev, [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect).
