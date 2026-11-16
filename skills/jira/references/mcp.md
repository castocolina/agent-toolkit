# Atlassian MCP and REST reference

Load when the step runs through the Atlassian MCP server or REST, or needs non-trivial JQL. Evidence tags: VERIFIED (official docs or OpenAPI spec read 2026-11), SOURCED (Atlassian community or KB snippet), UNVERIFIED (test on the instance).

## MCP tool names

Bind every call to the schemas the session actually exposes (the prefix depends on the server name, often `mcp__atlassian__`). Atlassian's supported-tools page lists the v2 names below and says they exist only on MCP v2 (VERIFIED, support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools). Older v1 servers use the v1 names; v1 had no link or attachment tool (UNVERIFIED), and the page documents no v1 name, so every v1 name below is UNVERIFIED (checked 2026-11-07; read the schema). Many tools take a `cloudId` from `getAccessibleAtlassianResources`, which the page says is needed before other calls (VERIFIED, same page, checked 2026-11-07; read the schema).

| Intent | v2 name | v1 name |
|---|---|---|
| Get issue | `getJiraIssue` | same |
| JQL search | `searchJiraIssuesUsingJql` | same |
| Create / edit | `createJiraIssue` / `editJiraIssue` | same |
| List projects (the create flow needs a project key) | `listJiraProjects` | `getVisibleJiraProjects` (UNVERIFIED) |
| Issue types of a project | `listJiraProjectIssueTypesMetadata` | `getJiraProjectIssueTypesMetadata` |
| Fields of one issue type (required, allowed values) | `getJiraIssueTypeMetaWithFields` | same |
| Available transitions | `listJiraIssueTransitions` | `getTransitionsForJiraIssue` |
| Transition (v2 can also set sprint or backlog) | `transitionJiraIssue` | same |
| Comment | `addOrEditJiraIssueComment` | `addCommentToJiraIssue` |
| Account id by name or email | `lookupJiraAccountId` | same |
| Current user | `getJiraCurrentUser`, or `atlassianUserInfo` (a common tool on the v2 page) | not documented |
| Link types / create link | `listJiraIssueLinkTypes` / `createJiraIssueLink` | none |
| Remote (web) link | `createJiraIssueRemoteIssueLink` | none |
| Attachment upload | `uploadAttachmentToJiraIssue` | none |
| Boards / sprints of a board | `listJiraBoards` / `listJiraBoardSprints` (active, future or closed) | none |
| Create, populate, start or close a sprint | `manageJiraSprint` | none |

The page lists more v2 tools than the table (changelogs, comments, assignable users, filters, statuses, board configuration, watching, worklogs, hierarchy conversion, attachment download; delete tools are disabled by default). The catalog churns: read the supported-tools page and the live schemas for anything not in the table.

Description format: deployment table in SKILL.md (the markdown claim is SOURCED from Atlassian developer community thread 101278, which reports raw ADF dropped on edit; the supported-tools page states no description format, checked 2026-11-07, so keep reading the issue back).

## REST fallback

Use REST only when credentials already exist on the machine (jira-cli's config, or variables the user names); never ask the user to paste a token into chat and never echo it. `jira --debug` may print auth headers, so keep it out of shared output (jira-cli's own skill, checked 2026-11-07). First make one authenticated read (`GET /rest/api/{v}/myself` or the requested issue); give setup advice only if it fails. jira-cli setups keep the server URL and login in the `jira init` config and the token in `JIRA_API_TOKEN` (Cloud: basic auth with email and API token; DC: basic with password, or a personal access token as Bearer when `JIRA_AUTH_TYPE=bearer`; VERIFIED, jira-cli README).

`{v}` is `3` on Cloud and `2` on Data Center (Cloud also serves v2, which takes wiki markup instead of ADF). Paths are VERIFIED in the Cloud OpenAPI specs; DC parity is UNVERIFIED where marked.

| Purpose | Call |
|---|---|
| Current user | `GET /rest/api/{v}/myself` (Cloud `accountId`; DC `name`) |
| Field ids (Sprint, Epic Link, story points) | `GET /rest/api/{v}/field` |
| Issue types, then required fields | `GET /rest/api/{v}/issue/createmeta/{project}/issuetypes`, then `.../issuetypes/{issueTypeId}`: each field has `required`, `allowedValues`, `hasDefaultValue`. The old `GET /rest/api/3/issue/createmeta` is deprecated on Cloud. DC: UNVERIFIED (exists from Jira 8.4 in practice) |
| Create / edit | `POST /rest/api/{v}/issue` / `PUT /rest/api/{v}/issue/{key}` with `{"fields":{...}}` |
| Transitions | `GET /rest/api/{v}/issue/{key}/transitions?expand=transitions.fields` (lists each transition's required fields), then `POST` the same path with `{"transition":{"id":"31"}}` plus any required `fields`. Obtain missing values and get approval for the full payload first. An empty list means no transition is available from the current status |
| Edit-screen fields | `GET /rest/api/{v}/issue/{key}/editmeta` |
| Link types / link | `GET /rest/api/{v}/issueLinkType`; `POST /rest/api/{v}/issueLink` with `{"type":{"name":"Blocks"},"inwardIssue":{"key":"A"},"outwardIssue":{"key":"B"}}` |
| Remote link | `POST /rest/api/{v}/issue/{key}/remotelink` with `{"object":{"url":"https://...","title":"..."}}`; a repeated `globalId` updates instead of duplicating |
| Attachment | `POST /rest/api/{v}/issue/{key}/attachments`, multipart field `file`, header `X-Atlassian-Token: no-check` (blocked without it) |
| Boards / future sprints | `GET /rest/agile/1.0/board?projectKeyOrId=KEY`; `GET /rest/agile/1.0/board/{id}/sprint?state=future` |
| Move to sprint / epic | `POST /rest/agile/1.0/sprint/{id}/issue` or `/rest/agile/1.0/epic/{key}/issue` with `{"issues":["KEY"]}`, max 50 each; the epic call does not work for team-managed epics |

## JQL that is not obvious

- Epic children: on Cloud use `parent = EPIC-1`; it works in company-managed and team-managed projects. `"Epic Link" = EPIC-1` (quoted, two words) is the DC form; Atlassian kept it in Cloud JQL when it deprecated the REST field, but team-managed projects never had it (VERIFIED, deprecation notice 54048).
- Prefer `statusCategory = "In Progress"` or `statusCategory != Done` over workflow status names, which differ per project.
- Cloud JQL user clauses take account ids or `currentUser()`, not usernames.
- Custom fields by id: `cf[10020] = 41`, with the id from `/field`. The `statusCategory` and `cf[...]` forms are not re-checked against Atlassian's JQL fields reference (https://support.atlassian.com/jira-software-cloud/docs/jql-fields/ did not render when checked 2026-11-07): confirm them there or on the instance.
- `issueFunction in hasLinks(...)` and other `issueFunction` clauses need ScriptRunner. Native: `issue in linkedIssues("KEY")` or `issue in linkedIssues("KEY", "is blocked by")`.

## Errors

| Response | Usual cause | Do |
|---|---|---|
| 400 with an `errors` map | A field is required, not on the screen, or in the wrong format (for example a plain string as a v3 `description`) | Look up the named field by operation: create metadata for create, `editmeta` for edit, `transitions?expand=transitions.fields` for a transition. Fix it and re-confirm the payload; on a screen or permission limit, stop and explain instead of retrying from create metadata |
| 401 | Expired token or disconnected MCP | Report it; the user reconnects (`/mcp`) or refreshes the token. Never run `jira init` |
| 403 | Missing project permission (edit, transition, link) | Report the missing permission |
| 404 | Wrong key, or no Browse permission: Jira answers 404 for issues you cannot see | Say both are possible |
