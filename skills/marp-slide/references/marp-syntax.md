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
- Math: `$inline$` and `$$ block $$`, rendered by MathJax (default) or KaTeX via `math: katex`. Macros that MathJax accepts may fail under KaTeX.
- Emoji shortcodes such as `:rocket:` render as emoji images; unknown shortcodes stay as text.
- Speaker notes: any non-directive HTML comment.

## Built-in themes

Use these only when the user asks for a built-in theme instead of a bundled template.

| Theme | Classes it defines | Look |
|---|---|---|
| `default` | `invert` | light, GitHub-like |
| `gaia` | `lead`, `invert`, `gaia` (alternate color scheme) | warm light, larger type |
| `uncover` | `invert` | minimal, centered |

`lead` exists only in `gaia` among the built-ins; the bundled templates define their own `section.lead`. Recolor `gaia` through its CSS variables in a `<style>` block:

```css
section {
  --color-background: #fff;
  --color-foreground: #333;
  --color-highlight: #c2255c;
}
```
