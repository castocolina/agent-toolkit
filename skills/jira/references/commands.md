# jira CLI reference

Syntax for [ankitpokhrel/jira-cli](https://github.com/ankitpokhrel/jira-cli), checked against its README and source (main branch, 2026-11). Every command below runs without a prompt only with the arguments shown; dropping a required argument opens an interactive prompt that an agent cannot answer.

## Read

```bash
jira issue view KEY --comments 5        # --raw prints the API JSON, --plain prints plain text
jira issue list --plain --paginate 1    # cheapest authenticated read; jira me only prints the saved login
jira issue list --plain --no-headers --columns key,summary,status,assignee
jira issue list -a"$(jira me)" -s"In Progress" -yHigh -tBug -lbackend --created week --updated -2d
jira issue list -q"assignee = currentUser() AND statusCategory != Done"   # raw JQL; configured project ANDed in unless the JQL names a project (SKILL.md gotcha)
jira issue list --paginate 10:50        # start:limit
jira epic list EPIC-1 --plain           # issues in an epic
jira sprint list --current --plain      # issues in the active sprint; --next = next planned sprint
jira sprint list --table --plain --columns id,name,start,state --state future
jira me                                 # prints the login saved by jira init
jira serverinfo                         # prints Version and Deployment Type
```

`jira sprint list` covers only the board saved as `board.id` in the CLI config (SKILL.md gotcha; `-c FILE` or `JIRA_CONFIG_FILE` selects another config) and at most 25 recent sprints. `jira board list` lists the boards of the project.

## Create and edit

```bash
body_file=$(mktemp)
trap 'rm -f "$body_file"' EXIT
cat > "$body_file" <<'EOF'
Markdown body; the CLI converts it to Jira wiki markup.
EOF
jira issue create --no-input --raw -pPROJ -tStory -s"Summary" \
  -a"$(jira me)" -P EPIC-1 -CCheckout -yHigh -lbackend --template "$body_file"

jira issue edit KEY --no-input -s"New summary" < "$body_file"   # edit has no --template; body from stdin replaces the whole description
jira issue edit KEY --no-input -P EPIC-1          # set or change the parent epic
jira issue edit KEY --no-input --label -old --label new --skip-notify
```

- Always pass `--no-input`: without it, create and edit end in an interactive Submit / Add metadata / Cancel menu even when every flag is set. With it, a missing `-s` or `-t` fails at once, but a project-required custom field you did not pass fails only at the API. Get the required list from create-field metadata first (mcp.md); the CLI has no metadata command.
- `-b` beats `--template` and stdin. For multi-line bodies use `--template FILE` on create and stdin on edit, never `$(...)` substitution, which mangles quotes and newlines.
- `--raw` on create prints JSON with the new key for the read-back.
- `--custom name=value` works only for custom fields declared under `issue.fields.custom` in the CLI config; anything else needs MCP or REST.
- On edit, `-l` and `-C` add to the existing labels and components and a leading minus removes one: `--component -OLD --component NEW`. The `-C` help text says "Replace components", but the source sends add/remove operations (VERIFIED, jira-cli `issue/edit` and `pkg/jira/edit.go`).
- `-P` sends `parent` on team-managed projects and writes the epic key into the Epic Link field named by `epic.link` in the CLI config on company-managed ones (VERIFIED, jira-cli source). Whether Cloud still accepts that Epic Link write is UNVERIFIED: re-read the parent and fall back to `jira epic add`.

## Transition, assign, comment

```bash
jira issue move KEY Done --comment "Shipped in 2.4" -RFixed   # exact target status name
jira issue assign KEY "$(jira me)"     # also: default (project default), x (unassign)
jira issue comment add KEY --template "$body_file"
```

- `--comment`, `-R` and `-a` on `move` work only if the transition screen has those fields.

## Epics, sprints, links

```bash
jira epic add EPIC-1 KEY-1 KEY-2        # Agile epic API, up to 50 issues; not for team-managed epics (use edit -P)
jira epic remove KEY-1
jira sprint add SPRINT_ID KEY-1 KEY-2   # up to 50 issues
jira issue link KEY-1 KEY-2 Blocks      # link type name as configured on the instance
jira issue link remote KEY https://github.com/org/repo/pull/7 "PR #7"
jira issue unlink KEY-1 KEY-2
```

- The CLI has no attachment command; use MCP or REST (mcp.md).
