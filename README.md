# Agent Toolkit

Opinionated skills shared by [@leonardocouy](https://github.com/leonardocouy) for improving daily work efficiency with Claude Code. Skills are packaged instructions and scripts that extend agent capabilities across development, documentation, planning, and professional workflows.

Fork of [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Skills follow the [Agent Skills](https://agentskills.io/) format.

---

## 🧭 Quick Navigation

**[🚀 Installation](#-installation)** • **[📚 Available Skills](#-available-skills)** • **[🤖 Agents & Commands](#-agents--commands)** • **[📖 Skill Structure](#-skill-structure)** • **[🤝 Contributing](#-contributing)** • **[📄 License](#-license)** • **[🔗 Links](#-links)**

---

## 🚀 Installation

### Claude Code (skills, agents, commands)

```bash
claude plugin marketplace add castocolina/agent-toolkit

# Install specific skill
claude plugin install humanizer@agent-toolkit
claude plugin install codex@agent-toolkit

# Install specific agent
claude plugin install agent-codebase-pattern-finder@agent-toolkit

# Install specific command
claude plugin install command-codex-plan@agent-toolkit
```

Interactive alternative: run `/plugin` inside Claude Code.

### Switching from the upstream marketplace

Both marketplaces are named `agent-toolkit`, so remove the old one first.

> **Warning:** removing a marketplace uninstalls the plugins you installed from it and deletes their saved options, secrets and data where it can. Note any plugin settings you need before you run it.

`claude plugin marketplace remove agent-toolkit`, then run the add command above. Plugins you installed from the old marketplace are uninstalled by the remove; reinstall the ones you want with `claude plugin install <plugin>@agent-toolkit`.

### Codex, Cursor, GitHub Copilot CLI, opencode, pi (skills only)

| Harness | Project scope | User scope |
|---------|---------------|------------|
| Codex | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a codex -y` | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a codex -g -y` |
| Cursor | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a cursor -y` | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a cursor -g -y` |
| GitHub Copilot CLI | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a github-copilot -y` | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a github-copilot -g -y` |
| opencode | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a opencode -y` | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a opencode -g -y` |
| pi | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a pi -y` | `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a pi -g -y` |

Install every skill at once: `npx -y skills add castocolina/agent-toolkit --skill '*' -a codex -y`

Agents and commands are Claude Code-only.

### Available Plugins

Each skill, agent, and command is an individual plugin that can be installed separately:

- **Skills** → See [Available Skills](#-available-skills) for the full list
- **Agents** → See [Agents](#agents) (install as `agent-<name>@agent-toolkit`)
- **Commands** → See [Slash Commands](#slash-commands) (install as `command-<name>@agent-toolkit`)

### Update Plugins

```bash
claude plugin marketplace update agent-toolkit
```

You can also **Enable auto-update** to get the latest versions automatically (in `/plugin` → Marketplaces → agent-toolkit).

### Manual install (skills only)

**Claude Code** — from a clone of the repo:

```bash
mkdir -p ~/.claude/skills && cp -r skills/<skill-name> ~/.claude/skills/
```

**Other harnesses** — replace `<dir>` with the harness directory from the table. The command installs every skill and replaces any same-named skill already in that directory; to install one skill, use `cp -r "$T"/skills/<skill-name> ~/<dir>/` instead of the `cp -r "$T"/skills/. ~/<dir>/` step.

```bash
T=$(mktemp -d) && git clone --depth 1 https://github.com/castocolina/agent-toolkit.git "$T" && mkdir -p ~/<dir> && cp -r "$T"/skills/. ~/<dir>/ && rm -rf "$T"
```

| Harness | `<dir>` |
|---------|---------|
| Codex | `.agents/skills` |
| Cursor | `.agents/skills` |
| GitHub Copilot CLI | `.agents/skills` |
| opencode | `.agents/skills` |
| pi | `.agents/skills` |

Today the `skills` CLI installs every harness above into the shared `.agents/skills` directory (verified 2026-10-24).

**For claude.ai** — Skills only

Add skills to project knowledge or paste SKILL.md contents into the conversation.

---

## 📚 Available Skills

| Category | Skill | Description |
|----------|-------|-------------|
| 🤖 AI Tools | [codex](skills/codex/README.md) | Advanced code analysis with GPT-5.2 |
| 🤖 AI Tools | [gemini](skills/gemini/README.md) | Large-scale review (200k+ context) |
| 🤖 AI Tools | [perplexity](skills/perplexity/README.md) | Web search & research |
| 🔮 Meta | [agent-md-refactor](skills/agent-md-refactor/README.md) | Refactor bloated agent instruction files |
| 🔮 Meta | [command-creator](skills/command-creator/README.md) | Create Claude Code slash commands |
| 🔮 Meta | [plugin-forge](skills/plugin-forge/README.md) | Build Claude Code plugins & manifests |
| 🔮 Meta | [skill-judge](skills/skill-judge/README.md) | Evaluate skill design quality |
| 🧩 Meta | [skill-updater](skills/skill-updater/README.md) | Check skills, commands and agents against their sources and models |
| 📝 Documentation | [backend-to-frontend-handoff-docs](skills/backend-to-frontend-handoff-docs/README.md) | API handoff docs for frontend |
| 📝 Documentation | [c4-architecture](skills/c4-architecture/README.md) | C4 architecture diagrams with Mermaid |
| 📝 Documentation | [crafting-effective-readmes](skills/crafting-effective-readmes/README.md) | Write effective README files |
| 📝 Documentation | [draw-io](skills/draw-io/README.md) | Create & edit draw.io diagrams |
| 📝 Documentation | [pr-diagrams](skills/pr-diagrams/README.md) | Render draw.io PR diagrams, attach them with gh and reuse them in promotion PRs |
| 📝 Documentation | [excalidraw](skills/excalidraw/README.md) | Work with Excalidraw diagrams |
| 📝 Documentation | [frontend-to-backend-requirements](skills/frontend-to-backend-requirements/README.md) | Document API requirements |
| 📝 Documentation | [marp-slide](skills/marp-slide/README.md) | Professional presentation slides |
| 📝 Documentation | [mermaid-diagrams](skills/mermaid-diagrams/README.md) | Software diagrams with Mermaid |
| 📝 Documentation | [writing-clearly-and-concisely](skills/writing-clearly-and-concisely/README.md) | Clear, professional writing |
| 🎨 Design & Frontend | [design-system-starter](skills/design-system-starter/README.md) | Create design systems |
| 🎨 Design & Frontend | [mui](skills/mui/README.md) | Material-UI v7 patterns |
| 🎨 Design & Frontend | [ui-ux-principles](skills/ui-ux-principles/README.md) | Eight UI/UX rules for building and reviewing screens |
| 🎨 Design & Frontend | [openapi-to-typescript](skills/openapi-to-typescript/README.md) | Convert OpenAPI to TypeScript |
| 🎨 Design & Frontend | [react-dev](skills/react-dev/README.md) | Type-safe React 18-19 with TypeScript |
| 🎨 Design & Frontend | [react-useeffect](skills/react-useeffect/README.md) | React useEffect best practices |
| 🛠️ Development | [database-schema-designer](skills/database-schema-designer/README.md) | Design robust database schemas |
| 🛠️ Development | [dependency-updater](skills/dependency-updater/README.md) | Smart dependency management |
| 🛠️ Development | [naming-analyzer](skills/naming-analyzer/README.md) | Suggest better variable/function names |
| 🛠️ Development | [lesson-learned](skills/lesson-learned/README.md) | Extract SE lessons from recent code changes |
| 🛠️ Development | [reducing-entropy](skills/reducing-entropy/README.md) | Minimize codebase size |
| 🛠️ Development | [session-handoff](skills/session-handoff/README.md) | Seamless AI session transfers |
| 🎯 Planning | [game-changing-features](skills/game-changing-features/README.md) | Find 10x product opportunities |
| 🎯 Planning | [gepetto](skills/gepetto/README.md) | Detailed implementation planning |
| 🎯 Planning | [requirements-clarity](skills/requirements-clarity/README.md) | Clarify requirements before coding |
| 🎯 Planning | [ship-learn-next](skills/ship-learn-next/README.md) | Turn learning into actionable reps |
| 👔 Professional | [daily-meeting-update](skills/daily-meeting-update/README.md) | Interactive daily standup generator |
| 👔 Professional | [difficult-workplace-conversations](skills/difficult-workplace-conversations/README.md) | Navigate difficult conversations |
| 👔 Professional | [feedback-mastery](skills/feedback-mastery/README.md) | Deliver constructive feedback |
| 👔 Professional | [professional-communication](skills/professional-communication/README.md) | Technical communication guide |
| 🧪 Testing | [qa-test-planner](skills/qa-test-planner/README.md) | Comprehensive QA test planning |
| 📦 Git | [commit-work](skills/commit-work/README.md) | High-quality git commits |
| 🔧 Utilities | [datadog-cli](skills/datadog-cli/README.md) | Debug with Datadog logs & metrics |
| 🔧 Utilities | [domain-name-brainstormer](skills/domain-name-brainstormer/README.md) | Generate & check domain names |
| 🔧 Utilities | [humanizer](skills/humanizer/README.md) | Remove AI writing patterns |
| 🔧 Utilities | [meme-factory](skills/meme-factory/README.md) | Generate memes with API |
| 🔧 Utilities | [jira](skills/jira/README.md) | Natural language Jira interaction |
| 🔧 Utilities | [web-to-markdown](skills/web-to-markdown/README.md) | Convert webpages to Markdown |

---

## 🤖 Agents & Commands

> **Requires [Claude Code CLI](https://docs.anthropic.com/claude-code)** — These agents and commands are exclusive to Claude Code users.
>
> For full access, add the marketplace and install plugins:
> ```bash
> claude plugin marketplace add castocolina/agent-toolkit
> claude plugin install codex@agent-toolkit
> ```

### Agents

Specialized sub-agents that Claude Code can delegate tasks to:

| Agent | Description |
|-------|-------------|
| ascii-ui-mockup-generator | Visualize UI concepts through ASCII mockups |
| codebase-pattern-finder | Find similar implementations and patterns |
| communication-excellence-coach | Email refinement, tone calibration, roleplay |
| general-purpose | Default agent for complex multi-step tasks |
| mermaid-diagram-specialist | Create flowcharts, sequence diagrams, ERDs |
| ui-ux-designer | Research-backed UI/UX design feedback |

### Slash Commands

Reusable workflows invoked with `/command-name`:

| Command | Description |
|---------|-------------|
| `/codex-plan` | Create implementation plans using Codex 5.2 |
| `/compose-email` | Draft professional emails |
| `/explain-changes-mental-model` | Build mental model of code changes |
| `/explain-pr-changes` | Generate PR summaries |
| `/sync-branch` | Sync feature branch with main |
| `/sync-skills-readme` | Update README skills table |
| `/viral-tweet` | Optimize tweet ideas for X engagement |

---

## 📖 Skill Structure

Each skill contains:
- `SKILL.md` - Detailed instructions for the agent (with YAML frontmatter)
- `README.md` - User-friendly documentation with examples
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)

---

## Automated audits

Scheduled skill audits compare non-synced skills against the pinned skill rubric, collect eval evidence, and may open a review PR. The schedule is opt-in: `AUDIT_ENABLED` must be `true`; workflow dispatch remains available for forced runs and drills. The workflow also uses `AUDIT_PR_DIAGRAMS` (`none`, `mermaid`, or `drawio`; default `mermaid`), `AUDIT_RESEARCH_MODELS` (a comma-separated list of judge model IDs) and `AUDIT_MERGER_MODEL` (the model for rubric refreshes, merge decisions, fixes, upstream recommendations, and evals).

### Phase 1 knobs

All knobs are repository variables. An unset or empty variable takes the default below. The workflows validate the values (`audit.py validate-knobs`) and fail closed on an invalid one.

| Name | Default | Meaning |
|---|---|---|
| `AUDIT_ENABLED` | unset | `true` turns the schedule on. Dispatch works either way, so forced runs and drills are possible while it is unset. |
| `AUDIT_INTERVAL_DAYS` | `15` | `15` or `30`; scheduled runs only. A scheduled run inside the interval does no spec fetch, starts no model and writes no state. |
| `AUDIT_RESEARCH_MODELS` | `auto` | Comma list of model IDs or `auto`; one or two judge lanes (two lanes must differ). |
| `AUDIT_MERGER_MODEL` | `auto` | Editing agents: rubric refresh, merge decision, fixer, PR body, upstream recommendations. |
| `AUDIT_REVIEW_MODEL` | empty (review off) | PR reviewer model, for example Opus; `auto` is allowed. Set it only after the containment drill passes (UNVERIFIED, see below). |
| `AUDIT_REVIEW_EFFORT` | `high` | Reviewer reasoning effort: `none`, `minimal`, `low`, `medium`, `high`, `xhigh` or `max`. The local CLI 1.0.103 help lists these levels; Actions behavior is UNVERIFIED. |
| `AUDIT_ON_POSITIVE` | `label` | `none` or `label`. `label` adds `audit-review:positive` to a positive review; `none` adds no label. |
| `AUDIT_AUTOMERGE` | unset | Accepted, not acted on in Phase 1 (see Automerge below). |
| `AUDIT_PR_DIAGRAMS` | `mermaid` | `none`, `mermaid` or `drawio`. |

The Phase 1 configuration uses `AUDIT_RESEARCH_MODELS=auto`, `AUDIT_MERGER_MODEL=auto`, `AUDIT_INTERVAL_DAYS=15` and `AUDIT_PR_DIAGRAMS=mermaid`, with `AUDIT_ENABLED`, `AUDIT_REVIEW_MODEL` and `AUDIT_AUTOMERGE` left unset. A second judge lane is a later edit of `AUDIT_RESEARCH_MODELS`.

**PR review.** `skill-audit-review.yaml` reviews each audit PR after `apply`, and on dispatch with a PR number to retry. The reviewer is read-only: `.github/audit/copilot-review.sh` allows the read tool only, has no shell, and gets no GitHub token. A trusted validator checks its answer. The review publishes the commit status `skill-audit/review` on the PR head and one `audit-review:*` label. A push to the PR removes the review labels, and the new head has no status yet. A reviewer error, an `unsure` verdict, an invalid answer, a truncated diff or a failed gate can never produce a positive outcome; it yields `needs-human` or `changes`.

**Fail-safe: the reviewer is off until the containment drill passes.** While `AUDIT_REVIEW_MODEL` is empty, the review job labels the PR `audit-review:skipped`, runs no gate and posts no status. Set `AUDIT_REVIEW_MODEL` only after the drill in `docs/audit/ci-spike.md` (Phase 1 spike additions, item 11) shows that the reviewer cannot run a shell command, write a file or fetch a URL. Until then every review outcome in Actions is UNVERIFIED.

**Automerge.** `AUDIT_AUTOMERGE=true` is accepted but not acted on in Phase 1. When it is set to `true`, the review posts a notice on the PR, once, saying so. No auto-merge is armed and no merge call exists in Phase 1. Automerge returns in Phase 2, after the spike verifies how `gh pr merge --auto` binds to a head SHA (UNVERIFIED).

Before enabling scheduled runs, check the repository's default workflow-token setting with `gh api repos/{owner}/{repo}/actions/permissions/workflow --jq .default_workflow_permissions`. Every audit job declares its own `permissions:`, so the audit must behave the same under `read` and `write`; this check is pending the spike, so do not assume it is verified. The partial spike confirms only local Copilot CLI flags. Its Actions installation/authentication, tool behavior in Actions, review workflow events, repository settings, and available models remain UNVERIFIED until the spike is run. `astral-sh/setup-uv` is pinned to a commit SHA (`0c5e2b8115b80b4c7c5ddf6ffdd634974642d182`, tag `v5.4.1`). The workflow still installs the Copilot CLI with an unversioned `npm install -g @github/copilot`: that version is UNVERIFIED until the spike records it, and pinning it is tracked in `docs/audit/ci-spike.md`.

An `audit-upstream` issue lists stale inspiration sources with update/ignore recommendations. Recommendations do not authorize changes. To approve specific rows, dispatch `skill-audit.yaml` with `approved_upstreams` set to the exact comma-separated `skill|source` keys from that issue. The workflow validates the keys against currently stale rows and treats the approval as applying only to those rows; supplying approvals also forces a run. Unapproved stale sources remain report-only. You can also update a skill manually.

The apply job builds the PR body with a body-only Copilot prompt: the diff stat, a trimmed diff (~60KB cap) and the decision rationale go into the prompt and the body comes back on stdout, following the section structure of `commands/explain-pr-changes.md`; if Copilot fails or returns an empty body, a plain generated summary is used and the fallback is logged. `AUDIT_PR_DIAGRAMS=drawio` currently logs a warning and renders with mermaid: the drawio CLI cannot be installed reliably on a hosted runner yet (UNVERIFIED pending the spike), so xvfb is not installed.

### Required secrets and variables

Secrets and variables must be configured in the repository settings; workflow jobs receive them through their explicit job environments.

| Name | Kind | Purpose |
|---|---|---|
| `COPILOT_GITHUB_TOKEN` | Secret | Fine-grained PAT with Copilot Requests access, used by the Copilot CLI jobs, including the PR reviewer in `skill-audit-review.yaml`. |
| `AUDIT_BOT_TOKEN` | Secret | Fine-grained PAT with read/write Contents, Pull requests, Issues (including labels), and Variables access. Used for PR/issue operations and to write `AUDIT_LAST_STATE`; `variables` is not a `GITHUB_TOKEN` permission. Phase 1 adds no permission to this token: review statuses and labels go through the workflow token (UNVERIFIED in Actions, see `docs/audit/ci-spike.md`). |
| `AUDIT_RESEARCH_MODELS` | Variable | Comma-separated Copilot judge model IDs; entries are trimmed and blanks removed. |
| `AUDIT_MERGER_MODEL` | Variable | Model used for rubric refresh, decision, fixer, upstream recommendations, and eval runner. |
| `AUDIT_PR_DIAGRAMS` | Variable | PR diagram format: `none`, `mermaid` (default), or `drawio`. `drawio` currently falls back to `mermaid` with a warning because the drawio CLI cannot be installed reliably on a hosted runner yet (UNVERIFIED). |
| `AUDIT_ENABLED` | Variable | Set to `true` to enable scheduled runs; dispatch is not disabled by this switch. |
| `AUDIT_INTERVAL_DAYS` | Variable | `15` (default) or `30`; scheduled runs only. |
| `AUDIT_REVIEW_MODEL` | Variable | PR reviewer model. Empty (default) turns the review off. |
| `AUDIT_REVIEW_EFFORT` | Variable | Reviewer reasoning effort (default `high`). |
| `AUDIT_ON_POSITIVE` | Variable | `label` (default) or `none`. |
| `AUDIT_AUTOMERGE` | Variable | Accepted, not acted on in Phase 1. |
| `AUDIT_LAST_STATE` | Variable | Audit state (`judge_sha`, judged skill tree SHAs, and recorded stale-upstream dates); written by the `state`, `checkpoint` and `attempt` jobs; failures keep the detect-owned baseline and `checked_at`. |

## 🤝 Contributing

Contributions are welcome! When adding new skills:

1. Follow the [Agent Skills](https://agentskills.io/) format
2. Include both `SKILL.md` (for agents) and `README.md` (for users)
3. Add YAML frontmatter to `SKILL.md` with `name:` and `description:` fields
4. Update this README.md with a link to your skill

---

## 📄 License

MIT

---

## 🔗 Links

- [Agent Skills Format](https://agentskills.io/)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [GitHub Repository](https://github.com/castocolina/agent-toolkit)
