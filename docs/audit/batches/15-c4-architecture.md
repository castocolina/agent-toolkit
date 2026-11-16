# Batch 15

## c4-architecture (skill)

### c4-architecture#D7-1
- severity: medium
- dimension: D7
- location: skills/c4-architecture/evals/evals.json:1
- fix: Add a small repository fixture with build configuration, deployment manifests, runtime dependencies, and a shared library. Assert that generated views distinguish containers from libraries and attach evidence to inferred boundaries and relationships.

### c4-architecture#D8-1
- severity: high
- dimension: D8
- location: skills/c4-architecture/references/advanced-patterns.md:436
- fix: Use Container_Boundary for the API's internal components, add a handler component as the relationship endpoint, and connect that handler to the circuit breaker. Validate the corrected example with the target Mermaid renderer.

### c4-architecture#D7-1
- severity: medium
- dimension: D7
- location: skills/c4-architecture/evals/evals.json
- fix: Add one or two evals with a small fixture tree (build files, docker-compose, service manifests) so 'evidence-backed' assertions grade real extraction, plus an eval for the renderer-downgrade fallback branch.

### c4-architecture#D8-1
- severity: medium
- dimension: D8
- location: skills/c4-architecture/SKILL.md:31
- fix: Align the element threshold across files: c4-syntax.md says 'under 15 elements' and common-mistakes.md says 'under 20 (ideally under 15)'; pick one rule ('under 20, ideally 15') so an agent following the syntax reference does not reject diagrams the main skill allows.

### c4-architecture#D1-1
- severity: medium
- dimension: D1
- location: skills/c4-architecture/references/advanced-patterns.md:175
- fix: Remove or sharply compress generic CQRS, API gateway, and cloud-deployment walkthroughs and basic C4 definitions. Retain non-obvious boundary decisions, evidence-extraction rules, and Mermaid-specific incompatibilities, with minimal examples for those issues.

### c4-architecture#D6-1
- severity: medium
- dimension: D6
- location: skills/c4-architecture/SKILL.md:16
- fix: Make module count an optional complexity hint, not a restriction. Select component views according to the requested question, audience, meaningful responsibility boundaries, and available evidence; honor explicit component-view requests when the container can be identified.

### c4-architecture#D1-1
- severity: low
- dimension: D1
- location: skills/c4-architecture/SKILL.md:18
- fix: The Level 1-4 rows restate the C4 hierarchy the model knows; keep only the non-obvious rows (Level 4 rarely useful; Dynamic/Deployment are supplementary, not levels).

### c4-architecture#D1-2
- severity: low
- dimension: D1
- location: skills/c4-architecture/SKILL.md:30
- fix: State the rule once here; drop the duplicate 'Always model message topics/queues as separate containers' directive in references/advanced-patterns.md and keep only common-mistakes.md's wrong/correct example.

### c4-architecture#D2-1
- severity: medium
- dimension: D2
- location: skills/c4-architecture/SKILL.md:37
- fix: Make verification a loop, not a clause: 'fix failing elements, re-render, and re-validate until the diagram passes'; currently nothing says what to do when validation fails.

### c4-architecture#D3-1
- severity: low
- dimension: D3
- location: skills/c4-architecture/SKILL.md:37
- fix: This is the only in-body environment fact; inline two or three highest-cost mistakes (shared library as container, single broker box, bidirectional arrows) as a short NEVER list in SKILL.md, keeping the full catalogue in common-mistakes.md.

### c4-architecture#D6-1
- severity: low
- dimension: D6
- location: skills/c4-architecture/SKILL.md:32
- fix: Add the default for the common unknown-audience case (e.g., 'audience unstated: Levels 1-2'); otherwise this bullet is a menu with no default.
