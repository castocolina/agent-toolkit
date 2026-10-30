# Design System Component Examples

Examples focus on semantic-token contracts, accessible composition, theme validation, and compatibility-preserving evolution. Map the semantic variables to brand values in the theme layer, not in components.

## Semantic tokens and state contract

```css
:root,
[data-theme="light"] {
  --color-action: var(--brand-action-light);
  --color-on-action: var(--brand-on-action-light);
  --color-focus: var(--brand-focus-light);
  --color-surface: var(--brand-surface-light);
  --color-text: var(--brand-text-light);
  --color-danger: var(--brand-danger-light);
}

[data-theme="dark"] {
  --color-action: var(--brand-action-dark);
  --color-on-action: var(--brand-on-action-dark);
  --color-focus: var(--brand-focus-dark);
  --color-surface: var(--brand-surface-dark);
  --color-text: var(--brand-text-dark);
  --color-danger: var(--brand-danger-dark);
}
```

Components consume roles for default, hover, focus, and error states; they never select product palette values directly:

```css
.button {
  color: var(--color-on-action);
  background: var(--color-action);
}
.button:hover { background: color-mix(in srgb, var(--color-action), var(--color-text) 12%); }
.button:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.field[aria-invalid="true"] { border-color: var(--color-danger); }
```

## Accessible field composition

`controlId` is required and must be unique per rendered control. The render prop receives all association and validation props; the control must spread them onto the actual input. Hint/error IDs are stable derivatives of `controlId`, and only the displayed message is referenced.

```tsx
import type { InputHTMLAttributes, ReactNode } from 'react';

type FieldControlProps = Pick<
  InputHTMLAttributes<HTMLInputElement>,
  'id' | 'required' | 'aria-invalid' | 'aria-describedby'
>;

interface FormFieldProps {
  controlId: string;
  label: string;
  required?: boolean;
  hint?: string;
  error?: string;
  children: (props: FieldControlProps) => ReactNode;
}

function FormField({ controlId, label, required = false, hint, error, children }: FormFieldProps) {
  const hintId = `${controlId}-hint`;
  const errorId = `${controlId}-error`;
  const describedBy = error ? errorId : hint ? hintId : undefined;
  return (
    <div>
      <label htmlFor={controlId}>{label}{required ? ' (required)' : ''}</label>
      {children({
        id: controlId,
        required,
        'aria-invalid': error ? true : undefined,
        'aria-describedby': describedBy,
      })}
      {hint && !error && <p id={hintId}>{hint}</p>}
      {error && <p id={errorId} role="alert">{error}</p>}
    </div>
  );
}

<FormField controlId="email" label="Email" required hint="Work address">
  {(props) => <input {...props} type="email" />}
</FormField>
```

The label's `htmlFor` matches the input `id`; required status reaches the input; errors set `aria-invalid` and replace hint association with the error association.

## Theme-state validation

After a theme change, verify computed semantic roles and interaction states rather than checking only the theme attribute. Include light and dark modes, keyboard focus, hover, disabled, and validation error states; confirm contrast against each mapped surface.

```ts
for (const theme of ['light', 'dark']) {
  document.documentElement.dataset.theme = theme;
  const button = getByRole('button', { name: 'Save' });
  expect(getComputedStyle(button).backgroundColor).not.toBe('');
  button.focus();
  expect(getComputedStyle(button).outlineStyle).not.toBe('none');
}
```

## Compatibility-preserving evolution

Add variants as optional props with a default matching existing behavior. Keep established semantic token roles and DOM/accessibility contracts stable; introduce new roles additively and deprecate old ones before removal.

```ts
type ButtonProps = {
  variant?: 'primary' | 'secondary' | 'quiet'; // quiet is additive
};

const variantToken = {
  primary: '--color-action',
  secondary: '--color-surface',
  quiet: '--color-surface',
} as const;
```
