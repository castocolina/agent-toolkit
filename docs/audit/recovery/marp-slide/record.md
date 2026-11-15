| item | fate | value | decision | reason class | reason |
| --- | --- | --- | --- | --- | --- |
| s003 When to Use | not-lost | real | none | text-present | The frontmatter description and README "When it triggers" list the same request types; the Japanese phrases are translated to English ("make it look good" stays in the Existing deck path) |
| s005 2. Content Structuring | not-lost | low | none | text-present | New deck step 4 (one ## heading and one message per slide) and Fit (45-character headings, 5 bullets) replace the 5-7-character Japanese rule |
| s008 1. Default Theme | redistributed skills/marp-slide/SKILL.md | low | none | moved-to skills/marp-slide/SKILL.md | The style table row "default" carries background and pick-when; the README now points to SKILL.md |
| s011 4. Dark Mode Theme | redistributed skills/marp-slide/SKILL.md | low | none | moved-to skills/marp-slide/SKILL.md | The style table row "dark" carries background and pick-when; the glow effect is visible in template-dark.md |
| s012 5. Gradient Background Theme | redistributed skills/marp-slide/SKILL.md | low | none | moved-to skills/marp-slide/SKILL.md | The style table row "gradient" carries background, the warm/teal per-slide classes and pick-when |
| s013 6. Tech/Code Theme | redistributed skills/marp-slide/SKILL.md | low | none | moved-to skills/marp-slide/SKILL.md | The style table row "tech" carries background, monospace headings and pick-when |
| s015 Key Features | removed-on-merit | low | drop | superseded-by README intro paragraph | A marketing list (7 themes, quality checklist, multi-language); the README intro and "When it triggers" state the real capabilities |
| s016 Example 1: Basic Presentation | removed-on-merit | low | drop | generic-model-knowledge | An illustrative chat transcript with bracketed placeholders and the /mnt/user-data/outputs path; no rule or template |
| s017 Example 2: Tech Meetup | removed-on-merit | low | drop | generic-model-knowledge | An illustrative chat transcript; the tech row of the style table already maps a developer audience to the tech template |
| s018 Example 3: Business Proposal | removed-on-merit | low | drop | generic-model-knowledge | An illustrative chat transcript; the business row of the style table already maps proposals and reports to the business template |
| s020 File Structure | removed-on-merit | real | intended-change | fact-update | The README tree now lists the current references/ files and evals/ and no longer lists theme-*.css or the four deleted references |
| s021 Output | removed-on-merit | low | intended-change | scope-change | The mandate to save under /mnt/user-data/outputs/ became the Save section (requested path first, honest report); export formats moved to references/export.md |
| s022 Quality Standards | not-lost | low | none | text-present | Fit and Validate hold the measurable limits (one line per heading, 5 bullets, contrast ratios, rendered check) |
| s023 Internal Documentation | not-lost | low | none | text-present | The README File structure tree lists each current reference with its purpose |
| s027 When to Use This Skill | not-lost | real | none | text-present | The description names slides, presentations, decks, lectures, seminars, custom theme CSS and redesign requests, and the exclusions |
| s029 Step 2: Create Slides | not-lost | real | none | text-present | New deck steps 3-4 and the References section load only the template and reference the step needs |
| s030 1. Default Theme | not-lost | low | none | text-present | The style table row "default" |
| s033 4. Dark Mode Theme | not-lost | low | none | text-present | The style table row "dark" |
| s035 6. Tech/Code Theme | not-lost | low | none | text-present | The style table row "tech" |
| s037 Basic Workflow | not-lost | real | none | text-present | New deck steps 1-4, Fit, Validate and Save cover understand, style, template, structure, refine, images and output; "formality level" and the 15-25 characters per line are replaced by the Fit limits |
| s038 Handling "Make It Look Good" Requests | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Theme inference and automatic fixes live in New deck step 3 and the Existing deck path; the rest (h3 sub-sections, intro-body-conclusion flow, parallel lists, consistent terms) is generic |
| s040 File Output | removed-on-merit | low | intended-change | scope-change | Replaced by the Save section; the fixed /mnt/user-data/outputs/ target is used only if that directory exists |
| s041 Quality Checklist | not-lost | real | none | text-present | The Validate lint list and render checks cover theme, embedded style, lead title slide, headings, bullets, image paths and saving, with measurable limits |
| s042 Core Documentation | not-lost | low | none | text-present | The References section lists each current reference file with the step that loads it |
| s043 Quality & Selection Guides | not-lost | low | none | text-present | Selection lives in the style table and quality in Fit and Validate; the two reference files are triaged in their own rows |
| s044 Templates & Assets | not-lost | low | none | text-present | The style table names every template; theme-*.css rows are file rows below |
| s047 (preamble) | removed-on-merit | real | intended-change | fact-update | template-basic.md now uses section.final instead of section:last-of-type, which matched every slide because Marp Core wraps each slide in its own inline SVG |
| s050 (preamble) | removed-on-merit | real | intended-change | safety-fix | template-colorful.md darkened the heading and accent-3 colors (#ff6b9d to #c2255c, #4d96ff to #1a56c4) for text contrast and replaced section:last-of-type with section.final |
| s054 (preamble) | removed-on-merit | real | intended-change | fact-update | template-gradient.md replaced section:nth-child(Nn) backgrounds, which never match in Marp Core, with section.warm and section.teal classes and darkened the gradients for contrast |
| s060 Fragmented List (Progressive Display) | removed-to-fit | real | restore-references | users-ask-by-name | Slides that reveal bullets one by one are asked for by name; the Gotchas name only `*` bullets, not that ordered lists use `1)` (Marpit fragmented-list docs; Marp CLI bespoke template README) |
| s063 Important Notes | not-lost | real | none | text-present | Gotchas: fragmented lists step through only in the HTML presenter; PDF and PPTX show every item |
| s064 Math Notation (Marp Core Extension) | not-lost | low | none | text-present | marp-syntax.md Content features: Math bullet |
| s065 Multi-line Math | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): An aligned multi-line TeX block; a model writes it unprompted and the `$$ block $$` syntax is in marp-syntax.md |
| s067 Important Notes | not-lost | low | none | text-present | marp-syntax.md Math bullet warns that macros MathJax accepts may fail under KaTeX |
| s068 Emoji (Marp Core Extension) | not-lost | low | none | text-present | marp-syntax.md Content features: Emoji bullet |
| s069 Disable | removed-on-merit | low | drop | wrong | user accepted the drop (2026-11-13, call delegated to the controller): `--marpit-auto-scaling` and a `no-scaling` class do not exist in Marp Core (src/auto-scaling gates fitting on the theme `@auto-scaling` metadata, docs/markdown.md); the snippet never worked |
| s070 Two-Column Layout | removed-on-merit | low | drop | wrong | user accepted the drop (2026-11-13, call delegated to the controller): The `style="display:flex"` attributes are stripped (marp-core src/html/allowlist.ts allows no style attribute), so the columns never lay out; the class-based version is restored under s083 |
| s071 Styled Box | removed-on-merit | low | drop | wrong | user accepted the drop (2026-11-13, call delegated to the controller): The inline `style=` box is stripped by Marp Core without `--html`; a class plus a rule in the style block (the s083 restore covers it) is the working form |
| s073 Watch Mode | removed-to-fit | real | restore-references | users-ask-by-name | `--watch`/`-w` and `--server`/`-s` (and `--preview`/`-p`) are what a user asks for to see a deck live; export.md has none of them, and they block an agent shell so a warning must come with them |
| s074 Specify Theme | removed-to-fit | real | restore-references | users-ask-by-name | `--theme` takes a built-in name or a CSS file (Marp CLI README); export.md and theme-css-guide.md cover only `--theme-set` |
| s075 Batch Convert Multiple Files | not-lost | low | none | text-present | export.md "Folder of decks" row (`-I slides/ -o dist/`); shell globbing is basic |
| s076 HTML Output Options | not-lost | low | none | text-present | export.md HTML presenter row and the `--html` bullet; the old comment "standalone HTML (using CDN)" was wrong (`--html` enables HTML tags) |
| s077 PDF Output Options | not-lost | low | none | text-present | export.md PDF rows (`--pdf`, `--pdf-notes --pdf-outlines`, `--allow-local-files` in the SKILL); the old comment "PDF without page numbers" was wrong |
| s078 Image Output | removed-to-fit | real | restore-references | users-ask-by-name | export.md has only PNG; `--images jpeg`, `--image-scale 2` (high-resolution output) and the first-slide-only `--image` form are real options (Marp CLI README) |
| s079 Export | removed-to-fit | real | restore-references | users-ask-by-name | The Marp for VS Code export path (toolbar quick pick "Export slide deck...", command `markdown.marp.export`, HTML/PDF/PPTX/PNG/JPEG/TXT) is asked for by name and appears nowhere in the current files |
| s080 Settings | removed-to-fit | real | restore-references | users-ask-by-name | `markdown.marp.themes` (register a theme CSS) is the VS Code way to use a custom theme; the old `markdown.marp.enableHtml` is deprecated since v2, restore it as `markdown.marp.html` |
| s081 Basic Workflow | not-lost | low | none | text-present | export.md GitHub Actions section holds a current workflow with a pinned CLI major |
| s082 Publish to GitHub Pages | removed-on-merit | low | drop | stale | user accepted the drop (2026-11-13, call delegated to the controller): Built on peaceiris/actions-gh-pages@v3, actions/upload-artifact@v3 and a `:latest` docker action; a model writes a current Pages deploy unprompted and the Marp part is only `-o index.html` |
| s083 3. Two-Column Layout | removed-to-fit | real | restore-references | reusable-template | A column layout is a common request and the current skill gives no recipe; a `div` with a class plus a rule in the style block works without `--html` (allowlist allows div and class, not style) |
| s084 4. Progress Bar | removed-to-fit | real | restore-references | users-ask-by-name | The old CSS used non-existent variables, but the feature is real: `--bespoke.progress` (HTML presenter), plus `--bespoke.osc` and the `transition` directive (Marp CLI README) |
| s086 Official References | not-lost | low | none | text-present | The links are in README Resources and at the top of each reference; the VS Code marketplace link returns with the s079 restore |
| s087 ✅ Good Examples | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): A four-line example of short parallel titles (Introduction, Problem, Solution, Results); a model writes concise titles unprompted |
| s088 ❌ Bad Examples | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Two verbose heading examples; the 45-character limit in Fit is the enforceable rule |
| s089 ✅ Good Examples | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Parallel short bullets; Fit limits bullets to 5 of about 12 words |
| s090 ❌ Bad Examples | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Three inconsistent bullets; the same Fit limits apply |
| s091 Basic Structure | removed-on-merit | low | drop | generic-model-knowledge | Title, agenda, content, summary skeleton; New deck step 2 (claim, evidence, action) and step 4 (title slide lead, one message per slide) replace it |
| s092 Recommended Slide Count | removed-to-fit | real | restore-references | users-ask-by-name | Slide count by talk length (5 min 5-8, 10 min 10-15, 20 min 15-25) is a concrete heuristic users state ("a 10-minute talk") and nothing current gives it |
| s094 Using Whitespace | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Three general design sentences; the Fit rules already cap density |
| s096 When Using Additional Colors | removed-on-merit | low | drop | wrong | The `<span style="color:...">` example is stripped by Marp Core without `--html` (Gotchas) |
| s097 Effective Usage | removed-on-merit | low | drop | generic-model-knowledge | Generic image advice (purpose, resolution, size) |
| s099 Font Size Guidelines | redistributed skills/marp-slide/assets/template-basic.md | low | none | moved-to skills/marp-slide/assets/template-basic.md | The sizes (h1 56, h2 40, body 22) are set in each template's style block and vary per template |
| s100 Animations and Transitions | removed-on-merit | low | drop | stale | user accepted the drop (2026-11-13, call delegated to the controller): "Marp does not support animations" is outdated: the Marp CLI bespoke template supports slide transitions (`transition` directive, `--bespoke.transition`); the replacement fact goes with the s084 resto |
| s101 Checklist | not-lost | real | none | text-present | The Validate lint list and render checks cover each item (titles, bullets, one message, density, images, consistency) |
| s103 Regular Images | not-lost | low | none | text-present | image-patterns.md table row "Figure inside the text flow" |
| s107 Background Size (Numeric Values) | not-lost | low | none | text-present | image-patterns.md table: `![bg 80%]` sets background-size |
| s109 Three or More Splits | not-lost | low | none | text-present | image-patterns.md "Side-by-side comparison" row (equal split in source order) and the split behavior note |
| s113 Brightness Adjustment | not-lost | low | none | text-present | image-patterns.md filter list and the `brightness:0.5` row; the value range is CSS filter knowledge |
| s114 Grayscale | not-lost | low | none | text-present | image-patterns.md filter list names `grayscale` |
| s118 Pattern 3: Multiple Image Comparison | removed-on-merit | real | intended-change | fact-update | Two bg images with `left:50%` and `right:50%` do not give a before/after pair; image-patterns.md states the split rule (Marpit image-syntax docs) |
| s119 Pattern 4: Vertical Comparison | not-lost | low | none | text-present | image-patterns.md "Stacked comparison" row |
| s121 Important Notes | not-lost | real | none | text-present | image-patterns.md bullets: bg behind text, source order, relative paths, missing image behavior |
| s123 Main Global Directives | removed-on-merit | real | intended-change | fact-update | The old table presented local directives (paginate, header, footer, class, colors) as deck-wide and offered A4; marp-syntax.md now separates global and local directives per the Marpit directives docs |
| s124 Size Directive (Marp Core) | removed-on-merit | low | intended-change | fact-update | `A4` is not a built-in size (Marp Core: built-in themes provide 16:9 and 4:3 only); the SKILL Gotchas state the two values |
| s126 Slide Breaks | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): `---` as the slide separator; every bundled template uses it and the model knows it |
| s132 Title Slide | not-lost | low | none | text-present | SKILL New deck step 4 (`_class: lead`) and marp-syntax.md (`_paginate: false`) |
| s135 Features | not-lost | low | none | text-present | marp-syntax.md built-in themes table, row `default` |
| s136 invert (Inverted Colors) | not-lost | low | none | text-present | The table lists `invert` for default, gaia and uncover |
| s139 Features | not-lost | low | none | text-present | marp-syntax.md built-in themes table, row `gaia` |
| s140 Color Variations | not-lost | low | none | text-present | The table lists the gaia classes (`lead`, `invert`, `gaia`) and the CSS-variable recolor example |
| s141 Distinctive Styles | not-lost | low | none | text-present | The table's "Look" column describes gaia |
| s143 Features | not-lost | low | none | text-present | marp-syntax.md table row `uncover`; the old "elegant serif font" claim was wrong (uncover uses a sans-serif stack, marp-core themes/uncover.scss) |
| s144 Distinctive Styles | removed-on-merit | low | drop | wrong | user accepted the drop (2026-11-13, call delegated to the controller): "Serif font for headings" is wrong: uncover's font-family is Cantarell, Open Sans, Helvetica Neue, sans-serif (marp-core themes/uncover.scss) |
| s145 Customization Example | not-lost | low | none | text-present | marp-syntax.md shows the same override technique for gaia (CSS variables in a style block) |
| s146 Theme Comparison Table | not-lost | low | none | text-present | marp-syntax.md built-in themes table (theme, classes, look) replaces it; its Font column was inaccurate for uncover |
| s148 invert | not-lost | low | none | text-present | marp-syntax.md table and the `_class: lead invert` bullet |
| s149 When to Choose default | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Four generic reasons to pick the default theme; the style table's `default` row covers "anything else or unspecified" |
| s150 Extending Official Themes | not-lost | real | none | text-present | theme-css-guide.md recipe: `/* @theme name */` plus `@import 'default';` then rules |
| s151 Switching Between Multiple Themes | removed-on-merit | real | intended-change | fact-update | `theme` is a global directive and the last value wins, so a mid-deck `<!-- theme: gaia -->` restyles every slide; the SKILL Gotchas say so |
| s154 Using uncover Theme | removed-on-merit | real | intended-change | fact-update | The sample used `_class: lead`, which uncover does not define (only `invert`); marp-syntax.md and the Validate lint now state which classes each built-in theme defines |
| s155 Official References | not-lost | low | none | text-present | marp-syntax.md and theme-css-guide.md headers link the theme sources and the Theme CSS specification |
| s158 Basic Theme CSS Example | not-lost | low | none | text-present | theme-css-guide.md "Turn a template into a reusable theme file" shows the `@theme` header, rules and registration |
| s161 Custom Size Definition | not-lost | low | none | text-present | theme-css-guide.md step 2 (`/* @size A4 1123px 794px */`); the format `@size <name> <w> <h>` matches marp-core src/size |
| s162 Pagination | not-lost | low | none | text-present | theme-css-guide.md bullet on `section::after` with `attr(data-marpit-pagination)` and `attr(data-marpit-pagination-total)` |
| s163 Header | not-lost | low | none | text-present | theme-css-guide.md bullet: header and footer are inserted elements to position absolutely inside section |
| s164 Footer | not-lost | low | none | text-present | Same bullet; every template styles footer |
| s165 Loading with @import | not-lost | real | none | text-present | theme-css-guide.md recipe step 1 (`@import 'default';`) |
| s166 Inheriting Named Themes with @import-theme | removed-to-fit | real | restore-references | users-ask-by-name | The `@import-theme` rule is the preprocessor-safe form of `@import` (Marpit theme-css docs); the current guide never mentions it, and a Sass or PostCSS user needs it |
| s167 lead Class (Title Slide) | redistributed skills/marp-slide/assets/template-minimal.md | low | none | moved-to skills/marp-slide/assets/template-minimal.md | Every template defines `section.lead` (flex centered in minimal and business); theme-css-guide notes the templates define their own |
| s168 invert Class (Inverted Colors) | removed-on-merit | low | drop | generic-model-knowledge | Eight lines of CSS for a black-background class; built-in themes define `invert` and the lint requires every `_class` to be defined |
| s169 Scoped Style (Slide-Specific Styles) | not-lost | low | none | text-present | SKILL Gotchas and theme-css-guide.md both name `<style scoped>` |
| s170 Background Image Styling | removed-on-merit | low | drop | wrong | user accepted the drop (2026-11-13, call delegated to the controller): `section[data-marpit-background-image]` is not a Marpit attribute (advanced backgrounds use `data-marpit-advanced-background`, marpit src/postcss/advanced_background.js), so the rule never matched |
| s171 List Styling | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Ordinary list CSS; each template already styles lists |
| s172 Table Styling | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Ordinary table CSS; the business and tech templates already style tables |
| s173 Code Block Styling | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Ordinary pre and code CSS; the tech and dark templates already style code |
| s174 Responsive Design | removed-on-merit | real | intended-change | fact-update | Screen-width `@media` queries do nothing because slides are fixed-size and scaled as a whole; theme-css-guide.md says so |
| s175 Minimal Theme | not-lost | low | none | text-present | template-minimal.md carries the minimal style and the recipe turns a template into a theme |
| s178 Best Practices | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-13, call delegated to the controller): Contrast (4.5:1) and fallback fonts are kept in Validate and Gotchas; the rest (font sizes, 60px padding, `@media print` styles) is generic and the print advice is unverified for Marp output |
| s180 Marp Theme Selection Guide | not-lost | low | none | text-present | The "Pick the path" and style table in SKILL.md replace the intro sentence |
| s181 1. Default (theme-default.css / template-basic.md) | not-lost | low | none | text-present | The style table row "default" |
| s184 4. Dark Mode (theme-dark.css / template-dark.md) | not-lost | low | none | text-present | The style table row "dark" |
| s189 Step 2: Choose by Atmosphere | not-lost | real | none | text-present | The style table "Pick when" column maps playful to colorful, visual keynote to gradient, academic to minimal, business to business and dark to dark, with a runner-up line |
| s192 When to Use Default Theme | not-lost | low | none | text-present | The style table: default is "anything else or unspecified" |
| s193 Suggesting Multiple Themes | removed-on-merit | real | intended-change | scope-change | The current New deck step 3 picks the first matching row and names the runner-up in one line instead of asking the user to choose, so an unattended run is never blocked |
| file:skills/marp-slide/assets/theme-default.css | removed-to-fit | real | restore-references | reusable-template | (2026-11-14, call delegated to the controller) The file was a copy of template-basic.md's style block with Japanese comments plus one `.bad-example` helper class that no current file keeps (it had no `@theme` header, so it was not loadable as a theme). Restored in skills/marp-slide/references/theme-snippets.md (Basic section) as `section .bad-example` with a note on when to use it; the rest of the file is already in template-basic.md; rendered with Marp CLI 4.5.1 (checked 2026-11-14) |
| file:skills/marp-slide/assets/theme-minimal.css | removed-on-merit | low | drop | superseded-by assets/template-minimal.md | (2026-11-14, call delegated to the controller) Re-checked against the current template: line-for-line copy of template-minimal.md's style block (0 unique rules; its `hr` rule is in the template), so the drop stands |
| file:skills/marp-slide/assets/theme-colorful.css | removed-to-fit | real | restore-references | reusable-template | (2026-11-14, call delegated to the controller) The file was a copy of the style block plus `li::marker` and `hr` rules (and the pre-contrast heading color #ff6b9d, which the template deliberately replaced with #c2255c); no @theme header. Restored in skills/marp-slide/references/theme-snippets.md (Colorful section) as copy-ready CSS with the template's color variables and a `section ` prefix, one use-when line each; the divider is written as an HTML `<hr>` because `---` and `***` are slide breaks; rendered with Marp CLI 4.5.1 (checked 2026-11-14) |
| file:skills/marp-slide/assets/theme-dark.css | removed-to-fit | real | restore-references | reusable-template | (2026-11-14, call delegated to the controller) The file was a copy of the style block plus link rules (`a` with a heading-color underline, `a:hover` glow) that no current file keeps; no @theme header. Restored in skills/marp-slide/references/theme-snippets.md (Dark section) as copy-ready CSS with the template's color variables and a `section ` prefix and a use-when line; rendered with Marp CLI 4.5.1 (checked 2026-11-14) |
| file:skills/marp-slide/assets/theme-business.css | removed-to-fit | real | restore-references | reusable-template | (2026-11-14, call delegated to the controller) The file was a copy of the template style block plus helper rules that no current file keeps: `.highlight-box`, `.number`, `.step`, blockquote and link rules. Restored in skills/marp-slide/references/theme-snippets.md (Business section) as copy-ready CSS with a note on when to use each, rewritten with the template's color variables and a `section ` prefix; the rest of the file is already in template-business.md. Loaded from SKILL.md References only for a callout, step list, styled table, quote or link style; rendered with Marp CLI 4.5.1 (checked 2026-11-14) |
| file:skills/marp-slide/assets/theme-gradient.css | removed-to-fit | real | restore-references | reusable-template | (2026-11-14, call delegated to the controller) The file carried the `section:nth-child(Nn)` backgrounds that never match in Marp Core (fixed in template-gradient.md; that part stays dropped) plus a `.text-box` frosted-box class that no current file keeps; no @theme header. Restored the `.text-box` rule in skills/marp-slide/references/theme-snippets.md (Gradient section) as `section .text-box` with a use-when line and a contrast reminder; rendered with Marp CLI 4.5.1 (checked 2026-11-14) |
| file:skills/marp-slide/assets/theme-tech.css | removed-to-fit | real | restore-references | reusable-template | (2026-11-14, call delegated to the controller) The file was a copy of the template style block plus helper rules that no current file keeps: table, link, blockquote and `.terminal` rules. Restored in skills/marp-slide/references/theme-snippets.md (Tech section) as copy-ready CSS with a note on when to use each, rewritten with the template's color variables and a `section ` prefix; the rest of the file is already in template-tech.md. Loaded from SKILL.md References only for a styled table, quote, terminal block or link style; rendered with Marp CLI 4.5.1 (checked 2026-11-14) |
| s001 Marp Slide Creator | not-lost | low | none | text-present | The README intro paragraph states the same purpose (create and redesign Marp decks from seven styles) |
| s002 Purpose | not-lost | low | none | text-present | The README intro and "When it triggers" carry seven styles, vague "make it look good" requests, image layouts and the style choice |
| s004 1. Theme Selection | not-lost | low | none | text-present | The SKILL.md style table replaces the README quick-selection list (same mapping from audience to style) |
| s006 3. Template Application | not-lost | low | none | text-present | The README intro and SKILL.md opening paragraph: each template is a complete deck with embedded CSS, no external files |
| s007 4. Image Integration | not-lost | low | none | text-present | references/image-patterns.md "Pick a pattern" table holds the side, centered, background and multi-image forms |
| s009 2. Minimal Theme | not-lost | low | none | text-present | The style table row "minimal" |
| s010 3. Colorful & Pop Theme | not-lost | low | none | text-present | The style table row "colorful" |
| s014 7. Business Theme | not-lost | low | none | text-present | The style table row "business"; the table CSS lives in template-business.md |
| s019 Example 4: Vague Request (Japanese) | not-lost | low | none | text-present | The Existing deck path ("make it look good") inventories, lists defects and applies the smallest fix; the example was a bracketed transcript in Japanese |
| s025 (preamble) | not-lost | real | none | text-present | The new frontmatter description keeps the old triggers (slides, presentations, custom theme CSS, make it look good) and adds exclusions; the "7 beautiful themes" wording became "seven bundled styles" |
| s026 Marp Slide Creator | not-lost | low | none | text-present | The SKILL.md title and opening paragraph state the purpose and how templates work |
| s028 Step 1: Select Theme | not-lost | real | none | text-present | New deck step 3 and the style table hold the same mapping plus the user-named-style rule and a runner-up line |
| s031 2. Minimal Theme | not-lost | low | none | text-present | The style table row "minimal" |
| s032 3. Colorful & Pop Theme | not-lost | low | none | text-present | The style table row "colorful" |
| s034 5. Gradient Background Theme | not-lost | low | none | text-present | The style table row "gradient" (with the warm and teal classes) |
| s036 7. Business Theme | not-lost | low | none | text-present | The style table row "business" |
| s039 Image Integration | not-lost | real | none | text-present | The References entry for references/image-patterns.md and its table cover side, centered, background and multi-image forms |
| s045 Official External Links | not-lost | low | none | text-present | references/theme-css-guide.md links the Marpit Theme CSS spec; marp-syntax.md links Marpit directives and Marp Core |
| s046 (preamble) | removed-on-merit | real | intended-change | fact-update | template-basic.md: `section:last-of-type { border-bottom: none }` became `section.final` (see s047) |
| s055 (preamble) | removed-on-merit | real | intended-change | safety-fix | template-gradient.md: the lead-slide gradient was darkened for contrast (see s054) |
| s061 Basic Usage | not-lost | low | none | text-present | The `*` bullet marker is in the Gotchas; the s060 restore adds the `1)` form |
| s062 Using Asterisks (*) | removed-on-merit | low | intended-change | fact-update | The claim that `--html` makes items appear sequentially is wrong: the Marp CLI bespoke HTML presenter does it (Marp CLI README); the Gotchas say HTML presenter only |
| s066 Math Examples | not-lost | low | none | text-present | marp-syntax.md Math bullet shows `$inline$` and `$$ block $$`; the quadratic-formula sample is generic |
| s072 Basic Commands | not-lost | low | none | text-present | references/export.md Commands table |
| s085 PDF Not Generated | not-lost | real | none | text-present | Gotchas: "No suitable browser found" without Chrome, Edge or Firefox; local images blank without `--allow-local-files` |
| s093 ❌ Too Crowded | not-lost | low | none | text-present | Fit: at most 5 bullets of about 12 words, split a dense slide |
| s095 Using Colors | redistributed skills/marp-slide/assets/template-basic.md | low | none | moved-to skills/marp-slide/assets/template-basic.md | The theme hex values live in the template's :root block |
| s098 Layout Tips | not-lost | low | none | text-present | image-patterns.md table row "Image beside bullets" (`![bg right:40%]`) |
| s102 Marp Image Syntax Reference | not-lost | low | none | text-present | image-patterns.md header: "Marpit image syntax as Marp Core renders it" with the official link |
| s104 Size Specification | not-lost | low | none | text-present | image-patterns.md table: `w:`/`h:` (or `width:`/`height:`) take any CSS length |
| s105 Basic Background Image | not-lost | low | none | text-present | image-patterns.md rows "Full-slide background" and the bg-behind-text bullet |
| s106 Background Size Keywords | not-lost | low | none | text-present | image-patterns.md row "Whole image, letterboxed": `contain`, `fit` alias, `auto`, default `cover` |
| s108 Basic Split | not-lost | low | none | text-present | image-patterns.md table row "Image beside bullets" (`![bg right:40%]`) and the split-region note |
| s110 Specifying Split Direction | not-lost | low | none | text-present | image-patterns.md "Stacked comparison" row: `vertical` flips the split |
| s111 Left/Right Alignment | not-lost | low | none | text-present | image-patterns.md "Image beside bullets" row: `left` mirrors `right` |
| s112 Size Ratio Specification | not-lost | low | none | text-present | image-patterns.md row `![bg right:40%]`: the percentage is the image's share |
| s115 Multiple Filters | not-lost | low | none | text-present | image-patterns.md: filters combine in one alt text, with a `blur:4px brightness:0.6` example |
| s116 Pattern 1: Text on Left, Image on Right | not-lost | low | none | text-present | image-patterns.md "Image beside bullets" row |
| s117 Pattern 2: Background Image + Overlay Text | not-lost | low | none | text-present | image-patterns.md row "Text over a photo" (`![bg brightness:0.5]`) |
| s120 Pattern 7: Background with Filter Effects | not-lost | low | none | text-present | image-patterns.md: filters apply to bg images too, with a combined `blur` and `brightness` example |
| s122 Official Reference | not-lost | low | none | text-present | Each current reference opens with its official documentation link |
| s125 Page-Specific Directives | not-lost | low | none | text-present | marp-syntax.md Directive scope table: `<!-- key -->` from here on, `<!-- _key -->` this slide only |
| s127 Pagination (Page Numbers) | not-lost | low | none | text-present | marp-syntax.md (`_paginate: false` hides one number) and the template frontmatter `paginate: true` |
| s128 Style Specification in Markdown | not-lost | low | none | text-present | Every template embeds its `<style>` block; the Gotchas explain scoped and class-based styling |
| s129 Scoped Style | not-lost | low | none | text-present | Gotchas and theme-css-guide.md name `<style scoped>` |
| s130 Comments | not-lost | low | none | text-present | Gotchas: a non-directive HTML comment becomes a speaker note; marp-syntax.md notes the same |
| s131 Official Reference Links | not-lost | low | none | text-present | marp-syntax.md opens with the Marpit directives and Marp Core links |
| s133 Marp Official Themes Reference | not-lost | low | none | text-present | marp-syntax.md "Built-in themes" section |
| s134 Official Theme List | not-lost | low | none | text-present | marp-syntax.md built-in themes table (default, gaia, uncover) |
| s137 Combined | not-lost | low | none | text-present | marp-syntax.md: `<!-- _class: lead invert -->` sets several classes |
| s138 Customization Example | not-lost | low | none | text-present | Every template restyles `default` through an embedded style block |
| s142 Customization Example | not-lost | low | none | text-present | marp-syntax.md carries the same gaia CSS-variable recolor block (`--color-background`, `--color-foreground`, `--color-highlight`) |
| s147 lead | not-lost | low | none | text-present | marp-syntax.md table: `lead` exists only in gaia among built-ins; templates define their own `section.lead` |
| s152 Using default Theme | removed-to-fit | real | restore-references | reusable-template | (2026-11-14, call delegated to the controller) The earlier claim that template-basic.md is the same deck was wrong: template-basic.md embeds a style block that restyles `default`, while the dropped example is a complete deck on the unmodified built-in theme (title, agenda, status). Restored in references/marp-syntax.md ("Example: a short deck on the default theme") in English with the invalid `lead` class replaced by `invert` (the only class `default` defines), the month kept, no embedded CSS; rendered with Marp CLI 4.5.1 to HTML, exit 0, the title slide kept `class="invert"` (checked 2026-11-14). |
| s153 Using gaia Theme | removed-to-fit | real | restore-references | reusable-template | (2026-11-14, call delegated to the controller) The earlier claim that marp-syntax.md covers this was wrong: it listed the gaia classes but had no complete deck. Restored in references/marp-syntax.md ("Example: a short deck on the gaia theme") with the title slide on `lead`, the concept slide kept, the three emoji list items written as plain words, and one added closing slide on `lead gaia` to show the alternate color scheme (the `gaia` class sets a blue background in the Marp Core 4.4.0 CSS); rendered with Marp CLI 4.5.1 to HTML, exit 0, the sections kept `class="lead"` and `class="lead gaia"` (checked 2026-11-14). |
| s156 Marp Theme CSS Creation Guide | not-lost | low | none | text-present | theme-css-guide.md header links the Marpit theme CSS specification |
| s157 @theme Metadata (Required) | not-lost | low | none | text-present | theme-css-guide.md recipe step 1: `/* @theme name */` as the first line |
| s159 HTML Structure | not-lost | low | none | text-present | theme-css-guide.md: every slide is a `<section>` of a fixed size; the Gotchas explain the inline SVG wrapping |
| s160 Default Size | not-lost | low | none | text-present | theme-css-guide.md: 1280x720 for 16:9 |
| s176 Dark Theme | not-lost | low | none | text-present | template-dark.md carries the dark style |
| s177 Embedding Styles in Markdown | not-lost | low | none | text-present | Every template embeds a style block and the Gotchas say to put rules there |
| s179 Official References | removed-on-merit | low | drop | out-of-scope | The Marpit JavaScript API link serves integrators; the skill authors decks and themes |
| s182 2. Simple & Minimal (theme-minimal.css / template-minimal.md) | not-lost | low | none | text-present | The style table row "minimal" |
| s183 3. Colorful & Pop (theme-colorful.css / template-colorful.md) | not-lost | low | none | text-present | The style table row "colorful" |
| s185 5. Gradient Background (theme-gradient.css / template-gradient.md) | not-lost | low | none | text-present | The style table row "gradient" |
| s186 6. Tech/Code (theme-tech.css / template-tech.md) | not-lost | low | none | text-present | The style table row "tech" |
| s187 7. Business-like (theme-business.css / template-business.md) | not-lost | low | none | text-present | The style table row "business" |
| s188 Step 1: Filter by Use Case | not-lost | low | none | text-present | The style table "Pick when" column |
| s190 Step 3: Choose by Background Color | not-lost | low | none | text-present | The style table "Background" column lists each style's background |
| s191 "Make it look good" / "Make it cool" | not-lost | real | none | text-present | The Existing deck path and New deck step 3 pick a style from the content when the request is vague |
| para:1f109d08 | removed-on-merit | low | drop | generic-model-knowledge | Front matter `backgroundImage: linear-gradient(...)` and `color: white`; marp-syntax.md lists these local directives |
| para:9b25b402 | removed-on-merit | low | drop | generic-model-knowledge | A three-bullet sample slide |
| para:4152c130 | removed-on-merit | low | drop | generic-model-knowledge | A list of emoji shortcodes (:rocket:, :tada:, ...); marp-syntax.md states the shortcode mechanism |
| para:9a7eafe6 | not-lost | low | none | text-present | SKILL New deck step 4: section dividers get `lead` |
| para:0dc025c1 | not-lost | low | none | text-present | marp-syntax.md scope table: `<!-- _backgroundColor: ... -->` is a spot directive |
| para:2a846276 | removed-to-fit | real | restore-references | users-ask-by-name | The VS Code marketplace link returns with the s079 Marp for VS Code section |
| para:7bef7f7d | not-lost | low | none | text-present | marp-syntax.md lists the `header` and `footer` directives |
| para:e1504c4b | not-lost | low | none | text-present | image-patterns.md "Figure inside the text flow" row |
| para:caac332b | not-lost | low | none | text-present | theme-css-guide.md pagination bullet (`attr(data-marpit-pagination)`) |
| para:8f63349a | not-lost | low | none | text-present | Every template has a `_class: lead` title slide |
| para:065fa4f4 | removed-on-merit | low | drop | generic-model-knowledge | `.katex` font-size tweak, ordinary CSS |
| para:0191cf49 | not-lost | low | none | text-present | Every template's frontmatter; the Gotchas state `size` values |
| para:3790d1f7 | removed-on-merit | low | drop | generic-model-knowledge | A Gaussian-integral `$$` block, a generic LaTeX example |
| para:0de69adc | removed-on-merit | low | drop | wrong | `<div style="text-align:center">` is stripped by Marp Core (no style attribute in the allowlist) |
| para:37ae2483 | not-lost | low | none | text-present | image-patterns.md filter list includes `contrast:1.5` |
| para:7ec489d5 | not-lost | low | none | text-present | marp-syntax.md lists `header` and `footer` as local directives; frontmatter form is the scope table's first row |
| para:a605a68d | not-lost | low | none | text-present | Template frontmatter |
| para:7e9b257f | not-lost | low | none | text-present | marp-syntax.md: `invert` in the built-in themes table |
| para:9a4383a1 | not-lost | low | none | text-present | image-patterns.md filter list includes `invert` |
| para:35244096 | removed-on-merit | low | drop | out-of-scope | A link to a third-party emoji cheat sheet |
| para:4c76f736 | removed-on-merit | low | drop | out-of-scope | A link to a third-party GitHub Marketplace action; export.md builds with the CLI directly |
| para:4bf9efba | not-lost | low | none | text-present | marp-syntax.md fit-heading bullet |
| para:bb5a9760 | not-lost | low | none | text-present | image-patterns.md filter list includes `sepia` |
| para:74d1c242 | not-lost | low | none | text-present | image-patterns.md "Side-by-side comparison" row |
| para:bbb7bfa7 | not-lost | low | none | text-present | marp-syntax.md built-in table (uncover) and the Validate lint on built-in themes |
| para:a9521df7 | removed-on-merit | low | drop | generic-model-knowledge | A quadratic-formula `$$` block, a generic LaTeX example |
| para:3c605010 | not-lost | low | none | text-present | marp-syntax.md: `<!-- header: '' -->` clears a header |
| para:42b195b3 | not-lost | low | none | text-present | marp-syntax.md built-in table (gaia) |
| para:358886af | not-lost | low | none | text-present | Every template's `_class: lead` title slide |
| para:ca5ffd31 | removed-on-merit | low | drop | generic-model-knowledge | A one-line intro to the best-practices file |
| para:277b152a | removed-on-merit | low | drop | generic-model-knowledge | A one-line intro to the syntax file; marp-syntax.md has its own intro |
| para:530464f2 | not-lost | low | none | text-present | marp-syntax.md Emoji bullet (`:rocket:`) |
| para:1ac5a02f | not-lost | low | none | text-present | image-patterns.md filter list includes `hue-rotate:180deg` |
| para:c70e66f0 | removed-on-merit | low | drop | generic-model-knowledge | A one-line intro to the advanced-features file |
| para:13d6afd2 | not-lost | low | none | text-present | marp-syntax.md Math bullet (`$inline$`) |
| para:9955ba0e | not-lost | low | none | text-present | image-patterns.md filter list includes `opacity:0.5` |
| para:410dd2f7 | not-lost | low | none | text-present | The Gotchas say which HTML renders by default and when `--html` is needed |
| para:898006c3 | removed-on-merit | low | drop | generic-model-knowledge | "Specify local fonts with an absolute path" is ordinary CSS; the Gotchas keep the font-fallback rule for Noto Sans JP |
| para:268b00c4 | not-lost | low | none | text-present | image-patterns.md filter list includes `saturate:2` |
| para:0aee5d31 | not-lost | low | none | text-present | image-patterns.md filter list includes `blur:5px` |
| para:adcff45b | not-lost | low | none | text-present | marp-syntax.md Emoji bullet |
| para:ddd0d516 | not-lost | low | none | text-present | The style table maps creative and event decks to colorful and gradient |
| para:40df1324 | removed-on-merit | low | drop | generic-model-knowledge | A one-line lead-in to a front matter snippet |
| para:b47c52bd | not-lost | low | none | text-present | marp-syntax.md Math bullet |
| para:056984d8 | not-lost | low | none | text-present | Validate lint: `marp: true` in the frontmatter |
| para:f23d486a | not-lost | low | none | text-present | The templates load Noto Sans JP with `@import`; the Gotchas keep the fallback rule |
| para:d3d6e895 | not-lost | low | none | text-present | marp-syntax.md states which features work in all built-in themes |
| para:6289a559 | not-lost | low | none | text-present | Gotchas: local images need `--allow-local-files` in PDF, PPTX and PNG |
| para:87ad077a | not-lost | low | none | text-present | marp-syntax.md table: `invert` class |
| para:027f6321 | not-lost | low | none | text-present | The style table maps academic and text-first decks to minimal |
| para:b9edb2ca | removed-to-fit | real | restore-references | users-ask-by-name | The VS Code preview shortcut (Ctrl+Shift+V) returns with the s079 Marp for VS Code section |
| para:d8b608cb | not-lost | low | none | text-present | Validate lint: every image path resolves relative to the deck file |
| para:adf7fb2c | removed-on-merit | low | drop | wrong | "Centered, large serif font" for uncover is wrong: uncover uses a sans-serif stack (marp-core themes/uncover.scss) |
| para:c3754908 | removed-on-merit | low | drop | generic-model-knowledge | A "use for" bullet for a built-in theme; the table's Look column covers it |
| para:dc547821 | not-lost | low | none | text-present | marp-syntax.md Math bullet |
| para:40ae2f21 | removed-on-merit | low | drop | generic-model-knowledge | A "use for" bullet for gaia (youth audiences); the table's Look column covers it |
| para:70908a8f | removed-on-merit | low | drop | generic-model-knowledge | A "use for" bullet for uncover (elegant impression) |
| para:7c58b3ff | removed-on-merit | low | drop | generic-model-knowledge | A "use for" bullet for gaia (design talks) |
| para:0dc068f1 | removed-to-fit | real | restore-references | users-ask-by-name | The VS Code preview shortcut (Cmd+Shift+V on macOS) returns with the s079 Marp for VS Code section |
| para:e1980922 | not-lost | low | none | text-present | marp-syntax.md table: gaia `lead` centers content |
| para:f428141d | removed-on-merit | low | drop | generic-model-knowledge | A "use for" bullet for gaia (visual impact) |
| para:9f8ab4b8 | not-lost | low | none | text-present | The style table maps dark requests to dark and tech |
| para:7e0ebbe7 | removed-on-merit | low | intended-change | fact-update | marp-syntax math bullet said MathJax is the default; Marp Core uses the first registered plugin and recommends declaring math: mathjax or math: katex, so the bullet says to declare it (Marp Core docs/markdown.md, checked 2026-11-13) |
| s048 (preamble) | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) the template's sample slide text moved from Japanese to English (Presentation, Agenda, Topic1, Slide, Point1 and the style subtitle) because every artifact is written in English; the CSS rules in this section are unchanged |
| s049 (preamble) | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) the template's sample slide text moved from Japanese to English (Presentation, Agenda, Topic1, Slide, Point1 and the style subtitle) because every artifact is written in English; the CSS rules in this section are unchanged |
| s052 (preamble) | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) the template's sample slide text moved from Japanese to English (Presentation, Agenda, Topic1, Slide, Point1 and the style subtitle) because every artifact is written in English; the CSS rules in this section are unchanged |
| s053 (preamble) | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) the template's sample slide text moved from Japanese to English (Presentation, Agenda, Topic1, Slide, Point1 and the style subtitle) because every artifact is written in English; the CSS rules in this section are unchanged |
| s056 (preamble) | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) the template's sample slide text moved from Japanese to English (Presentation, Agenda, Topic1, Slide, Point1 and the style subtitle) because every artifact is written in English; the CSS rules in this section are unchanged |
| s051 (preamble) | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) the template's sample slide text moved from Japanese to English because every artifact is written in English, and the closing slide now carries the final class (see s050); the CSS rules in this section are unchanged |
| s047 (preamble) | removed-on-merit | low | intended-change | fact-update | (2026-11-14, call delegated to the controller) template-basic.md: added `section.lead.final { border-bottom: none; }` after the `section.lead` rule, because `section.lead` and `section.final` have the same specificity and the later `lead` rule brought the border back on a `<!-- _class: lead final -->` closing title; every existing rule is kept |
| s050 (preamble) | removed-on-merit | low | intended-change | fact-update | (2026-11-14, call delegated to the controller) template-colorful.md: added `section.lead.final { border-bottom: none; }` after the `section.lead` rule for the same reason as s047; every existing rule is kept |
| s052 (preamble) | removed-on-merit | low | intended-change | fact-update | (2026-11-14, call delegated to the controller) template-dark.md: added `section.lead.final { border-bottom: none; }` after the `section.lead` rule for the same reason as s047; every existing rule is kept |
| s058 (preamble) | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) template-tech.md sample slide text moved from Japanese to English (Presentation, Technical (Code-focused), Agenda, Topic1, Slide, Point1) because every artifact is written in English; the CSS rules in this section are unchanged |
| para:f09a5421 | removed-on-merit | low | intended-change | fact-update | (2026-11-14, call delegated to the controller) The Validate intro "With Marp CLI (`npx @marp-team/marp-cli`, called `marp` below)" and its `marp` alias are replaced by `npx --yes @marp-team/marp-cli` written out in both commands, with Node.js and network access stated as requirements and the offline outcome (report the deck as not visually validated); the alias was not a real command in an agent shell |
| para:fcc3baa3 | removed-on-merit | low | intended-change | fact-update | (2026-11-14, call delegated to the controller) export.md line 3 said "Checked against Marp CLI 4.5 (`marp --help`)", a check that was never run; it now names the checks that were: the Marp CLI 4.5.1 README and a Marp CLI 4.5.1 run (`--version` v4.5.1 with Marp Core v4.4.0; an HTML render run from the pnpm store with node, checked 2026-11-14); the official-documentation link is kept |
| s059 (preamble) | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) template-tech.md sample slide text moved from Japanese to English (Presentation, Technical (Code-focused), Agenda, Topic1, Slide, Point1) because every artifact is written in English; the CSS rules in this section are unchanged |
| para:9c480253 | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) SKILL.md Existing deck step 2 ("Render the deck, or lint it without the CLI (see "Validate")") keeps its wording and gains the check against the deck's own style block and registered theme: an existing deck is never assumed to be an untouched bundled template, a deck with `theme: default` and its own `<style>` keeps its custom classes, and the built-in class list applies only when the deck uses no style block |
| para:b8cd5caf | removed-on-merit | low | intended-change | scope-change | (2026-11-14, call delegated to the controller) SKILL.md Save: the paragraph keeps every sentence and gains one: when an existing deck is written to a different directory than its source, image references are kept working by rebasing the relative paths or copying the assets, and the path changes and any unresolved asset are reported |
