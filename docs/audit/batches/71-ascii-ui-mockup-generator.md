# Batch 71

## ascii-ui-mockup-generator (agent)

### ascii-ui-mockup-generator#D8-1
- severity: medium
- dimension: D8
- location: agents/ascii-ui-mockup-generator.md:33
- fix: Make the example match its title and step 5. Either draw a sidebar next to the table or rename the example to 'Aligned table'. Also show the four rationale points as four bullets (Approach, Favors, Drawback, Best fit) instead of the single line '- Approach / Favors / Drawback / Best fit'.

### ascii-ui-mockup-generator#D8-2
- severity: low
- dimension: D8
- location: agents/ascii-ui-mockup-generator.md:20
- fix: Each task branch gives only 2 variants. Say where the third comes from, for example: 'When the dominant-task axis yields only two variants, take the third from the navigation-placement axis.'

### ascii-ui-mockup-generator#D8-1
- severity: medium
- dimension: D8
- location: agents/ascii-ui-mockup-generator.md:21
- fix: Define alignment in display cells rather than character counts. For Unicode layouts or non-ASCII labels, use a display-width-aware check that handles wide and combining characters, then repair and re-check. When rendered width cannot be verified, state that limitation and offer an ASCII/transliterated fallback rather than claiming the borders are validated.

### ascii-ui-mockup-generator#D1-1
- severity: low
- dimension: D1
- location: agents/ascii-ui-mockup-generator.md:43
- fix: Cut the generic wireframe notation (buttons, checkboxes, dropdowns): the model already uses these conventions. Keep only the non-obvious ones (scroll edge marks, modal as an inner box over the base screen).

### ascii-ui-mockup-generator#D2-1
- severity: low
- dimension: D2
- location: agents/ascii-ui-mockup-generator.md:23
- fix: Steps 5-6 are generic present-and-ask steps. Replace them with a domain decision, for example: before you ask, state which mockup you recommend for the top-ranked task and why. Then the step carries expert judgment.

### ascii-ui-mockup-generator#D3-1
- severity: low
- dimension: D3
- location: agents/ascii-ui-mockup-generator.md:48
- fix: Replace the check the agent cannot run (it cannot view a font) with a concrete gotcha: East Asian ambiguous-width and emoji characters take 2 columns in many terminals. Keep box-drawing lines free of such characters, and count wide characters as 2 when checking row lengths.

### ascii-ui-mockup-generator#D1-1
- severity: medium
- dimension: D1
- location: agents/ascii-ui-mockup-generator.md:18
- fix: Condense the requirements, rationale and selection scaffolding and the elementary table example into a compact output contract. Retain the dominant-task decision rules, and strengthen the knowledge delta with a concrete prioritization rule for which fields to retain, abbreviate or move to detail when comparison fields and primary actions compete for width.
