# loading

The wait thresholds, the submit rule and the decide-by-scope rule live in `SKILL.md` `## loading`. Timing from the NN/g skeleton and response-time pages; the in-button indicator from Apple HIG Buttons; the layout-shift target from web.dev, Optimize CLS.

## Decisions

- Why nothing under about 1 s: a placeholder that flashes on a fast load is noise. Past about 10 s the progress is a percent or estimate, not an indeterminate bar.
- Content that arrives later reserves its space up front, sized to the final content and adjusted per screen size (web.dev). Removing reserved space shifts the layout as much as inserting content does.
- A skeleton never replaces performance work (NN/g).

## Gotchas

- Wrapping the real component in MUI `Skeleton` infers its size, which keeps CLS near 0; a free-standing `Skeleton` needs explicit width and height.
- A skeleton still on screen after the request failed is a broken handoff: swap to the error state.
- Turn the pulse off under `prefers-reduced-motion` (NN/g says skeleton animation can cause accessibility problems; Tailwind's `motion-safe:` and `motion-reduce:` apply to any animation utility, https://tailwindcss.com/docs/animation, checked 2026-11-15).
- Check the skeleton color against the dark surface, not only the light one.

## Fix pattern

A list that shows a skeleton while loading, an empty state and the content (a failed request leaves `loading` false and renders the error state in `states.md`). One row component serves both states, so the skeleton has the real row's geometry:

```tsx
type Order = { id: string; customer: string; total: string };

function OrderRow({ order }: { order?: Order }) {
  // no order: a placeholder row; `.skeleton` takes its color from a theme role and
  // pulses only inside @media (prefers-reduced-motion: no-preference)
  return (
    <li className={order ? 'order-row' : 'order-row skeleton'} aria-hidden={order ? undefined : true}>
      <span className="order-customer">{order?.customer}</span>
      <span className="order-total">{order?.total}</span>
    </li>
  );
}

function OrderList({ loading, orders }: { loading: boolean; orders: Order[] }) {
  if (loading) {
    return (
      <ul aria-label="Orders" aria-busy="true">
        {Array.from({ length: 5 }, (_, i) => <OrderRow key={i} />)}
      </ul>
    );
  }
  if (orders.length === 0) {
    return <p>No orders yet. <a href="/orders/new">Create an order</a></p>;
  }
  return <ul aria-label="Orders">{orders.map((o) => <OrderRow key={o.id} order={o} />)}</ul>;
}
```

The pending submit:

```tsx
<button type="submit" disabled={saving} aria-busy={saving}>
  {saving ? <><Spinner aria-hidden /> Saving</> : 'Save'}
</button>
```
