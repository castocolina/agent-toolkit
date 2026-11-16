# Sources: gepetto (skill, synced, report-only)

Checked 2026-11-16. Analyst review only: no `track` call, no skill-updater run, no edit of the skill, the registry or README.md. Nothing under `skills/gepetto` was touched.

## Origins found

1. **Sync source: softaworks/gepetto** (MIT, default branch `main`, last push 2026-01-22, not archived). `.github/workflows/sync-gepetto.yaml` (present in this repo, daily cron) clones it, replaces `skills/gepetto/` with `gepetto/skills/gepetto/` and copies the repo-root `README.md` into the skill directory. All seven synced files (`SKILL.md`, the five `references/*.md`, `README.md`) are byte-identical to the current upstream `main` (compared through `gh api contents/...` on 2026-11-16). The last sync commit here is `e6077cf7` (github-actions[bot], 2026-01-23), after the upstream's last push, so the copy is current.
2. **Origin of the softaworks copy (baseline): softaworks/agent-toolkit at `3027f20f`.** `git diff --stat 3027f20f -- skills/gepetto skills/datadog-cli` is empty, so the softaworks original (`git show 3027f20f:skills/gepetto/SKILL.md`) equals the current SKILL.md. History of the skill here: `a0d85e8a` (Leonardo Flores, 2026-01-19, README sync), `859211cf` (2026-01-20) and `e6077cf7` (2026-01-23), both bot syncs.
3. **Tools and products the skill drives (vendor sources for facts.md):** Claude Code (Task/Agent tool, TodoWrite, AskUserQuestion, plugin commands), Gemini CLI and Gemini API model ids, Codex CLI and its model catalog, the `ralph-loop` plugin of anthropics/claude-plugins-official, and Ralphy (michaelshimeles/ralphy).
4. No other origin was found for the text itself: the credit lines name only Leonardo Flores and `softaworks/gepetto`. A web search on distinctive phrases was not run, because the upstream repository is the stated origin and the text is identical to it.

## Credit line

Present and untouched: `skills/gepetto/README.md` lines 481-483 (`**Crafted by:** Leonardo Flores`, `**License:** MIT`, `**Repository:** https://github.com/softaworks/gepetto`). The root `README.md` lines 3 and 5 credit @leonardocouy and softaworks/agent-toolkit for the repository as a whole. Nothing edited or proposed for removal.

## Registry state (docs/audit/upstream-sources.json)

- `rg -i "gepetto"` over the file finds no row; the `upstreams` output (read-only, run 2026-11-16) has no `gepetto` row either. The only row that covers the skill indirectly is the repo row `{skill: null, kind: repo, source: softaworks/agent-toolkit, ref: main}` (merge_base `3027f20f`, stale false).
- The `upstreams` exit code was 1 on 2026-11-16, caused by rows of other artifacts only (`crafting-effective-readmes` / `webern/cargo-readme`, HTTP 404; a stale `humanizer` Wikipedia row). None is a gepetto row.
- Stale sources of this skill: none. Synced files equal upstream (2026-11-16). One note: the README's marketplace repository `softaworks/agent-skills` has been renamed to `softaworks/agent-toolkit` (GitHub API returns `full_name softaworks/agent-toolkit` for the old name); it is recorded as a stale fact in facts.md, not as a stale source.

## Proposed registry rows (the controller applies them; I did not edit docs/audit/upstream-sources.json)

Required by the brief: `unversioned` rows for the vendor docs pages used (`upstreams` reports `stale: false` for them, so the date in facts.md is the age marker).

```json
{"skill": "gepetto", "kind": "unversioned", "source": "Claude Code docs, Tools reference (Agent, TodoWrite, AskUserQuestion, WebSearch, WebFetch): https://code.claude.com/docs/en/tools-reference", "ref": null, "credit": "Anthropic"}
{"skill": "gepetto", "kind": "unversioned", "source": "Claude Code docs, Create custom subagents (Task renamed to Agent in 2.1.63, Explore): https://code.claude.com/docs/en/sub-agents", "ref": null, "credit": "Anthropic"}
{"skill": "gepetto", "kind": "unversioned", "source": "Claude Code docs, Install and manage plugins (plugin marketplace add, plugin install, enable): https://code.claude.com/docs/en/discover-plugins", "ref": null, "credit": "Anthropic"}
{"skill": "gepetto", "kind": "unversioned", "source": "Gemini CLI docs, CLI reference (-m, --approval-mode, -p): https://geminicli.com/docs/cli/cli-reference/", "ref": null, "credit": "Google"}
{"skill": "gepetto", "kind": "unversioned", "source": "Gemini CLI docs, Model selection: https://geminicli.com/docs/cli/model/", "ref": null, "credit": "Google"}
{"skill": "gepetto", "kind": "unversioned", "source": "Gemini API docs, Deprecations (gemini-3-pro-preview): https://aistudio.google.com/docs/deprecations", "ref": null, "credit": "Google"}
{"skill": "gepetto", "kind": "unversioned", "source": "Gemini API docs, Models: https://aistudio.google.com/docs/models", "ref": null, "credit": "Google"}
{"skill": "gepetto", "kind": "unversioned", "source": "OpenAI API docs, Deprecations (gpt-5.2 family): https://developers.openai.com/api/docs/deprecations", "ref": null, "credit": "OpenAI"}
{"skill": "gepetto", "kind": "unversioned", "source": "Codex docs, CLI command reference (codex exec flags): https://developers.openai.com/codex/cli/reference", "ref": null, "credit": "OpenAI"}
{"skill": "gepetto", "kind": "unversioned", "source": "ralph-loop plugin, stop hook and /ralph-loop command (exact promise match): https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop", "ref": null, "credit": "Anthropic"}
{"skill": "gepetto", "kind": "unversioned", "source": "Ralphy README (engines, flags, defaults): https://github.com/michaelshimeles/ralphy/blob/main/README.md", "ref": null, "credit": "Michael Shimeles (michaelshimeles)"}
{"skill": "gepetto", "kind": "unversioned", "source": "npm registry, add-skill (deprecated, renamed to skills): https://www.npmjs.com/package/add-skill", "ref": null, "credit": "Vercel Labs"}
```

Note on the Codex row: `https://developers.openai.com/codex/cli/reference` answers a 308 redirect to `https://learn.chatgpt.com/docs/developer-commands?surface=cli` (checked 2026-11-16); the registry may carry either URL. The tool's own output (`codex exec --help`, `codex debug models`, codex-cli 0.162.1 installed here) was the primary source for the Codex facts and needs no row.

Optional, not required by the brief (the controller decides; `track` refuses synced skills, so this would only feed `upstreams`): a row for the sync source in the `github` shape the registry already uses.

```json
{"skill": "gepetto", "kind": "github", "source": "softaworks/gepetto", "ref": "main", "credit": "Leonardo Flores (@leonardocouy)"}
```

`validate_entry` was not run on this proposal (the registry was not touched); check it before applying.

## Stale source dates

| source | state | date checked |
|---|---|---|
| softaworks/gepetto (sync source) | not stale: all 7 synced files byte-identical to `main` | 2026-11-16 |
| softaworks original at `3027f20f` | identical to current files | 2026-11-16 |
| softaworks/agent-skills (README marketplace name) | renamed to softaworks/agent-toolkit; old name redirects | 2026-11-16 |
