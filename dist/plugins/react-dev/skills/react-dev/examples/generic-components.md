# Generic Components

The column builder in SKILL.md owns the key/value pairing rule. This file covers the rest of generic inference: where `T` is inferred from, how to stop it widening, and the syntax traps. Every snippet type-checks under TypeScript 5.6 with `@types/react` 19.

## A table that consumes the builder's columns

```tsx
// Column<T> and columnsFor<T>() as in SKILL.md
type TableProps<T> = { rows: readonly T[]; columns: readonly Column<T>[]; rowKey: (row: T) => string | number };
declare function Table<T>(props: TableProps<T>): ReactElement; // body: map rows x columns, calling column.cell(row)

<Table rows={users} columns={columns} rowKey={(u) => u.id} />; // T = User, so u.id is number without annotation
```

Sorting belongs to the owner of `rows` (derive a sorted copy during render); a `useState(props.rows)` copy inside the table goes stale when the parent's rows change.

## Choose the inference source with `NoInfer` (TypeScript 5.4+)

`T` is inferred from every prop that mentions it. A secondary prop such as `value` or `defaultValue` can widen `T` instead of being checked against it:

```tsx
type SelectProps<T> = {
  options: readonly T[];
  value: NoInfer<T> | null;          // checked against T, never a source for it
  onChange: (value: T) => void;
  getKey: (option: T) => string;     // identity for <option value> and for finding the selection
  getLabel: (option: T) => string;
};

export function Select<T>({ options, value, onChange, getKey, getLabel }: SelectProps<T>) {
  return (
    <select
      value={value === null ? '' : getKey(value)}
      onChange={(e) => {
        const next = options.find((o) => getKey(o) === e.currentTarget.value);
        if (next !== undefined) onChange(next);
      }}
    >
      <option value="" disabled>Select…</option>
      {options.map((o) => <option key={getKey(o)} value={getKey(o)}>{getLabel(o)}</option>)}
    </select>
  );
}
```

With `value: T | null`, `<Select options={['asc', 'desc'] as const} value="random" … />` compiles because `T` widens to `'asc' | 'desc' | 'random'`; with `NoInfer` it is an error. Before TypeScript 5.4, get the same effect with a second parameter: `<T, V extends T = T>` and `value: V | null`.

Match options by `getKey`, not by reference (`value === option`): the selected object usually comes from a different fetch or a copy and is never `===` to an option.

## Literal unions from a prop: `const` type parameters (TypeScript 5.0+)

```tsx
export function Tabs<const T extends readonly string[]>({ tabs, active }: { tabs: T; active: T[number] }) {
  return <div>{tabs.map((t) => <button key={t} aria-pressed={t === active}>{t}</button>)}</div>;
}

<Tabs tabs={['profile', 'billing']} active="billing" />;
// @ts-expect-error 'security' is not one of the tabs
<Tabs tabs={['profile', 'billing']} active="security" />;
```

Without `const`, `tabs` infers as `string[]` and any `active` string passes. On TypeScript 5.0 to 5.2 the constraint must be `readonly string[]` (a mutable constraint silently falls back to `string[]`); from 5.3 either works.

## Syntax traps

| Trap | Fix |
|---|---|
| `const f = <T>(x: T) => x` in a `.tsx` file parses as JSX | `<T,>(x: T) => x` or `<T extends unknown>` |
| Inference picks the wrong `T` and the error lands deep in a callback | pass it explicitly: `<List<Row> items={rows} render={(r) => r.id} />` |
| `forwardRef` or `memo` around a generic component makes `T` `unknown` | cast the result to a generic call signature (react-19-patterns.md), or use the React 19 `ref` prop and skip `forwardRef` |
| Discriminated props destructured in the parameter list stop narrowing after one is reassigned | keep destructured bindings `const`; narrowing of destructured unions needs TypeScript 4.6+ and unassigned bindings |
| `Record<string, T>` lookups typed as always present | enable `noUncheckedIndexedAccess`, or type the map as `Partial<Record<K, T>>` |
