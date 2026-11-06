# Batch 38

## excalidraw (skill)

### excalidraw#D8-1
- severity: high
- dimension: D8
- location: skills/excalidraw/SKILL.md:57
- fix: Keep the label-level diff for reporting, but add a preservation validator that compares complete elements by ID and top-level scene data against an explicit allowlist of permitted changes. Require that validator to pass before replacement, returning only a structured summary rather than scene JSON.

### excalidraw#D8-2
- severity: medium
- dimension: D8
- location: skills/excalidraw/scripts/scene.py:142
- fix: Preserve connection multiplicity, using multisets of endpoint-and-label tuples or stable arrow IDs with an appropriate comparison fallback. Report additions and removals when parallel-arrow counts change.

### excalidraw#D8-3
- severity: medium
- dimension: D8
- location: skills/excalidraw/scripts/scene.py:179
- fix: Calculate boundary intersections according to the element type: rectangular, elliptical or diamond. Account for rotation when connecting existing shapes, or explicitly route unsupported geometry to the worker instead of generating detached endpoints.

### excalidraw#D8-4
- severity: medium
- dimension: D8
- location: skills/excalidraw/scripts/scene.py:160
- fix: For arrow containers, position bound text from the actual points translated by the arrow's x/y, rather than from its unsigned width/height. Preserve box-centering behavior for node labels and verify labelled connections pointing left and upward.

### excalidraw#D7-1
- severity: medium
- dimension: D7
- location: tests/skills/excalidraw/test_scene.py
- fix: Add a test that edits a fixture with a pre-existing dangling binding and asserts exit 1, the 'refusing to write an invalid scene' message and no output file. Add an eval prompt that asks to rename an arrow label and asserts that the agent uses `--relabel` and reads the resulting diff correctly.

### excalidraw#D8-1
- severity: medium
- dimension: D8
- location: skills/excalidraw/SKILL.md:47
- fix: Add: "Relabelling an arrow shows in diff as one removed and one added connection between the same two boxes; that pair is expected, not a bug."

### excalidraw#D8-2
- severity: low
- dimension: D8
- location: skills/excalidraw/SKILL.md:41
- fix: Document it: "`--add-node` also refuses a label that an existing arrow already uses; pick a different box label." Or limit the check in scene.py to labels whose container is a shape.

### excalidraw#D1-1
- severity: low
- dimension: D1
- location: skills/excalidraw/SKILL.md:43
- fix: Merge the two statements: keep the refusal guarantee once, in line 26 or line 43, and add the `.tmp` detail to it.

### excalidraw#D2-1
- severity: low
- dimension: D2
- location: skills/excalidraw/SKILL.md:41
- fix: Add a short layout procedure before the spec: put the main path on y=0 left to right, offset each decision branch by ±140 in y at the decision node's x plus 280, and run `summary` on OUT to confirm every edge before reporting.
