# marp-slide: sources

Checked 2026-11-13. Review only: no `track` call, no registry edit, no artifact edit.

## Origin

- The skill is a copy of `skills/marp-slide` from softaworks/agent-toolkit. `git diff --stat 3027f20f dbff837f -- skills/marp-slide` is empty, so the baseline equals the fork point. The one upstream commit is `06825f04` (Leonardo Flores, 2026-01-18, "feat: add 23 curated skills with comprehensive documentation"); `gh api repos/softaworks/agent-toolkit/commits?path=skills/marp-slide` returns only that commit, so upstream has not changed the skill since the fork.
- The same text exists in davila7/claude-code-templates (`cli-tool/components/skills/creative-design/marp-slide`, added 2026-01-25, identical SKILL.md frontmatter and README license line "This skill is part of the agent-skills project"). It is a later copy, not an origin; no earlier origin was found (web searches on the distinctive phrases "7 pre-designed themes", the Japanese trigger phrases and the file layout return only the softaworks and davila7 copies and aggregator pages). The original author beyond softaworks is unknown.
- Registry state: `docs/audit/upstream-sources.json` has no row with `skill: marp-slide`. Only the repo-level softaworks row (`skill: null`, `kind: repo`) exists.
- Credit state: `skills/marp-slide/README.md` has no credit line (it keeps the original license line "This skill is part of the agent-skills project", which must stay). The root `README.md` credits softaworks only in its header ("Fork of softaworks/agent-toolkit by @leonardocouy") and lists marp-slide in the skills table with no credit.

## Missing credit line

Add to `skills/marp-slide/README.md`, as a new `## Credits` section above `## License`, in the form the softaworks-derived skills use (for example `skills/database-schema-designer/README.md`):

```text
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The Marp tools themselves (Marpit, Marp Core, Marp CLI, Marp for VS Code) are by the Marp team; their pages are the `unversioned` rows below, so the README Resources list already links them.

## Proposed registry rows

The first row is the origin. The rest are the official documentation pages used for facts.md (each an `unversioned` row, as the plan asks; the Marp CLI README could instead be a `github-path` row `marp-team/marp-cli:README.md` on `main`, which `upstreams` can check for change, if the controller prefers a tracked source).

```json
{"skill": "marp-slide", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/marp-slide", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marp CLI README: https://github.com/marp-team/marp-cli", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marp CLI Docker image: https://hub.docker.com/r/marpteam/marp-cli", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marp Core, Markdown features (docs/markdown.md): https://github.com/marp-team/marp-core/blob/main/docs/markdown.md", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marp Core, Built-in themes: https://github.com/marp-team/marp-core/tree/main/themes", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marpit, Directives: https://marpit.marp.app/directives", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marpit, Image syntax: https://marpit.marp.app/image-syntax", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marpit, Theme CSS: https://marpit.marp.app/theme-css", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marpit, Fragmented list: https://marpit.marp.app/fragmented-list", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marpit, Inline SVG slide: https://marpit.marp.app/inline-svg", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "Marp for VS Code README: https://github.com/marp-team/marp-vscode", "ref": null, "credit": "Marp team"}
{"skill": "marp-slide", "kind": "unversioned", "source": "WCAG 2.2, Understanding contrast (minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html", "ref": null, "credit": "W3C"}
{"skill": "marp-slide", "kind": "unversioned", "source": "GitHub Actions runner images, Ubuntu 24.04: https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md", "ref": null, "credit": "GitHub"}
```

Notes for validation: every row passes `validate_entry` by shape (kebab-case skill that exists, allowed kind, `github-path` source `owner/repo:path` with a non-empty `ref`, `unversioned` with `ref` null and a non-empty source and credit). I did not write them to the registry (the brief forbids touching `docs/audit/upstream-sources.json`). Because `upstreams` reports `stale: false` for `unversioned` rows, the date in facts.md is the only age signal for those pages.

## skill-updater style review (review only)

Read `skills/skill-updater/SKILL.md`; no `track` call made; `upstreams` was not run because the artifact has no registry row yet (step 2: a credit/origin with no row means propose the row and make no `track` call).

- Upstream changes since the fork: none (single upstream commit, equal to the baseline). Adopt: none. Adapt: none. Ignore: not applicable.
- Origin row: once the first row above exists, the first `upstreams` run will report `stale: false` and `ours_updated` reads `skills/marp-slide/SKILL.md` and `references/`, which have local commits, so the `no local commit` error will not occur.
- Model-validity pass: the artifact's counter-habit rules are the Gotchas (never set `theme:` to a style label; never use `section:nth-child`; never rely on `style=`; `_class` replaces classes; pass `--no-stdin`). They are Marp behavior facts, each checked against the docs or source in facts.md, not model habits that a newer model may have outgrown, so no model probe result changes them. No model probe was run (no eval runner invoked; review only).

## Items for the restore brief (adopt and adapt)

Restore rows (from record.md), each rewritten in the current style into `references/` and checked by an eval where behavior changes:

1. Fragmented lists (s060): `*` for bullets and `1)` for ordered lists; the HTML presenter steps through them one by one (Marp CLI bespoke template; VS Code integrated browser also shows them); PDF and PPTX show everything. Add the `1)` form next to the existing Gotcha.
2. Live preview and serving (s073): `--watch`/`-w`, `--server`/`-s`, `--preview`/`-p` (not in Docker), with a warning that watch and server never exit, so an agent shell must not run them in the foreground.
3. `--theme` (s074): override by built-in name or CSS file; `--theme-set` stays in the theme guide.
4. Image output (s078): `--images jpeg`, `--image` (first slide only), `--image-scale 2`, `--jpeg-quality`.
5. Marp for VS Code (s079, s080, three `para:` rows, s086's marketplace link): `marp: true` turns the features on; preview with Ctrl+Shift+V (Cmd+Shift+V on macOS); export through the toolbar quick pick "Export slide deck..." (`markdown.marp.export`) to HTML, PDF, PPTX, PNG, JPEG, TXT; settings `markdown.marp.themes`, `markdown.marp.html` (not the deprecated `markdown.marp.enableHtml`), `markdown.marp.exportType`, `markdown.marp.browser`; marketplace id `marp-team.marp-vscode`. Put it in a new `references/vscode.md` (or a section of export.md) with a trigger in SKILL.md References.
6. Two-column and callout layouts (s083, folding in the working half of s071): a `div` with a class plus a rule in the style block (no `--html` needed; `style=` is stripped); tell the user the decision "split a slide rather than squeeze columns" still applies unless columns are requested.
7. Bespoke HTML features (s084, s100): `--bespoke.progress` (progress bar), `--bespoke.osc`, `--bespoke.transition` and the `transition` directive; HTML presenter only.
8. Slide count by talk length (s092): 5 min 5-8, 10 min 10-15, 20 min 15-25, labelled a rule of thumb.
9. `@import-theme` (s166): the preprocessor form of `@import`.

Fact fixes to apply (facts.md, outcome `corrected` or `pointer`):

- `--notes` needs no browser: fix the SKILL.md Gotchas line and the export.md table row (README: only PDF, PPTX and PNG/JPEG are marked as needing a browser).
- Math: replace "MathJax (default)" in marp-syntax.md with "declare `math: mathjax` or `math: katex`; the default depends on the build".
- GitHub Actions in export.md: replace the hardcoded `@v4` majors with an instruction to use each action's current major (checkout and upload-artifact are at v7 on 2026-11-13).
- The quoted error "No suitable browser found" is not in the README; keep it only as a symptom.

Credit: add the `## Credits` line above to `skills/marp-slide/README.md`.
