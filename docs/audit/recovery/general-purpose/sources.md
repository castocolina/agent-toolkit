# Sources: general-purpose (agent)

Checked 2026-11-15.

## Origins found

1. softaworks/agent-toolkit, `agents/general-purpose.md` at `3027f20f`: byte-identical in body to the baseline `dbff837f` (name, description, `model: default`, `color: blue`, then the sections General Purpose Agent, Behavioral Mindset, Focus Areas, Key Actions, Outputs, Boundaries). No credit line for it in softaworks' README (it has none at `3027f20f`) and none in this repo's root `README.md` (it lists general-purpose only in the agents table).
2. Structure, not text: the heading set Behavioral Mindset / Focus Areas / Key Actions / Outputs / Boundaries (Will, Will Not) is the agent-file template of SuperClaude-Org/SuperClaude_Framework (MIT, `gh`-style license check via GitHub API: spdx MIT; its `security-engineer.md` has exactly these headings). I did not find a `general-purpose` agent in that repo, and the same description line is mirrored on third-party listings (aitmpl.com, vibehackers.io, skillselion.com, claudecowork.im) with no author given, so the text origin is softaworks (or an earlier template user); I could not confirm authorship.
3. The current file shares none of the baseline's phrases (`recovery inventory` phrase fate: 0% kept, 0% moved, 100% gone, 100% new). It is our own rewrite, so no upstream text is carried; the only inheritance is the section idea of a coordinator that delegates.
4. Vendor docs it follows (frontmatter values, built-in agent, subagent context isolation, tool allowlists): Claude Code docs, Create custom subagents.

## Missing credit line

None required for text: nothing of the SuperClaude or softaworks wording survives, and the softaworks fork carries no credit line to preserve. Optional, if the controller wants provenance for the baseline's origin: add to the root `README.md` "Agent credits:" paragraph, exact text:

`general-purpose began as the softaworks/agent-toolkit agent of that name (https://github.com/softaworks/agent-toolkit/blob/main/agents/general-purpose.md), whose section layout follows the SuperClaude Framework agent template (MIT); the current text is a rewrite, and its subagent facts follow Anthropic's Claude Code documentation (Anthropic).`

Do not add it if the coordinator prefers credits only for surviving text; the other agents in that paragraph (mermaid-diagram-specialist, communication-excellence-coach, codebase-pattern-finder) credit upstreams whose text the file still carries or follows.

## Proposed registry rows (docs/audit/upstream-sources.json)

The existing row (`skill: general-purpose`, `kind: local`, `artifact_kind: agent`) stays only if no row below is added; `local` rows mean "no upstream", and docs are an upstream for the facts. Proposed additions (same shape as the existing `ui-ux-designer` and `mermaid-diagram-specialist` rows):

```json
{
  "skill": "general-purpose",
  "kind": "unversioned",
  "source": "Claude Code docs, Create custom subagents (frontmatter, built-in general-purpose agent, context isolation): https://code.claude.com/docs/en/sub-agents",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "agent"
}
```

Optional second row for the template origin (only if the optional credit line above is added):

```json
{
  "skill": "general-purpose",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:agents/general-purpose.md",
  "ref": "main",
  "credit": "softaworks (agent-toolkit), template after SuperClaude-Org/SuperClaude_Framework (MIT)",
  "artifact_kind": "agent"
}
```

`validate_entry` shape: `github-path` needs `owner/repo:path` and a non-empty `ref`; `unversioned` needs a non-empty title and URL and `ref` null. I did not run `validate_entry` on these (no registry edit made).

## skill-updater style review (REVIEW ONLY, no `track` call, no registry edit)

- Step 1: scope `agents/general-purpose.md` exists, not synced.
- Step 2: only a `kind: local` row exists, so there is no upstream diff to read; `upstreams` was not run (it skips `local` rows). A credit line naming an upstream does not exist; origin 1 above is a proposed row, not a `track` call.
- Step 6 model-validity pass: the file has no rule that counters a model habit (no banned words, substitutions or suppressions); its rules are coordination rules (owner per requirement, gates, retry caps, serialize commits). No probe run; keep all.
- Adopt / adapt / ignore items for the restore brief:
  - adapt: the baseline's Outputs line "Delegation decisions and rationale" into the Done-and-output Result section (who did each subtask, directly or by which specialist, and why), keeping the current four-section format.
  - ignore: baseline "Progress updates" (a one-shot subagent returns one final report), "Ignore specialist availability" (deliberately reversed in Process step 3), and "Make assumptions about requirements" (replaced by the record-as-assumption rule in step 1).
  - adapt (fact): House rules "a subagent cannot prompt the user" to "a subagent cannot ask the user questions" (see facts.md, corrected row).
- Step 8: the agent changes (restore), so it is judged in Step 7 of the plan.

## Docs pages used (proposed `unversioned` rows)

- Claude Code docs, Create custom subagents: https://code.claude.com/docs/en/sub-agents (the registry row above). The last 16,580 characters of that page were not read (page is 116,580 characters; the fetch covered the first 100,000); the facts used all came from the covered part.
