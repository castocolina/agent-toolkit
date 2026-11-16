# jira: sources (plan 14, batch 6, review only, 2026-11-07)

## Origin

- `skills/jira/` was added by Leonardo Flores (`@leonardocouy`) in softaworks/agent-toolkit commit `50760984` on 2026-01-21 (`feat: add jira skill for natural language Jira interaction`).
- `git diff 3027f20f dbff837f -- skills/jira` is empty: the baseline (2026-09-30) is byte for byte the softaworks original. Everything since is this repository's rewrite.
- Upstream today: `gh api repos/softaworks/agent-toolkit/commits?path=skills/jira` returns only `50760984`, so upstream has not changed since the fork. Nothing to adopt from it.
- No other origin was found: no credit line in README, SKILL.md or the references, and no distinctive uncredited text (the content is generic Jira usage). The root `README.md` lists the skill without a credit line. The registry has no `jira` row; `docs/audit/upstream-sources.md` lists jira only as `incidental-link`.

## Missing credit line

`skills/jira/README.md` has no credit line, while its siblings from the same upstream carry one (`skills/gemini/README.md` line 37, `skills/database-schema-designer/README.md` line 43). Line to add at the end of `skills/jira/README.md`, copied from them:

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

No credit, attribution or license line exists in the artifact that could be lost; none was touched.

## Proposed registry rows (docs/audit/upstream-sources.json)

Each row below passes `validate_entry` (checked with `scripts/audit/audit.py`, see Validation).

```text
{"skill": "jira", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/jira", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "jira", "kind": "github-path", "source": "ankitpokhrel/jira-cli:README.md", "ref": "main", "credit": "ankitpokhrel"}
{"skill": "jira", "kind": "github-path", "source": "ankitpokhrel/jira-cli:skills/jira-cli/SKILL.md", "ref": "main", "credit": "ankitpokhrel"}
{"skill": "jira", "kind": "unversioned", "source": "Atlassian Rovo MCP server, Supported tools: https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/", "ref": null, "credit": "Atlassian"}
{"skill": "jira", "kind": "unversioned", "source": "The Jira Cloud platform REST API (v3, OpenAPI): https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/", "ref": null, "credit": "Atlassian"}
{"skill": "jira", "kind": "unversioned", "source": "Jira Software Cloud REST API (Agile): https://developer.atlassian.com/cloud/jira/software/rest/intro/", "ref": null, "credit": "Atlassian"}
{"skill": "jira", "kind": "unversioned", "source": "Atlassian Document Format, structure: https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/", "ref": null, "credit": "Atlassian"}
{"skill": "jira", "kind": "unversioned", "source": "Deprecation of the Epic Link, Parent Link and other related fields in REST APIs and webhooks: https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-and-webhooks/54048", "ref": null, "credit": "Atlassian"}
{"skill": "jira", "kind": "unversioned", "source": "Retrieve Linked Work Items by Link Type in Jira Cloud: https://support.atlassian.com/jira/kb/how-to-retrieve-linkedissues-of-a-particular-issuelinktype/", "ref": null, "credit": "Atlassian"}
{"skill": "jira", "kind": "unversioned", "source": "Mike Cohn, User Stories (Mountain Goat Software): https://www.mountaingoatsoftware.com/agile/user-stories", "ref": null, "credit": "Mike Cohn"}
```

Notes on the rows:

- The two jira-cli rows are `github-path` so `upstreams` can flag drift. jira-cli's README changes often, so expect `stale: true` noise on that row; the commands.md values were checked against the v1.7.0 binary's `--help` as well (facts.md).
- The Atlassian KB page `.../retrieve-all-child-and-linked-work-items-of-an-epic-in-jira-cloud/` (epic children by `parent`) and `support.atlassian.com/jira-software-cloud/docs/what-is-an-issue/` (key format) were also read for facts; they are not worth a row of their own (the second backs only a dropped section). Add them as `unversioned` rows if the controller wants every page used.
- `upstreams` always reports `stale: false` for `unversioned` rows (known limit in the plan); the date in facts.md is the age marker.

## Skill-updater style review (REVIEW ONLY, no `track` call)

Step 2 of the updater: the artifact has no registry row and no credit line naming an upstream, so no `track` call is possible; the proposed rows above come first and `track` follows once they are committed.

softaworks original: unchanged since the fork. Decision: ignore (nothing new).

jira-cli's own agent skill, `skills/jira-cli/SKILL.md` (added 2026-10-15, commit `9c5bae80`, 83 lines), compared with our SKILL.md and commands.md:

| item | decision | note for the restore brief |
| --- | --- | --- |
| "Start with `jira --help`; the installed CLI's help is the source of truth" | adopt | one pointer line at the top of commands.md; it is the point-do-not-pin rule from the vendor |
| `--raw` (JSON) and `--csv` machine-readable output | adapt | commands.md already uses `--plain --columns --no-headers`; add `--raw` and `--csv` to the Read block as the parse-safe options |
| config file path (`$XDG_CONFIG_HOME/.jira/.config.yml`, else `~/.config/.jira/.config.yml`) and reading `issue.types` and `issue.fields.custom` before `create`, `edit` or `--custom` | adapt | our rule discovers custom field ids through REST `/field`; add the config as a first, zero-network source, and keep "never run `jira init`" (their rule: never without explicit confirmation) |
| `--custom key=value` key is the lowercased field name with hyphens (`Story Points` becomes `story-points`) | adopt | one line in commands.md beside the existing `--custom` bullet |
| invalid `jira issue move` state fails and lists the available states | adapt | worth one sentence: after a failed move, the error lists the states; keep our rule not to probe with a guessed state, because a valid guess executes |
| JQL patterns: `project IN (A, B)`, saved filter `filter='name'`, backlog query `sprint is empty and issuetype not in (Epic, Sub-task)`, a `project` clause in the JQL wins over `-p` | adapt | the project-precedence point is already our gotcha; add the saved-filter form |
| safe execution: never expose `JIRA_API_TOKEN` or config credentials, `--debug` may print auth headers; confirm destructive or externally visible changes; cache discoveries for the session | adopt | add the `--debug` warning to the token rule in mcp.md REST fallback; the rest is already in SKILL.md section 3 |
| nothing in it on sub-tasks, sprint close or `--history` | n/a | those come from our own restore rows (s045, s046, s050) |

From the v1.7.0 `--help` (not from a source row): `jira issue comment add --internal` (internal comment), the positional comment body, and the `-s~Open` negation and `-ax` unassigned filters are not in commands.md. Decision: adapt, optional one-liners; they are current-API details a model may not know.

From the Atlassian supported-tools page: v2 tools mcp.md does not list (`listJiraProjects`, `listJiraIssueChangelogs`, `listJiraIssueComments`, `listJiraIssueAssignableUsers`, `listJiraFilters`, `listJiraStatuses`, `getJiraBoardConfig`, `watchJiraIssue`, `addOrEditJiraIssueWorklog`, `convertJiraIssueHierarchy`, `downloadJiraIssueAttachment`; the delete tools are disabled by default). Decision: adapt as a pointer sentence in mcp.md ("other tools: see the supported-tools page; read the live schema"), plus the `listJiraProjects` row that the s035 restore needs; do not pin the whole catalog (it churns).

Model-validity pass: not run. The updater's pass sends a probe prompt through a model lane, and the batch rails forbid the analyst from using LLM lanes. Rules in this skill that counter a model habit and would be probed by the controller if wanted: epic linking through `jira issue link` (habit: treat an Epic link type as the parent), assigning by display name, interactive commands without `--no-input`, and reporting the create response instead of a read-back.

## Validation

Registry rows were validated with `validate_entry` from `scripts/audit/audit.py` (script: `tmp/jira-validate.py` in the worktree); result recorded in the analyst report.
