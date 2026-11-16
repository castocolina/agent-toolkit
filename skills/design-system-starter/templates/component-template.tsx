import type { ComponentPropsWithRef, MouseEvent } from 'react';

// Contract: semantic props only (no palette names); each intent/state maps to its own token role in CSS
// (`.ds-button[data-intent="primary"]:hover` -> var(--color-action-hover)). No root className or style:
// layout classes go on an outer wrapper. React 19 passes `ref` as a prop; on React 18 wrap in forwardRef.
export interface ButtonProps extends Omit<ComponentPropsWithRef<'button'>, 'className' | 'style'> {
  intent?: 'primary' | 'secondary' | 'danger'; // default keeps existing behavior when variants are added
  size?: 'sm' | 'md';
  loading?: boolean;
}

export function Button({ intent = 'primary', size = 'md', loading = false, type = 'button', onClick, ...rest }: ButtonProps) {
  // loading and aria-disabled block activation but stay focusable, so keyboard focus is not dropped mid-action
  const blocked = loading || rest['aria-disabled'] === true || rest['aria-disabled'] === 'true';
  const handleClick = (e: MouseEvent<HTMLButtonElement>) => (blocked ? e.preventDefault() : onClick?.(e));
  return (
    <button
      {...rest}
      type={type}
      className="ds-button"
      data-intent={intent}
      data-size={size}
      aria-disabled={blocked || undefined}
      aria-busy={loading || undefined}
      onClick={handleClick}
    />
  );
}
