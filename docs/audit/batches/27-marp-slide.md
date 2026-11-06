# Batch 27

## marp-slide (skill)

### marp-slide#D7-1
- severity: medium
- dimension: D7
- location: skills/marp-slide/evals/evals.json:20
- fix: Add an existing-deck fixture and a multi-variant gradient/image case. Assert preserved requested content, resolved assets, readable contrast, absence of overflow, and truthful reporting when rendering is unavailable.

### marp-slide#D8-1
- severity: high
- dimension: D8
- location: skills/marp-slide/assets/template-gradient.md:38
- fix: Darken the bright gradient stops or place text on a sufficiently opaque dark surface. Apply the correction to both gradient assets and verify every variant, not only the title slide.

### marp-slide#D8-2
- severity: high
- dimension: D8
- location: skills/marp-slide/references/advanced-features.md:336
- fix: Update the artifact upload to a supported version such as actions/upload-artifact@v4, update the checkout action as appropriate, and verify that the example successfully uploads the generated PDF.

### marp-slide#D8-1
- severity: low
- dimension: D8
- location: skills/marp-slide/SKILL.md:17
- fix: Define the no-CLI path: lint frontmatter and _class directives against references/marp-syntax.md and verify image paths resolve before delivering Markdown.

### marp-slide#D1-1
- severity: medium
- dimension: D1
- location: skills/marp-slide/references/best-practices.md:9
- fix: Trim the generic presentation tutorial. Retain the bundled-style decisions, Marpit-specific layout behavior, export limitations, and concrete rendering failures that the agent would otherwise miss.

### marp-slide#D2-1
- severity: medium
- dimension: D2
- location: skills/marp-slide/SKILL.md:14
- fix: Branch the workflow into new-deck creation and existing-deck redesign. For redesign, inspect the current deck, identify what must be preserved, diagnose its rendered problems, and apply only the necessary template or CSS changes.

### marp-slide#D6-1
- severity: medium
- dimension: D6
- location: skills/marp-slide/references/best-practices.md:29
- fix: Replace the character limit with a rendered-fit principle: preserve complete claims, avoid distracting wrapping, and split content when the chosen font and layout become difficult to read.

### marp-slide#D1-1
- severity: low
- dimension: D1
- location: skills/marp-slide/references/marp-syntax.md:1
- fix: Trim the reference to non-obvious semantics (underscore per-slide scope, size directive, class pitfalls) and cut the directives table and basic examples the model already knows.

### marp-slide#D2-1
- severity: low
- dimension: D2
- location: skills/marp-slide/SKILL.md:13
- fix: Keep only the unspecified default inline and defer ambiguous cases to references/theme-selection.md with one named default when dark is requested (e.g., tech) and the other as alternate.

### marp-slide#D3-1
- severity: medium
- dimension: D3
- location: skills/marp-slide/SKILL.md:35
- fix: Add the missing expert gotcha: Marp CLI PDF/PPTX/image export requires Chrome/Chromium (or the official Docker image); in headless CI pass a container or --browser path, so state it in Marp gotchas.

### marp-slide#D6-1
- severity: low
- dimension: D6
- location: skills/marp-slide/SKILL.md:15
- fix: Give a concrete fallback heuristic for when rendering is unavailable (e.g., approximate word or bullet count per slide) so density is decidable without a render.
