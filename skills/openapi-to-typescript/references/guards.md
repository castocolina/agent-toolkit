# Sound runtime guards

Load only when the user asked for runtime validation or type guards. A type predicate `value is T` is a promise to the compiler: `true` must imply that the value satisfies all of `T`. A guard may be stricter than `T` (it enforces exclusive `oneOf` and the exact shape behind an `Approximate` type), never looser.

Before writing each guard, ask: which malformed value would still return `true`? If one exists, the guard is unsound.

## What each construct must check

| Construct | Check |
|---|---|
| object | `typeof v === "object" && v !== null && !Array.isArray(v)` |
| required property | present and its full schema valid |
| optional property | absent (`!("x" in v)`), or present and its full schema valid. A present `undefined` is invalid: JSON never produces it, and under `exactOptionalPropertyTypes` it does not satisfy `x?: T` |
| `null` | accept `null` exactly where the emitted type has `\| null`, which the **Null rule** row in SKILL.md decides; do not re-derive it here. A nullable property with no `enum` accepts `null` (`tag` below); an `enum` that omits `null`, a `$ref` sibling and `nullable` without a same-schema `type` do not (`level`, `owner`, `lead` below) |
| array | `Array.isArray` and every element valid |
| `enum` | membership in the listed values |
| `oneOf` without discriminator | exactly one branch matches (count the matches) |
| `oneOf` with discriminator | the discriminator value selects the candidate branch, which must match; an unknown value returns `false` (the spec: "validation SHOULD fail"). Then still require that no other branch matches, unless every branch declares the discriminator property `required` with a single-value `enum`, the values are pairwise distinct, and each value is the one the mapping (or the implicit schema name) assigns to that branch; only then are the branches disjoint. Two branches that both require `kind: {enum: [x]}` still overlap. The discriminator is a hint; it does not lift `oneOf`'s exactly-one rule |
| `anyOf` with discriminator | the selected candidate must match; an unknown value returns `false` |
| `anyOf` | at least one branch matches |
| `allOf` | every branch matches |
| `additionalProperties: <schema>` | every key not in `properties` has a valid value |
| `additionalProperties: false` | no key outside `properties` |
| `additionalProperties` absent, `true` or `{}` (open object, `[key: string]: unknown`) | nothing for extra keys: any value is valid |
| `required` name with no `properties` entry | the key is present (`"id" in v`), and its value is valid against `additionalProperties` when that is a schema |
| recursive schema | track objects on the current call path in private state (below) so a cycle cannot loop forever |

Schema-only constraints (`pattern`, `minLength`, `minimum`, `maxItems`, `format`) are not part of the emitted type, so a guard is sound without them. Check them only when the user asks, and list them as unchecked in the report. If a construct affects the type and cannot be checked, omit that guard and report why rather than emit a predicate that claims the type.

## Exported signature

Every exported guard has exactly the signature `(value: unknown) => value is T`. Traversal state never appears in an exported signature: a caller could pre-fill it and make `isTreeNode(v, new WeakSet([v]))` return `true` for any object. A guard for a recursive schema is an exported wrapper that creates fresh state and delegates to a private helper; private helpers pass the same state to every other recursive helper they call, so mutually recursive schemas share one call path.

## Patterns

Type-checked with `tsc --strict` (also with `exactOptionalPropertyTypes`) against their declarations (`Animal = (Cat & { petType: "cat" }) | (Dog & { petType: "Dog" })`, `Shape = Circle | Square`, `TreeNode { value: string; children?: TreeNode[] }`, `Ticket { status: "active" | null; level: "low" | "high"; owner: Owner; lead: Owner }`; every object interface also carries `[key: string]: unknown` per SKILL.md's open-object rule, so no guard below checks extra keys except `isMetadata`). `isOwner`, `isCat`, `isDog`, `isCircle` and `isSquare` follow the `isPet` pattern.

```ts
type Rec = Record<string, unknown>;
const isRecord = (v: unknown): v is Rec =>
  typeof v === "object" && v !== null && !Array.isArray(v);

// Required `id`, `name`; optional nullable `tag`; optional dictionary `labels` of strings.
export function isPet(value: unknown): value is Pet {
  if (!isRecord(value)) return false;
  if (typeof value.id !== "string" || typeof value.name !== "string") return false;
  if ("tag" in value && value.tag !== null && typeof value.tag !== "string") return false;
  if ("labels" in value) {
    if (!isRecord(value.labels)) return false;
    if (!Object.values(value.labels).every((x) => typeof x === "string")) return false;
  }
  return true;
}

// Effective nullability (all required):
// status: {type: string, nullable: true, enum: [active, null]} -> "active" | null
// level:  {type: string, nullable: true, enum: [low, high]}  -> "low" | "high" (enum lists no null)
// owner:  {$ref: Owner, nullable: true}                       -> Owner (Reference Object sibling ignored)
// lead:   {allOf: [{$ref: Owner}], nullable: true}            -> Owner (no `type` in the same schema)
export function isTicket(value: unknown): value is Ticket {
  if (!isRecord(value)) return false;
  if (value.status !== null && value.status !== "active") return false;
  if (value.level !== "low" && value.level !== "high") return false;
  return isOwner(value.owner) && isOwner(value.lead);
}

// Discriminated oneOf: mapping { cat: Cat }, Dog implicit, so the values are "cat" and "Dog".
// Cat and Dog both type `petType` as plain string, so the branches overlap: the discriminator
// picks the candidate and no other branch may match. Drop the last line only when the branches are disjoint (see the table).
export function isAnimal(value: unknown): value is Animal {
  if (!isRecord(value)) return false;
  const candidate = value.petType === "cat" ? isCat : value.petType === "Dog" ? isDog : undefined;
  if (candidate === undefined || !candidate(value)) return false;
  return [isCat, isDog].filter((g) => g(value)).length === 1;
}

// oneOf without discriminator: stricter than the `Circle | Square` type, as the spec requires.
export function isShape(value: unknown): value is Shape {
  return [isCircle, isSquare].filter((g) => g(value)).length === 1;
}

// Recursive: the private helpers share `path` (schema name -> objects being checked on the call path).
type Path = Map<string, WeakSet<object>>;
function enter(path: Path, schema: string, v: object, check: () => boolean): boolean {
  let onPath = path.get(schema);
  if (onPath === undefined) path.set(schema, (onPath = new WeakSet()));
  if (onPath.has(v)) return true; // an outer frame is already checking v against this schema
  onPath.add(v);
  try {
    return check();
  } finally {
    onPath.delete(v); // path-only: a failed oneOf branch must not leave the object marked
  }
}
function checkTreeNode(value: unknown, path: Path): value is TreeNode {
  return isRecord(value) && enter(path, "TreeNode", value, () =>
    typeof value.value === "string" &&
    (!("children" in value) ||
      (Array.isArray(value.children) && value.children.every((c) => checkTreeNode(c, path)))));
}
export function isTreeNode(value: unknown): value is TreeNode {
  return checkTreeNode(value, new Map());
}

// Approximate type `{ version: number; [key: string]: string | number }`: the guard enforces the exact spec.
export function isMetadata(value: unknown): value is Metadata {
  if (!isRecord(value) || typeof value.version !== "number") return false;
  return Object.entries(value).every(([k, x]) => k === "version" || typeof x === "string");
}
```

Returning `true` on a revisit is sound only for the same schema, which is why `path` is keyed by schema name.

## Mutation tests

Run in a scratch file outside the repository (Node 23.6+ runs `.ts` directly; otherwise compile with `tsc` first), then delete it. For each guard, one valid sample must return `true`, including `null` wherever the type has `| null` (`tag: null`, `status: null`), and each of these that applies must return `false`:

- a present optional property of the wrong type (`tag: 5`) or present as `undefined` (`tag: undefined`)
- `null` in a property that is not nullable, including the cases where `nullable: true` has no effect: an `enum` that does not list `null`, `nullable` beside a `$ref`, and `nullable` without a same-schema `type` (`level`, `owner`, `lead` above)
- one bad element in an array, or one bad dictionary value
- a value that matches two `oneOf` branches, with or without a discriminator (`{ radius: 1, side: 2 }`; `{ petType: "cat", livesLeft: 9, bark: "x" }`, which also fits `Dog`)
- for branches whose discriminator enums are not distinct singletons (`A` and `B` both require `kind: {enum: [x]}`, plus `a` and `b`): `{ kind: "x", a: 1, b: 1 }`, which fits both
- an unknown discriminator value, and the implicit name where an explicit mapping replaced it (`"Cat"` when the mapping key is `cat`)
- an extra key when `additionalProperties: false`
- a missing `required` key that has no `properties` entry (`{}` for `{type: object, required: [id]}`)

An extra key on an open object must return `true`.

A cyclic valid value (`root.children = [root]`) must return `true` without hanging. Calling an exported guard with a second argument must be a compile error.

## NEVER

- NEVER check only `"x" in v` or only `Array.isArray`: present malformed values pass, and the compiler then trusts them.
- NEVER export a guard that takes traversal state: a pre-filled visited set turns it into `return true`.
- NEVER cast with `as any` inside a guard: it hides exactly the mismatch the guard exists to catch.
- NEVER let the discriminator alone decide a `oneOf` with overlapping branches: `{ petType: "cat", livesLeft: 9, bark: "x" }` matches both `Cat` and `Dog`, so the spec rejects it while a switch-only guard accepts it.
- NEVER test an optional property with `v.x !== undefined`: it accepts a present `undefined`, which falls outside `x?: T` under `exactOptionalPropertyTypes`.
