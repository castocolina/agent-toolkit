---
name: jira
description: "Work with live Jira issues through the jira CLI, Atlassian MCP or REST: view, search with JQL, create, edit, comment, transition, link, and set epic, sprint and assignee on Jira Cloud or Data Center. Use when asked to act on an issue, ticket or bug (keys like PROJ-123), query Jira, file a bug or ticket on the team board, draft or create a Jira story or task, or plan what goes into a sprint, even when the user only says 'ticket' or 'board'; also for clearly fictional Jira or JQL examples for a tutorial, without accessing Jira. Not for summarizing pasted Jira text with no Jira operation, user stories meant for other tools, generic estimation, GitHub or Linear issues, Jira administration or MCP server setup, or conceptual workflow discussion."
---

# Jira

## 1. Route the request

- **Fictional example or offline draft** the user asked for: write it, label it fictional or draft, and do not probe backends or ask for authentication.
- **Live operation:** choose backend and deployment (section 2), then follow section 3.
- **No backend:** say no backend can reach Jira and do not invent issue contents. Offer setup: install jira-cli (follow its Installation guide, `https://github.com/ankitpokhrel/jira-cli#installation`, which covers Homebrew, Nix, releases and Docker; checked 2026-11-07) and have the user run `jira init` themselves, or connect the Atlassian MCP server.

## 2. Backend and deployment

Pick the backend per step, in this order:

1. **jira CLI** when an authenticated read against the intended site succeeds: `jira issue view KEY --plain` for the issue at hand, or `jira issue list --plain --paginate 1`. `jira me` only prints the saved login and proves nothing. On an authentication or connection error, try the MCP before reporting Jira unreachable. Syntax: `references/commands.md`.
2. **Atlassian MCP** when the CLI is missing, or for what the CLI cannot do: list available transitions, read required create fields, upload attachments. Tools: `references/mcp.md`.
3. **REST** only with credentials already on the machine; prove them with an authenticated read (`GET /rest/api/{v}/myself` or the issue) before any setup advice (`references/mcp.md`).
4. Nothing can do the step: stop and name the missing capability. Never fall back to an interactive prompt (`jira init`, `jira issue move KEY` without a state, `create` without `--no-input`): the agent cannot answer it and the command hangs.

| Fact | Cloud (host `*.atlassian.net`, CLI `installation: Cloud`) | Data Center / Server (CLI `installation: Local`) |
|---|---|---|
| REST | v3 (v2 also served) | v2 |
| User identifier | `accountId` | username (`name`) |
| Epic of a story | `parent` field | Epic Link custom field (id per instance) |
| Raw REST description | ADF on v3 (wiki markup or a plain string is invalid there), wiki markup on v2 | wiki markup |
| Through the CLI | markdown; the CLI converts it to wiki markup and posts to v2 | same |
| Through the Atlassian MCP | markdown (SOURCED; check the read-back) | no DC support documented (UNVERIFIED) |

| Intent | jira CLI | MCP (v2 names; v1 aliases in mcp.md) |
|---|---|---|
| View / search | `jira issue view KEY`, `jira issue list -q"JQL"` | `getJiraIssue`, `searchJiraIssuesUsingJql` |
| Create / edit | `jira issue create --no-input ...`, `jira issue edit KEY --no-input ...` | `createJiraIssue`, `editJiraIssue` |
| Transition | `jira issue move KEY "Status"` (cannot list transitions; a failed move's error lists the states, commands.md) | `listJiraIssueTransitions`, then `transitionJiraIssue` |
| Comment | `jira issue comment add KEY --template FILE` | `addOrEditJiraIssueComment` |

## 3. Procedure for every change

1. **Fetch the live state the change depends on:** the current issue for edits; the available transitions for a move (names and ids differ per workflow; if the target is not in the list, propose a full multi-hop route only from a trusted workflow graph (for example MCP `getJiraWorkflows`, disabled by default); otherwise show the transitions offered now, take one approved hop at a time and re-read after each); CLI-only setups list transitions through REST with jira-cli's server, login and `JIRA_API_TOKEN` (mcp.md, Transitions); the required fields of project and issue type for a create (`--no-input` with a required field missing fails with an opaque error).
2. **Show the exact change:** original versus new text, the exact command or tool call, and side effects (watchers are notified, a transition may be one-way). Payloads you only display were not executed: say so and tell the user to re-read the created issue to check rendering.
3. **Get approval for that exact change.** Jira has no general undo and notifications cannot be recalled. A change to the approved content needs approval again. If the metadata shows a required field the approved draft lacks (for example `components`), still show the full exact command with a proposed value from the allowed values, list the alternatives, mark it pending and ask the user to choose or confirm; run nothing. Do not withhold the command.
4. **Apply non-interactively.**
5. **Re-read and report.** Jira can accept a request and still drop a field (not on the screen, format not rendered, link reversed), so state that you will do a separate read after the create and report what it shows, not what was sent or the create response. Compare it with the approved content or the user's request (a draft or request file in context is the source of the requested values). On a mismatch, name each field as requested versus stored (for example priority High requested, Medium stored), do not call the change done, and ask how to proceed.

**Batch:** list every change first. Default batch is 10 issues, so the list stays reviewable and a failure stays small; the user may raise it. Apply one issue at a time, verify each, and stop at the first failure: report done, failed (with the error) and not attempted, and ask how to continue. Propose no command for the not-attempted issues, not even a conditional one, until the user decides.

**Story or task:** creating one or rewriting its description, also read `references/story-anatomy.md` (statement format per deployment, sections, epic, sprint and assignee rules), plus `references/mcp.md` when that create goes through MCP or REST. For a draft card, the reply opens with the three bold As a / I want / so that lines as its first characters, with no heading, title or metadata before them; the sections follow. A draft is not a creation: say nothing was created and end by asking the user to review it before you create. Sprint: the next future sprint by default, never the active one unless the user explicitly asks (adding scope changes a running sprint's commitment); state that reason and write the chosen sprint id into the command, not a placeholder. Do not load story-anatomy.md for bugs, reads, transitions or comments.

## Gotchas

- An epic is hierarchy, not an issue link. Linking a story to its epic with `jira issue link` or an "Epic" link type does not put it under the epic.
- `jira sprint list` reads only the board saved in the CLI config (`board.id`; there is no board flag) and shows only active and closed sprints unless you pass `--state future`. Planning from it can pick another board's sprint or miss the upcoming ones; bind the lookup to the chosen board (story-anatomy.md, Sprint).
- Display names are not user identifiers on Cloud, and `jira issue assign KEY "Jo"` prompts when several users match. Use `$(jira me)`, an exact email or an account id.
- Custom field ids (Sprint, Epic Link, story points) differ per instance. Discover them; an id copied from another site writes the wrong field or fails.
- Link direction is easy to invert: neither jira-cli nor the REST docs say plainly which side of `Blocks` reads "blocks" (the REST docs only call the outward issue the "from" issue). Read the link back (`jira issue view A`, or `fields=issuelinks`) and fix a reversed one.
- jira-cli `edit` with a body replaces the whole description; show the original first.
- `jira issue list -q` ANDs `project=<configured>` onto the JQL unless the JQL has its own `project` clause (VERIFIED, jira-cli `pkg/jql`), so a cross-project query silently returns one project. Add `project in (A, B)` or run the full JQL through MCP `searchJiraIssuesUsingJql` or REST `GET /rest/api/3/search/jql` (Cloud; the old `/search` is being removed: the v3 reference marks `GET /rest/api/3/search` deprecated with "Endpoint is currently being removed", linking https://developer.atlassian.com/changelog/#CHANGE-2046, in https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/, checked 2026-11-07) or `/rest/api/2/search` (DC, UNVERIFIED: not in the Cloud spec and the DC docs were not read, 2026-11-07).

## Load only what the step needs

- `references/commands.md`: jira-cli flags beyond the table above (filters, create and edit fields, sprints, epics, links, remote links).
- `references/mcp.md`: MCP tool names (v1 and v2), REST calls with credentials, JQL pitfalls, error meanings.
- `references/story-anatomy.md`: only for creating or rewriting a story or task.
