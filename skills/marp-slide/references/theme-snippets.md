# Theme Snippets: Reusable Rules for Business, Tech, Dark, Colorful, Gradient and Basic

Copy-ready rules from the retired `theme-business.css`, `theme-tech.css`, `theme-dark.css`, `theme-colorful.css`, `theme-gradient.css` and `theme-default.css`, rewritten against the current templates. Paste the block you need at the end of the deck's `<style>` block, inside the same `<style>` element, so it can use that template's color variables (`--color-heading`, `--color-accent`, `--color-border`, in tech `--color-code-bg` and `--font-code`, in colorful `--color-accent-1` to `--color-accent-3`). Do not paste a snippet into another template: its variables do not exist there.

HTML needs no `--html` flag here: Marp Core keeps `div`, `span` and `class` without it (see `theme-css-guide.md` for the rule and the blank-line requirement inside a `div`). Only the `style` attribute is stripped, so every look below is a class plus a rule (a `div` and a `span` with these classes kept their class in a Marp CLI 4.5.1 HTML render, checked 2026-11-14).

The business and tech templates have no bottom border, so they need no `final` class; do not use `section:last-of-type` for a closing slide (Marp wraps every slide in its own SVG, so it matches every slide).

## Business (`template-business.md`)

The template already styles tables (navy header row, zebra rows), `strong` and inline `code`. These rules add what it lacks.

Callout box. Use for one key takeaway on a slide that has other content. Put a blank line after the opening `<div class="highlight-box">` and before `</div>` so the Markdown inside renders:

```css
section .highlight-box {
  background-color: #eff6ff;
  border-left: 4px solid var(--color-accent);
  padding: 20px;
  margin: 20px 0;
  border-radius: 4px;
}
```

Big number. Use for one headline figure, written `<div class="number">42%</div>` followed by a one-line caption:

```css
section .number {
  font-size: 48px;
  font-weight: 700;
  color: var(--color-accent);
  line-height: 1;
}
```

Numbered step badge. Use for a short process list, one per line: `<span class="step">1</span> Collect requirements`. Keep to 5 steps or fewer per slide:

```css
section .step {
  display: inline-block;
  width: 36px;
  height: 36px;
  background-color: var(--color-heading);
  color: #ffffff;
  border-radius: 50%;
  text-align: center;
  line-height: 36px;
  font-weight: 700;
  margin-right: 12px;
}
```

Quote. Use for a customer or stakeholder quotation written as a Markdown `>` block (body text `#6b7280` on white passes the 4.5:1 contrast check):

```css
section blockquote {
  border-left: 4px solid var(--color-accent);
  padding-left: 20px;
  color: #6b7280;
  font-style: italic;
  margin: 20px 0;
  font-size: 20px;
}
```

Link style. Use when the deck shows URLs (the hover rule only matters in the HTML presenter; PDF and PPTX ignore it):

```css
section a {
  color: var(--color-accent);
  text-decoration: none;
  border-bottom: 1px solid var(--color-accent);
}

section a:hover {
  color: var(--color-heading);
  border-bottom-color: var(--color-heading);
}
```

## Tech (`template-tech.md`)

The template already styles `pre`, inline `code`, headings with `#` prefixes and `strong`. These rules add what it lacks.

Styled table. Use for a comparison or option matrix; the header row takes the heading color on the code background:

```css
section table {
  border-collapse: collapse;
  width: 100%;
  margin: 20px 0;
}

section th, section td {
  border: 1px solid var(--color-border);
  padding: 10px;
  text-align: left;
}

section th {
  background-color: var(--color-code-bg);
  color: var(--color-heading);
  font-family: var(--font-code);
}
```

Link style. Use when the deck shows URLs; links take the heading blue and underline on hover in the HTML presenter:

```css
section a {
  color: var(--color-heading);
  text-decoration: none;
}

section a:hover {
  text-decoration: underline;
}
```

Quote. Use for a quotation or a one-line takeaway (`#8b949e` on the near-black background passes the 4.5:1 contrast check):

```css
section blockquote {
  border-left: 4px solid var(--color-accent);
  padding-left: 20px;
  color: #8b949e;
  font-style: italic;
  margin: 20px 0;
}
```

Terminal block. Use for shell output that is not a fenced code block, written `<div class="terminal">` with the command on one line. The rule prints a single `$ ` prompt before the block, so use one block per command; a multi-line session belongs in a normal fenced code block:

```css
section .terminal {
  background-color: #000000;
  color: #00ff00;
  font-family: var(--font-code);
  padding: 20px;
  border-radius: 6px;
  font-size: 16px;
}

section .terminal::before {
  content: '$ ';
  color: #00ff00;
  font-weight: 700;
}
```

## Dark (`template-dark.md`)

The template already styles headings with a glow, inline `code` and `strong`. This rule adds what it lacks.

Link with glow. Use when the deck shows URLs; links take the heading cyan with an underline, and the glow on hover shows only in the HTML presenter (PDF and PPTX ignore it):

```css
section a {
  color: var(--color-heading);
  text-decoration: none;
  border-bottom: 1px solid var(--color-heading);
}

section a:hover {
  text-shadow: 0 0 10px rgba(97, 218, 251, 0.5);
}
```

## Colorful (`template-colorful.md`)

The template already styles the gradient headings, the footer bar and `strong` in the pop colors. These rules add the colored list markers and the rainbow divider the retired theme file had.

Colored bullet markers. Use for every list in the deck; the marker takes the pink heading color and bold weight:

```css
section li::marker {
  color: var(--color-heading);
  font-weight: 700;
}
```

Rainbow divider. Use between two blocks on one slide. Write it as an HTML `<hr>` tag: `---` and `***` are slide breaks in Marp, so a Markdown rule never reaches this style (an `<hr>` tag stayed in the output of a Marp CLI 4.5.1 HTML render without `--html`, checked 2026-11-14):

```css
section hr {
  border: none;
  height: 4px;
  background: linear-gradient(90deg, var(--color-accent-1), var(--color-accent-2), var(--color-accent-3));
  margin: 30px 0;
  border-radius: 2px;
}
```

## Gradient (`template-gradient.md`)

The retired `theme-gradient.css` also carried a translucent box that no current file keeps.

Frosted text box. Use for one block of text over the gradient that needs a calmer backdrop. Put a blank line after the opening `<div class="text-box">` and before `</div>` so the Markdown inside renders. Check text contrast on every `warm` and `teal` slide variant after adding it:

```css
section .text-box {
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

## Basic (`template-basic.md`)

The retired `theme-default.css` carried one helper class that no current file keeps.

Bad-example box. Use for a "do not do this" line next to a good one, for example in a guideline or style-guide deck. Written `<div class="bad-example">` with the text on one line, so no blank lines are needed:

```css
section .bad-example {
  background-color: #fbe9e7;
  color: #c62828;
  padding: 8px 16px;
  border-radius: 4px;
}
```
