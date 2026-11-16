# React 19 Patterns

Code for the React 19 rules in SKILL.md (the rules themselves live there). All snippets type-check with `@types/react` 19 under `strict`.

## Refs: React 19 prop vs React 18-compatible `forwardRef`

```tsx
import { forwardRef, type ComponentPropsWithoutRef, type ForwardedRef, type ReactElement, type Ref } from 'react';

// React 19-only app: ref is an ordinary prop.
type ButtonProps = { variant: 'primary' | 'secondary'; ref?: Ref<HTMLButtonElement> } & ComponentPropsWithoutRef<'button'>;
export function Button({ variant, ref, ...rest }: ButtonProps) {
  return <button ref={ref} data-variant={variant} {...rest} />;
}

// Peers allow React 18: forwardRef (still valid in 19). A named function keeps the DevTools name.
type LibButtonProps = { variant: 'primary' | 'secondary' } & ComponentPropsWithoutRef<'button'>;
export const LibButton = forwardRef<HTMLButtonElement, LibButtonProps>(function LibButton({ variant, ...rest }, ref) {
  return <button ref={ref} data-variant={variant} {...rest} />;
});

// forwardRef erases generics: re-assert the generic call signature on the result.
type ListProps<T> = { items: T[]; label: (item: T) => string };
function ListInner<T>({ items, label }: ListProps<T>, ref: ForwardedRef<HTMLUListElement>) {
  return <ul ref={ref}>{items.map((i) => <li key={label(i)}>{label(i)}</li>)}</ul>;
}
export const List = forwardRef(ListInner) as <T>(props: ListProps<T> & { ref?: Ref<HTMLUListElement> }) => ReactElement;
```

Without the cast, `<List items={[1, 2]} label={(n) => ...} />` infers `n: unknown`. `memo()` erases generics the same way and takes the same cast.

## `useActionState`

```tsx
type SaveState = { status: 'idle' | 'saved' | 'error'; errors?: Partial<Record<'name', string[]>> };
declare function saveProfile(prev: SaveState, formData: FormData): Promise<SaveState>; // annotated return, 'use server' module

const [state, formAction, isPending] = useActionState(saveProfile, { status: 'idle' } satisfies SaveState);
```

Migration from `ReactDOM.useFormState`: same `(state, payload)` action signature; the import moves to `react` and the tuple gains `isPending`. When the action is a Server Action, also apply the authorization rules in SKILL.md (code in the server examples).

## `useOptimistic`: confirm, commit, roll back

```tsx
'use client';
import { startTransition, useOptimistic, useState } from 'react';

type Message = { id: string; text: string; pending?: true };

export function Thread({ initial }: { initial: Message[] }) {
  const [messages, setMessages] = useState(initial);          // authoritative state
  const [error, setError] = useState<string | null>(null);
  const [optimistic, addOptimistic] = useOptimistic(messages, (state, m: Message) => [...state, m]);

  async function send(formData: FormData) {                    // runs as an Action via <form action>
    const text = formData.get('text');
    if (typeof text !== 'string' || !text.trim()) return;
    setError(null);
    addOptimistic({ id: crypto.randomUUID(), text, pending: true }); // unique temp id: two quick sends never collide
    try {
      const res = await fetch('/api/messages', { method: 'POST', body: JSON.stringify({ text }) });
      if (!res.ok) throw new Error(`Send failed: ${res.status}`);
      const saved = (await res.json()) as Message;               // the server's id and text
      startTransition(() => setMessages((prev) => [...prev, saved])); // success: commit, after await needs its own transition
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Send failed');  // failure: base state unchanged, so the temp row disappears
    }
  }

  return (
    <>
      <ul>{optimistic.map((m) => <li key={m.id} aria-busy={m.pending}>{m.text}</li>)}</ul>
      {error && <p role="alert">{error}</p>}
      <form action={send}><input name="text" /><button>Send</button></form>
    </>
  );
}
```

When the Action ends, React renders the base state: the temp row is replaced by `saved` on success and simply vanishes on failure. If a parent owns `messages`, commit by calling the parent's callback or `router.refresh()` inside that inner transition instead of local `setMessages`. Validate `saved` at runtime if the API is untrusted; the cast only names the expected shape.

## `use()`

```tsx
// Server Component: create the promise, do not await, wrap the consumer in Suspense.
export default function Page() {
  const userPromise = fetchUser();                       // stable: created once per server render
  return <Suspense fallback={<Skeleton />}><Profile userPromise={userPromise} /></Suspense>;
}

// Client Component
'use client';
export function Profile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);                         // may sit inside if/loops; not inside try/catch
  return <h1>{user.name}</h1>;
}
```

In a client-only app, get the promise from a cache keyed by resource id (a module `Map`, or the data library's Suspense API), never from a call in render. `use(Context)` works like `useContext` but may be conditional; it is not supported in Server Components. The resolved value must be serializable when it crosses the server/client boundary.

## Transitions and deferred rendering

`startTransition(fn)` runs `fn` immediately and synchronously; it only lowers the priority of the state updates scheduled during it. Wrapping a heavy `filter` in it does not move that work off the input's critical path. Defer the render that does the work instead:

```tsx
const Results = memo(function Results({ query, products }: { query: string; products: Product[] }) {
  const q = query.toLowerCase();
  return <ul>{products.filter((p) => p.name.toLowerCase().includes(q)).map((p) => <li key={p.id}>{p.name}</li>)}</ul>;
});

export function Search({ products }: { products: Product[] }) {
  const [query, setQuery] = useState('');                // urgent: the input never lags
  const deferred = useDeferredValue(query);              // Results re-renders later, interruptibly
  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.currentTarget.value)} />
      <div style={{ opacity: query !== deferred ? 0.6 : 1 }}><Results query={deferred} products={products} /></div>
    </>
  );
}
```

`memo` is required: without it `Results` re-renders with the parent on every keystroke and the deferral buys nothing. When one synchronous computation is itself too slow (hundreds of milliseconds), no React API fixes it; move it to a Web Worker or index the data.

Use `useTransition` for navigation-like updates and Actions, where `isPending` drives UI: `startTransition(async () => { await save(); startTransition(() => setSaved(true)); })`.

## Migration checklist (React 18 to 19)

1. Pin `react`, `react-dom`, `@types/react`, `@types/react-dom` to 19 together.
2. Run the codemod exactly as the SKILL.md React 19 gotcha says (pinned version, real source roots, opt-in transforms for ref-callback returns and `ReactElement` props).
3. Replace `import { act } from 'react-dom/test-utils'` with `import { act } from 'react'`; replace other test-utils calls (for example with Testing Library).
4. `useFormState` from `react-dom` becomes `useActionState` from `react`.
5. Keep `forwardRef` in anything still published for React 18 peers; convert app-only components to the `ref` prop.
6. Re-run the typecheck and tests; fix ref callbacks that return values.
