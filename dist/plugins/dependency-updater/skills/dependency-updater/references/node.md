# Node.js resolver workflow

Confirm the repository's manager from lockfiles/workspace configuration (`package-lock.json`, `pnpm-lock.yaml`, or Yarn lock/config); do not generate a competing lockfile.

```bash
# Discover candidates; inspect output before writing
# Discovery only; inspect candidate versions and propose a package-to-target map.
# `taze major` does not write: it includes out-of-range and major candidates
# (read `taze --help` for the installed version's modes; checked 2026-11-15).
# Use plain `taze` only when the user asks for in-range bumps only.
taze major
# After approval, update only those manifest entries to their approved versions/ranges,
# then resolve with the owning manager. Do not use broad or floating write commands.
```

After updating only approved manifest entries, run the owning manager's install command and inspect the complete manifest/lockfile diff. Confirm every resolved target matches the approved package-to-target map exactly. Do not auto-approve a package because its prior major releases were compatible. Run the project's tests, type checks, build, and audit for each cohort.

## Scoped taze procedure

Checked 2026-11-15 against the taze README and `src/cli.ts` (https://github.com/antfu-collective/taze); taze was not installed here, so run `taze --help` for the live option and mode list before relying on a flag.

- Modes: plain `taze` only reports bumps inside the ranges already written in the manifest; `taze minor` also shows minor updates beyond the range, and `taze major` includes major updates. Without `--write` (`-w`) nothing is changed.
- `--json` prints the update information as JSON for agents; `-r` (`--recursive`) scans every workspace package, so use it only after confirming the workspace scope.
- Scoped write after approval, run only in a disposable copy of the project (the default for exact targets is to edit the manifest directly, see the last bullet): `taze major --write --include pkg1,pkg2` (or `taze minor ...` when every approved target is a minor or patch). `--include` (`-n`) takes comma-separated names or `/regex/`. A write without `--include` touches every package the mode reaches: that is a broad write and is not allowed.
- Side effects: `--write` also updates GitHub Actions versions in `.github/workflows` and the Node.js version in `.nvmrc`, `.node-version` and `devEngines.runtime`. Keep the write to the manifest with `--no-github-actions --no-node-version` (or `--include`), for example `taze major --write --include pkg1,pkg2 --no-github-actions --no-node-version`, then confirm with `git diff --stat` in that copy that only the intended `package.json` files changed and copy only the entries that match the approved map to the real manifest.
- taze moves a package to the latest version its mode allows, which may differ from the approved target: compare the manifest diff with the approved package-to-target map and edit the entry by hand if it differs.
- When exact targets are approved and differ from what the mode would pick, apply the approved versions directly in the manifest (the default). Alternatively run the scoped taze write in a disposable copy of the project, compare its diff with the approved package-to-target map, and copy only the approved entries to the real manifest. Then run the owning manager's install and verify the lockfile diff; never leave a floating write unchecked.

Security audit with the owning manager (checked 2026-11-15: https://docs.npmjs.com/cli/commands/npm-audit, https://yarnpkg.com/cli/npm/audit, `pnpm audit --help`):

```bash
npm audit            # npm; add --json or --audit-level=<level>
pnpm audit           # pnpm; add --json or --audit-level <level>
yarn npm audit       # Yarn Berry
# Preview a remediation before applying it; --force allows semver-major changes
npm audit fix --dry-run --json
```

Run `npm audit fix --dry-run --json` before any `npm audit fix --force`, and treat every major target it proposes as needing approval like any other breaking update.

For conflicts, use the owning manager's explain/tree command first (`npm explain`, `yarn why`, or the pnpm equivalent). Overrides/resolutions can alter transitive selection but cannot repair incompatible peer APIs or runtimes; verify the final peer graph and runtime behavior.
