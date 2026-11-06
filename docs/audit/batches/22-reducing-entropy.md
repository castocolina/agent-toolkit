# Batch 22

## reducing-entropy (skill)

### reducing-entropy#D7-1
- severity: medium
- dimension: D7
- location: skills/reducing-entropy/evals/evals.json:20
- fix: Provide a concrete code fixture for measured reductions and assertions for retained behavior and counting exclusions. For evidence-unavailable reviews, assert a measurement method and explicitly pending totals rather than actual before/after measurements.

### reducing-entropy#D7-2
- severity: medium
- dimension: D7
- location: skills/reducing-entropy/evals/trigger-queries.json:3
- fix: Replace several name-matching positives with realistic requests to shrink a specified module or choose the least-code implementation without naming the skill. Add contextual near-misses that request readability or local cleanup without codebase minimization.

### reducing-entropy#D7-1
- severity: medium
- dimension: D7
- location: skills/reducing-entropy/evals/trigger-queries.json:8
- fix: Replace several should-trigger queries with natural explicit requests that do not name the skill (e.g. 'this codebase is way too big — delete whatever we don't need'); all ten positives currently contain the literal skill name or 'entropy', so the explicitness axis is untested.

### reducing-entropy#D7-2
- severity: low
- dimension: D7
- location: skills/reducing-entropy/evals/evals.json:6
- fix: Bundle the module under evals/files/ so the measurement and merge-invariant steps run against real code instead of a described example.

### reducing-entropy#D8-1
- severity: low
- dimension: D8
- location: skills/reducing-entropy/SKILL.md:16
- fix: State what to do when several lenses apply at once (load all applicable references, with PAGNI gating deletion decisions) so the routing cannot stall on overlapping triggers.

### reducing-entropy#D1-1
- severity: medium
- dimension: D1
- location: skills/reducing-entropy/SKILL.md:29
- fix: Consolidate measurement and reporting into one contract and trim generic validation reminders. Keep the higher-value invariant-ownership comparison, consistent counting rules, complexity-displacement warning, and costly-retrofit exception.

### reducing-entropy#D5-1
- severity: low
- dimension: D5
- location: skills/reducing-entropy/adding-reference-mindsets.md:3
- fix: Move this maintenance note into repository-level contributor documentation instead of shipping a separate contributor-only file with the skill.

### reducing-entropy#D1-1
- severity: low
- dimension: D1
- location: skills/reducing-entropy/SKILL.md:12
- fix: Keep the named mindsets and the end-state rule; trim the rhetorical question, which restates the title-level intent the model already infers from the explicit request.

### reducing-entropy#D2-1
- severity: low
- dimension: D2
- location: skills/reducing-entropy/SKILL.md:28
- fix: Measure the baseline during inventory (step 1) so deletion candidates are proposed and ranked against measured sizes rather than counted after proposal.

### reducing-entropy#D3-1
- severity: low
- dimension: D3
- location: skills/reducing-entropy/SKILL.md:32
- fix: Add the why: tests and vendored/generated code are not first-party entropy, so removing them games the metric while hiding risk.

### reducing-entropy#D4-1
- severity: medium
- dimension: D4
- location: skills/reducing-entropy/SKILL.md:3
- fix: Guide deletion-biased codebase minimization: inventory deletable or mergeable code, guard behavior, public APIs, and data-retention obligations, and measure first-party line counts before and after. Use only when the user explicitly asks to reduce entropy, delete code, shrink or simplify the codebase, or choose the smallest implementation. Not for general refactoring, readability, or performance reviews.

### reducing-entropy#D5-1
- severity: low
- dimension: D5
- location: skills/reducing-entropy/adding-reference-mindsets.md:1
- fix: Move this contributor-process note to the repository's contributor documentation outside the shipped skill package; nothing in SKILL.md loads it.
