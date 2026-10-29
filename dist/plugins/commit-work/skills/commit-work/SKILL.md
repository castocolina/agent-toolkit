---
name: commit-work
description: Create or prepare reviewable Git commits by inspecting intended changes, selectively staging coherent units, reviewing the index, and writing Conventional Commit messages. Use when asked to commit work, stage selected changes, split a mixed tree, review staged content, or draft a commit message. Not for rebasing, squashing or force-pushing history, opening pull requests, or general code review unrelated to a commit.
---

# Commit work

Make each commit a coherent, independently buildable and testable change. Keep implementation and required tests together; separate tests only when they independently characterize existing behavior or form another self-contained change.

## Workflow

1. Establish which changes are approved for this task. Inspect status, staged diff, and working-tree diff; treat pre-existing index content as user-owned unless explicitly included. If unrelated staged content exists, stop and request authorization for an index-isolation strategy. Never proceed with an ordinary commit that would include unrelated staged content.
2. Define logical boundaries by behavior and independent verification, not by file category. Stop if merge conflicts remain unresolved.
3. Stage unmixed files by path. For mixed files, construct reviewed per-change patches and use `git apply --cached <patch>` in non-interactive shells; use `git add -p` only when an interactive human terminal is available. Do not stage broad repository paths indiscriminately.
4. Review the exact index (`git diff --cached`) and ensure it contains only the approved commit. Check secrets, generated artifacts, lockfile churn mixed with unrelated logic, and scope accuracy against current paths.
5. Run the fastest meaningful verification for the staged change: tests touching staged paths, then repository lint, then build; run the first applicable check. If it fails, stop, report the failure, and get direction. After verification-driven edits, review the staged diff again.
6. Write a Conventional Commit message. Use non-interactive `git commit -m` for a single-line message or `git commit -F <message-file>` for a body/footer. Read `references/commit-message-template.md` when the repository defines custom types/scopes, the user asks about format, or a multi-line body/breaking-change footer is needed. Do not retry a failed/empty commit blindly; inspect status and the index first.
7. After a commit, report its hash/message and verification. If verification after committing fails, stop and ask before repair; do not amend or add commits without authorization.
8. Stop when the approved intended-change set is exhausted, not when the whole tree is clean. Report remaining unrelated staged and unstaged changes without committing, discarding, or unstaging them.

## Git-specific gotchas

- Hooks can change the index after review; inspect status and the new staged diff before any retry.
- Never commit an unresolved merge: conflict markers can produce a syntactically valid but semantically partial result.
- During partial staging, working-tree content and index content differ; commands that read the file may test a version different from what will be committed. Verify the intended staged patch.
- Never stage repository-wide with `git add -A` when unrelated/untracked artifacts exist; they can enter the commit unnoticed.
- Never copy an old scope without checking current paths; monorepo moves make scopes misleading.
