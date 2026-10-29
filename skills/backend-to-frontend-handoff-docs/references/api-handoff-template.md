# API Handoff: [Feature]

## Business context
[Problem, users, essential domain terms]

## Endpoints
### [METHOD] [path]
- Purpose / auth:
- Request (wire names, required/optional/null semantics):
- Success status and response:
- Errors (status, stable discriminator/body, condition):
- Constraints / transitions / retry safety:

## Models and enums
[Only client-visible types, nullability, wire names, meanings]

## Integration behavior
[Pagination/order consistency, cache invalidation, real-time updates, reconciliation]

## Client scenarios
1. Success
2. Validation or conflict
3. Authorization/not-found as applicable
4. Timeout/retry or uncertain transition as applicable

## Open questions
[Unverified or unresolved behavior]
