# Batch 42

## command-creator (skill)

### command-creator#D7-1
- severity: low
- dimension: D7
- location: skills/command-creator/evals/evals.json
- fix: Add an eval that asks for a plan-then-implement command, with assertions that it writes nothing before an explicit approval signal and that it names where the plan is saved. Add a second eval in which the user approves updating an existing command, with assertions that it reads the file first, keeps the frontmatter and shows a diff.

### command-creator#D8-1
- severity: medium
- dimension: D8
- location: skills/command-creator/SKILL.md:15
- fix: Give this branch an outcome: 'say a skill fits better and stop without writing; if the user still wants a command, write one that calls the existing scripts by path and flag each missing script as a manual step.' Also note that the agent cannot see the / menu (line 41), so it should tell the user to check for /name instead of claiming it checked.

### command-creator#D8-1
- severity: high
- dimension: D8
- location: skills/command-creator/references/examples.md:53
- fix: Add an explicit encoding step for the final commit message: encode it as one single-quoted shell word, escaping embedded single quotes, then run `git commit -m <encoded-message>`. Update the example snippet accordingly and preserve its upstream attribution.

### command-creator#D8-2
- severity: medium
- dimension: D8
- location: skills/command-creator/SKILL.md:134
- fix: Make the initial collision offer distinguish viable resolutions: a renamed command, an explicitly approved resolution of the shadowing collision before updating the command, or routing a requested SKILL.md edit out of scope. Carry the selected resolution into the approved-update checklist instead of returning to the unchanged menu.

### command-creator#D1-1
- severity: low
- dimension: D1
- location: skills/command-creator/SKILL.md:52
- fix: Shorten this to the parts specific to commands: 'Delegate only with an agent type that exists (built-ins: Explore, Plan, general-purpose) or with context: fork plus agent:, and honor "no agents".' Drop the generic when-to-delegate reasoning, which the model and harness already handle.

### command-creator#D2-1
- severity: low
- dimension: D2
- location: skills/command-creator/SKILL.md:43
- fix: Mark each table as the lookup for its workflow step (for example 'Step 3 lookup' over ## Location and 'Step 5 lookup' over ## Frontmatter), so the Process pattern stays the spine and the tables read as its reference.

### command-creator#D1-1
- severity: low
- dimension: D1
- location: skills/command-creator/SKILL.md:68
- fix: Keep the complete silent-frontmatter warning and its auto-invocation consequence once in Gotchas; replace the repeated explanation in Frontmatter with a short cross-reference.
