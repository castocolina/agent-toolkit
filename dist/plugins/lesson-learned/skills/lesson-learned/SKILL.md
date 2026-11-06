---
name: lesson-learned
description: "Use when users ask what they learned, want an engineering takeaway, or reflect on recent commits, a branch diff, a specific commit, or staged/unstaged changes—even without naming Git or a principle. Ground one lesson in concrete changes and a next-time action. Not for generic engineering tutorials, ordinary bug reviews, or implementing refactors."
---

# Lesson Learned

Extract one evidence-backed engineering lesson from actual code changes. Show what the changes demonstrate, not a generic lecture.

## Load

- Always read [the diff-signal lookup](references/se-principles.md); its evidence column is the check a principle name must pass.
- Read [anti-patterns](references/anti-patterns.md) only when the candidate lesson is a cost the change introduced (a warning), not when it is about what went well.

## Choose the evidence scope

Run `git status --short` first. Then:

| Request | Evidence |
|---|---|
| Feature branch (default off the base branch) | Base: `git symbolic-ref --short refs/remotes/origin/HEAD`; if that fails, local `main` or `master` (`git rev-parse --verify --quiet main`); if neither exists, use the last 5 commits. State the base you used. Then `git log --oneline <base>..HEAD` and `git diff <base>...HEAD`. |
| Last N commits, or recent work on the base branch | `git log -p --first-parent -n <N>` (default N=5) |
| Revision range (`A..B`) | `git log -p --first-parent <range>` on the endpoints given; add no base |
| Specific commit | `git show <sha>`; for a merge commit, `git show --first-parent <sha>` |
| Working changes | `git diff`, `git diff --cached`, and every `??` path from `git status` |

If the user pasted a log or diff, read it instead of running these. An explicitly requested commit or range is used exactly as given, with no working changes added. For a default or whole-branch reflection, include uncommitted and `??` work alongside the branch commits and say so. On the base branch, a dirty tree means working changes first; add the last 5 commits only when the user asks about recent work; a clean base branch means the last 5 commits. If nothing is in scope, say there is no change evidence and stop; do not invent a lesson.

For a diff over 500 lines, read `--stat` first, then the high-signal hunks. Read an unchanged caller, contract or test only when a claim needs it, and say why you widened the scope.

## Git gotchas

- `??` files are new files that neither `git diff` nor `git diff --cached` shows. Missing them is how "no changes" gets reported for a repo full of new work. Status already hides ignored files.
- `git show <merge>` prints a combined diff that is empty for a clean merge, so a merge looks like it changed nothing. Plain `git log -p` also skips merge diffs; `--first-parent` shows what the merge brought in.
- Two dots on a diff (`git diff <base>..HEAD`) also shows base-only commits, reversed. Use three dots for branch work.

## Select and verify a lesson

1. List the candidate causal changes.
2. Rank them by observable consequence and evidence strength; a demonstrated trade-off beats a neat principle match.
3. Pick one with a defensible counterfactual: what would likely have happened without the change?
4. Verify it in code or tests. An improvement claim needs an observable consequence: changed output, a removed failure path, fewer coordinated edits for the same future change, or a test that now protects a behavior. With only the after-state, describe what changed, not an improvement.
5. Find the signal in the lookup and run its evidence check before using the principle name. If no row fits or the check fails, give the lesson without a label.

## Present

Every answer has three parts: what changed (files or commits you read, with a short code or test reference), why it matters (the observable consequence and counterfactual), and one next-time practice. Name a principle only when step 5 passed. Default to one lesson; add at most two more for independent concerns. If the changes are trivial or the evidence is thin, say so.

- Written report or notes: a `## Lesson: <principle or plain description>` heading, then **What changed:**, **Why it matters:**, **Next time:**.
- Quick conversational question: one or two short paragraphs of plain prose, with no headings, code blocks or lists. Mention commands you would run in a sentence, if at all. End with one concrete next-time practice drawn from the evidence you have; with no diff to read, make it conditional ("if the diff shows X, do Y"). Never reply only with a request for more input.

## NEVER

- NEVER let a commit message override contradictory code or tests: a message records intent, and the lesson is about what the code does.
- NEVER call many-file edits shotgun surgery, or an extraction better modularity, from file counts or moved lines alone: renames, generated output and new imports between the pieces produce the same signal (se-principles.md has the checks).
- NEVER cite a file, commit or line you did not read: the lesson is only worth the evidence it points to.
- NEVER turn the reflection into a bug review or refactor plan: the user asked what the work teaches, so give one next-time practice instead.
