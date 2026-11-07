# Gemini Skill

Runs the Gemini CLI as a headless, read-only second-opinion reviewer for code, architecture and plan reviews and big-context (>200k token) analysis, then verifies each Gemini finding against the source before reporting it. `SKILL.md` holds the runtime rules (approval modes, timeouts, context boundary, gotchas); this file is for people installing or maintaining the skill.

## Installation

**Claude Code:**

```bash
cp -r skills/gemini ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

Requires the Gemini CLI (`npm install -g @google/gemini-cli`) with authentication configured; `gemini --version` confirms it is on `PATH`.

## Files

- `SKILL.md` - defaults, approval-mode table, workflow, command shapes and gotchas.
- `references/model-selection.md` - model choices, loaded only when the model choice matters.
- `references/troubleshooting.md` - hung-run and out-of-memory symptoms, loaded only when a run misbehaves.
- `evals/` - output evals, trigger queries, and fixtures in `evals/files/`.

## Maintenance

Flags, approval modes, exit codes and model names follow the official Gemini CLI docs. Re-check them against the CLI reference and `gemini --help` when the CLI changes.

## Resources

- [Gemini CLI repository and docs](https://github.com/google-gemini/gemini-cli)
- [Gemini CLI Documentation](https://github.com/google/generative-ai-docs)
- [Gemini API Reference](https://ai.google.dev/docs)
- [Model Comparison](https://ai.google.dev/models/gemini)

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

CLI flags, approval modes, exit codes, models and session behavior were checked against the official Gemini CLI documentation (Google).
