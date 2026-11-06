// packages/ui-kit/src/TextInput.tsx
import type { ComponentPropsWithoutRef } from 'react';

type TextInputProps = {
  label: string;
  error?: string;
} & ComponentPropsWithoutRef<'input'>;

export function TextInput({ label, error, id, ...rest }: TextInputProps) {
  return (
    <label htmlFor={id}>
      {label}
      <input id={id} aria-invalid={!!error} {...rest} />
      {error && <span role="alert">{error}</span>}
    </label>
  );
}
