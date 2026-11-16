# Batch 73

## communication-excellence-coach (agent)

### communication-excellence-coach#D8-1
- severity: medium
- dimension: D8
- location: agents/communication-excellence-coach.md:67
- fix: feedback-mastery is preloaded via `skills:` (line 9), so a handoff to it does not resolve: the agent cannot tell whether to deliver structured feedback itself or decline. Replace it with: 'Structured feedback: apply the preloaded feedback-mastery skill (SBI) inside Review or Roleplay; hand off only when the user wants a feedback document written from scratch (`/compose-email` for an email).'

### communication-excellence-coach#D8-2
- severity: low
- dimension: D8
- location: agents/communication-excellence-coach.md:18
- fix: Add a rule for the case the router misses, when the user has talking points or a draft and also has an upcoming conversation: 'Draft plus upcoming conversation -> Review first, then offer Roleplay using the revised wording.'

### communication-excellence-coach#D8-1
- severity: medium
- dimension: D8
- location: agents/communication-excellence-coach.md:41
- fix: Add an explicit branch: when the ask is retained but the objection remains unresolved, stay with the same concern and probe the missing constraint, evidence or trade-off; advance to a new concern only after the current one is addressed.

### communication-excellence-coach#D1-1
- severity: low
- dimension: D1
- location: agents/communication-excellence-coach.md:58
- fix: Delete this line. The frontmatter `tools: Read, Glob, Grep` already makes the agent read-only, and the line 14 sentence 'You suggest; the user decides and sends' already covers sending. Use the freed line for a non-obvious communication gotcha.

### communication-excellence-coach#D1-2
- severity: low
- dimension: D1
- location: agents/communication-excellence-coach.md:57
- fix: Keep only the non-obvious half: 'flag a factual gap and ask rather than fill it.' Cut the generic 'do not over-rewrite' advice, or give a concrete limit, for example 'keep at least the user's opening and closing sentences unless they carry the biggest risk.'

### communication-excellence-coach#D2-1
- severity: medium
- dimension: D2
- location: agents/communication-excellence-coach.md:18
- fix: Give presentation outlines their own short procedure. For example: 'For an outline, check in order: (1) does the decision or ask come in the first slide or minute, (2) does every section answer a question the audience has at that point, (3) is there a fallback if the room rejects the main option. Report each gap as a structure suggestion.' Today the outline branch gets only a category label and no expert sequence.

### communication-excellence-coach#D3-1
- severity: low
- dimension: D3
- location: agents/communication-excellence-coach.md:60
- fix: Add one or two more gotchas from real experience. For example: 'A Slack message that opens with only "hey, got a minute?" leaves the reader anxious and idle: put the ask in the same message.' Or: 'In an architecture review, "we could consider" reads as optional to senior readers: state the recommendation as the recommendation.'

### communication-excellence-coach#D1-1
- severity: low
- dimension: D1
- location: agents/communication-excellence-coach.md:54
- fix: Consolidate the duplicated uncertainty, SBI and factual-fidelity explanations into a brief instruction to apply the preloaded skills' accuracy and SBI gates. Keep the coach-specific risk prioritization, safety-flag preservation and roleplay rules.
