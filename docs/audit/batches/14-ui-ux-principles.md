# Batch 14

## ui-ux-principles (skill)

### ui-ux-principles#D8-1
- severity: medium
- dimension: D8
- location: skills/ui-ux-principles/SKILL.md:78
- fix: Define a render-only review branch with screenshot/viewport/region evidence. Provide an explicit unverified outcome for code-dependent checks, and require file:line evidence only when source is available.

### ui-ux-principles#D7-1
- severity: low
- dimension: D7
- location: skills/ui-ux-principles/evals/evals.json
- fix: Add two evals: a Tailwind or Vue component with `dark:` patches and arbitrary values like `bg-[#3b82f6]`, asserting consistency and tokens fail, and a component where a table scrolls inside its own container, asserting responsive passes.

### ui-ux-principles#D8-1
- severity: medium
- dimension: D8
- location: skills/ui-ux-principles/SKILL.md:21
- fix: Make both say the same thing: "A pending submit disables its button at once; the in-button indicator may appear after about 1 s."

### ui-ux-principles#D8-2
- severity: low
- dimension: D8
- location: skills/ui-ux-principles/SKILL.md:40
- fix: State the verdict: "No theme in the repo: tokens is fail, with evidence naming the literal and the fix 'add a theme role'."

### ui-ux-principles#D1-1
- severity: medium
- dimension: D1
- location: skills/ui-ux-principles/SKILL.md:27
- fix: Compress familiar mobile-first, component-reuse and interaction guidance into a brief activation checklist. Preserve the task-specific decision policies, defect ownership, accessibility exceptions and framework gotchas that materially change the agent's decisions.

### ui-ux-principles#D2-1
- severity: medium
- dimension: D2
- location: skills/ui-ux-principles/SKILL.md:13
- fix: Add a brief goal-and-risk check when context is unclear: identify the primary user task, intended completion action and cost of a mistaken action, then use those answers to choose prominence and recovery behavior.

### ui-ux-principles#D6-1
- severity: medium
- dimension: D6
- location: skills/ui-ux-principles/SKILL.md:83
- fix: Make one filled action the default rather than a universal constraint. Permit justified exceptions based on independent user tasks or the existing design system, while retaining mandatory accessibility and functional-state checks.

### ui-ux-principles#D1-1
- severity: low
- dimension: D1
- location: skills/ui-ux-principles/SKILL.md:27
- fix: Shorten these Rule lines to the non-obvious pass lines only, such as the 360/768/1280/1920 test matrix and container-scoped scroll. Drop the restated mobile-first and token basics.

### ui-ux-principles#D2-1
- severity: medium
- dimension: D2
- location: skills/ui-ux-principles/SKILL.md:16
- fix: Add a short build checklist: theme located, state branches written, names and keyboard path checked, literals moved to the theme, renders done or listed as not rendered. Each item should carry a one-line reason, so build mode gets the same ordered procedure as review mode.

### ui-ux-principles#D3-1
- severity: medium
- dimension: D3
- location: skills/ui-ux-principles/SKILL.md:101
- fix: Add a reason to each Trap. Lift the two or three highest-impact gotchas into SKILL.md so the agent reads them before the trigger appears: MUI Skeleton has no ARIA, sx string values are literals, Tailwind arbitrary values are literals.

### ui-ux-principles#D6-1
- severity: low
- dimension: D6
- location: skills/ui-ux-principles/SKILL.md:40
- fix: Replace it with a default plus an escape hatch: "No theme in the repo: on a review, fail tokens and name the missing role; on a build, create one :root custom-property block for the new roles, tell the user, and continue."
