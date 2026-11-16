# Batch 43

## qa-test-planner (skill)

### qa-test-planner#D7-1
- severity: low
- dimension: D7
- location: skills/qa-test-planner/evals/trigger-queries.json
- fix: Replace the two weakest negatives with near-misses that use the skill's vocabulary without naming it (for example 'smoke suite for tonight's hotfix, 30 min'). Trim the positives to 10 so the 8-10 split holds.

### qa-test-planner#D8-1
- severity: low
- dimension: D8
- location: skills/qa-test-planner/SKILL.md:98
- fix: Say that the script writes one case per run, so a suite needs one call per TC ID with distinct IDs. List the accepted --type values (functional|ui|integration|regression|performance|security) so an agent does not hit exit 2 on its first try.

### qa-test-planner#D8-1
- severity: high
- dimension: D8
- location: skills/qa-test-planner/SKILL.md:39
- fix: Distinguish confirmed non-impact from missing impact information. Exclude an area only when the available evidence establishes that it is unrelated. Otherwise record the impact as Unknown, request the missing change or dependency information, and provisionally retain critical journeys or list their checks as Blocked with an owner.

### qa-test-planner#D7-1
- severity: medium
- dimension: D7
- location: skills/qa-test-planner/evals/evals.json:91
- fix: For both file-generation evals, require an actual successful script invocation, a parsed manifest, and a read of the named Markdown file. Assert the supplied values and Unknown/Open Questions fields directly against that artifact; a proposed command or description of future verification must not satisfy these checks.

### qa-test-planner#D1-1
- severity: low
- dimension: D1
- location: skills/qa-test-planner/SKILL.md:37
- fix: Cut the skeleton line and the generic 'Scope' bullet, because the model already knows a standard plan layout. Keep only the non-obvious rules: the out-of-scope reason test, the K-line risk format, and exit gates with no bare pass rate.

### qa-test-planner#D2-1
- severity: low
- dimension: D2
- location: skills/qa-test-planner/SKILL.md:24
- fix: Add a checkpoint for the combined plan-plus-cases path: once the plan is written, check that every K risk has at least one TC ID planned before writing the steps. This turns the process pattern into phases with a gate instead of an ordering hint.

### qa-test-planner#D4-1
- severity: low
- dimension: D4
- location: skills/qa-test-planner/SKILL.md:3
- fix: Create manual QA test plans, executable manual test cases, regression and smoke suites, release-gate (ship or block) decisions, Figma design-validation checklists and structured bug reports (repro rate, environment, Open Questions). Use only when the user invokes qa-test-planner by name or /qa-test-planner. Not for Cypress, Playwright, unit or API test automation, fixing implementation code, or manual QA requests that do not name this skill.
