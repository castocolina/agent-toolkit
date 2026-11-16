// app/users/[id]/ProfileForm.tsx (React 18.3, Next.js 14)
'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { updateProfile } from './actions';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>Save</button>;
}

export function ProfileForm({ userId, name }: { userId: string; name: string }) {
  const [state, formAction] = useFormState(updateProfile.bind(null, userId), { message: '' });
  return (
    <form action={formAction}>
      <input name="name" defaultValue={name} />
      {state.message && <p>{state.message}</p>}
      <SubmitButton />
    </form>
  );
}
