# Batch 12

## openapi-to-typescript (skill)

### openapi-to-typescript#D7-1
- severity: medium
- dimension: D7
- location: skills/openapi-to-typescript/evals/evals.json:7
- fix: Make the prompt, expected output, and assertions agree: define ApiError in the input or omit it, and explicitly request runtime guards when asserting their presence. Add complete operation and schema inputs for composition, parameter-location, and response-variant cases.

### openapi-to-typescript#D7-2
- severity: medium
- dimension: D7
- location: skills/openapi-to-typescript/evals/trigger-queries.json:23
- fix: Add realistic OpenAPI 3.0 context to ambiguous positives and pair them with closely matched standalone JSON Schema, non-TypeScript, and unsupported-version negatives.

### openapi-to-typescript#D8-1
- severity: medium
- dimension: D8
- location: skills/openapi-to-typescript/SKILL.md:32
- fix: Add a validation loop using the repository's TypeScript check, plus guard cases covering present malformed optionals, nullable branches, array elements, and compositions. Fix failures before reporting completion; explicitly report when validation cannot run.

### openapi-to-typescript#D8-2
- severity: low
- dimension: D8
- location: skills/openapi-to-typescript/SKILL.md:14
- fix: Define one deterministic naming algorithm, including parameter markers and any singularization policy, and make the example match it. Include a collision example demonstrating the specified disambiguation rule.

### openapi-to-typescript#D7-1
- severity: low
- dimension: D7
- location: skills/openapi-to-typescript/evals/evals.json:16
- fix: Add evals for recursive $ref guards (cycle safety) and operationId collisions — both rule-heavy paths no eval covers

### openapi-to-typescript#D8-1
- severity: low
- dimension: D8
- location: skills/openapi-to-typescript/SKILL.md:12
- fix: State the empty-schemas branch explicitly: emit only operation types and report zero named schemas, so the agent is not left guessing

### openapi-to-typescript#D1-1
- severity: medium
- dimension: D1
- location: skills/openapi-to-typescript/SKILL.md:21
- fix: Consolidate repeated warnings and elementary mappings. Preserve the 3.0-specific nullable rules, named recursive references, media/status distinctions, and refusal policies; add concrete context-sensitive transformations rather than repeating basic TypeScript mappings.

### openapi-to-typescript#D3-1
- severity: medium
- dimension: D3
- location: skills/openapi-to-typescript/SKILL.md:36
- fix: Add explicit warnings that OpenAPI 3.0 Reference Object siblings are ignored, and that readOnly/writeOnly affect request/response projection and requiredness. Explain the incorrect contracts produced when these distinctions are ignored.

### openapi-to-typescript#D6-1
- severity: medium
- dimension: D6
- location: skills/openapi-to-typescript/SKILL.md:23
- fix: Provide a default representation for pure dictionaries and an explicit policy for mixed fixed/additional properties. Require a diagnostic rather than an incompatible index signature when exact representation is unavailable, and identify any deliberately approximate representation as such.

### openapi-to-typescript#D1-1
- severity: low
- dimension: D1
- location: skills/openapi-to-typescript/SKILL.md:12
- fix: Drop the ask-for-file clause (default agent behavior); keep the version and paths checks, which are the non-obvious part

### openapi-to-typescript#D2-1
- severity: low
- dimension: D2
- location: skills/openapi-to-typescript/SKILL.md:14
- fix: Give one collision example with the exact emitted names (e.g. two GET /users/{id} operations → GetUserById and GetUserByIdQueryParams) so the suffix rule is unambiguous

### openapi-to-typescript#D3-1
- severity: low
- dimension: D3
- location: skills/openapi-to-typescript/SKILL.md:21
- fix: Add the missing environment gotchas: oneOf without a discriminator field, and readOnly/writeOnly asymmetry between request and response types

### openapi-to-typescript#D6-1
- severity: low
- dimension: D6
- location: skills/openapi-to-typescript/SKILL.md:15
- fix: For large specs, summarize planned type names before writing (or support a dry run) so a naming collision does not produce a full-file rewrite
