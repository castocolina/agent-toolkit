# Refresh the audit rubric

Update the rubric and structural references in this checkout using only the evidence listed below. This is a repository-editing task; do not use the network or invent source content. You cannot run commands: the caller runs the checks on the host after your edits.

## Evidence you may use

- `skills/agentskills-research/SKILL.md` and its referenced instructions, including its **When upstream structure changes** procedure when `STRUCTURE_CHANGED={{STRUCTURE_CHANGED}}` is true.
- `{{FETCH_RESULT}}`: the specification fetch result, including `structure_changed`, `new_pages`, `removed_pages`, `changed`, and `rubric_stale`.
- `{{PAGES_JSON}}`: the fetched page inventory. Rows with `"mapped": false` are new upstream pages, pre-downloaded as `audit-pages/<page>.mdx`.
- `{{NEW_PAGES}}`: JSON list of the new upstream pages (the `mapped: false` rows of the inventory). These pre-downloaded files are the only allowed source for their content. Copy their upstream bytes verbatim after the required source header; do not summarize, reconstruct, or fetch them.
- `{{REMOVED_PAGES}}`: JSON list of the pages that no longer exist upstream; this is the only record of their removal. Delete their pinned reference files, `SOURCE.json` entries and navigation list entries as the research procedure requires; never keep a stale reference.
- `{{SPEC_DIFF}}`: the specification change diff behind this run (supplied by the caller; this checkout is too shallow to recompute it).
- Existing pinned reference files under `skills/skill-judge/references/agentskills/`, `SOURCE.json`, `skills/skill-judge/references/rubric.md`, judge eval file lists, research fixtures/tests, and other files explicitly named in the research instructions.
- Applicable repository tests.

## Required scope

Make the updates required by `agentskills-research`, including all structural repairs needed for the fetcher's source map, fixtures, tests, reference additions/deletions, rubric source remapping and judge eval file lists. Do not modify unrelated skills. Keep new reference pages verbatim and preserve required mappings. Every newly committed page reference must begin with `<!-- Source: https://github.com/agentskills/agentskills (CC-BY-4.0), verbatim copy, see SOURCE.json -->` and have a matching header-inclusive SHA-256 entry in `SOURCE.json`. `docs-navigation.json.txt` uses its own `# Source:` header. Use `audit-pages/pages.json` as the page inventory and the `mapped: false` page files as the sole content source for any newly listed page.

When changing `rubric.md`, copy `rubric_version`, `spec_sha` and every `max` from `rubric.md` as required by its current schema; bump the version only according to the research procedure. Set `spec_sha` from `SOURCE.json` when the instructions require it. Never fabricate a SHA, criterion, source anchor, or rubric maximum.

## Exact output

Write all updates directly to their repository paths. The rubric output is exactly `skills/skill-judge/references/rubric.md`. Structural/reference changes must be in their repository paths and captured by the caller in `repairs.patch`; do not create or edit `repairs.patch` yourself. Do not emit a JSON response in place of file edits.

Do not run any commands (you have no shell) and do not claim that checks passed. After your edits the caller runs `python3 scripts/audit/audit.py rubric-check` and the fetcher tests (`tests/skills/agentskills-research/test-fetch-spec.sh` plus the tests required by the research instructions) on the host, and fails the run if they do not pass.
