# Batch 10

## qa-test-planner (skill)

### qa-test-planner#D7-1
- severity: medium
- dimension: D7
- location: skills/qa-test-planner/SKILL.md:45
- fix: Add a documented non-interactive JSON input mode, implement --help, and emit a machine-readable result manifest separately from diagnostic output. Extend the existing smoke tests to exercise those interfaces.

### qa-test-planner#D8-1
- severity: high
- dimension: D8
- location: skills/qa-test-planner/references/bug_report_templates.md:383
- fix: Remove rare crashes from the unconditional Low examples. Classify crashes by impact and recoverability, record reproduction frequency separately, and label response-time targets as organization-specific examples rather than established policy.

### qa-test-planner#D7-1
- severity: medium
- dimension: D7
- location: skills/qa-test-planner/SKILL.md:45
- fix: Give the scripts a non-interactive mode (all fields as flags or a stdin template), add --help, and drop color codes from stdout so agents can run them directly

### qa-test-planner#D8-1
- severity: low
- dimension: D8
- location: skills/qa-test-planner/SKILL.md:26
- fix: Add 'mark unknown environment facts as Unknown; never guess them' so deliverables stay honest when the requester cannot supply the facts

### qa-test-planner#D1-1
- severity: medium
- dimension: D1
- location: skills/qa-test-planner/SKILL.md:23
- fix: Condense the standard input-partition and deliverable inventories. Retain the concrete safeguards, and replace generic coverage reminders with decisions for deriving observable oracles for retries, state transitions, and irreversible operations.

### qa-test-planner#D2-1
- severity: medium
- dimension: D2
- location: skills/qa-test-planner/SKILL.md:14
- fix: Add a compact plan branch: establish requirements and risk owners, select scope from changed behavior and dependencies, derive entry/exit gates from critical coverage and unresolved risk, then reconcile the plan with available environments and execution time.

### qa-test-planner#D1-1
- severity: low
- dimension: D1
- location: skills/qa-test-planner/SKILL.md:23
- fix: Boundary value analysis is textbook knowledge; compress step 2 to 'partition inputs by behavior with boundaries and failure paths' and spend the tokens on the non-obvious safeguards

### qa-test-planner#D2-1
- severity: low
- dimension: D2
- location: skills/qa-test-planner/SKILL.md:15
- fix: Add a default for combined requests, e.g. 'produce the plan first, then cases that trace to its risks'

### qa-test-planner#D3-1
- severity: low
- dimension: D3
- location: skills/qa-test-planner/SKILL.md:30
- fix: Add a NEVER item such as 'Never assume deterministic clocks or timezones; freeze time or state the timezone in test data, or runs flake across machines'

### qa-test-planner#D6-1
- severity: low
- dimension: D6
- location: skills/qa-test-planner/SKILL.md:16
- fix: State a default precedence (e.g. failure impact first, then changed-code overlap) so prioritization is reproducible
