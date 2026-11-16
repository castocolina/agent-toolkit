---
description: Regenerate the "Available Skills" table in the root README.md from each skills/*/SKILL.md name and description. Use after adding, removing, renaming or re-describing a skill, when the skills list or table in the README is stale or missing an entry, or when asked to update or sync the README skill list, even without the word "table". Not for editing any other README section or for a skill's own README.md.
---

# Sync Skills README

Rebuild only the table under `## 📚 Available Skills` in the root README.md from the skills in `skills/`. Everything else in README.md stays byte-identical.

## Workflow

1. **Collect.** List the directories in `skills/` (ignore plain files and dot-directories). For each, read `skills/<dir>/SKILL.md` and take `name:` and `description:` from the frontmatter. Join folded (`>`) or literal (`|`) description lines with single spaces.
   - No SKILL.md: skip and warn `⚠️ Skipped <dir>: No SKILL.md found`.
   - Missing `name` or `description`: skip and warn `⚠️ Skipped <dir>: Missing name or description in frontmatter`.
2. **Categorize.** Walk the table below top to bottom and take the first category with a keyword that matches the skill name. A keyword matches when its hyphen-separated tokens appear as a contiguous run of the name's hyphen-separated tokens (trailing `s` ignored on each token): `web-to-markdown` matches only that run, `docs` matches `backend-to-frontend-handoff-docs`, and a keyword equal to the whole name always matches. If no category matches, repeat on the description words (single-token keywords only; the description lowercased and split on every character other than a-z and 0-9, so `slash-command,` gives `slash` and `command`; trailing `s` ignored). If still none, use Utilities. Whole tokens only: the substring `ai` would match almost every description.

   | Category | Emoji | Keywords |
   |----------|-------|----------|
   | AI Tools | 🤖 | codex, gemini, perplexity, ai, llm, model |
   | Meta | 🔮 | command-creator, plugin-forge, plugin, command |
   | Documentation | 📝 | docs, documentation, handoff, requirements, diagram, mermaid, draw, excalidraw, marp, slide, c4-architecture |
   | Design & Frontend | 🎨 | design, frontend, ui, openapi, typescript, system |
   | Development | 🛠️ | session, entropy, development, workflow, database, dependency |
   | Planning | 🎯 | plan, planning, spec, forge, gepetto, clarity, game-changing, features |
   | Professional | 👔 | professional, communication, career, soft-skill, feedback, conversation |
   | Testing | 🧪 | test, testing, qa, quality |
   | Git | 📦 | commit, git, branch, pr, pull-request |
   | Utilities | 🔧 | domain, meme, web-to-markdown, utility, tool, datadog |

   Row order is both the precedence and the output order, so a skill matching two categories always lands in the earlier one: `backend-to-frontend-handoff-docs` hits Documentation (`docs`, `handoff`) and Design & Frontend (`frontend`) and goes to Documentation. To pin a skill, add its name as a keyword to the category you want, in a row at or before any category it would otherwise hit; a new keyword placed in a later row is shadowed.
   Sanity check before building rows: for each skill placed by the description-word pass or by the Utilities fallback, if the category contradicts what the skill plainly does, keep the mechanical result and list it under Warnings with the keyword that would pin it (for example `skill-judge` for Meta).
3. **Build rows.** One per skill, sorted by category order above, then by directory name (the same value used in the link):
   `| <emoji> <Category> | [<name>](skills/<dir>/README.md) | <summary> |`
   The link uses the directory name, not the `name:` value. Summary: an action-oriented phrase of about 50 characters or fewer, built only from facts in that description (e.g. `Code analysis, refactoring & automated edits`): drop a trailing `Use when...` clause (if the description is only trigger wording, state the action it asks for instead), keep the leading verb and object, join two capabilities with `&`, and cut qualifiers until it fits. Never add model versions, context sizes or other details the description does not state. Escape `|` as `\|`. If `skills/<dir>/README.md` is absent, keep the row and warn `⚠️ <dir>: skills/<dir>/README.md not found, link will be broken`.
4. **Replace.** If `skills/` is missing or no valid skills remain, stop without editing: `❌ No valid skills found in skills/`. Otherwise find the heading by its text `Available Skills` after `## `, trimming trailing whitespace (the emoji may carry a U+FE0F variation selector, so never match the line byte for byte). If it is absent, or no `|` table follows it, stop without editing: `❌ Could not find '## 📚 Available Skills' section in README.md`. Save a copy with `backup=$(mktemp) && cp README.md "$backup" && echo "$backup"` (stop if it fails) and record the absolute path it prints, then replace only the header, delimiter and contiguous `|` rows under that heading with `| Category | Skill | Description |`, `|----------|-------|-------------|` and the new rows. Keep the heading, the `---` separators and all later prose.
5. **Verify and show.** Each Bash call is a new shell, so `$backup` is gone: use the literal recorded path in every later command. `diff <recorded-path> README.md`: every changed line must be inside the table, and the new row count must equal the number of valid skills. Show the diff to the user. On a mismatch, restore with `cp <recorded-path> README.md` and report the failure.
6. **Report.** Only README.md was edited:

   ```
   ✅ README.md updated
   - Total skills: <n>
   - Categories: <Category> <count>, ...
   - Rows added: <names>; removed: <names>
   - Warnings: <skipped skills, or none>
   ```

## Gotchas

- Reading only the first description line truncates a folded or literal summary to `>` or `|`.
- Hyphenated keywords (`command-creator`, `c4-architecture`) match only as a contiguous run of name tokens, never as one token: `c4-architecture` does not match a skill named `c4`.
- The description-word pass matches generic words (`model`, `tool`, `system`, `plan`, `test`) that appear in unrelated descriptions, so a skill can land in AI Tools or Planning by accident. Pin it by its name instead of adding broader keywords.
- An unescaped `|` in a description splits the cell and breaks the whole table.
- A link built from `name:` breaks when the directory name differs.
- Replacing "until the next heading" eats the `---` separator and prose that follow the table.
- Do not use Grep to parse frontmatter: it returns one line per match, so it misses folded descriptions and matches `name:` in body text. Read the file.
