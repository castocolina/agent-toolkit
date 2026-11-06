# Test and Publish Workflows

Source: https://code.claude.com/docs/en/plugins/create-marketplace and https://code.claude.com/docs/en/plugins/cli-reference (checked 2026-11-04). Run the `claude plugin ...` commands in a shell; `/...` commands run inside a Claude Code session.

## Local install test

Run after `bump_version.py` and a clean `claude plugin validate` (SKILL.md steps 3-4):

```bash
claude plugin marketplace add <root>                  # prints: Successfully added marketplace: <marketplace>
claude plugin install <plugin>@<marketplace>          # <plugin> is the entry name
claude plugin list                                    # shows <plugin>@<marketplace> with Status: enabled
claude plugin details <plugin>                        # loaded version and component inventory
```

Then, in a new session:

1. Confirm the loaded version is the one you bumped to, from `claude plugin details <plugin>`. Do not trust the `version` in `claude plugin list --json` for a local-path marketplace: it is recorded at install, while `folderVersion` is what sessions load.
2. Run every new skill and command by its namespaced name (rules in `plugin-structure.md`), and give each new agent a task. Type `/<plugin>:` to list them: `claude plugin details` omits commands in `commands/` subdirectories.
3. Trigger each hook event the plugin handles and call one tool from each MCP server. Check the `/plugin` Errors tab for `path not found` or `path escapes plugin directory`.
4. After editing files, run `/reload-plugins`. A local-path marketplace loads the plugin in place, so no reinstall or bump is needed while iterating.

For a single-session check without installing: `claude --plugin-dir <plugin-dir>` (standard layout: `<root>/plugins/<plugin>`).

To start over: `claude plugin marketplace remove <marketplace>` removes the marketplace and uninstalls its plugins.

## Publish

Only when the user asked to publish, and only through the repository's own flow:

1. Stage only `<plugin-dir>` and `.claude-plugin/marketplace.json` (standard: `git add plugins/<plugin> .claude-plugin/marketplace.json`; a remote plugin's directory is committed in its own repository, not here), never `git add .`, which sweeps in unrelated work. Review `git diff --cached`.
2. Commit, then push the branch or open a pull request the way the repository releases (protected default branch, release branch, PR review). Never push to the default branch unless the user asked for exactly that.
3. Optional: `claude plugin tag <plugin-dir> --dry-run`, then without `--dry-run`, creates the tag `<plugin>--v<version>`. It refuses when `plugin.json` and the marketplace entry disagree on the version, or when the working tree is dirty.

## How users install and update

```bash
claude plugin marketplace add owner/repo              # or a git URL, or an absolute local path
claude plugin install <plugin>@<marketplace>
claude plugin marketplace update <marketplace>        # fetch the new catalog
claude plugin update <plugin>@<marketplace>           # loads in the next session or after /reload-plugins
```

If `claude plugin update` prints `already at the latest version`, the plugin's `version` was not bumped before publishing (see the SKILL.md gotchas).
