# Sources: codebase-pattern-finder (agent)

Checked 2026-11-15.

## Origins found

1. HumanLayer, `humanlayer/humanlayer` (Apache-2.0, `gh api repos/humanlayer/humanlayer/license`), file `.claude/agents/codebase-pattern-finder.md`. The baseline `dbff837f` file is byte-identical to that file at commit `f3478b88ba0d3a91166b2f8e5908714f865fd43f` (2025-10-04, "Update sub-agents to use sonnet model"): `diff` of the two outputs is empty (checked with `gh api ...contents/...?ref=f3478b88...` against `git show dbff837f:agents/codebase-pattern-finder.md`). The same text is in npm `humanlayer@0.17.2` (https://unpkg.com/humanlayer@0.17.2-npm/.claude/agents/codebase-pattern-finder.md).
2. softaworks/agent-toolkit, `agents/codebase-pattern-finder.md` at `3027f20f`: identical to the baseline (the baseline is the unmodified fork), so softaworks is the route the text reached this repo by. Its README has no credit line for this agent (`git grep` of `3027f20f` finds none).
3. The HumanLayer file was removed from `main` on 2026-10-22 (commit `d8197bab`, "HumanLayer: the desktop app, daemon, CLI, web UI, API, and plugins"). The prompt now lives in `apps/riptide-daemon/src/agents/claudecode/agents/codebase-pattern-finder.ts` with the same text and tools `Grep, Glob, Read, Bash, Skill`; `LS` is gone from the tool list, though the prompt text still mentions it.
4. No other distinctive uncredited origin: the current file's body (Never, Procedure, Gotchas) is our own rewrite.

## Missing credit line

The root `README.md` agent-credit paragraph has no sentence for this agent; the registry row is `kind: local`, which says "no upstream" and is wrong. Add this sentence to the "Agent credits:" paragraph (after the mermaid-diagram-specialist one), exact text:

`codebase-pattern-finder is adapted from [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer/blob/f3478b88ba0d3a91166b2f8e5908714f865fd43f/.claude/agents/codebase-pattern-finder.md) by HumanLayer (Apache-2.0), through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/agents/codebase-pattern-finder.md); its tool and model facts follow Anthropic's Claude Code documentation (Anthropic).`

The commit-pinned link is used because the path no longer exists on `main`.

## Proposed registry rows (docs/audit/upstream-sources.json)

All four pass `validate_entry` (checked with a throwaway script). The existing `kind: local` row for this agent (`"skill": "codebase-pattern-finder", "kind": "local"`) should be removed when these are added: a local row says the artifact has no upstream. The HumanLayer row keeps `source` at the original path and points `new_path` at the TypeScript port, the skill-updater `path-moved` shape, so `upstreams` follows the live file.

```json
{
  "skill": "codebase-pattern-finder",
  "kind": "github-path",
  "source": "humanlayer/humanlayer:.claude/agents/codebase-pattern-finder.md",
  "ref": "main",
  "credit": "HumanLayer",
  "artifact_kind": "agent",
  "new_path": "apps/riptide-daemon/src/agents/claudecode/agents/codebase-pattern-finder.ts"
}
```

```json
{
  "skill": "codebase-pattern-finder",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:agents/codebase-pattern-finder.md",
  "ref": "main",
  "credit": "softaworks",
  "artifact_kind": "agent"
}
```

```json
{
  "skill": "codebase-pattern-finder",
  "kind": "unversioned",
  "source": "Claude Code docs, Create custom subagents (https://code.claude.com/docs/en/sub-agents)",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "agent"
}
```

```json
{
  "skill": "codebase-pattern-finder",
  "kind": "unversioned",
  "source": "Claude Code docs, Tools reference (https://code.claude.com/docs/en/tools-reference)",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "agent"
}
```

## skill-updater style review (review only, no `track` call, `upstreams` not run)

Step 2 of the skill: the only row is `kind: local` but a credit-worthy upstream exists, so the row is proposed above and no `track` call is made.

Upstream compare: the HumanLayer prompt at `f3478b88` equals the baseline; the live TypeScript port has the same prompt text, only the tool list changed (`LS` removed, `Bash` and `Skill` added) and the `description` is the same.

- adopt: drop `LS` from `tools` (documented non-tool; the upstream port also removed it). Keep it read-only: do not add `Bash`.
- ignore: the `Bash` and `Skill` additions in the TypeScript port (the agent is a read-only delegate; the current description says it never writes), and the whole upstream prompt body (our rewrite is a deliberate, judged replacement; no upstream change since the baseline).
- adapt (optional, small): the Gotcha "Grep respects `.gitignore`" can add that Glob lists gitignored files by default (tools reference), a real way to reach hidden generated code.
- Model-validity pass: the rules that counter a model habit (never evaluate, verbatim quotes, re-Read before reporting) are still sound for current Sonnet; the removed "think deeply" and filler lines need no restoring. No model ID is hardcoded (`sonnet` is an alias).
- Restore brief: no `restore-*` rows and no `drop-pending` restore needed if the controller accepts the s007 DROP verdict; if it overrules, restore the worked example only as an output-format example with a clearly fictional marker, into the agent file.
