---
name: draw-io
description: Create and edit uncompressed .drawio diagrams and export PNG. Use when the user asks for a draw.io file, an architecture diagram, an AWS icon diagram, a Quarto or reveal.js slide figure, or a layout fix in mxGraph XML. Keywords include .drawio, mxCell, mxgraph.aws4, and diagram export.
---

# draw.io Diagram Skill

## 1. Basic Rules

- Edit only `.drawio` files
- Do not directly edit `.drawio.png` files
- Use auto-generated `.drawio.png` by pre-commit hook in slides

## 2. Font Settings

For diagrams used in Quarto slides,
specify `defaultFontFamily` in mxGraphModel tag:

```xml
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>
```

Also explicitly specify `fontFamily` in each text element's style attribute:

```xml
style="text;html=1;fontSize=27;fontFamily=Noto Sans JP;"
```

## 3. Conversion Commands

See conversion script at [scripts/convert-drawio-to-png.sh](scripts/convert-drawio-to-png.sh).

```sh
# Convert all .drawio files
mise exec -- pre-commit run --all-files

# Convert specific .drawio file
mise exec -- pre-commit run convert-drawio-to-png --files assets/my-diagram.drawio

# Run script directly (using skill's script)
bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram1.drawio
```

Export matches the page background the user chose. Pass `-t` only for a transparent page. Do not add `-t` for a light, dark, or custom plate.

```sh
# Transparent, only if the user asked for it
DRAWIO_BACKGROUND=transparent bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram1.drawio

# Light or dark plate: the script rewrites background on a temp copy, then exports without -t
DRAWIO_BACKGROUND=light bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram1.drawio
DRAWIO_BACKGROUND=dark bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram1.drawio

# File as stored, no -t
bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram1.drawio
```

| Option | Description |
|--------|-------------|
| `-x` | Export mode |
| `-f png` | PNG format output |
| `-s 2` | 2x scale (high resolution) |
| `-t` | Transparent background |
| `-o` | Output file path |

## 4. Layout Adjustment

### 4.1. Coordinate Adjustment Steps

1. Open `.drawio` file in text editor (plain XML format)
2. Find `mxCell` for element to adjust (search by `value` attribute for text)
3. Adjust coordinates in `mxGeometry` tag
   - `x`: Position from left
   - `y`: Position from top
   - `width`: Width
   - `height`: Height
4. Run conversion and verify

### 4.2. Coordinate Calculation

- Element center coordinate = `y + (height / 2)`
- To align multiple elements, calculate and match center coordinates

## 5. Design Principles

### 5.1. Basic Principles

- Clarity: Create simple, visually clean diagrams
- Consistency: Unify colors, fonts, icon sizes, line thickness
- Accuracy: Do not sacrifice accuracy for simplification

### 5.2. Element Rules

- Label all elements
- Use arrows to indicate direction
  Prefer two unidirectional arrows over one bidirectional arrow. A single double-headed arrow hides which call is which. `references/layout-guidelines.md` uses the same rule.
- Use latest official icons
- Add legend to explain custom symbols

### 5.3. Accessibility

- Ensure sufficient color contrast. Contrast is harmony of the whole diagram, not a fixed ink color. Text must separate from its component fill. The component must separate from its container. The container and the arrows must separate from the page. Black, gray, or white can all be correct.
- Use patterns in addition to colors

### 5.4. Progressive Disclosure

Separate complex systems into staged diagrams:

| Diagram Type | Purpose |
|--------------|---------|
| Context Diagram | System overview from external perspective |
| System Diagram | Main components and relationships |
| Component Diagram | Technical details and integration points |
| Deployment Diagram | Infrastructure configuration |
| Data Flow Diagram | Data flow and transformation |
| Sequence Diagram | Time-series interactions |

### 5.5. Metadata

Include title, description, last updated, author, and version in diagrams.

## 6. Best Practices

### 6.1. Background Color

Ask which page background the user wants: transparent, light, dark, or another color. `#ffffff` and `#1e1e1e` are suggestions, not a closed default. Do not strip `background` just to force transparency.

- Transparent: every stroke, icon, and fill must still read on both a light slide and a dark slide. If it will not, ask for the theme before export.
- Light plate: `background="#ffffff"` with dark ink on light fills.
- Dark plate: `background="#1e1e1e"` with light ink on dark fills.
- Other: use the user's color, then retune component fill, `fontColor`, and arrow `strokeColor` so the set stays harmonious.

`-t` on the PNG export keeps the page transparent. Use it only when the user asked for a transparent background.

### 6.2. Font Size

- Use 1.5x standard font size (around 18px) for PDF readability

### 6.3. Japanese Text Width

- Allow 30-40px per character
- Insufficient width causes unintended line breaks

```xml
<!-- For 10-character text, allow 300-400px -->
<mxGeometry x="140" y="60" width="400" height="40" />
```

### 6.4. Arrow Placement

Do not draw a straight line from A to B unless they share an axis and the span is empty. If they are not aligned, or a box sits between them, a straight line cuts the diagram.

Default style:

```xml
style="edgeStyle=orthogonalEdgeStyle;curved=1;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;"
```

Decide the target per arrow. This is not the Mermaid subgraph rule.

- The message is "this block talks to that block": end on the parent container.
- The message is "this call enters this service": end on that node.
- Leave and enter from the side that faces the other end (`exitX`/`exitY`, `entryX`/`entryY`). The elbow runs through the gutter between groups, not through a container.
- The edge `parent` is the common ancestor (usually the page, `1`), not a buried child.
- Do not put every arrow on the back layer. A back-layer arrow hides its label under a container. Route it in the gap. If it must cross, divert it. Do not bury it.

Keep the label in that gutter, more than 20px from the line and from any box or text. Never under a container. Position arrows so they do not overlap labels. Keep the arrow start and end at least 20px from a label edge.

Do not bury arrows behind boxes. This layering hides the label under the container:

```xml
<!-- Title -->
<mxCell id="title" value="..." .../>

<!-- Don't: arrows forced to the back layer -->
<mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;curved=1;..." edge="1"/>

<!-- Other elements (front layer) cover the arrow and its label -->
<mxCell id="box1" .../>
```

### 6.5. Arrow Connection to Text Labels

For text elements, exitX/exitY don't work, so use explicit coordinates:

```xml
<!-- Good: Explicit coordinates with sourcePoint/targetPoint -->
<mxCell id="arrow" style="..." edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="1279" y="500" as="sourcePoint"/>
    <mxPoint x="119" y="500" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="1279" y="560"/>
      <mxPoint x="119" y="560"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 6.6. edgeLabel Offset Adjustment

Adjust offset attribute to distance arrow labels from arrows:

```xml
<!-- Place above arrow (negative value to distance) -->
<mxPoint x="0" y="-40" as="offset"/>

<!-- Place below arrow (positive value to distance) -->
<mxPoint x="0" y="40" as="offset"/>
```

### 6.7. Remove Unnecessary Elements

- Remove decorative icons irrelevant to context
- Example: If ECR exists, separate Docker icon is unnecessary

### 6.8. Labels and Headings

- Service name only: 1 line
- Service name + supplementary info: 2 lines with line break
- Redundant notation (e.g., ECR Container Registry): shorten to 1 line
- Use `&lt;br&gt;` tag for line breaks

### 6.9. Containers Are Parents

A container is the `parent` of its components, not a rectangle drawn behind siblings. Children use coordinates relative to the container. The user can then drag the block and redistribute it.

- YOU MUST: At least 30px margin inside the parent, measured from the container origin
- YOU MUST: Account for rounded corners (`rounded=1`) and stroke width
- YOU MUST: The container stroke must read against the page background
- YOU MUST: Visually verify the PNG

Proportion is the slide canvas (16:9), not a GitHub column. One idea per diagram. Do not stretch horizontally so that text has to shrink.

Coordinate check, measured inside the parent:

```text
Container origin y=0, height=400 -> inner range is y=0-400
Internal element top: 30 or more
Internal element bottom: height - 30 or less (e.g., up to y=370)
```

Bad example (overflow: the label starts 10px inside a frame whose top is y=20, and it is not a child, so the block cannot be dragged together):

```xml
<mxCell id="bg" value="VPC" style="rounded=1;strokeWidth=3;" vertex="1" parent="1">
  <mxGeometry x="500" y="20" width="560" height="400" as="geometry"/>
</mxCell>
<mxCell id="label" value="Title" style="text;" vertex="1" parent="1">
  <mxGeometry x="510" y="30" width="540" height="35" as="geometry"/>
</mxCell>
```

Margin alone is not enough if the title is still a sibling on the page. This keeps the 30px inset but does not group:

```xml
<!-- Background frame -->
<mxCell id="bg" style="rounded=1;strokeWidth=3;..." vertex="1" parent="1">
  <mxGeometry x="500" y="20" width="560" height="430" as="geometry"/>
</mxCell>
<!-- y=50 is 30px from frame top (y=20), but parent is still the page -->
<mxCell id="label" value="Title" style="text;..." vertex="1" parent="1">
  <mxGeometry x="510" y="50" width="540" height="35" as="geometry"/>
</mxCell>
```

Good example (child of the container, 30px inside it, moves with the block):

```xml
<mxCell id="vpc" value="VPC" style="rounded=1;strokeWidth=3;fillColor=#E6F2F8;fontColor=#111111;strokeColor=#1565c0;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="560" height="400" as="geometry"/>
</mxCell>
<mxCell id="alb" value="ALB" style="rounded=1;fillColor=#ffffff;fontColor=#111111;" vertex="1" parent="vpc">
  <mxGeometry x="30" y="40" width="120" height="60" as="geometry"/>
</mxCell>
```

`fontColor=#111111` here is dark ink on a light fill, not the only legal text color. On a dark fill, use a light `fontColor`. For an AWS group, use `shape=mxgraph.aws4.group` and still parent the services to that cell.

## 7. Reference

Load only what the task needs.

- **MANDATORY** before placing groups or arrows: [references/layout-guidelines.md](references/layout-guidelines.md)
- **MANDATORY** for an AWS icon: run [scripts/find_aws_icon.py](scripts/find_aws_icon.py). **Do NOT load** [references/aws-icons.md](references/aws-icons.md) unless that script misses the service.
- **Do NOT load** `aws-icons.md` for a non-AWS diagram.

AWS icon search examples:

```sh
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py ec2
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py lambda
```

## 8. Checklist

- [ ] Page background matches the user's choice. Transparent is `page="0"` plus `-t`. Light or dark sets `background` and does not pass `-t`
- [ ] Arrows do not penetrate boxes or icons (verify in PNG)
- [ ] Text contrasts with its component fill; components, arrows, and containers contrast with the page
- [ ] Font size appropriate (larger recommended)
- [ ] Arrows are curved orthogonal unless A and B share an axis and the span is empty
- [ ] Each arrow ends on the container or the node, chosen per message
- [ ] Arrow labels sit in the gutter, 20px+ from the line and from any box or text
- [ ] Arrows not overlapping labels (verify in PNG)
- [ ] Arrow start/end at least 20px from label edges
- [ ] Arrows do not cut through containers (verify in PNG)
- [ ] Container children use `parent` of that container, coordinates relative to it
- [ ] Internal elements not overflowing the container (verify in PNG)
- [ ] 30px+ margin inside the container
- [ ] AWS service names are official names/correct abbreviations
- [ ] AWS icons are latest version (mxgraph.aws4.*)
- [ ] No unnecessary elements remaining
- [ ] Visually verified PNG conversion

## 9. Image Display in reveal.js Slides

Add `auto-stretch: false` to YAML header:

```yaml
---
title: "Your Presentation"
format:
  revealjs:
    auto-stretch: false
---
```

This ensures correct image display on mobile devices.
