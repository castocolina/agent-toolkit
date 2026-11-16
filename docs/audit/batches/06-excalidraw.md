# Batch 06

## excalidraw (skill)

### excalidraw#D7-1
- severity: medium
- dimension: D7
- location: skills/excalidraw/evals/evals.json:7
- fix: Supply real scene fixtures and require created or edited artifacts. Assert parseability, editor acceptance, preserved unrelated elements, unique IDs, reciprocal bindings, and the requested label or connection changes.

### excalidraw#D7-2
- severity: medium
- dimension: D7
- location: skills/excalidraw/evals/trigger-queries.json:31
- fix: Give these positives explicit Excalidraw file paths or prior-context cues. Add format-unspecified diagram requests as boundary cases rather than assuming every flowchart uses Excalidraw.

### excalidraw#D8-1
- severity: medium
- dimension: D8
- location: skills/excalidraw/SKILL.md:12
- fix: Document a supported PNG round-trip tool and exact validation steps, or explicitly request a plain .excalidraw export before editing when that capability is unavailable.

### excalidraw#D8-2
- severity: medium
- dimension: D8
- location: skills/excalidraw/SKILL.md:28
- fix: Provide a known-good minimal scene template or a pinned creation tool, document required fields, and add an editor-open or render validation step with a repair-and-recheck loop.

### excalidraw#D7-1
- severity: medium
- dimension: D7
- location: skills/excalidraw/evals/evals.json:16
- fix: Bundle a small evals/files/architecture.excalidraw.json fixture so the modify path runs against a real scene; the referenced file does not exist.

### excalidraw#D8-1
- severity: medium
- dimension: D8
- location: skills/excalidraw/SKILL.md:3
- fix: Add a compare workflow (delegate a pairwise label/binding diff to the worker and report differences textually) or drop 'compare' from the description; the body defines no comparison procedure.

### excalidraw#D1-1
- severity: low
- dimension: D1
- location: skills/excalidraw/SKILL.md:24
- fix: Keep one precise ID invariant and one validation check, and consolidate repeated preservation instructions while retaining the explanations of binding and image-loss hazards.

### excalidraw#D4-1
- severity: low
- dimension: D4
- location: skills/excalidraw/SKILL.md:3
- fix: Create, inspect, modify, and compare editable Excalidraw diagrams. Use when the user supplies .excalidraw, .excalidraw.json, or source-embedded .excalidraw.png files, asks to change diagram labels or connections, or requests Excalidraw flowcharts or architecture sketches. Keep scene JSON out of the main conversation context. Not for Mermaid, draw.io, PlantUML, Graphviz, ordinary PNG editing, or text-only architecture explanations.

### excalidraw#D6-1
- severity: medium
- dimension: D6
- location: skills/excalidraw/SKILL.md:8
- fix: Default to bounded structured extraction for small read-only lookups without exposing scene JSON. Require isolation for large scenes and substantial edits, and reserve status announcements for cases where delegation materially affects execution.

### excalidraw#D1-1
- severity: low
- dimension: D1
- location: skills/excalidraw/SKILL.md:8
- fix: State the delegation rule once and cut the repeated restatements within the same paragraph; the rule is expert, the triple repetition is token waste.

### excalidraw#D2-1
- severity: low
- dimension: D2
- location: skills/excalidraw/SKILL.md:10
- fix: Add a short entry-point decision above the procedure (create / inspect / modify / compare) so each advertised mode routes to its own workflow instead of all modes funneling into the editing steps.

### excalidraw#D3-1
- severity: low
- dimension: D3
- location: skills/excalidraw/SKILL.md:12
- fix: Add a Format-gotchas entry for .excalidraw.png naming the specific loss (image editors that re-encode the PNG strip the embedded scene chunk) so the hazard lives with the other gotchas.

### excalidraw#D6-1
- severity: medium
- dimension: D6
- location: skills/excalidraw/SKILL.md:12
- fix: Name the default tool or exact operation for editing .excalidraw.png; vague guidance on a fragile, loss-prone operation invites corruption.
