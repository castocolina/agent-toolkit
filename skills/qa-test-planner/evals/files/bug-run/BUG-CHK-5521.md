# BUG-CHK-5521: [Checkout] Double order and charge when Pay is clicked twice

**Severity:** Critical
**Priority:** P0
**Type:** Unknown
**Status:** Open
**Reported:** 2026-11-03
**Reporter:** Unknown

---

## Environment

- **OS:** Unknown
- **Browser:** Unknown
- **Device:** Unknown
- **Build:** 2.4.0-rc2
- **URL:** Unknown

---

## Description

Clicking Pay twice quickly can create two orders and two charges; reproduced on staging in 2 of 10 attempts; support ticket #5521

---

## Steps to Reproduce

1. Add one item to the cart
2. Go to checkout
3. Click Pay twice quickly


---

## Expected Behavior

One order and one charge

---

## Actual Behavior

In 2 of 10 attempts, two orders and two charges

---

## Visual Evidence

- [ ] Screenshot attached
- [ ] Screen recording attached
- [ ] Console logs attached

**Console Errors:**
```
Unknown (whether console errors were observed)
```

---

## Impact

- **Reproduction rate:** 2/10
- **User Impact:** Unknown
- **Workaround:** Unknown (whether a workaround exists)

---

## Additional Context







**Is this a regression?** Unknown

---

## Root Cause

[To be filled by developer]

---

## Fix

[To be filled by developer]

---

## Verification

- [ ] Bug fix verified in dev environment
- [ ] Regression testing completed
- [ ] Related test cases passing

**Verified By:** ___________
**Date:** ___________

---

## Open Questions

- Type: Unknown
- Reporter: Unknown
- OS: Unknown
- Browser: Unknown
- Device: Unknown
- URL: Unknown
- Console errors: Unknown
- User impact: Unknown
- Workaround: Unknown
- Regression: Unknown

