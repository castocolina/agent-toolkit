# Batch 68

## mermaid-diagram-specialist (agent)

### mermaid-diagram-specialist#D8-1
- severity: medium
- dimension: D8
- location: agents/mermaid-diagram-specialist.md:19
- fix: Resolve the case where validation fails on a restyle-only request (step 3 says 'on failure fix'). For example: 'If the original fails to parse during a restyle, treat it as mixed: apply the minimal repair first, list it as a repair change, then restyle.' As written, step 3's fix conflicts with 'every label stays'.

### mermaid-diagram-specialist#D8-2
- severity: low
- dimension: D8
- location: agents/mermaid-diagram-specialist.md:17
- fix: Add an outcome for a wrong-meaning repair that comes with no source material, such as: 'If no source material was supplied, ask for it or return the specific relationships you could not verify, per step 2.' Without that, the comparison has nothing to check against.

### mermaid-diagram-specialist#D1-1
- severity: low
- dimension: D1
- location: agents/mermaid-diagram-specialist.md:21
- fix: Merge steps 3 and 4 into one line, such as '3. Run the skill's validation loop, then report.' The model already knows the generic draft-validate-fix loop, and the preloaded skill states it in full.

### mermaid-diagram-specialist#D2-1
- severity: medium
- dimension: D2
- location: agents/mermaid-diagram-specialist.md:14
- fix: Add a delegate-level decision for new diagrams, such as: 'If the material answers more than one question (for example both data model and request flow), return one diagram per question rather than one combined diagram, and say which question each answers.' The procedure has no rule for scope or splitting.

### mermaid-diagram-specialist#D3-1
- severity: medium
- dimension: D3
- location: agents/mermaid-diagram-specialist.md:24
- fix: Add a short Gotchas list of delegate-context facts. Example: 'The caller sees only your reply, not scratch .mmd/.svg files, so return the final source inline.' Example: 'A clean mmdc run does not prove that GitHub renders it, so name any version-specific construct.'

### mermaid-diagram-specialist#D6-1
- severity: low
- dimension: D6
- location: agents/mermaid-diagram-specialist.md:15
- fix: Add an escape hatch with a threshold, such as: 'Rewrite only when more than half the edges are wrong or the type itself is wrong, and say so in the change list.' Otherwise the agent cannot tell when a rewrite is allowed.

### mermaid-diagram-specialist#D1-1
- severity: low
- dimension: D1
- location: agents/mermaid-diagram-specialist.md:9
- fix: Remove that opening sentence from the body. Begin directly with the preloaded mermaid-diagrams skill’s authority, retaining the delegate-specific procedure, safeguards and output contract.
