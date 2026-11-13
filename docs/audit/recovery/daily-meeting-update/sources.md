# daily-meeting-update: sources (plan 14, batch 5, checked 2026-11-07)

## Origin

- The skill came from softaworks/agent-toolkit. `git show 3027f20f:skills/daily-meeting-update/` has the same README.md, SKILL.md and scripts/claude_digest.py as baseline `dbff837f` (`git diff --stat 3027f20f dbff837f` is empty for the folder).
- Upstream commits touching the path: `ededc4e5` (2026-01-22, "add daily-meeting-update skill for standup generation") and `87afc180` (2026-01-22, "add Claude Code session history integration"), both authored by Leonardo Flores (leonardocouy). `gh api repos/softaworks/agent-toolkit/commits?path=skills/daily-meeting-update` shows nothing newer, and upstream `main` is `3027f20f`, the fork point.
- Current state: the folder has no credit line and no registry row (`docs/audit/upstream-sources.json` has no row with `skill: daily-meeting-update`), unlike `database-schema-designer` and `gemini`, which carry both.
- No uncredited distinctive content beyond that: the October rewrite is our own (window, provenance and consent gates, digest fixes). No web search was needed.

## Missing credit line (add to skills/daily-meeting-update/README.md, last section before `## Installation` or at the end)

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

This is the exact line `skills/database-schema-designer/README.md` and `skills/gemini/README.md` use. Each registry `credit` below must also appear in README.md, SKILL.md or references/ (`audit.py` `credit_issues`), so the README needs one more sentence naming the vendors, in the style of `database-schema-designer`:

```text
Tool and platform facts were checked against the official documentation of Anthropic (Claude Code), GitHub (gh CLI), Atlassian (Jira JQL), ankitpokhrel (jira-cli), Cory Bennett (go-jira) and the Python Software Foundation.
```

## Proposed registry rows (verbatim JSON, to append to docs/audit/upstream-sources.json)

```json
[
  {
    "skill": "daily-meeting-update",
    "kind": "github-path",
    "source": "softaworks/agent-toolkit:skills/daily-meeting-update",
    "ref": "main",
    "credit": "softaworks/agent-toolkit"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "github",
    "source": "ankitpokhrel/jira-cli",
    "ref": "main",
    "credit": "ankitpokhrel"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "go-jira README, configuration and commands (the other tool installed as jira): https://github.com/go-jira/jira",
    "ref": null,
    "credit": "ankitpokhrel"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Claude Code docs, Tools reference (AskUserQuestion): https://code.claude.com/docs/en/tools-reference",
    "ref": null,
    "credit": "Anthropic"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Claude Agent SDK docs, Handle approvals and user input (AskUserQuestion limits): https://code.claude.com/docs/en/agent-sdk/user-input",
    "ref": null,
    "credit": "Anthropic"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Claude Code docs, Manage sessions (where transcripts are stored): https://code.claude.com/docs/en/sessions",
    "ref": null,
    "credit": "Anthropic"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Claude Code docs, Extend Claude with skills (CLAUDE_SKILL_DIR, install paths): https://code.claude.com/docs/en/skills",
    "ref": null,
    "credit": "Anthropic"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Claude Code docs, Permissions (mcp__server__tool naming): https://code.claude.com/docs/en/permissions",
    "ref": null,
    "credit": "Anthropic"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "GitHub CLI manual, gh search prs: https://cli.github.com/manual/gh_search_prs",
    "ref": null,
    "credit": "GitHub"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "GitHub CLI manual, gh pr view: https://cli.github.com/manual/gh_pr_view",
    "ref": null,
    "credit": "GitHub"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Atlassian Support, JQL fields (resolved, updated, time zone): https://support.atlassian.com/jira-software-cloud/docs/jql-fields/",
    "ref": null,
    "credit": "Atlassian"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Atlassian Support, JQL functions (currentUser): https://support.atlassian.com/jira-software-cloud/docs/jql-functions/",
    "ref": null,
    "credit": "Atlassian"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Python docs, zoneinfo: https://docs.python.org/3/library/zoneinfo.html",
    "ref": null,
    "credit": "Python Software Foundation"
  },
  {
    "skill": "daily-meeting-update",
    "kind": "unversioned",
    "source": "Python docs, pathlib (PurePath.is_relative_to): https://docs.python.org/3/library/pathlib.html",
    "ref": null,
    "credit": "Python Software Foundation"
  }
]
```

Notes for the registry: the `github-path` and `github` rows are read by `upstreams` (stale detection); every `unversioned` row is stale-blind (known limit, plan 14 Step 5). The go-jira row reuses the credit `ankitpokhrel` only so the README needs no further name; the controller may give it its own credit (the go-jira author is Cory Bennett, go-jira/jira) and add that name to the README sentence instead.

## Skill-updater style review (REVIEW ONLY, no `track` call, nothing edited)

Reading of `skills/skill-updater/SKILL.md` steps 1-7 applied by hand:

1. Scope: `skills/daily-meeting-update/` exists, not a synced skill.
2. Rows: none for this artifact, and the README holds no credit line naming the upstream. Per step 2 the review proposes the row (above), still does step 6, and gives no `track` call.
3. Upstream change check (step 3-4, run by hand because no row exists): upstream `main` still equals the fork point; the last upstream commit on the path is `87afc180`, which is inside our baseline. There is no upstream change to classify. Result: nothing to adopt, adapt or ignore from upstream; row status after registration would be `current` with `--sha 87afc180`.
4. Model-validity pass (step 6): NOT run. It needs a probe lane (`pi-cmd runner`), which the brief's rails do not give an analyst; the controller can run it. Candidate rules that counter a model habit, with a prompt each:
   - "Omit unpicked sessions silently: never name, count or explain them" (habit: reporting "I left out 2 sessions"). Prompt: a standup request with a 3-session digest, user picks 2.
   - "Never report an investigation or an open PR as delivered" (habit: listing an open PR under Yesterday as done). Prompt: a draft PR and a ticket In Progress, user says "I worked on it".
   - "Never quote session-log text" (habit: pasting titles or prompts). Prompt: a digest with a file named like a secret.
   - "At most 15 bullets, fold minor items" (habit: long lists). Prompt: 25 merged PRs.
   Keep each unless the probe output shows the habit absent.

### Adopt / adapt / ignore items for the restore brief

| item | decision | note |
| --- | --- | --- |
| upstream skill text (everything at `3027f20f`) | ignore | our October rewrite supersedes it on purpose (consent, window, provenance, no log text); restore only through the record rows |
| structured question tool sentence (rows s022, s024, s026) | adapt | name `AskUserQuestion` (the baseline's `AskUserQuestionTool` is stale); up to 4 questions per call fits the four required answers; 2-4 options per question, so for more than 4 sessions list them as a numbered text list instead of multiSelect; it is not available in subagents, so say "when the question tool is available" |
| output template and worked example (rows s013, s031, s036) | adapt | put in `references/output-template.md`; load at step 4; keep the PRs & Reviews `**Opened:**`, `**Merged:**`, `**Reviews:**` lines and the Links footer; show an open or draft PR under Today or In progress and the merged PR under Yesterday (provenance gate); each number carries its title |
| Git commits source (row s023, purpose-change-pending) | recommend ignore (KEEP-CURRENT) | if the user restores it: one query row `git -C REPO log --all --author=<user.email> --since=START --until=END`, activity-not-outcome per the provenance gate |
| `${CLAUDE_SKILL_DIR}` for the digest path | adopt (small fact fix) | replaces "from the skill root"; see facts.md |
| `claude_digest.py`: honor `CLAUDE_CONFIG_DIR`; refresh the stale module docstring | adopt as a script fix | the docstring still shows `"title": "Fix authentication bug"`, `"project": "/home/user/my-app"` and the old default sentence, which contradict the `Session <id>` titles and the `[unresolved project: ...]` value; the script change needs a test in tests/skills/daily-meeting-update |
| README: Python 3.9 or later and `tzdata` on Windows; retention note; credit lines above | adopt | see facts.md and the credit text above |

## Controller one-line rows (go-jira credited to its author, Cory Bennett)

{"skill": "daily-meeting-update", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/daily-meeting-update", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "daily-meeting-update", "kind": "github", "source": "ankitpokhrel/jira-cli", "ref": "main", "credit": "ankitpokhrel"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "go-jira README, configuration and commands (the other tool installed as jira): https://github.com/go-jira/jira", "ref": null, "credit": "Cory Bennett"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Claude Code docs, Tools reference (AskUserQuestion): https://code.claude.com/docs/en/tools-reference", "ref": null, "credit": "Anthropic"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Claude Agent SDK docs, Handle approvals and user input (AskUserQuestion limits): https://code.claude.com/docs/en/agent-sdk/user-input", "ref": null, "credit": "Anthropic"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Claude Code docs, Manage sessions (where transcripts are stored): https://code.claude.com/docs/en/sessions", "ref": null, "credit": "Anthropic"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Claude Code docs, Extend Claude with skills (CLAUDE_SKILL_DIR, install paths): https://code.claude.com/docs/en/skills", "ref": null, "credit": "Anthropic"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Claude Code docs, Permissions (mcp__server__tool naming): https://code.claude.com/docs/en/permissions", "ref": null, "credit": "Anthropic"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "GitHub CLI manual, gh search prs: https://cli.github.com/manual/gh_search_prs", "ref": null, "credit": "GitHub"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "GitHub CLI manual, gh pr view: https://cli.github.com/manual/gh_pr_view", "ref": null, "credit": "GitHub"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Atlassian Support, JQL fields (resolved, updated, time zone): https://support.atlassian.com/jira-software-cloud/docs/jql-fields/", "ref": null, "credit": "Atlassian"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Atlassian Support, JQL functions (currentUser): https://support.atlassian.com/jira-software-cloud/docs/jql-functions/", "ref": null, "credit": "Atlassian"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Python docs, zoneinfo: https://docs.python.org/3/library/zoneinfo.html", "ref": null, "credit": "Python Software Foundation"}
{"skill": "daily-meeting-update", "kind": "unversioned", "source": "Python docs, pathlib (PurePath.is_relative_to): https://docs.python.org/3/library/pathlib.html", "ref": null, "credit": "Python Software Foundation"}
