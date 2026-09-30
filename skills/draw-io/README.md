# draw-io Diagram Skill

A Claude Code skill for creating, editing, and managing draw.io diagrams with professional quality standards.

## Purpose

This skill enables AI-assisted creation and maintenance of draw.io architecture diagrams, flowcharts, and technical documentation visuals. It ensures consistent styling, proper layout, and automated PNG conversion for presentations and documentation.

## When to Use This Skill

Use this skill when you need to:

- Create or edit `.drawio` XML diagram files
- Convert diagrams to PNG. Transparent only if the user asks; otherwise keep the page background they chose.
- Adjust element positions and layouts programmatically
- Ensure consistent font families (especially for Quarto slides)
- Work with AWS architecture diagrams using official icons
- Maintain professional diagram quality with accessibility standards
- Debug layout issues or element overlaps

## How It Works

The skill provides:

1. **Direct XML Editing**: Manipulates `.drawio` files as structured XML
2. **Automated Conversion**: Converts diagrams to high-resolution PNG via pre-commit hooks or scripts
3. **Layout Calculations**: Computes proper spacing, alignment, and margins
4. **Icon Integration**: Searches and integrates official AWS icons
5. **Quality Assurance**: Applies design principles and accessibility guidelines

## Key Features

### 1. Font Management

Ensures consistent typography across diagrams:

- Sets `defaultFontFamily` in mxGraphModel
- Applies `fontFamily` to individual text elements
- Recommended: "Noto Sans JP" for Japanese text support

### 2. PNG Conversion

Multiple conversion methods:

```bash
# Via pre-commit hook (all files)
mise exec -- pre-commit run --all-files

# Specific file via pre-commit
mise exec -- pre-commit run convert-drawio-to-png --files assets/my-diagram.drawio

# Direct script execution
bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram.drawio
```

Conversion produces:
- 2x scale (high resolution)
- Transparent background
- PNG format suitable for presentations

### 3. Layout Adjustment

Programmatic element positioning:

- Calculate element centers: `y + (height / 2)`
- Align multiple elements by matching center coordinates
- Maintain minimum 30px margins from container boundaries
- Position arrows to avoid label overlaps (20px+ clearance)

### 4. AWS Icon Integration

Search and integrate official AWS service icons:

```bash
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py ec2
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py lambda
```

Uses latest `mxgraph.aws4.*` icon set.

### 5. Design Principles

Enforces professional standards:

- **Clarity**: Simple, visually clean diagrams
- **Consistency**: Unified colors, fonts, icon sizes, line thickness
- **Accuracy**: Precise technical representation
- **Accessibility**: Sufficient color contrast, pattern usage
- **Progressive Disclosure**: Staged diagrams for complex systems

### 6. Quality Checklist

Automated validation ensures:

- Page background matches the user's choice (transparent, light, dark, or other)
- Appropriate font sizes (1.5x standard for readability)
- Curved orthogonal arrows unless the span is empty and aligned
- 30px+ margins from container boundaries
- Official AWS service names and latest icons
- Visual verification of PNG output

## Usage Examples

### Example 1: Create AWS Architecture Diagram

```xml
<!-- Set font family -->
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>

  <!-- Container is the parent. Child coordinates are relative to it. -->
  <mxCell id="vpc" value="VPC" style="rounded=1;strokeWidth=3;fillColor=#E6F2F8;fontColor=#111111;strokeColor=#1565c0;" vertex="1" parent="1">
    <mxGeometry x="40" y="40" width="560" height="430" as="geometry"/>
  </mxCell>

  <mxCell id="title" value="VPC" style="text;fontSize=18;fontFamily=Noto Sans JP;fontColor=#111111;" vertex="1" parent="vpc">
    <mxGeometry x="30" y="30" width="500" height="35" as="geometry"/>
  </mxCell>

  <!-- Arrow with explicit coordinates -->
  <mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;curved=1;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;" edge="1" parent="1">
    <mxGeometry relative="1" as="geometry">
      <mxPoint x="100" y="200" as="sourcePoint"/>
      <mxPoint x="500" y="200" as="targetPoint"/>
    </mxGeometry>
  </mxCell>

  <!-- Arrow label with offset -->
  <mxCell id="label1" value="API Request" style="edgeLabel;fontSize=14;fontFamily=Noto Sans JP;">
    <mxGeometry relative="1" as="geometry">
      <mxPoint x="0" y="-20" as="offset"/>
    </mxGeometry>
  </mxCell>
</mxGraphModel>
```

### Example 2: Convert Diagram to PNG

```bash
# Edit the diagram
vim architecture.drawio

# Convert to PNG (via pre-commit hook)
mise exec -- pre-commit run convert-drawio-to-png --files architecture.drawio

# Result: architecture.drawio.png (2x resolution, transparent)
```

### Example 3: Find AWS Icon

```bash
# Search for EC2 icon
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py ec2

# Output: mxgraph.aws4.compute.ec2_instance
```

### Example 4: Progressive Disclosure Diagram Set

For complex systems, create staged diagrams:

1. **Context Diagram**: External perspective (users, external systems)
2. **System Diagram**: Main components (services, databases)
3. **Component Diagram**: Technical details (APIs, queues, caches)
4. **Deployment Diagram**: Infrastructure (VPCs, regions, availability zones)
5. **Data Flow Diagram**: Data transformations and flows
6. **Sequence Diagram**: Time-series interactions

## Best Practices

### Text Width Calculation

Japanese text requires 30-40px per character:

```xml
<!-- For 10-character text: 300-400px width -->
<mxGeometry x="140" y="60" width="400" height="40" />
```

### Arrow Layering

Do not force arrows to the back layer. This XML is the pattern that hides the label under the box:

```xml
<mxCell id="title" value="..." .../>
<mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;curved=1;..." .../> <!-- Don't: back layer -->
<mxCell id="box1" .../> <!-- Front layer covers the arrow and its label -->
```

### Container Margins

Measure the 30px margin inside the parent, not on the page:

```text
Container origin y=0, height=400
Element top: y ≥ 30
Element bottom: y ≤ 370
```

The old page math (frame y=20, element y≥50) is the sibling pattern. It insets correctly and still does not group.

### Page Background

Do not force a transparent page. Ask: transparent, light, dark, or another color. `#ffffff` and `#1e1e1e` are suggestions. Contrast is harmony of text, component, container, arrow, and page — not a fixed ink color.

Transparent is still a valid choice when the user asks for it:

```xml
<!-- One option, not the only option -->
<mxGraphModel page="0" ...>

<!-- Also valid when the user wants a light or dark plate -->
<mxGraphModel background="#ffffff" ...>
<mxGraphModel background="#1e1e1e" ...>
```

## File Structure

```
~/.claude/skills/draw-io/
├── SKILL.md                          # This documentation
├── README.md                         # User-facing guide
├── scripts/
│   ├── convert-drawio-to-png.sh     # PNG conversion script
│   └── find_aws_icon.py             # AWS icon search utility
└── references/
    ├── layout-guidelines.md         # Detailed layout rules
    └── aws-icons.md                 # AWS icon catalog
```

## Integration with Presentations

For reveal.js slides (Quarto), add to YAML header:

```yaml
---
title: "Your Presentation"
format:
  revealjs:
    auto-stretch: false
---
```

This ensures correct image sizing on mobile devices.

## Quality Assurance Checklist

Before finalizing any diagram:

- [ ] Page background matches the user's choice
- [ ] Font size appropriate (18px+ for readability)
- [ ] Arrows are curved orthogonal unless A and B share an axis and the span is empty
- [ ] Arrows not overlapping labels (verified in PNG)
- [ ] Arrow endpoints 20px+ from labels
- [ ] Internal elements not overflowing the container
- [ ] Arrows not penetrating boxes/icons
- [ ] Internal elements have 30px+ margins from frames
- [ ] AWS service names are official/correct
- [ ] AWS icons use latest version (`mxgraph.aws4.*`)
- [ ] No unnecessary decorative elements
- [ ] PNG conversion visually verified

## References

- [Layout Guidelines](references/layout-guidelines.md) - Detailed spacing and alignment rules
- [AWS Icons](references/aws-icons.md) - Complete AWS icon catalog
- [draw.io Documentation](https://www.drawio.com/doc/) - Official draw.io reference

## Skill Metadata

- **Name**: draw-io
- **Type**: Diagram creation and editing
- **Input**: `.drawio` XML files
- **Output**: `.drawio.png` high-resolution images
- **Dependencies**: drawio CLI, Python 3.x, pre-commit hooks
