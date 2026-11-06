# Batch 35

## mermaid-diagrams (skill)

### mermaid-diagrams#D7-1
- severity: medium
- dimension: D7
- location: skills/mermaid-diagrams/evals/evals.json:189
- fix: Add assertions requiring distinct, consistently applied team colors for Sales, Warehouse, Shipping, and Support, including a check that every team-owned node receives the corresponding styling.

### mermaid-diagrams#D8-1
- severity: high
- dimension: D8
- location: skills/mermaid-diagrams/references/erd-diagrams.md:31
- fix: Replace that relationship with 'CUSTOMER ||..o{ ORDER : "places"' so the worked example matches its declared surrogate primary key and the schema-to-diagram procedure.

### mermaid-diagrams#D8-2
- severity: medium
- dimension: D8
- location: skills/mermaid-diagrams/SKILL.md:18
- fix: Add an appearance-only editing branch that reads authoring-rules.md section 6, loads advanced-features.md when changing theme/config, preserves diagram semantics, and checks text/fill contrast before validation.

### mermaid-diagrams#D7-1
- severity: low
- dimension: D7
- location: skills/mermaid-diagrams/evals/trigger-queries.json
- fix: Add 2-3 should-trigger queries that do not name a diagram (e.g. 'show how a request moves through auth, cache and DB for the wiki'). Relabel or reword the GitHub-version query so it is a clear near-miss, e.g. one asking about Mermaid version history with no diagram task.

### mermaid-diagrams#D8-1
- severity: low
- dimension: D8
- location: skills/mermaid-diagrams/SKILL.md:18
- fix: Add to step 4: after exit 0, check the rendered size against authoring-rules.md section 2 and split the diagram if it fails.

### mermaid-diagrams#D1-1
- severity: medium
- dimension: D1
- location: skills/mermaid-diagrams/references/authoring-rules.md:75
- fix: Compress the standard shape vocabulary and basic grammar surveys into brief activation reminders. Retain the stadium-versus-rounded-rectangle trap, house-style overrides, host constraints, silent failures, and examples that demonstrate non-obvious behavior.

### mermaid-diagrams#D1-1
- severity: low
- dimension: D1
- location: skills/mermaid-diagrams/references/advanced-features.md:28
- fix: Keep only the non-obvious facts (the `-i README.md -o out.md` rewrite, `themeVariables` honored only with `theme: base`, `click` stripped on GitHub). Drop the generic flag examples.

### mermaid-diagrams#D2-1
- severity: low
- dimension: D2
- location: skills/mermaid-diagrams/SKILL.md:10
- fix: Add one line to step 1: if the diagram type or a cardinality is not settled by the supplied material, state the assumption in the reply, or ask one question when two types are plausible.

### mermaid-diagrams#D3-1
- severity: low
- dimension: D3
- location: skills/mermaid-diagrams/SKILL.md:50
- fix: Write the one-line consequence inline, e.g. 'NEVER link a node inside a subgraph to an outside node while relying on that subgraph's `direction`: Mermaid silently drops it.' Keep the pointer after it.

### mermaid-diagrams#D4-1
- severity: low
- dimension: D4
- location: skills/mermaid-diagrams/SKILL.md:3
- fix: Replace with: "Create, edit, and repair Mermaid diagrams (.mmd files or ```mermaid blocks in Markdown). Use when users ask to diagram, visualize, model, map out or show sequence flows, class models, ER diagrams or database schemas, state machines, flowcharts, C4 or architecture-beta software and infrastructure architecture (including terse requests such as 'architecture: mobile client, API, database, email provider'), Gantt schedules, pie proportions or Git branch history, or when a Mermaid diagram fails to render or export (mmdc, GitHub), even without naming Mermaid. Choose the type from the question the diagram answers, using flowchart only as a last resort. Not for prose-only explanations, explaining an existing diagram without changing it, PlantUML or draw.io work, matplotlib data charts, or interactive diagram-canvas components."

### mermaid-diagrams#D5-1
- severity: low
- dimension: D5
- location: skills/mermaid-diagrams/references/authoring-rules.md:3
- fix: Keep the numbers, but note in SKILL.md that the citations are fixed. Optionally split sections 4-6 (flowchart-only) into a flowchart reference so non-flowchart work never loads them.

### mermaid-diagrams#D6-1
- severity: low
- dimension: D6
- location: skills/mermaid-diagrams/references/authoring-rules.md:104
- fix: Add a default selector: A for architecture or service maps, B when the diagram shows status, C for before/after. Say that mixing palettes in one diagram is an error.
