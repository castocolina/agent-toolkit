# Batch 59

## ascii-ui-mockup-generator (agent)

### ascii-ui-mockup-generator#D1-1
- severity: high
- dimension: D1
- location: agents/ascii-ui-mockup-generator.md:39
- fix: Remove the self-praise and compress generic quality assurances. Replace them with concrete layout heuristics, such as keeping comparison fields aligned across repeated records while reserving stacked layouts for independently scanned items.

### ascii-ui-mockup-generator#D3-1
- severity: high
- dimension: D3
- location: agents/ascii-ui-mockup-generator.md:20
- fix: Add an ASCII-specific Gotchas section: never align columns with tabs because viewer tab stops differ; never substitute emoji or Unicode box-drawing characters in ASCII-only output because encoding and display-width assumptions can fail; explain how these mistakes damage the mockup.

### ascii-ui-mockup-generator#D4-1
- severity: high
- dimension: D4
- location: agents/ascii-ui-mockup-generator.md:3
- fix: Replace the frontmatter with valid YAML, using a folded scalar to satisfy YAML's colon-space constraint:
---
name: ascii-ui-mockup-generator
description: >-
  Create ASCII UI wireframes with distinct layout alternatives, design rationales,
  and a component handoff. Use when users want to explore dashboard, form,
  navigation, or screen layouts before implementation, including requests to
  sketch how an interface could look. Not for implementing UI code or producing
  high-fidelity visual designs.
model: sonnet
color: green
---

### ascii-ui-mockup-generator#D7-1
- severity: medium
- dimension: D7
- location: agents/ascii-ui-mockup-generator.md:41
- fix: Add: "The initial task is done when the numbered ASCII mockups, their rationales, and a selection question have been delivered. A refinement task is done when the requested changes and any requested implementation handoff have been delivered."

### ascii-ui-mockup-generator#D8-1
- severity: medium
- dimension: D8
- location: agents/ascii-ui-mockup-generator.md:19
- fix: Establish target character widths before drawing and state assumptions when widths are unspecified. When content exceeds a target width, stack fields or explicitly mark horizontal overflow rather than breaking borders. Before delivery, check required components and row alignment, repair violations, and repeat the check.

### ascii-ui-mockup-generator#D2-1
- severity: medium
- dimension: D2
- location: agents/ascii-ui-mockup-generator.md:22
- fix: Before drawing, rank the primary user tasks, identify required content that must remain invariant across alternatives, and assign each variant a distinct trade-off. Evaluate the resulting layouts against those tasks before writing their rationales.

### ascii-ui-mockup-generator#D6-1
- severity: medium
- dimension: D6
- location: agents/ascii-ui-mockup-generator.md:14
- fix: Default to three structurally distinct alternatives for exploratory requests, but honor an explicit option count and produce only the requested revision when refining an existing mockup.

## general-purpose (agent)

### general-purpose#D1-1
- severity: high
- dimension: D1
- location: agents/general-purpose.md:21
- fix: Remove repeated capability declarations from Behavioral Mindset, Focus Areas, and the Will list. Replace them with knowledge specific to this agent's environment, such as actual specialist responsibilities, integration constraints, and observed failure modes.

### general-purpose#D2-1
- severity: high
- dimension: D2
- location: agents/general-purpose.md:28
- fix: Replace the generic sequence with an explicit reasoning process: map each requirement to an observable acceptance check and its owning component, identify dependency order, establish baseline behavior before changes, and select verification gates according to the affected components.

### general-purpose#D7-1
- severity: medium
- dimension: D7
- location: agents/general-purpose.md:36
- fix: Add: 'The task is complete only when every requested acceptance criterion is satisfied and required validation succeeds. Return Markdown sections for Result, Changes with file paths, Validation with observed checks and outcomes, and Remaining blockers. Label blocked or unverified work as incomplete.'

### general-purpose#D8-1
- severity: medium
- dimension: D8
- location: agents/general-purpose.md:29
- fix: Resolve the branch explicitly: delegate a bounded subtask when an available specialist matches its requirements; otherwise execute it directly if the available tools and scope permit. If delegation fails, inspect the failure and take the direct path when feasible; otherwise return the concrete blocker and needed capability to the caller.

### general-purpose#D4-1
- severity: low
- dimension: D4
- location: agents/general-purpose.md:4
- fix: Replace with 'model: inherit' to use the invoking model through a documented model selector.

### general-purpose#D4-2
- severity: medium
- dimension: D4
- location: agents/general-purpose.md:3
- fix: Coordinate general programming work across multiple files or components, including debugging, implementation, and validation. Use for complex, multi-step requests that do not fit a single specialist, or when specialist results need integration. Prefer a dedicated specialist for a focused domain task.

### general-purpose#D3-1
- severity: medium
- dimension: D3
- location: agents/general-purpose.md:49
- fix: Add delegation-specific prohibitions with reasons: never assign concurrent workers overlapping files because stale snapshots can overwrite changes; never accept a specialist's success summary as verification evidence because it may omit failed or unrun checks—inspect the resulting changes and observed validation output.

### general-purpose#D6-1
- severity: medium
- dimension: D6
- location: agents/general-purpose.md:44
- fix: Preserve discretion for read-only investigation and reversible local edits, but require a target-and-impact check before destructive or shared-state operations. Require authorization covering the proposed operation and use a preview or recovery plan where available.
