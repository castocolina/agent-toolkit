# Marp Slide Creator

A skill for creating and redesigning [Marp](https://marp.app/) Markdown slide decks. It ships seven ready-to-copy deck templates with embedded CSS (default, minimal, business, tech, dark, gradient, colorful), a render-and-fix check with Marp CLI, and notes on the Marp behavior that silently breaks decks. `SKILL.md` holds the workflow, the style table and the gotchas.

## When it triggers

Requests for slides, a presentation, deck, talk, lecture or seminar slides, custom Marp theme CSS, or making an existing deck less crowded or better looking. It is not for `.pptx` editing, export-only requests, summaries or speaker scripts.

## Installation

**Claude Code:**

```bash
cp -r skills/marp-slide ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

Rendering checks use Marp CLI (`npx @marp-team/marp-cli`); PDF, PPTX and PNG output also need Chrome, Edge or Firefox. Without the CLI the skill lints the deck and says it was not rendered.

## File structure

```
marp-slide/
├── SKILL.md                 # Workflow, style table, fit rules, gotchas
├── README.md                # This file
├── assets/
│   └── template-*.md        # Seven complete decks with embedded CSS
├── references/
│   ├── marp-syntax.md       # Directive scope, built-in themes, fit headings, math
│   ├── image-patterns.md    # Image layouts and their surprises
│   ├── theme-css-guide.md   # CSS scoping, template-to-theme recipe, @size
│   ├── theme-snippets.md    # Callout, step, quote, link, table and terminal CSS for business and tech
│   ├── export.md            # Marp CLI export commands, browser, CI, live preview, HTML presenter options
│   ├── vscode.md            # Marp for VS Code preview, export, settings
│   └── slide-count.md       # Slide count by talk length (rule of thumb)
└── evals/
    ├── evals.json           # Output evals
    ├── trigger-queries.json # Trigger evals
    └── files/               # Eval input decks
```

## Resources

- [Marp Official Site](https://marp.app/)
- [Marpit Directives](https://marpit.marp.app/directives)
- [Marpit Image Syntax](https://marpit.marp.app/image-syntax)
- [Marp CLI GitHub](https://github.com/marp-team/marp-cli)
- [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Marp tooling and documentation (Marpit, Marp Core, Marp CLI, Marp for VS Code) come from the Marp team. Contrast thresholds follow the W3C WCAG 2.2 "Understanding contrast (minimum)" page. GitHub-hosted runner facts come from GitHub's actions/runner-images readme.

## License

This skill is part of the agent-skills project.
