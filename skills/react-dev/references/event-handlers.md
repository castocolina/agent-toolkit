# Event Handlers

Value extraction and React-vs-DOM event behavior. Snippets type-check with `@types/react` 19 and TypeScript 5.6 `lib.dom`.

## Checklist

- Read from `e.currentTarget`: `valueAsNumber` (is `NaN` when empty or partial, so check `Number.isNaN`), `checked` (not `value`, which is the static `"on"`), `files?.[0]` (`FileList | null`), `Array.from(selectedOptions, (o) => o.value)` for `<select multiple>`.
- `FormData.get` returns `string | File | null`: narrow with `typeof v === 'string'`.
- Handler props: `ChangeEventHandler<HTMLInputElement>` or `ComponentProps<'input'>['onBlur']`.
- In files that also add native listeners, import React's events under aliases (`type KeyboardEvent as ReactKeyboardEvent`); they shadow the DOM globals with the same names.

## Which button submitted

With several submit buttons, the clicked one is on the native event, which React types as a plain `Event`:

```tsx
const onSubmit = (e: FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const submitter = (e.nativeEvent as SubmitEvent).submitter; // HTMLElement | null
  const data = new FormData(e.currentTarget, submitter);      // includes the clicked button's name=value
  return data.get('intent');                                   // the clicked button's value
};
```

## Where React differs from the DOM

| Behavior | Consequence |
|---|---|
| `onChange` fires on every keystroke (the DOM `input` event), not on blur | do not expect DOM `change` timing; use `onBlur` for commit-on-leave |
| Since React 17, listeners attach to the root container, not `document` | `e.stopPropagation()` in a React handler now also stops native listeners on `document` |
| `onScroll` does not bubble since React 17 | attach it to the element that scrolls |
| `wheel`, `touchstart` and `touchmove` are registered as passive | `e.preventDefault()` in `onWheel` is ignored: add a native listener with `{ passive: false }` in an Effect |
| `onFocus` / `onBlur` bubble (they map to `focusin` / `focusout`) | a container's `onBlur` fires when focus moves between its children; check `e.currentTarget.contains(e.relatedTarget)` |

Source for the "Since React 17" rows (root-container listeners, `onScroll` bubbling, passive `onWheel`/`onTouchStart`/`onTouchMove`): React v17 release post, https://legacy.reactjs.org/blog/2020/10/20/react-v17.html, checked 2026-11-08.

## Enter to submit and IME composition

An `<input>` inside a form already submits on Enter natively, and browsers generally do not submit on the Enter that confirms an IME composition. Do not add a `keydown` handler for that case: a handler calling `requestSubmit()` on top of the native submission submits twice.

Add one only for custom Enter behavior, such as Enter-to-send in a `<textarea>` (which has no native submission). Return early for every other key and during composition, and call `preventDefault()` only for the Enter you handle:

```tsx
const onKeyDown = (e: ReactKeyboardEvent<HTMLTextAreaElement>) => {
  const composing = e.nativeEvent.isComposing || e.nativeEvent.keyCode === 229;  // Safari can report isComposing=false on the IME-confirm Enter
  if (e.key !== 'Enter' || e.shiftKey || composing) return;                      // Shift+Enter: newline; composing: IME confirm
  e.preventDefault();                                                       // no newline for the handled Enter
  e.currentTarget.form?.requestSubmit();                                    // runs validation and onSubmit once
};
```

## Custom DOM events

Augmenting `WindowEventMap` types listeners only. `dispatchEvent` accepts any `Event`, so `new CustomEvent('cart:updated', { detail: { count: 'three' } })` still compiles. Route every producer through one typed helper:

```ts
declare global {
  interface WindowEventMap { 'cart:updated': CustomEvent<{ count: number }> }
}

export function dispatchCartUpdated(detail: WindowEventMap['cart:updated']['detail']) {
  window.dispatchEvent(new CustomEvent('cart:updated', { detail }));
}

window.addEventListener('cart:updated', (e) => console.log(e.detail.count)); // e: CustomEvent<{ count: number }>

// cart.type-test.ts (compile-only, never called)
export function cartContract() {
  // @ts-expect-error count must be a number
  dispatchCartUpdated({ count: 'three' });
}
```

For an element, augment `HTMLElementEventMap` instead. React's JSX props do not know custom events; subscribe in an Effect with a ref.
