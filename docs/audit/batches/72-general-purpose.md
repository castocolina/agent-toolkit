# Batch 72

## general-purpose (agent)

### general-purpose#D4-1
- severity: high
- dimension: D4
- location: agents/general-purpose.md:3
- fix: Quote the value so the frontmatter parses. An unquoted plain scalar containing ': ' is a YAML error ('mapping values are not allowed here'). Per artifact-specs.md, a plugin agent whose YAML does not parse loads under its file name with no fields, so the description that routes it is lost. Replacement: description: "Coordinate multi-file, multi-component programming work end to end: break the request down, delegate to matching specialists or implement directly, integrate their changes and run the project's verification gates. Use for complex multi-step debugging, implementation or refactoring that spans several files or components, or when specialist results need integrating and verifying, even if coordination is not requested. Not for trivial one-step edits or a focused single-domain task a dedicated specialist owns. Unlike the built-in general-purpose agent, it returns Result, Changes, Validation and Remaining blockers."

### general-purpose#D8-1
- severity: medium
- dimension: D8
- location: agents/general-purpose.md:15
- fix: Add the failure branch: if a gate or the acceptance check fails, fix the cause (or re-delegate with the failing output), rerun the same gates, and repeat at most N times. After that, report the failure under Validation and mark the work incomplete. As written, the 'validation fails' branch does not resolve to an action.

### general-purpose#D8-2
- severity: low
- dimension: D8
- location: agents/general-purpose.md:13
- fix: Renumber the ordered list 1-4, or restore the missing step 2, so the agent does not look for a step that does not exist.

### general-purpose#D4-1
- severity: high
- dimension: D4
- location: agents/general-purpose.md:3
- fix: Use the following folded-scalar field to repair YAML parsing and preserve the routing description:
description: >-
  Coordinate multi-file, multi-component programming work end to end: break the request down, delegate to matching specialists or implement directly, integrate their changes and run the project's verification gates. Use for complex multi-step debugging, implementation or refactoring that spans several files or components, or when specialist results need integrating and verifying, even if coordination is not requested. Not for trivial one-step edits or a focused single-domain task a dedicated specialist owns. Unlike the built-in general-purpose agent, it returns Result, Changes, Validation and Remaining blockers.

### general-purpose#D1-1
- severity: low
- dimension: D1
- location: agents/general-purpose.md:20
- fix: Keep the repo-specific trailer and checkout rules. Drop or shorten generic lines such as 'Read the output yourself' (line 15), which the model already follows, so expert content dominates the body.

### general-purpose#D2-1
- severity: medium
- dimension: D2
- location: agents/general-purpose.md:12
- fix: Split step 1 into separate phases: plan (owner, order, acceptance check), baseline (run the tests and record pre-existing failures) and reproduce (for bugs). Give each phase a 'before moving on, ask: ...' checkpoint so the Process pattern has clear phase boundaries.

### general-purpose#D3-1
- severity: low
- dimension: D3
- location: agents/general-purpose.md:26
- fix: Add environment-specific gotchas with reasons. Examples: a specialist whose frontmatter `tools` excludes Edit/Bash cannot apply or verify changes, so delegate verification elsewhere. Plugin agents ignore `permissionMode`, so a specialist may stall on a permission prompt.

### general-purpose#D6-1
- severity: low
- dimension: D6
- location: agents/general-purpose.md:12
- fix: Define 'clear' with a default. For example: fix without reproduction only when the defect is visible in a single code path and a test can be written that fails before the fix. Otherwise stop and report it under Remaining blockers.

### general-purpose#D1-1
- severity: medium
- dimension: D1
- location: agents/general-purpose.md:33
- fix: Consolidate routine verification reporting into the output contract: "Validation lists commands actually run, their observed outcomes, and required checks not run." Keep the separate orchestration-specific rules about overlapping worker files, unreliable specialist summaries, and checkout/revision provenance.
