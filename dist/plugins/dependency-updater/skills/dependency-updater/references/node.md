# Node.js resolver workflow

Confirm the repository's manager from lockfiles/workspace configuration (`package-lock.json`, `pnpm-lock.yaml`, or Yarn lock/config); do not generate a competing lockfile. When more than one lockfile exists (for example both `package-lock.json` and `pnpm-lock.yaml`), the manager is the one named in the `packageManager` field of `package.json` (https://github.com/nodejs/corepack, checked 2026-11-16) or in the repository's documented install command; if neither says, stop and ask instead of picking one and generating its lockfile.

```bash
# Discover candidates; inspect output before writing
# Discovery only; inspect candidate versions and propose a package-to-target map.
# `taze major` does not write: it includes out-of-range and major candidates
# (read `taze --help` for the installed version's modes; checked 2026-11-15).
# Use plain `taze` only when the user asks for in-range bumps only.
taze major
# After approval (for the auto-apply cohort: after the target map and the snapshot),
# update only those manifest entries to their target versions/ranges,
# then resolve with the owning manager. Do not use broad or floating write commands.
```

After updating only the manifest entries of the shown package-to-target map (approved explicitly for ask-per-target changes, shown for auto-apply cohorts), run the owning manager's install command and inspect the complete manifest/lockfile diff. Confirm every resolved target matches that map exactly. Do not auto-approve a package because its prior major releases were compatible. Run the project's tests, type checks, build, and audit for each cohort.

## Scoped taze procedure

Checked 2026-11-15, and again 2026-11-16 for the `taze minor` semantics (latest minor within the same major), the `taze patch` mode, `--include`, `--write`, `--no-github-actions`, `--no-node-version`, `-r`, `--include-locked`, `--peer`, and the `--update`, `--install` and `--interactive` flags, against the taze README and `src/cli.ts` and `src/constants.ts` (https://github.com/antfu-collective/taze); taze was not installed here, so run `taze --help` for the live option and mode list before relying on a flag.

- Modes: plain `taze` only reports bumps inside the ranges already written in the manifest; `taze minor` also shows minor updates beyond the range, and `taze major` includes major updates. The discovery invocations in this file (`taze`, `taze minor`, `taze major`, optionally with `--json` and `-r`) change nothing. Do not assume that of every flag: `--write` (`-w`), `--update` (`-u`, update directly after bumping), `--install` (`-i`, install after bumping) and `--interactive` (`-I`) can modify files or prompt even when `--write` is absent, so `scripts/run-taze.sh` treats all of them, and any combined short flag such as `-rw`, as a write and not as a scan.
- `--json` prints the update information as JSON for agents; `-r` (`--recursive`) scans every workspace package, so use it only after confirming the workspace scope.
- Scoped write, run only in a disposable copy of the project (the default for exact targets is to edit the manifest directly, see the last bullet): `taze major --write --include pkg1,pkg2 --no-github-actions --no-node-version` for approved majors, and `taze minor --write --include <the auto-apply cohort's package names from the map> --no-github-actions --no-node-version` for the auto-apply cohort (the stable, unpinned, non-0.x MINOR and PATCH targets of the scan, written after the target map and the snapshot; add `-r` only for a confirmed workspace). `taze minor` checks changes up to the latest minor within the same major, patch changes included, so it moves a package to that latest minor, not to a smaller patch-only target in the map: for patch-only targets use `taze patch --write --include <names> --no-github-actions --no-node-version` (`patch` is in the mode list of `src/constants.ts`) or edit the manifest directly, and compare the copy's diff with the map either way. `--include` (`-n`) takes comma-separated names or `/regex/`. A write without `--include` touches every package the mode reaches: that is a broad write and is not allowed.
- taze skips locked packages (an exact version without `^` or `~`) by default; never add `--include-locked` (`-l`) to an auto-apply write, because exact pins stay unchanged unless the user asks to move them. Bumping `peerDependencies` is off by default (`--peer`), so a peer range is never moved by an auto-apply write. When the user approved a target for a package that is also declared under `peerDependencies` (for example react and react-dom in a workspace library's devDependencies and peerDependencies), change the peer range only when those specific entries (package, workspace path and section) are in the shown (and, where approval is required, approved) map, and otherwise leave it unchanged or ask: add `--peer` to the scoped taze write in the disposable copy, or edit the peer range directly, then check the diff against the map section by section (https://github.com/antfu-collective/taze, README "Peer Dependencies", checked 2026-11-16).
- Side effects: `--write` also updates GitHub Actions versions in `.github/workflows` and the Node.js version in `.nvmrc`, `.node-version` and `devEngines.runtime`. Keep the write to the manifest: the disposable-copy taze write needs `--include` (the names in the map) and both `--no-github-actions` and `--no-node-version`, never `--include` alone as a substitute for the two exclusion flags, for example `taze major --write --include pkg1,pkg2 --no-github-actions --no-node-version`, then confirm with `git diff --stat` in that copy that only the intended `package.json` files changed and copy only the entries that match the shown package-to-target map (approved explicitly for ask-per-target changes, shown for an auto-apply cohort) to the real manifest.
- taze moves a package to the latest version its mode allows, which may differ from the approved target: compare the manifest diff with the approved package-to-target map and edit the entry by hand if it differs.
- When exact targets are approved and differ from what the mode would pick, apply the approved versions directly in the manifest (the default). Alternatively run the scoped taze write in a disposable copy of the project, compare its diff with the approved package-to-target map, and copy only the approved entries to the real manifest. Then run the owning manager's install and verify the lockfile diff; never leave a floating write unchecked.

Security audit with the owning manager (checked 2026-11-15: https://docs.npmjs.com/cli/commands/npm-audit, https://yarnpkg.com/cli/npm/audit, `pnpm audit --help`):

```bash
npm audit            # npm; add --json or --audit-level=<level>
pnpm audit           # pnpm; add --json or --audit-level <level>
yarn npm audit       # Yarn Berry
yarn audit           # Yarn Classic (1.x); add --json or --level <level>
# Preview a remediation before applying it; --force allows semver-major changes
npm audit fix --dry-run --json
```

Say which Yarn is in use from the `packageManager` field or the lockfile format (Classic and Berry write different `yarn.lock` formats) and run only that Yarn's audit command (Classic: https://classic.yarnpkg.com/en/docs/cli/audit, checked 2026-11-16). When the audit cannot be run, report the scanner as unavailable and stop; never substitute another manager's audit.

Run `npm audit fix --dry-run --json` before any `npm audit fix --force`, and treat every major target it proposes as needing approval like any other breaking update.

For conflicts, use the owning manager's explain/tree command first (`npm explain`, `yarn why`, or the pnpm equivalent). Overrides/resolutions can alter transitive selection but cannot repair incompatible peer APIs or runtimes; verify the final peer graph and runtime behavior.
