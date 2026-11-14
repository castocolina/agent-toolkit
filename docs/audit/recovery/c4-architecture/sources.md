# Sources: c4-architecture (checked 2026-11-13)

## Origins found

1. **softaworks/agent-toolkit, `skills/c4-architecture`** (MIT, `gh api repos/softaworks/agent-toolkit --jq .license.spdx_id`). The baseline `dbff837f` is byte-for-byte the fork point `3027f20f`: `git diff --stat 3027f20f dbff837f -- skills/c4-architecture` is empty, so every baseline section is upstream text. The only upstream commit for the path is `06825f04` ("feat: add 23 curated skills", 2026-01-18). Upstream `main` is still `3027f20f3181758385a1bb8c022d4041dfb4de84`, the fork point, so nothing upstream changed since the fork.
2. **No origin before softaworks was found.** A web search on distinctive phrases ("Workout Tracker", "Vue PWA for tracking strength and CrossFit workouts", "Context + Container diagrams are sufficient") finds only copies. `davila7/claude-code-templates` (MIT, Daniel Avila) carries a SKILL.md that is identical to the softaworks file (`cmp` on `cli-tool/components/skills/creative-design/c4-architecture/SKILL.md`, 10575 bytes) but was added on 2026-01-25, a week after softaworks, so it is a downstream copy, not an origin. No registry row for it.
3. **Documentation the current text rests on** (each a proposed `unversioned` or tracked row below): Mermaid's C4 page and source, mermaid-cli, the C4 model site by Simon Brown, Simon Brown's post that supplies the quoted sentence in common-mistakes.md, and Puppeteer's troubleshooting page.

## Registry gap

`docs/audit/upstream-sources.json` has no row for `c4-architecture` at all (checked with `rg c4`; only the repo-level softaworks row exists). Credit gap: `skills/c4-architecture/README.md` has no Credits section and does not contain the text `softaworks/agent-toolkit`, so the `missing_credit` check would fail the moment the first row below is added. The upstream README never carried a credit either, so nothing was removed from this skill: the credit is simply new.

## Missing credit line (add to `skills/c4-architecture/README.md`, before "Additional Resources" or at the end, in the house style of naming-analyzer, mui and qa-test-planner)

```markdown
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-13): Mermaid (C4 diagram syntax, mermaid-cli), Simon Brown (C4 model), Puppeteer.
```

Every `credit` value in the rows below then appears verbatim in README.md or the references (`softaworks/agent-toolkit` in the README line; `Mermaid` and `Puppeteer` in SKILL.md and README.md; `Simon Brown` in common-mistakes.md and the README line).

## Proposed registry rows (verbatim JSON)

All six validate (`validate_entry`) and ran through `python3 scripts/audit/audit.py upstreams --registry <temp copy>` read-only with `error: null` and `stale: false` on 2026-11-13; no `track` call was made.

```json
[
  {
    "skill": "c4-architecture",
    "kind": "github-path",
    "source": "softaworks/agent-toolkit:skills/c4-architecture",
    "ref": "main",
    "credit": "softaworks/agent-toolkit"
  },
  {
    "skill": "c4-architecture",
    "kind": "github-path",
    "source": "mermaid-js/mermaid:packages/mermaid/src/docs/syntax/c4.md",
    "ref": "develop",
    "credit": "Mermaid"
  },
  {
    "skill": "c4-architecture",
    "kind": "github",
    "source": "mermaid-js/mermaid-cli",
    "ref": "master",
    "credit": "Mermaid"
  },
  {
    "skill": "c4-architecture",
    "kind": "unversioned",
    "source": "C4 model, Diagrams (https://c4model.com/diagrams), with Notation, Code, System context and the Container, Software system and Queues and topics abstraction pages",
    "ref": null,
    "credit": "Simon Brown"
  },
  {
    "skill": "c4-architecture",
    "kind": "unversioned",
    "source": "Simon Brown, Diagramming distributed architectures with the C4 model (https://dev.to/simonbrown/diagramming-distributed-architectures-with-the-c4-model-51cm)",
    "ref": null,
    "credit": "Simon Brown"
  },
  {
    "skill": "c4-architecture",
    "kind": "unversioned",
    "source": "Puppeteer, Troubleshooting (https://pptr.dev/troubleshooting)",
    "ref": null,
    "credit": "Puppeteer"
  }
]
```

Why a tracked row for the Mermaid source file and mermaid-cli: both churn (the C4 page gained the 11.17.1 wrap note, last upstream commit to the page 2026-10-30; mermaid-cli went from the 11.17.0 pin to 12.2.0 on 2026-11-02), and a `github-path` or `github` row is the only kind `upstreams` can mark stale. The `unversioned` rows are never reported stale (known limit in plan 14 Step 5); their check date lives in facts.md.

## skill-updater style review (review only, no `track` call)

Order of `SKILL.md` steps followed: scope resolved (`skills/c4-architecture/`, not synced); no existing rows, so the missing-row path (step 2) applies and no `track` call is allowed; the proposed rows were run through `upstreams` on a temp registry; contents test for the softaworks path passes (the path exists at `main`); no `error`; `stale: false` (upstream last touched 2026-01-18, `main` equals the fork point).

| item | decision | one-line reason |
| --- | --- | --- |
| softaworks `skills/c4-architecture` (no change since the fork point) | ignore | Upstream is identical to the baseline we already carry; nothing to port. Record `current` with `--sha 3027f20f3181758385a1bb8c022d4041dfb4de84` once the row exists. |
| Mermaid C4 page (mermaid-js/mermaid `c4.md`, 2026-10-30) | adapt | Matches the current c4-syntax.md on every point checked (see facts.md); the only differences are unsupported parameters of `UpdateElementStyle` (sprite, techn, legendText, legendSprite), which stay out on purpose. |
| mermaid-cli 12.2.0 (2026-11-02) replacing the 11.17.0 pin | adapt | Every syntax fact reproduced on 12.2.0. Reword SKILL.md step 5.1 and README Installation to say "mmdc 11 or newer; the checks were run on 11.17.0 and again on 12.2.0 (2026-11-13)" and keep `npx -y -p @mermaid-js/mermaid-cli mmdc` as the offline-unsafe fallback, keeping the 11.17.0 pin only as the known-good version. |
| advanced-patterns.md example labels `EKS 1.30`, `Node.js 20` | adapt | EKS 1.30 is no longer offered and Node.js 20 is EOL; the labels are illustrative, so drop the EKS number (or say it comes from the IaC) and use `Node.js 22`. |
| advanced-patterns.md "the official Mermaid example does (`bigbank-api x8`)" | adapt | The official label is `bigbank-api*** x8`; quote it exactly or say "a replica count such as x8". |
| common-mistakes.md Simon Brown quote | adapt | Add the source URL (the dev.to post of 2021-05-19) next to the quote; never remove the attribution already there. |
| README credit | adopt (new) | Add the Credits section above. |
| Restore rows from record.md | adopt | s011 and s031 (one SKILL.md step 5 check bullet), s094, s095, s104 (common-mistakes.md). |
| Drop-pending rows | ignore for now | s012, s023, s032, s041, s045, s047, s048, s050, s051, s053, s076, s078, s079, s081: verdict DROP in the report; the controller decides. |

Model-validity pass: **not run.** The pass needs a tool-less probe through the repo's LLM probe lane (`audit.py pi-cmd runner`), and the brief for this analyst forbids LLM-lane review. Rules that exist to counter a model habit, for the controller to probe if wanted, each with the prompt that should elicit the habit:

- "NEVER number labels in C4Dynamic" (habit: hand-numbered steps; the baseline's own examples did it). Prompt: "Draw the user sign-in flow as a Mermaid C4Dynamic diagram: browser, API controller, auth service, database."
- "NEVER use BiRel" (habit: two-way arrows for request/response). Prompt: "Draw a Mermaid C4Container diagram for a React app that calls an order API which reads and writes PostgreSQL."
- "NEVER draw one Kafka box wired to every service". Prompt: "Draw a Mermaid C4Container diagram for order, inventory and payment services that talk through Kafka."
- "NEVER give a Container a { } body" and "NEVER write C4Landscape". Prompts: "Show the Order API container with its controller and repository inside it as Mermaid C4." and "Draw a Mermaid system landscape for four internal systems."
- "NEVER draw a shared library as a container". Prompt: "Draw a C4 container view of two services and the shared utils library both import."

Local evidence already in hand: the baseline text itself shows the first habit (hand-numbered labels in three examples), and the mmdc runs show the failure each rule prevents.
