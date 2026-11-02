# responsive

## Decisions

- Component that sits in slots of different widths (a card in a sidebar and in a grid): container query (`container-type: inline-size` plus `@container (inline-size > 30em)`), not a viewport media query (web.dev, MDN). A media query answers to the viewport, which says nothing about the slot.
- Fluid type: `clamp()` with `rem` bounds and a maximum at least twice the minimum, so text still reaches 200% on zoom (MDN, SC 1.4.4). Text sized in `vw` alone does not grow with zoom.
- 320 CSS px is the WCAG reflow fail line (SC 1.4.10: no two-dimensional scrolling); 360 px is only the narrowest test width.
- The viewport meta `width=device-width` is required, or phones render the desktop width zoomed out (web.dev).
- Tailwind: unprefixed utilities are the base; `sm:` to `2xl:` are min-width (40, 48, 64, 80, 96 rem), so `sm:` is not "small screens".

## Gotchas

- An inner scroll for a table, map or code block passes only when the page itself does not scroll sideways at the same width.
- A sticky header that covers the focused control at a narrow width fails SC 2.4.11; add `scroll-margin` or `scroll-padding`.
- Grow touch padding under `@media (any-pointer: coarse)` instead of enlarging the icon (web.dev).
- Disabling zoom (`user-scalable=no`, `maximum-scale=1`) blocks the 200% resize (UNVERIFIED: inferred from SC 1.4.4, not stated in the pages read).

## Fix pattern

```tsx
<Grid container spacing={2}>
  <Grid size={{ xs: 12, md: 3 }}><Filters /></Grid>
  <Grid size={{ xs: 12, md: 9 }}><OrdersList /></Grid>
</Grid>
```

```css
.card-slot { container-type: inline-size; }
@container (inline-size > 30em) { .card { grid-template-columns: 8rem 1fr; } }
```
