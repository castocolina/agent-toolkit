# Regression Testing

## Select scope by change risk

Run targeted regression on changed behavior, its dependencies, and integration boundaries. Expand to critical paths when impact is broad, dependency ownership is unclear, or release risk warrants it. Run smoke checks before the selected suite; stop and investigate if a smoke failure invalidates later results. Prioritize by user/business impact and data/security consequences, not merely feature visibility.

## Preserve test validity

- **Isolation:** Control test data and state; make cases order-independent. Record shared accounts, fixtures, or environment mutations and reset them explicitly. A prior case must not make a later case pass or fail.
- **Visual comparisons:** Match viewport, device scale, browser, fonts, theme, locale, data, and loading state to the approved reference. A mismatch is not evidence of a product regression.
- **Intermittent failures:** Preserve the initial failure and environment details. Repeat under the same conditions to characterize frequency; do not convert a failure to pass by retrying or suppress it as flaky without evidence. Separate product defects from test/environment instability, and track both.
- **Release risk:** A failing test is not waived by a workaround or schedule pressure. Only the authorized release-risk owner may accept a documented residual risk, rationale, affected scope, mitigation/workaround, owner, and follow-up plan. Acceptance does not erase the failure or override a non-waivable gate such as a P0/security/data-loss blocker.

## Reusable test and report schemas

Use these fields; omit inapplicable fields rather than inventing facts.

**Case:** ID | priority/risk | changed behavior and oracle | prerequisites/isolation | steps with expected result | data | cleanup | evidence.

**Run report:** build/environment and matched visual conditions | selected scope and rationale | pass/fail/blocked with linked evidence | intermittent reproduction details | unresolved risks and owner | release decision and authorized acceptance, if any.

An oracle must state an observable expected result, not “works as expected.” Record unknowns as unknown. Keep evidence sufficient to reproduce and distinguish an application failure from setup or test instability.
