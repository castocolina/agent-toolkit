# Crafting Effective READMEs

A skill for Claude Code that writes, updates, and audits README files so the intended reader reaches a first success the repository actually supports.

## What It Does

- Settles which README is in scope (root or monorepo package) and who reads it, from the user's statement first and repository evidence second.
- Derives install commands and prerequisites from manifests and CI instead of the local machine.
- Validates the first-use path in a clean environment, or labels each claim `executed`, `static`, or `unverified` when it cannot run it.
- Flags README traps: workspace-root commands, unreleased examples, generated regions, registry rendering, anchor slugs, and badges.
- Starts from a project-type template (`templates/oss.md`, `personal.md`, `internal.md`, `xdg-config.md`) once the README type is settled.

`SKILL.md` holds the workflow and gotchas; `references/section-checklist.md` holds the per-type sections.

## Project Types and Templates

| Project type | Audience | Template |
|---|---|---|
| OSS | Users and contributors of a public project with an OSI-approved license | `templates/oss.md` |
| Personal | Future-you and portfolio viewers | `templates/personal.md` |
| Internal | New team members and on-call engineers | `templates/internal.md` |
| Config (dotfiles, `~/.config`, script folders) | A confused future-you | `templates/xdg-config.md` |

A template loads only for the chosen type. Its placeholders are filled from repository evidence; a fact the repository does not show stays a visible placeholder.

## When to Use

- "Write a README for this project"
- "Update the README after this change"
- "Review my README against package.json"
- "What sections should my README have?"
- "Make this README Standard Readme compliant"

Not for API references, user manuals, changelogs, contributor guides, or docstrings.

## Installation

```bash
cp -r skills/crafting-effective-readmes ~/.claude/skills/
```

On claude.ai, add the skill to project knowledge or paste `SKILL.md` into the conversation.

## Directory Structure

```
crafting-effective-readmes/
  SKILL.md                              # Workflow, validation, gotchas, gated reference list
  references/
    section-checklist.md                # Sections by project type
    standard-readme-spec.md             # Standard Readme specification
    standard-readme-example-minimal.md  # Minimal compliant example
    standard-readme-example-maximal.md  # Full-featured compliant example
    art-of-readme.md                    # Reader-funnel ordering
    make-a-readme.md                    # Purpose of common sections
  templates/
    oss.md                              # Open-source project README
    personal.md                         # Side project or portfolio README
    internal.md                         # Team service or internal tool README
    xdg-config.md                       # Dotfiles, ~/.config or script folder README
  evals/                                # Output evals, trigger queries, fixtures
```

## Related Skills

- `writing-clearly-and-concisely` - general prose quality

## Attribution

- Original skill by @joshuadavidthomas from [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills) (MIT)
- `references/art-of-readme.md` from [hackergrrl/art-of-readme](https://github.com/hackergrrl/art-of-readme), licensed under the [Creative Commons Attribution License 2.0](http://creativecommons.org/licenses/by/2.0/)
- `references/standard-readme-spec.md` and the two `standard-readme-example-*.md` files from [Standard Readme](https://github.com/RichardLitt/standard-readme) by Richard Litt
- `references/make-a-readme.md` from [Make a README](https://www.makeareadme.com) by Danny Guo
- Imported through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) (`skills/crafting-effective-readmes`)
- Facts in `SKILL.md` were checked against the documentation of GitHub, GitLab, npm, pnpm, the Python Packaging Authority, the Python Software Foundation, The Rust Project, The Go Authors, SPDX, the OpenJS Foundation and Shields.io, and against the generated-region markers of All Contributors, Posit (usethis), Thorsten Lorenz (doctoc), terraform-docs, Jon Schlinkert (markdown-toc), Diogo Sousa (cargo-rdme) and cargo-readme contributors
