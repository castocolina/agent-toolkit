# Marketplace Schema Reference

Source: https://code.claude.com/docs/en/plugins/marketplace-reference (checked 2026-11-04). The minimal file and the version, name and relative-path rules are in SKILL.md; this file covers the rest.

## Top-level fields

- Required: `name`, `owner` (`owner.name` required; `email`, `url` optional), `plugins`.
- `name`: letters, digits, `.`, `_`, `-`, starting with a letter or digit. Reserved and refused: official names such as `claude-plugins-official` or `anthropic-plugins`, look-alikes such as `official-claude-plugins`, names starting with `claudeai-`, and `npm`, `github`, `gh`, `inline`, `builtin`. Pick a name other authors are unlikely to use; a user can register only one marketplace per name.
- Optional: `description` (validate warns when missing), `version`, `metadata.pluginRoot`, `forceRemoveDeletedPlugins`, `renames` (old plugin name -> new name, or `null` for a removed plugin).
- Unknown keys are ignored at load time, so a typo fails silently; `claude plugin validate` reports them as warnings.

## Plugin entries

Required: `name`, `source`. An entry also accepts every `plugin.json` field (`description`, `version`, `author`, `keywords`, ...) plus `category`, `tags`, `strict`, `displayName`, `defaultEnabled`. An entry display field (description, author, keywords, ...) overrides the `plugin.json` value in listings.

Component fields in an entry (`commands`, `agents`, `skills`, `hooks`): with the default `strict: true` they are appended to `plugin.json`; with `strict: false` and a `plugin.json` present, the plugin fails to load with `conflicting manifests`. Prefer declaring components in `plugin.json` only.

## Source types

| Type | Shape | Use when |
| :- | :- | :- |
| Relative path | `"./plugins/my-plugin"` | Plugin files live in the marketplace repository |
| `github` | `{"source": "github", "repo": "owner/repo", "ref": "v1.0.0"}` | Plugin is its own GitHub repository |
| `url` | `{"source": "url", "url": "https://git.example.com/plugin.git"}` | Git repository on any host |
| `git-subdir` | `{"source": "git-subdir", "url": "owner/monorepo", "path": "tools/my-plugin"}` | Plugin is a subdirectory of another repository |

`ref` (branch or tag) and `sha` (full 40-character commit) pin the git-based types. `npm`, `archive` and `command` sources also exist; see the source page above.

A relative path resolves only when Claude Code has the marketplace files: it works when the marketplace was added from GitHub, git or a local directory, not when it was added by a direct URL to `marketplace.json`.

## metadata.pluginRoot

`metadata.pluginRoot` (Claude Code v2.1.239+) lets an entry use a bare directory name: with `"metadata": {"pluginRoot": "./plugins"}`, `"source": "formatter"` resolves to `./plugins/formatter`. It has no effect on a source that already starts with `./`, so the `./plugins/<name>` source that `create_plugin.py` writes is never double-prefixed. A top-level `pluginRoot` key is not read.

## Team distribution

Make a hosted marketplace available to everyone working in a repository via `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "company-marketplace": {
      "source": {"source": "github", "repo": "company/marketplace"}
    }
  }
}
```
