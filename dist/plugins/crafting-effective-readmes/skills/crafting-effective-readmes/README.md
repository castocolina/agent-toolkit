# Crafting Effective READMEs

A skill for Claude Code that writes, updates, and audits README files so the intended reader reaches a first success the repository actually supports.

## What It Does

- Settles which README is in scope (root or monorepo package) and who reads it, from the user's statement first and repository evidence second.
- Derives install commands and prerequisites from manifests and CI instead of the local machine.
- Validates the first-use path in a clean environment, or labels each claim `executed`, `static`, or `unverified` when it cannot run it.
- Flags README traps: workspace-root commands, unreleased examples, generated regions, registry rendering, anchor slugs, and badges.

`SKILL.md` holds the workflow and gotchas; `references/section-checklist.md` holds the per-type sections.

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
  evals/                                # Output evals, trigger queries, fixtures
```

## Related Skills

- `writing-clearly-and-concisely` - general prose quality

## Attribution

- Original skill by @joshuadavidthomas from [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills) (MIT)
- `references/art-of-readme.md` from [hackergrrl/art-of-readme](https://github.com/hackergrrl/art-of-readme), licensed under the [Creative Commons Attribution License 2.0](http://creativecommons.org/licenses/by/2.0/)
- `references/standard-readme-spec.md` and the two `standard-readme-example-*.md` files from [Standard Readme](https://github.com/RichardLitt/standard-readme) by Richard Litt
- `references/make-a-readme.md` from [Make a README](https://www.makeareadme.com) by Danny Guo
