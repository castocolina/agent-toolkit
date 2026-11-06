# Batch 69

## codebase-pattern-finder (agent)

### codebase-pattern-finder#D8-1
- severity: medium
- dimension: D8
- location: agents/codebase-pattern-finder.md:49
- fix: Resolve the branch where the 'smallest self-contained section' (line 20) runs past 40 lines. For example: 'If the smallest working section exceeds 40 lines, quote the signature and the key 40 lines, mark the omissions with `// ... (lines N-M omitted)`, and cite the full range in **Found in**.'

### codebase-pattern-finder#D8-1
- severity: medium
- dimension: D8
- location: agents/codebase-pattern-finder.md:50
- fix: Make 40 lines the default rather than an absolute limit: permit the smallest complete verbatim section to exceed it when necessary, with a brief explanation, or explicitly allow multiple linked excerpts labeled as partial and cite the complete implementation.

### codebase-pattern-finder#D1-1
- severity: low
- dimension: D1
- location: agents/codebase-pattern-finder.md:18
- fix: Cut the generic category list. Keep only the non-obvious part: "always open the callers and the tests that exercise each candidate".

### codebase-pattern-finder#D2-1
- severity: low
- dimension: D2
- location: agents/codebase-pattern-finder.md:21
- fix: Add a search strategy to step 1 for the first pass, not only for the fallback. For example: grep the identifier or API name first, then the import or call sites, then the test directory. This turns the procedure into an expert search order.

### codebase-pattern-finder#D3-1
- severity: low
- dimension: D3
- location: agents/codebase-pattern-finder.md:14
- fix: Replace this NEVER item. The `tools:` allowlist already enforces it. Use a landmine instead, for example: 'Never cite a line range from a file you read with an offset or limit without checking the full snippet boundaries: a truncated read cuts a function mid-body.'

### codebase-pattern-finder#D1-1
- severity: low
- dimension: D1
- location: agents/codebase-pattern-finder.md:50
- fix: State the non-ranking prohibition once under Never. Retain file-path ordering and the factual-differences example, but remove the repeated ranking prohibitions from the procedure and closing guidance.
