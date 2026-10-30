import * as React from 'react';

export interface ComponentProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

function ComponentBase(
  { variant = 'primary', size = 'md', className, type = 'button', ...props }: ComponentProps,
  ref: React.ForwardedRef<HTMLButtonElement>,
) {
  return (
    <button
      {...props}
      ref={ref}
      type={type}
      className={[
        'component',
        `component--${variant}`,
        `component--${size}`,
        className,
      ].filter(Boolean).join(' ')}
    />
  );
}

const ForwardedComponent = React.forwardRef(ComponentBase);
ForwardedComponent.displayName = 'Component';

function Header({ children }: { children: React.ReactNode }) {
  return <div className="component__header">{children}</div>;
}

function Body({ children }: { children: React.ReactNode }) {
  return <div className="component__body">{children}</div>;
}

export const Component = Object.assign(ForwardedComponent, { Header, Body });
export default Component;
