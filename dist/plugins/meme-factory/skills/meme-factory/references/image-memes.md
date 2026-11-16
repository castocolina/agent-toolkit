# Image meme details

Read this after SKILL.md steps 3 to 6 when you need more than the template table and the escape table: a template outside the table, an extension or animation choice, a custom or screenshot background, a status code you cannot explain, worked requests, or where the URL will be posted. Facts below were checked live against `api.memegen.link` and the service README (https://github.com/jacebrowning/memegen) on 2026-11-07; re-read the live catalog when a value matters.

## More templates by use case

Template IDs are short, not the meme's full name. Line counts come from `https://api.memegen.link/templates/<id>`, which also lists the template's `styles`.

| ID | Lines | Use for |
|---|---|---|
| `drake` | 2 | Rejecting one thing, approving another; also a hard choice between two options |
| `gru` | 4 | A plan that goes wrong at the last step |
| `db` | 3 | Being distracted by something new |
| `cmm` | 1 | Stating an opinion confidently |
| `spongebob` | 2 | Mocking someone's statement |
| `pigeon` | 3 | Misidentifying something obvious |
| `success` | 2 | A small win, once confirmed |
| `ds` | 3 | The two-buttons meme (Daily Struggle): a hard choice between two buttons, a third caption for the sweating face |
| `custom` | any | Any image the user supplies, with `background` |

The long IDs `two-buttons`, `distracted-boyfriend`, `gru-plan`, `change-my-mind`, `mocking-spongebob`, `is-this-a-pigeon`, `success-kid`, `surprised-pikachu` and `uno-draw-25` all return 404. The working IDs are `db` (distracted-boyfriend), `gru` (gru-plan), `cmm` (change-my-mind), `spongebob` (mocking-spongebob), `pigeon` (is-this-a-pigeon), `success` (success-kid) and `ds` (Daily Struggle, the two-buttons meme, 3 lines; `https://api.memegen.link/templates/ds`, source https://knowyourmeme.com/memes/daily-struggle-two-buttons, checked 2026-11-07). There is no `surprised-pikachu` or `uno-draw-25` template at all (catalog checked 2026-11-07): say so, and offer a template from the table that fits the joke. `python3 scripts/meme_generator.py list-templates` prints more verified IDs.

## Image formats and animation

Put the extension at the end of the last caption. Without one, the service answers 302 and redirects to `.jpg`, so write it.

| Extension | Use |
|---|---|
| `.png` | Default, best quality |
| `.jpg` | Smaller files |
| `.gif`, `.webp` | Animated when the template has an animated background, or to animate the text on a static background; otherwise a still image |

A template whose `styles` list contains `animated` (for example `buzz`, `fine`, `fry`, `rollsafe`) also takes `?style=animated`. Pick `.webp` or `.gif` only when the destination displays them. Source: the Available Formats section of the memegen README, checked 2026-11-07.

## Endpoints

| Endpoint | Purpose |
|---|---|
| `/templates/` | List all templates (JSON, `id` and `lines`) |
| `/templates/{id}` | One template: its `lines` and `styles` |
| `/fonts/` | Font IDs and aliases |
| `/images/{id}/{caption1}/{caption2}.{ext}` | The meme image |

The service is free and open-source, needs no API key, keeps no state (the whole meme is in the URL) and renders each image on demand.

## Custom and screenshot backgrounds

Use template `custom` with `background=<image URL>`, percent-encoded. The service fetches that URL itself, so it must be publicly reachable. A private, localhost or intranet address, an invalid host or a URL that is not an image returns 415 (checked live). `/images/custom/a/b.png` with no `background` returns 422.

A screenshot of an app or a graph makes a good background for a meme that comments on it, but it must be hosted somewhere public first. That uploads the screenshot to the public web, so run the redaction step in SKILL.md on it too and ask before publishing anything internal.

Working example (HTTP 200):
`https://api.memegen.link/images/custom/_/my_background.png?background=https%3A%2F%2Fwww.gstatic.com%2Fwebp%2Fgallery%2F1.png`

## Social cards

Use `width=1200&height=630`, which pads the image to the exact size. Meta asks for at least 1200 x 630 pixels at about a 1.91:1 ratio (https://developers.facebook.com/docs/sharing/webmasters/images, checked 2026-11-07). Other platforms' preferred sizes have no vendor source here; ask the user or check the platform's docs.

## Worked requests

Request to URL, each checked with HTTP 200:

| Request | URL |
|---|---|
| bugs everywhere | `https://api.memegen.link/images/buzz/bugs/bugs_everywhere.png` |
| production is down (confirmed) | `https://api.memegen.link/images/fine/production_is_down/this_is_fine.png` |
| memory at 99% (percent is `~p`) | `https://api.memegen.link/images/fine/memory_usage_at_99~p/this_is_fine.png` |
| social card | `https://api.memegen.link/images/buzz/features/features_everywhere.png?width=1200&height=630` |
| text only at the top | `https://api.memegen.link/images/rollsafe/cant_have_bugs_in_production/_.png?layout=top` |

## Where the URL goes

- Slack and Discord: post the plain image URL ending in `.png` or `.jpg`; they usually show a preview. Also give the user the Markdown form in case the preview does not appear.

## Checks and diagnosis

- 404: wrong template ID or an empty path segment. 422: unknown `style` or `font`, a width or height of 1-9, or `custom` without `background`. 415: the `background` or `style` image URL is not publicly reachable or not an image.
