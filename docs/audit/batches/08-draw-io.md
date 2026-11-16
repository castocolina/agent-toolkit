# Batch 08

## draw-io (skill)

### draw-io#D8-1
- severity: high
- dimension: D8
- location: skills/draw-io/scripts/convert-drawio-to-png.sh:59
- fix: Make staging an explicit opt-in or place it in a separate pre-commit wrapper. Standalone conversion should succeed without Git and leave the index unchanged.

### draw-io#D8-2
- severity: high
- dimension: D8
- location: skills/draw-io/scripts/convert-drawio-to-png.sh:39
- fix: Export to a temporary PNG, validate it, and atomically replace the destination only after success. On failure, remove only temporary artifacts and preserve the previous PNG.

### draw-io#D7-1
- severity: medium
- dimension: D7
- location: skills/draw-io/evals/evals.json:7
- fix: Require an actual parseable .drawio document and assertions for its root cells, requested nodes, edges, and background rather than accepting a plan.

### draw-io#D7-2
- severity: medium
- dimension: D7
- location: skills/draw-io/scripts/find_aws_icon.py:61
- fix: Implement --help for both scripts and machine-readable result modes, with diagnostics on stderr. Extend the existing tests to verify those interfaces and background-selection branches.

### draw-io#D7-1
- severity: low
- dimension: D7
- location: skills/draw-io/scripts/find_aws_icon.py:57
- fix: Handle -h/--help explicitly (print usage, exit 0); a '--help' query currently falls through to 'No icons found'. Add the same to convert-drawio-to-png.sh

### draw-io#D8-1
- severity: medium
- dimension: D8
- location: skills/draw-io/SKILL.md:35
- fix: State prerequisites (mise, the repo's convert-drawio-to-png pre-commit hook) and give the direct script invocation as the fallback when they are absent

### draw-io#D8-2
- severity: low
- dimension: D8
- location: skills/draw-io/SKILL.md:41
- fix: Use the spec's relative convention 'bash scripts/convert-drawio-to-png.sh' so commands work outside the Claude Code skills layout

### draw-io#D4-1
- severity: medium
- dimension: D4
- location: skills/draw-io/SKILL.md:3
- fix: Create and edit uncompressed .drawio/mxGraph XML diagrams and export editable PNGs. Use for draw.io files, AWS architecture diagrams with mxgraph.aws4 icons, connector or container layout fixes, and diagram figures for Quarto/reveal.js, including requests for an editable architecture diagram without naming draw.io. Not for Mermaid, Excalidraw, Graphviz, general slide styling, or OCR.

### draw-io#D1-1
- severity: medium
- dimension: D1
- location: skills/draw-io/SKILL.md:84
- fix: Delete elementary coordinate explanations and generic clarity/consistency advice. Retain mxGraph-specific containment, connector routing, font propagation, and export constraints.

### draw-io#D2-1
- severity: medium
- dimension: D2
- location: skills/draw-io/SKILL.md:73
- fix: Add a short creation sequence: establish topology and output constraints, initialize the document, create parent containers before children, connect and route edges, export, inspect, and repeat corrections until the checklist passes.

### draw-io#D5-1
- severity: medium
- dimension: D5
- location: skills/draw-io/SKILL.md:41
- fix: Use skill-root-relative script references and resolve the installed skill directory at runtime. Preserve the target project's working directory or pass absolute diagram paths.

### draw-io#D6-1
- severity: medium
- dimension: D6
- location: skills/draw-io/SKILL.md:236
- fix: Apply 16:9 proportions and slide-specific sizing only to slide figures. Otherwise preserve the user's intended medium, canvas, and aspect ratio.

### draw-io#D1-1
- severity: medium
- dimension: D1
- location: skills/draw-io/SKILL.md:114
- fix: Replace the 5.4 diagram-type taxonomy table (model-known) with expert guidance on when to split one system into staged diagrams and the staging order to use

### draw-io#D1-2
- severity: low
- dimension: D1
- location: skills/draw-io/SKILL.md:84
- fix: Delete the center-coordinate arithmetic; keep only the rule to match centers when aligning elements

### draw-io#D2-1
- severity: low
- dimension: D2
- location: skills/draw-io/SKILL.md:72
- fix: Compress 4.1 to a diagnostic principle (find the misaligned pair by value, fix geometry as a child of its container, re-export and verify) and drop the editor mechanics

### draw-io#D3-1
- severity: low
- dimension: D3
- location: skills/draw-io/SKILL.md:152
- fix: Consolidate the NEVER items scattered across sections 2-6.9 (back-layer arrows, -t misuse, sibling labels) into one Gotchas list with reasons

### draw-io#D4-1
- severity: low
- dimension: D4
- location: skills/draw-io/SKILL.md:3
- fix: Append a boundary to the description: 'Not for Mermaid, Excalidraw, Graphviz/DOT, or generic image editing.'
