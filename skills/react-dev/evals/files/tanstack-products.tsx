// src/routes/products.tsx (file-based routing via @tanstack/router-plugin)
import { createFileRoute } from '@tanstack/react-router';
import { z } from 'zod';

const productSearch = z.object({
  page: z.number().int().min(1).default(1),
  sort: z.enum(['new', 'top']).default('new'),
  locale: z.enum(['en', 'de']).default('en'), // only used for formatting in the component
});

export const Route = createFileRoute('/products')({
  validateSearch: productSearch,
  loaderDeps: ({ search }) => search,
  loader: ({ deps }) => fetchProducts(deps.page, deps.sort),
  component: Products,
});

function Products() {
  const products = Route.useLoaderData();
  const { locale } = Route.useSearch();
  const price = new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' });
  return <ul>{products.map((p) => <li key={p.id}>{p.name} {price.format(p.price)}</li>)}</ul>;
}

// src/components/Nav.tsx
// <Link to="/products">Products</Link>
//
// tsc:
// src/components/Nav.tsx(6,6): error TS2741: Property 'search' is missing in type '{ to: "/products"; children: string; }'
//   but required in type 'LinkComponentProps<"a", RegisteredRouter, string, "/products", string, "">'.
