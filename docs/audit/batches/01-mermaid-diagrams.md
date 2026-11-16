# Batch 01

## mermaid-diagrams (skill)

### mermaid-diagrams#D1-1
- severity: high
- dimension: D1
- location: skills/mermaid-diagrams/SKILL.md:44
- fix: Remove the basic syntax introduction, four inline tutorials, and generic reasons to diagram. Keep the classification gate, host constraints, subgraph-direction trap, and renderer-specific failures; leave syntax examples in the already-gated type references.

### mermaid-diagrams#D7-1
- severity: medium
- dimension: D7
- location: skills/mermaid-diagrams/evals/evals.json:9
- fix: Add realistic repair and renderer-boundary cases, including special-character labels, GitHub architecture icons, and a larger C4 example. Assert successful parsing/rendering and correct entity relationships, not only declaration keywords.

### mermaid-diagrams#D8-1
- severity: high
- dimension: D8
- location: skills/mermaid-diagrams/references/architecture-diagrams.md:64
- fix: Use built-in icons throughout default examples. Put custom icons only in a separately gated example that includes the required host registration and target-renderer verification.

### mermaid-diagrams#D8-2
- severity: high
- dimension: D8
- location: skills/mermaid-diagrams/references/c4-diagrams.md:279
- fix: Give every C4 element a unique identifier, such as person_user and svc_user, and update each Rel call to target the intended element. Validate identifier uniqueness across the complete example.

### mermaid-diagrams#D7-1
- severity: low
- dimension: D7
- location: skills/mermaid-diagrams/evals/evals.json:6
- fix: Prompts are terse commands without realistic user context (file paths, backstory, casual phrasing) and no broken-syntax repair case; add a casual context-rich prompt and a malformed-source repair eval with verifiable assertions.

### mermaid-diagrams#D8-1
- severity: medium
- dimension: D8
- location: skills/mermaid-diagrams/SKILL.md:127
- fix: The load table has rows only for Class, Sequence, Flowchart, ERD, C4, architecture, and theming; State, Git, Gantt, and Pie are promised by the description and classification table but have no routing target. Add rows (e.g., route them to references/advanced-features.md) or inline minimal syntax.

### mermaid-diagrams#D4-1
- severity: medium
- dimension: D4
- location: skills/mermaid-diagrams/SKILL.md:3
- fix: Create, edit, and repair Mermaid diagrams in Markdown or .mmd files. Use when users ask to diagram, visualize, model, map out, or show software interactions, schemas, architecture, lifecycles, processes, schedules, proportions, or Git history, even without naming Mermaid. Classify the question before choosing sequenceDiagram, classDiagram, erDiagram, C4, stateDiagram-v2, flowchart, architecture-beta, gantt, pie, or gitGraph. Not for prose-only explanations, PlantUML or draw.io editing, matplotlib data charts, or interactive diagram-canvas components.

### mermaid-diagrams#D2-1
- severity: medium
- dimension: D2
- location: skills/mermaid-diagrams/SKILL.md:29
- fix: Add a brief grounding checkpoint before drawing: identify the audience and abstraction level, extract entities and relationships from supplied code/schema or facts, and distinguish confirmed relationships from assumptions before choosing notation.

### mermaid-diagrams#D6-1
- severity: medium
- dimension: D6
- location: skills/mermaid-diagrams/SKILL.md:176
- fix: Make diagrams conditional on the user's requested deliverable or a clear explanatory benefit. Explicitly respect prose-only requests and avoid creating diagrams merely because a task involves architecture, schemas, or refactoring.

### mermaid-diagrams#D1-1
- severity: low
- dimension: D1
- location: skills/mermaid-diagrams/SKILL.md:172
- fix: Delete the section; 'Always diagram when starting new projects' and 'Align stakeholders' are generic advocacy the model already knows and they dilute the expert classification and pitfall content.

### mermaid-diagrams#D2-1
- severity: low
- dimension: D2
- location: skills/mermaid-diagrams/SKILL.md:143
- fix: Replace Best Practices items 2-5 (fit the column, connect at the boundary, shapes are roles, color by role) with one-line pointers to the matching authoring-rules.md sections instead of duplicating them.

### mermaid-diagrams#D3-1
- severity: low
- dimension: D3
- location: skills/mermaid-diagrams/SKILL.md:170
- fix: State the why explicitly (color-vision deficiency affects ~8% of men and docs often print or render in grayscale), so the rule is followed for the right reason.

### mermaid-diagrams#D4-1
- severity: low
- dimension: D4
- location: skills/mermaid-diagrams/SKILL.md:3
- fix: Append a boundary against near-miss neighbours the trigger queries already test as negatives, e.g., 'Mermaid text syntax only; not for PlantUML, draw.io, matplotlib charts, or image editors.'

### mermaid-diagrams#D6-1
- severity: low
- dimension: D6
- location: skills/mermaid-diagrams/SKILL.md:35
- fix: The shape/palette/proportion rules in authoring-rules.md are flowchart-centric; add per-type calibration notes for State, Git, Gantt, and Pie or explicitly exempt those types from the palette and shape rules.
