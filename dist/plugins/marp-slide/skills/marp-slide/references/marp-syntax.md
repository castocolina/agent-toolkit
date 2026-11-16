# Marp Directive and Built-in Theme Notes

Only the semantics that are easy to get wrong. Full lists: https://marpit.marp.app/directives and https://github.com/marp-team/marp-core

## Directive scope

| Form | Scope |
|---|---|
| frontmatter `key: value` | whole deck from slide 1 |
| `<!-- key: value -->` | this slide and every later slide (local directives only) |
| `<!-- _key: value -->` | this slide only |

- Global directives (`theme`, `style`, `headingDivider`, `lang`; Marp Core adds `size`, `math`) ignore the underscore and position: one value for the whole deck, the last definition wins.
- Local directives: `paginate`, `header`, `footer`, `class`, `backgroundColor`, `backgroundImage`, `backgroundPosition`, `backgroundRepeat`, `backgroundSize`, `color`.
- `<!-- _class: lead invert -->` sets several classes. `class` replaces the slide's classes rather than adding to them, so `<!-- _class: warm -->` after a `<!-- class: lead -->` drops `lead`.
- `<!-- header: '' -->` clears a header from that slide onward; `<!-- _paginate: false -->` hides one page number.
- `headingDivider: 2` starts a new slide at every `#` and `##`, so the deck needs no `---`; a manual `---` right before such a heading leaves an empty slide.

## Content features (Marp Core)

- Fit heading: `## <!-- fit --> Long title` scales one heading to the slide width. It works only in themes that declare `@auto-scaling` (all built-ins, so every bundled template); prefer a shorter heading.
- Math: `$inline$` and `$$ block $$`, always declare the library with `math: mathjax` or `math: katex`, because the default depends on the Marp Core build and Marp Core recommends declaring it whenever a deck uses math (https://github.com/marp-team/marp-core/blob/main/docs/markdown.md, checked 2026-11-13). Macros that MathJax accepts may fail under KaTeX.
- Emoji shortcodes such as `:rocket:` render as emoji images; unknown shortcodes stay as text.
- Speaker notes: any non-directive HTML comment.
- Fragmented lists (Marpit, https://marpit.marp.app/fragmented-list): a bullet list written with `*` markers, or an ordered list written with `1)` markers, becomes fragments that the HTML presenter reveals one item at a time. A normal `-` bullet or `1.` number stays a static list. Use them when the user wants points revealed progressively; PDF and PPTX show every item.

## Built-in themes

Use these only when the user asks for a built-in theme instead of a bundled template.

| Theme | Classes it defines | Look |
|---|---|---|
| `default` | `invert` | light, GitHub-like |
| `gaia` | `lead`, `invert`, `gaia` (alternate color scheme) | warm light, larger type |
| `uncover` | `invert` | minimal, centered |

`lead` exists only in `gaia` among the built-ins, and `invert` exists in all three (confirmed in the Marp Core 4.4.0 theme CSS, checked 2026-11-14); the bundled templates define their own `section.lead`. Recolor `gaia` through its CSS variables in a `<style>` block:

```css
section {
  --color-background: #fff;
  --color-foreground: #333;
  --color-highlight: #c2255c;
}
```

### Example: a short deck on the `default` theme

Use for a plain status report with no bundled template. `default` has no `lead` class, so the title slide uses `invert` (the only class this theme defines) and the other slides stay plain. Rendered to HTML with Marp CLI 4.5.1 (checked 2026-11-14):

```markdown
---
marp: true
theme: default
paginate: true
---

<!-- _class: invert -->

# Project Report

October 2024

---

## Agenda

1. Progress status
2. Challenges and solutions
3. Future plans

---

## Progress status

- Task A: completed
- Task B: in progress
- Task C: on schedule
```

### Example: a short deck on the `gaia` theme

Use for a creative launch or design talk that wants the built-in `gaia` look. `lead` and `gaia` exist only in this theme, and `lead gaia` on one slide switches that slide to the alternate color scheme (a blue background in the Marp Core 4.4.0 CSS, checked 2026-11-14). Rendered to HTML with Marp CLI 4.5.1 (checked 2026-11-14):

```markdown
---
marp: true
theme: gaia
---

<!-- _class: lead -->

# New Product Launch

Innovative design

---

## Concept

**Three pillars**

1. Beauty
2. Speed
3. Usability

---

<!-- _class: lead gaia -->

## Next step

Pilot with five customers
```
