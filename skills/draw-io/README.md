# draw-io Diagram Skill

An agent skill for creating and editing draw.io diagrams as plain mxGraph XML and exporting them to PNGs that stay editable (the diagram is embedded in the PNG). It covers architecture and AWS diagrams, container and connector layout fixes, and figures for Quarto or reveal.js slides.

The authoring rules, decision tables and gotchas live in [SKILL.md](SKILL.md); this file only covers setup.

## Requirements

- The `drawio` CLI (draw.io desktop) on `PATH`, for PNG export
- Python 3, for PNG validation in the export script and the AWS icon lookup
- `timeout(1)` from GNU coreutils, to bound each export (macOS: `brew install coreutils` provides `gtimeout`, which the script also finds); `DRAWIO_TIMEOUT=0` skips it
- Optional: `pre-commit`, to regenerate PNGs on every commit

## Installation

**Claude Code:**

```bash
cp -r skills/draw-io ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/convert-drawio-to-png.sh [--stage] FILE.drawio...` | Export `FILE.drawio.png` next to each input (2x, diagram embedded). Background via `DRAWIO_BACKGROUND=file\|transparent\|light\|dark\|#rrggbb`. JSON result on stdout. A failed export keeps the previous PNG. `--stage` runs `git add`, for pre-commit hooks only. |
| `scripts/find_aws_icon.py [--json] QUERY` | Print the `mxgraph.aws4.*` style for matching AWS services from `references/aws-icons.md`. |

Both accept `--help`. Their tests are in `tests/skills/draw-io/` in this repository.

## File Structure

```
draw-io/
├── SKILL.md                      # Agent instructions
├── README.md                     # This file
├── scripts/
│   ├── convert-drawio-to-png.sh  # PNG export
│   └── find_aws_icon.py          # AWS icon lookup
├── references/
│   ├── layout-guidelines.md      # AWS group nesting, line meaning, placement
│   └── aws-icons.md              # AWS icon catalog
└── evals/                        # Output evals, trigger queries, fixtures
```

## References

- [draw.io documentation](https://www.drawio.com/doc/)

## Sources

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/main/skills/draw-io) by @leonardocouy; this version is rewritten. Facts were checked on 2026-11-15 against the draw.io (JGraph) desktop CLI (`drawio --help`, 32.6.1) and the draw.io source and shape index ([Sidebar-AWS4.js](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/js/diagramly/sidebar/Sidebar-AWS4.js), [mxAWS4.js](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/shapes/mxAWS4.js), [drawio-mcp shape index and XML reference](https://github.com/jgraph/drawio-mcp)), the [Quarto reveal.js reference](https://quarto.org/docs/reference/formats/presentations/revealjs.html) (Quarto), [pre-commit](https://pre-commit.com/) (pre-commit) and Amazon Web Services documentation (Amazon Web Services).
