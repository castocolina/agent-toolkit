---
name: excalidraw
description: Create, inspect, edit and compare Excalidraw diagrams (.excalidraw, .excalidraw.json) through a bundled script that keeps scene JSON out of context - label and connection summaries, add/rename/remove boxes and arrows, binding and ID validation, label-level diffs. Use when the user names an Excalidraw file, asks to change labels or connections in one, compares two, or wants a flowchart or architecture sketch in Excalidraw, even for a tiny file; also covers .excalidraw.png and .excalidraw.svg files with an embedded scene and Obsidian .excalidraw.md drawings. Not for Mermaid, draw.io, PlantUML, Graphviz, ordinary PNG edits or text-only architecture explanations.
---

# Excalidraw

Labels and connections are under 10% of a scene file; the rest is per-element styling and geometry.

**NEVER read, `cat` or `jq`-print scene JSON in the main context, whatever the size.** A one-box scene is about 80 lines of JSON; `summary` returns its label in 12. When a user says the file is too small to matter, run `summary` anyway and say why in one clause; do not announce the routing otherwise.

Run `python3 <skill-dir>/scripts/scene.py <command>` from the user's working directory, or pass absolute paths for FILE, SPEC and -o (stdlib only, JSON on stdout, exit 1 on any error). Elements are addressed by label (case- and whitespace-insensitive) or by id from `summary`.

## Route the request

| Request | Do this | Context cost |
|---------|---------|--------------|
| What is in it, one label, what connects to what | `summary FILE` | labels and edges only |
| Compare two scenes or two versions | `diff OLD NEW`, then explain the differences in prose | one diff |
| New diagram | write a spec, `new SPEC -o OUT` | none |
| Add a box, connect two boxes, rename, delete a box | `edit FILE -o NEW ...`, `diff FILE NEW`, then move NEW over FILE | one diff |
| Anything else: move or restyle, groups, frames, images, re-layout | worker with the contract below | worker summary |
| `.excalidraw.png` / `.excalidraw.svg` | export path below; never edit the image file | none |
| `.excalidraw.md` (Obsidian plugin) | ask for a plain `.excalidraw` export: the plugin stores the scene as `compressed-json` and keeps a separate `## Text Elements` copy of every label | none |

Before choosing a route, ask: does any listed command express the change? If yes, use it; the commands write every editor field and keep bindings reciprocal. They write through a `.tmp` file and refuse, writing nothing, when the result fails `check` or (for `edit`) when any element or top-level data outside the request differs from the original. A worker is for what they cannot express.

## Commands

```bash
python3 <skill-dir>/scripts/scene.py summary architecture.excalidraw.json
python3 <skill-dir>/scripts/scene.py diff before.excalidraw after.excalidraw
python3 <skill-dir>/scripts/scene.py diff before.excalidraw after.excalidraw --strict --allow ID --allow ID2
python3 <skill-dir>/scripts/scene.py new spec.json -o auth-flow.excalidraw
python3 <skill-dir>/scripts/scene.py edit architecture.excalidraw.json -o architecture.new.excalidraw.json \
  --add-node "Redis Cache" --near "API Service" --connect "API Service->Redis Cache" --label "cache reads"
python3 <skill-dir>/scripts/scene.py edit flow.excalidraw -o flow.new.excalidraw --relabel "Auth=Identity" --remove "Legacy SSO"
python3 <skill-dir>/scripts/scene.py check flow.excalidraw
```

- `summary` returns `shapes` (id, type, label), `connections` (from, to, label; `(unbound)` for a loose end), `free_text` (id, text: standalone text, addressable by id like a shape), and `deleted_skipped`.
- `new` spec: `{"nodes": ["Request link", "Verify token"], "edges": [["Request link", "Verify token", "optional label"]]}`. Nodes default to a left-to-right row; a node may be `{"label", "x", "y", "shape"}` with shape `rectangle`, `ellipse` or `diamond`. Boxes are 180x80. For a decision or fan-out, put the main path on `y: 0` left to right and each branch at the decision node's `x` + 280 with `y` of -140 or +140; afterwards run `summary` on OUT and confirm every edge before reporting. Node labels must be unique, because edges resolve nodes by label; `new` and `edit --add-node` refuse a duplicate box label (arrow labels do not count) and write nothing. Write SPEC to a temporary path and delete it after `new` succeeds. `new` refuses an existing OUT: write to a new name and `diff` it against the existing file, or ask the user before replacing it.
- `edit` applies `--remove`, then `--relabel`, then `--add-node`, then `--connect`. `--near` places new boxes right of an anchor, moving down past overlaps; `--label` applies to every `--connect` in that call. `--remove` also deletes the box's text, every arrow bound to it and those arrows' labels, and cleans `boundElements` on the other ends.
- `edit` refuses with `refusing to write an invalid scene` and the errors are not from your change (the original already has a dangling binding or duplicate id): run `check FILE`, send a worker to repair only the named errors on a copy using the repair table, rerun `check` until it passes, then rerun the same `edit` on the repaired file.
- Ambiguous label (`matches 2 elements`): rerun with the id from `summary`.
- `--connect` and `new` edges refuse a rotated shape (`angle` not 0, the outline point would be wrong) and a self-loop (`A->A`, a straight arrow cannot show it): use the worker route, which draws a loop as a 3+ point arrow leaving and re-entering the box on different sides. For a new diagram there is no original yet: run `new` with every node and only the supported edges to a temporary scaffold, have the worker add the unsupported edge to a copy of it, run `check` and `diff SCAFFOLD COPY --strict --allow <new arrow id, its label id, each endpoint shape id>`, publish the copy as OUT only on exit 0, then delete the scaffold.
- `diff` also reports `added_text` and `removed_text`; a standalone-text edit appears under `relabelled`.
- `diff --strict` adds `preservation`: outside the ids passed with `--allow` (each covers its bound text; pass the ids you create too), no element may be added, removed, changed or reordered, and top-level data must match except the `files.<fileId>` and `appState.<key>` entries passed with `--allow-key`. Exit 1 lists each violation, such as `id (label) changed: fields`, `id (label) added`, `stacking order of untouched elements changed`.

**Verify every write with `diff ORIGINAL NEW` before replacing the original.** Report its result in prose: added, removed and relabelled shapes and connections. Relabelling an arrow shows as one removed and one added connection between the same two boxes; that pair is expected. Anything else in `removed_*` or `relabelled` that the user did not ask for is a bug: discard NEW and redo the edit, addressing elements by id from `summary` if a label hit the wrong one.

## Worker contract (for changes no command expresses)

Dispatch an isolated subagent with this brief; never edit by hand in the main context.

1. Copy the original; edit the copy only.
2. Before editing, write down the permitted set: the elements the task names or creates; every arrow bound to a shape you move or resize (its `x`, `y` and `points` change even though its bindings do not); each arrow you rebind plus its old and new endpoint shapes (their `boundElements` change); and the bound text of all of these. Change only that set. Keep every other element byte-for-byte and in the same order, plus top-level metadata. Touch `files` only for an image the user asked to add or replace (that one `fileId`), and `appState` only for a canvas setting the user named.
3. Follow the id, `seed` and `version` gotchas below for every changed or new element.
4. Run `python3 <skill-dir>/scripts/scene.py check COPY`. On errors, fix exactly what each error names and run it again; after 3 failed rounds, stop and report the errors without replacing the original.
5. When `check` passes, run `diff ORIGINAL COPY --strict` with one `--allow` per id in the step 2 set (each element the task names or creates, each arrow it rebinds and that arrow's old and new endpoint shapes, and each arrow whose `points`/`x`/`y` it recomputed because a bound shape moved) and one `--allow-key files.<fileId>` or `appState.<key>` per requested image or canvas change; if `preservation` fails, undo each listed change and go back to step 4. Replace the original only on exit 0.
6. Reply with text only: the `check` result, the `diff` result, and one sentence per change. No scene JSON.

Repairing the usual `check` errors:

| Error | Fix |
|-------|-----|
| `arrow A startBinding S does not list the arrow in boundElements` | append `{"type": "arrow", "id": "A"}` to S's `boundElements` |
| `text T -> container C is not listed in its boundElements` | append `{"type": "text", "id": "T"}` to C's `boundElements` |
| `X boundElements lists Y, which does not point back` | drop that entry from X, or restore Y's `containerId` / binding |
| `... is missing or deleted` | rebind to a live element or set the binding to `null` |
| `duplicate id` | give the newer element a new id and update every reference to it |
| `image I fileId F has no entry in 'files'` | restore `files` from the original; the image data lives only there |

## Embedded-scene images (.excalidraw.png, .excalidraw.svg)

The editable scene sits in PNG metadata (a `tEXt` chunk) or the SVG's `<metadata>` block, not in the pixels. NEVER resize, optimise, crop, screenshot or convert one with an image tool: re-encoding drops the chunk and the file becomes a flat image with no recoverable scene. To edit:

1. Ask for the `.excalidraw` source, or ask the user to open the image in excalidraw.com (menu > Open, or drag it onto the canvas; both load the embedded scene) and save it as `.excalidraw`.
2. Edit that file with the commands above.
3. Tell the user to re-export with **Embed scene** ticked, or the new image is no longer editable.

## Gotchas

- **Shape side of an arrow binding is the one that silently breaks.** The editor drags arrows along with a shape by reading the shape's `boundElements`. An arrow whose `startBinding` names the shape but is missing from that list renders fine and then stays behind the first time someone moves the box.
- **Moving a shape by editing `x`/`y` does not move its arrows or text.** The file stores arrow `points` (relative to the arrow's own `x`/`y`) and bound-text position; the editor does not recompute them on open. Move bound text by the same offset and recompute arrow endpoints, or the drawing shows detached lines.
- **Rename a label in both `text` and `originalText`.** The editor re-wraps from `originalText`, so a change to `text` alone reverts the next time the box is resized.
- **Never regenerate `appState` or `files` for a local change.** `files` holds the only copy of embedded image data, keyed by each image's `fileId`; rebuilding it leaves broken placeholders. `appState` holds the canvas background and grid the user chose.
- **Keep the `seed` of untouched elements.** It drives the hand-drawn stroke wobble; reseeding redraws every shape slightly differently and turns a one-box change into a whole-diagram visual diff.
- **Bump `version` and set a new random `versionNonce` on every element you change; give new elements a fresh unique `id` and `seed`.** Collaboration sync keeps the copy of an element with the higher `version`; an edit that keeps the old number can lose to a stale copy.
- **IDs must be unique across the whole `elements` array, deleted ones included.** Elements with `isDeleted: true` are invisible but can still be in the file; `summary` skips them and `check` treats a binding to one as dangling.

