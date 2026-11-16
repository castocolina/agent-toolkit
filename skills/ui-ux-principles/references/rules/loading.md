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
export type Order = { id: string; customer: string; total: string };

export function OrderRow({ order, onDelete }: { order?: Order; onDelete?: (id: string) => void }) {
  // no order: a placeholder row; `.skeleton` takes its color from a theme role and
  // pulses only inside @media (prefers-reduced-motion: no-preference)
  return (
    <li className={order ? 'order-row' : 'order-row skeleton'} aria-hidden={order ? undefined : true}>
      <span className="order-customer">{order?.customer}</span>
      <span className="order-total">{order?.total}</span>
      {/* the delete control's box is reserved in both states; only a loaded row fills it */}
      <span className="order-actions">
        {order && onDelete && (
          <button type="button" aria-label={`Delete order for ${order.customer}`} onClick={() => onDelete(order.id)}>Delete</button>
        )}
      </span>
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

The geometry match comes from the CSS, because empty spans collapse to zero size. The row, both text boxes and the delete control's box get fixed dimensions in both states, and the skeleton only paints the same boxes:

```css
.order-row { display: flex; justify-content: space-between; align-items: center; gap: 1rem; min-height: 3rem; padding: 0.75rem 1rem; }
.order-customer, .order-total { display: block; height: 1.5rem; line-height: 1.5rem; }   /* same display and height empty or filled */
.order-customer { width: 14rem; max-width: 60%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.order-total { width: 6rem; text-align: right; }
.order-actions { flex: none; width: 5rem; height: 1.5rem; }   /* reserved whether or not the delete button is there */
.order-actions button { width: 100%; height: 100%; }
.skeleton .order-customer, .skeleton .order-total { background: var(--skeleton-bg); border-radius: 0.25rem; }   /* a theme role, checked on the dark surface too */
@media (prefers-reduced-motion: no-preference) {
  .skeleton .order-customer, .skeleton .order-total { animation: skeleton-pulse 1.5s ease-in-out infinite; }
}
@keyframes skeleton-pulse { 50% { opacity: 0.5; } }
```

The widths and heights above are placeholders for the product's own sizes: take them from the real text, then the placeholder block matches the loaded row and the page does not shift when data lands.

The pending submit:

```tsx
<button type="submit" disabled={saving} aria-busy={saving}>
  {saving ? <><Spinner aria-hidden /> Saving</> : 'Save'}
</button>
```
