---
name: marp-slide
description: Create or redesign Marp Markdown slide decks with seven bundled visual styles, embedded CSS, and Marpit image layouts. Use for slides, presentation decks, lectures, seminars, or better slide design, even without naming Marp. Supports custom themes and requests to improve an existing deck. Not for editing PowerPoint files, summarizing presentations, standalone speaker scripts, or conversion-only requests.
---

# Marp Slide Creator

Create Markdown slide decks with Marp/Marpit. Templates have embedded styling.

## Workflow

1. Establish the audience's intended decision or learning outcome and the deck topic. If either is missing or too vague to ground a deck, ask a focused question for the specific topic and/or audience before drafting; never invent a topic from sparse input. Derive a claim–evidence–action outline; each slide must advance that outcome. Do not borrow a template's sample narrative.
2. Select a bundled style: technical → tech; business → business; creative → colorful/gradient; academic → minimal; unspecified → default; dark requested → dark/tech. See `references/theme-selection.md` only when ambiguous.
3. Start from `assets/template-*.md` (basic, minimal, colorful, dark, gradient, tech, business). Keep its embedded CSS; style labels are not necessarily registered Marp theme names.
4. Choose statement, diagram, code, quote, list, or image layouts as appropriate. For list slides, use concise headings and no more than five bullets per slide; split or restructure a denser checklist instead of squeezing it into columns. Judge density by rendered readability and available space.
5. Load `references/marp-syntax.md` only when unsure about directives or `_class` semantics; `references/image-patterns.md` for images; `references/advanced-features.md` for math, fragments, or export; `references/theme-css-guide.md` for custom CSS. Load `references/best-practices.md` when diagnosing visual quality.
6. Review a rendered deck when Marp CLI is available; fix contrast, overflow, missing assets, and placeholders, then render again. Check every gradient variant.
7. Save at the user's requested path; otherwise use a suitable workspace output directory. Use `/mnt/user-data/outputs/` only if it exists. Report actual path, or provide Markdown if writing is unavailable.

## Marp gotchas

- Never assume a bundled style label is a registered Marp theme; template CSS is embedded and self-contained.
- Progressive/fragmented lists are HTML/browser-only; they do not survive PDF/PPTX export.
- For offline export, do not rely only on downloaded fonts; include a usable local/system fallback.

## Image layouts

Use `![bg right:40%](image.png)` for an image region beside text, `![bg](image.png)` for a background, and ordinary sized images for inline figures. Consult `references/image-patterns.md` for split backgrounds and filters.

## Quality check

- Marp frontmatter and embedded template styling are present.
- Narrative advances the stated outcome; no sample placeholders remain.
- Images resolve; rendered slides have readable contrast and no overflow.
- Check export-specific behavior if delivering PDF/PPTX.

## References

- `references/theme-selection.md`: read for ambiguous theme selection.
- `references/marp-syntax.md`: read only for uncertain directives or `_class` semantics.
- `references/image-patterns.md`: read when placing or splitting images.
- `references/advanced-features.md`: read when using math, fragments, or export options.
- `references/theme-css-guide.md`: read when creating custom CSS.
- `references/official-themes.md`: read only when choosing/extending an official built-in theme.
- `references/best-practices.md`: read when diagnosing visual quality.
- `assets/theme-*.css`: load only when building a custom theme from scratch or delivering an external stylesheet; skip for ordinary template decks.
