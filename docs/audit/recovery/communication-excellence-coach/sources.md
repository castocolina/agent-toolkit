# Sources: communication-excellence-coach (agent)

Checked 2026-11-15, batch 13 (BASE cbeef0af79f76accabee5197e396f3d7dd22117d). Review only: no `track` call, no edit of the artifact, no edit of `docs/audit/upstream-sources.json` or `README.md`.

## Origins found

1. Original author: `davila7/claude-code-templates` (MIT, "Copyright (c) 2025 Daniel (San) Avila"), file `cli-tool/components/agents/business-marketing/communication-excellence-coach.md` on `main`. Evidence: the baseline body at `dbff837f` is that file's body line for line (diffed against upstream at commit `1c194fd27b9c`, 2026-01-25); the only differences are the `description` line (ours "PROACTIVELY use when reviewing communication drafts ...", upstream "Communication specialist providing ... research-backed suggestions") and our added `color: green`. The upstream path has 4 commits, the latest `5e485af3cb73` (2026-09-28, "improve: enhance communication-excellence-coach (#1020)"), file blob `5fe4d6d18882`. A web search on the distinctive example ("Roleplay as my team lead who I need to ask for a deadline extension") lists the same agent on aitmpl.com, vibehackers.io and remoteopenclaw.com under `davila7/claude-code-templates`.
2. Direct upstream: `softaworks/agent-toolkit`, file `agents/communication-excellence-coach.md` on `main` (MIT). Introduced in `673fe769` (2026-01-18, "add 6 agents and 4 commands from claude-plugins"), last changed by `ebb0419d` (2026-01-19, moved to the agents root and cross-references fixed). Its blob `35a822b5` equals our file at `3027f20f` and at `dbff837f` (`git diff --stat 3027f20f dbff837f` is empty); upstream `main` head is still `3027f20f`, so softaworks has no change since the fork point.

The current file is a full rewrite (new Intake, Review, Roleplay, NEVER, Gotchas and Handoffs sections); apart from the frontmatter keys and the What-Why-How, SBI and Coach Feedback names, no baseline sentence survives.

## Missing credit

The current agent carries no credit and the root `README.md` has none for it (its "Agent credits" line names only mermaid-diagram-specialist; line 5 credits the fork source and stays untouched). Proposed line for the root `README.md`, appended to the "Agent credits" paragraph under the Agents table:

```text
communication-excellence-coach is adapted from [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/business-marketing/communication-excellence-coach.md) by Daniel Avila (MIT), through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/agents/communication-excellence-coach.md).
```

## Proposed registry rows (verbatim; each passes `validate_entry`, checked with `tmp/cec-validate.py`)

The existing row `{"skill": "communication-excellence-coach", "kind": "local", ...}` says "no upstream", which is now wrong; replace it with the first two rows.

```json
{"skill": "communication-excellence-coach", "kind": "github-path", "source": "davila7/claude-code-templates:cli-tool/components/agents/business-marketing/communication-excellence-coach.md", "ref": "main", "credit": "Daniel Avila (davila7)", "artifact_kind": "agent"}
{"skill": "communication-excellence-coach", "kind": "github-path", "source": "softaworks/agent-toolkit:agents/communication-excellence-coach.md", "ref": "main", "credit": "softaworks", "artifact_kind": "agent"}
{"skill": "communication-excellence-coach", "kind": "unversioned", "source": "Claude Code docs, Create custom subagents (https://code.claude.com/docs/en/sub-agents)", "ref": null, "credit": "Anthropic", "artifact_kind": "agent"}
{"skill": "communication-excellence-coach", "kind": "unversioned", "source": "Claude Code docs, Plugins overview (https://code.claude.com/docs/en/plugins)", "ref": null, "credit": "Anthropic", "artifact_kind": "agent"}
{"skill": "communication-excellence-coach", "kind": "unversioned", "source": "Slack Help Center, Use threads to organize discussions (https://slack.com/help/articles/115000769927-Use-threads-to-organize-discussions-)", "ref": null, "credit": "Slack", "artifact_kind": "agent"}
```

The last three are the official pages used in `facts.md`.

## skill-updater style review (review only)

- Rows: the registry holds only the `local` row, so `upstreams` has nothing to compare; the two `github-path` rows above were checked by hand with `gh api` (both paths resolve on `main`; softaworks unchanged since the fork point; davila7 changed since our copy, below).
- Upstream change in `davila7` since our baseline copy (diff of upstream `main` against the Jan 2026 text our baseline holds):
  - Rewritten `description` with three `<example>` blocks and "Use PROACTIVELY": ignore. Our description is a deliberate rewrite and states its own exclusions; the example blocks are dispatcher scaffolding, not guidance.
  - `model: opus` changed to `model: sonnet`: ignore. Model choice is this repo's call (the agent's difficult-conversation judgment is why it stays on the `opus` alias); the alias is verified in `facts.md`.
  - Roleplay "Hold the persona" step (keep the character's concerns and resistance across the whole exchange, do not turn agreeable because the user applied one technique): ignore, already covered. The current Roleplay section is stricter: one in-character objection at a time, and a branch table that repeats or sharpens the objection until the reply answers it while keeping the ask.
  - Tool-scope line ("`Glob`/`Grep` only to locate a draft the user references, never to browse the codebase"): adapt, optional and low priority. One clause in Intake step 2 ("a file path you can Read") could add "use Glob or Grep only to find a file the user named". The agent already lists only read tools, so the risk is wasted calls, not harm.
  - "When to Pause and Flag" (harassment, discrimination, retaliation, termination, PIP, legal or HR-documented action, threats, safety, whistleblower content: still give tone and structure feedback, and add a note to involve HR or legal before sending): adapt, recommended. The current file declines legal review and keeps safety or escalation flags in drafts (NEVER, Handoffs), and feedback-mastery R6 covers formal matters, but R6 reaches the agent only when the model loads the preloaded skill's section; no line in the agent says to add the HR or legal note on a harassment, PIP or termination draft. Brief item: one sentence in Handoffs naming those drafts and requiring the "involve HR or legal before sending" note while still giving the wording feedback.
  - Handoff lines to `customer-support`, `email-composer` and `email-sequence` skills: ignore. Those artifacts do not exist in this repo.
  - See Also fixes (`professional-communication`, `difficult-workplace-conversations`, `email-composer`): ignore. It confirms the baseline names were wrong (record row s020); this repo has no See Also section and `difficult-workplace-conversations` is a separate skill that the current Handoffs do not name (adopt candidate below).
- Adopt: none.
- Adapt: the HR or legal flag sentence above (recommended); the Glob or Grep scoping clause (optional).
- Optional Step 6 consideration, not a recorded loss: name `difficult-workplace-conversations` in the roleplay handoff for high-stakes scenarios (termination, PIP, harassment), since the agent preloads only `feedback-mastery`, whose description routes layoffs and formal matters to that skill. The skill exists at `skills/difficult-workplace-conversations`.
- Ignore: the upstream example blocks, the model change, the non-existent skill names.
- Model-validity note: the NEVER and Gotchas rules counter habits a model has (polishing away a safety flag, deleting honest hedges, inferring motive in feedback); each is kept. The Intake route and the Review gap test are not model-validity items; they are this agent's own procedure.
