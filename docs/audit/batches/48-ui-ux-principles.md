# Batch 48

## ui-ux-principles (skill)

### ui-ux-principles#D7-1
- severity: low
- dimension: D7
- location: skills/ui-ux-principles/evals/evals.json
- fix: Add one eval with a product grid that repeats a filled Add to cart, plus a delete dialog with a filled Delete. Assert hierarchy pass for the grid with the list map cited, and hierarchy fail for the dialog with the fix 'make Delete outlined with the danger role'.

### ui-ux-principles#D8-1
- severity: medium
- dimension: D8
- location: skills/ui-ux-principles/SKILL.md:12
- fix: Taken literally, the route skips step 1 (the non-UI exit) and step 2 (the Actions/Layout/Requests questions). On a build branch an agent then picks the fill and the destructive-action treatment without the step 2 reasoning. Change it to: 'Route: always run steps 1-2, then build or fix → step 3; review, verdict or diagnostic → step 4; review and fix → step 4, then step 3; finish edits with step 5.'

### ui-ux-principles#D8-1
- severity: high
- dimension: D8
- location: skills/ui-ux-principles/SKILL.md:50
- fix: Determine source-only responsive verdicts from the resolved outer box and available containing-block width, including padding, borders, margins, box-sizing and flex shrinking. Explicitly reject the 350px-plus-padding example; require a render when those dimensions cannot be established.

### ui-ux-principles#D1-1
- severity: low
- dimension: D1
- location: skills/ui-ux-principles/SKILL.md:95
- fix: Cut the outline:none clause, because current models already know it. Keep only the non-obvious traps on this line: the Tailwind `hover:` wrapping in @media (hover: hover) and the disabled-colour non-fail.

### ui-ux-principles#D2-1
- severity: low
- dimension: D2
- location: skills/ui-ux-principles/SKILL.md:8
- fix: This is a Tool-pattern skill but it has no code example in SKILL.md. Add one short passing snippet, for example an MUI list with a Skeleton region with aria-busy, an error branch with retry, an empty-mounted role="status" and one contained button, so the agent can match against working code.

### ui-ux-principles#D3-1
- severity: low
- dimension: D3
- location: skills/ui-ux-principles/SKILL.md:154
- fix: Add a short `## Gotchas` section next to NEVER that collects the cross-rule facts an agent misses: fetch resolves on 404/500; a MUI Button with no variant is text; an sx string is a literal but a number multiplies theme.spacing; Tailwind hover: never fires on touch.

### ui-ux-principles#D4-1
- severity: low
- dimension: D4
- location: skills/ui-ux-principles/SKILL.md:3
- fix: Apply eight pass/fail UI/UX rules (loading, responsive, hierarchy, tokens, consistency, accessibility, states, interaction) when building or changing a screen, and return a rule | pass/fail/na | evidence | fix table on review. Use when building, fixing or reviewing any UI screen or component in React, Vue, Svelte, HTML/CSS, MUI or Tailwind: loading skeletons, empty and error states, mobile layout, button emphasis, hard-coded colors, dark mode, WCAG contrast, focus rings, tap targets. Trigger even on 'review this page', 'make this look polished', 'why does this feel off' or 'fix the layout'. Not for backend or API work, copywriting, brand or logo design, scaffolding a design system (design-system-starter), or the MUI theme API and Grid migration (mui).

### ui-ux-principles#D6-1
- severity: medium
- dimension: D6
- location: skills/ui-ux-principles/SKILL.md:30
- fix: Keep the rigid eight-row table for explicit review or verdict requests. For an open diagnostic question, add an escape hatch: answer in the summary line, show only the failing rows, and offer the full table, so a casual question does not get a full audit format.

### ui-ux-principles#D1-1
- severity: medium
- dimension: D1
- location: skills/ui-ux-principles/SKILL.md:78
- fix: Compress the conventional accessible-name, keyboard, shared-component and token guidance into a brief activation checklist. Preserve the label-in-name and target-size distinctions, framework-specific traps, live-region timing, and source-versus-render decision criteria.
