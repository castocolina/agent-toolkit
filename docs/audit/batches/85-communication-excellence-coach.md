# Batch 85

## communication-excellence-coach (agent)

### communication-excellence-coach#D8-1
- severity: medium
- dimension: D8
- location: agents/communication-excellence-coach.md:43
- fix: Add an outcome for when the counterpart has no plausible concern left before the agreed exchange count: 'If no plausible new concern remains, have the counterpart accept the ask, end the roleplay early and give Coach Feedback.' Also add a fallback for a draft file path that Read cannot open: say so and ask the user to paste the text.

### communication-excellence-coach#D1-1
- severity: low
- dimension: D1
- location: agents/communication-excellence-coach.md:26
- fix: Replace this generic presentation advice with a fact the model would miss. Example: architecture-review decks that put the options before the recommendation get derailed by debate on option 1. Lead with the recommendation and the decision deadline.

### communication-excellence-coach#D2-1
- severity: low
- dimension: D2
- location: agents/communication-excellence-coach.md:26
- fix: Give outline review an ordered procedure like the draft path has. Step 1: name the audience's decision. Step 2: check that each slide or section earns its place against that decision. Step 3: flag the slide where the ask first appears. If it appears after the midpoint, list it under Biggest risk.

### communication-excellence-coach#D3-1
- severity: low
- dimension: D3
- location: agents/communication-excellence-coach.md:60
- fix: Add the non-obvious reason, as the other NEVER items do. For example: 'the user owns relationship risk; a message sent or a file changed by the coach cannot be unsent, and the user loses the chance to adjust voice.'

### communication-excellence-coach#D6-1
- severity: low
- dimension: D6
- location: agents/communication-excellence-coach.md:43
- fix: Let the counterpart's tone follow the role and relationship the user gave, not a fixed mood. Change (4) to 'resolved -> raise the next plausible concern for this counterpart, in a tone that fits their role', and keep the fixed tones only for branches (1)-(3), where they signal pushback.
