# Commit Work

A skill for staging and committing Git changes so each commit holds only the approved change. It leaves content the user already staged alone, splits mixed files without an interactive terminal, verifies the staged version rather than the working tree, and writes Conventional Commits messages with no attribution trailers. `SKILL.md` holds the intent routing, the workflow and the gotchas; nothing here repeats them.

## When it triggers

Requests to commit work, stage selected files or hunks, split a mixed tree into commits, review what is staged, or draft a commit message. It is not for rebasing, squashing, amending or force-pushing history, resolving merge conflicts, opening pull requests, or code review unrelated to a commit.

## Installation

**Claude Code:**

```bash
cp -r skills/commit-work ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

## File structure

```
commit-work/
├── SKILL.md                                 # Intent routing, workflow, gotchas
├── README.md                                # This file
├── references/commit-message-template.md    # Repository message rules, commitlint defaults, spec edge cases
└── evals/                                   # Output evals, fixtures in evals/files/, trigger queries
```

## Resources

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [`@commitlint/config-conventional`](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)
