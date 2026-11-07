# Sources: mermaid-diagram-specialist (agent)

Checked 2026-11-07, batch 1 (BASE 72734b5348dd396ffa9cf47a9ca8d7f7206ec6a1). Review only: no `track` call, no edit of the artifact.

## Origins found

1. Original author: `qazuor/qazuor.com`, file `.claude/skills/tech/mermaid-diagram-specialist.md` on `main` (MIT, last commit of that path `0aa1b25b3826efe9c21dc55a283ead409d981e05`, 2025-11-05). Evidence: the baseline text is that file apart from a trailing "Related Skills" list and a "Changelog" table, and its worked examples are the author's Hospeda tourism platform (Clerk, Mercado Pago, Astro/Hono). The upstream is a skill of the author's own project, not a Claude Code agent.
2. Direct upstream: `softaworks/agent-toolkit`, file `agents/mermaid-diagram-specialist.md` on `main` (MIT). Its only commit for the path is `673fe76917d9fcf73ef059a40c6e543f95bfad98` (2026-01-18, "add 6 agents and 4 commands from claude-plugins"); the file at `3027f20f` and at the baseline `dbff837f` is identical to upstream `main` today (diffed, no difference).

The current file is a full rewrite as a delegate of the `mermaid-diagrams` skill; no text of the original survives except the title.

## Missing credit

The current agent carries no credit and the root `README.md` has none for it. The README already credits the fork source in line 5 ("Fork of softaworks/agent-toolkit"), which stays untouched. Proposed line for the root `README.md` (a command or agent has no README of its own), placed under the Agents table:

```text
mermaid-diagram-specialist is adapted from [qazuor/qazuor.com](https://github.com/qazuor/qazuor.com/blob/main/.claude/skills/tech/mermaid-diagram-specialist.md) by qazuor (MIT), through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/agents/mermaid-diagram-specialist.md).
```

## Proposed registry rows (verbatim; each passes `validate_entry`)

The existing row `{"skill": "mermaid-diagram-specialist", "kind": "local", ...}` says "no upstream", which is now wrong; replace it with the first two rows (a `local` row beside real source rows is contradictory).

```json
{"skill": "mermaid-diagram-specialist", "kind": "github-path", "source": "qazuor/qazuor.com:.claude/skills/tech/mermaid-diagram-specialist.md", "ref": "main", "credit": "qazuor", "artifact_kind": "agent"}
{"skill": "mermaid-diagram-specialist", "kind": "github-path", "source": "softaworks/agent-toolkit:agents/mermaid-diagram-specialist.md", "ref": "main", "credit": "softaworks", "artifact_kind": "agent"}
{"skill": "mermaid-diagram-specialist", "kind": "unversioned", "source": "Claude Code docs, Create custom subagents (https://code.claude.com/docs/en/sub-agents)", "ref": null, "credit": "Anthropic", "artifact_kind": "agent"}
{"skill": "mermaid-diagram-specialist", "kind": "unversioned", "source": "Mermaid docs, Architecture Diagrams (https://mermaid.js.org/syntax/architecture.html)", "ref": null, "credit": "Mermaid", "artifact_kind": "agent"}
{"skill": "mermaid-diagram-specialist", "kind": "unversioned", "source": "GitHub Docs, Creating diagrams (https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)", "ref": null, "credit": "GitHub", "artifact_kind": "agent"}
```

The last three are the official pages used in `facts.md`. The other official pages checked there (Mermaid flowchart, sequence, class, ER, state, C4 and gantt syntax, plantuml.com, graphviz.org, drawio.com) only confirmed that a name exists, so they get no row.

## skill-updater style review (review only)

- Rows: the registry has only the `local` row today. `upstreams` was not run because no source row exists yet; the two `github-path` rows above were checked by hand with `gh api`: both paths resolve on `main`, upstream softaworks is unchanged since the baseline, and the qazuor file's last commit (2025-11-05) predates the fork.
- Upstream change since the baseline: none in softaworks. The qazuor file differs from ours only by its "Related Skills" list (tech-writer, architecture-validator, product-technical, agents of that project that this repo does not ship) and its "Changelog" table (author-internal version metadata). Both: ignore, they name artifacts that do not exist here and are not credits.
- Adopt: none.
- Adapt: none required. Optional, for the Step 6 brief only if the coordinator wants them (neither is recorded as a loss): a C4 Context and a C4 Component worked example in `skills/mermaid-diagrams/references/c4-diagrams.md` (it holds only a Container example), and a one-line mention of the Mermaid `journey` type in `authoring-rules.md` section 1 (the old agent listed it; the skill draws user journeys as flowcharts). Both are skill edits, outside this agent's file.
- Ignore: the Hospeda domain examples (project data of the original author), the old arrow and participant lists in the sequence section (wrong: `->>` is a synchronous solid arrow and `-)` the async one; there is no `database` participant keyword), and the old classDef palettes (white text on #10B981, #EF4444 and #3B82F6 is below 4.5:1).
- Model-validity pass: the rules that counter a model habit are the NEVER list (invent an edge or cardinality, rename nodes silently, change the type silently, call an unrun diagram validated). Not probed in this review: a probe needs the referee runner lane, which is outside the analyst's rails. The skill-updater run in a later cycle should probe the first and last rule (inventing an edge and claiming validation are the habits a model shows without a rule). Until then keep all four.
