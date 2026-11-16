---
name: mermaid-diagrams
description: "Create, edit and repair Mermaid diagrams (.mmd files or ```mermaid blocks in Markdown). Use when asked to diagram, visualize, model or map out sequence flows, class models, ER diagrams or database schemas, state machines, C4 or architecture-beta architecture (including terse requests such as 'architecture: mobile client, API, database, email provider'), Gantt schedules, pie splits or Git branch history, or when a Mermaid diagram fails to render or export (mmdc, GitHub), even without naming Mermaid. Pick the type from the question the diagram answers; flowchart is the last resort. Not for prose-only explanations, explaining an existing diagram without changing it, edits to a file that leave its mermaid block alone, PlantUML or draw.io work, matplotlib data charts, or interactive diagram-canvas components."
---

# Mermaid Diagramming

Unknown words break a diagram and parameters fail silently, so validate in the host that will render it.

## Workflow

1. **Ground** - state every assumption; never invent an edge the supplied code, schema, or facts do not show. An architecture, schema, or refactor question is not by itself a request for a diagram. If the supplied material does not settle the type or a cardinality, state the assumption in the reply; when two types are equally plausible, ask one question. Before drawing, ask yourself: what question does this diagram answer (pick the type for it from authoring-rules.md section 1 "Choose the diagram type"), and would a reader get the answer in under 10 seconds? If not, cut detail or split.
2. **Fork.** [authoring-rules.md](references/authoring-rules.md) is mandatory on every path, in the sections below (cited by number and heading; both are fixed, so these citations stay valid):

   | Job | Read | Change |
   |---|---|---|
   | Parse repair: it fails to render | section 7 "Labels that break the parser"; the type file only if the error is not covered | syntax only; keep every node, edge, label, and meaning |
   | Semantic repair: it renders, but arrows, elements, cardinalities, or layout are wrong | section 7; for a flowchart also section 4 "Subgraphs for grouping"; the type file, including its traps | whatever restores the meaning the user intended; say what changed and why |
   | Appearance only: colors, theme, or config of a diagram that is otherwise right | section 6 "Contrast and classDef palette"; [advanced-features.md](references/advanced-features.md) when the theme or frontmatter config changes | styling only; keep every node, edge, and label; check text/fill contrast before validating |
   | New diagram, type obvious and unstyled | sections 1 "Choose the diagram type" and 7; the type file | everything |
   | New diagram, otherwise | sections 1-3 ("Choose the diagram type", "Direction and proportion", "Type-native controls") and 6-7 ("Contrast and classDef palette", "Labels that break the parser"); for a flowchart also 4-5 ("Subgraphs for grouping", "Shapes mean roles"); the type file | everything |

   For a mixed job (for example a semantic repair that also asks for new colors), take the union of the Read cells and apply the broader Change cell. When the type is plausible but not obvious, use the last row.

   Do NOT load `c4-diagrams.md` for `architecture-beta` or for repairing a non-C4 diagram. For a flowchart, authoring-rules.md sections 4-5 are the type reference.
3. **Draw, then self-check before validating.** Scan every flowchart node and edge label: is any `[ ] ( ) { } < > |` unquoted? (Sequence messages like `find(id)` are legal as written; do not quote them.) Is there a `#` or `;` in sequence text? Is lowercase `end` used as a node or participant id? Does a target whose name starts with `o` or `x` follow a link directly (`A---orders` parses as a circle edge to `rders`)? Intended circle or cross edges stay. Fix each from section 7; mmdc reports only the first parse error, and `#` fails silently.
4. **Validate** - `npx -y @mermaid-js/mermaid-cli -i in.mmd -o out.svg`. The CLI's bundled Mermaid decides what parses. Pinning the CLI does not pin Mermaid (every 11.x CLI depends on `mermaid ^11`, so it resolves the latest 11.x). Only when the user names the host's Mermaid version, validate in a scratch project whose package manager overrides `mermaid` to that exact version, and report the version actually installed; for GitHub or an unknown host, validate unpinned and name in the reply any version-gated construct from "Renderer and host constraints" that the diagram uses. Rerun after each fix; after three failing rounds, stop and report the remaining error with your best version. Then check the source against the Gotchas below, which exit 0 does not catch, and the rendered SVG's size against section 2 "Direction and proportion"; for a new diagram, split it if it fails; for a repair, keep the structure and report the readability problem instead. A Chromium sandbox error (`No usable sandbox`, `--no-sandbox`) is not a diagram error: write `{"args":["--no-sandbox"]}` to `puppeteer.json` and rerun with `-p puppeteer.json`. If it still cannot run (no network, no Chromium), say in the reply that the diagram was not validated and list as unverified each construct you changed or added (for example the newly quoted labels, `<br/>` line breaks, a renamed `End` node, entity codes such as `#35;`), plus any version-gated syntax the diagram uses (for example `architecture-beta`).

| Type chosen | Read |
|---|---|
| Sequence | [sequence-diagrams.md](references/sequence-diagrams.md) |
| Class | [class-diagrams.md](references/class-diagrams.md) |
| ERD | [erd-diagrams.md](references/erd-diagrams.md) |
| C4 | [c4-diagrams.md](references/c4-diagrams.md) |
| architecture-beta | [architecture-diagrams.md](references/architecture-diagrams.md) |
| State, Git, Gantt, or Pie | [other-diagrams.md](references/other-diagrams.md) |
| Flowchart | authoring-rules.md sections 4-5 (the flowchart reference) |
| Frontmatter theme, click, export flags, accessibility | [advanced-features.md](references/advanced-features.md) |

## Renderer and host constraints

- `architecture-beta` needs Mermaid 11.1+; older hosts print a syntax error or raw text. Its icons are ONLY `cloud`, `database`, `disk`, `internet`, `server`. Never write `aws:`, `logos:`, or any other prefixed icon unless the user names a renderer that registers that pack. When the user asks for AWS, Docker, or other vendor logos, say in the reply that `aws:` and `logos:` icons render as `?` on GitHub and in the VS Code preview, and that built-in icons are used instead.
- `architecture-beta` edge labels (`a:R -[HTTPS]-> L:b`) parse in Mermaid 11.17 but not on every host; for GitHub put the protocol in the service title or use C4 `Rel`.
- Expanded node shapes `A@{ shape: cyl }` need Mermaid 11.3+; bracket shapes work everywhere.
- Frontmatter `config` needs Mermaid 10.5+; older hosts ignore it or print it as text. `look: handDrawn` needs 11+. `layout: elk` needs the host to register `@mermaid-js/layout-elk`, otherwise it silently falls back to dagre.
- GitHub bundles its own, older Mermaid: it lays out C4 its own way (labels may overlap or clip) and may lag on newer gitGraph options. Check the rendered result there, not only in Mermaid Live.

## Gotchas

These cost the most because the renderer accepts them, or because the cue to open the right file is easy to miss.

- NEVER write `Child <|-- Parent`: the arrowhead sits on the parent, and the inverted hierarchy renders with no error ([class-diagrams.md](references/class-diagrams.md)).
- NEVER reuse a C4 id: every Person, System, Container, and Component id must be unique across the diagram. A repeated id raises no error and silently redirects `Rel` arrows to the wrong element ([c4-diagrams.md](references/c4-diagrams.md)).
- NEVER write a gantt date in a format other than the declared `dateFormat`: it raises no error and the bar is drawn with a wrong span ([other-diagrams.md](references/other-diagrams.md)).
- NEVER read an ER cardinality glyph from the wrong end: each glyph describes the entity it touches, so `CUSTOMER }o--|| ORDER` (many customers per order) renders as happily as the intended `CUSTOMER ||--o{ ORDER` ([erd-diagrams.md](references/erd-diagrams.md)).
- NEVER put a `classDef` class on `[*]`: it is a parse error; style the first real state instead ([other-diagrams.md](references/other-diagrams.md)).
- NEVER leave out or mark optional the reply to a request in a detailed synchronous request/response sequence (anything the user describes call by call, or where they mention an answer coming back): every `->>` call gets its `-->>` reply unless the user says it is fire-and-forget (then use `-)`). A high-level overview may omit replies on purpose; say so. A syntax-only repair never adds reply edges. Two silent sequence traps live in [sequence-diagrams.md](references/sequence-diagrams.md): a label used where the alias id belongs creates a second participant, and an unbalanced `+`/`-` activation runs to the bottom.
- NEVER give a pie slice a negative value: it is a parse error ([other-diagrams.md](references/other-diagrams.md)).
- NEVER `checkout` a gitGraph branch before its `branch` line; it is a parse error. Add the `branch` line at the commit the branch really started from ([other-diagrams.md](references/other-diagrams.md)).
- NEVER link a node inside a flowchart subgraph to a node outside it while relying on that subgraph's `direction`: Mermaid silently drops the `direction` ([authoring-rules.md](references/authoring-rules.md) section 4 "Subgraphs for grouping").
- NEVER leave a raw `#` in sequence message text: the rest of the message silently disappears (section 7 "Labels that break the parser").
- The most frequent parse failures are lowercase `end` as an id (it closes a block), an unquoted `(` in a label (it opens a second shape), and a target starting with `o` or `x` right after a link (`A---orders` becomes a circle edge to `rders`); step 3 scans for them, and the fixes are in section 7.
