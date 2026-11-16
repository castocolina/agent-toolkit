# Meme Factory

A skill for building image-meme URLs with the free [memegen.link](https://memegen.link) API and for writing text-only memes (15 formats, from greentext, copypasta and ASCII to chat logs and corporate satire). It ships a small Python client that escapes captions the way memegen.link expects. `SKILL.md` holds the workflow, the verified template IDs, the escaping table and the gotchas.

## When it triggers

Requests for a meme, a reaction or comparison image, a meme URL for Slack, a PR, docs or a social post, or captions on an image URL the user supplies. It is not for captioning a photo it was not given, editing an existing image, logos, slide decks, serious infographics or video-to-GIF.

## Usage

Ask in plain words ("make a Slack meme about flaky tests"), or invoke it directly:

```
/meme-factory
/meme-factory drake "manual testing" "automated testing"
```

`/meme-factory` alone asks what the meme is about. `/meme-factory <template> <caption>...` names the template and gives one raw caption per template line; the skill escapes them, so do not pre-escape. Either way the skill redacts sensitive details from the captions first, because captions travel in the URL to a public service.

Check a generated URL with `curl -sI "<url>"`; it should print HTTP 200 and an image content type. Look up template IDs at https://api.memegen.link/templates/ rather than guessing them.

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
├── references/markdown-memes-guide.md # Text-only meme rules: greentext, copypasta, ASCII
├── references/text-memes.md          # The 15 text meme formats and Markdown techniques
├── references/blog-posts.md          # Blog platform tricks, mixing text and image memes, example post
├── references/image-memes.md         # Templates by use case, formats, endpoints, backgrounds, examples
└── evals/                            # Output evals and trigger queries
```

## Resources

- [memegen.link API docs](https://api.memegen.link/docs/)
- [memegen source and README](https://github.com/jacebrowning/memegen) by Jace Browning (MIT)
- [Template list](https://api.memegen.link/templates/)

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Image memes use the memegen API by Jace Browning ([jacebrowning/memegen](https://github.com/jacebrowning/memegen), MIT). The syntax and size facts in `references/` were checked against documentation from Meta, Material for MkDocs, Docusaurus and MDN Web Docs.
