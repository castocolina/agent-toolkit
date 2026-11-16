# Sources: writing-clearly-and-concisely

Checked 2026-11-15. Review only: no `track` call, no registry edit, no artifact edit. `upstreams` was run read-only for the whole registry; the two rows of this skill returned `error: null`, `stale: false` (a timestamp signal only: neither row has `last_upstream_sha`, so the current upstream was read against the artifact, below).

## Origins found

1. **softaworks/agent-toolkit, `skills/writing-clearly-and-concisely`** (fork point `3027f20f`). The skill's SKILL.md, README.md and `elements-of-style/` files at the fork point are the same package as the baseline `dbff837f` (the README at `3027f20f` is byte-for-byte the baseline README). The `repo` row (`softaworks/agent-toolkit`, `skill: null`) already covers the fork origin; no per-skill row is needed.
2. **joshuadavidthomas/agent-skills** (MIT, GitHub licence field MIT), the author credited in the README ("Original skill by @joshuadavidthomas"). Registry row exists: `github-path` `joshuadavidthomas/agent-skills:writing`, `ref` `main`, credit `@joshuadavidthomas`. Finding: upstream commit `516dee7a` (2026-07-20, "consolidate writing skills") removed `writing-clearly-and-concisely/` (SKILL.md, the five `elements-of-style/` files, `signs-of-ai-writing.md`) and `ai-writing-tropes/` and added the Orwell-based `writing/` skill, so the registered path is the successor, not our ancestor. Our skill's own text therefore no longer has a live upstream copy at that author; the row is still the right pointer (it is where the author's current thinking lives) and the credit line is correct.
3. **obra/the-elements-of-style** (no GitHub licence field; its `elements-of-style.md` is headed "Public domain text by William Strunk Jr."). Registry row exists: `github`, `ref` `main`, credit `obra/the-elements-of-style`. README says "Adapted from". Upstream (pushed 2026-08-12) is now a multi-harness plugin repository whose `skills/writing-clearly-and-concisely/` holds a SKILL.md close to the baseline and a single 995-line `elements-of-style.md`. A line-set comparison of that file against our five files finds, outside the table of contents and one wrapped line, only our two local edits (Shall, Will; They) and Section IV, which obra omits.
4. **Project Gutenberg ebook 37134, The Elements of Style by William Strunk Jr. (1869-1946), "Public domain in the USA".** The only origin for `elements-of-style/04-a-few-matters-of-form.md` (a stray Gutenberg anchor survives in the file) and the root of every `elements-of-style/` file. Not credited anywhere in the skill and not in the registry.
5. **Wikipedia:Signs of AI writing** (WikiProject AI Cleanup, CC BY-SA 4.0), the source of `signs-of-ai-writing.md`. The README credits it with the licence and a link, but the registry has no row for this skill (the only `wikipedia` row belongs to `humanizer`, tracked at revision 1383638008). The live page is revision 1385890265 (2026-11-15) and has been restructured (facts.md), so our file is a stale snapshot.
6. No other distinctive uncredited text: the hard cases, checkpoints and eval fixtures are this repository's own work (plan 8 rewrite of 2026-10-29 and 2026-11-06).

## Credit lines

Existing credit lines are intact and must not be reworded: `@joshuadavidthomas`, `joshuadavidthomas/agent-skills`, `obra/the-elements-of-style`, `William Strunk Jr.`, `WikiProject AI Cleanup` and the CC BY-SA 4.0 link all appear in `skills/writing-clearly-and-concisely/README.md`, so `credit_issues` (`missing_credit`) passes for the two current rows and for the rows below that reuse them.

Missing, to add as new bullets at the end of the README `## Attribution` list (a new line each, never rewording an existing bullet):

```text
- The public-domain text of *The Elements of Style* in `elements-of-style/` comes from [Project Gutenberg ebook 37134](https://www.gutenberg.org/ebooks/37134) by William Strunk Jr. (public domain in the USA), as packaged by obra/the-elements-of-style. Two entries in `elements-of-style/05-words-and-expressions-commonly-misused.md` (Shall, Will; They) are replaced by modern-usage notes; the original wording is in the Gutenberg text.
- `signs-of-ai-writing.md` is a snapshot of Wikipedia:Signs of AI writing as copied earlier; the live page has since been restructured. Wikipedia text is licensed CC BY-SA 4.0 under the Wikimedia Foundation Terms of Use.
- HTTP status examples (`401`, `403`, `409 Conflict`) follow RFC 9110 (IETF).
```

These bullets carry the strings `Project Gutenberg`, `Wikimedia Foundation` and `IETF` that the credit check needs for the proposed rows 3-5 below. Optional, for the restore brief only: a two-line provenance banner at the top of `signs-of-ai-writing.md` (source URL, CC BY-SA 4.0, snapshot note), because agents read that file standalone and BY-SA asks that a reuse state its source, licence and changes.

## Proposed registry rows (docs/audit/upstream-sources.json)

Origin rows (the two existing rows stay as they are; these are new):

```json
{"skill": "writing-clearly-and-concisely", "kind": "wikipedia", "source": "Wikipedia:Signs of AI writing", "ref": null, "credit": "WikiProject AI Cleanup"}
{"skill": "writing-clearly-and-concisely", "kind": "unversioned", "source": "Project Gutenberg, The Elements of Style by William Strunk (public domain in the USA): https://www.gutenberg.org/ebooks/37134", "ref": null, "credit": "William Strunk Jr."}
```

Docs pages used for facts.md (each `unversioned`; `upstreams` never reports these stale, so only a `skill-updater` run re-reads them). Each needs its credit text in the README, which the bullets above supply:

```json
{"skill": "writing-clearly-and-concisely", "kind": "unversioned", "source": "Wikimedia Foundation, Terms of Use (CC BY-SA 4.0 licensing of Wikipedia text): https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use", "ref": null, "credit": "Wikimedia Foundation"}
{"skill": "writing-clearly-and-concisely", "kind": "unversioned", "source": "IETF, RFC 9110 HTTP Semantics (status codes 401, 403, 409): https://www.rfc-editor.org/rfc/rfc9110.html", "ref": null, "credit": "IETF"}
```

If the coordinator prefers fewer rows, rows 3 and 4 (Wikimedia ToU, RFC 9110) can be dropped together with their README bullets, since the 401/403/409 codes are illustrative; rows 1 and 2 are the provenance rows that matter. The `wikipedia` row needs no `last_upstream_sha` until the snapshot is refreshed; once refreshed, set it to the revision copied (current: 1385890265).

## skill-updater review (REVIEW ONLY)

Reasoning only; nothing is tracked, edited or written to `docs/audit/<date>/updates.md` by this analyst.

Row `joshuadavidthomas/agent-skills:writing` (`github-path`): the contents test passes (`writing/` holds `README.md`, `SKILL.md`, `references/`). The consolidated `writing` skill is Orwell-based (ten rules from "Politics and the English Language", a reader-first section, a tropes field guide), not Strunk-based. Items:

| upstream item | decision | one-line reason |
| --- | --- | --- |
| Orwell rules 1, 2 (no stock figures, short word over long: "use" not "utilize", "is" not "serves as") | ignore | Edit step 1 already cuts puffery and "serves as" patterns, and a capable model substitutes short words unprompted. |
| Rule 5 (swap jargon for everyday words) | ignore | Contradicts our NEVER ("deprecated" is not "old", "idempotent" is not "safe"); upstream itself carves out exact technical terms. |
| Rule 6 (positive form), rule 7 (concrete language) | ignore | Both conflict with the invariant and claims checkpoints (a positive rewrite can flip a negation; concreteness can invent a fact); a deliberate local divergence recorded in record.md s006 and s013. |
| The swap test ("could this sentence appear unchanged in another project's README?") | adapt, optional | A cheap test for Flag and Draft that fits Edit step 1 (cut what carries no invariant); port as one clause only if the coordinator wants it; not required. |
| "Write for the reader" (what they know, what they came for; one piece, one need) | ignore | Audience design belongs to professional-communication; this skill is copyedit and short drafts under the checkpoints. |
| "Match tone to stakes" | ignore | Covered by Edit step 1 (puffery) and by the humanizer catalog (stakes inflation); not a clarity-edit rule. |
| The tells table and `references/tropes.md` | ignore | Duplicates `signs-of-ai-writing.md` and the humanizer pattern catalog; tropes.md ships under a separate zlib licence (`LICENSE-tropes`, from Xe Iaso's site), which would have to travel with it. |
| `references/politics-and-the-english-language.md` | ignore | Full essay, outside this skill's purpose; its licence status in the US was not checked, so do not import it. |
| "Before delivering" checklist | ignore | Our Invariant and Claims checkpoints do this with sharper tests. |
| New skill `writing-error-messages` (upstream) | ignore | Our Draft branch rule 2 already covers error messages (quote the identifier, name the fix, `Needs: remediation`); not diffed in depth. |

Row `obra/the-elements-of-style` (`github`): the repository now carries the same skill name with a single-file `elements-of-style.md`, plugin manifests for many harnesses and a `Public domain text by William Strunk Jr.` line.

| upstream item | decision | one-line reason |
| --- | --- | --- |
| Single 995-line `elements-of-style.md` with a "consumes about 12,000 tokens" warning | ignore | Our five-file split lets the load list read one section; the split is the point of the Reference load list. |
| "Public domain text by William Strunk Jr." line | adopt | Port the statement into the README Attribution (credit lines above); this repository never states the public-domain status. |
| Unedited Shall, Will and generic-he prescriptions | adapt | Keep our two disclosed replacements (record.md s083, s084) and name the difference in the README, as the first credit bullet does. |
| Multi-harness manifests (`.codex-plugin`, `.cursor-plugin`, and so on) | ignore | Distribution, not content; this repository builds its own plugins. |
| SKILL.md description "Apply Strunk's timeless writing rules to ANY prose" | ignore | Our narrower description with exclusions is the audited one. |

Model-validity pass: not run. It needs a probe lane (`pi-cmd runner`), which this analyst may not call; the rules in this skill that counter a model habit are the puffery and `-ing` tail cuts (Edit step 1) and the invented-actor and invented-figure guards (claims checkpoint). The evals in `evals/evals.json` already exercise them, so the coordinator can run the pass at the Step 4 review if it wants a probe on record.

Step 8 (judge on change) applies at Step 7 of the batch, not here.

## Adopt and adapt items for the restore brief

- adopt: README Attribution bullets above (public-domain statement with the Gutenberg link, disclosure of the two edited entries, snapshot and Wikimedia ToU note, RFC 9110 note). Credits already present are untouched.
- adapt, from facts.md row "its Markup, Citations and AFC sections": SKILL.md load list row 5 wording to "its Markup and Citations sections and the AFC-draft subsections: Wikipedia-only" (the local file has no `##` AFC section).
- adapt, optional: the swap test as one clause in Edit step 1.
- optional, no restore row requires it: name Strunk in the SKILL.md description or Reference note so that "apply Strunk" queries match (record.md s017, s021 found his name only in the README and "1918 prescriptions").
