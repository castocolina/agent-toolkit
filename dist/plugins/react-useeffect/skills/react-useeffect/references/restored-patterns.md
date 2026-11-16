# Measuring, sharing and initializing

Three decisions that the routing table in SKILL.md only names. Each section says which React versions it applies to. Facts checked 2026-11-15 against react.dev, written by the React team: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) (YMNNAE) and the [useMemo reference](https://react.dev/reference/react/useMemo).

## Memoizing a calculation: measure first

Applies to React 18 and 19.

1. Wrap the calculation in `console.time('filter')` and `console.timeEnd('filter')`.
2. Interact with the page so the calculation runs, and read the logged time. If it adds up to about 1ms or more per interaction, it might make sense to memoize it with `useMemo`. react.dev gives 1ms as its example, not a hard limit.
3. Test on a throttled CPU (the browser devtools CPU throttle) in a production build: development builds and a fast machine hide the cost.
4. `useMemo` does not make the first render faster. It only skips the calculation on re-renders whose dependencies did not change.
5. In Strict Mode development, React calls the calculation twice; that is development-only, so do not read the doubled time as the real cost.

Below the threshold, compute in render without `useMemo` (a string concatenation or a short filter is never worth it).

React Compiler: it can memoize automatically, so manual `useMemo` is needed less in many components. It reached stable 1.0 on 2025-10-07 (checked 2026-11-15, [release post](https://react.dev/blog/2025/10/07/react-compiler-1)); read [React Compiler](https://react.dev/learn/react-compiler) for the current status and supported React versions before writing one into advice. Manual `useMemo` remains an escape hatch, for example for a value used as an Effect dependency. In existing code leave memoization in place, or test before removing it.

## Two handlers share logic: extract a function

Applies to React 18 and 19 (react.dev, YMNNAE, "Sharing logic between event handlers").

When a Buy button and a Checkout button both need the same notification, do not watch `product.isInCart` in an Effect and show the toast there. Delete the Effect and put the shared logic in one function that both handlers call:

```tsx
function buyProduct() {
  addToCart(product);
  showNotification(`Added ${product.name} to the shopping cart!`);
}

function handleBuyClick() {
  buyProduct();
}

function handleCheckoutClick() {
  buyProduct();
  navigateTo('/checkout');
}
```

The Effect version also fires on reload whenever `product.isInCart` is already true, so the toast appears with no click. Only logic that runs because a component was displayed belongs in an Effect.

## Initialization that must run once, browser only

Applies to React 18 and 19, and to any server-rendered setup (react.dev, YMNNAE, "Initializing the application"; [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects) shows the same check).

Top-level module code runs once, when the module is imported, even if the component that needs it never renders. In a server-rendered app it also runs on the server (and during a build-time prerender), where `window`, `localStorage` and the DOM do not exist. Guard browser-only work at module level with a browser check:

```ts
if (typeof window !== 'undefined') { // Check if we're running in the browser.
  ensureAppInit().catch(reportInitError); // cached promise from anti-patterns.md, "Initialization that must run once"
}
```

Rules that stay in force:

- Keep this in the app entry or root module (`App` or the entry file), never in a leaf component's file: it runs on import.
- Do not mark the work done before it succeeds. react.dev shows a plain `didInit` flag, and this skill allows that only for synchronous work that cannot fail. For fallible or async work use the cached promise cleared on failure, as in [anti-patterns](anti-patterns.md#initialization-that-must-run-once).
- Without the `typeof window` guard in a server-rendered app, the initialization throws on the server or runs once per server process instead of once per page load.
- An Effect on `App` is the alternative that never runs on the server (Effects run only in the browser). Keep the cached promise there too, so the Strict Mode replay does not start the work twice.
