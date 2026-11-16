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
2. Render the deck, or lint it without the CLI (see "Validate"). Check it against its own style block and registered theme; never assume it is an untouched bundled template. A deck with `theme: default` and its own `<style>` keeps its custom classes; the built-in class list applies only when the deck uses no style block.
3. List the concrete defects: clipped content, low contrast, wrapping headings, broken images, more than 5 bullets, and the dead CSS named in "Gotchas".
4. Apply the smallest fix per defect: split a dense slide, shorten a heading, repair a directive, or swap in one template's `<style>` block when the colors themselves are the problem.
5. Diff the result against the step 1 inventory, render or lint again, and report each change with its reason.

## New deck

1. Topic and audience must be concrete. If either is missing or too vague to ground a deck ("stuff"), ask one focused question and stop: draft nothing and claim no file.
2. Outline claim, evidence, action toward what the audience must decide or learn. Never reuse a template's sample narrative. When the user gives a talk length but no slide count, read `references/slide-count.md`.
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

An explicit appearance preference from the user (for example a light background) overrides the audience-based default in this table, even when it names no bundled style: pick the row whose background matches it.

If the user asks for a built-in theme (`default`, `gaia`, `uncover`) or a registered custom theme instead of a bundled style, skip the table and the templates. Start the frontmatter with `marp: true` and `theme: <name>` (a custom theme also needs `--theme-set` at render time, see "Validate"), pick every `_class` value only from the theme's own definition (for a built-in theme, its class list in `references/marp-syntax.md`; for a registered custom theme, that theme's CSS and any theme it imports, because the `references/marp-syntax.md` class list covers only the built-in themes; when a custom class's definition cannot be established, do not use it), and read `references/marp-syntax.md` (plus `references/theme-css-guide.md` for a custom theme) before building.

4. With a bundled template, the title slide gets `<!-- _class: lead -->` and names the topic and the stated audience (for example "for junior backend developers"); section dividers also get `lead`. Each content slide gets one `##` heading and one message. These are defaults for the bundled layouts: the user's requested design, image-led slides, dense technical content and intentional columns are exceptions (a slide may carry a second heading, or a title without an audience), and the rendered-fit and readability checks in "Fit" still apply to them.

## Fit

Rendered fit decides, not character counts: a slide passes when nothing is clipped, every heading stays on one line and no text needed shrinking. Marp clips overflow silently, so PDF and PNG simply lose the bottom bullets. The basic, business, colorful, dark and gradient templates pin `##` at the top (`position: absolute`) and center the body vertically, so a two-line heading collides with a tall body; tech and minimal keep the heading in the flow, but the rendered-fit check applies to every style.

Without a render, use this fallback: heading up to about 45 characters; at most 5 bullets of about 12 words; or one code block up to 12 lines; or one image plus up to 3 bullets. Split a slide rather than shrinking type or squeezing into columns, and keep every claim complete.

## Validate

With Marp CLI, run through `npx`; this needs Node.js and network access (to fetch the package the first time). Offline, or without Node.js, report the deck as not visually validated and use the lint below:

```bash
mkdir -p /tmp/deck
npx --yes @marp-team/marp-cli --no-stdin deck.md -o /tmp/deck/deck.html                 # parse check, no browser needed
npx --yes @marp-team/marp-cli --no-stdin deck.md --images png -o /tmp/deck/slide.png    # one PNG per slide, needs a browser
```

For a deck on a registered custom theme, add `--theme-set <theme>.css` to both commands, right after the input file (`deck.md --theme-set <theme>.css -o ...`). `--theme-set` is an array option and takes every path that follows it as a theme file: written before the input, or as `--theme-set=<theme>.css` before it, it swallows `deck.md` and Marp prints its help and exits 0 without converting (Marp CLI 4.5.1 HTML run, checked 2026-11-14), so also confirm the output file exists.

Add `--allow-local-files` when the deck uses local images. If either command fails (no CLI, no browser, a parse error), report the deck as not visually validated, give the error, and fall back to the lint below. Inspect every PNG for clipped content, contrast (body text 4.5:1, headings 3:1, on every gradient variant and image), leftover placeholders (`Topic1`, `Point1`, `Your Name`, `Month XX`) and blank image areas; fix and render again until clean.

Without the CLI, lint instead and tell the user the deck was not rendered:
- `marp: true` in the frontmatter, then by mode: a bundled template needs `theme: default` and its `<style>` block intact; a built-in theme (`default`, `gaia`, `uncover`) needs every `_class` to be in that theme's class list in `references/marp-syntax.md` (`lead` and the `gaia` class exist only in `gaia`; `invert` exists in all three); a registered custom theme needs a valid `/* @theme name */` file and `theme: name`, and may omit the `<style>` block;
- every `_class` value names a class the style block or theme defines (`lead`, `final` where present; `warm`, `teal` in gradient);
- `size:` is `16:9` or `4:3`, or a size the chosen custom theme defines with `@size`;
- every image path resolves relative to the deck file;
- no leftover placeholder (`Topic1`, `Point1`, `Your Name`, `Month XX`);
- every heading fits one line, about 45 characters;
- nothing from "Gotchas" is present, and every slide is within the fallback limits in "Fit".

## Save

Write to the requested path; else next to the user's existing deck, else a workspace path such as `slides/<topic>.md`. Use `/mnt/user-data/outputs/` only if that directory exists. When an existing deck is written to a different directory than its source, keep its image references working: rebase the relative paths or copy the assets, and report the path changes and any asset that could not be resolved. Report the real path and whether it was rendered. If writing is impossible, return the Markdown inline and never claim a save.

## Gotchas

Each of these produces a wrong deck with no error:
- NEVER set `theme:` to a style label (`tech`, `gradient`): only `default`, `gaia` and `uncover` are built in, and Marp ignores an unknown name.
- NEVER vary slides with `section:nth-child()`: Marp Core wraps each slide in its own inline SVG, so every slide is child 1. Use `<!-- _class: name -->` plus a `section.name` rule.
- NEVER rely on `style="..."` attributes: Marp Core strips them (and escapes tags such as `<iframe>`) unless rendered with `--html`. Put a class on the element and its rule in the `<style>` block, or use `<style scoped>` for one slide.
- `_class` replaces the slide's classes: for a variant on a title or divider slide write `<!-- _class: lead warm -->`; a bare `warm` drops `lead` and loses the centering.
- An HTML comment that is not a directive becomes a speaker note and is exported by `--pdf-notes` and `--notes`; never leave drafting comments in a deck.
- `theme` and `size` apply to the whole deck and the last value wins, so a mid-deck `<!-- theme: gaia -->` restyles every slide. With the built-in themes `size:` takes only `16:9` (default) or `4:3`, and `A4` falls back to 16:9; a registered custom theme can define more sizes with `@size` (`references/theme-css-guide.md` defines A4).
- Marp CLI waits for Markdown on stdin when stdin is not a terminal, so an agent shell hangs; pass `--no-stdin`.
- PDF, PPTX and PNG/JPEG conversion start Chrome, Edge or Firefox and fail with a missing-browser error (typically "No suitable browser found") without one; pass `--browser-path` or set `CHROME_PATH`. HTML and `--notes` output need no browser.
- Local images show in HTML but come out blank in PDF, PPTX and PNG unless `--allow-local-files` is passed.
- Fragmented lists (`*` bullets, or `1)` for ordered ones) step through only in the HTML presenter; PDF and PPTX show every item at once.
- NEVER run `--watch`, `--server` or `--preview` in a foreground agent shell: they never exit (see `references/export.md`).
- Templates load Noto Sans JP from Google Fonts at render time; an offline render falls back to the font stack, so never strip the fallbacks.

## References

Load only what the current step needs:
- `assets/template-<style>.md`: the chosen style only; do not open the other templates.
- `references/image-patterns.md`: the deck places, splits or filters images.
- `references/marp-syntax.md`: directives beyond `_class: lead` and `paginate`, headers and footers, fit headings, math, progressively revealed (fragmented) lists, or a built-in theme instead of a template.
- `references/theme-css-guide.md`: CSS changes beyond color swaps, columns or callout boxes, a custom `@size`, or turning a template into a reusable theme file.
- `references/export.md`: the user wants PDF, PPTX, images or a CI build, a live preview or served deck (`--watch`, `--server`), `--theme` on the command line, a progress bar or slide transitions in the HTML output.
- `references/theme-snippets.md`: only when the user wants a callout, step list, terminal block, styled table, quote or link style in the business or tech template, a glowing link in dark, colored bullet markers or a rainbow divider in colorful, a frosted text box in gradient, or a bad-example box in basic.
- `references/vscode.md`: the user works in VS Code (Marp for VS Code preview, export, `markdown.marp.*` settings).
- `references/slide-count.md`: the user gives a talk length and no slide count (also named in New deck step 2).
