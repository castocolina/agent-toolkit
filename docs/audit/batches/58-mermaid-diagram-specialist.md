# Batch 58

## mermaid-diagram-specialist (agent)

### mermaid-diagram-specialist#D1-1
- severity: high
- dimension: D1
- location: agents/mermaid-diagram-specialist.md:115
- fix: Remove elementary syntax explanations and generic engineering advice. Replace them with tested, non-obvious renderer constraints, diagram-selection trade-offs, and project-specific modeling conventions that the model would otherwise miss.

### mermaid-diagram-specialist#D5-1
- severity: high
- dimension: D5
- location: agents/mermaid-diagram-specialist.md:59
- fix: Move useful detailed examples and type-specific rules into a Mermaid skill and preload it through skills:. Keep the agent under 200 lines with its role, modeling workflow, validation policy and output contract.

### mermaid-diagram-specialist#D7-1
- severity: medium
- dimension: D7
- location: agents/mermaid-diagram-specialist.md:552
- fix: Add: 'The task is complete once the requested diagrams satisfy every Success Criteria item and have been returned as fenced mermaid Markdown blocks.'

### mermaid-diagram-specialist#D8-1
- severity: high
- dimension: D8
- location: agents/mermaid-diagram-specialist.md:190
- fix: Use 'participant DB as Database' for portable database participants. Describe -> and --> as lines without arrowheads, and ->> and -->> as solid and dotted arrowhead messages. For explicit asynchronous open arrows, use -) or --) only when supported by the target renderer.

### mermaid-diagram-specialist#D8-2
- severity: high
- dimension: D8
- location: agents/mermaid-diagram-specialist.md:419
- fix: Declare 'ContainerDb(db, "Database", "PostgreSQL", "Stores all data")' inside the C4Component fence before the relationship, and check that every relationship endpoint is declared within its own diagram.

### mermaid-diagram-specialist#D8-3
- severity: medium
- dimension: D8
- location: agents/mermaid-diagram-specialist.md:571
- fix: Identify the target renderer before using compatibility-sensitive syntax. If C4 is unsupported, return a labeled flowchart preserving the intended boundaries and relationships. On parse failure, revise and revalidate; if rendering is unavailable, perform static checks and explicitly report that rendering was not verified.

### mermaid-diagram-specialist#D2-1
- severity: medium
- dimension: D2
- location: agents/mermaid-diagram-specialist.md:83
- fix: Add a short procedure: identify the audience and question, choose context for external actors and systems, container for deployable units, or component for internals of one container; derive nodes and relationships from supplied evidence and explicitly record assumptions before drawing.

### mermaid-diagram-specialist#D3-1
- severity: medium
- dimension: D3
- location: agents/mermaid-diagram-specialist.md:562
- fix: Add a compact Gotchas section with specific prohibitions and reasons, such as never using unquoted lowercase 'end' in flowchart labels because it can be parsed as a control token, and quoting labels containing parser-significant punctuation rather than relying on plain-label parsing.

### mermaid-diagram-specialist#D4-1
- severity: low
- dimension: D4
- location: agents/mermaid-diagram-specialist.md:3
- fix: Use supported frontmatter only:
---
name: mermaid-diagram-specialist
description: >-
  Mermaid diagram specialist for creating flowcharts, sequence diagrams, ERDs,
  and architecture visualizations
---
Move category, usage, input and output information into the system-prompt body. This avoids relying on agent fields the host ignores.

### mermaid-diagram-specialist#D4-2
- severity: low
- dimension: D4
- location: agents/mermaid-diagram-specialist.md:4
- fix: Create and revise Mermaid flowcharts, sequence diagrams, ERDs, state machines and C4 architecture diagrams in Markdown. Use when a user wants to visualize workflows, document a data model or explain component interactions, even without naming Mermaid. Not for non-Mermaid artwork or implementing the documented system.

### mermaid-diagram-specialist#D6-1
- severity: medium
- dimension: D6
- location: agents/mermaid-diagram-specialist.md:609
- fix: Make approximately 20 nodes a readability target, not a completeness limit. For larger inputs, preserve all required elements using an overview and focused subdiagrams, or retain a complete diagram when explicitly requested.
