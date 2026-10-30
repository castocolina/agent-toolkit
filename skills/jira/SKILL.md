---
name: jira
description: "Work with live Jira issues using jira CLI or Atlassian MCP: view, create, edit, comment, transition, search with JQL, and check sprint/backlog status. Use when asked to act on an issue or ticket, query Jira, or manage sprint planning against Jira, including issue keys like PROJ-123. Also use to draft clearly fictional Jira/JQL examples for tutorials when requested, without accessing Jira. Not for summarizing pasted Jira text without a requested Jira operation, generic ticket estimation/planning, GitHub/Linear issues, Jira administration, or conceptual Jira workflow discussion."
---

# Jira

## Offline fictional examples

For explicitly fictional tutorials or examples, draft clearly labeled fictional Jira/JQL syntax without probing the CLI or MCP tools, requiring authentication, or providing a setup handoff. Load only the relevant syntax guidance from `references/commands.md` or `references/mcp.md`.

## Backend selection

For live Jira operations, check whether `jira` CLI is available; otherwise inspect actual exposed `mcp__atlassian__*` tools. Use whichever supported backend exists. If neither is available, explain the blocker and provide setup guidance: link to the jira-cli installation project (`https://github.com/ankitpokhrel/jira-cli`) and explain that after installation the user can run `jira init` interactively to configure Jira URL and authentication. Do not run interactive initialization or imply Jira access is available.

| Intent | CLI | MCP |
|---|---|---|
| View issue | `jira issue view KEY` | `mcp__atlassian__getJiraIssue(issueKey)` |
| Search | `jira issue list ...` | `mcp__atlassian__searchJiraIssuesUsingJql(jql)` |
| Create | `jira issue create ... --no-input` | `mcp__atlassian__createJiraIssue` |
| Edit | `jira issue edit KEY ...` | `mcp__atlassian__editJiraIssue` |
| Transitions | `jira issue move KEY STATE` | get transitions, then `transitionJiraIssue(issueKey, transitionId)` |
| Comment | `jira issue comment add KEY ...` | `mcp__atlassian__addCommentToJiraIssue` |

Bind MCP calls to actual exposed tool schemas; do not invent aliases. Load `references/commands.md` or `references/mcp.md` only for complex fields, JQL, transitions, linking, or troubleshooting. Multiline CLI bodies should use `--template <file>`, not command substitution.

## Operation paths

- **Read/list:** query only requested data; no mutation preflight is needed.
- **Create:** if code, ticket, or PR context is referenced, read it before drafting. Fetch project and issue-type metadata for required fields; get user approval of content; then create non-interactively with all required fields supplied.
- **Existing issue mutation:** fetch current issue and relevant transition/link context, show original versus proposed change, explain one-way or notifying effects, obtain approval, apply, then fetch again to verify. Jira transitions may be one-way and edits have no general undo.
- **Batch:** present the full change list before acting; execute one approved batch of at most 10 issues. Re-confirm before exceeding that size; verify each result and stop on partial failure.

## Mutation checklist

- Fetch status and available transitions before transitioning; names and IDs differ across projects and intermediate states may be required.
- Show original description before replacement.
- Discover required fields before CLI `--no-input`; missing fields can fail opaquely.
- Resolve MCP assignees to account IDs; display names are not valid identifiers.
- Preserve existing data, obtain approval for exact changes, and surface authentication failures without entering interactive setup.

## No backend

Provide the jira-cli project or Atlassian MCP setup options and ask the user to configure one. Do not claim to have accessed Jira or summarize pasted tickets as if they were live data.
