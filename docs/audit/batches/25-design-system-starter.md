# Batch 25

## design-system-starter (skill)

### design-system-starter#D7-1
- severity: medium
- dimension: D7
- location: skills/design-system-starter/evals/evals.json:16
- fix: Add a token fixture with a cycle, a missing alias target, and an actual failing foreground/background pair. Assert that each defect is identified and corrected or explicitly blocks component implementation.

### design-system-starter#D7-2
- severity: medium
- dimension: D7
- location: skills/design-system-starter/evals/trigger-queries.json:23
- fix: Label the standalone modal audit as a near-miss negative, or rewrite the positive to specify reviewing a shared modal primitive used across the design system.

### design-system-starter#D8-1
- severity: high
- dimension: D8
- location: skills/design-system-starter/templates/component-template.tsx:38
- fix: Keep the button scaffold limited to valid phrasing content and remove its Header/Body members, or provide a separate non-interactive container scaffold for compound Header/Body composition. Validate the resulting DOM structure in a rendered example.

### design-system-starter#D7-1
- severity: low
- dimension: D7
- location: skills/design-system-starter/evals/evals.json:26
- fix: Add a small legacy-UI fixture under evals/files/ (a page with hardcoded hex values and icon-only buttons) and reference it in the eval's files so audit assertions are checkable against an actual input.

### design-system-starter#D8-1
- severity: low
- dimension: D8
- location: skills/design-system-starter/SKILL.md:24
- fix: State the no-rig fallback: when the project has no component test setup, do a keyboard-only and 200%-zoom pass on the pilot screen and say so, instead of leaving the check undefined.

### design-system-starter#D1-1
- severity: medium
- dimension: D1
- location: skills/design-system-starter/SKILL.md:16
- fix: Compress the standard token-category and documentation inventories into short output requirements. Keep the substantive guidance on selecting an adopter, validating theme-state pairs, limiting escape hatches, and preserving token meaning.

### design-system-starter#D5-1
- severity: medium
- dimension: D5
- location: skills/design-system-starter/SKILL.md:42
- fix: Load templates/component-template.tsx only when implementing a React component scaffold; explicitly skip it for token-only deliverables and other frameworks.

### design-system-starter#D6-1
- severity: medium
- dimension: D6
- location: skills/design-system-starter/checklists/design-system-checklist.md:365
- fix: Make the checklist scope-dependent, allow justified N/A entries, and gate release on the chosen pilot and supported distribution channels. Treat component inventories, publication platforms, and numeric budgets as project decisions rather than universal requirements.

### design-system-starter#D1-1
- severity: medium
- dimension: D1
- location: skills/design-system-starter/checklists/design-system-checklist.md:312
- fix: Cut Governance, Adoption & Maintenance, Pre-Launch and Post-Launch (lines 312-386) to the few items that gate design-system correctness; the model already knows generic program management, and by line count this dilutes the expert SKILL.md.

### design-system-starter#D2-1
- severity: low
- dimension: D2
- location: skills/design-system-starter/SKILL.md:19
- fix: Add a tie-breaker: when several patterns qualify equally, pick the one whose consuming screen is already scheduled for change this cycle, so adoption is measurable.

### design-system-starter#D3-1
- severity: low
- dimension: D3
- location: skills/design-system-starter/SKILL.md:35
- fix: Move this to-do into workflow step 8; a gotchas entry should be a mistake with a reason, e.g. "Never document a component by example alone — list props and states, or consumers copy the example's exact prop set."

### design-system-starter#D5-1
- severity: low
- dimension: D5
- location: skills/design-system-starter/SKILL.md:42
- fix: Gate it like the other three resources: "Load templates/component-template.tsx only when scaffolding a brand-new component; otherwise compose from the existing hierarchy."

### design-system-starter#D6-1
- severity: low
- dimension: D6
- location: skills/design-system-starter/SKILL.md:21
- fix: Name the verification method for this fragile check: computed-style assertions per theme and state (as in references/component-examples.md) or an axe contrast-rule run; thresholds alone leave the agent guessing how to measure.
