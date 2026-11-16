# React Router v7 and v8 Typing

Load only when `react-router` is the installed router. Read its major and mode first; most typing mistakes come from applying one mode's API to another.

## Mode and version decide the API

| You see | Mode | How route types arrive |
|---|---|---|
| `app/routes.ts`, `@react-router/dev`, `react-router.config.ts` | Framework | generated `./+types/<route>` per route module |
| `createBrowserRouter([...])` with `loader` / `action` | Data | inferred by hand: `useLoaderData<typeof loader>()` |
| `<BrowserRouter>` / `<Routes>` only | Declarative | no loaders; `useParams` returns `string \| undefined` values |

| Topic | v7 | v8 |
|---|---|---|
| Middleware | 7.9+: opt-in `future.v8_middleware`, unprefixed APIs; 7.3 to 7.8: opt-in `future.unstable_middleware`, `unstable_`-prefixed APIs | always on, unprefixed APIs |
| `context` in loaders, actions, middleware | `AppLoadContext` (module augmentation) unless middleware is enabled, then `RouterContextProvider` | always `RouterContextProvider`; `AppLoadContext` is gone (removed in 8.0.1) |
| Custom server `getLoadContext` | may return a plain object without middleware | must return a `RouterContextProvider` |

## Framework Mode setup

```json
{
  "include": [".react-router/types/**/*"],
  "compilerOptions": { "rootDirs": [".", "./.react-router/types"] }
}
```

Git-ignore `.react-router/`. `react-router dev` regenerates types when `routes.ts` changes, but CI does not: use `"typecheck": "react-router typegen && tsc"`, or `tsc` reports errors against stale or missing `+types`.

```tsx
// app/routes/product.tsx
import { data, isRouteErrorResponse } from 'react-router';
import type { Route } from './+types/product';

export async function loader({ params }: Route.LoaderArgs) {
  const product = await getProduct(params.id);              // params.id: string, from the route path
  if (!product) throw data('Product not found', { status: 404 });
  return { product };
}

export default function Product({ loaderData }: Route.ComponentProps) {
  return <h1>{loaderData.product.name}</h1>;                // typed from loader, no generic needed
}

export function ErrorBoundary({ error }: Route.ErrorBoundaryProps) {
  if (isRouteErrorResponse(error)) return <p>{error.status} {error.data}</p>;
  return <p>Unexpected error</p>;
}
```

Generated names: `Route.LoaderArgs`, `ClientLoaderArgs`, `ActionArgs`, `ClientActionArgs`, `ComponentProps`, `ErrorBoundaryProps`, `HydrateFallbackProps`. Do not hand-write `useLoaderData<...>()` generics in Framework Mode; they drift from the loader. `throw data(...)` payloads are not sanitized in production the way thrown `Error` messages are, so never put internals in them.

## Typed context (v8, or v7.9+ with `future.v8_middleware`)

The code below uses the stable names. On 7.3 to 7.8 the same APIs are prefixed and the flag differs:

| 7.9+ and v8 | 7.3 to 7.8 |
|---|---|
| `future: { v8_middleware: true }` (v7 only) | `future: { unstable_middleware: true }` plus `declare module 'react-router' { interface Future { unstable_middleware: true } }` |
| `export const middleware`, `export const clientMiddleware` | `export const unstable_middleware`, `export const unstable_clientMiddleware` |
| `Route.MiddlewareFunction`, `Route.ClientMiddlewareFunction` | `Route.unstable_MiddlewareFunction`, `Route.unstable_ClientMiddlewareFunction` |
| `createContext`, `RouterContextProvider` | `unstable_createContext`, `unstable_RouterContextProvider` |

The unstable API changed shape across 7.x (notably in 7.8), so prefer upgrading to 7.9+ before adding middleware; write the prefixed form only when the version cannot move.

```ts
// app/context.ts
import { createContext } from 'react-router';
export const userContext = createContext<User | null>(null);

// app/root.tsx
export const middleware: Route.MiddlewareFunction[] = [
  async ({ request, context }, next) => {
    context.set(userContext, await getUserFromSession(request));
    return next();                                         // server middleware returns the Response
  },
];

// any loader below it
export async function loader({ context }: Route.LoaderArgs) {
  const user = context.get(userContext);                   // User | null
}
```

Upgrading v7 to v8: delete the `declare module 'react-router' { interface AppLoadContext { ... } }` block, create one `createContext` per value, and make `getLoadContext` build a `new RouterContextProvider()` and `set` each value. Client-side middleware is `clientMiddleware: Route.ClientMiddlewareFunction[]`.

## Search params are untyped

`useSearchParams()` and `new URL(request.url).searchParams` give strings. Parse once in the loader and return the typed result, so the component reads it from `loaderData` instead of re-parsing:

```ts
const searchSchema = z.object({ page: z.coerce.number().int().min(1).catch(1), q: z.string().catch('') });

export async function loader({ request }: Route.LoaderArgs) {
  const search = searchSchema.parse(Object.fromEntries(new URL(request.url).searchParams));
  return { search, results: await findProducts(search) };
}
```

`Object.fromEntries` keeps only the last value of a repeated key; use `searchParams.getAll('tag')` for arrays.

## Mutations

| Need | Use |
|---|---|
| Submit and navigate (create, then go to the new page) | `<Form method="post">` + route `action`, `redirect()` from the action |
| Submit without navigating (like button, inline edit) | `const fetcher = useFetcher<typeof action>()`; `fetcher.data` is the action's return type |
| Action result on the current page | `actionData` in `Route.ComponentProps` (Framework) or `useActionData<typeof action>()` (Data) |
| Pending UI | `useNavigation().state` for navigations, `fetcher.state` for fetchers |

Return validation errors with `data({ errors }, { status: 400 })` instead of throwing, so the form re-renders with them rather than hitting the ErrorBoundary.
