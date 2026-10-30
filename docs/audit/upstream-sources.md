# Upstream inspiration sources

Classifications use fast triage: `inspiration-source` means the skill text credits the source as the origin of its content; implementation pointers, tools, documentation/resource links without origin-credit, and example URLs are `incidental-link`.

## Confirmed seed sources

| Skill | Source | Classification | Evidence / decision |
|---|---|---|---|
| humanizer | `blader/humanizer` | inspiration-source | `SKILL.md` credits the original skill to @blader. Tracked in JSON. |
| humanizer | Wikipedia:Signs of AI writing | inspiration-source | The Wikipedia API resolves the title to page ID 75478314 (`Wikipedia:Signs of AI writing`), confirming this page exists. `SKILL.md` says the guide is based on it. Tracked in JSON. |
| react-useeffect | `reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md` | inspiration-source | README says skill is based on official React documentation and lists this guide. Tracked in JSON. |
| agent-md-refactor | Matt Pocock post | inspiration-source | README explicitly says based on the post. Unversioned citation tracked in JSON. |
| domain-name-brainstormer | Lenny's Newsletter | inspiration-source | SKILL.md says inspired by Ben Aiad's use case. Unversioned citation tracked in JSON. |
| repository | `softaworks/agent-toolkit` | inspiration-source | Required whole-repository upstream seed; tracked in JSON. |

## Additional scan classifications

| Skill | Source | Classification | Evidence / decision |
|---|---|---|---|
| writing-clearly-and-concisely | `joshuadavidthomas/agent-skills:writing` | inspiration-source | README credits the original skill to the author/repository; the upstream directory is `writing/` (the `writing-clearly-and-concisely/` directory does not exist). Tracked as `github-path`. |
| reducing-entropy | `joshuadavidthomas/agent-skills:reducing-entropy` | inspiration-source | README credits the original skill; upstream directory is `reducing-entropy/`. Tracked as `github-path`. |
| crafting-effective-readmes | `joshuadavidthomas/agent-skills:crafting-effective-readmes` | inspiration-source | README credits the original skill; upstream directory is `crafting-effective-readmes/`. Tracked as `github-path`. |
| writing-clearly-and-concisely | `obra/the-elements-of-style` | inspiration-source | README says adapted from it. Tracked in JSON (candidate flagged in brief). |
| session-handoff | `castocolina/agent-toolkit` | incidental-link | README links to test support/scenarios, not content origin. |
| skill-judge | `agentskills/agentskills` | incidental-link | README references the specification this skill evaluates; not credited as originating the skill content. |
| dependency-updater | listed CLI/tool repositories | incidental-link | Tool alternatives, not content origins. |
| mermaid-diagrams, marp-slide, mui, draw-io, c4-architecture, gemini, jira, pr-diagrams, meme-factory, design-system-starter | documentation/tool URLs | incidental-link | Resource, product, API, or usage links rather than origins of skill content. |
| remaining scanned skill URLs/examples | placeholder/example URLs and operational references | incidental-link | No source-origin credit found in SKILL.md or README.md. |

No seed was omitted: `rg` confirmed each credited seed in the respective skill. The broader scan found no additional origin-credit sources beyond those listed above; generic documentation, tools, and unrelated operational links were classified incidental.

## Audit results and proposed decisions

The source audit was run as requested. Staleness is relative to the last local change recorded by the audit. Each decision below is **proposed: user may override**.

| Skill/source | Result | Proposed decision and one-line reason |
|---|---|---|
| humanizer / `blader/humanizer` | current | ignore — source commit `2026-10-28T07:17:33Z` is older than local skill commit `2026-10-28T17:40:37-03:00`; no newer change to inspect. |
| humanizer / Wikipedia:Signs of AI writing | current | ignore — latest revision `2026-10-27T23:56:47Z` predates local skill commit `2026-10-28T17:40:37-03:00`; confirmed page ID 75478314. |
| react-useeffect / React guide path | current | ignore — path commit `2025-11-10T19:22:50Z` predates local skill commit `2026-01-21T19:30:06-03:00`. |
| agent-md-refactor / Matt Pocock post | unversioned | ignore — no reliable machine-readable update date is available for the citation. |
| domain-name-brainstormer / Lenny's Newsletter | unversioned | ignore — no reliable machine-readable update date is available for the citation. |
| repository / `softaworks/agent-toolkit` | current | ignore — merge-base `011baf4acea99174acb5486a9b662a7e084be63b` and latest `main` commit share the same timestamp; no newer commits exist on upstream main. |
| writing-clearly-and-concisely / `joshuadavidthomas/agent-skills:writing` | stale | update — commit `516dee7a` (2026-07-20), “consolidate writing skills,” changes the upstream skill structure and combines writing skills. The local source was last changed 2026-01-18; inspect the consolidated material for selective adaptation. |
| reducing-entropy / `joshuadavidthomas/agent-skills:reducing-entropy` | stale | ignore — path-specific API reports only `dd2ead06` (2026-02-18), moving skill directories to repo root; it is structural, not a change to the referenced entropy guidance. |
| crafting-effective-readmes / `joshuadavidthomas/agent-skills:crafting-effective-readmes` | stale | update — `dd2ead06` (2026-02-18) moved skill directories, and `eb7b6b9a` (2026-08-11) rewrote the README for multi-harness use and added `everyharness.yaml`; the changed README `style-guide.md` warrants comparison before porting. |
| writing-clearly-and-concisely / `obra/the-elements-of-style` | stale | ignore — path commit `c3643382` (2025-10-18) created the skill and moved `elements-of-style.md`; latest relevant content commit `58aa887d` (2025-10-13) streamlined the Elements of Style text. |

### Candidate fixes for Task 5

These are proposals, not user-approved updates:
- writing-clearly-and-concisely: review upstream `writing/SKILL.md` at `516dee7a` (“consolidate writing skills,” 2026-07-20) against the local skill; decide whether to adapt any consolidated writing guidance.
- reducing-entropy: ignore upstream `dd2ead06` (2026-02-18) for Task 5; it only moved directories to repository root and did not change entropy guidance.
- crafting-effective-readmes: review the upstream style guide change at `eb7b6b9a` (2026-08-11, multi-harness README rewrite and everyharness metadata) and compare the moved `crafting-effective-readmes/style-guide.md` before deciding what to port.

The upstream audit command completed successfully after adding a Wikipedia User-Agent. No skill content was changed. The base-to-main repository compare reported `identical` (0 commits, 0 files), so there was no repo diff to review.
