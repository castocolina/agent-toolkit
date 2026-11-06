# Batch 46

## openapi-to-typescript (skill)

### openapi-to-typescript#D7-1
- severity: low
- dimension: D7
- location: skills/openapi-to-typescript/evals/evals.json:9
- fix: Remove `references/guards.md` from the `files` of the `spec-types` and `shapes-guards` evals. Listing it hands the reference to the run, so these evals cannot catch a run that skips the gated load. Add an assertion that the guard output follows a guards.md-only rule, such as the `"x" in v` presence check.

### openapi-to-typescript#D8-1
- severity: medium
- dimension: D8
- location: skills/openapi-to-typescript/SKILL.md:57
- fix: Add a mapping row for a `discriminator` on a base schema that its subtypes extend through `allOf: [{$ref: Base}, ...]`, the form springdoc and NestJS usually emit and which the description names. Following the current table, `Base` becomes a plain interface, each subtype becomes `Base & {...}`, and the discriminator property stays `string`, with no report. Say whether to narrow each subtype's discriminator to its mapping value and whether to emit a union of the subtypes, and mark the result `Approximate` when you cannot.

### openapi-to-typescript#D8-1
- severity: high
- dimension: D8
- location: skills/openapi-to-typescript/references/guards.md:14
- fix: State that null is allowed when the same Schema Object declares type and nullable: true, provided any enum present includes null and other applicable constraints permit it. Explicitly distinguish an absent enum from an enum that excludes null, and add a mutation check accepting null for a nullable property without an enum.

### openapi-to-typescript#D8-2
- severity: high
- dimension: D8
- location: skills/openapi-to-typescript/references/guards.md:77
- fix: Export an unknown-only wrapper that creates fresh traversal state and delegates to a private recursive helper. Keep WeakSet parameters private, including per-schema state threaded through mutually recursive helpers, so callers cannot prepopulate the visited set and bypass validation.

### openapi-to-typescript#D8-3
- severity: high
- dimension: D8
- location: skills/openapi-to-typescript/SKILL.md:58
- fix: Replace the unconditional exact claim with: emit A | B, preserving approximation from every branch. Explicitly propagate Approximate status through references, unions, intersections, arrays, object properties and request projections; only call a composite exact when its constituent mappings and the composition itself are exact.

### openapi-to-typescript#D1-1
- severity: low
- dimension: D1
- location: skills/openapi-to-typescript/SKILL.md:157
- fix: Shorten this step to the part the model would miss: "Fix the mapping decision that caused the error." Models already avoid `any`, casts and `@ts-ignore` as fixes and already rerun until the check passes.
