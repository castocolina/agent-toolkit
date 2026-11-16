# API Handoff: [Feature]

## Business context
[Problem, users, essential domain terms]

## Endpoints
### [METHOD] [path]
- Purpose / auth:
- Request (wire names, required/optional/null semantics):
- Example request and success payloads (real values from the code or the supplied contract, never placeholders):
- Success status and response:
- Errors (status, stable discriminator/body, condition):
- Validation rules the UI should mirror (required, min and max, formats, conditional rules; only what the backend enforces):
- Constraints / transitions / retry safety:
- Rate limits (only when the code or contract defines them): the limit, the 429 Too Many Requests response and whether it carries Retry-After (RFC 6585 section 4; Retry-After is a number of seconds or an HTTP-date, RFC 9110 section 10.2.3; checked 2026-11-15):

Document the status code the handler actually returns for each failure. RFC 9110 names 422 Unprocessable Content (well-formed request, instructions cannot be processed, section 15.5.21) and 409 Conflict (conflict with the current state of the resource, section 15.5.10); checked 2026-11-15.

## Models and enums
[Only client-visible types, nullability, wire names, meanings]

Enum display labels: include them only when the backend defines them; never invent labels.

## Integration behavior
[Pagination/order consistency, cache invalidation, real-time updates, reconciliation]

Recommended call flow: the order of calls the backend requires or supports (for example fetch, then submit, then refetch); omit when the code shows no required order.

Cache behavior only when the code sets or relies on it: validators (ETag, Last-Modified; RFC 9110 section 8.8) and invalidation of stored responses after an unsafe method (RFC 9111 section 4.4); checked 2026-11-15.

## Client scenarios
1. Success
2. Validation or conflict
3. Authorization/not-found as applicable
4. Timeout/retry or uncertain transition as applicable

## Assumptions and trade-offs
[Assumptions or trade-offs the backend made that the client should know about; omit when none]

## Open questions
[Unverified or unresolved behavior]
