# Batch 70

## sync-skills-readme (command)

### sync-skills-readme#D8-1
- severity: medium
- dimension: D8
- location: commands/sync-skills-readme.md:31
- fix: State the key: "then by directory name (the same value used in the link)"

### sync-skills-readme#D8-2
- severity: low
- dimension: D8
- location: commands/sync-skills-readme.md:34
- fix: Move the precondition checks to the top of the workflow as step 0: stop with `❌ No valid skills found in skills/` if `skills/` is missing, and with `❌ README.md not found` if the root README.md is absent, before reading any SKILL.md

### sync-skills-readme#D8-1
- severity: medium
- dimension: D8
- location: commands/sync-skills-readme.md:35
- fix: Explicitly record the absolute backup path printed in step 4 and use that literal path, or reassign `backup` to that recorded path, in every subsequent shell invocation. Use the same recorded path for both verification and rollback rather than relying on shell-variable persistence across tool calls.

### sync-skills-readme#D1-1
- severity: low
- dimension: D1
- location: commands/sync-skills-readme.md:51
- fix: Keep each rule in one place: either delete these two Gotchas bullets or cut the duplicate clauses from step 3, so every line adds something new

### sync-skills-readme#D2-1
- severity: low
- dimension: D2
- location: commands/sync-skills-readme.md:33
- fix: Add one before/after pair for a trigger-only description, for example "Use when the user needs documentation written for an API..." -> "Write API docs & frontend handoff notes", so the agent learns the approach and not just one answer

### sync-skills-readme#D3-1
- severity: medium
- dimension: D3
- location: commands/sync-skills-readme.md:34
- fix: Add a Gotcha: "Match the heading by its text `Available Skills` after `## ` and trim trailing whitespace; emoji may carry a U+FE0F variation selector, so an exact byte match can miss a heading that is present."
