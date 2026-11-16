# Batch 52

## design-system-starter (skill)

### design-system-starter#D7-1
- severity: medium
- dimension: D7
- location: skills/design-system-starter/evals/evals.json:37
- fix: Make the assertion verifiable: 'Lists at least one button text/background pair from legacy-settings.html with its hex values and computed ratio, marks it below 4.5:1, and names a passing replacement token'. Also add an assertion to casual-brand-kit that a component documentation guide lists props, defaults and states.

### design-system-starter#D8-1
- severity: medium
- dimension: D8
- location: skills/design-system-starter/SKILL.md:24
- fix: Add a short runnable resolver next to the contrast script, for example a python3 heredoc that loads the token JSON, follows each `{a.b.c}` reference, and prints a JSON list of cycles and missing targets. Then the blocking alias check (the broken-tokens eval branch) is mechanical rather than traced by hand.

### design-system-starter#D8-1
- severity: high
- dimension: D8
- location: skills/design-system-starter/SKILL.md:41
- fix: Preserve foreground alpha with `formatHex8(toGamut('rgb', 'oklch')(parse(value)))` and pass that eight-digit hex to the existing compositing calculation. Require translucent backgrounds to be resolved over their actual underlying surface before using the opaque-background calculation.

### design-system-starter#D7-1
- severity: medium
- dimension: D7
- location: skills/design-system-starter/evals/evals.json:9
- fix: Add verifiable assertions to the token-generating cases requiring JSON parseability and validation against the selected token format, including object-valued colors and dimensions for DTCG 2025.10. Include an older-toolchain case that permits legacy strings only when the output explicitly selects that compatibility format.

### design-system-starter#D1-1
- severity: low
- dimension: D1
- location: skills/design-system-starter/SKILL.md:60
- fix: Delete this gotcha or cut it to one line pointing to a tested dialog primitive. Current models already know the standard modal-dialog requirements, and nothing in the line is specific to design systems.

### design-system-starter#D2-1
- severity: low
- dimension: D2
- location: skills/design-system-starter/SKILL.md:44
- fix: Add a decision question for promoting a component to the next level, for example: 'Before promoting a pattern to the shared library, ask: do two consumers already use it with the same props? If not, keep it local to the pilot.'

### design-system-starter#D3-1
- severity: low
- dimension: D3
- location: skills/design-system-starter/SKILL.md:55
- fix: Replace this general documentation advice with a concrete design-system failure learned from real use, such as a token-build or theme-switch mistake seen in the evals. Keep the gotcha list for facts that defy reasonable assumptions.

### design-system-starter#D4-1
- severity: low
- dimension: D4
- location: skills/design-system-starter/SKILL.md:3
- fix: Set up or evolve a shared design system - semantic design tokens (DTCG .tokens.json, CSS custom properties), light/dark token themes, reusable component APIs (atoms, molecules, organisms), contrast-checked token pairs, and versioned migration off scattered styles. Use when asked to create a design system or token file, convert raw values into semantic tokens, standardize UI across apps or teams, define component library conventions, or version and deprecate shared tokens and components, even if the user only says the screens look inconsistent or all over the place and never says 'design system' or 'tokens'. Not for reviewing or fixing one screen or component against UI rules (ui-ux-principles), one-off pages, ARIA how-to questions in an existing form, Storybook stories for existing components, SVG icon optimization, logos, or marketing copy.

### design-system-starter#D6-1
- severity: low
- dimension: D6
- location: skills/design-system-starter/SKILL.md:41
- fix: Give the gamut conversion as an exact command with a pinned version, as the hex contrast path already does, for example: `npx -y -p culori@4 node --input-type=module -e "import {parse,toGamut,formatHex} from 'culori'; console.log(formatHex(toGamut('rgb','oklch')(parse(process.argv[1]))))" 'oklch(0.6 0.2 250)'`. This fragile step currently has less guidance than the easy one.

### design-system-starter#D1-1
- severity: low
- dimension: D1
- location: skills/design-system-starter/references/component-examples.md:110
- fix: Replace the generic union/lookup demonstration with a compact renamed-token or deprecated-prop alias example showing the old contract remaining functional through the next major release and its announced removal in the following major.
