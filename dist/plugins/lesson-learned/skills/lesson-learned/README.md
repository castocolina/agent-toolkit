# Lesson Learned

Extract software engineering takeaways from your recent code changes.

## Purpose

Most developers ship code and move on. But the fastest way to grow is to pause and reflect: what principle did I just apply? What trade-off did I make? What would I do differently?

This skill analyzes recent git history and surfaces the engineering lesson embedded in the work you just did.

## When to Use

- After finishing a feature or PR
- After a debugging session
- After a refactor
- When you want to reflect on recent work
- Trigger phrases: "what is the lesson here?", "what can I learn from this?", "engineering takeaway"

## How It Works

1. **Determine scope** -- Feature branch against its base branch, the last N commits (default 5), a specific SHA, or working changes including untracked files.
2. **Gather and verify** -- Reads the scoped log and diff, then checks each candidate lesson against code and tests rather than commit messages.
3. **Present the lesson** -- One lesson (at most three), with what changed, why it matters, and a next-time practice. A principle name is used only when the evidence supports it.

## Output Format

```markdown
## Lesson: Separation of Concerns

**What changed:** `src/auth/handler.ts` now calls `validateToken()` from the new
`src/auth/token.ts`, which imports nothing from the handler.
**Why it matters:** The new `token.test.ts` covers expiry without an HTTP request;
before the split, that check could only be tested through the handler.
**Next time:** Move a rule into its own module when it needs its own tests.
```

## Prerequisites

- A git repository with commits or uncommitted changes

## Related Files

- `references/se-principles.md` -- Diff signals mapped to candidate lessons, with the evidence each needs
- `references/anti-patterns.md` -- Anti-pattern signals and their false positives

## Credits

Based on the original skill in [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/main/skills/lesson-learned) (PR #11) by Matt White, via softaworks/agent-toolkit; this version is rewritten.

The git commands and behaviors in `SKILL.md` follow the documentation of the Git project ([git-log](https://git-scm.com/docs/git-log), [git-diff](https://git-scm.com/docs/git-diff), [git-show](https://git-scm.com/docs/git-show), [git-status](https://git-scm.com/docs/git-status), [git-symbolic-ref](https://git-scm.com/docs/git-symbolic-ref), [git-rev-parse](https://git-scm.com/docs/git-rev-parse)), checked 2026-11-07.
