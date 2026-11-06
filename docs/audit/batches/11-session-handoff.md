# Batch 11

## session-handoff (skill)

### session-handoff#D6-1
- severity: high
- dimension: D6
- location: skills/session-handoff/scripts/create_handoff.py:334
- fix: Create handoff files exclusively and refuse collisions by default. Generate a unique suffix or require an explicit overwrite option before replacement, and add a deterministic same-timestamp collision test.

### session-handoff#D7-1
- severity: medium
- dimension: D7
- location: skills/session-handoff/scripts/validate_handoff.py:303
- fix: Use argparse consistently across the helpers, document exit codes and examples through --help, and add a JSON output mode with diagnostics on stderr. Extend the existing tests to validate help behavior and parse the JSON result.

### session-handoff#D8-1
- severity: medium
- dimension: D8
- location: skills/session-handoff/scripts/check_staleness.py:35
- fix: Preserve status-record whitespace and parse porcelain output without stripping its prefix, preferably using NUL-delimited status records with explicit rename handling. Add a test asserting the exact changed pathname when the first record is an unstaged tracked modification.

### session-handoff#D8-2
- severity: medium
- dimension: D8
- location: skills/session-handoff/scripts/validate_handoff.py:126
- fix: Validate root-relative filenames as well as paths containing slashes, filtering URLs separately. Apply the same correction to staleness reference extraction and add missing-root-file cases to both script test suites.

### session-handoff#D7-1
- severity: low
- dimension: D7
- location: skills/session-handoff/scripts/validate_handoff.py:302
- fix: Usage prints only on missing arguments with no --help flag and free-form output; switch to argparse with --help and add a --json output mode so agents can consume results programmatically

### session-handoff#D8-1
- severity: low
- dimension: D8
- location: skills/session-handoff/SKILL.md:49
- fix: Validation is a single pass before Step 4 confirms; add 'fix reported issues and re-run until the verdict is READY' between Steps 3 and 4

### session-handoff#D1-1
- severity: medium
- dimension: D1
- location: skills/session-handoff/SKILL.md:153
- fix: Remove the repeated resource catalogue and compress generic open/fill/report instructions. Keep one CREATE route, one RESUME route, exact script interfaces, the irreconstructable-context prioritization, bounded lineage, and implementation-specific safeguards.

### session-handoff#D1-1
- severity: low
- dimension: D1
- location: skills/session-handoff/SKILL.md:42
- fix: The four-section list restates the structure references/handoff-template.md already defines; keep only the 'three required sections' rule and point to the template

### session-handoff#D2-1
- severity: low
- dimension: D2
- location: skills/session-handoff/SKILL.md:137
- fix: Step 6 edits or chains handoffs without re-validation; add 're-run validate_handoff.py after editing or chaining a handoff before finalizing'

### session-handoff#D3-1
- severity: medium
- dimension: D3
- location: skills/session-handoff/SKILL.md:64
- fix: Gotchas exist only on the CREATE side; add resume-side failure modes with reasons, e.g. 'FRESH only compares files and commits; after a revert or rebase, re-verify assumptions by hand'

### session-handoff#D5-1
- severity: low
- dimension: D5
- location: skills/session-handoff/scripts/__pycache__
- fix: Delete scripts/__pycache__/ and add it to .gitignore

### session-handoff#D5-2
- severity: low
- dimension: D5
- location: skills/session-handoff/SKILL.md:28
- fix: Use spec-relative paths (scripts/create_handoff.py) and state once that paths are relative to the skill directory, instead of placeholder prose in every command

### session-handoff#D6-1
- severity: low
- dimension: D6
- location: skills/session-handoff/SKILL.md:40
- fix: Give a rule of thumb, e.g. one paragraph per section for under a day of remaining work; full evidence and reproduction commands for multi-day work
