---
name: session-handoff
description: "Create, validate, and resume project-session handoff documents in .claude/handoffs/ using bundled Python scaffolding, secret checks, and staleness reports. Use when the user asks to pause coding, save session state, transfer work to another agent, load a handoff, or resume a handoff chain. Suggest a handoff at major milestones or near context limits. Not for ordinary status emails, ADRs, commit messages, PR descriptions, or updates to persistent harness memory."
---

# Session Handoff

A handoff is a markdown file in `<project>/.claude/handoffs/` named `YYYY-MM-DD-HHMMSS-<slug>.md` that lets a fresh agent continue without rediscovering context. Commands below are written as `scripts/<name>.py` for short. Run them as `python3 "$SKILL_DIR/scripts/<name>.py"`, where `SKILL_DIR` is the directory this SKILL.md was loaded from, with the project root as the working directory; a bare relative `scripts/` path only resolves when cwd is the skill directory. Every script takes `--help` (exit codes, examples) and `--json` (one JSON result on stdout, errors on stderr).

## Choose the mode

| Situation | Action |
|-----------|--------|
| User wants to stop, switch tasks, hand over to another agent, or context is nearly full | CREATE |
| User wants to continue earlier work or names a handoff | RESUME |
| 5+ file edits, long debugging, or design decisions made, and no handoff asked for | Suggest once: "We've made significant progress. Say 'create handoff' when you want this context saved." |
| Small self-contained task (a one-line fix, a single question) | No handoff: the diff or commit is the record. Say so in one line. |

## CREATE

1. **Scaffold.** `python3 scripts/create_handoff.py implementing-user-auth`. When this work continues an earlier handoff, add `--continues-from 2026-01-15-143022-implementing-user-auth.md` (the exact filename in `.claude/handoffs/`). The script prints the new path; it never overwrites, so a same-second name gets a `-2` suffix.
2. **Fill.** Before writing, ask: "What would the next agent waste an hour rediscovering?" Write in this priority order:
   1. State that is not in the repository: what was verified, what was only assumed, what failed.
   2. Exact reproduction commands with the observed result and its date.
   3. Rejected hypotheses, each with the reason it was rejected.
   4. Decisions with the options rejected (the rationale, not just the outcome).
   5. A first next step concrete enough to run without asking.

   The validator requires three sections: Current State Summary, Important Context and Immediate Next Steps, each at least 50 characters with no `[TODO:` left. Delete optional scaffold sections that do not apply instead of leaving placeholders, except the six recommended headings (step 3): keep those with one line of content. A fact you do not know (was staging deployed? did CI pass?) is written as `Unknown` and asked of the user, never guessed. Read [references/handoff-template.md](references/handoff-template.md) only when unsure what an optional section should hold.

   **Depth:** under a day of remaining work by the same person: one short paragraph per required section. Multi-day work or a different agent: full evidence, with commands, outputs, `file:line` references and rejected hypotheses.

   Weak Important Context: "Tests are flaky, be careful." Strong: "`pytest tests/test_pool.py` fails about 1 run in 5 with `TimeoutError` only when `DB_POOL_SIZE` < 10 (seen 2026-11-03, 6 of 30 runs); raising the pool hides it, the real cause is the unclosed cursor in `src/db/pool.py:88`."

3. **Validate until READY.** `python3 scripts/validate_handoff.py <handoff-file>`, then act on the verdict and re-run after every fix:

   | Verdict (exit) | Meaning | Action |
   |----------------|---------|--------|
   | READY (0) | Score 70+, no TODOs, required sections complete, no secrets | Report (below) |
   | NEEDS_WORK (1) | TODOs left, a required section missing or under 50 characters, or score below 70 | Fill what the report lists, re-run |
   | BLOCKED (1) | A potential secret matched | Delete the value, keep only the variable name, re-run |
   | exit 2 | Wrong path or usage | Fix the command |

   The score starts at 100 and loses 30 for any TODO left, 10 per missing or incomplete required section, 20 for any secret, 5 per missing referenced file (max 20) and 2 per missing recommended section (Architecture Overview, Critical Files, Files Modified, Decisions Made, Assumptions Made, Potential Gotchas). So missing files and deleted recommended headings alone can reach NEEDS_WORK: 4 missing files plus all 6 headings deleted scores 68. Fix or delete each listed path, since the next agent will open them. Then report the path, final score, warnings left and first next step.

## RESUME

1. **List.** `python3 scripts/list_handoffs.py`
2. **Check staleness.** `python3 scripts/check_staleness.py <handoff-file>`. When the user already supplied this output, review it instead of re-running it.

   | Level (exit) | Action |
   |--------------|--------|
   | FRESH (0) | Resume |
   | SLIGHTLY_STALE (0) | Read the listed commits and changed files, then resume |
   | STALE (1) | Re-check every assumption and next step against the current code before acting |
   | VERY_STALE (2) | Tell the user; re-explore, then offer a fresh handoff |
   | UNKNOWN (2) | Commit and file counts mean nothing here; recover by cause (below), and resume only after the applicable checks pass |

   UNKNOWN by cause (the report's Issues line says which):
   - **Baseline recorded, git repo, baseline not an ancestor of HEAD** (rebase, reset, force-push): `git cat-file -e '<baseline>^{commit}'` checks the commit exists; if it does, `git diff --stat '<baseline>' HEAD` compares its tree with HEAD. If it is gone, find the old tip with `git reflog`. Then treat the handoff as STALE.
   - **No baseline in the handoff**: ask the user for a trustworthy baseline commit, or verify the relevant files and assumptions by hand; never claim a baseline comparison you did not run.
   - **Not a git repo**: skip git commands; verify the cited files, environment state, blockers and next steps directly.

3. **Load.** Read the handoff completely, then the predecessor named under Handoff Chain. Read at most the latest plus two predecessors; summarise older links from the oldest one you read instead of walking an unbounded chain.
4. **Verify before editing.** First ask: which line of this handoff, if false now, would make Immediate Next Steps item 1 harmful? Verify that line first. Then check the branch (`git branch --show-current`), the working tree (`git status`), and each assumption and blocker the handoff lists. When the level is not FRESH or a referenced file is missing, also work through [references/resume-checklist.md](references/resume-checklist.md) (environment checks, red flags). Do not load handoff-template.md to resume.
5. **Begin** with Immediate Next Steps item 1.
6. **Update or chain.** After editing a handoff, re-run `validate_handoff.py` until READY. For a new session, create a new handoff with `--continues-from` instead of rewriting the old one: the old file is the evidence the chain points to.

## Gotchas

Creating:
- NEVER write a secret value into a handoff or repeat one in your reply: handoffs get committed and pasted into other sessions. Replace each secret with a variable name, e.g. `$DATABASE_URL`, and say where the real value lives ("set in the shell from the team vault"). The scanner only matches quoted assignments (`api_key = "..."`), any `scheme://user:password@` URL (placeholders like `<password>` or `$DB_PASSWORD` are ignored), 20+ character `Bearer` values and known prefixes (`ghp_`, `sk-`, `xox`, PEM headers). Unquoted assignments pass as clean, so check them by hand: `export API_KEY=abcd1234efgh5678`, `DATABASE_PASSWORD=hunter2hunter2`.
- NEVER run `create_handoff.py` from a subdirectory: it writes to `<cwd>/.claude/handoffs/`, so the handoff lands where `list_handoffs.py` run from the root will not find it.
- The scaffold's Files Modified table lists at most ten tracked (staged or unstaged) files and no untracked ones. Add relevant new files from `git status` by hand, or the next agent will not know they exist.
- `--continues-from` takes the exact filename, not a path or a partial name. Anything else exits 2 and writes nothing.

Resuming:
- FRESH only compares age, commit count, changed files and branch. It cannot see a staging deploy, a database migration, an environment variable or a ticket status, so re-check blockers and assumptions even when FRESH.
- `check_staleness.py` inspects the directory in the handoff's `Project:` line when it exists. A handoff copied from another checkout or worktree is then compared with that checkout, not yours: confirm `Project:` equals `git rev-parse --show-toplevel` first.
- `list_handoffs.py` marks a handoff Complete when it has no `[TODO:` markers; that is not validation. Run `validate_handoff.py` on the one you load when its quality matters.
- Referenced files resolve against the project root and the handoff's directory only. A path written relative to a subdirectory reports as missing although it exists.
