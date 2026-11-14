# plugin-forge: sources (checked 2026-11-13)

## Origins found

1. **softaworks/agent-toolkit, `skills/plugin-forge`.** The baseline (`dbff837f`) tree of `skills/plugin-forge/` is byte-identical to the fork point `3027f20f` (`git diff --stat 3027f20f dbff837f -- skills/plugin-forge` is empty). Upstream's only commit on the path is `c0556074cf27084747944ce5655a0f886d0d9c9c` (2026-01-18, Leonardo Flores / @leonardocouy, "feat: add plugin-forge skill and fix perplexity frontmatter"), which predates the fork, so upstream has had no change since the fork point. `gh api repos/softaworks/agent-toolkit/contents/skills/plugin-forge?ref=main` still lists README.md, SKILL.md, references and scripts. The upstream files carry no credit, license or author line of their own. The registry has only the repo-level `softaworks/agent-toolkit` row (skill null) and no `plugin-forge` row; the root README credits the fork as a whole ("Fork of softaworks/agent-toolkit by @leonardocouy").
2. **davila7/claude-code-templates, `cli-tool/components/skills/development/plugin-forge`.** Its SKILL.md is byte-identical to the baseline SKILL.md (`diff` empty), and its README and references/scripts carry the same file set. Its single commit on the path is 2026-01-25 ("Add component migrator agent and migrate initial components"), seven days after the softaworks commit, so it is a later copy or a sibling copy of the same text, not an origin we can credit; the MIT repository carries no author line in the skill. No registry row and no credit line is proposed. Recorded so a later reader does not mistake it for the source.
3. **Official Claude Code plugin docs** (code.claude.com) used to verify every fact in facts.md. Each page is an `unversioned` row. The CLI itself (`claude` 2.1.323) was also run; tool output needs no row.

No other uncredited origin was found: a web search on "Plugin Forge streamlines the entire lifecycle of Claude Code plugin development" and on the script names returned only third-party directory listings of the same softaworks or davila7 text.

## Proposed registry rows (docs/audit/upstream-sources.json, one JSON object per line)

```json
{"skill": "plugin-forge", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/plugin-forge", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Plugins overview: https://code.claude.com/docs/en/plugins", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Create a plugin (layout, --plugin-dir, claude plugin init): https://code.claude.com/docs/en/plugins/create", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Plugin manifest reference (fields, name rules, path rules, standard layout): https://code.claude.com/docs/en/plugins/manifest-reference", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Add components to a plugin (component names, hooks, bin/): https://code.claude.com/docs/en/plugins/components", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Marketplace reference (fields, reserved names, sources, strict mode): https://code.claude.com/docs/en/plugins/marketplace-reference", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Create a marketplace (walkthrough, validate, local test): https://code.claude.com/docs/en/plugins/create-marketplace", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Host and maintain a marketplace (release a new version, renames): https://code.claude.com/docs/en/plugins/host-marketplace", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Plugin loading reference (versions, in-place plugins): https://code.claude.com/docs/en/plugins/loading", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Publish and distribute a plugin (pre-release checklist, tagging): https://code.claude.com/docs/en/plugins/publish", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Plugin commands reference (claude plugin subcommands, /reload-plugins): https://code.claude.com/docs/en/plugins/cli-reference", "ref": null, "credit": "Anthropic"}
{"skill": "plugin-forge", "kind": "unversioned", "source": "Claude Code docs, Hooks reference (hook events): https://code.claude.com/docs/en/hooks", "ref": null, "credit": "Anthropic"}
```

The `github-path` row can be tracked (upstream exists, path resolves, unchanged since the fork). Known limit: `upstreams` reports `stale: false` for every `unversioned` row, so no scheduled run notices a changed docs page; the check date in facts.md is the reader's age signal.

## Credit line

The README has no credit line, so the softaworks origin is uncredited in the skill. Exact lines to add at the end of `skills/plugin-forge/README.md` (same wording as the sibling skills `mui` and `naming-analyzer`, plus the docs owners as `naming-analyzer` does):

```markdown
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-13): Anthropic (Claude Code plugin documentation).
```

The root README line "Fork of softaworks/agent-toolkit by @leonardocouy" stays untouched.

## Skill-updater style review (review only, no `track` call)

Scope `skills/plugin-forge/`; the artifact is not gepetto or datadog-cli.

- **Step 2 (rows).** No `plugin-forge` row exists, so `upstreams` has nothing to report; the review above proposes the rows. Once the `github-path` row is added, the controller may run `python3 scripts/audit/audit.py track --registry docs/audit/upstream-sources.json --artifact plugin-forge --source softaworks/agent-toolkit:skills/plugin-forge --status current --sha c0556074cf27084747944ce5655a0f886d0d9c9c` (not run here). The row's `ours_updated` reads `git log` on SKILL.md and references/, which has commits, so it will not hit the `no local commit` case.
- **Step 4 (upstream change).** None: upstream's only commit predates the fork, `gh api` shows no later commit on `skills/plugin-forge`. Adopt: none. Adapt: none. Ignore: nothing to ignore.
- **Adopt and adapt items from the docs review (for the Step 6 brief; none restores baseline text):**
  1. Adopt, SKILL.md Script contract: add exact `anthropics` to the reserved-name sentence and say `claude plugin init` and `claude plugin tag` refuse such a name, or point to the live name table in the manifest reference (facts row 1, outcome corrected).
  2. Adopt, SKILL.md Workflow step 1: say that besides `github`, `git-subdir` and `url`, plugins can also come from `npm`, `archive` and `command` sources, which are not a git repository, and point at marketplace-schema.md (facts row, outcome corrected).
  3. Adopt, references/plugin-structure.md: remove the unverified "settings.json: only `agent` and `subagentStatusLine` take effect" comment or replace it with a pointer to the live Standard layout; the fixer needs a record row for that removed line (a `para:` row, `removed-on-merit`, `low`, `intended-change`, `fact-update`).
  4. Adopt, references/plugin-structure.md: add `anthropics-` to the prefix list; bump the "checked" date; change "Claude Code 2.1.318" to "2.1.323" in the `claude plugin details` note (rechecked 2026-11-13); mention that `workflows/`, `themes/` and `monitors/monitors.json` also exist and that `skills/` is preferred over `commands/` for new plugins, pointing to the Standard layout.
  5. Adapt, references/marketplace-schema.md (Top-level fields, `name`): write the reserved-name sentence as examples plus a pointer to the live Reserved names section, because the enumerated list is incomplete (pip, uv, cargo, skills-dir, synced, claude-plugin-test, JavaScript member names).
  6. Adapt (replaces the stale hook-event list of s057 with a live value): add one line to plugin-structure.md pointing to https://code.claude.com/docs/en/hooks.md#hook-events and noting that `hooks/hooks.json` wraps the event map in a top-level `"hooks"` key (a file with only the event map fails to load). This is the `point, do not pin` answer for the dropped nine-event list.
  7. Optional adapt, SKILL.md Workflow step 1: a personal plugin that needs no marketplace can be scaffolded with `claude plugin init <name>` (writes `~/.claude/skills/<name>/`, loads as `<name>@skills-dir`); today the skill says nothing about it and the description excludes "standalone skills/commands without plugin packaging". Add only a one-line pointer to the Create page if the controller judges it within scope.
  8. Optional adapt, SKILL.md Script contract: list the JSON keys each script prints (create: `status`, `plugin`, `paths`, `version` or `marketplace_entry` for `--dry-run`; bump: `status`, `plugin`, `old_version`, `new_version`, `paths`) so a caller can parse them; the old human console samples (s015, s016) are dropped as stale.
  9. Optional adapt, workflows.md Local install test: validation can use `claude plugin validate --strict` in CI (exit 1 on warnings), and `--profile directory` exists for directory submissions (CLI 2.1.323); only add if it serves the skill's publish step.
- **Model-validity pass (step 6).** Not run: it needs an LLM probe lane, which the analyst rails forbid. Rules that could counter a model habit, for the controller to probe: "set `version` in one place" (a model may sync both files, as the baseline did), "stage only the plugin directory and marketplace.json, never `git add .`", and "never push to the default branch unless asked". The other rules are factual and docs-backed.
