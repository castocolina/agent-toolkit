# Command Creator

An agent skill that turns a workflow you repeat by hand into a Claude Code slash command: a Markdown file in `.claude/commands/` (project) or `~/.claude/commands/` (personal) that you run as `/command-name`. It captures your steps in order, picks the location, writes the frontmatter and argument handling, and adds the stop, approval and retry rules that keep a command safe when a step fails or times out.

The workflow, decision tables, gotchas and validation checklist live in [SKILL.md](SKILL.md); this file only covers setup.

## Installation

**Claude Code:**

```bash
cp -r skills/command-creator ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

Then ask, for example: "I keep running the same release steps by hand; make it a `/release` command for this repo."

## File Structure

```
command-creator/
├── SKILL.md                 # Agent instructions
├── README.md                # This file
├── references/
│   ├── patterns.md          # Body skeletons for the four command patterns
│   └── examples.md          # Four complete commands from the erk project
└── evals/                   # Output evals, trigger queries, fixtures
```

## Credits

The worked examples in `references/examples.md` are real commands from the erk project, adapted here.

## References

- [Claude Code skills and commands](https://code.claude.com/docs/en/skills)
