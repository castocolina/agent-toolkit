---
name: marp-slide
description: Create or redesign Marp Markdown (`.md`) slide decks from seven bundled styles with embedded CSS, Marpit image layouts and a render-and-fix check. Use for slides, a presentation, deck, talk, lecture or seminar slides, custom Marp theme CSS, or making an existing deck look better, less crowded or more readable, even without naming Marp. Not for editing `.pptx`, Google Slides or Keynote files, export-only or conversion-only requests, summarizing a presentation, speaker scripts, or HTML infographics.
---

# Marp Slide Creator

Each `assets/template-*.md` is a complete deck: frontmatter (`marp: true`, `theme: default`, `paginate: true`), one `<style>` block that restyles Marp's built-in `default` theme, and sample slides. Keep the frontmatter and style block; replace every sample slide. Basic, dark and colorful end with `<!-- _class: final -->`, which removes the bottom border; keep it on the last slide (`<!-- _class: lead final -->` for a closing title).

## Pick the path

- **New deck**: follow "New deck", then "Fit", "Validate" and "Save".
- **Existing deck** ("redesign", "less crowded", "make it look good", fix its CSS): follow "Existing deck", then "Save".

## Existing deck

1. Inventory: list every claim, number, code block, image path and speaker note, plus the slide order. All of it survives unless the user asked to change it.
2. Render the deck, or lint it without the CLI (see "Validate").
3. List the concrete defects: clipped content, low contrast, wrapping headings, broken images, more than 5 bullets, and the dead CSS named in "Gotchas".
4. Apply the smallest fix per defect: split a dense slide, shorten a heading, repair a directive, or swap in one template's `<style>` block when the colors themselves are the problem.
5. Diff the result against the step 1 inventory, render or lint again, and report each change with its reason.

## New deck

1. Topic and audience must be concrete. If either is missing or too vague to ground a deck ("stuff"), ask one focused question and stop: draft nothing and claim no file.
2. Outline claim, evidence, action toward what the audience must decide or learn. Never reuse a template's sample narrative.
3. Pick one style. A style the user names wins; otherwise take the first matching row and mention the runner-up in one line.

| Style | Template | Pick when | Background |
|---|---|---|---|
| tech | `template-tech.md` | code or developer audience, including "dark" plus code | near-black, monospace headings |
| business | `template-business.md` | business, proposal, report, tables | white, navy |
| minimal | `template-minimal.md` | academic, text-first | white, light type |
| dark | `template-dark.md` | dark requested, no code | black, cyan accents |
| gradient | `template-gradient.md` | visual keynote, little text | dark gradient; `<!-- _class: warm -->` or `teal` per slide |
| colorful | `template-colorful.md` | playful event, young audience | light pink |
| default | `template-basic.md` | anything else or unspecified | light beige |

4. With a bundled template, the title slide gets `<!-- _class: lead -->` and names the topic and the stated audience (for example "for junior backend developers"); section dividers also get `lead`. Each content slide gets one `##` heading and one message.

## Fit

Rendered fit decides, not character counts: a slide passes when nothing is clipped, every heading stays on one line and no text needed shrinking. Marp clips overflow silently, so PDF and PNG simply lose the bottom bullets. The templates pin `##` at the top and center the body vertically, so a two-line heading collides with a tall body.

Without a render, use this fallback: heading up to about 45 characters; at most 5 bullets of about 12 words; or one code block up to 12 lines; or one image plus up to 3 bullets. Split a slide rather than shrinking type or squeezing into columns, and keep every claim complete.

## Validate

With Marp CLI (`npx @marp-team/marp-cli`, called `marp` below):

```bash
marp --no-stdin deck.md -o /tmp/deck/deck.html                 # parse check, no browser needed
marp --no-stdin deck.md --images png -o /tmp/deck/slide.png    # one PNG per slide, needs a browser
```

Add `--allow-local-files` when the deck uses local images. Inspect every PNG for clipped content, contrast (body text 4.5:1, headings 3:1, on every gradient variant and image), leftover placeholders (`Topic1`, `Point1`, `Your Name`, `Month XX`) and blank image areas; fix and render again until clean.

Without the CLI, lint instead and tell the user the deck was not rendered:
- `marp: true` in the frontmatter, then by mode: a bundled template needs `theme: default` and its `<style>` block intact; a built-in theme (`gaia`, `uncover`) needs every `_class` to be one it defines (`lead` only in `gaia`); a registered custom theme needs a valid `/* @theme name */` file and `theme: name`, and may omit the `<style>` block;
- every `_class` value names a class the style block or theme defines (`lead`, `final` where present; `warm`, `teal` in gradient);
- every image path resolves relative to the deck file;
- no leftover placeholder (`Topic1`, `Point1`, `Your Name`, `Month XX`);
- every heading fits one line, about 45 characters;
- nothing from "Gotchas" is present, and every slide is within the fallback limits in "Fit".

## Save

Write to the requested path; else next to the user's existing deck, else a workspace path such as `slides/<topic>.md`. Use `/mnt/user-data/outputs/` only if that directory exists. Report the real path and whether it was rendered. If writing is impossible, return the Markdown inline and never claim a save.

## Gotchas

Each of these produces a wrong deck with no error:
- NEVER set `theme:` to a style label (`tech`, `gradient`): only `default`, `gaia` and `uncover` are built in, and Marp ignores an unknown name.
- NEVER vary slides with `section:nth-child()`: Marp Core wraps each slide in its own inline SVG, so every slide is child 1. Use `<!-- _class: name -->` plus a `section.name` rule.
- NEVER rely on `style="..."` attributes: Marp Core strips them (and escapes tags such as `<iframe>`) unless rendered with `--html`. Put a class on the element and its rule in the `<style>` block, or use `<style scoped>` for one slide.
- `_class` replaces the slide's classes: for a variant on a title or divider slide write `<!-- _class: lead warm -->`; a bare `warm` drops `lead` and loses the centering.
- An HTML comment that is not a directive becomes a speaker note and is exported by `--pdf-notes` and `--notes`; never leave drafting comments in a deck.
- `theme` and `size` apply to the whole deck and the last value wins, so a mid-deck `<!-- theme: gaia -->` restyles every slide. `size:` takes only `16:9` (default) or `4:3`; `A4` falls back to 16:9.
- Marp CLI waits for Markdown on stdin when stdin is not a terminal, so an agent shell hangs; pass `--no-stdin`.
- PDF, PPTX, PNG and `--notes` conversion start Chrome, Edge or Firefox and fail with "No suitable browser found" without one; pass `--browser-path` or set `CHROME_PATH`.
- Local images show in HTML but come out blank in PDF, PPTX and PNG unless `--allow-local-files` is passed.
- Fragmented lists (`*` bullets) step through only in the HTML presenter; PDF and PPTX show every item at once.
- Templates load Noto Sans JP from Google Fonts at render time; an offline render falls back to the font stack, so never strip the fallbacks.

## References

Load only what the current step needs:
- `assets/template-<style>.md`: the chosen style only; do not open the other templates.
- `references/image-patterns.md`: the deck places, splits or filters images.
- `references/marp-syntax.md`: directives beyond `_class: lead` and `paginate`, headers and footers, fit headings, math, or a built-in theme instead of a template.
- `references/theme-css-guide.md`: CSS changes beyond color swaps, a custom `@size`, or turning a template into a reusable theme file.
- `references/export.md`: the user wants PDF, PPTX, images or a CI build.
