---
name: openapi-to-typescript
description: "Convert OpenAPI 3.0.x JSON/YAML specifications into TypeScript schema and request/response types plus runtime type guards. Use when generating frontend types from an API spec or converting components/schemas and paths to TS, including when the user only asks for backend API interfaces. Keywords: OpenAPI 3.0, $ref, oneOf, allOf, type guard. Not for Swagger 2.0, OpenAPI 3.1, HTTP clients, mock servers, standalone JSON Schema/Zod conversion, or spec-only validation."
---

# OpenAPI to TypeScript

Generate declarations from the supplied OpenAPI 3.0.x document, preserving schema semantics rather than guessing. This skill does not generate a client or validate a spec without producing types.

## Preflight and inventory

1. Read the provided JSON/YAML; ask for the file only if absent. Confirm `openapi` starts with `3.0`, `paths` exists, and note whether `components.schemas` exists. Stop with a specific incompatibility report for Swagger 2.0/3.1 or invalid input.
2. Before generation, identify refs outside `components/schemas`, unresolved/external refs, and unsupported constructs. Resolve only refs whose targets are present and understood. Stop and report unresolved/external refs instead of silently weakening types.
3. Inventory each operation: `operationId`, method/path, path/query/header/cookie parameters, request media types, and each response status/media type/schema. Use `operationId` for stable names where present; otherwise derive names from method and path, stripping braces and PascalCasing segments (e.g. `GET /users/{id}/orders` → `GetUserByIdOrders`). Detect collisions before emission; disambiguate deterministically with parameter or status/media suffixes and state the rule.
4. Write to `types/api.ts` by default. Use an existing repository types convention if found; ask only if competing locations are ambiguous. Report the actual path written.

## Non-obvious schema decisions

- Requiredness is independent of nullability: required non-nullable `name` is `name: string`; required nullable is `name: string | null`; optional nullable is `name?: string | null`. In OpenAPI 3.0, `nullable: true` modifies a typed schema; do not interpret `type: null` as a valid 3.0 schema.
- Keep named `$ref`s as named TS references, including recursive references. Do not inline them: duplication drifts and recursion can become impossible to represent.
- `oneOf` maps to a union, `allOf` generally to an intersection, and enums to literal unions. Do not assume every `allOf` is safely representable as interface inheritance; preserve composition semantics.
- Keep parameters distinct by location. Path parameters are required by the path contract; query/header/cookie requiredness follows the parameter declaration. Request and response variants must retain media type and status distinctions where their schemas differ.
- Model additional properties/dictionaries explicitly. Do not turn an unconstrained object into an invented fixed interface.
- Generate errors only from documented response schemas. A generic fallback is opt-in and must use a collision-safe name. If the supplied spec defines a reusable error schema such as `ApiError`, emit its TypeScript type like other named schemas and include its guard when runtime guards are requested; do not fabricate error shapes.

## Runtime type guards

Load [guard-generation rules](references/guards.md) when emitting runtime guards. A predicate must validate every condition implied by the type: required fields, every present optional field, nested objects, array elements, enum membership, nullable branches, and additional-property constraints. Make recursive checks cycle-safe. If a schema cannot be checked soundly, report it and do not emit a predicate that claims the broader type.

## Output

Emit schema types first, then operation parameter/request and documented response types, followed by guards when requested. If a GET (or any operation) has no documented response schema, omit its response type rather than aliasing it to `unknown`; report that response schema is undocumented. Preserve source descriptions as JSDoc where useful. Do not emit undocumented success/error response shapes as facts. Summarize unsupported or unresolved constructs, naming collisions and chosen output path.

## Gotchas

- Never conflate absent and nullable properties: doing so rejects valid payloads or accepts invalid ones.
- Never accept an unresolved external reference and substitute `unknown` silently; callers may believe the generated contract is complete.
- Never invent response schemas for undocumented statuses; represent only documented content and note the gap.
- Never implement guards that check only required fields: malformed present optionals or array elements would pass a false type predicate.
