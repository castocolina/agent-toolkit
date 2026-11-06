# Batch 31

## plugin-forge (skill)

### plugin-forge#D6-1
- severity: high
- dimension: D6
- location: skills/plugin-forge/references/workflows.md:106
- fix: Stage only the intended plugin and marketplace changes, inspect the diff, and use the repository's actual release branch or PR workflow. Perform commits and pushes only within the user's authorized publication scope.

### plugin-forge#D7-1
- severity: low
- dimension: D7
- location: skills/plugin-forge/scripts/bump_version.py:57
- fix: Send diagnostics to stderr and reserve stdout for structured results, or consistently emit structured error objects. Update CLI tests to check the output-channel contract and --help behavior.

### plugin-forge#D8-1
- severity: high
- dimension: D8
- location: skills/plugin-forge/SKILL.md:15
- fix: Replace the two execution steps with one fully specified scaffold invocation. State that successful execution already registers the marketplace entry, so later edits should update that entry rather than duplicate it.

### plugin-forge#D8-2
- severity: high
- dimension: D8
- location: skills/plugin-forge/scripts/bump_version.py:23
- fix: Validate the entire supported version string before computing or writing anything. Require three valid nonnegative SemVer core components, explicitly handle or reject prerelease/build metadata, and test that invalid versions leave both manifests unchanged.

### plugin-forge#D7-1
- severity: low
- dimension: D7
- location: skills/plugin-forge/scripts/bump_version.py:61
- fix: Error diagnostics print to stdout although SKILL.md documents stdout as the JSON channel (the test even asserts them in r.stdout); route errors to stderr like create_plugin.py does and document exit codes in --help.

### plugin-forge#D8-1
- severity: low
- dimension: D8
- location: skills/plugin-forge/references/workflows.md:124
- fix: Name the concrete discovery method (type `/` and autocomplete the plugin-prefixed command, or inspect the installed plugin's commands directory) so the agent is not left guessing how to verify.

### plugin-forge#D1-1
- severity: low
- dimension: D1
- location: skills/plugin-forge/SKILL.md:12
- fix: State the scaffold precondition and generated artifacts once. Keep the execution-unavailable fallback brief and refer back to that contract rather than repeating the same behavior.

### plugin-forge#D2-1
- severity: medium
- dimension: D2
- location: skills/plugin-forge/SKILL.md:18
- fix: Order the release procedure as component changes, synchronized version bump, manifest/path validation, local installation, reload and installed-version verification, then publication.

### plugin-forge#D1-1
- severity: low
- dimension: D1
- location: skills/plugin-forge/references/workflows.md:59
- fix: Delete the semantic-versioning tutorial and the conventional-commit examples; the model knows both. Keep the plugin-specific rule (both manifests must match) and the testing steps.

### plugin-forge#D2-1
- severity: low
- dimension: D2
- location: skills/plugin-forge/SKILL.md:16
- fix: This script contract is stated three times (lines 8, 12, 15, 16); state it once at the scaffold step and drop the repetitions to save body tokens.

### plugin-forge#D3-1
- severity: low
- dimension: D3
- location: skills/plugin-forge/SKILL.md:27
- fix: Add the missing gotcha: when marketplace.json sets `pluginRoot`, relative `source` values resolve against it, so create_plugin.py's unconditional `./plugins/<name>` source can double-prefix; document the interaction or make the script respect an existing pluginRoot.

### plugin-forge#D6-1
- severity: low
- dimension: D6
- location: skills/plugin-forge/SKILL.md:15
- fix: The script mutates a shared marketplace manifest with no preview; add a --dry-run flag or instruct the agent to show the planned manifest entry before running against a shared marketplace root.
