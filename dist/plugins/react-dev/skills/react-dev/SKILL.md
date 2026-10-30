---
name: react-dev
metadata:
  version: "1.0.0"
description: "Build and refactor type-safe React 18–19 components, hooks, events, forms, refs, Server Components, and TanStack Router or React Router v7 integrations. Use for .tsx work or when props, event targets, nullable hook state, generic inference, route params, or React 19 migrations need TypeScript help. Not for non-React TypeScript, vanilla JavaScript React, React Native navigation, styling-only or test-only work, or general runtime effect debugging."
---

# React TypeScript

Classify the problem before choosing a pattern: native-element extension, variant union, generic key/value invariant, action state, server/client boundary, or routing. Identify each guarantee's source (schema, framework, or caller), preserve it through the API, then verify the contract before expanding implementation.

## Core contracts

- Extend native props with `ComponentPropsWithoutRef<'button'>`; model mutually exclusive variants as discriminated unions. `ReactNode` covers text, numbers, null, and elements; `JSX.Element` does not.
- Explicitly type state when initialized as `null` or a narrow literal union. DOM refs are nullable and need checks. React 19 requires a `useRef` initializer; timer refs can use `useRef<ReturnType<typeof setTimeout> | undefined>(undefined)`.
- Keep generic relationships intact. A column keyed by `K extends keyof T` must not receive `T[keyof T]` as if it were the value for that particular key. A safe general renderer accepts the whole row; property-specific renderers should capture `K` in a builder.
- Use `useActionState` when returned state or validation feedback is needed; its action must accept `(previousState, payload)` and return the same state shape on every path. Keep simple direct actions and router-managed Form/useFetcher flows when they suffice.
- Default to ref-as-prop in React 19-only components; use `forwardRef` when supporting React 18-compatible libraries. Explicit tuple return annotations and `as const` both preserve tuple shape.

## React 19 execution boundaries

`use()` can be conditional or in loops, but a suspending call needs an ancestor Suspense boundary and a stable promise from a Server Component or Suspense-enabled cache. Creating a fresh promise during client render can repeatedly suspend. Keep server actions in a server module; `'use client'` modules cannot define inline `'use server'` actions. A Client Component can still be server-rendered; a client-only marker does not make browser globals safe during render.

For `useOptimistic`, dispatch updates from an Action/transition. After an `await`, mark base-state updates with a new transition where needed; handle failures so optimistic state rolls back.

## Router decision and references

Use the router already installed. For a greenfield app requiring typed validated search params, default to TanStack Router. Load only the installed router's reference. Distinguish React Router Framework Mode from Data Mode. Load React 19 patterns only for React 19 work; load server examples only in a compatible framework. Event- or hook-only work does not need router/server manuals.

- [TanStack Router](references/tanstack-router.md): route trees, search validation, loaders, context.
- [React Router](references/react-router.md): load for installed React Router version/mode.
- [React 19 patterns](references/react-19-patterns.md): Actions, `use`, optimistic updates, migration.
- [Hooks](references/hooks.md): load for nontrivial ref/hook typing questions.
- [Event handlers](references/event-handlers.md): load for currentTarget/value extraction or specialized handlers.
- [Generic component example](examples/generic-components.md): load when implementing generic inference.
- [Server component examples](examples/server-components.md): load for framework execution boundaries.

## Gotchas

- Do not use `any` for event handlers: it discards the target guarantees that make `currentTarget` safe.
- Do not read `event.target.value` as though it were a string: `target` may be a descendant and its value is not generally typed. Prefer a constrained element and `currentTarget`.
- Do not mismatch an action's return value and `useActionState` initial state; the tuple type encodes the action's state contract.
- Do not read `beforeLoad` output with `useLoaderData`; it is route context. Follow the installed router's typed APIs and loader-dependency flow for validated search.
