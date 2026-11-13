# Jira Skill

Lets an agent read and change live Jira issues through the [jira CLI](https://github.com/ankitpokhrel/jira-cli), the Atlassian MCP server or the Jira REST API, on Jira Cloud or Data Center. Every change is fetched, shown, approved, applied and read back. `SKILL.md` holds the routing, the deployment differences, the change procedure and the gotchas.

## When it triggers

Requests that act on Jira: viewing or searching issues (keys like `PROJ-123`, JQL), creating stories, tasks and bugs, editing, commenting, transitioning, linking, and putting work into a sprint or under an epic. It also drafts clearly fictional Jira or JQL examples for tutorials without touching Jira. It is not for summarizing pasted ticket text, generic estimation, GitHub or Linear issues, Jira administration or MCP server setup.

## Installation

**Claude Code:**

```bash
cp -r skills/jira ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

It needs one backend: the jira CLI configured with `jira init` (run it yourself; it is interactive), or the Atlassian MCP server connected to your site. REST calls are used only when credentials are already on the machine.

## File structure

```
jira/
├── SKILL.md                  # Routing, deployment table, change procedure, gotchas
├── README.md                 # This file
├── references/
│   ├── commands.md           # jira CLI syntax, checked against its source
│   ├── mcp.md                # MCP tool names (v1 and v2), REST calls, JQL pitfalls, errors
│   └── story-anatomy.md      # Story and task house rules: statement, sections, epic, sprint, assignee
└── evals/
    ├── evals.json            # Output evals
    ├── trigger-queries.json  # Trigger evals
    └── files/                # Eval inputs (backend responses, batch log)
```

`story-anatomy.md` holds the repository owner's house policy for stories and tasks; claims in the references carry VERIFIED, SOURCED or UNVERIFIED tags.

## Resources

- [jira-cli](https://github.com/ankitpokhrel/jira-cli)
- [Atlassian Rovo MCP server: supported tools](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/)
- [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Jira Software Cloud (Agile) REST API](https://developer.atlassian.com/cloud/jira/software/rest/intro/)
- [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
- Mike Cohn, [User Stories](https://www.mountaingoatsoftware.com/agile/user-stories) (Mountain Goat Software): the story statement template behind `story-anatomy.md`

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

CLI flags and syntax in `references/commands.md` were checked against the jira-cli v1.7.0 help output and its README and agent skill (ankitpokhrel); MCP and REST facts against Atlassian's published documentation.
