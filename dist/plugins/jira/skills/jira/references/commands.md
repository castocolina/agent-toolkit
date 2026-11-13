# jira CLI reference

Syntax for [ankitpokhrel/jira-cli](https://github.com/ankitpokhrel/jira-cli), checked against its README and source (main branch, 2026-11). Every command below runs without a prompt only with the arguments shown; dropping a required argument opens an interactive prompt that an agent cannot answer. The installed CLI's own help is the source of truth for flags and syntax: start with `jira --help`, then `jira <command> <subcommand> --help` (jira-cli's own skill says the same, checked 2026-11-07).

## Read

```bash
jira issue view KEY --comments 5        # --raw prints the API JSON, --plain prints plain text
jira issue list --plain --paginate 1    # cheapest authenticated read; jira me only prints the saved login
jira issue list --plain --no-headers --columns key,summary,status,assignee
jira issue list -a"$(jira me)" -s"In Progress" -yHigh -tBug -lbackend --created week --updated -2d
jira issue list -q"assignee = currentUser() AND statusCategory != Done"   # raw JQL; configured project ANDed in unless the JQL names a project (SKILL.md gotcha)
jira issue list -q"filter='my saved filter'"    # saved filter by name, as raw JQL
jira issue list --paginate 10:50        # start:limit
jira issue list "login error"           # positional text search, like the Jira UI search box
jira issue list --history               # issues you accessed recently
jira issue list -w                      # issues you are watching (--watching)
jira issue list --raw                   # JSON; --csv prints CSV. Parse-safe next to --plain --columns --no-headers
jira epic list EPIC-1 --plain           # issues in an epic
jira sprint list --current --plain      # issues in the active sprint; --next = next planned sprint
jira sprint list --table --plain --columns id,name,start,state --state future
jira me                                 # prints the login saved by jira init
jira serverinfo                         # information about the Jira instance; read its output for the fields
```

`jira sprint list` covers only the board saved as `board.id` in the CLI config (SKILL.md gotcha; `-c FILE` or `JIRA_CONFIG_FILE` selects another config) and only a limited number of sprints: v1.7.0 `jira sprint list --help` says the top 50 and the README says 25 recent (checked 2026-11-07), so narrow the list with `--state` and trust the live output. `jira board list` lists the boards of the project.

## Create and edit

```bash
body_file=$(mktemp)
trap 'rm -f "$body_file"' EXIT
cat > "$body_file" <<'EOF'
Markdown body; the CLI converts it to Jira wiki markup.
EOF
jira issue create --no-input --raw -pPROJ -tStory -s"Summary" \
  -a"$(jira me)" -P EPIC-1 -CCheckout -yHigh -lbackend --template "$body_file"

jira issue create --no-input -pPROJ -tSub-task -P PROJ-123 -s"Sub-task summary"   # sub-task: -P (parent) is mandatory

jira issue edit KEY --no-input -s"New summary" < "$body_file"   # edit has no --template; body from stdin replaces the whole description
jira issue edit KEY --no-input -P EPIC-1          # set or change the parent epic
jira issue edit KEY --no-input --label -old --label new --skip-notify
```

- Always pass `--no-input`: without it, create and edit end in an interactive Submit / Add metadata / Cancel menu even when every flag is set. With it, a missing `-s` or `-t` fails at once, but a project-required custom field you did not pass fails only at the API. Get the required list from create-field metadata first (mcp.md); the CLI has no metadata command.
- `-b` beats `--template` and stdin. For multi-line bodies prefer `--template FILE` on create (documented) and stdin on edit; the help's own multi-line `-b` form is `-b$'line\n\nline'`.
- `--raw` on create prints JSON with the new key for the read-back.
- Sub-task: `-P` is mandatory, and `-t` must name the project's sub-task issue type (`jira issue create --help`: "this field is mandatory when creating a sub-task"; the type name comes from the issue types in the CLI config, checked 2026-11-07). Pass `--no-input` as for any create.
- `--custom name=value` works only for custom fields declared under `issue.fields.custom` in the CLI config; anything else needs MCP or REST. The key is the configured field name lowercased with hyphens (`Story Points` becomes `story-points`; jira-cli's own skill, checked 2026-11-07). The config file (`$XDG_CONFIG_HOME/.jira/.config.yml`, else `~/.config/.jira/.config.yml`; `-c FILE` or `JIRA_CONFIG_FILE` selects another) lists `issue.types` and `issue.fields.custom`, so read it first as a zero-network source before building `create`, `edit` or `--custom`, and print no credentials from it. It can lag behind Jira: if a field is missing, discover it through REST `/field` (mcp.md) and never run `jira init` to refresh it.
- On edit, `-l` and `-C` add to the existing labels and components and a leading minus removes one: `--component -OLD --component NEW`. The `-C` help text says "Replace components", but the source sends add/remove operations (VERIFIED, jira-cli `issue/edit` and `pkg/jira/edit.go`).
- `-P` sends `parent` on team-managed projects and writes the epic key into the Epic Link field named by `epic.link` in the CLI config on company-managed ones (VERIFIED, jira-cli source). Whether Cloud still accepts that Epic Link write is UNVERIFIED: re-read the parent and fall back to `jira epic add`.

## Transition, assign, comment

```bash
jira issue move KEY Done --comment "Shipped in 2.4" -RFixed   # exact target status name
jira issue assign KEY "$(jira me)"     # also: default (project default), x (unassign)
jira issue comment add KEY --template "$body_file"
```

- `--comment`, `-R` and `-a` on `move` work only if the transition screen has those fields.
- A `move` to a status the workflow does not offer fails and the error lists the available states (jira-cli's own skill, checked 2026-11-07). Use that list after a failure; do not probe with a guessed status, because a valid guess executes.

## Epics, sprints, links

```bash
jira epic add EPIC-1 KEY-1 KEY-2        # Agile epic API, up to 50 issues; not for team-managed epics (use edit -P)
jira epic remove KEY-1
jira sprint add SPRINT_ID KEY-1 KEY-2   # up to 50 issues
jira sprint close SPRINT_ID             # alias: complete; SPRINT_ID is the numeric id, e.g. 123
jira issue link KEY-1 KEY-2 Blocks      # link type name as configured on the instance
jira issue link remote KEY https://github.com/org/repo/pull/7 "PR #7"
jira issue unlink KEY-1 KEY-2
```

- `sprint close` affects the whole team and the CLI has no command to reopen a sprint: list its issues first (`jira sprint list SPRINT_ID --plain`), get approval for that exact sprint id (SKILL.md section 3), then re-read the sprint and its issues. What happens to unfinished issues is not in the help (UNVERIFIED; check the read-back).
- The CLI has no attachment command; use MCP or REST (mcp.md).
