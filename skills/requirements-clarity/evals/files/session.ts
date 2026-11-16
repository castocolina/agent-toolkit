// src/auth/session.ts
import { redirect } from "./router";

export const SESSION_TTL_MINUTES = 30;

export async function apiFetch(input: RequestInfo, init?: RequestInit): Promise<Response> {
  const res = await fetch(input, { ...init, credentials: "include" });
  if (res.status === 401) {
    // Session expired: drop the user on the login page. Unsaved form state is lost.
    redirect("/login");
  }
  return res;
}
