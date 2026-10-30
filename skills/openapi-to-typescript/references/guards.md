# Sound runtime guards

Load when generating runtime predicates from OpenAPI schemas. A TypeScript type predicate is a promise to the compiler: returning `true` must imply that the value satisfies the entire target type.

## Required checks

- Start from `unknown`; reject `null`, arrays, and primitives when an object is required.
- Check each required own/inherited property as appropriate for the generated contract, then recursively validate its schema.
- For each optional property, accept absence; if present, validate its complete schema. Optional does not mean untyped.
- For nullable schemas, accept `null` only when `nullable: true`; otherwise recurse into the non-null schema.
- Validate every array element recursively, not only `Array.isArray`.
- Validate enum membership and all composition branches (`oneOf`, `anyOf`, `allOf`) according to their semantics.
- For dictionaries, validate each value against `additionalProperties` when it is a schema. Enforce closed-object constraints when represented in the emitted type.
- For recursive schemas, track object identity on the current traversal path (e.g. `WeakSet<object>`) to prevent infinite loops; do not treat a cycle alone as proof that unchecked properties are valid.

Prefer small reusable validators for primitives, arrays, objects, and compositions. Avoid `any` casts that bypass the check. Unknown or unsupported keywords that affect validity must be reported; omit the guard rather than emitting an unsound predicate.

## Example: optional and nullable

For `type: object`, required `[id]`, `id: string`, and optional `label: {type: string, nullable: true}`:

```ts
function isItem(value: unknown): value is Item {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
  const v = value as Record<string, unknown>;
  if (typeof v.id !== "string") return false;
  if ("label" in v && v.label !== null && typeof v.label !== "string") return false;
  return true;
}
```
