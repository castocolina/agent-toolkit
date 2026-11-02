---
description: Draft user-facing release notes from the git history between two refs (default last version tag to HEAD) and print them as Markdown. Use when preparing a release, before tagging a version, or when asked for "release notes", "what changed since v1.4", or "write the changelog entry". Reads git history only, never edits files, tags or pushes. Not for describing a single pull request (use explain-pr-changes).
argument-hint: "[from-ref] [to-ref]"
allowed-tools: Bash(git log:*), Bash(git describe:*), Bash(git rev-parse:*), Bash(git show:*)
---

Draft release notes for the range `$0..$1` (defaults: the last version tag, and `HEAD`). The command is read-only: print the notes, write nothing.

Copy this checklist and tick each step off:

- [ ] 1. Resolve the range
- [ ] 2. Collect the commits
- [ ] 3. Drop noise
- [ ] 4. Group
- [ ] 5. Write the notes

## 1. Resolve the range

1. If `$0` is given, it is the start and `$1` defaults to `HEAD`. Validate each ref with `git rev-parse --verify <ref>^{commit}`; if one fails, stop and name it. Skip to step 2.
2. Otherwise find the newest stable tag reachable from `HEAD`:
   `git describe --tags --abbrev=0 --match 'v[0-9]*' HEAD`, then accept it only if it matches `^v[0-9]+\.[0-9]+\.[0-9]+$`. If it is a pre-release such as `v1.4.0-rc1`, rerun from `<tag>^` until a stable tag appears. `--tags` is required, or lightweight tags are invisible.
3. If the tag resolves to the same commit as `HEAD`, rerun from `HEAD^` and use the older tag as the start.
4. If `git describe` prints `No names found` or `No tags can describe`:
   - `git rev-parse --is-shallow-repository` prints `true`: stop and ask for a start ref that is available locally. Do not fetch; this command is read-only.
   - Otherwise this is the first release: the log command in step 2 runs as `git log --first-parent --format='%h%x09%s' <to>` (no `<from>..`) and the header says "First release".

## 2. Collect the commits

```bash
git log --first-parent --format='%h%x09%s%x09%b' <from>..<to>
```

If the log prints nothing, stop with `No commits in <from>..<to>.`

A generic merge subject (`Merge pull request #N from ...`) carries the PR title on the first non-empty body line: use that as the subject.

`--first-parent` yields one line per merged PR in both merge-commit and squash workflows; `--no-merges` lists every feature-branch commit.

Breaking-change footers live in the body, so list them once:

```bash
git log --first-parent --grep='^BREAKING[ -]CHANGE' --format='%h' <from>..<to>
```

## 3. Drop noise

- A `Revert "X"` commit and the commit it reverts, when both are in the range: they cancel. If only the revert is in range, keep it as a fix line.
- `Merge branch 'main' into ...` and `Merge remote-tracking branch ...`.
- Bot bumps (`chore(deps)`, `Bump x from a to b`) unless the subject mentions a CVE or "security". Those stay and go under Fixes.
- If nothing is left, print `No user-facing changes since <from>.` and stop.

## 4. Group

Sections, in this order, omitting empty ones:

1. Breaking changes: a `!` before the colon in the subject (`feat(api)!:`) or a sha from the footer list.
2. Features: `feat`.
3. Fixes: `fix`, `perf`, and the security bumps.
4. Internal: `docs`, `ci`, `test`, `refactor`, `chore`, collapsed into one line with a count.

A subject without a conventional prefix goes under Internal. Do not guess its type from its wording.

## 5. Write the notes

Rewrite each subject for the person who upgrades: what changed for them, not the internal wording. One line per PR, at most 100 characters. When several commits carry the same `(#123)`, merge them into one line. Keep the PR number as it appears in the subject; do not build links, because the remote host is unknown.

The header names `<to>` when `$1` was given, and says `Unreleased` otherwise (`<to>` is then `HEAD`). In a first release, the range reads `First release` in place of `<from>..<to>`.

Output format (Markdown, nothing before or after it):

```markdown
## <to-ref or "Unreleased"> (<from>..<to>)

### Breaking changes
- Removed the `--legacy` flag; use `--compat` instead (#212)

### Features
- Added CSV export to the report page (#230)

### Fixes
- Fixed a crash when the config file is empty (#241)

### Internal
- 7 internal changes (docs, ci, refactor)
```

## NEVER

- NEVER run `git tag`, `git push` or edit `CHANGELOG.md`. The user reviews the notes before anything is published, and a tag that CI has already consumed is hard to retract.
- NEVER mark a change as breaking because its wording says "remove" or "rename". Only the `!` marker and the footer count; a guessed label makes users plan a major upgrade for nothing.
- NEVER combine `--no-merges` with `--first-parent`. It silently drops every merged PR in a merge-commit workflow.
- NEVER describe a benefit the subject does not state. When a subject is too thin to say what changed for the user, put it under Internal.

## Gotchas

- A shallow CI checkout has no tags at all. The failure looks like a first release, so check `--is-shallow-repository` before concluding that.
- Tags created on a release branch are not reachable from `main`. If `git describe` returns a version older than expected, ask the user for `$0` instead of guessing.
