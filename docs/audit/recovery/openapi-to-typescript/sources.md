# openapi-to-typescript: sources (plan 14, batch 7, checked 2026-11-07)

## Origin

- The skill came from softaworks/agent-toolkit. `git show 3027f20f:skills/openapi-to-typescript/` holds only README.md and SKILL.md, and `git diff --stat 3027f20f dbff837f -- skills/openapi-to-typescript` is empty: the baseline is the upstream text.
- Upstream history: one commit touches the path, `06825f04` (2026-01-18, Leonardo Flores, "feat: add 23 curated skills with comprehensive documentation"). `gh api repos/softaworks/agent-toolkit/commits?path=skills/openapi-to-typescript` shows nothing newer; upstream `main` is `3027f20f`, the fork point.
- Web search on the old distinctive phrases (the file header "DO NOT EDIT MANUALLY - Regenerate from OpenAPI schema", "Error Types (always include)") found only listings and copies of the softaworks skill (skillselion.com, llmbase.ai, claudskills.com, aitmpl.com, a `cachemoney/agent-toolkit` fork). No earlier origin.
- Current state: README.md ends with "Part of the Softaworks Agent Skills collection." (the license line, kept), but the folder has no credit line of the form the other softaworks skills use, and `docs/audit/upstream-sources.json` has no row with `skill: openapi-to-typescript`.
- Everything in the current SKILL.md and references/guards.md is our own rewrite after the fork (commits `de35b734`, `46b06765`, `b60f1ff0`); it quotes the OpenAPI 3.0.3 specification, which the rows below credit.

## Missing credit line (add to skills/openapi-to-typescript/README.md, before `## License`; the existing License line stays untouched)

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

This is the exact line `skills/database-schema-designer/README.md` uses. Each registry `credit` must also appear in SKILL.md, README.md or references/ (`audit.py` `credit_issues`), so the README needs one sentence naming the vendors:

```text
Spec and tool facts were checked against the official documentation of the OpenAPI Initiative (OpenAPI 3.0.3, 3.1.0), SmartBear (Swagger 2.0), the IETF (RFC 6901), Ecma International (ECMAScript), JSON Schema, Microsoft (TypeScript), Node.js, npm, FastAPI, springdoc and NestJS.
```

## Proposed registry rows (verbatim JSON, one object per line, to append to docs/audit/upstream-sources.json)

All rows pass `validate_entry` (checked 2026-11-07 with a throwaway script). Each page is the official page used in facts.md.

```json
{"skill": "openapi-to-typescript", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/openapi-to-typescript", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "OpenAPI Specification 3.0.3: https://spec.openapis.org/oas/v3.0.3", "ref": null, "credit": "OpenAPI Initiative"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "OpenAPI Specification 3.1.0 and the migration guide from 3.0 to 3.1: https://spec.openapis.org/oas/v3.1.0 and https://www.openapis.org/blog/2021/02/16/migrating-from-openapi-3-0-to-3-1-0", "ref": null, "credit": "OpenAPI Initiative"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "Swagger 2.0 specification: https://swagger.io/specification/v2/", "ref": null, "credit": "SmartBear"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "RFC 6901, JavaScript Object Notation (JSON) Pointer: https://www.rfc-editor.org/rfc/rfc6901", "ref": null, "credit": "IETF"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "ECMA-262, Number.MAX_SAFE_INTEGER: https://tc39.es/ecma262/", "ref": null, "credit": "Ecma International"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "JSON Schema, const keyword: https://json-schema.org/understanding-json-schema/reference/const", "ref": null, "credit": "JSON Schema"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "TypeScript TSConfig reference: https://www.typescriptlang.org/tsconfig/", "ref": null, "credit": "Microsoft"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "Node.js docs, Modules: TypeScript, and Errors (ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX): https://nodejs.org/api/typescript.html and https://nodejs.org/api/errors.html", "ref": null, "credit": "Node.js"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "npm docs, npx: https://docs.npmjs.com/cli/v11/commands/npx", "ref": null, "credit": "npm"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "FastAPI release notes, 0.99.0 (OpenAPI 3.1.0): https://fastapi.tiangolo.com/release-notes/", "ref": null, "credit": "FastAPI"}
{"skill": "openapi-to-typescript", "kind": "unversioned", "source": "springdoc-openapi documentation and changelog (2.8.0, OpenAPI 3.1 default): https://springdoc.org/ and https://github.com/springdoc/springdoc-openapi/blob/main/CHANGELOG.md", "ref": null, "credit": "springdoc"}
{"skill": "openapi-to-typescript", "kind": "github-path", "source": "nestjs/swagger:lib/fixtures/document.base.ts", "ref": "master", "credit": "NestJS"}
```

Known limit: `upstreams` reports `stale: false` for `unversioned` rows, so only a skill-updater run notices a changed page. The `nestjs/swagger` row is a `github-path` so a change of the default `openapi` version shows up as `stale`; `master` is that repository's default branch.

## skill-updater style review (review only, no `track` call)

- Upstream change since the fork: none. The only upstream commit on the path is `06825f04` (2026-01-18), already in the baseline. Adopt: none. Adapt: none. Ignore: none. The softaworks version also predates every rule that makes the current skill what it is (preflight table, naming algorithm, Null rule, open-object rule, guard soundness).
- The git-side `upstreams` run was not made: the registry has no row for this artifact yet. After the rows land, the row `softaworks/agent-toolkit:skills/openapi-to-typescript` is expected to read `stale: false` (no upstream commit after the local ones).
- Model-validity pass: NOT run. It needs a tool-less probe through an LLM lane, which the analyst rails (4) forbid. Rules that exist to counter a model habit and should be probed by the controller (each prompt without the skill loaded, behavior present once means keep): (1) never emit a TS `enum` for a spec `enum`; (2) never add `| null` for `nullable: true` beside a `$ref`; (3) never invent an `ApiError`; (4) never write `as any` casts inside guards; (5) never rename query keys to camelCase; (6) `allOf` as `A & B` not `interface extends`. The existing evals (spec-types, pets-operations, shapes-guards, union-ref, open-objects) already test several of these with the skill loaded.

## Items for the restore brief (the controller decides)

- Credit: add the two README sentences above (no existing line is removed).
- Facts (facts.md): guards.md "Node 23.6+" becomes "Node 22.18+ or 23.6+" or a pointer to https://nodejs.org/api/typescript.html; the SKILL.md FastAPI Gotcha also names springdoc 2.8.0 and later (3.1 by default since 2.8.0, `springdoc.api-docs.version` selects 3.0).
- Optional (adapt, from the one borderline drop, s018 and s026): one clause in the Mapping decisions format rows, "add `/** format: <name> */` for `uuid`, `email`, `uri`, `date`, `date-time` when the schema has no `description`", so the JSDoc keeps the information the TS type loses. Skipping it is also defensible (see the Step 3 table in the report).
- Optional: the validation loop could use the documented `npx --package=typescript tsc ...` form instead of `-p` (npm documents `-p` as maintained but undocumented for npx).
- No restore to references/ is proposed: no row is `restore-*`.
