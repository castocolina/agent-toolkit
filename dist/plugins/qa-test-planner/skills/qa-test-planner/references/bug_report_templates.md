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

## Fields for tracking and fixing

Add these to the base template when the team tracks a bug through a fix, or when the tracker has the fields. Write `Unknown` for what the reporter does not know; never guess a version or an assignee.

```markdown
**Status:** Open | In Progress | In Review | Fixed | Verified | Closed
**Assignee:** [developer / Unassigned]

## Evidence (additions)
- Before state: [screenshot / none]   After state: [screenshot / none]   Error message: [screenshot / none]
- Video recording: [link / none]
- Network errors: [method, URL, status / Unknown]

## Impact (addition)
- Business impact: [revenue, support load, user trust, contractual / Unknown]

## Context (additions)
- Last working version: [vX.Y.Z / Unknown]
- First broken version: [vX.Y.Z / Unknown]
- Related: [feature ticket, test case, similar bug]

## Developer section (filled by the developer)
- Root cause: [after investigation]
- Fix description: [approach]
- Files changed: [paths]
- Fix PR: [link]

## QA verification
- [ ] Fix verified in dev
- [ ] Fix verified in staging
- [ ] Regression cases passed
- [ ] Related cases updated
- [ ] Ready for production
**Verified by:** [name]   **Date:** YYYY-MM-DD   **Build:** [vX.Y.Z or commit]
```

Keep the reproduction rate as measured (`3/10`, `1 occurrence, not yet reproduced`, `Unknown`): the lifecycle fields never replace it with "Always".

## Quick template

For a minor issue, when the environment and steps are short. Anything with unknown rate, data impact or security relevance uses the base template instead.

```markdown
# BUG-[ID]: [Area] [what fails] when [trigger]

**Severity:** Low | Medium | Untriaged
**Environment:** [browser, OS, build / Unknown]

## Issue
[one paragraph]

## Steps
1. [step]
2. [step]

## Expected
[what should happen]

## Actual
[what happens]

## Screenshot
[attached / none]
```

## Security bug template

Extends the base template for a vulnerability. Keep it out of any public tracker; the class, the affected data, the safe verification and the disclosure owner of the security row above still apply.

```markdown
# BUG-[ID]: [Security issue title]

**Type:** Security
**OWASP category:** [category name, with the edition stated / Unknown]
**CONFIDENTIAL - DO NOT SHARE PUBLICLY**

## Vulnerability
**Class:** [XSS / injection / authentication bypass / broken access control / other]
**Risk level:** Critical | High | Medium | Low | Untriaged
**Exploitability:** Easy | Moderate | Difficult | Unknown

## Description
[Describe the vulnerability without exploit code, live tokens or real user data]

## Impact
- [ ] Data exposure
- [ ] Privilege escalation
- [ ] Account takeover
- [ ] Service disruption
- [ ] Other: [specify]
**Affected data:** [personal data / payment data / credentials / Unknown]

## How to verify
[Safe verification on a dedicated test account, sanitized; never a working exploit]

## Recommended fix
[High-level remediation, or Unknown]

## References
- [CVE, if one applies]
- [OWASP reference]

## Disclosure
- Internal report date: YYYY-MM-DD
- Expected fix date: [YYYY-MM-DD / Unknown]
- Public disclosure: [N/A / date]   Disclosure owner: [name / Unknown]
```

OWASP category ids belong to one edition of the list. Name the edition with the id, for example OWASP Top 10:2025 (https://top10.owasp.org/2025, checked 2026-11-07), or the edition the team follows; if you cannot say which one applies, write `Unknown` and tell the user to read the live list at https://top10.owasp.org. Never write an id without its edition.

Severity and priority still follow the sections below: a security or data-loss bug starts at P0 at any rate, and the risk level above does not replace the severity.

## Pre-submit checklist

- [ ] The title names the area, the behavior and the trigger
- [ ] Someone else can reproduce it from the steps (preconditions included)
- [ ] Expected and actual are stated, with the exact message
- [ ] The environment is complete, each gap written `Unknown`
- [ ] Evidence is attached and redacted
- [ ] Severity (by impact) and priority (by the grid below) are set, or `Untriaged`
- [ ] Duplicates were checked
- [ ] Related items (cases, features, similar bugs) are linked

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
