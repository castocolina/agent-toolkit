# Release 2.4 - change list and regression catalog

Regression window: 2 hours of manual testing, one tester, staging only.

## Changes in 2.4

- PAY-311: payment provider SDK upgraded from 5.2 to 6.0 (card charge and refund calls).
- PROF-88: profile page avatar crop dialog redesigned (frontend only).
- CART-140: cart now merges guest cart into account cart on login.

## Regression catalog (estimated minutes)

| ID | Case | Area | Minutes |
| :- | :- | :- | :- |
| SMOKE-001 | Login with a seeded account | auth | 5 |
| SMOKE-002 | Add item to cart and reach checkout | cart | 5 |
| TC-PAY-001 | Card charge creates exactly one order and one charge | payment | 15 |
| TC-PAY-002 | Full refund returns money and marks the order refunded | payment | 20 |
| TC-PAY-003 | Declined card creates no order | payment | 10 |
| TC-CART-004 | Guest cart merges into account cart on login | cart | 15 |
| TC-CART-005 | Merged cart keeps the higher quantity for duplicate items | cart | 10 |
| TC-PROF-006 | Avatar crop dialog matches the new design | profile | 20 |
| TC-PROF-007 | Avatar upload rejects files over 5 MB | profile | 10 |
| TC-SRCH-008 | Search returns results for a known product | search | 10 |
| TC-NOTIF-009 | Order confirmation email is sent once | notifications | 15 |
| TC-I18N-010 | German locale renders checkout labels | i18n | 15 |
