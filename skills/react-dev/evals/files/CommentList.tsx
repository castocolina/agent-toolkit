// app/components/CommentList.tsx (React 19)
'use client';

import { useOptimistic, useState } from 'react';

type Comment = { id: string; text: string };

export function CommentList({ initial }: { initial: Comment[] }) {
  const [comments, setComments] = useState(initial);
  const [optimistic, addOptimistic] = useOptimistic(comments, (state, c: Comment) => [...state, c]);

  async function handleClick(text: string) {
    addOptimistic({ id: 'temp', text });
    setComments((prev) => [...prev, { id: 'temp', text }]);
    await fetch('/api/comments', { method: 'POST', body: JSON.stringify({ text }) });
  }

  return (
    <>
      <ul>{optimistic.map((c) => <li key={c.id}>{c.text}</li>)}</ul>
      <button onClick={() => handleClick('+1')}>+1</button>
    </>
  );
}

// Reports: React warns "An optimistic state update occurred outside a transition or action",
// a 500 from the API still leaves the comment on screen, and two quick clicks log a duplicate-key warning.
