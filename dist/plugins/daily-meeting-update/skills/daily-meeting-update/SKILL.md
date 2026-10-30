---
name: daily-meeting-update
description: "Generate concise Markdown daily standup or scrum updates covering yesterday, today, blockers, and discussion topics. Use when preparing for a daily team sync or short yesterday/today update, even without saying standup. Interview only for missing facts; optionally use explicitly approved GitHub, Jira, or Claude Code activity. Not for weekly reports, meeting agendas, performance reviews, timesheets, or retrospectives."
user-invocable: true
---

# Daily Meeting Update

Produce an accurate, brief daily standup update from user-provided facts. Integrations are optional evidence, never a substitute for the user's context.

## Fast path

If the user already supplied yesterday, today, blockers, and discussion topics, treat those as answered and generate directly. Ask only for missing or ambiguous facts. For time-pressed requests (“quick daily”, “meeting in 5 minutes”), skip integration offers and ask all missing questions in one message. If answers remain vague after two focused questions, offer a candidate grounded in approved activity and ask for confirmation; never invent.

## Optional integrations: detect, ask, filter

Before consent, discover only executable presence and advertised tool availability. Ask before accessing any integration. Run authentication checks, repository commands, MCP requests, and history reads only after explicit approval for that integration and scope. For GitHub/Jira, ask which repositories/projects; access only those approved. For Claude Code history, ask consent, then show sanitized session titles for user selection. If the harness lacks `AskUserQuestionTool`, present numbered options and accept comma-separated selections (e.g. `1,3`). If an integration fails or is unavailable, continue with the interview.

Run the bundled digest from the loaded skill root:

```bash
python3 scripts/claude_digest.py --format json
python3 scripts/claude_digest.py --date today --format json
python3 scripts/claude_digest.py --project ~/my-app --format json
```

The digest filters messages to the requested local calendar day; sessions spanning days contribute only matching-day activity. Prefer the recorded `cwd` as project path. If path metadata is absent, preserve the encoded identifier as unresolved rather than guessing. JSONL parse errors should not discard valid other lines/sessions.

## Interview

Ask only what's missing, one compact question or group when convenient:

1. Yesterday / since last standup: completed outcomes and other work.
2. Today: planned work.
3. Blockers: impediment or “none”.
4. Topics: decisions/questions for the team or “none”.

When approved activity exists, show a concise summary to prompt memory, then ask what is missing. Group duplicate activity appearing in session history, commits, PRs, Jira, and answers by work item. Distinguish completed outcomes from investigation and future plans. Prioritize blockers and decisions needing team action.

Session logs may contain secrets or internal URLs. NEVER quote session message contents verbatim; surface selected titles, branches, filenames, and verified work summaries only.

## Output

```markdown
# Daily Update - [DATE]

## Yesterday
- [Completed outcomes; include approved PR/ticket context without duplicates]

## Today
- [Plans]

## Blockers
- [Blocker or “No blockers”]

## PRs & Reviews (if approved/pulled)
- [Relevant activity with title/context]

## Jira (if approved/pulled)
- [Relevant ticket activity with title/context]

## Topics for Discussion
- [Topics or “None”]
```

Keep to 15 bullets or fewer. Include links only when available. Do not include ticket/PR numbers without context.

## Never

- Never access a repo/project without explicit approval.
- Never skip the discussion-topic question unless already answered.
- Never let tool activity replace asking why, blockers, or plans.
- Never claim an investigation as completed delivery.
- Never quote session-file contents verbatim; do not include unrelated or personal sessions.
