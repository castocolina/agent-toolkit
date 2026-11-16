# draw-io: sources (analyst, 2026-11-15)

## Origin

- The skill is `skills/draw-io` of softaworks/agent-toolkit. It exists at the fork point `3027f20f` with README.md, SKILL.md, references/aws-icons.md, references/layout-guidelines.md and the two scripts. Upstream history for the path is one commit, `06825f04` "feat: add 23 curated skills with comprehensive documentation" by Leonardo Flores (@leonardocouy), 2026-01-18. Upstream `main` is still `3027f20f` (2026-03-05), and every file under `skills/draw-io` there has the same blob sha as at the fork point (SKILL.md `7df85f38`, README.md `bb2ffb68`, aws-icons.md `87c339c0`, layout-guidelines.md `fd5a7932`, convert-drawio-to-png.sh `0bdcc562`, find_aws_icon.py `8cb66235`). So upstream has nothing newer to adopt.
- No credit line for it exists today: `skills/draw-io/README.md` has none, `docs/audit/upstream-sources.json` has no `draw-io` row, and `docs/audit/upstream-sources.md` lists draw-io only as "incidental-link". Both are gaps: the skill's text is derived from the softaworks original.
- No other origin found. The Japanese-language aws-icons.md and the Quarto/Noto Sans JP guidance name no author. A web search was not needed: the distinctive phrases ("Arrow Layering", "Text Width Calculation") match the upstream files byte for byte at the fork point.

## Missing credit line (add to `skills/draw-io/README.md`, in a new Sources paragraph after References)

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/main/skills/draw-io) by @leonardocouy; this version is rewritten. Facts were checked on 2026-11-15 against the draw.io (JGraph) desktop CLI (`drawio --help`, 32.6.1) and the draw.io source and shape index ([Sidebar-AWS4.js](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/js/diagramly/sidebar/Sidebar-AWS4.js), [mxAWS4.js](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/shapes/mxAWS4.js), [drawio-mcp shape index and XML reference](https://github.com/jgraph/drawio-mcp)), the [Quarto reveal.js reference](https://quarto.org/docs/reference/formats/presentations/revealjs.html) (Quarto), [pre-commit](https://pre-commit.com/) (pre-commit) and Amazon Web Services documentation (Amazon Web Services).
```

`audit.py check --strict` fails with `missing_credit` unless each row's `credit` text appears verbatim in SKILL.md, README.md or `references/*.md`; the line above contains `softaworks/agent-toolkit`, `draw.io (JGraph)`, `Quarto`, `pre-commit` and `Amazon Web Services` exactly as the rows below spell them.

## Proposed registry rows (docs/audit/upstream-sources.json; add by hand)

```json
[
  {"skill": "draw-io", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/draw-io", "ref": "main", "credit": "softaworks/agent-toolkit"},
  {"skill": "draw-io", "kind": "github-path", "source": "jgraph/drawio:src/main/webapp/js/diagramly/sidebar/Sidebar-AWS4.js", "ref": "dev", "credit": "draw.io (JGraph)"},
  {"skill": "draw-io", "kind": "github-path", "source": "jgraph/drawio:src/main/webapp/shapes/mxAWS4.js", "ref": "dev", "credit": "draw.io (JGraph)"},
  {"skill": "draw-io", "kind": "github-path", "source": "jgraph/drawio-mcp:shape-search/search-index.json", "ref": "main", "credit": "draw.io (JGraph)"},
  {"skill": "draw-io", "kind": "github-path", "source": "jgraph/drawio-mcp:shared/xml-reference.md", "ref": "main", "credit": "draw.io (JGraph)"},
  {"skill": "draw-io", "kind": "github-path", "source": "jgraph/drawio-desktop:README.md", "ref": "dev", "credit": "draw.io (JGraph)"},
  {"skill": "draw-io", "kind": "unversioned", "source": "mxGraph API, mxGeometry (sourcePoint, targetPoint, points, offset): https://jgraph.github.io/mxgraph/docs/js-api/files/model/mxGeometry-js.html", "ref": null, "credit": "draw.io (JGraph)"},
  {"skill": "draw-io", "kind": "unversioned", "source": "Quarto, Reveal.js options reference (auto-stretch): https://quarto.org/docs/reference/formats/presentations/revealjs.html", "ref": null, "credit": "Quarto"},
  {"skill": "draw-io", "kind": "unversioned", "source": "pre-commit documentation and changelog (repo: local hooks, language: unsupported, 4.4.0): https://pre-commit.com/", "ref": null, "credit": "pre-commit"},
  {"skill": "draw-io", "kind": "unversioned", "source": "AWS Docs, Amazon Q Developer rename (CodeWhisperer became part of Amazon Q Developer): https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/service-rename.html", "ref": null, "credit": "Amazon Web Services"},
  {"skill": "draw-io", "kind": "unversioned", "source": "AWS Prescriptive Guidance, Modern data-centric use cases (Amazon QLDB end of support 2025-07-31): https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/modern-data-centric-use-cases/modern-data-centric-use-cases.pdf", "ref": null, "credit": "Amazon Web Services"},
  {"skill": "draw-io", "kind": "unversioned", "source": "AWS Architecture Icons (official icon and service names): https://aws.amazon.com/architecture/icons/", "ref": null, "credit": "Amazon Web Services"}
]
```

Notes on the rows:

- The `Sidebar-AWS4.js`, `mxAWS4.js`, `search-index.json` and `xml-reference.md` rows are `github-path`, not `unversioned`, because they are repository files: `upstreams` can then report `stale` when the AWS palette or the shape index changes, which is exactly what makes the catalog names go bad. The Sidebar file's last change was 2026-09-08 (`f3abfe0f`) and the shape index's 2026-11-11 (`cfc1b916`).
- The registry row `upstream-sources.md` classifies draw-io as "incidental-link"; it should be re-labelled once the first row lands (the softaworks row is an origin).
- The CLI help itself (`drawio --help` 32.6.1) is tool output, not a URL; the `jgraph/drawio-desktop:README.md` row stands for the vendor's CLI/update documentation. The desktop README does not list the export flags, so the `--help` output remains the flag source (read it live).
- The vendor skill at `jgraph/drawio-mcp:plugins/claude-code/skills/drawio/SKILL.md` (last changed 2026-10-26, `63549788`) is a peer skill, not an origin of this one. It was read for adopt/adapt ideas below; add a row only if the coordinator wants its churn tracked: `{"skill": "draw-io", "kind": "github-path", "source": "jgraph/drawio-mcp:plugins/claude-code/skills/drawio/SKILL.md", "ref": "main", "credit": "draw.io (JGraph)"}`.

## skill-updater review (REVIEW ONLY; no `track` call, no `upstreams` run)

Procedure used: `skills/skill-updater/SKILL.md` steps 2 to 6 by reasoning only. There is no `draw-io` registry row yet, so step 2 gives "no row, propose the row" (above) and no `track` call; the `upstreams` command would report nothing for this skill.

| item | decision | one-line reason |
| --- | --- | --- |
| softaworks upstream `skills/draw-io` | ignore | upstream `main` equals the fork point; every file's blob sha is unchanged, so there is nothing newer to port. |
| vendor skill: "never guess `mxgraph.*` names; look them up" (find-shapes.js over the shape index) | adapt | The catalog has 92 of 470 names in neither the palette nor the shape index (facts.md, aws-icon-name-check.md); fix the known-wrong rows (groups, subnets, `group_vpc2`, retired services) and add a warning plus a pointer to the live shape index or draw.io's shape search, keeping `find_aws_icon.py` as the offline lookup. |
| vendor reference: edge labels `labelBackgroundColor=default;defaultLabelBackgroundColor=page` | adapt | Offer it beside the existing `labelBackgroundColor=none`; the skill's "opaque white by default" claim was not reproduced (no export run). |
| vendor reference: `background=...` with `adaptiveColors="none"` for dark pages, and the CLI's `--theme dark\|light\|auto` | adapt (needs one real export to confirm before it is written as fact) | The skill's dark plate (`#1e1e1e`, `DRAWIO_BACKGROUND=dark`) says nothing about draw.io's dark-mode color adaptation; an author must confirm in a PNG whether colors survive, then add one line. |
| CLI `--normalize` (files each edge at the nearest common ancestor, grows a container that would clip children) and `--layout libavoid` (routes edges around shapes without moving vertices) | adapt, optional | Both automate rules the skill states by hand (edge `parent`, 30px margins, no arrow through a box); mention as optional, "if `drawio --help` lists them", never as a requirement (older builds lack them). |
| pre-commit `language: unsupported` (4.4.0+) | adapt | Keep `language: system` for older pre-commit and name the new spelling. |
| vendor skill: Mermaid conversion, ELK flow presets, URL output, WSL paths, color themes, MCP servers, `--disable-gpu` | ignore | Different scope (diagram generation from Mermaid or MCP); `--disable-gpu` is not in the 32.6.1 help. |
| Model-validity pass | not run | The pass needs the probe lane (`pi-cmd runner`), and this analyst may not use an LLM lane. Candidate habit-countering rules for the coordinator to probe: "NEVER pass -t unless asked", "NEVER rely on defaultFontFamily", "no decorative duplicates (ECR vs Docker icon)", "two one-way arrows instead of a double-headed one". |
