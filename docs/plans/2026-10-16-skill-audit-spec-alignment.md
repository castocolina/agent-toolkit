# Plan: Spec-Aligned skill-judge Refactor + Full Skills Audit (Grade A/B)

**Date:** 2026-10-16
**Status:** In execution
**Driver:** pi agent (GLM 5.3) + subagent judges (GPT-6.1-sol, GLM 5.3 Flash)

## Goal

Refactor `skills/skill-judge` so its rubric incorporates the official Agent Skills
specification docs (agentskills.io), then audit **all 43 skills** in this repo with
**parallel subagent judges**, merge their criteria, and fix every skill until it earns
**Grade A (≥90%) or Grade B (≥80%)** under the unified rubric. Also refresh the README
install section with current, non-interactive install methods for Claude Code, Cursor,
opencode, and pi.

## Context

- Fork `castocolina/agent-toolkit` is ahead of `softaworks/agent-toolkit` by 2 commits
  (`dbff837`, `18ca982`). Upstream PR #48 is open but unreviewed; the work is already
  merged into our fork's `main`, so no merge action is needed.
- Old `skill-judge` (752 lines) scores 8 dimensions / 120 points but ignores the
  official spec docs: best practices, evaluating skills, optimizing descriptions,
  using scripts, and the format specification.
- Five skills exceed the 500-line SKILL.md limit (qa-test-planner 757,
  database-schema-designer 687, design-system-starter 603, mui 504,
  dependency-updater 491).
- User requirements:
  1. Evaluator (skill-judge) must READ the spec sections, not just summarize them.
  2. Judging runs as subagents in parallel + GPT-6.1-sol evaluating independently.
  3. Criteria from all judges are MERGED before any fix.
  4. Fixes are executed by GLM 5.3 Flash subagents.
  5. Final: every skill ≥ Grade B (ideally A).

## Recent Work

- `dbff837` docs(skills): tighten draw.io and mermaid authoring rules
- `18ca982` fix(draw-io): drop python3 from PNG export

## Phases

### Phase 1 — Refactor skill-judge (spec alignment)

- [P] Save the five official spec pages into `skills/skill-judge/references/`
      (`spec.md`, `best-practices.md`, `evaluating-skills.md`,
      `optimizing-descriptions.md`, `using-scripts.md`), trimmed to essentials.
- [P] Rewrite `skills/skill-judge/SKILL.md` (< 500 lines) with the unified rubric
      (150 points, 8 dimensions), MANDATORY reference-reading steps in the protocol,
      and JSON output contract for machine-mergeable verdicts.
- [V] skill-judge itself complies: < 500 lines, valid frontmatter, name matches dir,
      references load conditionally, self-evaluation ≥ Grade A.

### Phase 2 — README install section (current, non-interactive)

- [P] Replace outdated interactive `/plugin` instructions with direct commands:
      skills CLI (`npx skills add … -a <agent> -g -y`), Claude Code 2.1 CLI
      (`claude plugin marketplace add` + `claude plugin install … -y`), Cursor
      (`~/.cursor/skills/`, `.cursor/skills/`), opencode v2 (`.opencode/skills/`,
      `~/.config/opencode/skills/`, `~/.agents/skills/`), pi (`~/.agents/skills/`,
      `.agents/skills/`), and universal git-clone into `~/.agents/skills/`.
- [V] Every command runs headless (no TTY prompt), paths verified against current
      harness docs (opencode v2 docs, pi docs/skills.md, claude plugin --help).

### Phase 3 — Parallel audit (subagents)

- [P] Build judge prompt from refactored skill-judge + batch assignments.
- [P] Spawn judges in parallel:
      - Judge A: pi subagent (default model) — batches 1–5 of ~9 skills.
      - Judge B: `pi -p --provider openai --model gpt-6.1-sol` — same batches,
        independent spec-based rubric view.
      Each outputs `docs/audit/judgements/<judge>/<skill>.json` (scores per dimension,
      evidence, top fixes).
- [P] Merge criteria into `docs/audit/2026-10-16-audit-report.md`: per-skill averaged
      scores, deltas between judges, unified fix list, target grades.
- [V] All 43 skills have 2 independent verdicts; merged report lists every skill with
      current grade and concrete fix items.

### Phase 4 — Fixes via GLM 5.3 Flash

- [P] Spawn `pi -p --provider zai-coding-cn --model glm-5.3-flash` subagents (batches)
      applying ONLY the merged fix list per skill (description rewrites, split >500-line
      bodies into references/, add gotchas/defaults, script hardening, evals/ stubs).
- [P] Guardrails: keep `name` matching directory, description ≤1024 chars, README.md
      untouched, no skill deletion.
- [V] `git diff` review per skill; frontmatter lint; line counts < 500.

### Phase 5 — Re-audit & confirm grades

- [P] Re-run both judges on fixed skills.
- [P] Any skill < B (120/150) gets another GLM 5.3 Flash fix round (max 2 extra rounds).
- [V] Final report: every skill ≥ 120/150 (B), target ≥ 135/150 (A).

### Phase 6 — Commit

- [P] Logical commits: skill-judge refactor; README install docs; audit artifacts;
      per-category skill fixes; final report.
- [V] Clean `git status`; conventional commit messages.

## Key Constraints

- **Never** delete a skill or its README.md (repo marketplace convention).
- **Never** let fixes contradict the official spec pages in `references/`.
- Judge outputs MUST be JSON so criteria merge is mechanical, not vibes.
- Fixes go ONLY to `skills/` in the repo (installed copies sync later).
