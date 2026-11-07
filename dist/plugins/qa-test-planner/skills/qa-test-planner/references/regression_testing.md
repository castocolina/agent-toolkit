# Regression Testing

How to select a regression or smoke suite from a change, keep its results trustworthy, and record the release decision. Ordering follows the precedence in SKILL.md section 5.

## Select scope by change

1. List what changed (tickets, commits, config, dependency bumps) and, for each, the behavior it touches.
2. Add the direct dependencies and the integration boundaries each change crosses (an API, a queue, a payment provider).
3. Widen to every critical journey when the impact is broad, ownership of a dependency is unclear, or a shared component (auth, checkout, a design-system token) changed.
4. Smoke first: the few P0 checks that prove the build is testable at all. The default smoke set is the cases the catalog or suite marks `SMOKE-`, in ID order; a product with no smoke cases uses the SKILL.md section 5 precedence until the first non-smoke case. When the requester supplies no catalog and no `SMOKE-` cases, write the smoke set as `Unknown`, name its owner under Open Questions, and keep one Blocked smoke check per critical journey instead of inventing `SMOKE-` IDs. If smoke fails, stop and report; later results on a broken build are noise.
5. Fit the time box: order by the SKILL.md precedence, run down the list, and list every case that did not fit as residual risk with its owner. A cut case is never reported as passing.

## Suite tiers

Pick the tier from the change and the scope above. Durations are placeholders: replace them with the team's measured times, and never present them as targets.

| Tier | Purpose | When (default cadence) | Coverage | Duration (example) |
| :- | :- | :- | :- | :- |
| Smoke | Quick check that the build is testable | Every build, before detailed testing (daily at least) | Critical user paths, core functionality, system health, build stability | 15-30 min |
| Targeted | Test the impacted areas | After a specific change | Modified feature area, related components, integration points, dependent functionality | 30-60 min |
| Full | Comprehensive validation | Before a release, weekly as a default | All functional cases, integration scenarios, UI validation, data integrity, security checks | 2-4 hours |
| Sanity | Quick validation of a fix | After a hotfix | The fixed behavior and its direct neighbors | 10-15 min |

A hotfix or a single fix uses the sanity tier; targeted, full and smoke stay as the table's When column says, and SKILL.md section 5 precedence still orders the cases inside the chosen tier.

Smoke suite example (the `SMOKE-` prefix), to adapt to the product:

```text
SMOKE-001: A seeded user can sign in
SMOKE-002: The user can reach the main features
SMOKE-003: Critical API endpoints respond
SMOKE-004: The data store answers a seeded read
SMOKE-005: The user can complete the primary action
SMOKE-006: The user can sign out
```

Those six IDs illustrate the shape only; when the requester supplies no catalog and no `SMOKE-` cases, follow the smoke step and write the smoke set as `Unknown` instead of copying them.

## Build the suite

1. **Identify critical paths.** A journey is critical when the answer to any of these is yes:
   - What can users not live without?
   - What generates revenue?
   - What handles sensitive data?
   - What is used most often?
   Step 3 of the scope rule widens to "every critical journey"; this list defines it.
2. **Prioritize** by the SKILL.md section 5 precedence. How often each priority runs is a default the team's own cadence overrides:

   | Priority | Run |
   | :- | :- |
   | P0 | Every build |
   | P1 | Daily or weekly |
   | P2 | Weekly or at release |
   | P3 | At release only |

3. **Order the run.** Smoke first, and stop on a smoke failure; then the SKILL.md precedence (P0 first), tracking every failure; then, if time remains, an exploratory pass: unscripted, time-boxed, reporting what it finds as new cases or bugs, never as a pass of a listed case.

## Keep results valid

- **Visual comparisons:** match viewport, device-pixel ratio, theme, fonts, content and color profile to the reference before counting a difference (SKILL.md routes the full procedure).
- **Intermittent failures:** keep the first failure's evidence and environment. Rerun under the same conditions to measure the rate (3/10). Never turn a failure into a pass by retrying until green, and never label it flaky without evidence that the product is not at fault; track product defects and test or environment instability separately.
- **Environment drift:** record the build, data snapshot and feature flags for the run; a pass against a different flag set says nothing about the release.

## Release decision

The release gate and its single waiver exception are defined in SKILL.md section 3, step 4. A waiver record holds:

- the failing case and its evidence,
- the owner's name and role,
- the rationale and the affected scope,
- the mitigation or workaround, with who applies it,
- the follow-up: ticket, owner and date, and when the waiver expires.

A waiver does not erase the failure: the run report still shows it as failing. Security and data-loss failures get no other exception.

## Run report

- Build, environment, feature flags, and the visual conditions matched.
- Selected scope and why; cases cut for time, listed as residual risk.
- Pass / fail / blocked per case, each with linked evidence.
- Intermittent failures with their measured rate.
- Unresolved risks and their owners.
- Release decision, with the waiver record when one exists.

### Run report template

Counts are a summary of the per-case results, never the gate: the release decision comes from the release gate (SKILL.md section 3, step 4), so no pass-rate row decides anything. Values in brackets are placeholders.

```markdown
# Test Run: [release]

**Date:** YYYY-MM-DD   **Build:** [vX.Y.Z or commit]   **Tester:** [name]   **Environment:** [staging / Unknown]
**Feature flags / data snapshot:** [values]   **Visual conditions matched:** [viewport, DPR, theme / n/a]

## Summary
Total [n]  Executed [n]  Passed [n]  Failed [n]  Blocked [n]  Not run / cut for time [n] (listed as residual risk)

## By priority
| Priority | Total | Pass | Fail | Blocked | Not run |
| :- | :- | :- | :- | :- | :- |
| P0 | [n] | [n] | [n] | [n] | [n] |
| P1 | [n] | [n] | [n] | [n] | [n] |
| P2 | [n] | [n] | [n] | [n] | [n] |
| P3 | [n] | [n] | [n] | [n] | [n] |

## Per case
| Case | Result | Evidence | Bug |
| :- | :- | :- | :- |
| TC-AREA-NNN | Pass / Fail / Blocked | [link to screenshot, request ID, order ID] | BUG-NNN / none |

## Critical failures
- TC-AREA-NNN: [what failed] | Bug: BUG-NNN | Status: [open / in progress] | Impact: [users, money, data] | Fix date: [YYYY-MM-DD or Unknown]

## Blocked cases
- TC-AREA-NNN: [missing prerequisite] | Owner: [name or Unknown]

## Intermittent failures
- [case]: [measured rate, n/10]

## Risks
- [unresolved risk] | Owner: [name or Unknown]

## Release decision
[Block / Ship / Ship under waiver] per the release gate; waiver record: [fields above, or none]

## Next steps
- Retest after [BUG-NNN] is fixed
- Run the cases still not run, or accept them as residual risk in writing
- Final smoke on the release build before deployment
```

A filled example of the Critical failures block, with illustrative values:

```markdown
- TC-PAY-001: Card payment fails for one card brand | Bug: BUG-NNN | Status: in progress | Impact: part of card payments blocked (measure the share from the ledger; do not estimate) | Fix date: YYYY-MM-DD
- TC-AUTH-045: Session expires early | Bug: BUG-NNN | Status: under investigation | Impact: users signed out unexpectedly
Decision: Block. The payment failure is a P0, so the gate blocks release; ship only with a waiver from its authorized release-risk owner.
```

## Coverage tracking

Keep a matrix that shows gaps, not only counts. Traceability per ID (SKILL.md section 2) is the source; the matrix is its summary by feature.

```markdown
| Feature | Requirements | Cases | Status | Gaps |
| :- | :- | :- | :- | :- |
| [feature] | [n] | [n] | Complete / Partial | [uncovered requirement, or none] |
```

## Regression checklist

Before execution:
- [ ] Test environment ready and build deployed (ID recorded)
- [ ] Test data seeded
- [ ] Previously fixed bugs verified as fixed
- [ ] Suite reviewed and updated for this release

During execution:
- [ ] Follow the run order above
- [ ] Document every failure, with a screenshot or recording
- [ ] Note unexpected behavior
- [ ] Track blockers, each with an owner

After execution:
- [ ] Compile results (the run report above)
- [ ] File the new bugs
- [ ] Update the cases
- [ ] Report to stakeholders
- [ ] Archive the artifacts
