# Excalidraw Skill

A skill for creating, inspecting, editing and comparing Excalidraw diagrams (`*.excalidraw`, `*.excalidraw.json`) without loading scene JSON into the agent's context.

## Why

Excalidraw files have a very low signal-to-noise ratio. Each element carries 20+ geometry and styling properties (x, y, seed, version, roughness, ...), while the content that matters, labels and connections, is under 10% of the file. Measured on real diagrams:

- 14-element diagram: 596 lines, 16K
- 79-element diagram: 2,916 lines, 88K (tens of thousands of tokens; more lines than the Read tool returns in one call, so it needs paging)

Token counts depend on the tokenizer, so the sizes above are lines and bytes. Reading 7 such diagrams directly cost about 67k tokens, a third of a 200k-token window; the window size varies by model (see the "Context window" row of the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview), checked 2026-11-13).

## What it does

`scripts/scene.py` (Python 3, standard library only) does the work and prints only compact JSON:

- `summary` lists shapes, labels and connections.
- `diff` reports label-level changes between two scenes.
- `new` builds a scene from a short node/edge spec.
- `edit` adds, connects, renames and removes boxes while keeping bindings reciprocal.
- `check` validates IDs, bindings, frames and image references.

Changes the script cannot express go to an isolated subagent under a fixed contract. `SKILL.md` holds the routing, the commands, the worker contract and the format gotchas.

## Installation

**Claude Code:**

```bash
cp -r skills/excalidraw ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

## Tests

```bash
python3 -m unittest discover -s tests/skills/excalidraw -p 'test_*.py'
```

## Credits and sources

- The skill began as `skills/excalidraw` in softaworks/agent-toolkit; `scripts/scene.py`, the routing and the worker contract were written for this repository.
- The scene format and the embedded-scene export (`.excalidraw.png`, `.excalidraw.svg`, "Embed scene") follow the [Excalidraw](https://plus.excalidraw.com/docs/sdk/codebase/json-schema) documentation and source.
- The Obsidian `.excalidraw.md` layout (`compressed-json`, `## Text Elements`) follows the Obsidian Excalidraw plugin by Zsolt Viczian.
- The context-window statement follows Anthropic's [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).

## License

Part of the Softaworks Agent Skills collection.
