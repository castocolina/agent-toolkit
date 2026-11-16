// app/users/[id]/actions.ts
'use server';

import { db } from '@/lib/db';
import { auth } from '@/lib/auth'; // auth(): Promise<{ user: { id: string; role: 'admin' | 'member' } } | null>

export async function updateProfile(userId: string, prevState: { message: string }, formData: FormData) {
  const name = formData.get('name');
  if (typeof name !== 'string' || name.length < 2) {
    return { message: 'Name must be at least 2 characters' };
  }
  await db.user.update({ where: { id: userId }, data: { name } });
}
