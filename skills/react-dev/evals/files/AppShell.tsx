// src/AppShell.tsx: navigation is a zustand store, not a router
import { create } from 'zustand';

type Screen = 'orders' | 'order-detail' | 'settings';

export const useNav = create<{ screen: Screen; params: Record<string, string>; go: (s: Screen, p?: Record<string, string>) => void }>((set) => ({
  screen: 'orders',
  params: {},
  go: (screen, params = {}) => set({ screen, params }),
}));

export function AppShell() {
  const { screen, params } = useNav();
  if (screen === 'order-detail') return <OrderDetail orderId={params.orderId} />;
  if (screen === 'settings') return <Settings />;
  return <Orders />;
}

declare function Orders(): JSX.Element;
declare function Settings(): JSX.Element;
declare function OrderDetail(props: { orderId: string }): JSX.Element;
