# interaction

## State table

| state | requirement | source |
|-------|-------------|--------|
| hover | Pointer devices only; carries no essential information | Tailwind wraps `hover:` in `@media (hover: hover)` |
| focus-visible | Visible on keyboard focus, at least 3:1 against adjacent colors; restyle it, never delete it | MDN `:focus-visible`, web.dev Focus, SC 1.4.11, 2.4.7 |
| active | Every custom button has a press state, or it "can feel unresponsive" | Apple HIG Buttons |
| disabled | Looks inert and is inert | practice, no fetched source |

## Decisions

- `:focus-visible`, not `:focus`: the browser shows it for keyboard focus and not for a mouse click (MDN), so the ring no longer bothers mouse users. Keep `:focus:not(:focus-visible)` only when a visible replacement exists.
- Inert means the native `disabled` attribute, or `aria-disabled="true"` plus a handler that blocks the action when the control must stay focusable for discoverability.
- Focus Appearance (SC 2.4.13: a 2 CSS px perimeter, 3:1 between focused and unfocused) is AAA in WCAG 2.2: a good target, not an AA fail line.
- Links, inputs, selects, menu items and tabs need the same states as buttons.

## Gotchas

- A Tailwind `hover:` reveal (an action that appears on row hover) never shows on touch, because `hover:` only applies under `@media (hover: hover)`. Make the action visible or reachable by focus.
- MUI `Button` and `IconButton` bring their own focus-visible and pressed states; a custom `sx` that sets `outline: none` or overrides `'&:focus-visible'` removes them.
- Avoid positive `tabindex` (web.dev Focus): fix the DOM order so tab order follows the visual order.

## Fix pattern

```css
@media (hover: hover) { .btn:hover { background: var(--color-primary-hover); } }
.btn:active { background: var(--color-primary-active); }
.btn:focus-visible { outline: 3px solid var(--color-focus); outline-offset: 2px; }
.btn:disabled { cursor: not-allowed; }
```
