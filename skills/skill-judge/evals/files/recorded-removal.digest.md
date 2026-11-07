=== previous-version digest: removed-template at evals/files/removed-template.previous ===
sections:
- evals/files/removed-template/SKILL.md.txt: # Release Notes | Turn the merged pull requests of one release into a changelog entry that readers can scan in under a minute.
- evals/files/removed-template/SKILL.md.txt: ## Workflow | 1. List the pull requests merged since the previous tag with `gh pr list --state merged --search "merged:>DATE"`.
- evals/files/removed-template/SKILL.md.txt: ## Template | ```markdown
- evals/files/removed-template/SKILL.md.txt: ## Gotchas | - Squash-merged pull requests carry the title of the branch, so reread each title before copying it; titles such as "fix
removed units (1, showing 1):
- para:7f0c3909 evals/files/removed-template/SKILL.md.txt: ```markdown ## [X.Y.Z] - YYYY-MM-DD ### Breaking - <what breaks, who is affected, the migration step> (#123) ### Added - <new capability in the user's words> (#124) ### Changed - <behaviour that differs from the previous release> (#125) ### Fixed - <the symptom users saw, not the root cause> (#126) 
removed or reduced files:
- none
record: evals/files/recorded-removal/record.md
