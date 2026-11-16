# Daily Meeting Update

Generate a short Markdown daily standup update (yesterday, today, blockers, discussion topics) through a brief interview, optionally enriched with GitHub, Jira or Claude Code activity that you approve. The workflow, gates and output format live in [SKILL.md](SKILL.md); this file is for humans.

## When to use

"Help me with my daily", "prepare my standup", "scrum update", "what's my status for today's meeting?". Not for weekly reports, meeting agendas, performance reviews, timesheets or retrospectives.

## Integrations

All optional; the skill works from your answers alone. Before you approve anything it only checks that a tool exists. Authentication checks, repo or ticket queries and history reads happen only for the integrations and scopes you approve.

| Integration | Needs |
|-------------|-------|
| GitHub | `gh` CLI |
| Jira | `jira` CLI or an Atlassian or Jira MCP server (tools named `mcp__<server>__*`, `mcp__atlassian__*` being the common name) |
| Claude Code history | `~/.claude/projects/` session logs (under `$CLAUDE_CONFIG_DIR/projects` when that is set), read by `scripts/claude_digest.py` |

Python 3.9 or later is needed for the window one-liner and the digest script (plus `tzdata` on Windows, which has no system time zone database; [zoneinfo](https://docs.python.org/3/library/zoneinfo.html) and [pathlib](https://docs.python.org/3/library/pathlib.html), checked 2026-11-07).

## Claude Code digest

```bash
python3 scripts/claude_digest.py [--date today|yesterday|YYYY-MM-DD] [--project PATH] [--format json|text]
```

It reports, per session active on that local calendar day: id, project (`cwd`), branch, up to 10 file names touched and the Bash command count. A session that switched project or branch that day is listed once per pair. Titles are `Session <id>`: no message text is ever copied out, because logs can hold secrets and internal URLs. You pick which sessions count; the rest are dropped. Claude Code keeps transcripts for 30 days by default (`cleanupPeriodDays`), so an older day digests as `session_count: 0`, and their format is internal to Claude Code and can change on any release, so an empty digest for a day that had sessions can mean the format changed ([Claude Code docs, Manage sessions](https://code.claude.com/docs/en/sessions), checked 2026-11-07).

Tests: `python3 -m unittest discover -s tests/skills/daily-meeting-update` from the repository root.

## Example output

```markdown
# Daily Update - 2026-01-22

## Yesterday
- Fixed login timeout (merged PR #120 - fix: login timeout)
- Researched payment providers

## Today
- Continue OAuth flow (PR #125 - feat: add OAuth flow)

## Blockers
- No blockers

## Topics for Discussion
- Architecture of the new payments module
```

## Installation

**Claude Code:** `cp -r skills/daily-meeting-update ~/.claude/skills/`

**claude.ai:** add the skill to project knowledge or paste SKILL.md into the conversation.

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Tool and platform facts were checked against the official documentation of Anthropic (Claude Code), GitHub (gh CLI), Atlassian (Jira JQL), ankitpokhrel (jira-cli), Cory Bennett (go-jira) and the Python Software Foundation.
