# Batch 55

## commit-work (skill)

### commit-work#D7-1
- severity: low
- dimension: D7
- location: skills/commit-work/evals/evals.json:10
- fix: In review-and-commit, add an assertion that the staged version is verified (step 5) and that `git write-tree` runs before the commit and is compared with `git rev-parse 'HEAD^{tree}'` after it. Also add an eval whose fixture shows a pre-commit hook that reformats a file and lets the commit succeed. Assert that the agent reports the tree difference and asks before amending.

### commit-work#D8-1
- severity: low
- dimension: D8
- location: skills/commit-work/SKILL.md:31
- fix: Name the directory: `git checkout-index -a --prefix=<gitdir>/commit-work-verify/`. This keeps it out of `git status`, and step 8's existing cleanup of `<gitdir>/commit-work*` then removes it. Today the export location and its removal are left to guesswork.

### commit-work#D6-1
- severity: high
- dimension: D6
- location: skills/commit-work/SKILL.md:34
- fix: Create a uniquely named scratch directory under the Git directory for each run, place its temporary index, patches and message there, and clean up only that run-owned directory. Remove the wildcard cleanup instruction.

### commit-work#D8-1
- severity: medium
- dimension: D8
- location: skills/commit-work/SKILL.md:29
- fix: Gate the partial-file patch method on the path being tracked. For an untracked path, explicitly stop and ask whether the whole file is approved or request the exact approved new-file content; explain that ordinary git diff omits untracked files rather than proceeding with an empty patch.

### commit-work#D1-1
- severity: low
- dimension: D1
- location: skills/commit-work/SKILL.md:32
- fix: Shorten this to 'Write the message in Conventional Commits 1.0.0; the body says why.' The model already knows the header, body and footer layout. Keep the parts it lacks: `-F <gitdir>/commit-work-msg.txt` instead of a bare `git commit`, the no-trailers default and the gated reference read.

### commit-work#D1-2
- severity: low
- dimension: D1
- location: skills/commit-work/SKILL.md:8
- fix: Keep only the non-obvious part: 'Split by behavior: an implementation and the tests that pin it go in the same commit.' Drop the generic atomic-commit definition.

### commit-work#D1-1
- severity: low
- dimension: D1
- location: skills/commit-work/SKILL.md:10
- fix: Condense the familiar intent table into a short guard preserving its safety boundaries: drafting and review are read-only, drafting returns only message text, staging stops after step 4, and committing requires approval. Retain the detailed non-obvious index and hook procedures.
