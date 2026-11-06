// src/components/ChatComposer.tsx (React 19)
import type { KeyboardEvent } from 'react';

export function ChatComposer({ onSend }: { onSend: (text: string) => void }) {
  const onKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') e.currentTarget.form?.requestSubmit();
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        const text = new FormData(e.currentTarget).get('message');
        if (typeof text === 'string' && text.trim()) onSend(text);
        e.currentTarget.reset();
      }}
    >
      <textarea name="message" onKeyDown={onKeyDown} />
      <button>Send</button>
    </form>
  );
}

// Bug reports:
// 1. Japanese users: pressing Enter to confirm a kana-to-kanji conversion sends the half-typed message (seen on Safari too).
// 2. Shift+Enter should add a new line but sends the message.
// 3. After sending with Enter, a stray newline is left in the box.
