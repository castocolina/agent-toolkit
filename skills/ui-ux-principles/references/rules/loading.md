# loading

## Wait table

Timing from the NN/g skeleton and response-time pages; the layout-shift target from web.dev, Optimize CLS.

| wait | show |
|------|------|
| under about 1 s | Nothing. A placeholder that flashes on a fast load is noise. |
| about 1 to 10 s, a page or several regions | Skeleton with the final block sizes. |
| about 1 to 10 s, one module (a card, a chart) | Spinner inside that module. |
| over about 10 s, uploads, downloads, conversions | Progress with a percent or estimate and a way to cancel. |
| a submit or other write | Button disabled at once; the indicator inside it (Apple HIG Buttons) may wait about 1 s. |

## Decisions

- The wait is unknown when you only have code. Decide by scope, not by guessing latency: a page or several regions gets a skeleton, so a page-level spinner fails whatever the backend speed.
- Content that arrives later reserves its space up front, sized to the final content and adjusted per screen size (web.dev). Removing reserved space shifts the layout as much as inserting content does.
- A skeleton never replaces performance work (NN/g).

## Gotchas

- MUI `Skeleton` has no ARIA attributes and is not focusable: announce the wait yourself with `aria-busy` on the region or a `role="status"` text.
- Wrapping the real component in MUI `Skeleton` infers its size, which keeps CLS near 0; a free-standing `Skeleton` needs explicit width and height.
- A skeleton still on screen after the request failed is a broken handoff: swap to the error state.
- Turn the pulse off under `prefers-reduced-motion` (NN/g says skeleton animation can cause accessibility problems; the pairing itself is UNVERIFIED).
- Check the skeleton color against the dark surface, not only the light one.

## Fix pattern

```tsx
if (status === 'loading') {
  return (
    <ul aria-busy="true">
      {[0, 1, 2].map((i) => <li key={i}><Skeleton variant="rounded" height={48} /></li>)}
    </ul>
  );
}
```

```tsx
<button type="submit" disabled={saving} aria-busy={saving}>
  {saving ? <><Spinner aria-hidden /> Saving</> : 'Save'}
</button>
```
