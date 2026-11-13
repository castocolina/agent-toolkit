---
name: react-dev
metadata:
  version: "1.0.0"
description: "Type React 18 and 19 code in TypeScript: component props and refs, event handlers, generic components that infer row or option types, React 19 Actions (useActionState, useOptimistic, use), Server Components and Server Actions, and TanStack Router or React Router v7/v8 typing. Use for .tsx work, React 19 or router upgrades, and requests like 'type this prop or handler', 'make the table infer the row type', 'replace useFormState', 'type the loader or search params'. Not for useEffect bugs or deciding whether an Effect is needed (react-useeffect), React Native, non-React or plain-JS code, styling-only or test-only work."
---

# React TypeScript

Pin the versions, classify the problem, load one reference, then prove the contract with the type checker.

## 1. Pin versions before choosing an API

Read `package.json` (and the lockfile if ranges are wide) for `react`, `@types/react`, the router and the framework.

Migration target first: when the task is upgrading an app to React 19, the target is 19 regardless of what is installed.
0. Before touching anything, run `git status --porcelain`. If it prints anything, ask the user to commit or stash first, or work in a separate clean `git worktree` from HEAD, so the later diff shows only the upgrade.
1. Update `react`, `react-dom`, `@types/react` and `@types/react-dom` to 19 together.
2. With `<dirs>` = the real source roots (from `tsconfig.json` `include` and the layout: `app/`, `components/`, `src/`, or each package's source directory), run `npx types-react-codemod@3.5.3 preset-19 <dirs>`, then always the two transforms it leaves off by default (eps1lon/types-react-codemod README, https://github.com/eps1lon/types-react-codemod, checked 2026-11-07): `npx types-react-codemod@3.5.3 no-implicit-ref-callback-return <dirs>` and `npx types-react-codemod@3.5.3 react-element-default-any-props <dirs>`. Fix by hand only what a transform could not rewrite.
3. Review `git diff`, then typecheck (step 5). A published package whose peers allow 18 stays React 18-compatible unless changing that peer contract was requested.

Otherwise, preflight: if the installed `react` major and the `@types/react` / `@types/react-dom` majors differ, pin the types to the runtime major first; otherwise every later type error is noise. Then pick the API target; first matching row wins:

| You find | Write |
|---|---|
| A library or shared package whose `peerDependencies` still allow 18 (even with `react` 19 in `devDependencies`) | React 18-compatible code: `forwardRef`, no `use`, `useActionState` or `useOptimistic` |
| `react` 18 in `dependencies` | React 18-compatible code, as above |
| `react` 19 in `dependencies` | React 19 APIs: `ref` as a prop, `useActionState`, `use`, `useOptimistic` |
| No `package.json` in view, but the user names a major ("React 19 Button") | the requested major's APIs, and say the target was taken from the request |
| Neither metadata nor a requested major | React 18-compatible code, and say that you assumed it |

## 2. Classify, then load only what the task needs

Before writing any component, ask where it renders:

| Kind | How to tell | Applies |
|---|---|---|
| Server Component | RSC framework (Next.js App Router), file without `'use client'` and not imported from one | no hooks or browser APIs; `await` data; may call Server Actions |
| Server- or build-time-rendered client component | inside the client boundary of an SSR/RSC app (Next.js, React Router Framework Mode), including React Router `ssr: false` SPA mode (the root still renders at build time into `index.html`) and any prerendered route | renders without a browser, then hydrates: browser globals only in effects and event handlers, hydration-stable first render |
| Browser-only (CSR) component | a plain Vite/CRA app mounted with `createRoot` and no prerender step, or a subtree confirmed client-only (`next/dynamic` with `ssr: false`, rendered only after mount) | `window` is safe in render; no hydration constraint |

`'use client'` marks the boundary where server modules hand over to client modules; it does not mean browser-only execution. When unsure which kind applies, treat it as server-rendered.

| Task | Read | Do NOT load |
|---|---|---|
| Native-element wrapper, variants, children, refs | this file only | routers, server examples |
| Generic table, select or list that must infer `T` | [examples/generic-components.md](examples/generic-components.md) | react-19-patterns.md unless refs are involved |
| Reading values from events, IME, native vs synthetic events | [references/event-handlers.md](references/event-handlers.md) | everything else |
| Hook typing, context, external stores, storage or SSR-safe state | [references/hooks.md](references/hooks.md) | routers |
| Actions, `useOptimistic`, `use`, transitions, React 19 migration | [references/react-19-patterns.md](references/react-19-patterns.md) | server examples unless the app has Server Components |
| Server Components, Server Actions, Next.js App Router pages | [examples/server-components.md](examples/server-components.md), plus react-19-patterns.md for the hooks | router references |
| Routing | the installed router's reference only | the other router's reference |
| React 19 migration plus a router upgrade | react-19-patterns.md and the installed router's reference together | server examples unless the app uses them |

Router choice, in order:
1. One router installed: [TanStack Router](references/tanstack-router.md) or [React Router](references/react-router.md), matched to the installed major (React Router v7 and v8 type `context` differently).
2. Both installed: the one that owns route definitions (`createRouter` with a route tree, or `routes.ts` / `createBrowserRouter`).
3. Next.js App Router: no router reference; params come from file conventions (see server examples).
4. None installed, greenfield, typed validated search params needed: TanStack Router.
5. None installed in an existing app: keep its current navigation, do not recommend installing a router, and say what stays untyped.

## 3. Contracts that are easy to get wrong

Activation checklist, no explanation needed: native props via `ComponentPropsWithoutRef<'button'>`, variants as a discriminated union, `children: ReactNode`, an explicit state type when the initializer is `null`, `[]` or one member of a literal union.

| Ref need | Use |
|---|---|
| Component used only by a React 19 app | `ref?: Ref<HTMLButtonElement>` as an ordinary prop |
| Library or shared package whose peers allow React 18 | `forwardRef`; it still works in 19 (React plans to deprecate it later, it is not removed) |
| Generic component plus a ref on React 18 | `forwardRef` erases `T`; re-assert the call signature (react-19-patterns.md) |
| Parent calls commands (`focus`, `clear`) on the component | `useImperativeHandle`; type the ref `Ref<Handle>` with the handle, not the element (react-19-patterns.md) |

| Form need (React 19; on 18 use `onSubmit` with your own state) | Use |
|---|---|
| Returned state, validation errors or pending flag for a form | `const [state, formAction, isPending] = useActionState(action, initial)` from `react`; the action is `(previousState, formData)` and returns the same state type on every path; disable submit with `isPending` (`useFormState` had no third element, so migrations must add it) |
| Pending flag inside a child of the form | `useFormStatus` from `react-dom` |
| Mutation with nothing to show back | `<form action={fn}>` directly |
| React Router route mutation | route `action` with `<Form>` or `useFetcher`; do not wrap it in `useActionState` |

Before writing a generic API, ask: which two positions must agree (a key and its value, a key and its renderer), and which type parameter carries that agreement to both? If the answer is "`keyof T` on one side and `T[keyof T]` on the other", the API accepts mismatched pairs. Capture the key per call instead:

```tsx
type Column<T> = { header: string; cell: (row: T) => ReactNode };

function columnsFor<T>() {
  return <K extends keyof T>(
    key: K,
    header: string,
    render: (value: T[K], row: T) => ReactNode = (value) => String(value),
  ): Column<T> => ({ header, cell: (row) => render(row[key], row) });
}

type User = { id: number; name: string; createdAt: Date };
const col = columnsFor<User>();
const columns: Column<User>[] = [                              // runtime array: valid renderers only
  col('name', 'Name', (name) => name.toUpperCase()),           // name: string
  col('createdAt', 'Created', (d) => d.toLocaleDateString()),  // d: Date
];

// columns.type-test.tsx: compile-only, never called or imported by app code.
export function columnContract() {
  // @ts-expect-error createdAt is a Date, so a string renderer is rejected
  col('createdAt', 'Created', (value: string) => value.trim());
}
```

`K` is checked inside each `col` call; packaging into `Column<T>` drops `K` only after the pairing is proven, so the array stays one plain type. The uncorrelated shape `{ key: keyof T; render: (value: T[keyof T]) => ReactNode }` loses key-specific contextual typing: every renderer receives `string | number | Date`, so `(d) => d.toLocaleDateString()` fails and authors reach for casts. Under `strictFunctionTypes` (part of `strict`) it rejects a `(value: string) => ...` renderer, but declared with method syntax (`render(value: T[keyof T]): ReactNode`) or with `strictFunctionTypes` off, parameters are bivariant and that narrower renderer is accepted, then crashes at runtime.

## 4. Gotchas

- Handlers: with several submit buttons read `(e.nativeEvent as SubmitEvent).submitter` (`currentTarget` is the form); before treating Enter as submit, skip it while composing (`e.nativeEvent.isComposing || e.nativeEvent.keyCode === 229`); for Enter-to-send in a `<textarea>`, also let Shift+Enter through and call `preventDefault()` only on the Enter you handle, then `requestSubmit()` once. Code in event-handlers.md.
- NEVER read `window` or `localStorage` during render or in a `useState` initializer of a server-rendered client component (any `'use client'` file in an SSR or RSC app): it also renders on the server, so you get a server `ReferenceError` or a hydration mismatch. Start from a hydration-stable value, read after mount inside `try`, validate the parsed JSON, and never write until the current key has been read (a key change must not write the old key's value).
- NEVER trust Server Action arguments, including `.bind` arguments and hidden inputs: every exported action is a public POST endpoint, and a page-level auth check does not cover it. Authenticate and authorize the target resource inside each action and return a typed failure state. Keep actions in a `'use server'` module; a `'use client'` file can import them but cannot define one inline.
- NEVER create the promise for `use()` during client render: a new promise each render shows the Suspense fallback every render. Create it in a Server Component or a cache keyed by resource id; in a Server Component just `await`. Never wrap `use()` in `try/catch` (it throws to suspend); use an Error Boundary.
- NEVER assume state set after an `await` inside `startTransition` is a transition: React requires another `startTransition` around those setters.
- NEVER drive a text input's value from a transition: transitions cannot control text inputs. Keep the input state urgent and defer the expensive child with `useDeferredValue` plus `memo`.
- NEVER call the `useOptimistic` setter outside an Action or transition: React warns and the optimistic value only flashes. Give each optimistic item a unique temporary id (`crypto.randomUUID()`), treat `!res.ok` as a failure, commit the server's record to the base state only after success (inside a new `startTransition`), and on failure leave the base state unchanged so the optimistic item disappears, then show an error.
- NEVER leave a `useActionState` action's return type to inference: a success path that falls through returns `undefined`, widening state to `State | undefined`, and the errors appear at the `useActionState` call and wherever `state` is read, not in the action. Annotate the action as returning `Promise<State>` so the missing return fails in the action itself.
- NEVER read TanStack Router `beforeLoad` output with `useLoaderData`: it is route context (`useRouteContext`). And NEVER skip the `Register` declaration: without it `Link` and `useNavigate` fall back to loose types and stop checking route literals.
- NEVER pass a Zod 3 schema with `.default()` straight to TanStack Router `validateSearch`: its input type then requires `search` on every `Link` to the route. Wrap it in `zodValidator()` from `@tanstack/zod-adapter` and use `fallback(schema, value)`; Zod 4 schemas go in directly. In `loaderDeps`, return only the search keys the loader uses: returning all of `search` reloads on every unrelated key change.
- NEVER keep `declare module 'react-router' { interface AppLoadContext }` on React Router v8: middleware is always on and `context` is a `RouterContextProvider`. Type each value with `createContext`, read it with `context.get`, and make a custom server's `getLoadContext` return a `RouterContextProvider`. In Framework Mode, type loaders with `Route.LoaderArgs` from `./+types/<route>`, not hand-written argument types.
- NEVER type Next.js 15+ `params` or `searchParams` as plain objects: they are Promises; `await` them in Server Components and `use()` them in Client Components.
- React 19 upgrade breaks: `act` moves from `react-dom/test-utils` to `react` and the other test-utils are removed; `@types/react` 19 requires a `useRef` argument, rejects ref callbacks with an implicit return (`ref={(n) => (x = n)}` needs a block body), drops the global `JSX` namespace for `React.JSX`, and types `ReactElement` props as `unknown`. The migration order and codemods are in step 1.

## 5. Validate

1. Regenerate route types only where the project generates them, or errors describe stale routes:

   | Project | Generate with |
   |---|---|
   | React Router Framework Mode (`@react-router/dev` installed) | `react-router typegen` |
   | TanStack Router file-based routing | its configured `@tanstack/router-plugin` (runs with dev/build) or `tsr generate` from `@tanstack/router-cli` |
   | Next.js 15.5+ using `PageProps` / `LayoutProps` helpers | `next typegen` (not available before 15.5; Next.js 15.5 release post, https://nextjs.org/blog/next-15-5, checked 2026-11-07) |
   | React Router Data or Declarative Mode, TanStack code-based routes, no router | nothing; never install router tooling just to validate |

2. Run the project's typecheck script, or `npx tsc --noEmit -p .` when a `tsconfig.json` exists. If that `tsconfig.json` is a solution file (`"files": []` plus `references`, as in the Vite react-ts template), `-p .` checks nothing and passes silently: run `npx tsc -b`, or `npx tsc --noEmit -p tsconfig.app.json` on the referenced app config, and check that config's `include` covers your `*.type-test.tsx` files. If it fails, fix the first error your change caused, rerun, and repeat until it passes; report errors that existed before your change separately. With no tsconfig, say the contract is unchecked.
3. Put each designed contract's rejected case as a `// @ts-expect-error` line inside an uncalled, exported function (exported so `noUnusedLocals` does not fail it with TS6133) in a `*.type-test.ts` / `*.type-test.tsx` file that the `noEmit` typecheck includes (check the tsconfig `include` globs cover it). It fails the typecheck if the contract loosens and never runs. Do not use `.d.ts` / `.test-d.ts` for this: declaration files cannot hold function bodies, and `.test-d.ts` needs a separately configured runner such as `tsd`.
4. Report the React and router versions you assumed, and any guarantee left to runtime validation.
