# TanStack Router Typing

Load only when `@tanstack/react-router` is installed (or chosen for a greenfield app). The type safety comes from three places that are easy to skip: registering the router, validating search, and routing data through `loaderDeps` and context.

## 1. Register the router once

```ts
// src/router.tsx
import { createRouter } from '@tanstack/react-router';
import { routeTree } from './routeTree.gen';     // written by @tanstack/router-plugin (Vite, Rspack, Webpack) or the CLI

export const router = createRouter({ routeTree, context: { queryClient } });

declare module '@tanstack/react-router' {
  interface Register { router: typeof router }
}
```

Without `Register`, top-level `Link`, `useNavigate` and `useSearch` do not know your routes. `routeTree.gen.ts` is generated: commit it or generate it before `tsc` in CI, and never edit it by hand.

## 2. Route-bound hooks over `from` strings

| Where the component lives | Read params, search, loader data with |
|---|---|
| In the route file | `Route.useParams()`, `Route.useSearch()`, `Route.useLoaderData()`, `Route.useRouteContext()` |
| Code-split file without the `Route` import | `const route = getRouteApi('/users/$userId')`, then `route.useSearch()` |
| Shared component rendered under many routes | `useSearch({ strict: false })`: every key optional, still typed |

A `from` that does not match the rendering route throws at runtime. A `Link` without `from` checks `to` against the union of every route, which is slow on large trees; pass `from` to narrow it.

## 3. Search validation depends on the Zod major

```tsx
// Zod 4 (or Valibot, ArkType): pass the schema directly
validateSearch: z.object({ page: z.number().int().min(1).catch(1), sort: z.enum(['new', 'top']).catch('new') }),

// Zod 3: use the adapter, or `search` becomes required on every Link to this route
import { zodValidator, fallback } from '@tanstack/zod-adapter';
validateSearch: zodValidator(z.object({ page: fallback(z.number().int().min(1), 1).default(1) })),
```

Why the adapter matters is in the SKILL.md gotcha; inside it use `fallback()`, not Zod 3 `.catch()`, which types the field as `unknown`. Search values are parsed as JSON, so `page=2` arrives as a number; no `z.coerce` needed.

Keep or drop search keys across links with middlewares on the route: `search: { middlewares: [retainSearchParams(['locale']), stripSearchParams({ page: 1 })] }`.

## 4. Loader data, `loaderDeps` and context

```tsx
export const Route = createFileRoute('/products')({
  validateSearch: productSearch,
  loaderDeps: ({ search }) => ({ page: search.page, sort: search.sort }), // only these keys refetch and key the cache
  beforeLoad: async ({ context, location }) => {
    const user = await context.auth.getUser();
    if (!user) throw redirect({ to: '/login', search: { redirect: location.href } });
    return { user };                                                    // merged into context for this route and children
  },
  loader: ({ deps, context }) => context.queryClient.ensureQueryData(productsQuery(deps, context.user.id)),
});

function Products() {
  const { user } = Route.useRouteContext();                   // beforeLoad output: context, not loader data
  const deps = Route.useLoaderDeps();
  const { data } = useSuspenseQuery(productsQuery(deps, user.id)); // never undefined: the loader ensured it
}
```

- Loaders cannot read `search` directly; anything not listed in `loaderDeps` neither refetches nor separates cache entries, so two pages share one cached result.
- Type the root context once with `createRootRouteWithContext<{ queryClient: QueryClient; auth: Auth }>()({ ... })`; `createRouter` then requires a matching `context`.
- With TanStack Query, `useSuspenseQuery` (not `useQuery`) after `ensureQueryData` gives non-optional `data`.

## 5. Update search with a functional updater

Give `useNavigate` the route it renders under, then pass `search` as a function of the previous search. `prev` and the returned object are checked against that route's `validateSearch`, so a wrong key or value type fails to compile and the other params survive the update:

```tsx
// src/routes/products.tsx
const navigate = useNavigate({ from: Route.fullPath });

const setCategory = (category: string) =>
  navigate({ search: (prev) => ({ ...prev, category, page: 1 }) });  // keep sortBy, reset page

const setSort = (sortBy: 'price' | 'name') =>
  navigate({ search: (prev) => ({ ...prev, sortBy }) });             // sortBy: 'rating' is a type error

<Link from={Route.fullPath} search={(prev) => ({ ...prev, page: prev.page + 1 })}>Next</Link>  // `to` may be omitted when `from` is set
```

Without `from` the router cannot assume the current route, so `prev` has every key optional and `{ ...prev, page: 1 }` fails against a route whose keys are required (here `sortBy`). In a shared component rendered under several routes, read with `useSearch({ strict: false })` (section 2) and navigate with an explicit `to` and a `search` object that sets every required key. Spread `prev` rather than passing a fresh object, or every param not named is dropped. Sources: https://tanstack.com/router/latest/docs/framework/react/guide/search-params (sections on `useNavigate`, `Link` and `strict: false`), checked 2026-11-07; the snippet type-checked under `strict` with `@tanstack/react-router` 1.170.46 and a registered router.

## Type helpers

Prefer narrowed helpers over bare ones: `LinkProps` without type arguments resolves against every route. Use `as const satisfies LinkProps` (or `LinkProps<RegisteredRouter, '/posts'>`) for reusable link objects, or `ValidateLinkOptions` in a wrapper component's props so its `to` stays checked.
