# Bug Report Templates

One base template, the extra fields each bug type needs, and how to set severity and priority. Write `Unknown` for any fact the reporter did not give.

## Base template

```markdown
# BUG-[ID]: [Area] [what fails] when [trigger]

**Severity:** Critical | High | Medium | Low | Untriaged
**Priority:** P0 | P1 | P2 | P3 | Untriaged
**Type:** Functional | UI | Performance | Security | Data | Crash
**Status:** Open
**Reporter:** [name]  **Reported:** YYYY-MM-DD

## Environment
- OS: [Windows 11 / Unknown]
- Browser: [Chrome 120 / Unknown]
- Device: [Desktop / iPhone 15 / Unknown]
- Build: [v2.5.0 or commit / Unknown]
- Environment: [Production / Staging / Dev / Unknown]
- URL: [exact page]

## Steps to Reproduce
Preconditions: [account, seeded data, feature flags]
1. [action with exact input]
2. [action]
Reproduction rate: [3/10 attempts / 1 occurrence, not yet reproduced / Unknown]

## Expected Behavior
[what should happen, observable]

## Actual Behavior
[what happens, with the exact message]

## Evidence
- Screenshot or recording: [attached / none]
- Console errors: [paste / Unknown]
- Failed requests: [method, URL, status / Unknown]

## Impact
- Users affected: [all / role / segment / Unknown]
- Data impact: [lost / corrupted / none / Unknown]
- Workaround: [describe / none / Unknown]

## Context
- Regression: [Yes since vX / No / Unknown]
- Related: [test case, feature, similar bug]

## Open Questions
- [each Unknown above that the fixer needs]
```

A good title names the area, the failing behavior and the trigger: "[Checkout] Cart total shows $0 when a discount code is applied twice". "Checkout broken" or "Please fix ASAP" gives triage nothing to sort by.

## Extra fields by type

| Type | Add | Why it matters |
| :- | :- | :- |
| UI / visual | Figma frame link and version, viewport, theme, device-pixel ratio, measured value vs design value | Without matching conditions the mismatch may be the comparison, not the product |
| Performance | Metric, expected vs actual with percentile (p95, not average), data size, network profile, baseline build | An average hides the slow tail; a different data size makes the baseline meaningless |
| Security | Vulnerability class, affected data, how to verify without a working exploit, disclosure owner | A public tracker with a payload or a live token turns the report into the attack |
| Crash / error | Exact error text, stack trace, logs before the crash, whether data was lost, whether the app recovers on restart | Recoverability and data loss set the severity, not the word "crash" |

Before attaching evidence, redact it: HAR files and console logs carry cookies, bearer tokens and personal data.

## Severity: set by impact, not by symptom

| Severity | Criteria |
| :- | :- |
| Critical | Data loss or corruption, security breach, money charged wrongly, or a crash with no recovery path |
| High | A core journey is blocked with no workaround, or a crash that loses the user's unsaved work |
| Medium | A feature fails partly and a workaround exists; a crash that recovers with no data lost |
| Low | Cosmetic or copy issue with no functional effect |

Classify a crash by what it costs (data, recovery), never by how often it happens: a rare crash that corrupts an order is still Critical. Record the reproduction rate separately; it feeds priority, not severity.

Response-time targets (for example Critical within 4 hours) are organization policy. Use the requester's if given; otherwise leave them out rather than present an example as a rule.

## Priority: severity adjusted by rate and exposure

Start from severity, then raise or lower one step for how often and how widely it hits. This grid is an illustrative default, not policy:

| Rate \ Severity | Low | Medium | High | Critical |
| :- | :- | :- | :- | :- |
| 1 occurrence, not reproduced | P3 | P3 | P2 | P1 |
| Intermittent (1/10 to 5/10) | P3 | P2 | P1 | P0 |
| Most attempts (6/10 or more) | P2 | P1 | P0 | P0 |
| Unknown (intermittent, not measured) | P3 | P2 | P1 | P0 |

With an Unknown rate the priority comes from impact alone: mark it provisional (`P1 (provisional)`), write the rate as `Unknown`, and ask for it under Open Questions (with the script, pass the grid value to `--priority` and say "priority provisional, rate Unknown" in `--description`); re-triage once a safe rerun measures it.

Exception to the grid: a security or data-loss bug starts at P0 at any rate, including a single unreproduced occurrence; only its owner may downgrade it, in writing.
