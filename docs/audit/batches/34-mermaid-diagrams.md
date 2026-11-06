# Batch 34

## mermaid-diagrams (skill)

### mermaid-diagrams#D7-1
- severity: low
- dimension: D7
- location: skills/mermaid-diagrams/evals/evals.json:25
- fix: Add assertions for PK/FK annotations, exactly one order and one product per line item, the corresponding many-side endpoints, and explicit assumptions where minimum child counts are unspecified.

### mermaid-diagrams#D8-1
- severity: medium
- dimension: D8
- location: skills/mermaid-diagrams/SKILL.md:15
- fix: Separate parse-only repair from semantic or rendering repair. For incorrect arrows, missing elements or other silent failures, load the matching type reference even when parsing succeeds, and permit corrections that restore the user-intended meaning. Keep syntax-only preservation for requests limited to parse repair.

### mermaid-diagrams#D7-1
- severity: medium
- dimension: D7
- location: skills/mermaid-diagrams/evals/evals.json
- fix: Add an eval for a flowchart of about 12 nodes. Its assertions should check that `classDef` sets fill, stroke and color together, that the diagram is TD, that no cross-boundary edge sits beside a subgraph `direction`, and that the diagram is split if it is oversized. Add a repair eval for a lowercase `end` in a sequence diagram.

### mermaid-diagrams#D8-1
- severity: medium
- dimension: D8
- location: skills/mermaid-diagrams/SKILL.md:15
- fix: Reconcile steps 2 and 3. Say that a repair reads only authoring-rules.md section 7, and that the full read applies to new diagrams only. The mandatory-read line currently contradicts the repair shortcut.

### mermaid-diagrams#D8-2
- severity: low
- dimension: D8
- location: README.md
- fix: Update the README pointers to match the current SKILL.md and mmdc validation step. The README stays as the repo-required file.

### mermaid-diagrams#D1-1
- severity: medium
- dimension: D1
- location: skills/mermaid-diagrams/references/class-diagrams.md:35
- fix: Reduce the standard relationship table to a brief orientation reminder, and shorten the basic shape/link inventories and routine example members. Retain the Mermaid-specific generics, multiplicity parsing, identifier and renderer traps.

### mermaid-diagrams#D6-1
- severity: medium
- dimension: D6
- location: skills/mermaid-diagrams/references/authoring-rules.md:92
- fix: Make the node-count threshold and bundled palettes defaults rather than requirements. Permit host-themed diagrams and other accessible palettes when they suit the audience; retain strict contrast requirements whenever custom colors are used.

### mermaid-diagrams#D1-1
- severity: low
- dimension: D1
- location: skills/mermaid-diagrams/references/flowcharts.md:5
- fix: Delete the basic link and shape syntax list, which the model already knows. Keep only the `A(Text)` vs `A([Text])` confusion and the `linkStyle` index-shift trap.

### mermaid-diagrams#D1-2
- severity: low
- dimension: D1
- location: skills/mermaid-diagrams/references/sequence-diagrams.md:28
- fix: Trim the arrow table to the non-obvious rows (`-)` async and `-x` lost), since the model knows the standard arrows.

### mermaid-diagrams#D2-1
- severity: medium
- dimension: D2
- location: skills/mermaid-diagrams/SKILL.md:13
- fix: Put the repair-or-new fork before the read step and say which sections each path reads. SKILL.md would then show the routing as a clear decision tree. Most of the thinking framework (choose by question answered) lives only in authoring-rules.md section 1; add one line to SKILL.md naming it.

### mermaid-diagrams#D3-1
- severity: medium
- dimension: D3
- location: skills/mermaid-diagrams/SKILL.md
- fix: Add a short `## Gotchas` or NEVER list to SKILL.md with the highest-cost silent failures and a pointer to each type file. Candidates: the inverted class arrow, a gantt date that does not match dateFormat, the gitGraph `checkout` before `branch`, and the subgraph `direction` being ignored. The agent often will not recognize the trigger to open the right type file.

### mermaid-diagrams#D4-1
- severity: low
- dimension: D4
- location: skills/mermaid-diagrams/SKILL.md:3
- fix: Replace the description with: "Create, edit, and repair Mermaid diagrams (.mmd files or ```mermaid blocks in Markdown). Use this skill when users ask to diagram, visualize, model, map out, or show sequence diagrams, class diagrams, ER diagrams or database schemas, state machines, flowcharts, software architecture (including terse requests such as 'architecture: mobile client, API, database, email provider'), Gantt schedules, pie proportions, or Git branch history, or when a Mermaid diagram fails to render or export (mmdc, GitHub), even without naming Mermaid. Choose the diagram type from the question being answered: sequenceDiagram, classDiagram, erDiagram, C4, stateDiagram-v2, architecture-beta, gantt, pie, gitGraph, with flowchart as the last resort. Not for prose-only explanations, explaining an existing diagram without changing it, PlantUML or draw.io work, matplotlib data charts, or interactive diagram-canvas components."

### mermaid-diagrams#D5-1
- severity: low
- dimension: D5
- location: skills/mermaid-diagrams/references/authoring-rules.md
- fix: Move the flowchart-only sections 4-6 into `flowcharts.md`, or tell the agent to read them only for a flowchart. A sequence or ERD diagram would then not load them.

### mermaid-diagrams#D6-1
- severity: low
- dimension: D6
- location: skills/mermaid-diagrams/references/architecture-diagrams.md
- fix: Keep one default pack example and cut the list of alternative packs. This section is already gated to renderers known to register the pack, so a menu adds no value.
