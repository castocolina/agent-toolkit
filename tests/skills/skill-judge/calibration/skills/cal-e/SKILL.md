---
name: cal-e
description: Draft user-facing release notes from the merged pull requests of a release range, grouped by what changes for users, with breaking changes called out and every entry traced to its PR number. Use when asked to "write release notes", "draft the changelog for this release", "what shipped since the last tag", or to turn a list of merged PRs or commits into notes, even when the user only gives a tag range or pastes a PR list. Returns the notes plus a list of PRs it could not classify; it does not tag, publish or edit releases. Not for commit-message style checks, API reference docs, or marketing announcements.
---

# Release Notes Drafter

Readers of release notes ask one question: what do I have to do, or what can I now do? Write for them, not for the people who merged. Never edit a release or a tag: this skill drafts text and the user publishes it.

## Workflow

1. **Fix the range.** Ask for two tags or two dates when they are missing. Never assume "the last release" is the newest tag: pre-release and backport tags make that wrong. Get the merged PRs of the range with the `gh` CLI or read the list the user pasted.
2. **Cancel reverts.** A PR and its own revert inside the range both vanish from the notes. A revert of a PR that shipped in an earlier release is a Fixed entry.
3. **Classify each PR by user impact, first match wins:** Breaking (users must act), Added, Changed, Fixed, Internal (left out). Squash-merge titles describe the code ("refactor retry loop"), not the effect, so read the PR body and labels first. When title and body disagree, trust the body.
4. **Write breaking entries last, and with care.** Each states who is affected, what to do instead, and a before and after line. When the PR has no migration text, put it under "Could not classify" instead of guessing.
5. **One line per entry,** in the user's vocabulary, ending with the PR number. Several PRs that ship one feature in parts become one entry that lists every number. Credit contributors by handle only when the project's earlier notes do.
6. **Check for edge cases** (below) before you call the draft done.
7. **Long ranges.** When the PR list is longer than you can finish, save the unclassified PR numbers to a handoff file in the user's project (`.claude/handoffs/`) and say so. Never present a partial list as complete.

## Edge cases

- A PR behind a feature flag that is off by default is Internal until the flag flips; mention the flag in the entry that turns it on.
- A docs-only PR is Internal unless the docs describe behavior users could not discover otherwise.
- A PR merged to a release branch and to the main branch appears twice in a range: dedupe by PR number.
- Bot-authored dependency PRs are Internal by default.

## NEVER

- Never copy commit subjects verbatim: they are written for reviewers and say "fix" without saying what broke.
- Never put a dependency bump under Fixed unless the PR body names a user-visible bug; bumps pile up as noise and readers stop reading the section.
- Never drop a breaking change because it is small: a one-line rename breaks as many users as a large rewrite.
- Never invent a migration step: users follow it, and a wrong step is worse than a blank one.

## Output

Markdown with one heading per category in the order Breaking, Added, Changed, Fixed (empty categories omitted), then "Could not classify" with each PR number and the reason.

## Gotchas

- If the skill reports that a file it needs is missing, it was installed without its folder: copy the whole directory to `~/.claude/skills/cal-e/`.
- Labels such as `bug` are set by authors and are wrong often enough that they only break ties, never decide a category.
