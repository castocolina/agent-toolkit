---
name: command-creator
description: "Create or update Claude Code slash-command files (.claude/commands/*.md or ~/.claude/commands/): frontmatter, $ARGUMENTS and $0 placeholders, ! pre-run context, approval gates, retry and stop rules. Use when the user wants a reusable /command for a recurring workflow, or describes doing the same multi-step task by hand (a release, a CI fix loop, a PR submission) or keeps pasting the same long prompt, and wants one thing to type instead, even without the words 'slash command'. Not for skills (SKILL.md), subagents (.claude/agents/), shell aliases or scripts, CI workflows, running an existing command, or reviewing or scoring a command file."
---

# Command Creator

Argument placeholders and bang lines are resolved before the model reads a command body. The job is to turn a procedure the user already performs into a body that runs it in the right order, stops at the right points, and survives partial failure.

**This file escapes its own placeholders.** A skill body is substituted on load just like a command, so in this file's source every placeholder written to document one (`\$ARGUMENTS`, `\$0`, `\$version`) carries a backslash before its dollar sign, and bang lines are described in words rather than written out. If you see that backslash, it protects this file only: write placeholders in the command file without it. The files under `references/` are read raw, so their placeholders and bang lines appear exactly as a command file needs them.

## Workflow

1. **Capture the procedure.** Before drafting, ask: what does the user do by hand, in what order, what changes state (local or remote), and what does "done" look like? Use what the user gave (a transcript, a checklist, a description) and ask only about gaps that change behavior, permissions or scope. If the user has not described the workflow at all, ask for its steps; never invent release, deploy or publish actions, arguments or tool integrations. If the user's order puts a side effect before a read-only check (publish before tests, push before lint), say so, propose the safe order, and ask before changing it; never keep or change the order silently.
2. **Command or skill?** Since commands were merged into skills, both create `/name`. Write a command for a single prompt the user starts. If the workflow needs bundled scripts or reference files, say a skill fits better (out of scope here) and stop without writing. If the user still wants a command, write one that calls the existing scripts by path, and flag each script that does not exist yet as a manual step. Before writing, look for `<name>` in `.claude/skills/<name>/`, `~/.claude/skills/<name>/` and the target commands directory. If any exists, write nothing and reply with this template:

   > `/<name>` is already taken by `<existing paths>` (a same-named skill shadows a command with no warning). Options:
   > 1. Rename the new command: `<name>-cmd`, or a namespaced path such as `.claude/commands/<group>/<name>.md`, invoked as `/<group>:<name>`.
   > 2. Update the existing command `<command path>`: with your yes I will read it first, keep its frontmatter unless the change needs it edited, change only what you asked for, and show you the diff. If a same-named skill also exists, the command stays shadowed, so you first approve how that is resolved (rename or remove the skill, your call) before I update.
   > 3. Put the change in the existing skill `<skill path>`: editing a SKILL.md is outside this skill, so I will say what to change and leave the edit to you or a skill-authoring tool.
   >
   > Nothing is written until you choose.

   Offer only the options that apply (no option 2 without an existing command, no option 3 without a skill). Never write a shadowed command, and never overwrite an existing file without the user's yes. On an approved update, carry the chosen resolution forward, do what option 2 says, then run steps 6-7.
3. **Choose the location** (table below). There is no `name` field: the file stem is the name. A subfolder adds a namespace: `.claude/commands/frontend/component.md` is `/frontend:component`.
4. **Choose the pattern** (table below). Read the matching skeleton in [patterns](references/patterns.md) unless the command is one tool call with no argument to validate; do NOT load it for that case.
5. **Write frontmatter and arguments** (sections below). Decide, do not default: `disable-model-invocation: true` if the body commits, pushes, publishes, deploys, sends or deletes; `arguments:` for fixed-shape values and `\$ARGUMENTS` for free text; `argument-hint` exactly when the body reads arguments.
6. **Validate in a loop.** Walk the checklist at the end of this file against the draft, fix every failing item, and walk it again; write the file only when every item passes.
7. **Write and report.** Create the file, then give its path and an invocation that matches `argument-hint`. Never claim it was tested unless you ran it.

Read [examples](references/examples.md) only when the user asks for a worked example, or when the command maps several failing checks to different fixes or needs fixed SUCCESS and STUCK report formats; read only the section for that pattern. Do NOT load it when the skeleton in `patterns.md` already covers the body.

## Location

| Situation | Write to |
| :- | :- |
| Inside a repository, unless the user says global or personal | `.claude/commands/<name>.md` (project; shared through git) |
| User says "global", "personal", "for all my projects", even inside a repository | `~/.claude/commands/<name>.md` |
| Not inside a repository | `~/.claude/commands/<name>.md` |
| Signals conflict ("for my team" with no repository open; "just for me" but they want it committed) | Ask; offer both paths |

The pinned Claude Code docs document the project path only; `~/.claude/commands/` is the long-standing personal location. You cannot see the `/` menu: tell the user to check that `/<name>` appears, and offer the project path if it does not.

## Patterns

| Task shape | Pattern | The body must define |
| :- | :- | :- |
| One bounded action, maybe with arguments (run a script, summarize a file) | Simple execution | argument validation, the exact tool call, what to show |
| Run a check, fix, re-run until it passes | Iterative fixing | a baseline check first; max attempts, each one fix plus a fresh check (default 5 unless the user gives one); a stuck rule from observed results (the same failure, same check and file and message, survives two fix attempts: stop); SUCCESS as soon as a check passes (exit code 0); the stuck report |
| Several steps that commit, push, publish, deploy or send | Workflow with side effects | read-only checks first, the authorization point, what to inspect after a timeout before any retry, the report |
| Draft a plan, wait for approval, then act | Plan, approve, execute | the approval signal, that nothing is written before it, where the approved plan is saved |

Plan, approve, execute is an approval gate, not a delegation pattern. Before delegating any step, ask: what does a subagent give here that the main thread lacks: isolation from a large search, a specialized registered agent, or parallel work? If none, run it directly. When it does help, name an agent type that exists (built-ins: `Explore`, `Plan`, `general-purpose`; check the environment for custom ones) or use `context: fork` with `agent:`. Honor "no agents" when the user says it.

## Frontmatter

Every field is optional. Use only what the body needs:

| Field | Use it when | Fact that matters |
| :- | :- | :- |
| `description` | always | shown in the `/` menu; without it the first body line is used |
| `argument-hint` | the body reads arguments | autocomplete text only: it validates nothing, so the body must check the input. Show required as `<file>`, optional as `[base-branch]` |
| `arguments` | you want named placeholders | `arguments: file lines` makes `\$file`, `\$lines`; a missing named argument becomes empty, which the body can test |
| `disable-model-invocation: true` | the command commits, pushes, publishes, deploys, sends or deletes | otherwise Claude may start it on its own when it judges it relevant |
| `allowed-tools` | the user wants fewer prompts for safe tools | pre-approves tools for the turn; it does not restrict the others (`disallowed-tools` does) |
| `model`, `effort` | the user asks | apply to the rest of the turn |
| `context: fork`, `agent` | an isolated subagent run is worth it (see Patterns) | the body becomes the subagent's task; `agent` defaults to `general-purpose` |

Do not add `name` or `paths`: command files do not accept them. The frontmatter is read only when `---` is on line 1; broken YAML loads the body with no fields and no error.

## Arguments and pre-run context

Before choosing placeholders, ask: is the input free text that may contain spaces (a message, a search string)? Take `\$ARGUMENTS` whole. Is it one or more fixed-shape values (a version, a branch, a file)? Declare them in `arguments:` so the body can test each for empty. Never use `\$1` for the first value.

- `\$ARGUMENTS` is everything after the command name, as typed. If the body has no placeholder, the text is appended as `ARGUMENTS: <value>`.
- `\$0` is the FIRST positional argument (`\$ARGUMENTS[0]`); `\$1` is the second. How a quoted multi-word value is split is not documented, so when a value may contain spaces, take `\$ARGUMENTS` whole.
- A missing indexed placeholder stays literal (`\$1` shows up as that text). In a command file, a dollar sign that must stay literal where it would read as a placeholder (an awk field such as `\$1`) needs a backslash directly before it.
- A bang line is an exclamation mark immediately followed by a backtick-quoted shell command (see the skeleton in `patterns.md`). It runs while the prompt is built, before the model reads a word, and its output replaces it. A failing command aborts the whole invocation, so end context that may be absent with `|| true` (for example `git status --short 2>/dev/null || true`).
- `\${CLAUDE_PROJECT_DIR}` is the project root, for paths that must not depend on the current directory.

## Gotchas

- NEVER put a state-changing command in a bang line: it runs on every invocation, mistaken ones included, before any check, confirmation or approval step the body describes. Use bang lines only for cheap, read-only context.
- NEVER put `\$ARGUMENTS`, `\$0` or a named placeholder inside a bang line: the user's text becomes shell syntax before anything validated it.
- NEVER let the body splice arguments into shell unquoted. `foo\$bar`, `it's` and `a; rm -rf ~` are all realistic input. The body must spell out the encoding step, because the model that runs the command applies it to text nobody has seen yet:
  1. Validate first where the shape is fixed (allowed set or pattern; stop on anything else).
  2. Encode the value as one single-quoted shell word: wrap it in `'...'` and write each `'` inside it as `'\''`. So `it's` becomes `'it'\''s'`, and `a; rm -rf ~` becomes `'a; rm -rf ~'` (inert text).
  3. Place it by role. A positional operand (a path, a ref, a search pattern) goes after the tool's option terminator (`--`, or its own form such as `--end-of-options` for `git rev-parse`): `git add -- '-x'` stages a file named `-x`. An option value stays attached to its option and never goes after `--`: `git commit -m 'it'\''s a; rm -rf ~ test'` records that text as the message. Use fixed-string matching for search text. A value already held to a strict pattern such as `^[0-9]+\.[0-9]+\.[0-9]+$` cannot start with `-` or hold a quote, so it needs neither step 2 nor step 3.

  Example body line: "Search with `rg -n -F -- <encoded text>`; for `it's` that is `rg -n -F -- 'it'\''s'`."
- NEVER retry a publish, push, deploy or send blindly after a timeout: it may have succeeded. The body must say how to check (`npm view <pkg>@<version> version`, `git ls-remote origin refs/tags/v1.2.3 'refs/tags/v1.2.3^{}'`, `gh pr view`) and retry only when the check proves it did not happen.
- A same-named skill in `.claude/skills/` or `~/.claude/skills/` shadows the command with no warning: the user types `/name` and gets the skill. Check before writing (Workflow step 2).
- Frontmatter that does not start on line 1, or YAML that does not parse, is dropped silently, `disable-model-invocation: true` included: a publish command then becomes one Claude may start on its own. Keep `---` on line 1 and quote values that contain `:` or `#`.
- NEVER add a global override (a `git config --global` change, a user-level settings edit) the user did not ask for: it changes behavior for every later run in every project, not just this command.
- NEVER write a step that names a tool or integration the environment lacks (Slack, Jira, a custom agent type). Report it as a manual step, or ask which tool to use.
- Running the command is the user's authorization for what its description says, nothing broader. Anything outside it (a destructive cleanup, a force push, editing files the workflow does not own) needs an explicit confirmation step in the body.

## Worked example

User: "Make a project command that tags and pushes a release; I pass the version." The command file (write `\$version` without the backslash):

````markdown
---
description: Tag the current main commit as a release and push the tag
argument-hint: <version, e.g. 1.4.0>
arguments: version
disable-model-invocation: true
---

1. If `\$version` is empty or does not match `^[0-9]+\.[0-9]+\.[0-9]+$`, stop and ask for a version.
   (This strict pattern is the validation: the value cannot start with `-` or hold a quote.)
2. Check, in order, and stop with the reason on the first failure: the branch is `main`;
   `git status --short` is empty; `git fetch origin refs/heads/main` succeeds;
   `git rev-parse HEAD` equals `git rev-parse --verify FETCH_HEAD`;
   `git rev-parse -q --verify 'refs/tags/v\$version'` finds nothing;
   `git ls-remote origin 'refs/tags/v\$version'` succeeds and prints nothing.
3. Record the intended commit: TARGET = output of `git rev-parse HEAD`.
4. Run `git tag -a 'v\$version' -m 'Release \$version' TARGET` and check its exit status. Non-zero: stop and report
   the error; do not push and do not enter step 5. Zero: run `git push origin 'refs/tags/v\$version'`.
5. Only after a successful local tag: if the push fails or times out, never re-push straight away. Run
   `git ls-remote origin 'refs/tags/v\$version' 'refs/tags/v\$version^{}'`.
   - The query fails or times out: the state is unknown. Stop and report that; do not retry.
   - It succeeds with no output: the tag is not on the remote. Show the push error and ask before one retry.
   - The user declines the retry, or the state stayed unknown: never report success. Say the local tag
     `v\$version` still exists, so a rerun stops at step 2, and offer both ways on: delete it with
     `git tag -d 'v\$version'`, or push it later with `git push origin 'refs/tags/v\$version'`.
   - It succeeds with output: take the `^{}` (peeled) line's commit when present, else the plain tag line's value.
     Equal to TARGET: the push landed; report success. Anything else: report a conflict (someone else's tag)
     and stop; never overwrite it.
6. Report the tag and TARGET.
````

## Checklist

- [ ] The user's steps are all present, with nothing invented; any reorder for safety was proposed and agreed.
- [ ] The location follows the Location table. Creating: no skill or command shares the name. Approved update: the target is the command file the user approved, and any same-named skill was resolved the way the user approved in step 2.
- [ ] `description` is present; `argument-hint` is present exactly when the body reads arguments, and the invocation example matches it.
- [ ] Placeholders are 0-based (`\$0` is the first argument); a dollar sign that must stay literal has a backslash before it.
- [ ] Missing or malformed arguments are checked in the body, which says what happens then.
- [ ] Every argument reaches the shell as one single-quoted word (`'` written as `'\''`): a positional operand after `--` or the tool's own end-of-options form, an option value attached to its option; a value a strict pattern already validated is exempt.
- [ ] Read-only checks come before every side effect; bang lines are read-only and contain no placeholders.
- [ ] Side-effect commands set `disable-model-invocation: true` and confirm anything beyond their stated purpose.
- [ ] Loops have max attempts, a stuck rule and a pass condition; side effects have a post-timeout check before any retry.
- [ ] Every named tool, script and agent type exists in the user's environment, or is flagged as an assumption.
