# Two commits from one file

Read this from SKILL.md step 3 when a single tracked file holds hunks for two different commits, for example `src/components/Header.js` with a mobile-menu z-index bugfix and a refactor that extracts the menu logic into a hook. The bugfix goes first, the refactor second. `<run>` is the run directory from step 3, written literally into every command.

1. Capture the file's changes with one line of context, so nearby hunks stay apart: `git diff -U1 -- src/components/Header.js > <run>/all.diff`. Read the hunks and sort each into the bugfix or the refactor. If one hunk mixes both, stop and ask; never edit hunk counts by hand.
2. Copy `<run>/all.diff` to `<run>/pick.diff` and delete every refactor hunk, whole hunks only, keeping the file header. `pick.diff` now holds the bugfix alone.
3. Check, then stage the pick file into the index only: `git apply --cached --check <run>/pick.diff`, then `git apply --cached <run>/pick.diff`. With a temporary index (user content staged elsewhere), put the same `GIT_INDEX_FILE=<run>/index` prefix on both.
4. Review as step 4 says: `git diff --cached` shows only the bugfix hunks, and `git diff -- src/components/Header.js` still shows the refactor, unstaged. Verify the staged version as step 5 says: the bugfix must pass on its own, without the refactor.
5. Commit the first change, for example `git commit -m "fix(ui): correct mobile menu z-index"`.
6. Second commit: the file now differs from `HEAD` only by the refactor. Run step 3 again against the new `HEAD` (`git add -- src/components/Header.js` stages the rest of the file; with a temporary index, rebuild it from the new `HEAD` first), then steps 4 to 7, and commit, for example `git commit -m "refactor(ui): extract menu logic to custom hook"`.

If the refactor and the bugfix cannot pass the check separately (the bugfix needs the extracted hook), they are one change: commit them together.
