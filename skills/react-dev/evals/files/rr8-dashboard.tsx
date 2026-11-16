// app/routes/dashboard.tsx
import { redirect, useLoaderData } from 'react-router';

export async function loader({ context }: { context: { userId: string | null } }) {
  if (!context.userId) throw redirect('/login');
  return { widgets: await getWidgets(context.userId) };
}

export default function Dashboard() {
  const { widgets } = useLoaderData<typeof loader>();
  return <ul>{widgets.map((w) => <li key={w.id}>{w.title}</li>)}</ul>;
}

// tsc after the bump:
// app/routes/dashboard.tsx(4,33): error TS2322: Type 'RouterContextProvider' is not assignable to type '{ userId: string | null; }'.
