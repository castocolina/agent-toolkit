---
name: meme-factory
description: Generate template-based image memes with memegen.link, including encoded captions, sizing, and custom backgrounds, or textual Markdown memes such as greentext and copypasta. Use for meme requests, familiar reaction/comparison formats, photo captions when an image URL or template is available, or meme URLs for Slack, docs, or social posts. Not for writing a standalone funny caption for an unprovided photo, editing text in an existing PNG/image meme, creating slide decks with humorous illustrations, graphic design, logos, serious infographics, or turning video into GIFs.
---

# Meme Factory

## Quick reference

- Image URL: `https://api.memegen.link/images/{template}/{top}/{bottom}.png`; query parameters can set size/layout/style.
- Text-only formats: read `references/markdown-memes-guide.md`.
- Helper: `python skills/meme-factory/scripts/meme_generator.py generate <template> '<top>' '<bottom>'`.
- Complete raw captions go to `MemeGenerator.generate(template, top_text, bottom_text)`; never pre-encode them because the helper encodes again.

## Build the joke

1. Identify the contrast, reversal, or escalation that makes the situation funny.
2. Assign each panel/caption a narrative role: setup, rejected option, contrast, or payoff.
3. Draft the payoff first, then the setup; keep each caption short enough to survive the template crop and render legibly.
4. Check template capacity before choosing it. The helper's documented `generate` interface supports two caption fields only; use multi-panel templates only if each panel can be represented by those two fields, otherwise choose another template.
5. Avoid sending private incident details, customer names, credentials, or internal URLs to memegen.link; its URL may be logged or shared.

## Templates

| Template | Best fit |
|---|---|
| `buzz` | Ubiquity / repeated problem |
| `drake` | Two-option contrast |
| `success` | Clear win |
| `fine` | Things going wrong |
| `fry` | Ambiguity or uncertainty |
| `changemind` | Opinion plus challenge |
| `mordor` | Difficult task / warning |
| `distracted` | Priority conflict only when two captions adequately express it |

When outcome is uncertain, do not imply success. `suggest` prioritizes explicit success/failure terms; ambiguous deployment/testing contexts should stay neutral.

## Encoding traps

Pass raw text to the helper. Its encoder maps spaces to `_`, `%` to `~p`, `/` to `~s`, `?` to `~q`, `#` to `~h`, `-` to `--`, `_` to `__`, and `"` to `''`; single quote needs no transformation. Never pass already encoded text to this helper.

A template ID must match the API's actual ID (e.g. `changemind`, not prose variants). Use `https://api.memegen.link/templates/` to confirm uncertain IDs. Watermark control, where supported, is `?watermark=none`; verify the specific API behavior rather than assuming it.

Validate the resulting URL/image and text legibility before presenting it. Add concise alt text describing both image and joke. For text-only memes, preserve intentional literal formatting and do not call the image API.
