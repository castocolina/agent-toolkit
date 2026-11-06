# Batch 83

## codebase-pattern-finder (agent)

### codebase-pattern-finder#D8-1
- severity: medium
- dimension: D8
- location: agents/codebase-pattern-finder.md:19
- fix: Resolve the branch where the caller names no pattern type: 'If the caller names no type, treat the request as one feature pattern plus its Testing Patterns; do not search structural or integration types unless asked.' This also fixes which types the step-4 no-match lines must list.

### codebase-pattern-finder#D1-1
- severity: low
- dimension: D1
- location: agents/codebase-pattern-finder.md:15
- fix: Delete this NEVER item. The `tools: Grep, Glob, Read, LS` allowlist already enforces it, so the line repeats what the harness does.

### codebase-pattern-finder#D2-1
- severity: low
- dimension: D2
- location: agents/codebase-pattern-finder.md:19
- fix: Add a search-order step before step 1: search by identifier and by behavior synonyms, resolve each hit to its defining file, then open its callers and tests. This gives the agent a domain sequence rather than a list of categories.

### codebase-pattern-finder#D3-1
- severity: low
- dimension: D3
- location: agents/codebase-pattern-finder.md:13
- fix: Add the reason, like the other NEVER items have: for example, 'because a guessed rationale or critique gets read as the repository's documented intent'.
