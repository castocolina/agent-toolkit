# Server Components and Server Actions

Worked examples for the server/client rules in SKILL.md. File conventions shown are Next.js App Router 15+; the React parts apply to any RSC framework.

## Page props are Promises (Next.js 15+)

```tsx
// app/users/[id]/page.tsx (Server Component)
export default async function UserPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { id } = await params;
  const { tab } = await searchParams;               // string | string[] | undefined: narrow before use
  const user = await getUserDTO(id);                // data-access layer: authorizes and returns only public fields
  return <UserTabs user={user} tab={typeof tab === 'string' ? tab : 'profile'} />;
}
```

Check the installed version: Next 14 and earlier pass plain objects; 15.0 to 15.4 need the explicit Promise-typed props shown above. Only from 15.5 are the global `PageProps<'/users/[id]'>` and `LayoutProps<'/dashboard'>` helpers generated (by `next dev`, `next build`, or `next typegen` before a standalone `tsc --noEmit`); on earlier minors they and `next typegen` do not exist. Bracket segments are user input: validate `id` before querying.

## A Server Action that authorizes its target

The action is reachable by direct POST with any arguments, so the session check and the ownership check both live inside it.

```ts
// app/users/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';

const profileSchema = z.object({ name: z.string().min(2), bio: z.string().max(500).optional() });

export type ProfileState =
  | { status: 'idle' }
  | { status: 'invalid'; fieldErrors: Partial<Record<'name' | 'bio', string[]>> }
  | { status: 'forbidden' }
  | { status: 'saved' };

// Bound from the client as updateProfile.bind(null, userId): the bound id is client-controlled too.
export async function updateProfile(targetUserId: string, _prev: ProfileState, formData: FormData): Promise<ProfileState> {
  const session = await auth();
  if (!session) return { status: 'forbidden' };
  if (session.user.id !== targetUserId && session.user.role !== 'admin') return { status: 'forbidden' };

  const parsed = profileSchema.safeParse({ name: formData.get('name'), bio: formData.get('bio') ?? undefined });
  // Zod 4: z.flattenError(parsed.error).fieldErrors
  if (!parsed.success) return { status: 'invalid', fieldErrors: parsed.error.flatten().fieldErrors };

  await db.user.update({ where: { id: targetUserId }, data: parsed.data });
  revalidatePath(`/users/${targetUserId}`);
  return { status: 'saved' };                        // return what the UI needs, never the raw record
}
```

When the action only ever edits the caller's own record, drop the id argument and use `session.user.id`; there is nothing left to tamper with. A thrown error (instead of the `forbidden` state) reaches the nearest `error.tsx`, which suits unexpected failures but not a message the form should show.

```tsx
// app/users/[id]/ProfileForm.tsx
'use client';

import { useActionState } from 'react';
import { updateProfile, type ProfileState } from '../actions';

export function ProfileForm({ userId, name }: { userId: string; name: string }) {
  const [state, formAction, isPending] = useActionState<ProfileState, FormData>(
    updateProfile.bind(null, userId),
    { status: 'idle' },
  );
  return (
    <form action={formAction}>
      <input name="name" defaultValue={name} aria-invalid={state.status === 'invalid' && !!state.fieldErrors.name} />
      {state.status === 'invalid' && state.fieldErrors.name?.map((m) => <p key={m}>{m}</p>)}
      {state.status === 'forbidden' && <p role="alert">You cannot edit this profile.</p>}
      <button disabled={isPending}>Save</button>
    </form>
  );
}
```

`'use client'` files can import actions from a `'use server'` module but cannot define inline `'use server'` functions. Inline actions inside a Server Component close over render-time values; Next encrypts those captured values, but the docs say not to rely on that for secrets.

## Crossing the boundary

| Prop from a Server to a Client Component | Allowed |
|---|---|
| Plain objects, arrays, strings, numbers, `Date`, `Map`, `Set`, Promises of those | yes |
| Server Actions (functions from a `'use server'` module) | yes |
| Other functions (including component functions) and class instances | no, serialization error |
| Whole database rows | type-checks, but leaks every column to the browser: map to a DTO first |

`children` passed into a Client Component may be Server Components; a Client Component cannot import a Server Component module. Mark modules with secrets `import 'server-only'` so a client import fails the build.

## Streaming a promise to a client consumer

```tsx
// Server Component; ErrorBoundary is your own boundary or react-error-boundary's
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const commentsPromise = getComments(id);           // not awaited: the page shell streams first
  return (
    <ErrorBoundary fallback={<p>Comments failed to load.</p>}>
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments commentsPromise={commentsPromise} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

`Comments` is a Client Component calling `use(commentsPromise)` (see react-19-patterns.md). Await instead when the data is needed to render the shell; await in parallel with `Promise.all` when calls do not depend on each other.

## Browser-only state in a Client Component

Client Components are pre-rendered on the server, so `'use client'` and `import 'client-only'` do not make `window` safe during render. Use the keyed storage hook in [hooks.md](../references/hooks.md#external-state-and-ssr); it returns a `ready` flag so the component can render a placeholder instead of the fallback value when that distinction matters.
