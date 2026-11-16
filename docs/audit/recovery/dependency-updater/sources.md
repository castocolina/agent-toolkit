# Sources: dependency-updater

Checked 2026-11-15. Review only: no `track` call made, nothing edited under `skills/`, no registry or README edit (the controller applies the rows and the credit line below).

## Origin

- The whole skill is the softaworks/agent-toolkit skill `skills/dependency-updater` (added there 2026-01-18, commit `011baf4a`, its only commit). At baseline `dbff837f` SKILL.md, README.md and `scripts/` are byte-identical to `3027f20f` (blob ids `edede5b7`, `ef1cda22`, `07f3427a`), and the same blobs are still upstream `main` today (`gh api repos/softaworks/agent-toolkit/contents/skills/dependency-updater`). Nothing before it: the upstream skill has no credit line of its own.
- `davila7/claude-code-templates` (`cli-tool/components/skills/development/dependency-updater`, 2026-01-25) carries the identical SKILL.md blob `edede5b7`: a later copy of softaworks, not an origin. `connorads/dotfiles` and the skill directories (tessl, skills.sh, playbooks) list further copies. No earlier author was found by phrase search, so softaworks is the origin.
- Current files (references/, evals, rewritten SKILL.md and scripts) are this repo's own work on top of that origin.
- The registry has no row for `dependency-updater`, only the repo-level `softaworks/agent-toolkit` row; `docs/audit/upstream-sources.md` lists the skill as "incidental-link", which is wrong for the softaworks origin. README.md of the skill has no Credits section.

## Credit line to add (skills/dependency-updater/README.md, new `## Credits` section before `## License`, same wording as database-schema-designer, gemini and commit-work)

```text
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Tool commands and flags were checked against the official documentation of each tool (taze, npm, pnpm, pip, Go, Cargo, Bundler, Maven, .NET) on 2026-11-15.
```

The second paragraph is optional; the first is the missing credit line.

## Proposed registry rows (docs/audit/upstream-sources.json; `validate_entry` fields: skill, kind, source, ref, credit)

Origin row (convention of the 26 other `softaworks/agent-toolkit:skills/<name>` rows):

```json
{
  "skill": "dependency-updater",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/dependency-updater",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

Official pages used for the facts (one `unversioned` row each; `upstreams` never marks them stale, so only a `skill-updater` run re-reads them):

```json
[
  {"skill": "dependency-updater", "kind": "unversioned", "source": "taze README and CLI options: https://github.com/antfu-collective/taze", "ref": null, "credit": "Anthony Fu (antfu-collective)"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "npm Docs, package.json overrides: https://docs.npmjs.com/cli/configuring-npm/package-json#overrides", "ref": null, "credit": "npm (GitHub)"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "npm Docs, npm audit: https://docs.npmjs.com/cli/commands/npm-audit", "ref": null, "credit": "npm (GitHub)"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "pnpm CLI, pnpm audit: https://pnpm.io/11.x/cli/audit", "ref": null, "credit": "pnpm"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "Yarn manifest, resolutions: https://yarnpkg.com/configuration/manifest", "ref": null, "credit": "Yarn"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "Yarn CLI, yarn npm audit: https://yarnpkg.com/cli/npm/audit", "ref": null, "credit": "Yarn"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "Go, Vulnerability Management: https://go.dev/doc/security/vuln/", "ref": null, "credit": "The Go Authors"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "The Cargo Book, cargo update: https://doc.rust-lang.org/cargo/commands/cargo-update.html", "ref": null, "credit": "The Rust Project"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "RustSec cargo-audit: https://github.com/rustsec/rustsec/tree/main/cargo-audit", "ref": null, "credit": "RustSec"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "RubyGems Guides, bundle update: https://guides.rubygems.org/command-reference/bundle-update/", "ref": null, "credit": "Bundler team"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "bundler-audit README: https://github.com/rubysec/bundler-audit", "ref": null, "credit": "RubySec"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "Versions Maven Plugin, versions:use-dep-version: https://www.mojohaus.org/versions/versions-maven-plugin/use-dep-version-mojo.html", "ref": null, "credit": "MojoHaus"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "OWASP DependencyCheck, Maven plugin: https://github.com/dependency-check/DependencyCheck#maven-plugin", "ref": null, "credit": "OWASP"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": ".NET CLI, dotnet package list: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package", "ref": null, "credit": "Microsoft"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": ".NET CLI, dotnet package add: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-add-package", "ref": null, "credit": "Microsoft"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "dotnet-outdated README: https://github.com/dotnet-outdated/dotnet-outdated", "ref": null, "credit": "dotnet-outdated contributors"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "Safety CLI README: https://github.com/pyupio/safety", "ref": null, "credit": "Safety Cybersecurity"},
  {"skill": "dependency-updater", "kind": "unversioned", "source": "pip-review README: https://github.com/jgonggrijp/pip-review", "ref": null, "credit": "Joris Gonggrijp"}
]
```

Registry rows added in PR 6 review fix wave 1 (2026-11-16, `unversioned`, pages used in facts.md or the references that had no row; matched by URL against the registry first):

- https://semver.org/#spec-item-4 (Tom Preston-Werner)
- https://github.com/nodejs/corepack (Node.js, Corepack)
- https://classic.yarnpkg.com/en/docs/cli/audit (Yarn)
- https://dependency-check.github.io/DependencyCheck/dependency-check-gradle/ (OWASP)
- https://docs.astral.sh/uv/reference/cli/ (Astral)
- https://docs.astral.sh/uv/concepts/projects/sync/#upgrading-locked-package-versions (Astral; cited in python.md)
- https://docs.npmjs.com/cli/commands/npm-install (npm, GitHub)
- https://docs.npmjs.com/cli/using-npm/config (npm, GitHub)
- https://go.dev/ref/mod#minimal-version-selection (The Go Authors)
- https://python-poetry.org/docs/cli/#update (Poetry; cited in python.md)
- https://pipenv.pypa.io/en/latest/commands.html (Pipenv, Python Packaging Authority; cited in python.md)

Tool output used instead of a page (no row): `go help get|list|mod tidy` (go 1.27.4), `pnpm audit|why --help` (11.18.0), `pip help lock|list|check` (26.1.2), `uv lock|pip tree --help` (0.11.28).

## Skill-updater review (REVIEW ONLY; adopt / adapt / ignore for the restore brief)

Upstream state: no change since the fork point (all three upstream blobs equal `3027f20f`; one upstream commit in total). `upstreams` was not run: there is no registry row yet, so there is nothing to read; once the origin row is added, expect `stale: false`.

- ignore: any upstream change (none exists); the davila7 and connorads copies (downstream copies, not sources).
- adapt: restore s033 into references/node.md as the scoped taze procedure (modes, `--write`, `--include`, `-r`, `--json`, `--help` pointer, the GitHub Actions and Node-version side effect of `-w`, `--no-github-actions --no-node-version`, per-manager audit commands, `npm audit fix --dry-run --json` before any `--force`). Keep the current approval rule: do not restore the broad `taze minor --write`.
- adapt: restore s054 as a two-line conditional pointer in SKILL.md (check-tool.sh to verify a prerequisite tool, run-taze.sh for Node discovery in the target project's directory), per the two D5 findings of 2026-10-28.
- adapt: references/node.md lists the plain `taze` command twice (lines 7 and 9, two comments over one command); keep one.
- adapt (README, human-facing, still describes the baseline): reconcile with SKILL.md and give any removed README line a record row. Stale or unsafe items: "applies safe updates automatically" and the PATCH/MINOR auto-apply rows (decided by the s031/s032/s047 user answer, as is `.claude-plugin/marketplace.json`'s description "applies safe updates automatically, prompts for major versions" and eval 1's expected output); `rm go.sum`; the `rm -rf node_modules package-lock.json` reset; `mvn dependency-check:check` (use `mvn org.owasp:dependency-check-maven:check`); `pip-review` as the Python tool; `safety` (now `safety scan`); `dotnet outdated` with no install row (`dotnet tool install --global dotnet-outdated-tool`); the "Fix within 24 hours" table, which SKILL.md calls a suggestion, not an SLA.
- adapt (scripts, open findings from the 2026-10-28 judges, not part of this recovery): `check-tool.sh` `json_string` does not escape control characters (D8-1); `run-taze.sh` needs python3 without checking for it (D8-2), uses a here-string (`<<<`, which the repo's shell rules avoid; `printf '%s' "$output" | python3 -c ...` is the simple form), and captures taze output, so interactive `-I` cannot work (taze has `--json` for agent use).
- ignore: the 2026-10-28 D1 and D2 low suggestions that would add behavior (lockfile-conflict heuristics, fallback to `npm outdated`) are the judge's wishes, not baseline content; not recovery work.
- Model-validity pass: none run. The skill has no rule that exists to suppress a probe-able model habit (its rules are approval, ownership and destructive-recovery gates, which are procedure, not style); nothing proposed for removal.
- No `track` call is proposed until the origin row exists, and then it is the controller's call.
