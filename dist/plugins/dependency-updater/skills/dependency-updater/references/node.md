# Node.js resolver workflow

Confirm the repository's manager from lockfiles/workspace configuration (`package-lock.json`, `pnpm-lock.yaml`, or Yarn lock/config); do not generate a competing lockfile.

```bash
# Discover candidates; inspect output before writing
taze
# Discovery only; inspect candidate versions and propose a package-to-target map
taze
# After approval, update only those manifest entries to their approved versions/ranges,
# then resolve with the owning manager. Do not use broad or floating write commands.
```

After updating only approved manifest entries, run the owning manager's install command and inspect the complete manifest/lockfile diff. Confirm every resolved target matches the approved package-to-target map exactly. Do not auto-approve a package because its prior major releases were compatible. Run the project's tests, type checks, build, and audit for each cohort.

For conflicts, use the owning manager's explain/tree command first (`npm explain`, `yarn why`, or the pnpm equivalent). Overrides/resolutions can alter transitive selection but cannot repair incompatible peer APIs or runtimes; verify the final peer graph and runtime behavior.
