# Batch 47

## ui-ux-principles (skill)

### ui-ux-principles#D7-1
- severity: low
- dimension: D7
- location: skills/ui-ux-principles/evals/trigger-queries.json:131
- fix: Replace the duplicate with a different near-miss negative, such as 'Add analytics click tracking to every button on the pricing page'. Also add an a11y/interaction assertion to review-tailwind-vue-card so all eight rows of that eval are checked.

### ui-ux-principles#D8-1
- severity: medium
- dimension: D8
- location: skills/ui-ux-principles/SKILL.md:30
- fix: Name a default way to render, with a fallback. For example: 'Default: run the dev server and take a screenshot at 360/768/1280/1920 with Playwright (or the harness browser tool), and tab once to capture the focus ring. With no runnable app, list each as unverified: needs render.' Without it, the agent guesses how to verify, or quietly skips verification.

### ui-ux-principles#D8-1
- severity: high
- dimension: D8
- location: skills/ui-ux-principles/SKILL.md:99
- fix: Apply evidence-sufficiency checks to every input combination. Fail proven violations, pass only when all applicable criteria are established, and otherwise use na with the missing observation identified. Remove the blanket claim that loading never needs runtime evidence, and explicitly allow unverified CLS or timing checks.

### ui-ux-principles#D1-1
- severity: low
- dimension: D1
- location: skills/ui-ux-principles/SKILL.md:64
- fix: Cut the WCAG ratio recital, which the model already knows, to 'WCAG AA in every theme, non-text included'. Keep the non-obvious parts: 'in every theme', 'names contain the visible text' and the 24 px fail line versus the 44 px target.

### ui-ux-principles#D2-1
- severity: low
- dimension: D2
- location: skills/ui-ux-principles/SKILL.md:40
- fix: Turn each three-way verdict in a Rule line (responsive, loading) into a short ordered decision list, such as 1. shows overflow cause -> fail, 2. normal flow with nothing over 360 px and the primary action in flow -> pass, 3. else -> na unverified. This keeps the Tool pattern's decision-tree form instead of dense prose.

### ui-ux-principles#D3-1
- severity: medium
- dimension: D3
- location: skills/ui-ux-principles/SKILL.md:46
- fix: Add a short '## Gotchas' in SKILL.md for the cross-rule facts every review needs: a MUI Button with no variant is text and never counts as filled, while a custom .btn with a background does; a retry must clear the error before it refetches. The reference files only load on condition, so these facts are missing when the hierarchy or states rows are decided without them.

### ui-ux-principles#D4-1
- severity: low
- dimension: D4
- location: skills/ui-ux-principles/SKILL.md:3
- fix: Apply eight pass/fail UI/UX rules (loading, responsive, hierarchy, tokens, consistency, a11y, states, interaction) when building or changing a screen, and return a rule | pass/fail/na | evidence | fix table on review. Use when building, changing or reviewing any UI screen or component in React, Vue, Svelte, HTML/CSS, MUI or Tailwind: skeleton vs spinner, empty and error states, mobile layout, button hierarchy, hard-coded colors, dark mode without per-component overrides, WCAG contrast, focus rings, tap targets, icon-button names, hover/focus-visible/disabled states. Trigger even on 'review this page', 'make this look polished', 'why does this feel off' or 'fix the layout'. Not for backend or API work, copywriting, brand or logo design, scaffolding a design system or token pipeline (design-system-starter), or the MUI theme API and Grid migration (mui).

### ui-ux-principles#D1-1
- severity: medium
- dimension: D1
- location: skills/ui-ux-principles/SKILL.md:25
- fix: Condense the familiar theme, request-state and shared-control preflight reminders into one ordered checklist. Preserve the eight pass lines, custom exceptions, evidence routing and non-obvious framework/live-region gotchas rather than repeating general UI advice around them.

### ui-ux-principles#D6-1
- severity: medium
- dimension: D6
- location: skills/ui-ux-principles/SKILL.md:28
- fix: Make fluid sizing the default, but permit fixed preferred widths constrained by max-width, wrapping or breakpoint changes. Fail widths when they cause page-level overflow or an unreachable primary action, rather than failing every fixed-width declaration.
