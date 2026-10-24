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

Both marketplaces are named `agent-toolkit`, so remove the old one first: `claude plugin marketplace remove agent-toolkit`, then run the add command above. Plugins you installed from the old marketplace are uninstalled by the remove; reinstall the ones you want with `claude plugin install <plugin>@agent-toolkit`.

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

You can also **Enable auto-update** to get the latest versions automatically.

### Manual install (skills only)

**Claude Code** — from a clone of the repo:

```bash
mkdir -p ~/.claude/skills && cp -r skills/<skill-name> ~/.claude/skills/
```

**Other harnesses** — replace `<dir>` with the harness directory from the table:

```bash
T=$(mktemp -d) && git clone --depth 1 https://github.com/castocolina/agent-toolkit.git "$T" && mkdir -p ~/<dir> && cp -r "$T"/skills/. ~/<dir>/ && rm -rf "$T"
```

| Harness | `<dir>` |
|---------|---------|
| Codex | ~/.agents/skills |
| Cursor | ~/.agents/skills |
| GitHub Copilot CLI | ~/.agents/skills |
| opencode | ~/.agents/skills |
| pi | ~/.agents/skills |

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
| 📝 Documentation | [backend-to-frontend-handoff-docs](skills/backend-to-frontend-handoff-docs/README.md) | API handoff docs for frontend |
| 📝 Documentation | [c4-architecture](skills/c4-architecture/README.md) | C4 architecture diagrams with Mermaid |
| 📝 Documentation | [crafting-effective-readmes](skills/crafting-effective-readmes/README.md) | Write effective README files |
| 📝 Documentation | [draw-io](skills/draw-io/README.md) | Create & edit draw.io diagrams |
| 📝 Documentation | [excalidraw](skills/excalidraw/README.md) | Work with Excalidraw diagrams |
| 📝 Documentation | [frontend-to-backend-requirements](skills/frontend-to-backend-requirements/README.md) | Document API requirements |
| 📝 Documentation | [marp-slide](skills/marp-slide/README.md) | Professional presentation slides |
| 📝 Documentation | [mermaid-diagrams](skills/mermaid-diagrams/README.md) | Software diagrams with Mermaid |
| 📝 Documentation | [writing-clearly-and-concisely](skills/writing-clearly-and-concisely/README.md) | Clear, professional writing |
| 🎨 Design & Frontend | [design-system-starter](skills/design-system-starter/README.md) | Create design systems |
| 🎨 Design & Frontend | [mui](skills/mui/README.md) | Material-UI v7 patterns |
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
