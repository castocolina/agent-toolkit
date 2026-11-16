# Marp Theme CSS Notes

How Marp treats CSS, beyond ordinary CSS. Official specification: https://marpit.marp.app/theme-css (theme sources: https://github.com/marp-team/marp-core/tree/main/themes)

## How embedded CSS is scoped

- Every slide is a `<section>` with a fixed size (1280x720 for 16:9); `:root` in a deck's `<style>` or a theme means each `section`, which is why the templates keep their variables there.
- Selectors are scoped to slides, so `h2`, `footer` and `section::after` (the page number) style every slide; `<style scoped>` limits a block to the slide it sits on.
- `header` and `footer` are elements the `header`/`footer` directives insert; position them absolutely inside `section`.
- Page number text comes from `attr(data-marpit-pagination)` and `attr(data-marpit-pagination-total)` on `section::after`.
- Per-slide styling uses classes from `_class`: `section.warm { ... }`. Positional selectors on `section` (`:nth-child`, `:nth-of-type`) never match a later slide because each slide sits in its own inline SVG.
- `@media` queries for screen width do nothing useful: slides are fixed-size and scaled as a whole.

## Turn a template into a reusable theme file

Use this when several decks must share one style or a custom `@size` is needed (`@size` works only in a theme file, not in a deck's `<style>`).

1. Create `name.css` whose first lines are `/* @theme name */` and `@import 'default';` (Marpit resolves the theme name), then paste the template's `<style>` contents.
2. Add any sizes as metadata comments, such as `/* @size A4 1123px 794px */`, then `size: A4` in the deck works.
3. In the deck, delete the `<style>` block and set `theme: name`.
4. Render with the theme registered: `marp --no-stdin deck.md --theme-set name.css -o deck.html`. `--theme-set` takes several values, so put it after the input file; written before it, it swallows the deck path and Marp prints its help instead of converting.

A theme written from scratch without `@import` also needs `/* @auto-scaling true */` for `<!-- fit -->` headings to work.

## Contrast after color edits

Check text against each gradient stop, not the middle; for gradient text (`background-clip: text`, as in the colorful template) check both ends of the text gradient.
