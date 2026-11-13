---
name: daily-meeting-update
description: "Generate concise Markdown daily standup or scrum updates covering yesterday, today, blockers, and discussion topics. Use when preparing for a daily team sync or short yesterday/today update, even without saying standup. Interview only for missing facts; optionally use explicitly approved GitHub, Jira, or Claude Code activity. Not for weekly reports, meeting agendas, performance reviews, timesheets, or retrospectives."
user-invocable: true
---

# Daily Meeting Update

The user's answers are the source of truth; integrations only jog memory. Work through the steps in order.

## 1. Fast path

If the user already gave the four required answers (step 4) and approved no integration, skip steps 2 and 3 and draft. Once an integration is approved, the step 3 gates still run. For time-pressed requests ("quick daily", "meeting in 5 minutes", "no tools") skip integration offers and ask every missing answer in one message.

## 2. Optional integrations: detect, ask, then access

1. Before consent, check only that an executable exists (`command -v gh`, `command -v jira`) or that a tool is advertised (any tool of an Atlassian or Jira MCP server; the server name is the user's choice, so `mcp__atlassian__*` is only the common one). `gh auth status`, repo commands, MCP calls and history reads all touch account or private data, so they run only after approval.
2. Ask once per integration and scope: which GitHub repos, which Jira project keys, whether to read Claude Code history. Access only what was approved; with no confirmed repo or project, ask instead of querying account-wide, including after a scoped query fails. Where the `AskUserQuestion` tool is available (it is not inside subagents), ask these questions and the step 3 interview through it, one call per round with 1-4 questions and 2-4 options each (checked 2026-11-07: https://code.claude.com/docs/en/agent-sdk/user-input); otherwise ask in plain text.
3. Fix the window before any query: the last working day, or a span such as Friday-Sunday, in the user's IANA timezone `ZONE` (ask if unsure; on Monday or after leave, ask which days count). Print its UTC bounds, DST-safe:

   ```bash
   python3 -c 'import sys,datetime as d,zoneinfo as z;s=d.datetime.fromisoformat(sys.argv[1]).replace(tzinfo=z.ZoneInfo(sys.argv[2]));e=s+d.timedelta(days=int(sys.argv[3]) if len(sys.argv)>3 else 1);print(*(t.astimezone(d.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") for t in (s,e)))' FIRST_DAY ZONE [DAYS]
   ```

   It needs Python 3.9 or later (`zoneinfo`; plus the `tzdata` package on Windows); if it fails, run `python3 --version` and say what is missing. It prints `START END`. Searches use `START` only to discover candidates; an event (`mergedAt`, your review's `submittedAt`, `resolutiondate`) belongs to the window only when it falls in [`START`, `END`); a PR counts as opened in the window when its `createdAt` falls in [`START`, `END`). Later events, today's included, never go in Yesterday; with no event time, ask. Tie-breaks: a PR with both `createdAt` and `mergedAt` inside the window is reported once, as merged; a review with no `submittedAt` is asked about (the no-event-time rule), never placed by search `updated`.
4. Run the queries below. If one fails or is declined, say so in one line and go on to the interview.

| Source | Query |
|--------|--------------------------------------------|
| PRs you authored | `gh search prs --author @me --repo OWNER/REPO --updated ">=START" --json number,title,state,isDraft,url` |
| PRs you reviewed | `gh search prs --reviewed-by @me --repo OWNER/REPO --updated ">=START" --json number,title,state,url` |
| PR details, for each PR you report as done, reviewed or matched to a session | `gh pr view NUMBER --repo OWNER/REPO --json number,title,state,createdAt,mergedAt,headRefName,reviews,url` |
| Jira (MCP first, CLI only without it) | JQL `project IN ("KEY") AND assignee = currentUser() AND updated >= "FIRST_DAY"`, reading `status`, `resolution`, `resolutiondate`; CLI: `jira issue list --jql '<JQL>' --plain` |
| Claude Code history, once per day of the window | `TZ=ZONE python3 "${CLAUDE_SKILL_DIR}/scripts/claude_digest.py" --date DAY --format json` (add `--project PATH`); merge days by `id`, `project` and `branch` |

(gh flags and state values: https://cli.github.com/manual/gh_search_prs, https://cli.github.com/manual/gh_pr_view, checked 2026-11-07)

Always take the digest as JSON and render it yourself. Its titles are `Session <id>` by design (no message text is copied), so the user picks sessions by number, project, branch and files, through an `AskUserQuestion` question with `multiSelect: true` when there are 2 to 4 sessions, and from a numbered list in plain text otherwise (more than 4, a single one, or no tool). Omit unpicked sessions silently: never name, count or explain them in the update or the reply. On `session_count: 0`, say "no Claude Code sessions for that day" once and continue.

## Gotchas

- `gh pr list` returns only open PRs by default, so yesterday's merged work vanishes. `gh search prs` reports `state` as `open`, `closed` or `merged` (`gh pr view`: `OPEN`, `CLOSED`, `MERGED`); closed is never merged. Search output has no head branch, so match a PR to a session only on `headRefName` from `gh pr view`; if the details cannot be fetched, ask instead of inferring.
- `--author @me` misses PRs you only reviewed, hence the second query.
- "Updated" also moves on comment-only edits by anyone, so an updated hit is a candidate, never an event.
- Two unrelated tools install as `jira`: ankitpokhrel/jira-cli and go-jira. `issue list --jql` and `--plain` exist only in jira-cli, so run `jira version` first and use the CLI only when it prints `(Version="…"`; otherwise use the MCP or ask (https://github.com/ankitpokhrel/jira-cli, https://github.com/go-jira/jira, checked 2026-11-07).
- JQL dates use the Jira profile's timezone, not `ZONE`; if they may differ, discover from the day before `FIRST_DAY` and let the `resolutiondate` window decide (https://support.atlassian.com/jira-software-cloud/docs/jql-fields/, https://support.atlassian.com/jira-software-cloud/docs/jql-functions/, checked 2026-11-07).
- A digest `project` of `[unresolved project: …]` means no `cwd` was recorded; show it as is, never decode it into a path.
- With `--project`, the digest keeps only messages whose own recorded `cwd` lies inside that path.
- The digest reads Claude Code's transcripts under `$CLAUDE_CONFIG_DIR/projects` (default `~/.claude/projects`), kept 30 days by default. That file format is internal to Claude Code and can change on any release, so if a day with known sessions digests as empty, say so in one line instead of guessing (checked 2026-11-07: https://code.claude.com/docs/en/sessions).

## 3. Interview

Ask for topics even when tools found plenty: no tool can detect them. When approved activity exists, show a short summary first. Before drafting, apply these gates:

- Provenance: files touched, command counts, commits and open PRs are activity, not outcomes. Report something as done only when the user says so or the evidence is terminal: a merged PR, or a ticket whose resolution is a successful one for that project (Done, Fixed and the like). Won't Do, Duplicate, Cannot Reproduce and similar are triage outcomes; report them as such, never as delivered. Otherwise ask "done, or still in progress?".
- Contradiction: if activity conflicts with an answer (no blockers, but a ticket is flagged blocked or a review requested changes; "finished X", but its PR is still open), name the conflict and ask; never resolve it silently either way.
- Merge only the same work item: entries become one bullet when they share a ticket key, a PR, a PR `headRefName` equal to the session branch, or the user confirms they are one task. Different projects or branches stay separate bullets, even within one session.
- Vague after two focused questions: offer a candidate bullet grounded in approved activity and ask for confirmation.

## 4. Output

Sections, in order: `# Daily Update - YYYY-MM-DD` (the meeting date, today, not the window), `## Yesterday`, `## Today`, `## Blockers` ("No blockers"), `## PRs & Reviews` and `## Jira` (only when approved data was pulled), `## Topics for Discussion` ("None"). Yesterday, Today, Blockers and Topics are the four required answers. Item format: `- Fixed flaky checkout test (merged PR #412 - Fix flaky checkout integration test)`, `- PAY-231 - Retry policy for card payments (In Progress)`.

At most 15 bullets: past that, fold minor items into one bullet, never drop blockers or topics. Every PR or ticket number carries its title; links only when known.

When writing the update, read `references/output-template.md`: it holds the PRs & Reviews layout (Opened, Merged, Reviews with their outcome), the Links footer, a fill-in template and a filled example, and says where an open PR goes.

## Never

- Never quote session-log text: logs hold pasted secrets, tokens and internal URLs that would leak into a shared channel.
- Never report an investigation or an open PR as delivered: the team plans around it and finds out at the next standup.
- Never access an unapproved repo, project or session: approval of one scope is not approval of the account.
- Never let tool activity replace the why, the blockers or the plans: tools show motion, not intent or impediments.
