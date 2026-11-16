# Test Case Examples

Two complete cases in the base format of `references/test_case_templates.md`: a functional login case and a responsive UI case. They show what "observable, seeded, cleaned up" looks like. All data is seeded test data: write no real address and no password in a case (keep the password in the team's test-data store and cite it by name).

## Functional: valid login

```markdown
## TC-LOGIN-001: Valid user lands on the dashboard when signing in

**Priority:** P0   **Type:** Functional
**Requirement:** [REQ-ID or R1]   **Risk:** A valid user cannot sign in or lands in the wrong session
**Status:** Not Run   **Estimated time:** [minutes / Unknown]

### Objective
Verify that a user with valid credentials signs in and reaches the dashboard.

### Preconditions
- Seeded account qa+login@example.test, display name [seeded name], active, not signed in; its password is the test-data store entry "login-seed", not written here
- Browser cookies cleared; build: [vX.Y.Z]; environment: [staging]

### Steps
1. Open the login page ([base URL]/login)
   **Expected:** The login form shows an email field and a password field
2. Enter the seeded email
   **Expected:** The field accepts the input
3. Enter the seeded password
   **Expected:** The characters are masked
4. Click "Login"
   **Expected:**
   - A loading indicator appears
   - The browser lands on /dashboard
   - The welcome message names the seeded display name
   - The avatar or profile image shows in the header

### Test Data
| Field | Value | Why this value |
| :- | :- | :- |
| email | qa+login@example.test | seeded account for this case only |
| password | test-data store entry "login-seed" | valid credential, never committed |

### Post-conditions
- A session exists for the seeded account (the session cookie is set)
- The sign-in event is recorded where the team's analytics or audit view shows it, or this check is `Blocked` with its owner

### Cleanup
- Sign out and clear cookies, so a rerun starts signed out

### Evidence
- Screenshot of the dashboard, the request ID of the sign-in call

### Edge cases and variations (each its own case)
| Case | Variation | Expected result |
| :- | :- | :- |
| TC-LOGIN-002 | Invalid password | Refused with the generic message; no session |
| TC-LOGIN-003 | Unknown email | The same message and status as TC-LOGIN-002 (no account enumeration) |
| TC-LOGIN-004 | Injection string in the email field, such as `' OR '1'='1` | Rejected as invalid input; no session; no error detail leaks |
| TC-LOGIN-005 | Password at and beyond the documented maximum length | Accepted at the limit, refused beyond it, as the requirement states |
```

## UI: mobile navigation menu

```markdown
## TC-UI-045: Mobile navigation menu opens and matches the design

**Priority:** P1   **Type:** UI / Responsive
**Figma:** [exact frame link, version or last-edited date]
**Requirement:** [REQ-ID or R1]   **Risk:** The menu is unreachable or off-design on a phone

### Objective
Verify that the navigation menu works on phone viewports and matches the frame.

### Preconditions
- Responsive mode or a device at each viewport below, device-pixel ratio [1 / 2 / 3] recorded, theme [light], locale [en]
- Viewports (examples; use the breakpoints and devices the design defines): [375 px], [390 px], [428 px], [360 px]
- Build: [vX.Y.Z]; seeded content that matches the frame's content

### Steps
1. Open the homepage at the first viewport
   **Expected:** The hamburger icon is visible at the top right
2. Tap the hamburger icon
   **Expected:** The menu slides in from the right; an overlay covers the content; a close (X) button is visible
3. Tap a menu item
   **Expected:** The page navigates to that section and the menu closes
4. Measure the open menu in DevTools (computed styles) against the frame
   **Expected:** Each value equals the design value within the tolerance agreed for this run:
   - Menu width: [design value, e.g. 280 px]
   - Slide animation: [duration and easing, e.g. 300 ms ease-out]
   - Overlay: [opacity and color, e.g. 0.5 black]
   - Font: [size and line height, e.g. 16 px / 24 px]
5. Repeat steps 1-4 at each remaining viewport
   **Expected:** The same behavior and values, or a recorded difference in the discrepancy table (`references/figma_validation.md` section 4)

### Cleanup
- Close the menu; reset the viewport and any forced state

### Evidence
- A screenshot per viewport with its width and DPR in the file name; the measured values table
```

The numbers in square brackets and after "e.g." are example design values: take the real ones from the frame, with its version, and record the tolerance you agreed.
