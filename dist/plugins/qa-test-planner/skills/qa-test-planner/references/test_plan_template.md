# Test Plan Template

The fuller plan document. SKILL.md section 3 sets the shape every plan has (Requirements, Scope, Risks, Environments, Schedule, Exit gates, Residual risk, Open Questions); this file adds the sections a full plan document carries around it and a worked example. Every `Unknown` rule of SKILL.md section 2 still applies: a fact the requester did not give is written `Unknown` and repeated under Open Questions.

## Sections added around the SKILL.md shape

```markdown
# Test Plan: [Feature or release]

## Executive summary                        (before Requirements)
- Feature or release under test
- Testing objectives: the decision this plan supports (ship, block, retest)
- Key risks: the K IDs that matter most
- Timeline overview: [window / Unknown]

## Requirements ... Scope                   (SKILL.md shape)

## Test types and approach                  (after Scope)
Types, as the change needs: manual, exploratory, regression, integration, user acceptance.
Approach: black box; positive and negative cases; boundary value analysis; equivalence partitioning.

## Environments                             (SKILL.md shape; list each of these)
- Operating systems, browsers and versions, devices (mobile, tablet, desktop)
- Test data requirements (seeded accounts and records, per SKILL.md section 6)
- Backend and API environments, and the build under test

## Entry criteria                           (after Environments)
- [ ] Requirements documented
- [ ] Designs finalized (a Figma frame link and version when the change is visual)
- [ ] Test environment ready
- [ ] Test data seeded
- [ ] Build deployed, with its ID recorded

## Risks                                    (the SKILL.md K lines, as a table)
| ID | Failure mode | Probability (H/M/L) | Impact (H/M/L) | Mitigation | Cases | Owner |
| :- | :- | :- | :- | :- | :- | :- |
| K1 | [failure mode] | [H/M/L or Unknown] | [H/M/L or Unknown] | [mitigation] | TC-.. | [name or Unknown] |

## Schedule ... Exit gates ... Residual risk ... Open Questions   (SKILL.md shape)

## Deliverables                             (end)
Test plan, test cases, run reports, bug reports, test summary report.
```

- A criterion not met when testing starts turns the cases that depend on it into `Blocked`, each with an owner, as SKILL.md section 3 step 1 does for unknown scope. Never start executing as if it were met.
- Probability and impact are the requester's call or come from evidence (incident history, change size). Without either, write `Unknown`; never fill H/M/L to complete the table.

## Exit gates

Write the release gate of SKILL.md section 3, step 4, as the checklist below. Never add a pass-rate threshold: a percentage can hide the one P0 failure (SKILL.md section 6).

- [ ] Every critical requirement has an executed, passing case
- [ ] No P0 failure is open, or each one has a waiver that meets the gate
- [ ] Each blocked case has an owner
- [ ] Plan exit check (not part of the release gate of section 3, step 4): the regression tier the plan selected has run (smoke at minimum; tiers in `references/regression_testing.md`)

## Plan checklist

- [ ] Scope is defined, in and out, each exclusion with its evidence
- [ ] Entry criteria and exit gates are specified
- [ ] Risks are identified with mitigations and covering cases
- [ ] The schedule fits the environments and time available (SKILL.md section 3, step 5)

## Worked example: authentication feature

Request: "Create a test plan for the user authentication feature."

Facts the requester gave: login, registration and password reset in the web app. Facts not given: mobile apps, third-party sign-in, browsers and devices, dates, who accepts risk. The plan therefore carries those as `Unknown`, each with an owner and a smoke check, instead of assuming them.

```markdown
# Test Plan: User authentication

## Executive summary
- Under test: login, registration, password reset (web app)
- Objective: decide whether the authentication change can ship
- Key risks: K1 reset link reused or used late; K2 an unknown address is distinguishable from a known one
- Timeline: Unknown (owner: release manager)

## Requirements
R1: A valid user signs in. R2: A reset link works once and expires. R3: Registration rejects a duplicate address.

## Scope
In: login, registration, password reset (change: AUTH ticket)
Out: none excluded without evidence
Unknown: mobile apps, third-party sign-in (owner: product owner; question: do they change in this release?; smoke check: one sign-in per path, or Blocked)

## Test types and approach
Manual and exploratory; security checks for K1 and K2; positive and negative cases with boundary values (the link at both sides of its expiry).

## Entry criteria
[ ] Requirements documented  [ ] Designs finalized  [ ] Environment ready  [ ] Seeded accounts  [ ] Build deployed (ID: Unknown)

## Risks
| ID | Failure mode | Probability | Impact | Mitigation | Cases | Owner |
| K1 | Reset link usable after expiry or twice | Unknown | H | Controlled-clock cases on both sides of the boundary; reuse case asserts the password is unchanged | TC-AUTH-004, TC-AUTH-005 | Unknown |
| K2 | Unknown address answered differently | Unknown | M | Same message and status for known and unknown input | TC-AUTH-006 | Unknown |

## Exit gates
[ ] Every critical requirement has an executed, passing case  [ ] No open P0 or a waiver that meets the gate  [ ] Each blocked case has an owner  [ ] Smoke tier run

## Open Questions
Browsers and devices; third-party sign-in; mobile apps; dates; probability for K1 and K2; the release-risk owner.
```

Replace every placeholder with the requester's facts; the example shows the structure, not values to copy.
