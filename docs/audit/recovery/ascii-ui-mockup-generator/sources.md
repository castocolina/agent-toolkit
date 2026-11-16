# Sources: ascii-ui-mockup-generator (agent)

Checked 2026-11-15. Analyst review only: no `track` call, no edit of the artifact, the registry or README.md.

## Origins found

1. **Immediate source: softaworks/agent-toolkit** `agents/ascii-ui-mockup-generator.md`. The file at fork point `3027f20f` and at baseline `dbff837f` is the same text (it entered this repo in `673fe769`, "feat: add 6 agents and 4 commands from claude-plugins", by Leonardo Flores, 2026-01-18). The README credits Leonardo Flores (@leonardocouy) for the sibling commands "via softaworks/agent-toolkit".
2. **Earliest public copy found: ayoubben18/ab-method** (MIT, repo created 2025-08-10), `.claude/agents/ascii-ui-mockup-generator.md`, first commit `88174952` on 2025-08-17. `diff` against our `dbff837f` file shows one difference only: `model: opus` there, `model: sonnet` here. Body and `description` (two `<example>` blocks) are identical. Whether ab-method's author wrote it is not confirmed (its README names no source for the agent).
3. **Later copy: davila7/claude-code-templates** (MIT) `cli-tool/components/agents/development-tools/ascii-ui-mockup-generator.md`, added 2026-01-25 (after our import). Its body is identical to ours at `dbff837f`; its frontmatter differs (`description` rewritten without examples, `tools: Read, Write`). Not our source; it is a sibling copy. No adopt target (current upstream body equals the baseline body).
4. Web search on the persona sentence "You are an ASCII UI Mockup Specialist, an expert in translating abstract UI concepts ..." returns the same text in dozens of catalogs and mirrors; none names an earlier author than ab-method. Search was limited to GitHub code search and one web search (standard mode); an older origin may exist.

## Credit line: missing

The root README has an `Agent credits:` paragraph for mermaid-diagram-specialist, communication-excellence-coach and codebase-pattern-finder, and none for ascii-ui-mockup-generator (the table row at README line 174 has only a description). Proposed sentence to append to that paragraph (README is edited by the coordinator, not by me):

```text
ascii-ui-mockup-generator is adapted from [ayoubben18/ab-method](https://github.com/ayoubben18/ab-method/blob/main/.claude/agents/ascii-ui-mockup-generator.md) by Ayoub Ben (ayoubben18) (MIT), the earliest public copy found (the original author is not confirmed), through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/agents/ascii-ui-mockup-generator.md); its subagent frontmatter facts follow Anthropic's Claude Code documentation (Anthropic), its fence rule follows the CommonMark specification (CommonMark), and its display-width note follows Unicode Standard Annex #11 (Unicode Consortium).
```

## Proposed registry rows (docs/audit/upstream-sources.json)

The existing row is `kind: local` with no source (`last_reviewed 2026-11-04`). It is wrong now that origins are known: replace it by rows 1 and 2 (keep a `local` row only if the coordinator prefers; `upstreams` treats `local` as having no upstream). `last_upstream_sha`/`last_reviewed` fields are written by `track`, not by hand.

```json
{"skill": "ascii-ui-mockup-generator", "kind": "github-path", "source": "softaworks/agent-toolkit:agents/ascii-ui-mockup-generator.md", "ref": "main", "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit", "artifact_kind": "agent"}
{"skill": "ascii-ui-mockup-generator", "kind": "github-path", "source": "ayoubben18/ab-method:.claude/agents/ascii-ui-mockup-generator.md", "ref": "main", "credit": "Ayoub Ben (ayoubben18), earliest public copy found; original author not confirmed", "artifact_kind": "agent"}
{"skill": "ascii-ui-mockup-generator", "kind": "unversioned", "source": "Claude Code docs, Create custom subagents: https://code.claude.com/docs/en/sub-agents", "ref": null, "credit": "Anthropic", "artifact_kind": "agent"}
{"skill": "ascii-ui-mockup-generator", "kind": "unversioned", "source": "CommonMark Spec 0.31.2, Fenced code blocks: https://spec.commonmark.org/0.31.2/#fenced-code-blocks", "ref": null, "credit": "CommonMark", "artifact_kind": "agent"}
{"skill": "ascii-ui-mockup-generator", "kind": "unversioned", "source": "Unicode Standard Annex #11, East Asian Width: https://www.unicode.org/reports/tr11/", "ref": null, "credit": "Unicode Consortium", "artifact_kind": "agent"}
{"skill": "ascii-ui-mockup-generator", "kind": "unversioned", "source": "wcwidth documentation, Introduction: https://wcwidth.readthedocs.io/en/latest/intro.html", "ref": null, "credit": "Jeff Quast and wcwidth contributors", "artifact_kind": "agent"}
```

Note on the last row: the wcwidth credit string is my reading of the project's authorship (Jeff Quast maintains the package); confirm before adding, or use "wcwidth project" instead.

## skill-updater style review (REVIEW ONLY)

Rows reviewed: only the `local` row exists, so per `skill-updater` step 2 there is no upstream to diff; I diffed both located upstreams by hand instead.

- Upstream change since our baseline: none that applies. ab-method's current file equals our baseline body (model differs); davila7's body equals our baseline body.
- **ignore:** davila7 rewrote `description` without the two `<example>` blocks, the same direction as our description; nothing to port.
- **ignore:** ab-method `model: opus`; the repo ruling and the current file keep `sonnet` (an alias the Claude Code docs accept).
- **adapt (optional, low priority):** davila7 declares `tools: Read, Write`. Our agent has no `tools` field, so it inherits every tool (docs: "Inherits every tool available to subagents if omitted"), although its rules say never to write implementation code. A `tools:` allowlist (for example `Read`, and `Write` only if the agent must save a mockup file) would be least privilege. This is a design choice, not a content loss; the restore brief may leave it.
- **adopt (fact fix):** the "emoji take 2 cells" wording (facts.md, outcome `corrected`).
- Model-validity pass: not run (read-only analyst; no `track` call allowed, and no probe lane use). Rules that counter a model habit: "NEVER write implementation code", "NEVER align columns with tabs", "treat trimmed trailing spaces as a failure". Left as keep; a probe run belongs to the controller if wanted.
- No section is marked for restore, so no restore brief item beyond the one fact fix and the optional `tools` adapt.
- `gepetto` and `datadog-cli` untouched.
