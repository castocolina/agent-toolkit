---
name: excalidraw
description: Create, inspect, modify, and compare editable Excalidraw diagrams. Use when the user supplies *.excalidraw or *.excalidraw.json files or explicitly requests Excalidraw flowcharts or architecture sketches. Keep large scene JSON out of the primary conversation context. Not for Mermaid, draw.io, PlantUML, Graphviz, or text-only architecture explanations.
---

# Excalidraw

Keep scene JSON out of the main context for every file size, including a single label lookup or other small inspection. The main agent must not read, parse, or print the Excalidraw JSON directly. Say up front that even a tiny file or a single label lookup must be delegated, including when the user calls it too small to need delegation. Delegate all inspection to an isolated worker; write the delegate request so it asks for a text-only response containing only the requested labels, relationships, or a concise summary—never raw/full JSON. Only when delegation is impossible, use a local structured tool such as `jq` to extract just the needed fields without printing the scene or inviting the user to paste it, and call that the fallback, not main-context inspection.

## Safe editing procedure

1. Identify JSON versus `.excalidraw.png` (which may embed editable source). For embedded PNG source, use a tool that preserves the image and metadata; do not treat it as plain JSON.
2. Parse the scene and inspect only needed elements/relationships. Record existing IDs, element types, bound text, arrow endpoints, app/version metadata, and relevant layout.
3. Make the smallest edit. Preserve unrelated elements, IDs, files metadata, appState, and seed/version fields. Generate unique IDs for all new elements; never reuse an existing ID.
4. Update relationships atomically: when moving/deleting bound elements, repair `containerId`, `boundElements`, `startBinding`, and `endBinding` as applicable. Never leave arrows pointing at missing IDs or text bound to removed containers.
5. Validate output parses, preserves existing content, has unique IDs, and every non-null binding resolves to an existing element. Summarize changed labels and relationships, not raw JSON.

## Format gotchas

- An arrow's visual endpoints and bindings are distinct; changing one without the other can leave a line that looks connected but is semantically dangling.
- Bound text/container relationships must be reciprocal where the format requires them. Verify both sides after edits.
- Do not regenerate `appState`, `files`, or scene metadata for a local change; embedded images and user settings can be lost.
- Preserve existing `seed`/`version` values for untouched elements; use valid unique IDs and appropriate version metadata for new ones.
- IDs must be unique across the entire scene, not merely among newly created shapes.

## Worker task contracts

When dispatching a worker, require it to report the scene version, intended minimal diff, preserved IDs, new IDs, binding checks, and validation result. For creation, require valid Excalidraw JSON with an `elements` array and bound arrows referencing existing IDs. If worker execution fails, use bounded `jq` extraction/editing where supported or ask for a compact export; do not claim a file was changed without checking it.
