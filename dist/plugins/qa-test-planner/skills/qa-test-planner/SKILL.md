---
name: qa-test-planner
description: Use only when the user explicitly invokes qa-test-planner by name or /qa-test-planner to create manual QA plans, executable test cases, regression/smoke suites, Figma design-validation checklists, or structured bug reports. Not for writing Cypress/unit/API automation, fixing implementation code, or general testing requests.
metadata:
  trigger: explicit
---

# QA Test Planner

Create risk-traceable manual QA deliverables only after explicit invocation by skill name. Do not activate for general testing requests.

## Decide the deliverable

- Explicit plan request → test plan with scope, risks, environment, entry/exit criteria.
- Cases/request to test a flow → manual cases. If ambiguous, default to manual cases with a smoke core; ask only when plan, suite, or bug report is clearly intended.
- Regression/smoke request → prioritize by changed code, critical journeys, failure impact, and execution cost.
- Bug report request → capture reproducibility and evidence, not a guessed root cause.
- Figma comparison → use MCP only if available; otherwise request screenshots/specs and state the limitation.

## Build coverage from evidence

1. Identify requirement IDs, user-critical paths, and explicit invariants. For each, write the observable pass/fail oracle before the steps.
2. Partition inputs by behavior; include boundaries (minimum/maximum, just below/above, empty, malformed), state transitions, permissions, and failure/retry paths where relevant.
3. Map each case to requirement(s), risk, priority, and test data. Prioritize irreversible data/security/revenue failures over cosmetic issues.
4. Review the traceability map: every critical requirement has an executable case; uncovered requirements and blocked tests are explicit. Avoid duplicate cases that add no distinct risk coverage.
5. State environment, build, viewport, theme, locale, and device-pixel ratio when they affect reproducibility or visual comparison.

## Hard-earned safeguards

- Keep test data isolated and resettable; shared mutable accounts/orders cause order-dependent failures and conceal regressions.
- Each case must stand alone. A dependency on a previous case can make a failure disappear when the suite is reordered or rerun selectively.
- Confirm the Figma frame/version and matching viewport, theme, and device-pixel ratio before judging visual differences; otherwise false mismatches are expected.
- Record intermittent reproduction rate (for example, 2/10), never label it “Always”; frequency changes triage and response expectations.
- Never copy a color by eye. Compare measured values/tokens and account for rendering conditions; near-identical shades can pass casual review incorrectly.
- A P0 failure blocks release unless an authorized owner explicitly reclassifies the risk with documented rationale and acceptance. A workaround alone does not silently waive the gate.
- Pass-rate percentages are illustrative, not release policy. Derive gates from critical requirements, unresolved risk, blocked coverage, and stakeholder acceptance.

## Load only the needed reference

- Read `references/test_case_templates.md` when writing manual cases.
- Read `references/bug_report_templates.md` when documenting a bug.
- Read `references/regression_testing.md` when selecting or gating a suite.
- Read `references/figma_validation.md` for design comparison.

Scripts are optional local document generators, not test automation. They prompt interactively; inspect `--help` before use (the current scripts do not provide it), and do not invoke them in a non-interactive session. Draft directly from the relevant reference instead.
