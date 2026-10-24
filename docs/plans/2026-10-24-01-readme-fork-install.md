# Plan 1 — README Installs From This Fork

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Users install every skill, agent and command from `castocolina/agent-toolkit` with copy-pasteable, non-interactive commands for each supported harness.

**Architecture:** Documentation and marketplace metadata only. The marketplace keeps its name `agent-toolkit`, so `<plugin>@agent-toolkit` identifiers stay valid; only the owner and the repo references change.

**Tech Stack:** Markdown, `.claude-plugin/marketplace.json`, `scripts/build_plugins.py`.

**Spec:** [Roadmap](2026-10-24-00-roadmap.md) — Decisions 10, 15; Global Constraints apply.

Branch: `docs/<yy-mm-dd>-fork-install`. Depends on nothing.

## Review Focus

1. A user who already added `softaworks/agent-toolkit` as `agent-toolkit` adds this fork → the README tells them to remove the old marketplace first, because both have the same name. Pinned in Step 3.
2. A harness whose install path cannot be verified today → it is left out instead of guessed. Pinned in Step 2.
3. A copy-pasted command needs a TTY → not allowed; every command runs headless. Pinned in Step 5.

---

### Task 1: Marketplace owner and per-harness install commands

**Files:**
- Modify: `README.md` (install section, lines ~18-90; agents/commands note, lines ~145-152)
- Modify: `.claude-plugin/marketplace.json` (`owner`)
- Modify: `CONTRIBUTING.md` (repo references)

- [ ] **Step 1: Change the marketplace owner.** In `.claude-plugin/marketplace.json` set `owner` to `{"name":"castocolina","url":"https://github.com/castocolina"}`; leave `name: agent-toolkit` unchanged.
- [ ] **Step 2: Verify each harness command before writing it.** For each target, run its `--help` (or read its current official docs) and record the exact command in a scratch note; drop any harness whose path cannot be verified. Targets: skills CLI (`npx skills add castocolina/agent-toolkit …` with its non-interactive flags), Claude Code (`claude plugin marketplace add castocolina/agent-toolkit`, `claude plugin install <plugin>@agent-toolkit`, `claude plugin marketplace update agent-toolkit`), Codex, Cursor, opencode, pi, GitHub Copilot CLI, and a universal `git clone` into `~/.agents/skills/`.
- [ ] **Step 3: Rewrite the README install section** with one subsection per verified harness. Include "Switching from upstream: `claude plugin marketplace remove agent-toolkit`, then add this fork". Keep interactive `/plugin` only as a one-line "interactive alternative" note. Replace "Ask the agent: install from github.com/softaworks/agent-toolkit" with this fork. Add the attribution line "Fork of softaworks/agent-toolkit by @leonardocouy".
- [ ] **Step 4: Update `CONTRIBUTING.md`** so its clone/PR references point to `castocolina/agent-toolkit`.
- [ ] **Step 5: Verify**

  Run: `rg -c 'softaworks/agent-toolkit' README.md`
  Expected: `1` (the attribution).
  Run each Claude Code command from Step 3 in a scratch `HOME` (`HOME=$(mktemp -d) claude plugin marketplace add castocolina/agent-toolkit`, then one `claude plugin install humanizer@agent-toolkit`).
  Expected: both exit 0 without prompting; the installed plugin's source is the fork.
- [ ] **Step 6: Commit**

  Run `python3 scripts/build_plugins.py`, stage `dist/`, `.claude-plugin/marketplace.json`, `README.md`, `CONTRIBUTING.md`, then `git commit -m "docs(readme): install from castocolina fork with non-interactive commands"`. Open the PR with `/explain-pr-changes`.
