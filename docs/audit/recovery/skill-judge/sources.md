# skill-judge sources (plan 14, batch 14, checked 2026-11-15)

## Origins found

1. **shareAI-lab/lab-skills (Apache-2.0), the original author.** The softaworks skill at `3027f20f` (`skills/skill-judge/SKILL.md`, 752 lines) is byte-identical to the shareAI-lab file added on 2026-01-04 (`cf01f0cb`, "up skill judge skill"; `diff` of the two files lists 0 differing lines), 15 days before softaworks committed it (`40d4469f`, 2026-01-19, Leonardo Flores). The repo was `shareAI-lab/shareAI-skills` and is now `shareAI-lab/lab-skills` (GitHub redirects). Kode-CLI's `packages/builtin-skills/THIRD_PARTY_NOTICES.md` also lists `skill-judge/` under "ShareAI Skills (Apache-2.0)". The skill now lives at `agent-development/skill-judge` (moved by `c2fc86e5` and `0e1c561c`, 2026-08-14). Current repo head: `becee99823c8263da3e8d9f1dfac5745f1d81d70`. No credit line exists in `skills/skill-judge/README.md`, `SKILL.md` or `references/` at the baseline or now, and `docs/audit/upstream-sources.json` has no row with `skill: skill-judge`.
2. **softaworks/agent-toolkit** (fork point, Leonardo Flores / @leonardocouy). Upstream `skills/skill-judge` has one commit, `40d4469f` (2026-01-20 UTC), the fork-point text; nothing changed there since.
3. **Anthropic example skills** (anthropics/skills, Apache-2.0 per the Kode-CLI notice and the repo): the old pattern table and examples are named after and modeled on frontend-design, internal-comms, canvas-design, mcp-builder, docx, pdf and xlsx. The restored exemplar list names them, so the credit is needed.
4. **Agent Skills specification** (agentskills.io, CC-BY-4.0): the vendored mirror in `references/agentskills/` is pinned by its own `SOURCE.json`; that file is the provenance for the mirror and `agentskills-research` owns refreshing it. No registry row exists for the artifact.
5. **Claude Code documentation** (Anthropic): `references/claude-code/SOURCE.json` pins three pages; the profiles' field lists come from them. No registry row exists for the artifact.

## Proposed registry rows (docs/audit/upstream-sources.json, add by hand; the controller edits the file)

```json
{
  "skill": "skill-judge",
  "kind": "github-path",
  "source": "shareAI-lab/lab-skills:agent-development/skill-judge",
  "ref": "main",
  "credit": "shareAI-lab/lab-skills (Apache-2.0), via softaworks/agent-toolkit"
}
```

```json
{
  "skill": "skill-judge",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/skill-judge",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

```json
{
  "skill": "skill-judge",
  "kind": "unversioned",
  "source": "Anthropic example skills (frontend-design, internal-comms, canvas-design, mcp-builder, docx, pdf, xlsx): https://github.com/anthropics/skills",
  "ref": null,
  "credit": "Anthropic"
}
```

```json
{
  "skill": "skill-judge",
  "kind": "unversioned",
  "source": "Agent Skills specification (https://agentskills.io/specification)",
  "ref": null,
  "credit": "Agent Skills (agentskills.io)"
}
```

```json
{
  "skill": "skill-judge",
  "kind": "unversioned",
  "source": "Claude Code docs, Extend Claude with skills (https://code.claude.com/docs/en/skills)",
  "ref": null,
  "credit": "Anthropic"
}
```

```json
{
  "skill": "skill-judge",
  "kind": "unversioned",
  "source": "Claude Code docs, Create custom subagents (https://code.claude.com/docs/en/sub-agents)",
  "ref": null,
  "credit": "Anthropic"
}
```

```json
{
  "skill": "skill-judge",
  "kind": "unversioned",
  "source": "Pandoc User's Guide, --track-changes (https://pandoc.org/MANUAL.html)",
  "ref": null,
  "credit": "John MacFarlane (pandoc)"
}
```

```json
{
  "skill": "skill-judge",
  "kind": "unversioned",
  "source": "PyMuPDF documentation, Document.authenticate and needs_pass (https://pymupdf.readthedocs.io/en/latest/document.html)",
  "ref": null,
  "credit": "Artifex (PyMuPDF)"
}
```

```json
{
  "skill": "skill-judge",
  "kind": "unversioned",
  "source": "PyPI project pages for the example packages: https://pypi.org/project/camelot-py/ and https://pypi.org/project/tabula-py/",
  "ref": null,
  "credit": "PyPI"
}
```

Notes on the rows: every `credit` text must appear verbatim in `SKILL.md`, `README.md` or `references/*.md` (`audit.py check --strict`, `missing_credit`). The first row's `ours_updated` reads `git log` on `SKILL.md` and `references/` (skill-updater step 3), which has commits, so no `no local commit` error is expected. The last three rows are only needed if the restored worked-examples file keeps the pandoc, PyMuPDF and PyPI package names; drop the matching row if the restore removes a name. `upstreams` never marks an `unversioned` row stale, so the facts table dates are the age signal.

## Missing credit lines (exact text to add)

Add to `skills/skill-judge/README.md`, near the end (the README is the right place for a skill; the root README has no credit paragraph for skills):

```text
Adapted from [shareAI-lab/lab-skills](https://github.com/shareAI-lab/lab-skills) (Apache-2.0) through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy. The rubric was rederived from the Agent Skills specification, and the pattern examples name skills from [anthropics/skills](https://github.com/anthropics/skills).

Registry credits for this skill: shareAI-lab/lab-skills (Apache-2.0), via softaworks/agent-toolkit; softaworks/agent-toolkit; Anthropic; Agent Skills (agentskills.io); John MacFarlane (pandoc); Artifex (PyMuPDF); PyPI.
```

The verbatim strings the check looks for are in the second paragraph. No existing credit line is touched (there is none).

## Skill-updater review (review only)

Method: the `upstreams` command has no `skill-judge` row to read, so the equivalent was done by hand with `gh api` (read-only). No `track` call was made and no file outside `docs/audit/recovery/skill-judge/` was written.

- Origin 2 (softaworks): no change since the fork point. Nothing to classify.
- Origin 1 (shareAI-lab/lab-skills): rewritten on 2026-08-14 from 752 lines to a 169-line `SKILL.md` plus a 203-line `references/rubric.md` that still uses 120 points and D7 Structural pattern fit (10). Classified against this artifact:

| upstream change | decision | reason |
| --- | --- | --- |
| Hard gates reported before scoring (invalid frontmatter, name mismatch, broken resource paths, advertised capabilities the package does not implement, unsafe scripts, contradictory requirements) | adapt | most are already D4, D5, D8 or source-check findings; the missing piece is "advertised capability not implemented"; it is a rubric change, so not a restore: list for plan 9's cycle |
| Advice "do not invent precise paragraph percentages when the boundary is ambiguous" | ignore | rubric v5 fixes the D1 good ratio (70/20/10) in lines on purpose; contradicts a repo ruling on reproducible scoring |
| Review depth modes (quick review, full audit, comparison, revision review) | ignore | skill-judge's output contract is fixed by the verdict schema; comparison is already covered in SKILL.md and revision review by the previous-version digest |
| Bad review pattern "evaluating an example link inside a fenced code block as a broken live link" | adapt | a real false-positive for the source check (rubric source check part 1 already excludes paths in the user's project, but not links shown as examples in code fences); candidate Gotcha for SKILL.md, a judge-text change outside this restore |
| Bad review patterns "recommending fewer files when separation protects context" and "recommending more files without a loading strategy" | ignore | already covered: rubric D5 says a reference kept in `references/` is never a defect and removals name a destination |
| D3 note: a prohibition should name the condition, the failure it prevents and a better action | adapt | consistent with rubric D3 (specific NEVER with reasons); worded as an author-facing example it fits the restored anti-pattern example pair, so the restore brief may phrase the NEVER example that way, with no rubric change |
| Grade bands, 120-point total, "What is already strong" output section, "treat the result as diagnostic, not certification" applicability | ignore | replaced by rubric v5 and the schema on purpose; the applicability caveat is a framing, not a rule |
| Description reframed to "opinionated, practice-derived rubric ... not official certification" | ignore | this artifact is judged against the pinned spec, and its description is set by plan 4 and 13 |

- Model-validity pass: not run. It needs a probe through the repo's tool-less referee lane (an LLM call), and the analyst brief forbids judging artifacts with an LLM lane. Rules that counter a model habit and would be probed: "NEVER reward polish, length or self-praise" and "When two scores seem equally defensible, pick the lower". The controller may run it with `pi-cmd runner --model <MODEL>`.
- Stale-source checks: the `anthropics/skills` examples the old text quoted have changed (docx description, frontend-design anti-pattern list); recorded in `facts.md` as `corrected`, so the restore must write neutral examples rather than quote upstream.

## Adopt and adapt items for the restore brief

- Adopt: none (no upstream change applies unchanged).
- Adapt: phrase the restored D3 NEVER example with its condition, failure and better action (upstream rubric D3 note); optionally add the fenced-link false-positive and the "advertised but not implemented" check as a later judge-text proposal, not in this restore.
