# Marp CLI Export and CI

Checked against the Marp CLI 4.5.1 README and a Marp CLI 4.5.1 run (`--version` reports v4.5.1 with Marp Core v4.4.0; an HTML render ran from the pnpm store with node, checked 2026-11-14). Official documentation: https://github.com/marp-team/marp-cli

In this file `marp` means `npx --yes @marp-team/marp-cli` (no global install is assumed); the CI step below keeps the full form with the `@4` pin.

## Commands

| Output | Command | Needs a browser |
|---|---|---|
| HTML presenter (fragments, transitions) | `marp --no-stdin deck.md -o deck.html` | no |
| PDF | `marp --no-stdin deck.md --pdf -o deck.pdf` | yes |
| PDF with notes and bookmarks | add `--pdf-notes --pdf-outlines` | yes |
| PowerPoint | `marp --no-stdin deck.md --pptx -o deck.pptx` | yes |
| One PNG per slide | `marp --no-stdin deck.md --images png -o out/deck.png` (writes `deck.001.png`, ...) | yes |
| Speaker notes as text | `marp --no-stdin deck.md --notes -o deck.txt` | no |
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
      - uses: actions/checkout@vN        # replace vN: see below
      - run: npx --yes @marp-team/marp-cli@4 --no-stdin slides.md --pdf --allow-local-files -o slides.pdf
      - uses: actions/upload-artifact@vN # replace vN: see below
        with:
          name: slides
          path: slides.pdf
```

Replace each `vN` with the action's current major version, read from https://github.com/actions/checkout/releases and https://github.com/actions/upload-artifact/releases (checked 2026-11-13; both had moved well past `v4`). Pin the CLI major version (`@4`) so a new release cannot change the output unannounced.

## Images, theme and live serving

Source: https://github.com/marp-team/marp-cli (README option table), checked 2026-11-13. Run `marp --help` for the installed version's list.

- Images: `--images jpeg` writes one JPEG per slide (like `--images png`); `--image png` or `--image jpeg` converts only the first slide (a title-slide thumbnail). `--image-scale 2` renders at double resolution (default 1, and 2 for PPTX) without changing the slide size; `--jpeg-quality` sets JPEG quality (default 85). All of these need a browser.
- Theme from the command line: `--theme gaia` picks a built-in theme by name and `--theme custom.css` takes a CSS file (it needs no `@theme` comment). It overrides the deck's `theme:` directive. `--theme-set` (registering several themes by name) is covered in `theme-css-guide.md`.
- Live preview: `--watch` (`-w`) reconverts whenever the Markdown or a theme CSS file changes and refreshes an open HTML page; `--server` (`-s`) serves a folder over HTTP and converts on request (`?pdf`, `?pptx`; the port comes from `PORT`); `--preview` (`-p`) opens a preview window and turns watch on (it does not work in the Docker image).
- WARNING: `--watch`, `--server` and `--preview` never exit, so an agent shell that runs one in the foreground blocks forever. Start one only in a background process you will stop, or give the user the command to run themselves; for a single conversion drop the flag.

## HTML presenter features

Source: https://github.com/marp-team/marp-cli (README, bespoke template options), checked 2026-11-13. These apply only to the HTML output, not to PDF, PPTX or images.

- `--bespoke.progress` adds a progress bar on top of the deck (default off). Use it for a progress bar rather than hand-written CSS, which cannot rely on invented variables such as `--paginate`.
- `--bespoke.osc=false` hides the on-screen controller (default on).
- Slide transitions use the View Transition API, so they work only in browsers that support it: the `transition` local directive sets one (`transition: fade` in the frontmatter, `<!-- transition: cover -->` from a slide onward, `<!-- _transition: none -->` for one slide, `transition: fade 1s` for a duration), and `--bespoke.transition` switches the feature on or off for the whole output (default on). Built-in names: `fade`, `cover`, `push`, `wipe`, `zoom`, `cube`, `fall`, `none` (source: https://github.com/marp-team/marp-cli/tree/main/docs/bespoke-transitions, checked 2026-11-13). Marp is therefore not limited to static slides when the user wants animation.
- Fragmented lists (`*` bullets, `1)` numbered items) step through one item at a time here; see Gotchas in `SKILL.md`.
