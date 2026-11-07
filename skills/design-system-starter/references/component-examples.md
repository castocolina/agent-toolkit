# Design System Component Examples

Examples focus on semantic-token contracts, accessible composition, theme validation, and compatibility-preserving evolution. Map the semantic variables to brand values in the theme layer, not in components.

## Semantic tokens and state contract

```css
:root,
[data-theme="light"] {
  --color-action: var(--brand-action-light);
  --color-action-hover: var(--brand-action-hover-light);
  --color-on-action: var(--brand-on-action-light);
  --color-focus: var(--brand-focus-light);
  --color-surface: var(--brand-surface-light);
  --color-text: var(--brand-text-light);
  --color-border: var(--brand-border-light); /* UI boundary: at least 3:1 against --color-surface */
  --color-danger: var(--brand-danger-light);
}

[data-theme="dark"] {
  --color-action: var(--brand-action-dark);
  --color-action-hover: var(--brand-action-hover-dark);
  --color-on-action: var(--brand-on-action-dark);
  --color-focus: var(--brand-focus-dark);
  --color-surface: var(--brand-surface-dark);
  --color-text: var(--brand-text-dark);
  --color-border: var(--brand-border-dark); /* UI boundary: at least 3:1 against the dark --color-surface */
  --color-danger: var(--brand-danger-dark);
}
```

Variable naming: a token's DTCG path becomes its CSS variable by joining the path segments with `-` after the group prefix and dropping the structural segments `semantic` and `scale`, plus a trailing `default` or `ring`. So `color.semantic.border.default` is `--color-border` (the border token in `references/token-scales.md`, gray-500 in the starter template, 4.8345:1 on white), `color.semantic.focus.ring` is `--color-focus`, `spacing.scale.6` is `--spacing-6`, `radius.lg` is `--radius-lg` and `shadow.lg` is `--shadow-lg`. The scale variables (`--spacing-*`, `--radius-*`, `--shadow-*`) come from those scales as they are and need no per-theme block; only color roles change per theme.

Components consume roles for default, hover, focus, and error states; they never select product palette values directly. Every state gets its own role (no `color-mix()` or opacity derivation in components), so each state pair can be contrast-checked at token level:

```css
.ds-button[data-intent="primary"] {
  color: var(--color-on-action);
  background: var(--color-action);
}
.ds-button[data-intent="primary"]:hover { background: var(--color-action-hover); }
.ds-button:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.field[aria-invalid="true"] { border-color: var(--color-danger); }
```

## Accessible field composition

```tsx
import type { InputHTMLAttributes, ReactNode } from 'react';

type FieldControlProps = Pick<InputHTMLAttributes<HTMLInputElement>, 'id' | 'required' | 'aria-invalid' | 'aria-describedby'>;

interface FormFieldProps {
  controlId: string; // required and unique per rendered control; hint and error ids derive from it
  label: string;
  required?: boolean;
  hint?: string;
  error?: string; // when shown, replaces the hint in aria-describedby and sets aria-invalid
  children: (props: FieldControlProps) => ReactNode; // the control spreads these onto the real input
}

function FormField({ controlId, label, required = false, hint, error, children }: FormFieldProps) {
  const message = error || hint;
  const messageId = message ? `${controlId}-${error ? 'error' : 'hint'}` : undefined;
  return (
    <div>
      <label htmlFor={controlId}>{label}{required ? ' (required)' : ''}</label>
      {children({ id: controlId, required, 'aria-invalid': error ? true : undefined, 'aria-describedby': messageId })}
      {message && <p id={messageId} role={error ? 'alert' : undefined}>{message}</p>}
    </div>
  );
}

<FormField controlId="email" label="Email" required hint="Work address">
  {(props) => <input {...props} type="email" />}
</FormField>
```

## Theme-state validation

Run this in a real browser: jsdom does not compute rendered colors, so jest-axe turns color contrast off ([jest-axe README](https://github.com/NickColley/jest-axe): "Color contrast checks do not work in JSDOM so are turned off in jest-axe", checked 2026-11-07) and computed-style assertions there prove nothing. axe's `color-contrast` rule checks text only; check non-text pairs (borders, focus ring) from the resolved token values.

```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

for (const theme of ['light', 'dark']) {
  test(`pilot screen contrast, ${theme}`, async ({ page }) => {
    await page.goto('/pilot');
    await page.evaluate((t) => { document.documentElement.dataset.theme = t; }, theme);
    await page.getByRole('button', { name: 'Save' }).focus(); // repeat with hover() and error states
    const { violations } = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
    expect(violations).toEqual([]);
  });
}
```

## Deprecation alias

A renamed token keeps its old path as an alias with `$deprecated` (DTCG 2025.10) through the next major release; a renamed prop maps to the new one with the same default. Both are removed in the major after that.

```json
{
  "color": {
    "action": {
      "default": { "$type": "color", "$value": "{color.primitive.blue.600}" },
      "primary": { "$type": "color", "$value": "{color.action.default}", "$deprecated": "Use color.action.default; removed in 3.0.0" }
    }
  }
}
```

```ts
type Intent = 'primary' | 'secondary' | 'danger';
interface ButtonProps {
  intent?: Intent;
  /** @deprecated Use `intent`; removed in 3.0.0. */
  variant?: Intent;
}
const resolveIntent = ({ intent, variant }: ButtonProps): Intent => intent ?? variant ?? 'primary';
```

## Props conventions

Across components, use the same prop name for the same idea (`intent`, `size`, `disabled`, never `type="primary"` on one and `style="outlined"` on another). Give every optional prop a default so the bare component works, and document the default. Prefer composition (slots, compound parts) to a long list of content props such as `title`, `content`, `hasFooter`:

```tsx
// Predictable and defaulted
<Button intent="primary" size="md" />
<Input size="md" />

// Composable, instead of <Card title="..." content="..." footerContent="..." hasFooter />
<Card variant="elevated">
  <Card.Header><Card.Title level={2}>Title</Card.Title></Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Actions</Card.Footer>
</Card>
```

## Compound Card

No root `className`; variants are `data-variant` values mapped to role tokens in CSS, so a consumer class cannot override a color role. The heading level depends on the page, so `Card.Title` takes `level`. Header and Body sit on non-interactive containers; for a clickable card put one `<a>` in the title and stretch it over the card with CSS (SKILL.md nesting gotcha).

```tsx
import type { ReactNode } from 'react';

interface CardProps { variant?: 'default' | 'outlined' | 'elevated'; children: ReactNode }

export function Card({ variant = 'default', children }: CardProps) {
  return <div className="ds-card" data-variant={variant}>{children}</div>;
}
Card.Header = ({ children }: { children: ReactNode }) => <div className="ds-card__header">{children}</div>;
Card.Title = ({ level = 3, children }: { level?: 2 | 3 | 4; children: ReactNode }) => {
  const Heading = `h${level}` as const;
  return <Heading className="ds-card__title">{children}</Heading>;
};
Card.Body = ({ children }: { children: ReactNode }) => <div className="ds-card__body">{children}</div>;
Card.Footer = ({ children }: { children: ReactNode }) => <div className="ds-card__footer">{children}</div>;
```

```css
.ds-card { background: var(--color-surface); color: var(--color-text); border-radius: var(--radius-lg); padding: var(--spacing-6); }
.ds-card[data-variant="outlined"] { border: 1px solid var(--color-border); } /* a border role that passes 3:1, never gray-200 */
.ds-card[data-variant="elevated"] { box-shadow: var(--shadow-lg); }
.ds-card__header { margin-block-end: var(--spacing-4); }
.ds-card__footer { margin-block-start: var(--spacing-4); }
```

## Polymorphic component

An `as` prop lets one component render as a `<button>` (an action) or an `<a href>` (navigation); pick the element by behavior, and an `as="a"` without `href` is not a link. In React 19 `ref` is a plain prop, so no `forwardRef` or ref plumbing is needed (https://react.dev/blog/2024/12/05/react-19, checked 2026-11-07); on React 18 wrap in `forwardRef`.

```tsx
import type { ComponentPropsWithRef, ElementType } from 'react';

type Own<C extends ElementType> = { as?: C; intent?: 'primary' | 'secondary' };
export type PolymorphicButtonProps<C extends ElementType = 'button'> =
  Own<C> & Omit<ComponentPropsWithRef<C>, keyof Own<C> | 'className' | 'style'>;

export function PolymorphicButton<C extends ElementType = 'button'>({ as, intent = 'primary', ...rest }: PolymorphicButtonProps<C>) {
  const Component: ElementType = as ?? 'button';
  const nativeType = Component === 'button' ? { type: 'button' } : null; // a consumer-supplied type still wins via rest
  return <Component {...nativeType} {...rest} className="ds-button" data-intent={intent} />;
}

// <PolymorphicButton onClick={save}>Save</PolymorphicButton>
// <PolymorphicButton as="a" href="/login">Log in</PolymorphicButton>
```

## Modal on native dialog

Native `<dialog>` with `showModal()` focuses the first focusable element (or the one with `autofocus`), makes the rest of the page inert, closes on Escape and uses the top layer (https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog, checked 2026-11-07), so none of that is hand-written. The dialog is labelled by its heading and focus goes back to the opener on close.

```tsx
import { useEffect, useId, useRef, type ReactNode } from 'react';

interface ModalProps { open: boolean; onClose: () => void; title: string; size?: 'sm' | 'md' | 'lg'; children: ReactNode }

export function Modal({ open, onClose, title, size = 'md', children }: ModalProps) {
  const ref = useRef<HTMLDialogElement>(null);
  const opener = useRef<Element | null>(null);
  const titleId = useId();
  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) { opener.current = document.activeElement; dialog.showModal(); }
    if (!open && dialog.open) dialog.close();
  }, [open]);
  const handleClose = () => { // fires for Escape, the close button and dialog.close()
    (opener.current as HTMLElement | null)?.focus();
    onClose();
  };
  return (
    <dialog ref={ref} className="ds-modal" data-size={size} aria-labelledby={titleId} onClose={handleClose}>
      <h2 id={titleId}>{title}</h2>
      {children}
      <button type="button" onClick={() => ref.current?.close()}>Close</button>
    </dialog>
  );
}
```

```css
.ds-modal { background: var(--color-surface); color: var(--color-text); border-radius: var(--radius-lg); padding: var(--spacing-6); box-shadow: var(--shadow-xl); max-inline-size: min(100%, 32rem); }
.ds-modal[data-size="sm"] { max-inline-size: min(100%, 24rem); }
.ds-modal[data-size="lg"] { max-inline-size: min(100%, 48rem); }
.ds-modal::backdrop { background: rgb(0 0 0 / 0.5); }
```

Do not add `aria-modal`: `showModal()` already marks the dialog modal. Widths are examples; set them per product.

## Skip link and visually hidden text

A skip link is the first focusable element and lets keyboard users bypass repeated navigation (WCAG 2.2 SC 2.4.1 Bypass Blocks, Level A, https://www.w3.org/TR/WCAG22/, checked 2026-11-07). The target needs `tabindex="-1"` so focus lands on it.

```html
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <!-- header and navigation -->
  <main id="main-content" tabindex="-1">...</main>
</body>
```

```css
.visually-hidden,
.skip-link:not(:focus) {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0;
}
.skip-link:focus {
  position: fixed; inset-block-start: var(--spacing-4); inset-inline-start: var(--spacing-4);
  padding: var(--spacing-2) var(--spacing-4); background: var(--color-action); color: var(--color-on-action);
  border-radius: var(--radius-md); outline: 2px solid var(--color-focus); outline-offset: 2px;
}
```

`.visually-hidden` is also the pattern for text alternatives such as an avatar status.

## Theme toggle

The head script from the SKILL.md gotcha sets `data-theme` before first paint; the toggle reads that value instead of deciding a theme after mount, so there is no flash and the toggle starts in the real state.

```html
<script>
  try {
    var saved = localStorage.getItem('theme');
    document.documentElement.dataset.theme = saved === 'light' || saved === 'dark' ? saved
      : matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  } catch (e) {}
</script>
```

```tsx
import { useState } from 'react';

type Theme = 'light' | 'dark';
const readTheme = (): Theme => (document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light');

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(readTheme); // client-rendered app; with SSR, read it in an effect instead
  const toggle = () => {
    const next: Theme = theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch { /* storage blocked: the choice lasts for this page only */ }
    setTheme(next);
  };
  return (
    <button type="button" className="ds-theme-toggle" aria-pressed={theme === 'dark'} onClick={toggle}>
      Dark mode
    </button>
  );
}
```

A toggle keeps one stable label and reports its state with `aria-pressed`; do not swap the label and also set `aria-pressed`.

## Responsive navigation

A `<nav>` landmark with a labelled list of links, `aria-current="page"` on the current one, and a menu button on small screens that reports `aria-expanded` and names the list it controls through `aria-controls`.

```tsx
import { useId, useRef, useState } from 'react';

interface NavLink { href: string; label: string }

export function Navigation({ links, current }: { links: NavLink[]; current: string }) {
  const [open, setOpen] = useState(false);
  const menuId = useId();
  const toggleRef = useRef<HTMLButtonElement>(null);
  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape' && open) { setOpen(false); toggleRef.current?.focus(); }
  };
  return (
    <nav aria-label="Main" className="ds-nav" onKeyDown={onKeyDown}>
      <a href="/" className="ds-nav__brand">Logo</a>
      <button ref={toggleRef} type="button" className="ds-nav__toggle" aria-expanded={open} aria-controls={menuId} onClick={() => setOpen(!open)}>
        Menu
      </button>
      <ul id={menuId} className="ds-nav__list" data-open={open || undefined}>
        {links.map((link) => (
          <li key={link.href}>
            <a href={link.href} aria-current={link.href === current ? 'page' : undefined}>{link.label}</a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

```css
.ds-nav__list { display: none; }
.ds-nav__list[data-open] { display: block; }
@media (min-width: 48rem) { /* the breakpoint is a project decision */
  .ds-nav__toggle { display: none; }
  .ds-nav__list { display: flex; gap: var(--spacing-6); }
}
```
