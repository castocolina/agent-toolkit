---
name: plugin-forge
description: "Create and manage Claude Code marketplace plugins: scaffold plugin directories, edit plugin.json and marketplace.json, add commands, skills, agents, hooks, and MCP components, bump versions, and test or publish packages. Use when packaging Claude Code capabilities, repairing marketplace registration/manifests, or debugging a plugin install or update that does not pick up changes. Not for other IDE extensions, npm releases, or authoring standalone skills/commands without plugin packaging."
---

# Claude Code Plugin Forge

## Script contract

`scripts/` paths are relative to this skill's directory. Both scripts take `--marketplace-root <root>`, the directory that holds `.claude-plugin/marketplace.json` (it defaults to the current directory, so pass it explicitly), print one JSON object on stdout and diagnostics on stderr, and exit 0 on success or 2 on bad input with nothing written.

- `python3 scripts/create_plugin.py <name> --marketplace-root <root> --author-name <name> --author-email <email> --description <text> --keywords <a,b,c> [--category <cat>] [--dry-run]`: requires an existing, well-formed marketplace manifest (`name`, `owner.name`, a `plugins` array of objects with `name` and `source`) and a kebab-case name not yet used as a directory or entry. It rejects names `claude plugin validate` treats as Anthropic's own (`claude`, `anthropic`, `claude-code`, `claude-mods`, prefixes `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-`, or `official` beside claude/anthropic). Creates `<root>/plugins/<name>/` with `.claude-plugin/plugin.json` (version `0.1.0`), empty `commands/` and `skills/`, and `README.md`, then appends the entry `{name, source: "./plugins/<name>", description, keywords, category}` (no `version`: it lives only in `plugin.json`) (category defaults to `productivity`). `--dry-run` prints the planned paths and entry and writes nothing. It never creates a missing marketplace manifest.
- `python3 scripts/bump_version.py <name> major|minor|patch --marketplace-root <root>`: reads `plugins/<name>/.claude-plugin/plugin.json` and the plugin's marketplace entry, bumps the version Claude Code uses (`plugin.json`, else the entry), keeps an existing entry `version` equal, and never adds one. Requires a plain `MAJOR.MINOR.PATCH` (prerelease or build suffixes are rejected). With no version in either file it fails with `the plugin is versioned by commit SHA`: nothing to bump, just push. Part: `patch` for fixes; `minor` for a new skill, command, agent, hook or MCP server; `major` when a component is renamed or removed.

## Workflow

1. **Locate the plugin first; every later step depends on it.** Read its entry `source` in `marketplace.json`: a bare `source` such as `formatter` first resolves through `metadata.pluginRoot` (`./plugins` + `formatter` = `./plugins/formatter`); then **standard** is `./plugins/<name>` with a `.claude-plugin/plugin.json` (the scripts work; `bump_version.py` needs that manifest, so a manifest-less plugin counts as other local); **other local** is any other resolved `./` path; **remote** is a `github`, `git-subdir` or `url` object, whose `plugin.json` lives in that other repository. Note the **plugin directory** now: marketplace root + resolved source for a local plugin; the repository checkout root for `github`/`url`; checkout root + `path` for `git-subdir`. Steps 4-5 use it as `<plugin-dir>`. For a new plugin, confirm the marketplace root and a kebab-case name:
   - No `.claude-plugin/marketplace.json` yet: create it first with `{"name": "<kebab-name>", "owner": {"name": "<maintainer>"}, "plugins": []}` (all three keys are required).
   - Shared or team marketplace: run with `--dry-run` and show the user the entry before the real run.
   - Plugins kept outside `<root>/plugins/`, or a remote source (GitHub, git subdirectory): write the files by hand, reading `references/plugin-structure.md` and `references/marketplace-schema.md`.
   - Otherwise run `create_plugin.py` once. It registers the marketplace entry itself, so later metadata edits change that entry; never add a second one.
   - Cannot run commands here: say so, and give the exact command plus the files it would create and the entry it would append, from the contract above.
2. **Components.** Add `skills/`, `commands/`, `agents/`, `hooks/hooks.json`, or `.mcp.json` at the plugin root. Read `references/plugin-structure.md` for layout, command names, and manifest path rules.
3. **Version**, once per release, after the component changes. Standard: `bump_version.py`. Other local or remote: edit by hand the file that wins, which is the plugin's own `plugin.json` when it sets `version` (in the remote repository for a remote source), else the marketplace entry's `version`, else nothing (SHA-versioned). Drop `version` from the other file, or keep it equal.
4. **Validate.** `claude plugin validate <root>` checks the marketplace and the `plugin.json` of each relative-path plugin, then `claude plugin validate <plugin-dir>` checks component frontmatter and paths. `<plugin-dir>` is the directory noted in step 1; for a remote source, a local checkout of its repository (marketplace validation never fetches remote sources). Fix every error and rerun until it prints `Validation passed`.
5. **Test the install, then publish.** Read `references/workflows.md`: install from the marketplace, confirm the loaded version with `claude plugin details <name>`, run every new skill, command, and agent, and exercise hooks and MCP servers. A remote source is fetched at install, so push the plugin repository first. If its entry pins `ref` (tag or branch) or `sha` (full 40-character commit), push the new tag or commit, set the entry's `ref`/`sha` to it in `marketplace.json`, validate, then install from that revised entry; a pin left unchanged keeps everyone on the old commit. Publish only after that passes, and only within what the user asked for: a remote plugin's changes are committed and pushed in its own repository, separately from `marketplace.json`; for other-local, stage `<plugin-dir>` itself.

For a standard-layout scaffold-only or bump-only request, the contract above is enough; do not load the references. Other-local and remote scaffolding still need the step 1 reads.

## Gotchas

- Only `plugin.json` goes in `.claude-plugin/`. A component directory placed there is never discovered.
- `plugin.json` `version` beats the marketplace entry `version`: on a mismatch the entry value is ignored at install and `claude plugin validate` warns. Set `version` in one place, `plugin.json`. For the standard `./plugins/<name>` layout change it only through `bump_version.py`; for other-local and remote sources, edit the winning file by hand (step 3). A prerelease such as `2.0.0-beta.1`, which the script rejects, is also set by hand.
- A `version` that does not change keeps hosted users on their cached copy: `claude plugin update` prints `already at the latest version`, however many commits you push. Bump every release, or omit `version` from both files so the commit SHA becomes the version.
- A marketplace added from a local path loads relative-path plugins in place: edits apply at `/reload-plugins` with no bump. A passing local test therefore does not prove that hosted users will receive the update.
- The entry `name` is the install id (`<entry>@<marketplace>`); the `plugin.json` `name` prefixes every component (`/<name>:<skill>`). Keep them equal, or installing by the manifest name fails with `Plugin "<name>" not found in marketplace`.
- A relative `source` resolves from the marketplace root, not from `.claude-plugin/`, must start with `./` unless it is a bare name resolved through `metadata.pluginRoot`, and the resolved path must not contain `..`. A path to a missing directory passes validation and fails only at install with `Source path does not exist`.

## References

- `references/plugin-structure.md`: adding components, `plugin.json` fields, component path rules, command naming.
- `references/marketplace-schema.md`: editing `marketplace.json`, choosing a source type, `metadata.pluginRoot`, team distribution.
- `references/workflows.md`: local install test loop and the publish and update steps.
