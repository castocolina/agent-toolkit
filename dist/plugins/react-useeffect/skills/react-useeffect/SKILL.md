---
name: react-useeffect
description: "Review and refactor React behavior involving useEffect, derived state, subscriptions, and stale fetch responses. Use when asking about Effect dependencies/cleanup, avoiding redundant renders, or testing Effect behavior with React Testing Library. Not for standalone React Testing Library mocks, generic component features such as dropdown keyboard navigation, reducer-only undo/redo, generic networking, cache-library configuration, routing, Server Action forms, or TypeScript-only typing unless the question specifically concerns Effect/state-synchronization choices."
---

# React Effects: synchronize, then validate

An Effect synchronizes React with an external system. Before writing one, name the external system; if none exists, keep the logic in render or an event handler.

| Situation | Preferred location |
|---|---|
| Derived value / transformation | Render; `useMemo` only for measured expensive work |
| User-triggered action | Event handler |
| Prop/state changes require derived value | Render calculation |
| Identity change resets all local state | `key` on the subtree |
| Identity change adjusts one field but preserves other state | Derive that field or use a scoped adjustment; do not key the whole subtree |
| External subscription | `useSyncExternalStore` when its snapshot/subscribe contract fits |
| External widget/browser API/visibility analytics | Effect with symmetric cleanup where applicable |
| Fetch | Existing project data framework (React Query, SWR, framework loader) by default; hand-rolled Effect only otherwise |

Mixed event and prop logic: split it. Keep user-caused work in the event handler; derive prop-dependent values during render or synchronize an actual external system in an Effect.

## Effect correctness loop

1. State the synchronization invariant and external system.
2. Choose the branch above; don't use an Effect merely to copy React state into React state.
3. Check dependencies against every reactive value read. If dependencies cause unwanted repetition, fix identity/logic rather than suppressing the linter.
4. Pair setup with cleanup that reverses the subscription/resource created. Cleanup must tolerate repeated invocation: Strict Mode replays setup/cleanup in development to expose asymmetry; it is not a reason to disable Strict Mode.
5. Test rapid dependency changes and mount/unmount. For fetches, ensure stale results cannot win and handle non-2xx responses distinctly from network rejection.

Effects capture a render's values. A stale closure is not repaired by omitting a dependency; it is repaired by correct dependencies and an appropriate lifetime/identity strategy. External subscriptions must also provide a stable snapshot contract for concurrent rendering and SSR/hydration.

## Task-gated detail

Read [anti-patterns](anti-patterns.md) when auditing existing Effects, fetch races, notification chains, or initialization bugs. Read [alternatives](alternatives.md) when designing state logic, resetting identity, lifting state, or subscribing to an external store.
