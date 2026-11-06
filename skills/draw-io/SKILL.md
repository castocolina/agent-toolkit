---
name: draw-io
description: Create and edit uncompressed draw.io (.drawio, mxGraph XML) diagrams and export them to editable PNGs. Use for draw.io files, architecture or AWS diagrams with mxgraph.aws4 icons, container and connector layout fixes, and diagram figures for Quarto or reveal.js slides, including requests for an editable architecture diagram that do not name draw.io. Keywords include .drawio, .drawio.png, mxCell, mxGeometry, mxgraph.aws4. Not for Mermaid, Excalidraw, Graphviz/DOT, PlantUML, general slide styling, OCR, or generic image editing.
---

# draw.io Diagrams

The `.drawio` file is the source. `NAME.drawio.png` is generated from it with the diagram embedded (`drawio -e`), so the PNG reopens in draw.io. Edit the XML as text, export, look at the PNG, fix, repeat.

The scripts are in this skill's `scripts/` directory: `S=${CLAUDE_SKILL_DIR}/scripts` in Claude Code; elsewhere `S` is the `scripts/` folder next to this SKILL.md (for example `~/.claude/skills/draw-io/scripts`). Run them from the user's project and pass diagram paths relative to it, or absolute. Each PNG is written next to its `.drawio`.

## Workflow

1. **Settle the brief.**
   - New diagram: before writing XML, ask (or infer and state): Which medium: slide, document/README/PR, or a file to keep editing? Which page background? Which font, and is it installed where `drawio` runs (Fonts and text)? If the answer to "can a reader say the point in one sentence?" is no, split the diagram (Staging).
   - Edit of an existing diagram: keep its cell ids, styles, canvas and background; ask only about the change requested.
2. **Open the input.** If `<diagram>` holds base64 text instead of an `<mxGraphModel>` (often `compressed="true"`), decode it to a temp file, check that it parses and has an `<mxGraphModel>`, and only then move it over the original (same name, so the PNG name stays `in.drawio.png`):

   ```sh
   timeout 120 drawio --disable-update -x -f xml -u -o in.tmp.drawio in.drawio \
     && python3 -c 'import sys,xml.etree.ElementTree as E; sys.exit(E.parse(sys.argv[1]).find(".//mxGraphModel") is None)' in.tmp.drawio \
     && mv in.tmp.drawio in.drawio
   ```

   If that chain fails, delete `in.tmp.drawio`, leave `in.drawio` as it was, and tell the user the file could not be decoded.
3. **Write the skeleton**, then **containers before children**, then **edges last** (sections below).
4. **Export** with `convert-drawio-to-png.sh`.
5. **Look at the PNG** (open it as an image), walk the Checklist, fix the XML, re-export. Stop only when every item passes.

## Skeleton

```xml
<mxfile>
  <diagram id="p1" name="Page-1">
    <mxGraphModel background="#ffffff">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- vertices: containers first, then their children; edges after the vertices -->
        <mxCell id="api" value="API" style="rounded=1;html=1;fontFamily=Noto Sans JP;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="db" value="Postgres" style="shape=cylinder3;html=1;fontFamily=Noto Sans JP;" vertex="1" parent="1">
          <mxGeometry x="280" y="40" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="e1" value="SQL" style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=1;fontFamily=Noto Sans JP;" edge="1" parent="1" source="api" target="db">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Cells `0` and `1` are required: `1` is the default layer and the parent of every top-level cell. Write it uncompressed so it diffs and edits as text.

## Decisions

### Page background and export

Default: keep the background stored in the file; a new diagram gets a light plate. Ask only when a slide's theme is unknown and the user wants transparency.

| User wants | XML | Export |
|------------|-----|--------|
| Light plate | `background="#ffffff"`, dark ink on light fills | as stored, or `DRAWIO_BACKGROUND=light` |
| Dark plate | `background="#1e1e1e"`, light `fontColor`, `labelBackgroundColor=none` on edges | `DRAWIO_BACKGROUND=dark` |
| Another color | `background="#rrggbb"`, retune fills, `fontColor`, arrow `strokeColor` | `DRAWIO_BACKGROUND=#rrggbb` |
| Transparent (only on request) | strokes, icons and text must read on light and dark slides; if they cannot, ask for the theme | `DRAWIO_BACKGROUND=transparent` (passes `-t`) |

Contrast is the whole set, not one ink color: text against its fill, the component against its container, containers and arrows against the page.

### Medium and canvas

| Medium | Proportion | Text size |
|--------|------------|-----------|
| Slide (Quarto, reveal.js) | fit 16:9; do not stretch wide and shrink the text; in Quarto set `auto-stretch: false` under `format: revealjs:` so the image keeps its size on mobile | about 18px (1.5x the usual) |
| Document, README, PR body | the diagram's natural shape; no forced 16:9 | draw.io default (12px) reads well at the 2x export |
| Existing diagram | keep the user's canvas and aspect ratio | keep |

### Arrows

| Situation | Do |
|-----------|----|
| Ends share an axis and nothing sits between them | straight line |
| Otherwise | `edgeStyle=orthogonalEdgeStyle;curved=1;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;` |
| The message is "this block talks to that block" | end on the parent container |
| The message is "this call enters that service" | end on that node |
| Calls go both ways | two one-way arrows, not one double-headed arrow |
| Several flow types (ingestion, query, control) | line styles from `references/layout-guidelines.md` |

Leave and enter on the sides that face each other (`exitX`/`exitY`, `entryX`/`entryY`, 0-1 across the shape) so the elbow runs in the gutter between groups, never through a container.

### Staging a large system

Split when one picture would pass about 12 nodes, serve two audiences, or need arrows crossing containers more than twice. Order: context first (the system as one box plus users and external systems), then one diagram per box you zoom into, then deployment (network, accounts, regions) only if asked. Keep a shared box's name, color and relative position the same across stages so the reader can track it.

## Containers are parents

A container is the `parent` of its components, not a rectangle drawn behind siblings. Child coordinates are relative to the container origin: `child x = page x - container x`, `child y = page y - container y`. Dragging the container then moves its contents.

Worked example: an `ECS service` at page `(240,190)` inside `subnet` at page `(200,100)` becomes `parent="subnet"` with `x="40" y="90"`.

```xml
<mxCell id="subnet" value="Private subnet" style="rounded=1;html=1;verticalAlign=top;fillColor=#E6F2F8;strokeColor=#1565c0;fontColor=#111111;" vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="400" height="260" as="geometry"/>
</mxCell>
<mxCell id="ecs" value="ECS service" style="rounded=1;html=1;fillColor=#ffffff;fontColor=#111111;" vertex="1" parent="subnet">
  <mxGeometry x="40" y="90" width="120" height="60" as="geometry"/>
</mxCell>
```

- Keep at least 30px between every child and the container edge, measured inside the parent (`30 <= y` and `y + height <= container height - 30`), more with `rounded=1` or a thick stroke.
- `verticalAlign=top` puts the container title at the top; start children below it.
- AWS groups: `shape=mxgraph.aws4.group` with a `grIcon`, and the services still use that cell as `parent`.

## Edges and labels

- Document order is paint order. Write each edge after the vertices it connects; an edge written before a filled container is painted under it, line and label.
- Set the edge `parent` to the lowest common ancestor of its ends: the page (`1`) when they sit in different containers. Waypoints (`<Array as="points">`) use that parent's coordinates.
- Move a label off its line with `<mxPoint x="0" y="-20" as="offset"/>` inside the edge geometry (negative y is above a horizontal edge). Keep labels in the gutter, 20px or more from lines, boxes and other text.
- Edge labels have an opaque white label background by default. On a colored container or a dark page add `labelBackgroundColor=none` (or the page color).
- A `text;` cell does not take `exitX`/`exitY`. Connect to it with explicit points:

```xml
<mxCell id="arrow" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="1279" y="500" as="sourcePoint"/>
    <mxPoint x="119" y="500" as="targetPoint"/>
    <Array as="points"><mxPoint x="1279" y="560"/><mxPoint x="119" y="560"/></Array>
  </mxGeometry>
</mxCell>
```

- Line breaks in an `html=1` label are `&lt;br&gt;` in `value`. One line for a service name, two for name plus detail; shorten redundant names (`ECR Container Registry` to `Amazon ECR`).

## Fonts and text

- Put `fontFamily=...` in the style of every cell that shows text, containers and edges included. The CLI export ignores `defaultFontFamily` on `<mxGraphModel>` (same PNG with and without it, and draw.io drops it on re-save).
- The font must be installed where `drawio` runs. A missing font does not fail the export; it silently renders a fallback. For Japanese text on Quarto slides use `Noto Sans JP`.
- Before exporting with a named or CJK font, check it: `fc-list | grep -i "Noto Sans JP"`. No match: tell the user the PNG would use a fallback font, then either have them install the font or switch `fontFamily` to an installed one (`fc-list :lang=ja family` lists Japanese-capable families, for example `Noto Sans CJK JP`), re-export, and check the glyphs in the PNG.
- CJK labels need about 30-40px of width per character at `fontSize=27`; a narrower cell wraps the label.

## Export

```sh
bash "$S/convert-drawio-to-png.sh" docs/arch.drawio                               # background as stored
DRAWIO_BACKGROUND=dark bash "$S/convert-drawio-to-png.sh" docs/arch.drawio        # dark plate, no -t
DRAWIO_BACKGROUND=transparent bash "$S/convert-drawio-to-png.sh" slides/fig.drawio  # only when asked
```

- Needs the `drawio` CLI (draw.io desktop) on `PATH`. Output: 2x PNG with the diagram embedded, written to a temp file and moved over `NAME.drawio.png` only after it parses as a complete PNG whose embedded draw.io XML decodes. A failed, truncated, data-less or timed-out export keeps the previous PNG and the run goes on to the next file.
- `DRAWIO_TIMEOUT` (seconds, default 120) bounds each `drawio` call through `timeout(1)` (or `gtimeout` from Homebrew coreutils); raise it for a very large diagram. Without `timeout(1)` the script stops before running drawio and names the fix (GNU coreutils); `DRAWIO_TIMEOUT=0` runs unbounded.
- stdout is JSON, `[{"drawio":"docs/arch.drawio","png":"docs/arch.drawio.png","ok":true}]`; status goes to stderr. Exit 0 all exported, 1 any failure (including a missing `drawio`), 2 usage error. `--help` prints usage.
- `light`, `dark` and `#rrggbb` set `background` on every page of a parsed temp copy; the `.drawio` itself is untouched. A compressed page fails with "decode it first" (step 2).
- No `drawio` available: hand over the `.drawio` and say the PNG still needs exporting. Never fake a PNG.
- `Error: Export failed: NAME` from drawio means the XML does not parse; check it with `python3 -c 'import sys,xml.dom.minidom as m; m.parse(sys.argv[1])' NAME.drawio`.
- Running `drawio` by hand: add `--disable-update` and a `timeout`; the AppImage build can hang an export while it auto-updates (the script already passes it).
- A `drawio` call that hangs (even `drawio --version`) has one of three causes: (1) an instance left hung by an earlier run (e.g. a timed-out test) takes over every new call, so list it with `pgrep -af '[d]rawio'` (the bracket keeps the pattern from matching its own shell), kill only PIDs your own run started (`kill -9` if SIGTERM is ignored) and retry; `drawio --disable-update --version` then returns in about a second; (2) an auto-update, when the binary's mtime just changed (`ls -la --time-style=full-iso "$(command -v drawio)"`): wait for it to finish; (3) on a Linux Wayland session Electron can stall right after its Wayland setup with no output, so retry under XWayland with `env -u WAYLAND_DISPLAY drawio ...` (returns in about a second when this is the cause).

Regenerate PNGs on commit with a pre-commit hook. Copy the script into the repository (a hook needs a stable path) and pass `--stage`, which runs one `git add` for all generated PNGs:

```yaml
repos:
  - repo: local
    hooks:
      - id: convert-drawio-to-png
        name: convert draw.io to PNG
        entry: bash scripts/convert-drawio-to-png.sh --stage
        language: system
        files: \.drawio$
```

Run one file with `pre-commit run convert-drawio-to-png --files assets/arch.drawio` (prefix `mise exec --` when the project pins pre-commit with mise).

## AWS icons

Run `python3 "$S/find_aws_icon.py" <service>` and copy its `Style:` line (`--json` gives `[{name, icon, kind, style}]`; exit 1 means no match). Several rows can match: pick the service icon (`Amazon DynamoDB`), not a sub-resource (`DynamoDB Table`), unless the diagram is about that resource. Use the official name with its prefix (`Amazon S3`, `AWS Lambda`) and only `mxgraph.aws4.*` icons.

## Load only when needed

- `references/layout-guidelines.md`: read when drawing an AWS architecture (group nesting order) or a diagram with several flow types (line-style meaning, placement direction). Not needed for a single fix.
- `references/aws-icons.md`: read only when `find_aws_icon.py` finds nothing, to browse a category or the product-icon style. Do NOT load it for a non-AWS diagram, or to look up a service the script finds.

## Gotchas

- NEVER edit `NAME.drawio.png`: the next export regenerates it from the `.drawio` and your edit is gone.
- NEVER pass `-t` (`DRAWIO_BACKGROUND=transparent`) unless the user asked: `-t` overrides the stored background, so dark ink meant for a white plate lands on a dark slide.
- NEVER strip `background` to get transparency: without `-t` the export is an opaque white page anyway.
- NEVER draw a frame as a sibling rectangle behind its nodes: dragging moves only the frame and the block cannot be redistributed.
- NEVER put edges on the back layer (first in the file): the container painted after them covers the line and its label.
- NEVER rely on `defaultFontFamily`: the export ignores it, so the slide gets the fallback font.
- NEVER hand-edit compressed `<diagram>` content: it is deflated, URL-encoded base64; decode with `-u` first.
- NEVER run the script with `--stage` outside a pre-commit hook: it adds the PNGs to the user's index and they slip into the next commit.

## Checklist (on the PNG)

- [ ] Page background is the user's choice; `-t` only for transparent
- [ ] No arrow crosses a box, icon or container it does not connect
- [ ] No label is hidden, overlaps an arrow, or sits under a container; labels 20px+ from lines and boxes
- [ ] Every child sits inside its container with a 30px margin and has that container as `parent`
- [ ] Text contrasts with its fill; shapes, containers and arrows contrast with the page
- [ ] Every text-bearing cell has `fontFamily`; text is large enough for the medium
- [ ] AWS: official names, `mxgraph.aws4.*` icons, no decorative duplicates (an ECR icon makes a Docker icon redundant)
