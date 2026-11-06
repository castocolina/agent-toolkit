# Batch 63

## codebase-pattern-finder (agent)

### codebase-pattern-finder#D1-1
- severity: high
- dimension: D1
- location: agents/codebase-pattern-finder.md:50
- fix: Delete the native-tool pep talk and generic responsibility/category inventories. Retain the documentarian boundary and source-evidence requirements; replace generic exposition with concise, non-obvious rules for identifying genuinely comparable implementations.

### codebase-pattern-finder#D5-1
- severity: high
- dimension: D5
- location: agents/codebase-pattern-finder.md:58
- fix: Reduce the agent to at most 200 lines. If retaining the detailed report examples, move them into a dedicated reporting skill, preload it through `skills: [pattern-report-format]`, and leave only a compact output schema in the agent.

### codebase-pattern-finder#D7-1
- severity: medium
- dimension: D7
- location: agents/codebase-pattern-finder.md:225
- fix: Add: "The task is done when each requested pattern type has source-verified examples or an explicit no-match result, every example has a file:line citation, and the final report follows the Output Format."

### codebase-pattern-finder#D8-1
- severity: high
- dimension: D8
- location: agents/codebase-pattern-finder.md:36
- fix: Replace "Note which approach is preferred" with "Describe observed variations without inferring or recommending a preferred approach."

### codebase-pattern-finder#D8-2
- severity: medium
- dimension: D8
- location: agents/codebase-pattern-finder.md:53
- fix: If initial searches fail, broaden once using behavior synonyms and callers; if no examples remain, report the searched scope and an explicit no-match result. If implementations exist but relevant tests cannot be found, state that limitation and return the verified implementation examples without inventing tests.

### codebase-pattern-finder#D8-3
- severity: high
- dimension: D8
- location: agents/codebase-pattern-finder.md:111
- fix: In the illustrative handlers, parse and validate numeric query parameters before arithmetic and database calls. Require positive integer limits and pages, and check a non-default `?limit=20` case so the cursor query requests 21 records rather than "201".

### codebase-pattern-finder#D2-1
- severity: medium
- dimension: D2
- location: agents/codebase-pattern-finder.md:42
- fix: Add a selection procedure: identify the requested behavior, runtime/framework, and architectural layer; inspect candidate callers and tests; distinguish live implementations from fixtures or wrappers; then report relevant similarities and differences without ranking quality.

### codebase-pattern-finder#D3-1
- severity: medium
- dimension: D3
- location: agents/codebase-pattern-finder.md:214
- fix: Add reasoned gotchas, such as: when generated or vendored hits appear, do not count their copies as independent local implementations, because one upstream source can falsely look like a repository-wide convention; label provenance and trace copies to their maintained source.

## sync-skills-readme (command)

### sync-skills-readme#D7-1
- severity: high
- dimension: D7
- location: commands/sync-skills-readme.md
- fix: Add commands/evals/sync-skills-readme.json with at least three realistic scenarios and verifiable assertions: inventory changes with correct rows, links and ordering; missing frontmatter or a missing target section with the specified warning or stop behavior; and an edge case such as folded descriptions containing pipes. Assert that content outside the table remains unchanged.

### sync-skills-readme#D8-1
- severity: high
- dimension: D8
- location: commands/sync-skills-readme.md:89
- fix: Replace the shortened example with 'Code analysis, refactoring & automated edits'. Require summaries to retain only capabilities and factual details supported by the extracted metadata; do not introduce model versions or context limits from the illustrative table.

### sync-skills-readme#D8-2
- severity: medium
- dimension: D8
- location: commands/sync-skills-readme.md:98
- fix: Locate and replace only the table header, delimiter and contiguous table rows beneath the existing heading. Preserve the heading, separators, following prose and all attribution. Stop without editing if the table cannot be identified unambiguously. After editing, reread the result and verify row counts and unchanged content outside the table before reporting success.

### sync-skills-readme#D1-1
- severity: medium
- dimension: D1
- location: commands/sync-skills-readme.md:13
- fix: Condense directory enumeration and frontmatter extraction into one instruction, and remove the repeated tool catalog and basic YAML example. Retain the category mapping, precedence, table schema, sorting, edit boundaries and failure policies.

### sync-skills-readme#D2-1
- severity: medium
- dimension: D2
- location: commands/sync-skills-readme.md:59
- fix: Document the intended rationale for category precedence and provide an overlapping-keyword example showing why one category wins. Explain how to extend the mapping without unintentionally shadowing later categories.

### sync-skills-readme#D3-1
- severity: medium
- dimension: D3
- location: commands/sync-skills-readme.md:139
- fix: Add a brief Gotchas section: preserve folded and literal YAML descriptions when extracting metadata; escape pipes and normalize newlines before generating table cells; and resolve links from the actual directory path rather than assuming the metadata name is the path. Explain the truncation, malformed-table and broken-link failures these rules prevent.

### sync-skills-readme#D4-1
- severity: medium
- dimension: D4
- location: commands/sync-skills-readme.md:2
- fix: Synchronize the root README.md Available Skills table with metadata from skills/*/SKILL.md. Use after adding, removing, renaming or updating skills, or when the inventory table is stale. Regenerate categorized skill links and concise descriptions; not for rewriting other README sections.
