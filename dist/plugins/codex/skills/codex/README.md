Leave a star ⭐ if you like it 😘

# Codex Integration for Claude Code

<img width="2288" height="808" alt="skillcodex" src="https://github.com/user-attachments/assets/85336a9f-4680-479e-b3fe-d6a68cadc051" />


## Purpose
Enable Claude Code to invoke the Codex CLI (`codex exec` and session resumes) for automated code analysis, refactoring, and editing workflows.

## Prerequisites
- `codex` CLI installed and available on `PATH`.
- Codex configured with valid credentials and settings.
- Confirm the installation by running `codex --version`; resolve any errors before using the skill.

## Installation

Install this skill from the agent-toolkit marketplace:

```
claude plugin marketplace add castocolina/agent-toolkit
claude plugin install codex@agent-toolkit
```

The skill is adapted from [skills-directory/skill-codex](https://github.com/skills-directory/skill-codex) (see Credits). That repository keeps its skill under `plugins/skill-codex/skills/codex/` and has no root `SKILL.md`, so copying its repository root into `~/.claude/skills/codex` does not give a loadable skill and installs upstream's text instead of this one.

## Usage

### Important: Thinking Tokens
This skill does not send stderr to `/dev/null`. It captures stdout and stderr in separate logs, keeps stderr out of Claude Code's context on success, and shows it when diagnosing an error or when it holds a relevant warning, because stderr can hold the only useful failure diagnostics. If you want to see the thinking tokens for debugging or insight into Codex's reasoning process, explicitly ask Claude to show them.

### Example Workflow

**User prompt:**
```
Use codex to analyze this repository and suggest improvements for my claude code skill.
```

**Claude Code response:**
Claude will activate the Codex skill and:
1. Use your configured default model unless your prompt names one; valid models come from `codex debug models`.
2. Pick a reasoning effort for the task, or use the one in your prompt; the levels each model accepts (`low`, `medium`, `high`, and on newer models `xhigh`, `max`, `ultra`) are listed by `codex debug models`.
3. Select appropriate sandbox mode (defaults to `read-only` for analysis)
4. Run a command like the following (`<model>` is a model id from `codex debug models`; omit `-m` to use your default; `--skip-git-repo-check` is added only outside a Git repository, with your approval):
```bash
codex exec -m <model> \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  "Analyze this Claude Code skill repository comprehensively..." \
  >codex.stdout.log 2>codex.stderr.log
```

**Result:**
Claude will summarize the Codex analysis output, highlighting key suggestions and asking if you'd like to continue with follow-up actions.

### Detailed Instructions
See `SKILL.md` for complete operational instructions, CLI options, and workflow guidance.

## Credits

Adapted from [skills-directory/skill-codex](https://github.com/skills-directory/skill-codex) (MIT) through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit).

Documentation owners: the Codex CLI and its documentation at https://learn.chatgpt.com/docs are owned by OpenAI. Registry credits for this skill: skills-directory/skill-codex (MIT), via softaworks/agent-toolkit; softaworks; OpenAI.
