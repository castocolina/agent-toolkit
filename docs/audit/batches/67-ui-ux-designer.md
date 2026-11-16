# Batch 67

## ui-ux-designer (agent)

### ui-ux-designer#D8-1
- severity: medium
- dimension: D8
- location: agents/ui-ux-designer.md:56
- fix: State where a screen finding outside the eight rules goes (a task-flow, navigation or onboarding break from step 4). The skill forbids any second list, so add: 'Findings outside the eight rules go in a list after the summary line: finding, evidence or judgment, priority, fix.' Also say what priority a pass or na row gets ('none').

### ui-ux-designer#D8-2
- severity: medium
- dimension: D8
- location: agents/ui-ux-designer.md:29
- fix: Resolve the mixed input, such as two mockups plus 'which is better?': 'When both a screen and a decision are given, run step 2 on each screen, then step 3 on the choice. Output the table per screen, then the decision list.'

### ui-ux-designer#D8-1
- severity: high
- dimension: D8
- location: agents/ui-ux-designer.md:41
- fix: Replace the blanket code limitation with an evidence-dependent instruction: resolve imported styles and theme values in every shipped theme, and inspect interaction styles and request branches before assigning verdicts. Mark only unresolved colors, unobserved runtime behavior and unrendered layout as unverified; preserve source-proven passes and failures.

### ui-ux-designer#D1-1
- severity: low
- dimension: D1
- location: agents/ui-ux-designer.md:37
- fix: Cut the Stance section to one operational rule the model would not apply unprompted, for example: 'When the user's preferred option loses on task success, say so first and give the evidence, before any praise.' The model already defaults to being candid and evidence-led.

### ui-ux-designer#D2-1
- severity: low
- dimension: D2
- location: agents/ui-ux-designer.md:30
- fix: Add a thinking step for the flow critique that the description promises (navigation, onboarding): 'Before ranking, ask where the primary task stalls: entry, wayfinding, commitment or recovery, and which screen causes it.' The skill's eight rules do not cover these.

### ui-ux-designer#D3-1
- severity: low
- dimension: D3
- location: agents/ui-ux-designer.md:33
- fix: Add a NEVER item with its reason: 'NEVER use a 5-user test to pick a winner between alternatives: it finds usability problems but has no statistical power to compare success rates. Use it to find failures, and use A/B or a larger sample to choose.'

### ui-ux-designer#D1-1
- severity: medium
- dimension: D1
- location: agents/ui-ux-designer.md:37
- fix: Compress the general candidness and research-integrity reminders, retaining their safeguards. Add a compact UX-specific validation decision rule: use moderated task observation for discoverability failures, instrumentation for locating funnel loss, and randomized experiments for causal improvement claims; state what evidence each method cannot establish.
