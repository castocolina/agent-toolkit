# OpenAPI to TypeScript

An agent skill that turns an OpenAPI 3.0.x document (JSON or YAML) into TypeScript declarations: one type per component schema, per-operation parameter, request-body and response types, and, on request, sound runtime type guards.

## What you get

- Types that are exact for the spec, or marked `Approximate` with the reason (for example an exclusive `oneOf` that a TypeScript union cannot express).
- Separate request and response views when a schema has `readOnly` or `writeOnly` properties.
- Deterministic names, with any collision renamed and reported.
- A report of everything that was ignored, unsupported or undocumented, and whether `tsc` ran.

The conversion rules, naming algorithm and worked example live in [SKILL.md](SKILL.md); the guard rules live in [references/guards.md](references/guards.md).

## Example requests

- "Generate TypeScript types from api/openapi.yaml into src/types/api.ts."
- "Type the endpoints in openapi.json and add type guards so I can validate responses at runtime."
- "How should a oneOf with a discriminator map to TypeScript in our 3.0 spec?"

## Limits

- OpenAPI 3.0.x only. Swagger 2.0 and OpenAPI 3.1 are refused with the reason.
- External or unresolved `$ref`s stop the run until you accept a partial result.
- No HTTP client, mock server, Zod output or spec linting.

## Installation

**Claude Code:**

```bash
cp -r skills/openapi-to-typescript ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste the contents of `SKILL.md` into the conversation.

## Tests

Output evals and trigger queries are in `evals/`; the eval input specs are in `evals/files/`.

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Spec and tool facts were checked against the official documentation of the OpenAPI Initiative (OpenAPI 3.0.3, 3.1.0), SmartBear (Swagger 2.0), the IETF (RFC 6901), Ecma International (ECMAScript), JSON Schema, Microsoft (TypeScript), Node.js, npm, FastAPI, springdoc and NestJS.

## License

Part of the Softaworks Agent Skills collection.
