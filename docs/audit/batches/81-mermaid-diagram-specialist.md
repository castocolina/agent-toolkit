# Batch 81

## mermaid-diagram-specialist (agent)

### mermaid-diagram-specialist#D8-1
- severity: medium
- dimension: D8
- location: agents/mermaid-diagram-specialist.md:15
- fix: Add a branch for a diagram that has both problems: 'If it both fails to parse and has wrong meaning, fix parsing first, then check meaning against the source material, and report both change lists.' The current branch treats the two cases as mutually exclusive.

### mermaid-diagram-specialist#D1-1
- severity: low
- dimension: D1
- location: agents/mermaid-diagram-specialist.md:34
- fix: Shorten this to 'Return the final source inline.' A subagent already knows that only its reply reaches the caller, so keep the instruction and drop the explanation.

### mermaid-diagram-specialist#D2-1
- severity: medium
- dimension: D2
- location: agents/mermaid-diagram-specialist.md:21
- fix: Move this check to step 1, before 'Name the task kind'. As written, the agent picks a diagram type or starts a repair before it checks whether the request is for Mermaid at all and whether the material can support a diagram.

### mermaid-diagram-specialist#D3-1
- severity: low
- dimension: D3
- location: agents/mermaid-diagram-specialist.md:35
- fix: Name the constructs that usually break, for example the `architecture-beta` diagram type and C4 diagrams, which may validate locally but not render in GitHub's pinned Mermaid version. Then the agent knows which constructs to flag.
