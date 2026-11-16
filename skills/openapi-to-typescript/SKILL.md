---
name: openapi-to-typescript
description: "Convert OpenAPI 3.0.x JSON/YAML specs into TypeScript types for components/schemas and for each operation's parameters, request body and responses, plus runtime type guards on request; Swagger 2.0 and OpenAPI 3.1 input is detected and refused with the reason. Use when generating frontend or SDK types from openapi.yaml/openapi.json (including FastAPI, springdoc or NestJS output), typing the endpoints under paths, updating types/api.ts after the spec changed, or deciding how nullable, readOnly/writeOnly, oneOf/discriminator, allOf, additionalProperties or $ref map to TS, even when the user only says 'API types' or 'typed responses'. Keywords: OpenAPI 3.0, components/schemas, types/api.ts, type guard. Not for standalone JSON Schema or Zod conversion, non-TypeScript targets, HTTP clients, mock servers, or validating a spec without emitting types."
---

# OpenAPI to TypeScript

Turn one OpenAPI 3.0.x document into TypeScript declarations whose every type is either exact for the spec or marked `Approximate`. Nothing the spec does not document becomes a type.

Before emitting each type, ask: would a value the spec rejects compile, or a value it accepts fail to compile? If yes, the type is approximate: say so in its JSDoc and in the report (shape only; see [Approximation propagates](#mapping-decisions)).

## Workflow

0. **Mapping question, not a conversion.** When the user asks how a construct maps, or shows a fragment rather than a whole document to convert, answer from the [mapping table](#mapping-decisions) and naming rules: show the TS, state the assumptions (3.0 semantics; the fragment is the whole schema; referenced names exist), and write no file. Skip the document-level preflight rows (`openapi`, `paths`, references). Still refuse a fragment the user says is Swagger 2.0 or 3.1.
1. **Preflight** (conversions). Check the rows in order and stop at the first Stop that matches. On a Stop, report the reason and emit no TypeScript at all, not even an example. The version rows come first, so nothing later can bypass them.

   | Check | Input | Action |
   |---|---|---|
   | version | `swagger: "2.0"` | Stop: Swagger 2.0 (`definitions`, `in: body`) is not supported; the user must convert it to 3.0 first |
   | version | `openapi: 3.1.x` | Stop: 3.1 uses JSON Schema 2020-12 (`type: [string, "null"]`, `const`, no `nullable`); these 3.0 rules would mistype it |
   | version | `openapi` missing or any value other than `3.0.x` (`3.2.x`, `4.x`) | Stop: only 3.0.x is supported; report the version found |
   | structure | `paths` missing | Stop: not a valid 3.0 document (`paths` is REQUIRED in 3.0) |
   | references | a `$ref` not starting with `#/`, or whose target is missing | Stop before writing; list every such ref with its JSON pointer location. Only if the user then accepts a partial result, emit that type as `unknown` with `/** Unresolved: <ref> */` |
   | schemas | `components.schemas` absent or empty | Continue: emit operation types only and report "0 named schemas" |
   | none matched | | Continue |

2. **Resolve refs by the object kind expected at the use site**, never by where the target lives. Percent-decode the fragment, split it on `/`, then decode each segment (`~1` → `/` first, then `~0` → `~`; RFC 6901) before any lookup.
   - **Schema Object position** (`schema`, `items`, `properties/*`, `additionalProperties`, `allOf`/`oneOf`/`anyOf`): exactly `#/components/schemas/X` (one segment after `schemas`) is the named type from the name table (recursion included; never inline it). Any other existing pointer (`#/components/schemas/Address/properties/postcode`, `#/paths/~1pets/get/responses/200/content/application~1json/schema`) inlines the target's type, never under an invented name; `#/components/schemas/X` refs inside it stay named. If inlining would recurse into itself (no component name to break the cycle), stop and report the pointer.
   - **Parameter, Request Body, Response or Header position:** substitute the referenced object wherever it lives (`#/components/responses/NotFound`, or `#/paths/~1pets/get/responses/200` from another operation), then process it as if written there.
   - **Path Item `$ref`** (`/status: {$ref: "#/paths/~1health"}`): substitute the Path Item under the referencing path, so path-derived names come from the referencing path (`GetStatusResponse200`). If the target's operations carry an `operationId`, the copies repeat it, which 3.0 forbids ("MUST be unique among all operations"): report it, then let the collision rule rename the copies. A field present on both sides has undefined behaviour in 3.0: report it and ask.
   - A missing target: the preflight Stop above. Component keys must match `^[a-zA-Z0-9.\-_]+$` in 3.0, so a schema pointer that decodes to a name with `/` or `~` is missing.
3. **Plan every name before writing any code** (algorithm below). Build the whole table first, so a late collision cannot force a rewrite of names already written. For specs with more than about 30 operations, show the rename lines of the table before writing.
4. **Emit** to the repository's existing API-types location if one exists, else `types/api.ts`; ask only if two existing locations compete. Start the file with `// Generated by openapi-to-typescript from <spec path>. Regenerate; do not edit.` **Updating:** find the existing output by that header (`grep -rl "Generated by openapi-to-typescript"`), else by exports of known schema names (`export interface User`). Overwrite a file only when it carries the header; otherwise ask before replacing it, since it may hold hand edits. Compare its exports with the new ones and list the differences in the report. Carry each `description` into JSDoc. Order: schema types, then per-operation types, then guards (only when requested; see [Runtime guards](#runtime-guards)).
5. **Validate** (loop below), then **report** with this template (write `none` for an empty line):

   ```text
   Output: <path written>
   Named schemas: <count>
   Approximate: <Type> (<cause>); via: <containers>
   Ignored/unsupported: <construct at JSON pointer, and why>
   Renamed: <source> -> <TS name> (<collision>)
   Removed/renamed exports: <old export -> new export or removed> (updates only)
   No documented body: <operation status>; body present, schema undocumented: <operation status/media>
   Unchecked constraints: <pattern, minimum, ... per type>
   Type-check: <command and result, or "not run: <reason>">
   ```

## Naming algorithm

- **PascalCase:** split on non-alphanumerics and lower-to-upper boundaries, capitalise each part, keep the rest: `listPets`, `list_pets` → `ListPets`.
- **Schema name table first:** map every component key to a valid, unique TS name before naming any operation. PascalCase the key; prefix `Schema` when the result is empty or starts with a digit (`123Pet` → `Schema123Pet`); a name that equals another key's result, or a global the output uses (`Record`, `Blob`), takes the lowest free numeric suffix from 2 in `components.schemas` order (`pet-status`, `pet_status` → `PetStatus`, `PetStatus2`). Every `$ref` and every `Write` projection goes through this table. Inline schemas stay inline (`status?: "a" | "b"`); never invent names for them.
- **Operation base:** PascalCased `operationId`, prefixed with `Operation` when the result is empty or starts with a digit (`123` → `Operation123Response200`); collisions are resolved after this step. Without an `operationId`: HTTP method + each path segment PascalCased, with a `{param}` segment becoming `By` + Param. No singularisation: `GET /users/{id}/orders` → `GetUsersByIdOrders`.
- **Suffixes:** `{Base}PathParams`, `{Base}QueryParams`, `{Base}HeaderParams`, `{Base}CookieParams`, `{Base}RequestBody`, `{Base}Response{Status}` (`200`, `2XX`, `Default`). Add a media suffix (`application/problem+json` → `ProblemJson`) only when one status has several media types whose emitted types differ after media handling ([Bodies and responses](#mapping-decisions)); JSON and XML entries that reference the same schema still differ (object vs `string`): `GetReportResponse200Json`, `GetReportResponse200Xml`. Likewise `{Base}RequestBody{Media}` (`CreatePetRequestBodyJson`, `CreatePetRequestBodyFormData`).
- **Projections:** `{Schema}Write` for the request view (see readOnly/writeOnly below).
- **Collisions:** names in the schema table are allocated first and keep their slot. Any later generated name that collides gets the lowest free numeric suffix on its base, starting at 2, in document order (paths in file order, methods in the order get, put, post, delete, options, head, patch, trace). Example: `getUser` on `/users/{id}` and `get_user` on `/v2/users/{id}` both give `GetUser`; the second becomes `GetUser2`, so `GetUser2PathParams`, `GetUser2Response200`.

## Mapping decisions

Only the non-obvious ones; primitives and arrays map the usual way, and `enum` becomes a literal union.

| Spec construct | Emit | Why it is not obvious |
|---|---|---|
| **Null rule** (types and guards both follow it) | add `\| null` only when the same Schema Object declares `type` and `nullable: true`, any `enum` it has lists `null` (no `enum` means no restriction), and no other applicable constraint excludes null (an `allOf` sibling that is not nullable does). Otherwise emit the non-null type; when `nullable: true` had no effect, report it and ask whether null was intended. Required and nullable are independent: `a: T`, `a: T \| null`, `a?: T \| null` | 3.0.3: nullable adds null "only if `type` is explicitly defined within the same Schema Object. Other Schema Object constraints retain their defined behavior, and therefore may disallow the use of `null`" |
| `$ref` with sibling keys (`nullable`, `description`, `readOnly`) | the plain named type; report the ignored siblings and ask if null was intended | a 3.0 Reference Object "cannot be extended"; siblings "SHALL be ignored" |
| `readOnly` / `writeOnly` properties | `X` = response view: readOnly kept with its `required`, writeOnly dropped. `XWrite` = request view: readOnly dropped, writeOnly kept with its `required`. Request bodies use `XWrite`; emit it for every schema that needs a different request view, directly or through a referenced schema | `required` on a readOnly property applies to responses only, on writeOnly to requests only; one shared type forces clients to send server-owned fields |
| `oneOf` + `discriminator` | `(A & { kind: "a" }) \| (B & { kind: "B" })` using each `mapping` key, else the schema name as the value. Mark it `Approximate` unless every branch declares `kind` `required` with a single-value `enum`, the values are pairwise distinct, and each value is the one the mapping (or the implicit schema name) assigns to that branch | the implicit value is the schema name (`Dog`), not a lowercase word; a branch typed `kind: string` does not narrow; the discriminator is a hint, so a value that fits two branches still fails `oneOf` |
| `discriminator` on a base schema that subtypes extend with `allOf: [{$ref: Base}, ...]` (springdoc/NestJS form) | `Base` as declared; each subtype `Cat = Base & { ... } & { kind: "Cat" }`, narrowed to its `mapping` key or implicit schema name; a union `BaseVariant = Cat \| Dog` (name through the name table) of every schema whose `allOf` refs `Base`, used at every other `$ref` to `Base`. Mark `BaseVariant` `Approximate` | the subtype choice comes from the discriminator, a hint: plain schema validation of a `$ref: Base` payload checks only `Base` |
| `oneOf` without discriminator | `A \| B`, marked `Approximate` | TS unions are not exclusive; a value matching both branches compiles but the spec rejects it |
| `anyOf` | `A \| B`; exact only when `A` and `B` are (see propagation below) | |
| `allOf` | `A & B`; report any property whose types conflict (it becomes `never`) | composition is not inheritance; `interface extends` fails on conflicts instead of reporting them |
| **Open-object rule:** an object whose `additionalProperties` is absent, `true` or `{}` | its fixed properties plus `[key: string]: unknown` (with no properties: `Record<string, unknown>`), so the type stays open and exact. Only if the user asks for closed interfaces, omit the index signature and mark each such type `Approximate` | `additionalProperties` defaults to `true` in 3.0; without the index signature a valid fresh literal with an extra key (`{ id: "u", email: "e", extra: 1 }`) fails the excess-property check |
| a `required` name with no entry in `properties` | still a required key: typed `V` when `additionalProperties` is a schema, else `unknown` (`{type: object, required: [id]}` → `{ id: unknown; [key: string]: unknown }`). With `additionalProperties: false` the schema is unsatisfiable: report it and ask | `Record<string, unknown>` alone accepts `{}`, which the schema rejects |
| `additionalProperties: <schema>`, no `properties` | `Record<string, V>`, plus any required names per the row above | |
| `properties` + `additionalProperties: <schema>`, every fixed type assignable to `V` | interface plus `[key: string]: V`, with `\| undefined` added when a fixed property is optional | TS2411, see [Gotchas](#gotchas) |
| `properties` + `additionalProperties: <schema>`, a fixed type not assignable to `V` | interface plus `[key: string]: V \| <fixed types>`, marked `Approximate` | the exact shape is not expressible; the guard enforces it |
| `additionalProperties: false` | plain interface, marked `Approximate`; the guard rejects extra keys | TS types are open structurally (a non-literal value with extra keys compiles), so only the guard closes them |
| `format: date`, `date-time` | `string` | `JSON.parse` yields strings; `Date` would be a lie without a deserializer |
| `format: int64` | `number`; report if ids may exceed 2^53 | `JSON.parse` loses precision past `Number.MAX_SAFE_INTEGER` |
| `format: binary` in `application/octet-stream` or `multipart/*` | `Blob` for browser code; ask for other runtimes | `string` is wrong for raw bytes |
| `not`, or a keyword that changes the accepted shape and has no TS form | the base type, marked `Approximate`; report the keyword | |

**Approximation propagates.** A type is exact only when its own mapping is exact and so is every type it contains: referenced named types, union and intersection members, array items, dictionary values, property types and `Write` projections. One `Approximate` part makes the whole container approximate, whatever the composition. Put the `Approximate` JSDoc on the type where it originates and list each container in the report as "Approximate via <origin>". Exactness is about the JSON shape: schema-only constraints (`pattern`, `minLength`, `minimum`, `maxItems`, `format`) never have a TS form, so they are reported as unchecked instead of making every type approximate.

**Parameters.** Merge path-item and operation parameters by (`name`, `in`); the operation's definition wins. `in: path` is always required; for query, header and cookie `required` defaults to `false`. Keep the wire name as the key, quoted when it is not an identifier (`"X-Request-Id": string`). A header parameter named `Accept`, `Content-Type` or `Authorization` is ignored by the spec: never emit it. A parameter with `content` instead of `schema` uses the schema of its single media type. `style`/`explode` change serialisation, not the type. The `*Params` interfaces list declared parameters, not a Schema Object, so the open-object rule does not apply to them (it does apply to an object-typed parameter's schema).

**Bodies and responses.** `requestBody.required` defaults to `false`: then emit `{Base}RequestBody = X | undefined`. A response with no `content` (a bare `404`, a `204`) gets no type: never alias it to `unknown` or `void`; report "no body documented". A media type with no `schema` (`content: {application/json: {}}`) documents a body of unspecified shape: emit `unknown` for it (still `unknown | undefined` for an optional request body), report "body present, schema undocumented", never infer a shape from `example`/`examples`, and emit no guard for it. The media type decides what the client holds: JSON (`application/json` and `+json` suffixes such as `application/problem+json`) and form bodies (`application/x-www-form-urlencoded`, `multipart/form-data`, whose schema lists the fields) map their schema as usual; `text/*` and `application/xml` map to `string`, reporting that the schema describes the decoded content, not the raw body; any other media type maps to `Blob` per the `format: binary` row. Emit error types only from documented schemas; a schema such as `ApiError` is emitted only when the spec defines it.

## Worked example

Input (condensed):

```yaml
openapi: 3.0.3
info: {title: Users, version: "1"}
paths:
  /users/{id}:
    parameters:
      - {name: id, in: path, required: true, schema: {type: string}}
    get:
      operationId: getUser
      parameters:
        - {name: expand, in: query, schema: {type: string, enum: [teams]}}
        - {name: Authorization, in: header, required: true, schema: {type: string}}
      responses:
        "200": {description: ok, content: {application/json: {schema: {$ref: "#/components/schemas/User"}}}}
        "404": {description: not found}
    put:
      operationId: updateUser
      requestBody:
        required: true
        content: {application/json: {schema: {$ref: "#/components/schemas/User"}}}
      responses:
        "200": {description: ok, content: {application/json: {schema: {$ref: "#/components/schemas/User"}}}}
  /v2/users/{id}:
    get:
      operationId: get_user
      parameters:
        - {name: id, in: path, required: true, schema: {type: string}}
      responses:
        "200": {description: ok, content: {application/json: {schema: {$ref: "#/components/schemas/User"}}}}
components:
  schemas:
    User:
      type: object
      required: [id, email, password]
      properties:
        id: {type: string, readOnly: true}
        email: {type: string}
        nickname: {type: string, nullable: true}
        manager: {$ref: "#/components/schemas/User", nullable: true}
        password: {type: string, writeOnly: true}
```

Output (passes `tsc --strict`; repetitive declarations elided):

```ts
/** Response view. */
export interface User {
  id: string;
  email: string;
  nickname?: string | null;
  /** `nullable: true` beside this `$ref` is ignored in OpenAPI 3.0. */
  manager?: User;
  [key: string]: unknown; // additionalProperties defaults to true
}

/** Request view: readOnly `id` dropped, writeOnly `password` required. */
export interface UserWrite {
  email: string;
  nickname?: string | null;
  manager?: UserWrite;
  password: string;
  [key: string]: unknown;
}

export interface GetUserPathParams { id: string; } // inherited from the path item
export interface GetUserQueryParams { expand?: "teams"; }
export type UpdateUserRequestBody = UserWrite;
export type GetUser2Response200 = User;
// ...plus the remaining PathParams and Response200 types, named the same way.
```

Report:

```text
Output: types/api.ts
Named schemas: 1
Approximate: none
Ignored/unsupported: Authorization header parameter (spec rule; auth comes from securitySchemes); nullable beside the manager $ref (ask whether null was intended)
Renamed: get_user -> GetUser2 (collides with getUser)
Removed/renamed exports: none
No documented body: GET /users/{id} 404; body present, schema undocumented: none
Unchecked constraints: none
Type-check: npx tsc --noEmit --strict --target es2022 types/api.ts, exit 0
```

## Runtime guards

Emit guards only when the user asks for runtime validation or type guards. Then read [references/guards.md](references/guards.md): it owns the guard rules, the code patterns and the mutation tests. Do NOT load it for a types-only request.

## Validation loop

1. Type-check the path chosen in step 4 (`<out>` below). With a repository `tsconfig.json`, first confirm it includes that file: `npx tsc -p tsconfig.json --listFilesOnly | grep -Fx "$(realpath <out>)"` (the list holds absolute paths). If it is listed, run `npx tsc --noEmit -p tsconfig.json`; when that config has `strict` or `strictNullChecks` off, also run the strict standalone check below, because a lax config hides `| null` and optional-property errors that strict consumers hit. If there is no tsconfig or it excludes `<out>`, run `npx tsc --noEmit --strict --target es2022 <out>`, or `npx -p typescript tsc --noEmit --strict --target es2022 <out>` when the repository has no local TypeScript.
2. Fix each error by correcting the mapping decision, never with `any`, `as` casts or `@ts-ignore`, and rerun until it exits 0.
3. If guards were emitted, run the mutation tests from `references/guards.md` and fix every failure.
4. If a check cannot run (no Node, no TypeScript, no network), report "type-check not run: <reason>". Never report generated code as compiling when it was not checked.

## Gotchas

- FastAPI 0.99.0 and later emit `openapi: 3.1.0` by default (its release notes: "Upgrade OpenAPI 3.1.0, this uses JSON Schema 2020-12"), so a FastAPI `/openapi.json` hits the 3.1 stop. Read the version line; never assume 3.0 from the generator's name. Editing only the version string does not make the document 3.0: the schemas keep their 3.1 shapes. Ask for a document that really is 3.0.
- An interface with an optional fixed property and an index signature fails with TS2411 (`Property 'note' of type 'string | undefined' is not assignable to 'string' index type 'string'`) unless the index type includes `| undefined` or the project sets `exactOptionalPropertyTypes`.
- Node's type stripping (`node file.ts`, used for the guard mutation tests) rejects `enum` with `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`: TypeScript enum is not supported in strip-only mode.

## NEVER

- NEVER fold readOnly and writeOnly into one type for both directions: clients are then forced to send `id` and responses are typed as containing `password`.
- NEVER honour a sibling of `$ref` in 3.0 silently: tools disagree, so the contract changes depending on the generator; report it and ask.
- NEVER substitute `unknown` for an unresolved ref without the user's consent: callers believe the contract is complete.
- NEVER rename a query, header or cookie key to camelCase: the type then describes a parameter the server does not read.
- NEVER mark an approximate type as exact: users rely on the compiler for what it cannot check.
- NEVER emit a TS `enum` for a spec `enum`; emit a literal union. A string `enum` is nominal, so a parsed `"active"` payload is not assignable to it, it emits runtime code, and Node's type stripping rejects it (see [Gotchas](#gotchas)).
