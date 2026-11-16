// src/components/PostEditor.tsx (React 19, client-side form)
import type { FormEvent } from 'react';

type Intent = 'publish' | 'draft';

export function PostEditor({ onSave }: { onSave: (body: string, intent: Intent) => void }) {
  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const intent = data.get('intent') as Intent; // always null at runtime
    onSave(String(data.get('body')), intent);
  };

  return (
    <form onSubmit={onSubmit}>
      <textarea name="body" />
      <button name="intent" value="draft">Save draft</button>
      <button name="intent" value="publish">Publish</button>
    </form>
  );
}

// Bug: onSave always receives intent === null, so every post is saved as a draft.
