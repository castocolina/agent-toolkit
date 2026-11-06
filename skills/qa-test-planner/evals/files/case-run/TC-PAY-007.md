# TC-PAY-007: Declined card creates no order

**Priority:** P0 (Critical)
**Type:** Functional
**Requirement:** REQ-PAY-7
**Risk:** A declined payment still creates an order
**Status:** Not Run
**Estimated Time:** Unknown
**Created:** 2026-11-03

---

## Objective

A declined card leaves no order or charge



---

## Preconditions

- Seeded account qa+decline@example.test with one item in the cart


---

## Test Steps

1. Pay with the sandbox decline card
   **Expected:** Decline message shown; order list unchanged



---

## Test Data

The sandbox decline card

---

## Cleanup

- Empty the cart of qa+decline@example.test


---

## Edge Cases & Variations

None recorded

---

## Related Test Cases

None

---

## Execution History

| Date | Tester | Build | Result | Notes |
|------|--------|-------|--------|-------|
| | | | Not Run | |

---

## Notes



---

## Open Questions

- Estimated time: Unknown

