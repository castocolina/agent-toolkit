// app/load-context.ts (written for React Router 7, unchanged after the v8 bump)
import 'react-router';
import type { Request as ExpressRequest } from 'express';

declare module 'react-router' {
  interface AppLoadContext {
    userId: string | null;
  }
}

export function getLoadContext(req: ExpressRequest) {
  return { userId: req.session?.userId ?? null };
}
