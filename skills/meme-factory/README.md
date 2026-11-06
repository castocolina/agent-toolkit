# Meme Factory

A skill for building image-meme URLs with the free [memegen.link](https://memegen.link) API and for writing text-only memes (greentext, copypasta, ASCII). It ships a small Python client that escapes captions the way memegen.link expects. `SKILL.md` holds the workflow, the verified template IDs, the escaping table and the gotchas.

## When it triggers

Requests for a meme, a reaction or comparison image, a meme URL for Slack, a PR, docs or a social post, or captions on an image URL the user supplies. It is not for captioning a photo it was not given, editing an existing image, logos, slide decks, serious infographics or video-to-GIF.

## Installation

**Claude Code:**

```bash
cp -r skills/meme-factory ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation. Fetching images needs network access to `api.memegen.link`; add that domain at `claude.ai/settings/capabilities`.

## File structure

```
meme-factory/
├── SKILL.md                          # Workflow, templates, query params, escaping, gotchas
├── README.md                         # This file
├── scripts/meme_generator.py         # generate / suggest / list-templates CLI (Python 3.10+, stdlib only)
├── references/markdown-memes-guide.md # Text-only meme formats
└── evals/                            # Output evals and trigger queries
```

## Resources

- [memegen.link API docs](https://api.memegen.link/docs/)
- [memegen source and README](https://github.com/jacebrowning/memegen) by Jace Browning (MIT)
- [Template list](https://api.memegen.link/templates/)
