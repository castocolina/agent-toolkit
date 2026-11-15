# Sources: mermaid-diagrams (checked 2026-11-13)

## Origins found

1. **softaworks/agent-toolkit, `skills/mermaid-diagrams`** (MIT, `gh api repos/softaworks/agent-toolkit --jq .license.spdx_id`). The fork point `3027f20f` carries README.md, SKILL.md and `references/` (advanced-features, architecture-diagrams, c4-diagrams, class-diagrams, erd-diagrams, flowcharts, sequence-diagrams). The baseline `dbff837f` is not byte-for-byte the fork point: `git diff --stat 3027f20f dbff837f -- skills/mermaid-diagrams` shows README (4 lines), SKILL.md, advanced-features.md and flowcharts.md edited, and `references/authoring-rules.md` (151 lines) added locally. So the authoring-rules content (classify first, 900px column, palettes A to C, label rules) is this repository's own work, not upstream text. The upstream path was last changed by `025dcd00` ("docs[mermaid-diagrams]: add architecture diagrams reference and links (#5)", 2026-02-01) and created by `06825f04` (2026-01-18); upstream `main` is still `3027f20f3181758385a1bb8c022d4041dfb4de84` (2026-03-05), the fork point, so nothing upstream changed since the fork.
2. **No earlier origin found.** The old text is generic Mermaid-documentation prose and examples (the Title/Genre/Season domain model, the login sequence, the USER/ORDER/LINE_ITEM schema, the "System Context Diagram for E-commerce Platform"). A search for those distinctive pieces finds only copies of the softaworks skill; no author or earlier repository is named anywhere, so none is credited beyond softaworks.
3. **Documentation the current text rests on** (each a proposed `unversioned` row below): the Mermaid syntax pages for each diagram type, the Mermaid configuration pages (theming, layouts, configuration, directives, usage, icons, the ELK schema), Mermaid release notes (v11.0.0 and mermaid@12.0.0), the mermaid-cli repository, GitHub Docs on Mermaid in Markdown, the VS Code extension the README names, and Puppeteer's troubleshooting page (the sandbox rule in SKILL.md step 4, shared with c4-architecture).

## Registry gap and credit gap

`docs/audit/upstream-sources.json` has no row for `mermaid-diagrams` (checked with `rg mermaid-diagrams`; only the unrelated `mermaid-diagram-specialist` agent rows exist). `skills/mermaid-diagrams/README.md` has no credit line and does not contain the text `softaworks/agent-toolkit`, so the `missing_credit` check fails the moment the first row below is added. The upstream README never carried a credit either (`git show 3027f20f:skills/mermaid-diagrams/README.md` ends with "Support"), so nothing was removed: the credit is new.

## Missing credit line (add to `skills/mermaid-diagrams/README.md`, after Support, in the house style used for c4-architecture, database-schema-designer and gemini)

```markdown
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-13): Mermaid (diagram syntax, configuration, mermaid-cli), GitHub (Mermaid diagrams in Markdown), Matt Bierner (Markdown Preview Mermaid Support extension), Puppeteer (browser sandbox troubleshooting).
```

Every `credit` value in the rows below then appears verbatim in README.md: `softaworks/agent-toolkit`, `Mermaid`, `GitHub`, `Matt Bierner` and `Puppeteer` (SKILL.md uses only the lower-case `puppeteer.json`, which does not match the credit text).

## Proposed registry rows (verbatim JSON)

All 21 validate with `validate_entry` and ran through `python3 scripts/audit/audit.py upstreams --registry <temp file holding only these rows>` read-only on 2026-11-13, exit 0, `error: null`, `stale: false` on every row (the softaworks row reports `source_updated` 2026-02-01, before the fork). No `track` call was made. The file is also at `tmp/mermaid-diagrams-registry-rows.json`.

```json
[
  {
    "skill": "mermaid-diagrams",
    "kind": "github-path",
    "source": "softaworks/agent-toolkit:skills/mermaid-diagrams",
    "ref": "main",
    "credit": "softaworks/agent-toolkit"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "github",
    "source": "mermaid-js/mermaid-cli",
    "ref": "master",
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Flowchart syntax (https://mermaid.js.org/syntax/flowchart.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Architecture diagrams (https://mermaid.js.org/syntax/architecture.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Class diagrams (https://mermaid.js.org/syntax/classDiagram.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Entity relationship diagrams (https://mermaid.js.org/syntax/entityRelationshipDiagram.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Sequence diagrams (https://mermaid.js.org/syntax/sequenceDiagram.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Gantt diagrams (https://mermaid.js.org/syntax/gantt.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Gitgraph diagrams (https://mermaid.js.org/syntax/gitgraph.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, State diagrams (https://mermaid.js.org/syntax/stateDiagram.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Pie chart (https://mermaid.js.org/syntax/pie.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, XY chart (https://mermaid.js.org/syntax/xyChart.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Theme configuration (https://mermaid.js.org/config/theming.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Layouts (https://mermaid.js.org/config/layouts.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Configuration and directives (https://mermaid.js.org/config/configuration.html, https://mermaid.js.org/config/directives.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, Usage and icon packs (https://mermaid.js.org/config/usage.html, https://mermaid.js.org/config/icons.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid docs, ELK configuration schema (https://mermaid.js.org/config/schema-docs/config-properties-elk.html)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Mermaid releases, v11.0.0 and mermaid@12.0.0 notes (https://github.com/mermaid-js/mermaid/releases)",
    "ref": null,
    "credit": "Mermaid"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "GitHub Docs, Creating diagrams (https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)",
    "ref": null,
    "credit": "GitHub"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Visual Studio Marketplace, Markdown Preview Mermaid Support (https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)",
    "ref": null,
    "credit": "Matt Bierner"
  },
  {
    "skill": "mermaid-diagrams",
    "kind": "unversioned",
    "source": "Puppeteer, Troubleshooting (https://pptr.dev/troubleshooting)",
    "ref": null,
    "credit": "Puppeteer"
  }
]
```

## skill-updater style review (review only; no `track` call, no edit)

Read-only reasoning from `skills/skill-updater/SKILL.md`. Step 2: the artifact has no row, so the credit line gets a proposed row and no `track` call (the skill says `track` cannot create a source row). Step 3 and 4 run on the temp registry above: the `github-path` row has `error: null`, `source_updated` 2026-02-01 (the upstream path's last commit, before the fork), so there is no upstream change to classify and nothing is stale. Step 6, the model-validity pass, was not run: it needs the `pi-cmd` probe lane, which the analyst brief forbids; the controller can run it on the rules listed below.

Adopt, adapt, ignore items for the restore brief:

| item | verdict | reason |
| --- | --- | --- |
| Upstream softaworks changes since the fork | ignore | none exist: `main` is the fork point and the path's last commit predates it |
| Mermaid 12.0.0 default theme `redux-color`, look `neo`, layout `elk` (theming and layouts pages, release notes) | adapt | name the new defaults in SKILL.md Renderer constraints and in the restored config block, keep every classDef and palette rule (they set fill, stroke and color), give `theme: default`, `look: classic`, `layout: dagre` as the way back |
| `layout: elk` registration sentence in SKILL.md | adapt | correct it: bundled and automatic from 12.0.0, registration only for older hosts and the tiny build |
| "every 11.x CLI depends on mermaid ^11" in SKILL.md step 4 | adapt | an unpinned npx now resolves Mermaid 12; keep the rule that the CLI's bundled Mermaid decides |
| README Advanced Capabilities lines (five themes, dagre or ELK, classic or hand-drawn) | adapt | rewrite as pointers to the theming and layouts pages and `mmdc --help` |
| ELK options, theme variable names, built-in theme names (rows s041, s040, s038) | adopt | restore to `references/advanced-features.md` as verified facts, with the schema and theming pages as the pointer for the rest |
| Docker export and export flags (row s033) | adapt | restore the CLI README's `-u` form and `--size`, `-b`, `-s`, `-t`; drop the removed `-w` and `-H` |
| Abstract and static markers (row s113), participant links (row s171) | adopt | restore as one verified line each into `class-diagrams.md` and `sequence-diagrams.md` |
| Add the GitHub docs pointer: render a ```mermaid block containing `info` to read the host's Mermaid version | adopt | replaces the unverifiable "GitHub bundles an older Mermaid" with a way to read the value |
| Page-embedding material (HTML, React, responsive CSS; rows s054, s059, s060) | ignore | outside the skill (description excludes diagram-canvas components) and stale (`mermaid@10`, `contentLoaded`) |
| A pointer from c4-diagrams.md to the c4-architecture skill for full C4 work | adapt (optional) | the large C4 examples and event-driven patterns moved there; mermaid-diagrams does not mention the skill today |

Rules that exist to counter a model habit, candidates for the controller's model-validity probe: classify the type before drawing (flowchart is the habitual default), quote labels containing `( ) [ ] { } < > |`, give every synchronous `->>` call its `-->>` reply, prefer top-down layouts, and use palette-based colors with text color set on every fill. Not probed here.
