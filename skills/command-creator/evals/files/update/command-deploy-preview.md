Contents of .claude/commands/deploy-preview.md in the user's repository:

---
description: Build the current branch and deploy it to a preview environment
argument-hint: <branch>
arguments: branch
disable-model-invocation: true
allowed-tools: Bash(npm run build)
---

1. If `$branch` is empty, stop and ask for a branch.
2. Check that `git rev-parse --abbrev-ref HEAD` prints the branch; otherwise stop.
3. Run `npm run build`; stop on failure.
4. Run `npm run deploy:preview` and report the preview URL it prints.
