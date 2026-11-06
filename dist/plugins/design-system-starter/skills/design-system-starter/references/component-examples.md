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
  --color-danger: var(--brand-danger-light);
}

[data-theme="dark"] {
  --color-action: var(--brand-action-dark);
  --color-action-hover: var(--brand-action-hover-dark);
  --color-on-action: var(--brand-on-action-dark);
  --color-focus: var(--brand-focus-dark);
  --color-surface: var(--brand-surface-dark);
  --color-text: var(--brand-text-dark);
  --color-danger: var(--brand-danger-dark);
}
```

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

Run this in a real browser: jsdom does not compute rendered colors, so jest-axe turns color contrast off and computed-style assertions there prove nothing. axe's `color-contrast` rule checks text only; check non-text pairs (borders, focus ring) from the resolved token values.

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
