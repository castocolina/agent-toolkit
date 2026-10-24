# Skill Audit, Spec Alignment & Self-Maintaining Toolkit — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Date:** 2026-10-16 (revised 2026-10-24)
**Status:** Draft — not started (no task below has been executed)

**Goal:** Make `castocolina/agent-toolkit` a self-maintaining marketplace: a research skill keeps `skill-judge` aligned with the Agent Skills spec, every skill is judged and fixed to Grade B or better, a 15-day workflow re-audits and opens PRs, and the README installs from this fork.

**Architecture:** Six parts, each shipped as its own PR from its own branch. Deterministic work (fetching the spec, validating, merging verdicts, detecting change, naming branches, publishing diagrams) lives in tested scripts; LLM work (judging, fixing, merging opinions, writing PR bodies) consumes and emits JSON those scripts validate. The scheduled workflow reuses the same scripts, so local and CI audits produce the same artifacts.

**Tech Stack:** Bash (skill scripts, per `AGENTS.md`), Python 3.12 stdlib (repo tooling under `scripts/`, matching `build_plugins.py`), GitHub Actions, GitHub Copilot CLI (`copilot -p`), pi coding agent, `gh`, `skills-ref` (agentskills reference validator), drawio CLI (existing `skills/draw-io/scripts/convert-drawio-to-png.sh`).

**Spec:** The requirements are this document's **Decisions** section (user requirements and answers from the 2026-10-24 session, verbatim intent) plus the upstream Agent Skills docs at `https://github.com/agentskills/agentskills/tree/main/docs` (source of `https://agentskills.io`).

## Decisions

User decisions (theirs):

1. Research skill reads agentskills.io / `agentskills/agentskills` (specification, best practices, optimizing descriptions, evaluating skills, using scripts) and updates `skill-judge` from it.
2. Apply `skill-judge` to every skill in the repo, then fix each to Grade B (≥80%) or better, target A (≥90%).
3. Translate all non-Latin script text in skills to English (marp trigger phrases included). Kaomoji and typographic symbols are allowlisted. A check blocks new non-Latin script.
4. A workflow runs every ~15 days: refreshes the spec, several Copilot models research/judge, one merges and decides whether `skill-judge` or any skill needs updating.
5. When an update is needed, the workflow opens a PR from branch `feat|fix/<yy-mm-dd>-<title-slug>`; the PR body is generated with `commands/explain-pr-changes.md`.
6. Merge knob `AUDIT_MERGE_MODE`: `manual` (default, human review), `auto` (merge when CI is green), `agent` (delegate to GitHub Copilot code review).
7. Evals follow agentskills.io `evals/evals.json` (prompt, expected_output, files, assertions); written for all skills, executed only for skills whose files or the rubric changed.
8. Copilot model IDs come from repo variables `AUDIT_RESEARCH_MODELS` and `AUDIT_MERGER_MODEL`; defaults are chosen in spike Task F1.
9. Local judges: a native Claude Code Opus subagent and `pi -p --model router-env/my-referee-one`. Fixers stay GLM 5.3 Flash via pi (original requirement 4).
10. README gives non-interactive install commands per harness and references this fork as the marketplace instead of `softaworks/agent-toolkit`.
11. Skills that cite an inspiration source get that source located, its last update compared with ours, and a recommendation the user decides on.
12. `explain-pr-changes` takes `--diagrams=none|mermaid|drawio`. Diagram files live on ONE shared branch `pr-diagrams` in folders `<PR number>/`, are reused across related/promotion PRs (A→B consolidates several merged PRs into one, B→C reuses body, images, reviewers and only retitles), and may be deleted later by the user.
13. `jev-fast-decision` is used only to classify items and present them; decisions stay with the user.
14. Upstream PR #48 was closed and `docs/diagram-authoring-rules` deleted (done 2026-10-24).

Planner calls (mine — check these):

- C1. Default `--diagrams=mermaid` so the command's current behavior is unchanged.
- C2. Diagram publishing is a new skill `skills/pr-diagrams` (commands cannot ship scripts); the `command-explain-pr-changes` plugin bundles it.
- C3. Repo tooling is one CLI `scripts/audit/audit.py` with subcommands plus one test file, stdlib only (no new dependency).
- C4. Grades are percentages, so the rubric's total points can change when the spec changes without breaking thresholds.
- C5. Claude Code-only frontmatter fields (`user-invocable`, `disable-model-invocation`, `argument-hint`, `allowed-tools`) are allowlisted rather than removed; other unknown fields move under `metadata`.
- C6. Last audited state is stored in repo variable `AUDIT_LAST_STATE`, because Actions cache evicts entries unused for 7 days (< 15).
- C7. Bot pushes/PRs use secret `AUDIT_BOT_TOKEN`; PRs created with `GITHUB_TOKEN` do not trigger the `CI` workflow.
- C8. One plan document, six parts, one PR per part; Parts C, D, E are independent of A/B and may run in parallel.

## Global Constraints

- Work happens in worktrees under `.claude/worktrees/<branch-slug>/` (gitignored).
- Skill layout per `AGENTS.md`: `skills/<kebab-name>/SKILL.md` + `README.md`; scripts `#!/bin/bash`, `set -e`, status to stderr, JSON to stdout, cleanup trap.
- `SKILL.md` < 500 lines; frontmatter `name` == directory; `description` ≤ 1024 chars.
- Never delete a skill or any `skills/*/README.md`.
- Never edit `skills/gepetto` or `skills/datadog-cli`: `.github/workflows/sync-*.yaml` overwrites them daily. Findings for them go to `docs/audit/upstream-findings.md` only.
- Do not create `.zip` packages (none exist; the `AGENTS.md` zip rule is stale and out of scope).
- Before every commit that touches `skills/`, `agents/`, `commands/` or `.claude-plugin/`: `python3 scripts/build_plugins.py` and stage `dist/` + `.claude-plugin/marketplace.json` (CI fails otherwise).
- All generated artifacts in English (`AGENTS.local.md`).
- Copied agentskills docs are CC-BY-4.0: keep `SOURCE.json` with repo, commit SHA and license next to them.
- Conventional commit messages; PR bodies via `commands/explain-pr-changes.md`.

## Review Focus

1. Spec fetch fails mid-way (network, missing file) → previously stored references stay byte-identical; nothing partial is written. Pinned in Task A1.
2. A judge emits malformed JSON, scores outside 0..max, or a missing dimension → verdict rejected and reported, never merged. Pinned in Task A3.
3. An agent creates branch `pr-diagrams/<N>` instead of folder `<N>/` on `pr-diagrams` → `pr-diagrams.sh ensure` fails loudly and `publish` refuses. Pinned in Task E2.
4. Scheduled run with no spec change and no skill change → zero Copilot calls. Pinned in Task F2 (`detect`).
5. A fix lands in an auto-synced skill (`gepetto`, `datadog-cli`) → merge marks it `synced` and the fix list excludes it. Pinned in Task A3.

---

## Part A — Research skill and spec-aligned skill-judge

Branch: `feat/<yy-mm-dd>-agentskills-research`

### Task A1: `agentskills-research` skill with tested spec fetcher

**Files:**
- Create: `skills/agentskills-research/SKILL.md`, `skills/agentskills-research/README.md`
- Create: `skills/agentskills-research/scripts/fetch-spec.sh`
- Create: `skills/agentskills-research/evals/test-fetch-spec.sh`, `skills/agentskills-research/evals/fixtures/docs/**` (six small `.mdx` fixtures)
- Create (output of first real run): `skills/skill-judge/references/agentskills/{specification,quickstart,best-practices,evaluating-skills,optimizing-descriptions,using-scripts}.md`, `skills/skill-judge/references/agentskills/SOURCE.json`
- Modify: `.claude-plugin/marketplace.json` (new plugin entry), `README.md` (skills table)

**Interfaces:**
- Produces: `fetch-spec.sh [--dest DIR] [--ref REF]` → stdout `{"ref":"main","sha":"<40 hex>","changed":["best-practices.md",...],"unchanged":[...]}`; exit 0 on success, 1 on any fetch failure.
- Env overrides (tests/CI): `AGENTSKILLS_RAW_BASE` (default `https://raw.githubusercontent.com/agentskills/agentskills`), `AGENTSKILLS_SHA` (skips `git ls-remote`).
- Source map: `docs/specification.mdx` → `specification.md`; `docs/skill-creation/<page>.mdx` → `<page>.md` for quickstart, best-practices, evaluating-skills, optimizing-descriptions, using-scripts.
- `SOURCE.json`: `{"repo":"agentskills/agentskills","ref":"main","sha":"…","fetched_at":"<ISO8601>","license":"CC-BY-4.0","files":{"<name>.md":"<sha256>"}}`.

- [ ] **Step 1: Write failing tests** in `evals/test-fetch-spec.sh` (plain bash asserts, `AGENTSKILLS_RAW_BASE=file://$FIXTURES`, `AGENTSKILLS_SHA=deadbeef…`):
  - `test_first_run_all_changed`: empty dest → `changed` has 6 names; 6 files + `SOURCE.json` exist.
  - `test_second_run_unchanged`: rerun → `changed == []`, files byte-identical.
  - `test_one_file_changed`: edit one fixture → `changed == ["best-practices.md"]`.
  - `test_missing_source_keeps_dest`: delete one fixture → exit 1, dest tree `sha256sum` identical to before.
- [ ] **Step 2:** `bash skills/agentskills-research/evals/test-fetch-spec.sh` → FAIL (script missing).
- [ ] **Step 3: Implement `fetch-spec.sh`**: download all six into a `mktemp -d` staging dir first; only when all six succeed, compare sha256 with `SOURCE.json`, move changed files into dest, rewrite `SOURCE.json`. SHA via `git ls-remote https://github.com/agentskills/agentskills refs/heads/<ref>`. Content copied verbatim (no trimming) with a one-line attribution header.
- [ ] **Step 4:** rerun tests → all PASS.
- [ ] **Step 5: Write `SKILL.md`** (use superpowers:writing-skills; follow the fetched `best-practices.md` and `optimizing-descriptions.md`). Workflow: run `fetch-spec.sh`; if `changed` is empty report "spec unchanged at <sha>" and stop; otherwise read each changed file's `git diff`, list rule additions/removals, and update `skills/skill-judge/references/rubric.md` (Task A2) and bump its `rubric_version`. Description triggers: "refresh agent skills spec", "update skill-judge from agentskills.io".
- [ ] **Step 6:** Run `fetch-spec.sh` for real against `main`; commit the six references + `SOURCE.json`.
- [ ] **Step 7:** `python3 scripts/build_plugins.py`; commit `feat(agentskills-research): fetch and track Agent Skills spec`.

### Task A2: Refactor `skill-judge` onto the fetched spec

**Files:**
- Modify: `skills/skill-judge/SKILL.md` (752 → < 500 lines)
- Create: `skills/skill-judge/references/rubric.md`, `skills/skill-judge/references/verdict.schema.json`
- Create: `skills/skill-judge/evals/evals.json`

**Interfaces:**
- Consumes: `references/agentskills/*.md` (A1).
- Produces: `rubric.md` with front block `rubric_version: <int>`, `spec_sha: <sha>`, and 8 dimensions `D1`..`D8`, each with max points and the spec file/section it derives from.
- Produces: verdict JSON (one per skill per judge) — `{"skill","judge","rubric_version","spec_sha","scores":{"D1":int…"D8":int},"max":{"D1":int…},"total":int,"max_total":int,"percent":float,"grade":"A|B|C|D|F","skills_ref_valid":bool,"findings":[{"id","dimension","severity":"critical|high|medium|low","file","line","evidence","fix"}]}`. Grades: A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, else F.

- [ ] **Step 1:** Write `rubric.md`: keep the current 8 dimensions where the spec supports them; every criterion cites `references/agentskills/<file>.md#<heading>`.
- [ ] **Step 2:** Rewrite `SKILL.md`: protocol step 1 is MANDATORY `Read` of `rubric.md` plus each spec file the rubric cites (whole sections, not summaries); output is exactly one verdict JSON object per skill. Replace the Chinese bad-description example (lines ~267-271) with an English vague description (`"Handles document stuff"`).
- [ ] **Step 3:** Write `verdict.schema.json` matching the Interfaces block (documentation for judges; validation is Task A3).
- [ ] **Step 4:** `evals/evals.json` with ≥ 3 evals (a strong skill, a vague-description skill, an over-500-line skill) and assertions like `"Output is a single JSON object"`, `"D4 score is below half of max for the vague-description skill"`.
- [ ] **Step 5:** Verify `wc -l skills/skill-judge/SKILL.md` < 500 and `uvx --from 'git+https://github.com/agentskills/agentskills@<SOURCE.json sha>#subdirectory=skills-ref' skills-ref validate skills/skill-judge` exits 0.
- [ ] **Step 6:** build plugins; commit `refactor(skill-judge): derive rubric from Agent Skills spec`.

### Task A3: `scripts/audit/audit.py` — check, validate-verdict, merge, branch-name

**Files:**
- Create: `scripts/audit/audit.py`, `scripts/audit/test_audit.py`, `scripts/audit/non_latin_allowlist.txt`
- Test: `python3 -m unittest discover -s scripts/audit -v`

**Interfaces:**
- `audit.py check [--strict] [--skills a,b]` → `{"skills":[{"name","ok","issues":[{"code","detail"}]}]}`; codes `skills_ref`, `lines_over_500`, `description_too_long`, `name_mismatch`, `missing_readme`, `non_latin`. `--strict` exits 1 when any issue. `skills_ref` runs the pinned `skills-ref validate` and ignores the C5 allowlisted fields.
- `audit.py validate-verdict FILE...` → exit 1 and one `FILE: reason` line per invalid verdict.
- `audit.py merge --in DIR --out DIR` → writes `merged.json` (`{"skills":[{"name","percent","grade","judges":{judge:percent},"disagreement":bool,"synced":bool,"findings":[…]}],"needs_update":bool}`) and `report.md`. Rules: percent = mean of valid verdicts; `disagreement` when judge percents differ by > 10; findings deduped on `(dimension, file, fix lowercased)`; `synced` = skill in `{gepetto, datadog-cli}` and its findings excluded from the fix list; `needs_update` = any non-synced skill below 80 or any critical/high finding.
- `audit.py branch-name --type feat|fix --title TEXT [--date YY-MM-DD]` → `feat/26-10-24-refresh-skill-judge-rubric` (ASCII-folded, lowercase, `[a-z0-9-]`, slug ≤ 50 chars, date defaults to UTC today).
- Non-Latin rule: any char whose Unicode script is Han, Hiragana, Katakana, Hangul, Cyrillic, Arabic, Hebrew, Thai, Devanagari or Greek, unless the `path:line-text` is in `non_latin_allowlist.txt` (seed: the meme-factory kaomoji line, `·` in marp `official-themes.md`).

- [ ] **Step 1: Failing tests** in `test_audit.py`:
  - `test_check_flags_over_500_lines`, `test_check_flags_non_latin`, `test_check_allowlist_suppresses`, `test_check_name_mismatch` (tmp skill dirs).
  - `test_validate_rejects_missing_dimension`, `test_validate_rejects_score_over_max`, `test_validate_rejects_non_json`, `test_validate_accepts_valid`.
  - `test_merge_means_and_disagreement` (judges 92 and 78 → percent 85, `disagreement` true), `test_merge_skips_invalid_verdict`, `test_merge_marks_synced_skills` (gepetto findings absent from fix list), `test_merge_needs_update_on_high_finding`.
  - `test_branch_name_slug` (`"Refresh: skill-judge rubric ✨ für v2"` → `feat/26-10-24-refresh-skill-judge-rubric-fur-v2`), `test_branch_name_truncates`.
- [ ] **Step 2:** run tests → FAIL.
- [ ] **Step 3:** implement `audit.py` (argparse subcommands; `unicodedata` has no script property, so embed the script code-point ranges for the listed scripts as a module constant).
- [ ] **Step 4:** run tests → PASS. Run `python3 scripts/audit/audit.py check` on the repo and save the output as the Part B baseline (expect the 5 known `skills_ref` failures, 5 `lines_over_500`, the non-Latin files).
- [ ] **Step 5:** commit `feat(audit): add skill check, verdict validation and merge tooling`; open Part A PR with `/explain-pr-changes`.

---

## Part B — Audit and fix every skill

Branch: `fix/<yy-mm-dd>-skill-audit-fixes` (may split by category into several PRs). Depends on Part A.

### Task B1: Deterministic fixes (non-Latin, frontmatter)

**Files:** `skills/marp-slide/{SKILL.md,README.md,assets/template-*.md}`, `skills/draw-io/{scripts/find_aws_icon.py,references/aws-icons.md}`, frontmatter of `skills/{daily-meeting-update,design-system-starter,humanizer,qa-test-planner,react-dev}/SKILL.md`, `.github/workflows/main.yaml`.

- [ ] **Step 1:** `jev-fast-decision` classifies each non-Latin hit from the A3 baseline into `translate` / `allowlist`; present the table to the user; apply after approval.
- [ ] **Step 2:** Translate to English; marp trigger phrases become English equivalents ("make it look nice", "make it cool"). `find_aws_icon.py` behavior unchanged: `python3 skills/draw-io/scripts/find_aws_icon.py lambda` prints the same rows before and after.
- [ ] **Step 3:** Frontmatter: move `version`, `trigger`, `tags` under `metadata`; keep C5 fields; fix the YAML error in `design-system-starter` line 7.
- [ ] **Step 4:** `python3 scripts/audit/audit.py check --strict --skills <touched>` exits 0.
- [ ] **Step 5:** Add a `Validate skills` step to `.github/workflows/main.yaml` running `python3 scripts/audit/audit.py check --strict` (installs `uv` for `skills-ref`). Build plugins; commit `fix(skills): translate non-Latin text and normalize frontmatter`.

### Task B2: Evals for every skill

**Files:** Create `skills/<name>/evals/evals.json` for every skill except `gepetto`, `datadog-cli` (existing `skills/session-handoff/evals/*` stay; add `evals.json` beside them).

- [ ] **Step 1:** For each skill, ≥ 3 evals per agentskills `evaluating-skills.md`: varied phrasing (casual + precise), realistic context, ≥ 1 near-miss prompt that should NOT trigger the skill, objective assertions only. Dispatch in batches of ~9 skills to subagents.
- [ ] **Step 2:** `audit.py check` gains code `missing_evals` (test `test_check_flags_missing_evals` first); `check --strict` exits 0.
- [ ] **Step 3:** commit `test(skills): add agentskills evals for every skill`.

### Task B3: Judge, merge, fix, re-judge

**Files:** Create `docs/audit/<yyyy-mm-dd>/judgements/{opus,my-referee-one}/<skill>.json`, `docs/audit/<yyyy-mm-dd>/{merged.json,report.md}`; modify skills per the merged fix list.

- [ ] **Step 1: Judge A:** native Claude Code subagents (`Agent`, `model: opus`), ~9 skills each, prompt = `skills/skill-judge/SKILL.md` + skill path; write verdicts to `judgements/opus/`.
- [ ] **Step 2: Judge B:** `pi -p --model router-env/my-referee-one "<same prompt>"` per batch, in the background; write to `judgements/my-referee-one/`.
- [ ] **Step 3:** `audit.py validate-verdict docs/audit/<date>/judgements/*/*.json` → exit 0 (re-run a judge for any rejected verdict, max 2 retries, then record it as missing).
- [ ] **Step 4:** `audit.py merge` → `merged.json`, `report.md`. Present `disagreement` skills to the user before fixing.
- [ ] **Step 5: Fix:** `pi -p --provider zai-coding-cn --model glm-5.3-flash` per batch, applying ONLY the merged fix list; split > 500-line bodies into `references/`.
- [ ] **Step 6:** `audit.py check --strict` exits 0; `git diff --stat` reviewed per skill.
- [ ] **Step 7:** Re-run Steps 1-4 on fixed skills; any skill < 80 gets up to 2 more fix rounds; remaining ones are listed in `report.md` under "Below target".
- [ ] **Step 8:** Build plugins; commit per category; final `docs(audit): <date> skill audit report`.

---

## Part C — Upstream inspiration sources

Branch: `docs/<yy-mm-dd>-upstream-sources`. Independent.

### Task C1: Source registry and staleness report

**Files:** Create `docs/audit/upstream-sources.json`, `docs/audit/upstream-sources.md`; modify `scripts/audit/audit.py` (+ tests).

**Interfaces:**
- Registry entry: `{"skill","source","kind":"github|github-path|wikipedia|unversioned","ref"}` (`github-path` = `owner/repo:path`).
- `audit.py upstreams --registry FILE` → `[{"skill","source","source_updated":"<ISO>|null","ours_updated":"<ISO>","stale":bool}]`; `stale` = source newer than `git log -1 --format=%cI -- skills/<skill>`. GitHub via `gh api repos/<o>/<r>/commits?path=<p>&per_page=1`; Wikipedia via `https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=<t>&rvprop=timestamp&format=json`.

- [ ] **Step 1:** Seed known sources: `writing-clearly-and-concisely` ← `obra/the-elements-of-style`; `humanizer` ← `blader/humanizer` and `Wikipedia:Signs_of_AI_writing`; `react-useeffect` ← `reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md`; `agent-md-refactor` ← Matt Pocock post (unversioned); `domain-name-brainstormer` ← Lenny's Newsletter (unversioned); fork root ← `softaworks/agent-toolkit`.
- [ ] **Step 2:** Scan all `skills/*/{SKILL,README}.md` for further URLs/credits; `jev-fast-decision` classifies each as `inspiration-source` / `incidental-link`; present; add approved ones.
- [ ] **Step 3:** Tests `test_upstreams_stale_when_source_newer`, `test_upstreams_unversioned_never_stale` (stub the fetch function); implement; PASS.
- [ ] **Step 4:** Run it; for each stale source, diff upstream changes since our last change and write a per-skill recommendation (`update` / `ignore` + one-line reason) to `upstream-sources.md`. The user decides; approved updates become follow-up commits in this PR.
- [ ] **Step 5:** commit `docs(audit): track and report upstream inspiration sources`.

---

## Part D — README installs from this fork

Branch: `docs/<yy-mm-dd>-fork-install`. Independent.

### Task D1: Marketplace owner and per-harness install commands

**Files:** Modify `README.md` (install section, lines ~18-90 and ~145-152), `.claude-plugin/marketplace.json` (`owner`), `CONTRIBUTING.md` (repo references).

- [ ] **Step 1:** `owner` → `{"name":"castocolina","url":"https://github.com/castocolina"}`; keep marketplace `name: agent-toolkit` so `<plugin>@agent-toolkit` stays valid.
- [ ] **Step 2:** Verify every command against the installed CLI's `--help` or current official docs before writing it; drop any harness whose path cannot be verified rather than guessing. Targets: skills CLI (`npx skills add castocolina/agent-toolkit …` non-interactive flags), Claude Code (`claude plugin marketplace add castocolina/agent-toolkit`, `claude plugin install <plugin>@agent-toolkit`, `claude plugin marketplace update agent-toolkit`, and switching from upstream: `claude plugin marketplace remove agent-toolkit` first), Codex, Cursor, opencode, pi, GitHub Copilot CLI, and a universal `git clone` into `~/.agents/skills/`.
- [ ] **Step 3:** Interactive `/plugin` stays only as a one-line "interactive alternative" note. Add attribution: "Fork of softaworks/agent-toolkit by @leonardocouy".
- [ ] **Step 4:** Verify `rg -c 'softaworks/agent-toolkit' README.md` == 1 (the attribution) and run each Claude Code command once in a scratch `HOME` to confirm it installs from the fork.
- [ ] **Step 5:** build plugins; commit `docs(readme): install from castocolina fork with non-interactive commands`.

---

## Part E — `explain-pr-changes --diagrams` and shared `pr-diagrams` branch

Branch: `feat/<yy-mm-dd>-pr-diagrams`. Independent.

### Task E1: Spike — image upload options

- [ ] **Step 1:** Check whether `gh` or the REST/GraphQL API can now attach images to a PR body (user-attachments). Record the result in `skills/pr-diagrams/README.md` under "Why a shared branch". If a supported upload API exists, stop and present it to the user before Task E2; otherwise continue.

### Task E2: `pr-diagrams` skill with tested publisher

**Files:**
- Create: `skills/pr-diagrams/{SKILL.md,README.md}`, `skills/pr-diagrams/scripts/pr-diagrams.sh`, `skills/pr-diagrams/evals/{test-pr-diagrams.sh,evals.json}`
- Modify: `.claude-plugin/marketplace.json` (`command-explain-pr-changes` entry gets `"skills": ["./skills/pr-diagrams"]`; `pr-diagrams` also gets its own entry)

**Interfaces:**
- `pr-diagrams.sh ensure` — if `origin` has no `refs/heads/pr-diagrams`, create it as an orphan from the empty tree (`git commit-tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904`) and push; exit 1 if any `refs/heads/pr-diagrams/*` exists locally or on origin.
- `pr-diagrams.sh publish <PR> <file>...` — uploads each file to `<PR>/<basename>` on branch `pr-diagrams` via `gh api -X PUT repos/{owner}/{repo}/contents/<PR>/<name>` (no checkout, no new branch); stdout `[{"file","path","url"}]`, url = `https://github.com/<owner>/<repo>/blob/pr-diagrams/<PR>/<name>?raw=true`.
- `pr-diagrams.sh related <base> <head>` — PR numbers whose commits are in `<base>..<head>` (`gh api repos/{o}/{r}/commits/<sha>/pulls`) and that have a `<PR>/` folder; stdout `[{"pr","title","files":[…]}]`.
- `pr-diagrams.sh list <PR>` — stdout `[{"path","url"}]`.
- Env `GH` (default `gh`) lets tests substitute a stub.

- [ ] **Step 1: Failing tests** (local bare repo as `origin`, stub `GH`): `test_ensure_creates_orphan_branch` (branch has 0 parents, empty tree), `test_ensure_idempotent`, `test_ensure_fails_on_per_pr_branch` (pre-create `pr-diagrams/12` → exit 1, message names the rule), `test_publish_puts_under_pr_folder` (stub records path `12/flow.png` and branch `pr-diagrams`), `test_related_dedupes_prs`.
- [ ] **Step 2:** run → FAIL. **Step 3:** implement. **Step 4:** run → PASS.
- [ ] **Step 5:** `SKILL.md` states in its first section: "`pr-diagrams` is ONE shared branch; `<N>` is a folder inside it. Never create a branch named `pr-diagrams/<N>` or one branch per PR." Explains reuse and that users may delete folders when no longer needed.
- [ ] **Step 6:** build plugins; confirm `dist/plugins/command-explain-pr-changes/skills/pr-diagrams/` exists; commit `feat(pr-diagrams): shared branch publisher for PR diagrams`.

### Task E3: `explain-pr-changes` flags and promotion reuse

**Files:** Modify `commands/explain-pr-changes.md`; create `commands/evals/explain-pr-changes.json` (agentskills eval format).

- [ ] **Step 1:** Arguments: `--diagrams=none|mermaid|drawio` (default `mermaid`), `--reuse-from=<PR>`, remaining arguments keep today's "Close $ARGUMENTS" behavior.
- [ ] **Step 2:** Modes, decided in this order: (a) `--reuse-from` given or head is a long-lived branch (`PR_PROMOTION_BRANCHES`, default `develop,staging,main`) → promotion: run `related`; one related PR → reuse its body, diagrams and reviewers, title `[<head> → <base>] <original title>`; several → consolidated summary that links existing diagrams and adds at most one new consolidated diagram; (b) otherwise feature PR.
- [ ] **Step 3:** Ordering: create/update the PR first (number needed), then `ensure` + `publish`, then edit the body with the returned URLs. Mermaid: inline block in the body AND publish the `.mmd` source. Drawio: author per `skills/draw-io`, render with `skills/draw-io/scripts/convert-drawio-to-png.sh`, publish `.drawio` + `.png`. Before generating, reuse any diagram returned by `related` that still matches the change.
- [ ] **Step 4:** Evals: feature PR + mermaid, feature PR + drawio, promotion with 3 related PRs (assert no new per-PR branch, ≤ 1 new diagram), B→C single-related reuse (assert title format and reused body).
- [ ] **Step 5:** Dry run on a scratch PR in this fork with each `--diagrams` value; delete the scratch PR's folder afterwards. Commit `feat(explain-pr-changes): diagram flag and promotion reuse`.

---

## Part F — 15-day audit workflow

Branch: `feat/<yy-mm-dd>-scheduled-skill-audit`. Depends on A, B (B3 artifacts format), E.

### Task F1: Spike — Copilot CLI in Actions

- [ ] **Step 1:** Workflow `.github/workflows/copilot-smoke.yaml` (`workflow_dispatch` only): install Copilot CLI (verify npm package name from GitHub docs), auth with secret `COPILOT_GITHUB_TOKEN` (fine-grained PAT, "Copilot Requests" permission), list models, run `copilot -p "Reply with OK" -s --no-ask-user --model=<each>`.
- [ ] **Step 2:** Confirm Copilot code review's reviewer handle and bot login for `gh pr edit --add-reviewer`, and that it only submits `COMMENTED` reviews.
- [ ] **Step 3:** Present available models; the user picks; set repo variables `AUDIT_RESEARCH_MODELS`, `AUDIT_MERGER_MODEL`, `AUDIT_MERGE_MODE=manual`. Delete the smoke workflow.

### Task F2: `audit.py detect`

**Interfaces:**
- `audit.py detect --state JSON --spec-sha SHA [--force]` → `{"run_needed":bool,"spec_changed":bool,"skills":[names],"state":{"spec_sha","skills":{name: tree_sha}}}`; tree sha = `git rev-parse HEAD:skills/<name>`. `skills` = changed skills, or all skills when `spec_changed` or the rubric changed. Empty/invalid `--state` → treat as first run (all skills).

- [ ] **Step 1:** tests `test_detect_no_change_no_run`, `test_detect_spec_change_runs_all`, `test_detect_single_skill_change`, `test_detect_bad_state_runs_all`, `test_detect_force`; FAIL → implement → PASS; commit.

### Task F3: `.github/workflows/skill-audit.yaml`

**Files:** Create `.github/workflows/skill-audit.yaml`, `.github/audit/{research,merge,fix}-prompt.md`; modify `README.md` (one "Automated audits" paragraph with the knobs).

Jobs:
1. `detect` (no LLM): `fetch-spec.sh --dest $RUNNER_TEMP/spec`, `audit.py detect --state "$AUDIT_LAST_STATE"`, `audit.py upstreams`; outputs `run_needed`, `skills`. Stops here when nothing changed.
2. `research` (matrix over `AUDIT_RESEARCH_MODELS`): `copilot -p "$(cat .github/audit/research-prompt.md)" -s --no-ask-user --model=$M --allow-tool='read, write'` judging `skills` with `skill-judge` and running their `evals/evals.json`; `audit.py validate-verdict`; upload artifact `verdicts-<model>`.
3. `merge`: `audit.py merge`; merger model reads `merged.json` + spec diff + upstream report and writes `decision.json` `{"update":bool,"type":"feat|fix","title","targets":["skill-judge"|<skill>…],"rationale"}`; validated by `audit.py validate-decision` (add with test `test_validate_decision_rejects_unknown_target`).
4. `apply` (if `update`): branch via `audit.py branch-name`; fixer model applies `targets`; `audit.py check --strict`; evals for changed skills; `python3 scripts/build_plugins.py`; push with `AUDIT_BOT_TOKEN`; PR body via `copilot -p` following `commands/explain-pr-changes.md --diagrams=${AUDIT_PR_DIAGRAMS:-mermaid}` (install drawio + xvfb only when `drawio`).
5. Merge knob: `manual` → nothing; `auto` → `gh pr merge --auto --squash`; `agent` → request Copilot review; workflow `.github/workflows/skill-audit-gate.yaml` on `pull_request_review` from the Copilot bot enables auto-merge when the review has 0 comments, else adds label `needs-human`.
6. Always (when `research` ran): `gh variable set AUDIT_LAST_STATE` with `detect`'s `state`, so a "no update" decision is not re-researched next run.

- Schedule `0 6 1,16 * *` plus `workflow_dispatch` inputs `force` (bool) and `merge_mode`.
- Publishing = merging the PR; the existing `auto-bump.yaml` bumps the version and rebuilds `dist/`.

- [ ] **Step 1:** `actionlint` (downloaded via its official script) on both workflows → 0 errors.
- [ ] **Step 2:** Push branch; `gh workflow run skill-audit.yaml -f force=true -f merge_mode=manual` on the fork; expect a PR on `feat|fix/<yy-mm-dd>-…` whose CI runs, or a logged "no update" decision and an updated `AUDIT_LAST_STATE`.
- [ ] **Step 3:** Second dispatch without `force` → `detect` stops with `run_needed=false` (zero Copilot calls).
- [ ] **Step 4:** commit `feat(ci): scheduled skill audit with Copilot judges`; PR via `/explain-pr-changes`.

---

## Required secrets and variables (Part F)

| Name | Kind | Purpose |
|---|---|---|
| `COPILOT_GITHUB_TOKEN` | secret | Fine-grained PAT with "Copilot Requests" |
| `AUDIT_BOT_TOKEN` | secret | Fine-grained PAT: contents, pull-requests, variables write (pushes trigger CI) |
| `AUDIT_RESEARCH_MODELS` | variable | Comma list of Copilot model IDs (F1) |
| `AUDIT_MERGER_MODEL` | variable | Merger/fixer model ID (F1) |
| `AUDIT_MERGE_MODE` | variable | `manual` (default) / `auto` / `agent` |
| `AUDIT_PR_DIAGRAMS` | variable | `none` / `mermaid` (default) / `drawio` |
| `AUDIT_LAST_STATE` | variable | Written by the workflow (C6) |
