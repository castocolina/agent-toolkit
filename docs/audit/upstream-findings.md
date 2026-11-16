
## Baseline check (plan 2 Task 3)

- datadog-cli: no issues
- gepetto: no issues

## Content recovery, 2026-11-13 (plan 14)

- `.claude/commands/sync-skills-readme.md` lines ~71 and ~89 still use "Advanced code analysis with GPT-5.2" in their examples, so the next sync can regenerate the stale codex README row; report-only, not changed.
- `skills/pr-diagrams/scripts/pr-diagrams.sh` (usage line ~346, "capability ... always exit 0"), `skills/pr-diagrams/SKILL.md` line 29 and `skills/pr-diagrams/README.md` line 23 still say `capability` always exits 0, while `commands/explain-pr-changes.md` phase 4 now treats exit 2 or any other non-zero exit as a stop (checked 2026-11-14); report-only, batch 19 owns these files.
- `skills/pr-diagrams/references/pr-body.md` line 34 (none-mode filter, regex `/!\[[^]]*\](\[[^]]*\])?/`) also matches ordinary inline images such as `![arch](https://static.example.com/image.png)` when a diagram reference label collides, and leaves the URL suffix behind; it needs a pass that preserves inline images and an eval fixture (checked 2026-11-14); report-only, batch 19 owns this file.
- `crafting-effective-readmes`: the registry row `hackergrrl/art-of-readme` (kind `github`) answered `gh: Not Found (HTTP 404)` since 2026-11-06 and is not a rename: the owner account (user id 489362) is gone and there is no `noffle/art-of-readme`; the row was replaced by an `unversioned` row pointing at the last archived copy (Wayback snapshot 2026-06-15, CC BY 2.0, checked 2026-11-15), so the vendored `references/art-of-readme.md` has no live source to compare against.
