---
name: dependency-updater
description: "Audit, diagnose, and conservatively update project dependencies and lockfiles across Node, Python, Go, Rust, Ruby, Java, and .NET. Auto-applies safe minor and patch updates after a recoverable snapshot, with tests and a security audit per cohort, and asks before every major, 0.x or prerelease change. Use when asked to update dependencies, update the safe ones automatically, find outdated packages, resolve dependency conflicts, or remediate vulnerable packages. Not for runtime upgrades, package publishing, or Renovate configuration."
license: MIT
metadata:
  version: 1.0.0
---

# Dependency Updater

## Update policy

Auto-apply set: a PATCH or MINOR target of a dependency that is stable (not a 0.x version and not a prerelease), not exact-pinned, and whose update breaks no peer, ABI or runtime-floor constraint (read a target-specific dry run: the proposed constraint written in a disposable copy of the manifest, or a version-qualified resolver argument such as `npm install <pkg>@<version> --dry-run`; a package-only command (`poetry update <pkg> --dry-run`, `uv lock --upgrade-package <pkg> --dry-run`) may select a different version, so read the version it resolves and compare it with the mapped target, together with the runtime range the package declares, for npm its `engines` range; a dry run that does not name the target says nothing about it, and if the check cannot establish compatibility, ask per target). Exact pins stay unchanged unless the user asks to move them.

Ask per target, never auto-apply: every MAJOR, every 0.x or prerelease change, any update that fails a peer/ABI/runtime check, an exact pin the user wants moved, and anything the user asked to be asked about. The reason for 0.x: a 0.x version carries no compatibility promise, so even a nominal minor or patch update can break compatibility, whatever the scanner labels it; say so when you ask. When the user says "ask first", ask for every target. The table of update types and actions is in [update policy](references/update-policy.md); load it at step 4, when sorting scan targets into the auto-apply or ask-per-target set (its Fixed row also serves step 2).

## Constraint-first procedure

Branch on intent first. For an audit-only, diagnosis-only or outdated-list request, do steps 1 to 4 as non-mutating discovery, report the findings and candidates, and write nothing; enter the write workflow (steps 5 to 9) only when the user asked for updates. An audit-only request (vulnerabilities, "audit dependencies") instead runs the ecosystem's security scanner in its non-mutating mode and reports its findings and any scanner errors, without entering the update workflow.

1. Inspect the worktree; preserve unrelated edits. Identify the manifest, owning resolver, lockfile, runtime/toolchain envelope, and workspace topology. Multiple manifests may belong to different managers; never infer ownership from file presence alone. Verify the required tools are installed (see Scripts) and suggest the install command when one is missing.
2. Use the owning manager's constraint grammar to classify each dependency as exact, bounded, or unbounded. Do not infer pinning from `^`/`~`; Python, Ruby, Maven, Go, and .NET have different grammars. For 0.x versions and prerelease tags, even a nominal minor update can break compatibility. Dependencies pinned to an exact version stay unchanged unless the user asks to move them; say so in the plan and report. A Go `go.mod` requirement is a minimum-version-selection requirement, a deliberate pin only when the user or a comment says so (https://go.dev/ref/mod#minimal-version-selection, checked 2026-11-15); when unsure, ask the user.
3. Identify coupled workspace packages and peer/ABI/runtime constraints. Form compatible update cohorts; keep separate versions when consumers need incompatible majors.
4. Scan candidates, inspect release notes and the proposed manifest/lockfile diff, and sort every target into the auto-apply set or the ask-per-target set. Before the first write of any kind (an auto-applied cohort, or an approved MAJOR or other ask-per-target change when there is no auto-apply cohort), run the security audit once on the unchanged state as the baseline. If the scanner is unavailable or errors, report the blocker and stop before any write: a cohort is never applied without a baseline, unless the user explicitly decides to proceed without one.
5. Auto-apply each safe cohort: show the cohort's package-to-exact-target map; take a recoverable snapshot of the manifest and lockfile before any write (a copy outside the project, or a clean committed state when those files have no uncommitted edits; never overwrite unrelated user edits, preserve them); then write the targets as in step 7 and verify as in step 8. Report what was applied: each package with its exact version.
6. Ask about each MAJOR, 0.x or prerelease target and every other ask-per-target change individually, showing current to target version and the release notes. Package names never imply blanket approval, and an approved set stays explicit: a set of MAJOR, 0.x or prerelease targets is authorized only when the user explicitly identifies its targets. Apply approved targets one cohort at a time with the same snapshot, write and verify steps.
7. Update manifest and lockfile together with the owning resolver. Never use a different manager to generate a lockfile. Without a lockfile, update one package at a time and record the exact resolved version.
8. Run the resolver install/check, applicable tests, type checks, build, and security audit for each cohort, and compare the audit with the baseline. If the scanner could not run, stop and report that; never treat it as a pass: restore that cohort's snapshot unless the user explicitly decides to keep the unverified change, and ask before proceeding. A finding already in the baseline is reported, not a cohort failure, and a cohort that fixes a vulnerability stays even when unrelated findings remain. On a new or worsened finding, or any failing install, test, type check or build, stop, restore the snapshot of that cohort, report the exact failing command and the failing test or error, and ask before proceeding. The snapshot covers only the manifest and lockfile, so after restoring them name the installed environment the install may have changed (node_modules, virtualenv, vendor directory), keep user-owned state, and reinstall with the owning manager from the restored lockfile, asking first when the reinstall would delete anything beyond the managed dependency directory; report it if the environment cannot be restored. Preserve unrelated user changes.
9. Finalize: when at least one cohort was applied, run the install command and the security audit on the final state; when nothing was applied (every target declined, or an audit-only request), skip the install and report the scan. Then write the Report.

Before any write, produce a reviewable package-to-exact-target map, and say whether each proposal is non-mutating (read from a scan or an explain/tree command) or comes from a resolver-generated diff, which needs a disposable worktree so the real manifest and lockfile stay untouched.

## NEVER

- NEVER auto-apply a MAJOR, 0.x, prerelease, exact-pin or failed-peer-check target: a nominal semver-compatible bump is not proof of compatibility, so each one is asked per target.
- NEVER run a write-mode taze without `--include`: a mode without it rewrites every package it reaches, including GitHub Actions versions and Node version files, far beyond the approved set.
- NEVER delete a lockfile or environment before the explain or tree diagnosis, an approval and a snapshot: the reset discards the only reproducible dependency graph and the re-resolved one can differ silently.
- NEVER let another manager regenerate a lockfile: the resolved graph changes silently and builds stop being reproducible.

## Non-obvious failure modes

- npm overrides require a compatible npm version and can still leave direct-dependency peer contracts unsatisfied; Yarn Classic and Berry have distinct resolution behavior. A forced tree is not evidence of runtime/API compatibility.
- Lifecycle scripts may execute package code during install. Do not bypass review or run install scripts merely to make resolution succeed; follow the repository's established trust controls.
- A lockfile generated by another package manager or version may silently alter the resolved graph and make builds irreproducible.
- Python `pip` does not maintain a project lockfile by default. For Poetry, Pipenv, or another lock owner, use that owner's resolver and update the lock; don't substitute an environment-only `pip install`.
- A nominal semver-compatible update can still violate a peer requirement, ABI, or runtime floor. Check the actual resolver output and supported environment.

## Supported non-obvious operations

- Node: use `taze` for candidate discovery and scoped writes; recurse only after confirming workspace scope. See [Node workflow](references/node.md). Load node.md only for a Node manifest. Order for a Node write:
  1. By default edit the target versions directly in the manifest.
  2. Alternatively run a scoped taze write, only in a disposable copy of the project: `taze minor --write --include <the scanned candidate names> --no-github-actions --no-node-version` for the auto-apply cohort, or `taze major --write --include pkg1,pkg2 --no-github-actions --no-node-version` for approved majors (add `-r` only for a confirmed workspace). `taze minor` checks changes up to the latest minor within the same major (patch changes included), so it moves a package to that latest minor even when the map holds a smaller patch-only target: for patch-only targets use `taze patch --write --include <names> --no-github-actions --no-node-version`, or edit the manifest directly.
  3. After a taze write, compare the copy's diff with the package, workspace path and target map.
  4. Copy only the matching entries to the real manifest.
  5. Resolve with the owning manager.
  6. Check the complete diff.

  `-w`/`--write` also rewrites GitHub Actions versions and Node version files unless those two flags are set, and `--include` names only the cohort's packages.
- Python: update one package at a time when no lock owner exists; use the detected lock owner otherwise. See [Python workflow](references/python.md). Load python.md only when pip, Poetry, Pipenv or uv owns the graph.
- Other managers: use their native resolver and explicit target versions; see [manager commands](references/managers.md). Load managers.md only for Go, Cargo, Bundler, Maven, Gradle or .NET. For a Node task do not load python.md or managers.md.
- Scripts: resolve them from this skill's directory (the directory that holds this SKILL.md; for an installed skill use `${CLAUDE_PLUGIN_ROOT}/skills/dependency-updater/scripts/` or `$HOME/.claude/skills/dependency-updater/scripts/`, whichever exists), not from the project, and run them with the target project as the working directory.
- Scripts: for a prerequisite check, read and run `scripts/check-tool.sh <tool> [install-command]` (one JSON line on stdout, diagnostics on stderr, `--help` for usage).
- Scripts: for an unattended candidate scan of a Node project, first run `scripts/check-tool.sh taze` (prerequisite), then `scripts/run-taze.sh [-r] major` with the project as the working directory: the `major` mode also reports out-of-range and major candidates and writes nothing (JSON on stdout, diagnostics on stderr, `--help` for usage); add `-r` only for a confirmed workspace, and run `scripts/run-taze.sh [-r]` with no mode only when the user asks for in-range bumps only. Report the candidates for approval and apply nothing from a scan-only request. A candidate scan puts taze's parsed JSON in the `candidates` field (`{"status":"ok","candidates":{...}}`); when taze's output is not valid JSON it falls back to the text report in the `output` field (`{"status":"ok","output":"..."}`).

## Recovery and security

For a dependency conflict (a failed install, a peer error), run the owning manager's explain/tree command first (`npm explain <package>`, `yarn why`, `pnpm why`) and explain the conflict before changing anything; for a diagnosis-only request, propose the targeted change and write nothing; when the user requests or approves a fix, change the named package's version in a targeted way and verify it with the owning manager's install, the tests and a review of the lockfile diff. Before destructive recovery (deleting a lockfile, environment, or cache), diagnose with the manager's explain/tree command, get explicit approval, and save a recoverable snapshot. Security remediation timelines are suggestions subordinate to user priorities, not imposed SLAs. Never treat an override, cache clear, or lockfile deletion as a first-line fix.

## Report

Summarize candidates, the auto-applied cohorts and the approvals for the rest, changed packages and exact versions, lockfile changes, commands and gate results, any snapshot restored, unresolved vulnerabilities, and any blocker. Do not claim success if a required test/build/audit failed.
