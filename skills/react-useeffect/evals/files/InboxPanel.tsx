import { useEffect, useState } from 'react';

type Message = { id: string; from: string; body: string; archived: boolean };

export function InboxPanel({ threadId, messages }: { threadId: string; messages: Message[] }) {
  const [showArchived, setShowArchived] = useState(false); // user preference, kept across threads
  const [selected, setSelected] = useState<Message | null>(null);

  useEffect(() => {
    setSelected(null);
  }, [threadId]);

  const visible = messages.filter((m) => showArchived || !m.archived);

  return (
    <section aria-label={`Thread ${threadId}`}>
      <label>
        <input type="checkbox" checked={showArchived} onChange={(e) => setShowArchived(e.target.checked)} />
        Show archived
      </label>
      <ul>
        {visible.map((m) => (
          <li key={m.id}>
            <button onClick={() => setSelected(m)}>{m.from}</button>
          </li>
        ))}
      </ul>
      {selected && <article>{selected.body}</article>}
    </section>
  );
}
