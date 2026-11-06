# Marp CLI Export and CI

Checked against Marp CLI 4.5 (`marp --help`). Official documentation: https://github.com/marp-team/marp-cli

## Commands

| Output | Command | Needs a browser |
|---|---|---|
| HTML presenter (fragments, transitions) | `marp --no-stdin deck.md -o deck.html` | no |
| PDF | `marp --no-stdin deck.md --pdf -o deck.pdf` | yes |
| PDF with notes and bookmarks | add `--pdf-notes --pdf-outlines` | yes |
| PowerPoint | `marp --no-stdin deck.md --pptx -o deck.pptx` | yes |
| One PNG per slide | `marp --no-stdin deck.md --images png -o out/deck.png` (writes `deck.001.png`, ...) | yes |
| Speaker notes as text | `marp --no-stdin deck.md --notes -o deck.txt` | yes |
| Folder of decks | `marp --no-stdin -I slides/ -o dist/` | per format |

- Add `--html` only if the deck needs raw HTML beyond the default allowlist (for example `style=` attributes); it renders every HTML tag, scripts included, so never add it for an untrusted deck.
- `--pptx` slides are usually pre-rendered background images, so the text is not editable; the experimental `--pptx-editable` also needs LibreOffice Impress.

## Browser

Pick the browser kind with `--browser auto|chrome|edge|firefox` and a binary outside the usual install paths with `--browser-path` or `CHROME_PATH`. Without any browser, use the official image:

```bash
docker run --rm --init -v "$PWD":/home/marp/app/ -e LANG="$LANG" -e MARP_USER="$(id -u):$(id -g)" marpteam/marp-cli deck.md --pdf --allow-local-files
```

On Linux, `MARP_USER` keeps the output owned by you instead of failing on a permission error in the mounted folder.

## GitHub Actions

GitHub-hosted Ubuntu runners include Node.js and Google Chrome, so no container is needed:

```yaml
name: Build slides
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx --yes @marp-team/marp-cli@4 --no-stdin slides.md --pdf --allow-local-files -o slides.pdf
      - uses: actions/upload-artifact@v4
        with:
          name: slides
          path: slides.pdf
```

Pin the CLI major version (`@4`) so a new release cannot change the output unannounced.
