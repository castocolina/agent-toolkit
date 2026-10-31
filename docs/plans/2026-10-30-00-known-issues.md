# Known issues after plans 1-4 (2026-10-30)

Single source of truth for what is still wrong after the skill audit (PR #7) and the diagram work (#6, #9). Plans 6-9 in this directory fix these. Each item names its evidence so an executor can re-verify it before acting.

State when written: plans 1, 2, 3 and the alias follow-up are merged to `main`; plan 4 (PR #7, `feat/26-10-28-skill-audit-fixes`) is open and clean against `main` but has no CI run (a retarget to `main` does not trigger `pull_request`); plan 5 (PR #8, scheduled audit) is open and still being implemented.

## 1. Skills below the quality bar (plan 4 residuals)

Evidence: `docs/audit/2026-10-28/remaining-findings.md` on branch `feat/26-10-28-skill-audit-fixes` (359 findings: 26 high, 170 medium, 163 low). All 43 audited skills score 80.8 or higher; mean 88.7; A=14, B=29. The 90 percent target is not met for 29 skills.

High findings per skill (26 in 16 skills): plugin-forge 3, mermaid-diagrams 3, database-schema-designer 3, react-dev 2, mui 2, marp-slide 2, draw-io 2, and one each in session-handoff, qa-test-planner, jira, humanizer, feedback-mastery, design-system-starter, commit-work, command-creator, c4-architecture.

## 2. Four eval suites under 90 percent

| Suite | Result | Cause |
|---|---|---|
| excalidraw | 8/9 | Judge D7: no scene fixture, so the modify path never runs; one assertion needs an explicit label-only request to a delegate. |
| reducing-entropy | 6/8 | Judge D7: no code fixture; assertions need a loaded reference and a measured size, which a tool-less runner cannot produce. Positives name the skill literally. |
| marp-slide | 8/9 | Judge D7: no existing-deck fixture; one assertion needs the bundled template read. |
| mui | 8/9 | Judge D7: no fixture component; one assertion needs `slots`/`slotProps` in a migration answer. |

The judges flagged all four as D7 findings (missing fixtures). They were not fixed because plan 4 stopped after one high-only wave. The harness supports fixtures (`evals/files/`, injected by `file_blocks`); none of the four skills has that directory. The runner has no tools by design.

## 3. mui does not meet the UI/UX rules

The eight rules are in `skills/ui-ux-principles` (plan 6). State of `mui` as shipped in PR #7 (909 lines in total across `SKILL.md`, whose body is about 30 lines, and its resources; `main` has the older 1926-line version):

| Rule | main | PR #7 |
|---|---|---|
| Skeleton loading states | mentioned, not preferred | `Skeleton` removed |
| Responsive (mobile, tablet, desktop) | Grid only | `Grid size` only, no mobile-first guidance |
| Visual hierarchy, primary action | absent | absent |
| Design tokens | covered | covered |
| Component consistency and dark mode | covered, buggy example | nested-theme example is high finding |
| Accessibility | no `aria-` anywhere | one TextField case; theme toggle lacks `aria-label` (high finding) |
| Empty, error, success states | absent | absent |
| Interaction states (hover, focus, active, disabled) | hover and disabled only | same; no `focus-visible` |

Cause: the plan 4 rewrite targeted judge D1 (knowledge delta) and the judge rubric has no UX rules, so a skill can score 83 percent and fail all of them. `design-system-starter` overlaps on tokens, consistency and states.

## 4. Mermaid rules not wired into the PR command

`skills/mermaid-diagrams/references/authoring-rules.md` defines `flowchart TD`, an aspect ratio of at least 0.4, subgraph grouping and `classDef` with explicit `fill`, `stroke`, `color`. `commands/explain-pr-changes.md` reads the draw.io rules for drawio mode but never points to the Mermaid rules, so PR #7's body diagram is a single `flowchart LR` row of 8 nodes with no palette (screenshots in the 2026-10-30 session: light and dark GitHub themes).

A fix is prepared and uncommitted in worktree `.claude/worktrees/07-mermaid-rules` on branch `fix/26-10-30-mermaid-authoring-rules` (command step plus eval `mermaid-rules-paths`; targeted run 17/17, full 77-scenario gate not run). Ruling from the user: the generation rules belong to `mermaid-diagrams` and `draw-io`; the command stays source-agnostic (a pointer plus minimal fallback only). Those two skills have 3 output evals each and none checks layout. The agent `agents/mermaid-diagram-specialist.md` (616 lines) overlaps `mermaid-diagrams`.

## 5. Third-party sources

Registry: `docs/audit/upstream-sources.{json,md}` (10 rows). It holds `skill`, `source`, `ref`, `kind` only; no review dates. Plan 6 extends it (optional review fields; a `local` row kind for artifacts with no upstream) instead of adding a second file, which means relaxing plan 4's strict `validate_entry`. Staleness is derived from commit dates. Checked on 2026-10-30:

- `crafting-effective-readmes`: the commits-by-path API said "No commit found" because upstream moved its directories; the tree at `main` is fetchable. Only change worth noting: upstream style guide now points to a skill named `writing`. Nothing to port.
- `reducing-entropy`: upstream content unchanged since February; moved directories only. Ignore.
- `writing-clearly-and-concisely`: upstream consolidated into `writing` (Orwell doctrine plus `ai-writing-tropes`). **Open decision**: port Orwell material or keep.
- `obra/the-elements-of-style`: ignore. `humanizer`, `react-useeffect`, repo seed `softaworks/agent-toolkit`: current.
- Not content-checkable: agent-md-refactor (post), domain-name-brainstormer (newsletter).
- `gepetto`, `datadog-cli`: synced by workflow, never edited.

Gaps: no path-moved detection, no review dates, no check that a skill's own rules still hold for current models (example: the humanizer's dash-character rules, which current Anthropic models no longer trigger).

## 6. Artifacts nobody audited

`scripts/audit/audit.py` only walks `skills/`. Unjudged: 7 commands (`codex-plan`, `compose-email`, `explain-changes-mental-model`, `explain-pr-changes` (evals only), `sync-branch`, `sync-skills-readme`, `viral-tweet`) and 6 agents (`ascii-ui-mockup-generator`, `codebase-pattern-finder`, `communication-excellence-coach`, `general-purpose`, `mermaid-diagram-specialist` 616 lines, `ui-ux-designer` 478 lines). Several agents read like long skills; whether each should stay an agent, become a skill or be deleted is undecided. No judge profile exists for commands or agents.

## 7. Process and CI

- PR #7 has no CI run; push an empty commit or close and reopen it to trigger `main.yaml` (not done, user has not answered).
- Plan 5's scheduled audit covers skills only. Target flow (user, 2026-10-30): part 1 refreshes the judge from agentskills.io through `agentskills-research`; part 2 reviews every skill, command and agent through the new `skill-updater`. Plan 9 updates CI to this flow after plan 5 Phase 2.
- Plan 5 Phase 1 review findings (U1) queued: truth-table tests for `checkpoint`/`state` never stamping on failure, open-PR gate assertion, `--days` required, live-state read folded into the `interval` step.
- Plan 5 Phase 2 is blocked on the CI spike (10 open issues) and user inputs: jev provider and key, Copilot token, bot token.
- Main checkout hygiene: tooling edits (`graphify-out`, `.codegraph`, merge driver) now live in `.git/info/{exclude,attributes}`; the old local `main` is kept as `backup/main-pre-sync-2026-10-30`.

## 8. Decisions still open for the user

Accept or fix the 26 high findings and 4 suites; port the Orwell material or not; where each agent ends up (agent, skill, delete); whether to trigger CI on #7; jev provider and key; Copilot token.
