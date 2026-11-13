# Story and task anatomy

Read this only when creating a story or task, or rewriting its description. Evidence tags: VERIFIED (read in official docs or the jira-cli source), SOURCED (Atlassian community or KB snippet, not read in full), UNVERIFIED (not confirmed; test on the instance and re-read the issue).

## House policy

These are the owner's house rules, not industry or Atlassian rules. Apply them by default; the user can override any of them for one card.

1. **Statement first, three lines, bold parts:** As a **<role>**, I want **<what>**, so that **<why>**.
2. **Role is a real end-user persona of the product** (Finance Analyst, Support Agent), never "user", "developer" or "system". Mike Cohn's page says most stories are written from the view of a user or customer, and some from that of a stakeholder, another system or someone else who benefits, so this rule is stricter than the source (VERIFIED, mountaingoatsoftware.com/agile/user-stories, re-read 2026-11-07).
3. **"so that" names the goal or decision the persona gains**, not a restatement of the feature ("so that I can export" is weak). One goal per card; split otherwise.
4. **Sections, in this order:** Problem, Proposed solution, Business benefits (a revenue or cost estimate, or the words "needs data" with what data), Technical benefits, Acceptance criteria (checklist or Given/When/Then), Definition of Done, Out of scope, Risks, References (repos, scripts, Confluence pages, diagrams, docs, related cards).
5. **Always link an epic.** Find candidates, propose the best match and get approval; if none fits, ask. Never create the card unlinked without saying so.
6. **Sprint = the next future sprint, or the one after if the user says so. Never the active sprint** unless the user explicitly asks: adding scope to a running sprint changes its commitment.
7. **Assignee = the creator** (the authenticated user), sent explicitly. Never rely on the project default: it can only be the project lead or unassigned (SOURCED, Atlassian KB "unable to change the default assignee field", checked 2026-11-07), so an omitted assignee usually lands on the lead.

## The statement per deployment

Pick the format by deployment and backend (deployment table in SKILL.md).

| Write path | Bold | Line break | Status |
|---|---|---|---|
| Data Center/Server, REST v2 | `*text*` (wiki markup) | `\\` at line end | Bold SOURCED; `\\` semantics and whether a bare newline already breaks: UNVERIFIED |
| Cloud, REST v3 | ADF `strong` mark | ADF `hardBreak` node | VERIFIED (developer.atlassian.com ADF `strong`, `hardBreak`; v3 create says `description` takes ADF) |
| jira CLI, either deployment | markdown `**text**` | blank line or markdown hard break | Conversion VERIFIED (jira-cli `CreateV2`, `md.ToJiraMD`); how it treats single newlines: UNVERIFIED |
| Atlassian MCP (Cloud) | markdown `**text**` | blank line or markdown hard break | SOURCED; not in official docs |

DC description string (wiki markup; not executed against Jira):

```
As a *Support Agent*, \\
I want *to filter tickets by customer tier*, \\
so that *I answer premium customers first*.
```

Cloud v3 `description` (ADF shape built from the official node docs; not executed):

```json
{"type":"doc","version":1,"content":[{"type":"paragraph","content":[
  {"type":"text","text":"As a "},{"type":"text","text":"Support Agent","marks":[{"type":"strong"}]},{"type":"text","text":","},{"type":"hardBreak"},
  {"type":"text","text":"I want "},{"type":"text","text":"to filter tickets by customer tier","marks":[{"type":"strong"}]},{"type":"text","text":","},{"type":"hardBreak"},
  {"type":"text","text":"so that "},{"type":"text","text":"I answer premium customers first","marks":[{"type":"strong"}]},{"type":"text","text":"."}]}]}
```

Wiki markup or a plain string is not a valid Cloud v3 description: v3 takes only ADF, so say so whenever you show both payloads.

Pitfalls: `**text**` in wiki markup is not bold (stray asterisks, UNVERIFIED but expected); a wiki-markup or plain string sent as a v3 `description` is rejected or saved empty (SOURCED, JRACLOUD-71841); a `\n` inside an ADF text node is not a line break. After creating through the CLI or MCP, re-read the issue and check that the three lines and the bold parts rendered; fix the format before reporting success.

## Setting epic, sprint and assignee

Discover field ids with `GET /rest/api/{2|3}/field` (Sprint has schema custom `com.pyxis.greenhopper.jira:gh-sprint`, SOURCED: community and KB snippets, not in the Cloud spec, checked 2026-11-07) and confirm they are on the create screen with `GET /rest/api/{2|3}/issue/createmeta/{project}/issuetypes/{issueTypeId}` (or MCP `getJiraIssueTypeMetaWithFields`).

**Creator.** Always resolve it from the token that will write, on every backend including the CLI: Cloud `GET /rest/api/3/myself`, then `"assignee":{"accountId":"..."}` (VERIFIED); DC `GET /rest/api/2/myself`, then `"assignee":{"name":"..."}` (UNVERIFIED this session). CLI: `jira me` only prints the configured login, a hint that a DC Bearer token need not match, so confirm it against `myself` before passing it to `-a` (VERIFIED, jira-cli source). MCP: the current-user tool, then its account id.

**Epic.** Search candidates with JQL `project = KEY AND issuetype = Epic AND statusCategory != Done`. Set it as the parent (SKILL.md gotcha), per deployment:
- Cloud: `"parent":{"key":"EPIC-1"}` on create or edit. Atlassian deprecated Epic Link and Parent Link in Cloud create/update endpoints (company-managed projects) and made `parent` the field for both company-managed and team-managed projects (VERIFIED, developer community deprecation notice 54048; the notice excludes Server/DC).
- DC: the custom field named "Epic Link" holds the epic key: `"customfield_NNNNN":"EPIC-1"` (SOURCED, JSWSERVER-13517, checked 2026-11-07).
- CLI: `-P EPIC-1` on create or edit, then re-read the parent; fallback `jira epic add EPIC-1 KEY` (commands.md has the caveats).

**Sprint.**
1. Board: list the project's boards (`jira board list`, MCP `listJiraBoards`, or `GET /rest/agile/1.0/board?projectKeyOrId=KEY`). If more than one matches, ask the user which board; never pick one silently.
2. Future sprints of that board: `GET /rest/agile/1.0/board/{boardId}/sprint?state=future` (`state` accepts future, active, closed; VERIFIED Cloud Agile spec) or MCP `listJiraBoardSprints` for that board. `jira sprint list --state future --table --plain --columns id,name,start,state` only when the CLI config's `board.id` is that board (SKILL.md gotcha). Choose the earliest by start date (lowest id when dates are missing), and take candidates only from that board's sprint results. `originBoardId` is the board where the sprint was created; sprints can be shared across boards, so if it differs, still propose the sprint, say it is shared, and ask for confirmation.
3. None future: leave the sprint empty and say so; do not fall back to the active sprint.
4. Add after creation: `jira sprint add SPRINT_ID KEY`, or `POST /rest/agile/1.0/sprint/{id}/issue` with `{"issues":["KEY"]}` (max 50 issues; VERIFIED). Setting the Sprint field on create: value shape (number or object) is SOURCED and inconsistent, so prefer the move after creation.

DC parity of the Agile endpoints is UNVERIFIED; the paths are the same in practice.

## References section

Put every reference in the References section and also attach it as a real relation, so it survives description edits: related cards as issue links (`Blocks`, `Relates`; read link-type direction first), URLs to repos, PRs, scripts and Confluence pages as remote links, diagrams and docs as attachments. Syntax: commands.md (CLI), mcp.md (MCP and REST).

## Report after creating

State the key, the assignee, the parent epic, the sprint, the links added, and anything left empty with the reason (no future sprint, no epic approved, field not on the create screen).
