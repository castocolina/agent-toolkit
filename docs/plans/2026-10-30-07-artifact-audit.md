# Plan 7 — Audit Every Command, Agent and New Skill

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Judge every artifact the plan 4 audit did not cover (7 commands, 6 agents, the two new skills from plan 6) with two independent judges and produce a disposition for each: keep, fix, convert to a skill, or delete.

**Architecture:** `audit.py` learns to enumerate commands and agents; the existing judge, merge and report flow runs with the `--kind` profiles from plan 6; a triage table turns findings into the task list that plan 8 executes.

**Tech Stack:** `scripts/audit/audit.py`, pi lanes `my-referee-one` and `my-referee-two` (parallel; `my-referee-three` only as fallback), Python unittest.

**Spec:** [Known issues](2026-10-30-00-known-issues.md) section 6; [Plan 6](2026-10-30-06-new-skills.md) Task 4 profiles; Roadmap Global Constraints apply.

Branch: `feat/<yy-mm-dd>-artifact-audit`. Depends on plan 6 merged.

## Global Constraints

- Same lanes, language, attribution, `dist/` and protected-skill rules as plan 6.
- The audit changes no artifact; findings go to `docs/audit/<date>/` and `docs/audit/upstream-sources.json` (written only through `audit.py track`). Fixes are plan 8.
- Judges run read-only (`--tools read,grep,find,ls`); `my-coding` is never a judge.
- Verdict files are committed as soon as they are written (a plan 4 incident lost untracked verdicts).

## Review Focus

1. A command or agent is judged like a skill and fails on irrelevant dimensions → the profiles from plan 6 are used and the report states the profile. Pinned in Task 2.
2. An agent that is really a skill is graded as an agent and passes → Task 3 asks "would this load on demand and be reused across hosts" for each agent and records the answer.
3. The two lanes disagree by more than 10 points on an artifact (the threshold `merge` already flags in its `disagreement` field) → a third lane reads it and `merge` averages all verdicts it finds; the report names the disagreement so a human can look. Pinned in Task 2.
4. `explain-pr-changes` already has a full eval suite → it is judged for content but its eval suite is not rerun here.
5. Lane outage mid-run → completed verdicts are kept and only the missing lane reruns. Pinned in Task 2.

---

### Task 1: Enumerate artifacts in `audit.py`

**Files:**
- Modify: `scripts/audit/audit.py`, `tests/audit/test_audit.py`
- Test: `tests/audit/test_audit.py` (new class `ArtifactListTests`)

**Interfaces:**
- Consumes: repository layout `skills/<name>/`, `commands/<name>.md`, `agents/<name>.md`.
- Produces: `list_artifacts(root: Path) -> list[dict]` returning `{"kind": "skill"|"command"|"agent", "name": str, "path": str}` sorted by kind then name; subcommand `audit.py artifacts [--kind K]` prints it as JSON; `commands/evals/` and any non-`.md` file are excluded; a name under two kinds exits 2 (verdict files are keyed by name).

- [ ] **Step 1: Write failing tests** in a scratch tree: one skill, two commands plus a `commands/evals/x.json`, one agent → the list holds exactly those four, sorted; `--kind agent` filters; a stray `commands/notes.txt` is ignored; a missing `agents/` directory yields no agents and no error; a skill and a command both named `x` make `artifacts` exit 2.
- [ ] **Step 2: Run** `python3 -m unittest tests.audit.test_audit.ArtifactListTests -v` → FAIL.
- [ ] **Step 3: Implement** `list_artifacts` and the `artifacts` subcommand; keep `check` skills-only unless `--kind` is given.
- [ ] **Step 4: Add `check --kind skill|command|agent`** (default `skill`; `--skills` then names artifacts of that kind; output keeps the `{"skills": [{name, ok, synced, issues}]}` shape): a command needs a non-empty `description` in frontmatter; an agent needs `name` equal to the file stem and a non-empty `description`; field lists come from `docs/audit/artifact-specs.md` (plan 6, Task 4). Tests: valid and invalid fixtures for each.
- [ ] **Step 5: Run** the full `tests/audit` suite → PASS. Commit `feat(audit): enumerate and validate commands and agents`.

### Task 2: Judge with two lanes

**Files:**
- Create: `docs/audit/<date>/judgements/<lane>/<artifact>.json` (one per artifact and lane), `docs/audit/<date>/{merged.json,report.md}`

**Interfaces:**
- Consumes: `audit.py artifacts`, the judge-prompt builder with `--kind`, `audit.py validate-verdict`, `audit.py merge`.
- Produces: merged verdicts per artifact with grade, per-dimension scores and findings; `report.md` lists score, grade and high findings per artifact and the lane-disagreement list (gap above 10).

- [ ] **Step 1: Build the list** `python3 scripts/audit/audit.py artifacts > $OUT/artifacts.json`; assert per-kind counts with `jq`: 7 commands, 6 agents, and every skill directory (45 existing plus `ui-ux-principles` and `skill-updater`, so 47). Judge the 13 commands and agents plus the two new skills; the 45 existing skills are out of scope.
- [ ] **Step 2: Dispatch** one read-only pi call per artifact and lane, with the command taken from `python3 scripts/audit/audit.py pi-cmd judge --model router-env/my-referee-<n>` (never hard-coded) and the prompt from `audit.py judge-prompt --kind <kind> --artifact <path> --judge <slug>` (plan 6 Task 4); verdict files go to `docs/audit/<date>/judgements/<audit.py slug of the lane>/<artifact>.json`, because `validate-verdict` requires `judge` to equal the parent directory name, at most four calls in flight per lane; lane one and two in parallel; a failing lane (404 or 429) falls back to `my-referee-three` for that artifact only.
- [ ] **Step 3: Validate** every verdict with `audit.py validate-verdict`; an invalid one is rerun once, then reported as a harness failure.
- [ ] **Step 4: Commit the verdicts immediately** (`docs(audit): judge commands, agents and new skills`) before merging.
- [ ] **Step 5: Merge** with `python3 scripts/audit/audit.py merge --in docs/audit/<date>/judgements --out docs/audit/<date> --skills <the 15 judged names> --judges <the `audit.py slug` of lanes one, two and three, all three every time> --min-judges 2` (without `--skills` it enumerates only `skills/`; with it, `merge` and `validate-verdict` accept command and agent names unchanged, pinned by plan 6 Task 4 Step 2; no `--check`). `merge` reads `<in>/<slug>/<name>.json` for each listed slug, so with all three listed any two present files complete an artifact, whichever lanes wrote them. Exit 0 is expected; exit 2 means some artifact has fewer than two valid verdicts: rerun only its missing lane (Review Focus 5) and merge again. Ruling: no fixture dry run, because plan 5's `MergeTests` already pin this counting and the real command's exit code reports any short artifact. `merge` writes `report.md` itself; its `disagreement` field in `merged.json` flags the pairs.
- [ ] **Step 6: Third read** for each pair more than 10 points apart, unless that artifact already has a lane-three verdict (then list it for the user instead): judge it again with `my-referee-three` and record all three scores.
- [ ] **Step 6b: Re-merge** with the identical Step 5 command (lane three is already in `--judges`; its new verdict files now exist) so `merged.json` and `report.md` include the third score; the report's missing-verdict list for lane three is expected for artifacts judged by two lanes.
- [ ] **Step 7: Record the reviews:** `python3 scripts/audit/audit.py track --artifact <name> --artifact-kind <command|agent|skill> --status current --today <date>` for each of the 15 judged artifacts (they have no upstream, so the row is `local`, plan 6 Task 3 Interfaces (2)).
- [ ] **Step 8: Commit** `docs(audit): merge verdicts, write the report and record the reviews`.

### Task 3: Disposition of every artifact

**Files:**
- Create: `docs/audit/<date>/disposition.md`

**Interfaces:**
- Consumes: `report.md`, `merged.json`, [Known issues](2026-10-30-00-known-issues.md).
- Produces: a table `artifact | kind | score | decision | reason | plan 8 tasks`, decision one of `keep`, `fix`, `convert-to-skill`, `merge-into <skill>`, `delete`.

- [ ] **Step 1: For each agent, answer in the table:** is it a long reference (convert), a thin wrapper around a skill (merge into it or delete), or a real delegate worth its own context (keep and fix). Seed observations to check, not conclusions: `mermaid-diagram-specialist` overlaps `mermaid-diagrams`; `ui-ux-designer` overlaps `ui-ux-principles`; `general-purpose` restates a harness default.
- [ ] **Step 2: For each command,** record whether it has an eval file; a command with side effects (`sync-branch`, `sync-skills-readme`) must have one before plan 8 edits it.
- [ ] **Step 3: List the decisions that need the user** (`delete`, `convert-to-skill`, `merge-into`) in a closing section; plan 8 does not execute those until they are answered.
- [ ] **Step 4: Commit** `docs(audit): disposition for commands and agents`.

### Task 4: Ship

- [ ] **Step 1:** `python3 -m unittest discover -s tests/audit`, `python3 scripts/audit/audit.py check --strict`, `python3 scripts/build_plugins.py` clean.
- [ ] **Step 2:** Dual-lane review of the diff (tooling and report only), one fix wave, compact to 3-4 commits, push, PR via `commands/explain-pr-changes.md`, report the disposition table to the user.
