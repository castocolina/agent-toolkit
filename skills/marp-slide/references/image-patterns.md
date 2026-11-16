# Marp Image Patterns

Marpit image syntax as Marp Core renders it. Official documentation: https://marpit.marp.app/image-syntax

## Pick a pattern

| Need | Markdown | Note |
|---|---|---|
| Figure inside the text flow | `![w:600px](diagram.png)` | `w:`/`h:` (or `width:`/`height:`) take any CSS length |
| Image beside bullets | `![bg right:40%](photo.png)` | the percentage is the image's share; text reflows into the rest; `left` mirrors it |
| Full-slide background | `![bg](hero.jpg)` | default `cover` |
| Whole image, letterboxed | `![bg contain](chart.png)` | `fit` is an alias; `auto` keeps the original size; `![bg 80%]` sets `background-size` |
| Side-by-side comparison | `![bg](before.png)` then `![bg](after.png)` | equal split, left to right in source order |
| Stacked comparison | `![bg vertical](a.png)` then `![bg](b.png)` | `vertical` on any one image flips the split |
| Text over a photo | `![bg brightness:0.5](hero.jpg)` | darken the photo rather than adding a text shadow |

## Behavior that surprises

- Once any `bg` image on a slide has `left` or `right`, every `bg` image on that slide splits inside that side region: `![bg](a.png)` plus `![bg right:58%](b.png)` puts both images in the right 58%, each about 29% wide, and leaves the rest for text. You cannot put one image left and another right; for a full-width comparison mark neither.
- Filters (`blur:5px`, `brightness:0.5`, `contrast:1.5`, `grayscale`, `sepia`, `saturate:2`, `hue-rotate:180deg`, `invert`, `opacity:0.5`, `drop-shadow`) combine in one alt text, such as `![bg blur:4px brightness:0.6](x.jpg)`, and apply to `bg` images too.
- A full-slide `bg` image sits behind the text and never pushes it aside; use `left`/`right` when text and image must not overlap.
- Paths resolve relative to the Markdown file.
- A missing image renders as an empty area and the conversion still succeeds (a local one only logs a warning), so check every image slide in the render. Remote URLs need network access at render time.
