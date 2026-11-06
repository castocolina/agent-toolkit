# Regression Testing

How to select a regression or smoke suite from a change, keep its results trustworthy, and record the release decision. Ordering follows the precedence in SKILL.md section 5.

## Select scope by change

1. List what changed (tickets, commits, config, dependency bumps) and, for each, the behavior it touches.
2. Add the direct dependencies and the integration boundaries each change crosses (an API, a queue, a payment provider).
3. Widen to every critical journey when the impact is broad, ownership of a dependency is unclear, or a shared component (auth, checkout, a design-system token) changed.
4. Smoke first: the few P0 checks that prove the build is testable at all. If smoke fails, stop and report; later results on a broken build are noise.
5. Fit the time box: order by the SKILL.md precedence, run down the list, and list every case that did not fit as residual risk with its owner. A cut case is never reported as passing.

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
