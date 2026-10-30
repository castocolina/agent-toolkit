---
name: backend-to-frontend-handoff-docs
description: "Create frontend integration handoffs from completed backend endpoints, DTOs, validation, auth rules, and behavior. Use when backend work is ready for web or mobile clients and the user asks for a handoff, request/response contract, integration errors, or edge cases. Not for designing unimplemented APIs, frontend UI implementation, or public developer-portal references."
---

# Backend-to-Frontend Handoff

Document the wire contract the client must rely on, including failure and transition semantics. Do not infer behavior from names or intended design.

## Trace before drafting

When source files or repository access are unavailable, state that the contract is unverified and make a useful prompt-grounded handoff anyway: preserve supplied facts, mark unknown fields TBD, and give a concrete response example only from stated facts. Never infer authentication requirements, read/write semantics, validation, or business rules from endpoint names or labels. Facts the request states (for example “missing ID is 404” or “public”) are supplied contract facts: document them as stated, such as `404 — no record matches the ID`, and mark only the genuinely unspecified details (error body shape, headers) TBD.

For every endpoint, follow this sequence and resolve discrepancies before writing:

1. Route declaration → actual handler, method, path, and middleware.
2. Auth/authorization declarations → public status, scopes, and object-level checks.
3. Request validation/deserialization → accepted values, defaults, coercions, nullability.
4. Service/domain transition → state preconditions, irreversible effects, idempotency, concurrency behavior.
5. Response serializer → exact wire field names, omission vs `null`, status codes, pagination envelope.
6. Error mapping → reachable status codes and serialized discriminator/body.

Trace the handler before documenting any endpoint. Read serializers rather than copying DTO property names from memory. Errors drive client recovery: record them first, then success shapes, then derive client scenarios from known outcomes.

## Contract decisions that are easy to miss

- **Omitted vs `null`:** document whether omission means unchanged/default and null means clear, or whether serialization collapses them. They are not interchangeable.
- **Mutation retries:** say retry-safe only with explicit idempotency key, deduplication, or proven idempotent transition. A timeout does not prove the mutation failed.
- **Irreversible transitions:** specify terminal states and how the client reconciles uncertain outcomes. Do not recommend optimistic UI without rollback/refetch or authoritative reconciliation behavior.
- **Pagination:** identify cursor/offset semantics, ordering stability, and whether concurrent inserts can duplicate/skip items. Do not promise snapshot consistency without evidence.
- **Errors:** capture status plus stable machine discriminator and whether messages/field errors are safe to branch on. Distinguish validation, authorization, conflict, and transient failures.
- **Caching:** identify cache headers/validators and mutation invalidation effects; do not invent client cache policy from endpoint shape.

NEVER infer retry safety for mutations without implementation evidence. NEVER suggest optimistic UI for irreversible transitions without reconciliation. NEVER equate omitted and null fields without checking serializer semantics.

## Output and destination

Use `.claude/docs/ai/<feature>/api-handoff.md`; if the repository has no `.claude/`, use `docs/handoffs/<feature>/api-handoff.md`. Honor an explicitly requested destination. For updates, increment a version only if the existing convention does so; inspect existing files first. A simple CRUD endpoint still includes every confirmed integration fact: method/path, auth/public status, valid examples, success status, known error codes/shapes, and constraints. Omit only inapplicable sections, never known facts.

Read [the compact template](references/api-handoff-template.md) when drafting. Keep internal implementation paths/classes out unless they affect client integration. Resolve unknowns as explicit TBDs; do not fabricate. Preserve stated auth labels such as “public” exactly, but do not extrapolate them into claims about whether credentials are required or accepted unless the contract says so.

## Final verification

Check every documented claim against the traced source. Ensure omission/null, auth, errors, retry and transition safety, pagination, and cache claims are evidence-backed. Include the error scenarios that frontend must handle. Deliver the file and a brief path confirmation; answer questions normally rather than suppressing chat.
