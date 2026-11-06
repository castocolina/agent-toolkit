---
name: meme-factory
description: Build memegen.link image-meme URLs with real template IDs, correctly escaped captions, size and layout options, or a custom background image, and write text-only memes such as greentext and copypasta. Use when the user asks for a meme, a reaction or comparison image (drake, "this is fine", "X everywhere"), a meme URL for Slack, a PR, docs or a social post, or captions on an image URL they supply. Not for a caption on a photo with no image URL or template, editing text inside an existing image file, logos or graphic design, slide decks, serious infographics, or turning video into GIFs.
---

# Meme Factory

## Workflow

1. **Text-only request** (greentext, copypasta, ASCII, "no image"): read `references/markdown-memes-guide.md`, answer in text, and stop. Do not build an image URL.
2. **Redact first.** Captions travel in the URL to a public third-party service, which logs them, and anyone the link is pasted to can read them. Replace customer names, tokens or credentials, internal URLs or hostnames and incident IDs with a generic word, and tell the user what you replaced.
3. **Pick the template** from the table below. Check that the joke fits the template's line count before writing it.
4. **Write the joke.** First answer three questions. Who will see it: team Slack, a PR, or a public post? Who is the butt of the joke: the situation, the tool or yourselves, never a named teammate or customer? Which channel, and does its tone allow it? Then name the contrast and write the payoff (last line) first, then the setup. Keep each line under about 30 characters (about 20 on a 3-line template).
5. **Build the URL** from the skill root. Pass one raw caption per template line (as many as `lines`) and let the helper escape them:
   `python3 scripts/meme_generator.py generate <id> '<caption>'... [--width N] [--height N] [--layout top] [--font ID] [--style NAME|URL] [--background URL] [--extension png|jpg|gif|webp] [--markdown --alt '<picture and joke>']`
   No Python: build it by hand (see Hand-built URLs) and keep every query parameter you chose.
6. **Check it.** If you can fetch the URL, expect HTTP 200 and an image. 404 means a wrong template ID; 422 means an unknown `style` or `font`, or a width or height of 1-9. If you can view the image and a line wraps past two rows or is cropped, shorten it and regenerate once. If it still does not fit, say so and give the line count the template needs. Present the result as a Markdown image whose alt text describes both the picture and the joke.

Unsure which template fits? `python3 scripts/meme_generator.py suggest "<situation>"` runs a keyword heuristic (`--json` goes before the subcommand: `--json suggest ...`, `--json list-templates`). Treat it as a hint only. It returns `fry` for negated or uncertain outcomes ("did not fail", "might be broken") so the meme never implies a success nobody confirmed.

## Templates

| ID | Lines | Use for |
|---|---|---|
| `buzz` | 2 | X, X everywhere |
| `drake` | 2 | Drake: reject top, prefer bottom |
| `success` | 2 | Success Kid, confirmed wins only |
| `fine` | 2 | This is Fine |
| `fry` | 2 | Not sure if; also any unconfirmed outcome |
| `mordor` | 2 | One does not simply |
| `cmm` | 1 | Change My Mind hot take: one line only |
| `db` | 3 | Distracted Boyfriend: pass three captions |
| `custom` | any | The user's own image: `--background <image URL>` |

For any other meme, look up its `id` and `lines` in `https://api.memegen.link/templates/` (JSON). Never guess an ID from the meme's name: `changemind`, `distracted` and `pikachu` all return 404 with an error image. `python3 scripts/meme_generator.py list-templates` prints the verified IDs the helper knows.

## Query parameters

- `width`, `height`: scale the image. Setting both pads it to the exact size, for example `1200` x `630` for an Open Graph card.
- `layout`: only `default` or `top` (all text at the top). Any other value is silently ignored.
- `font`: a font ID or alias from `https://api.memegen.link/fonts/`, such as `impact` or `notosans`.
- `style`: a name from the template's `styles` array, or an image URL to overlay.
- `background`: an image URL used as the background with template `custom`.

The helper URL-encodes all of these. When you build a URL by hand, percent-encode any URL you put in a query value.

## Hand-built URLs

Shape: `https://api.memegen.link/images/<id>/<caption1>/<caption2>.<ext>?<params>`. Each caption is exactly one path segment, so a `/` inside a caption is always text and becomes `~s`, never a bare `/`. Split the user's text into captions at `/` only when they list one caption per panel ("me / new framework / old codebase"); a single quoted caption keeps its slash. A line break inside a caption is `~n`; a new caption is a new segment.

1. Apply the memegen escapes below to each caption.
2. Then percent-encode every remaining character except ASCII letters, digits and `-._~'` (`+` becomes `%2B`, `:` becomes `%3A`, `é` becomes `%C3%A9`). The order matters: percent-encoding first creates `%` signs that step 1 would turn into `~p`.
3. Append every chosen query parameter, percent-encoding any URL inside one.

Worked example (checked live, HTTP 200): captions `café is 50% done?` and `a/b tests` on the user's image at 800 px wide:
`https://api.memegen.link/images/custom/caf%C3%A9_is_50~p_done~q/a~sb_tests.png?background=https%3A%2F%2Fwww.gstatic.com%2Fwebp%2Fgallery%2F1.png&width=800`

Step 2 on ASCII punctuation (checked live, HTTP 200): caption `C++ @ 9:00!` becomes `C%2B%2B_%40_9%3A00%21`.

| Text | Write | Text | Write | Text | Write |
|---|---|---|---|---|---|
| space | `_` | `_` | `__` | `-` | `--` |
| newline | `~n` | `?` | `~q` | `&` | `~a` |
| `%` | `~p` | `#` | `~h` | `/` | `~s` |
| `\` | `~b` | `<` | `~l` | `>` | `~g` |
| `"` | `''` | `'` | `'` | | |

## Gotchas

- **Never feed escaped text to the helper.** It escapes again, so `a_b` turns into `a__b` and renders a literal underscore.
- **Never leave a path segment empty.** Use `_` for a blank line (`/images/custom/_/text.png`). An empty segment (`//`) returns 404. The helper inserts `_` for you.
- **Never use a two-line template for a three-panel joke.** The third panel is lost. Check `lines` first.
- **Never say a deploy or test run succeeded unless the user confirmed it.** A meme posted to Slack or a PR is read as a status report, so a premature success meme tells the team a broken release is fine. Use `fry` while the outcome is unknown.
