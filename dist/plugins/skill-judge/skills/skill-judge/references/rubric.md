rubric_version: 4
spec_sha: 69ef37e9424c0a7ea9dd2293b559e43ec8176379

# Skill Judge Rubric v4

Eight dimensions, 125 points. Grades use the percentage of the total, so the total can change in a later rubric version without touching the grade bands. The `source` column lists the pinned Agent Skills spec sections each dimension derives from; read them in full before scoring.

| id | name | max | source |
|----|------|-----|--------|
| D1 | Knowledge Delta | 20 | references/agentskills/best-practices.md#add-what-the-agent-lacks-omit-what-it-knows; references/agentskills/best-practices.md#start-from-real-expertise |
| D2 | Mindset, Procedures and Patterns | 15 | references/agentskills/best-practices.md#favor-procedures-over-declarations; references/agentskills/best-practices.md#patterns-for-effective-instructions |
| D3 | Anti-Pattern Quality | 15 | references/agentskills/best-practices.md#gotchas-sections |
| D4 | Specification Compliance | 15 | references/agentskills/specification.md#frontmatter; references/agentskills/specification.md#name-field; references/agentskills/specification.md#description-field; references/agentskills/optimizing-descriptions.md#writing-effective-descriptions |
| D5 | Progressive Disclosure | 15 | references/agentskills/specification.md#progressive-disclosure; references/agentskills/specification.md#file-references; references/agentskills/best-practices.md#structure-large-skills-with-progressive-disclosure |
| D6 | Freedom Calibration | 15 | references/agentskills/best-practices.md#match-specificity-to-fragility; references/agentskills/best-practices.md#provide-defaults-not-menus |
| D7 | Tests and Evals | 15 | references/agentskills/evaluating-skills.md#designing-test-cases; references/agentskills/optimizing-descriptions.md#designing-trigger-eval-queries; references/agentskills/using-scripts.md#designing-scripts-for-agentic-use |
| D8 | Practical Usability | 15 | references/agentskills/best-practices.md#validation-loops; references/agentskills/best-practices.md#checklists-for-multi-step-workflows; references/agentskills/specification.md#body-content |

## Scoring rules

- Score integers only, 0 to the dimension max. Quote evidence (file and line) for every score below max; each such score needs at least one finding.
- Judge only what the files show. Never credit a claim the skill makes about itself ("tested", "production-ready").
- Total = D1..D8. Percent = round(total / max_total * 100, 1). Grade: A at 90 or more, B at 80, C at 70, D at 60, otherwise F.
- Finding severity: critical = the skill will not load or will never trigger; high = a wrong or harmful instruction, or a dimension scored in its bottom band; medium = a measurable weakness; low = polish.

## Repository files that are never deductions

The repository requires `README.md`, `evals/` (including `evals/files/` eval inputs), bundled `references/` files and `SOURCE.json` (provenance next to copied documents). Never deduct for them under any dimension. Deduct only for redundant extras that serve no purpose for the agent or the repository, such as `CHANGELOG.md`, `INSTALLATION_GUIDE.md` or `CONTRIBUTING.md` (D5, low severity).

## D1: Knowledge Delta (20) — the core dimension

Does the skill add expert knowledge the agent lacks? Value = expert-only knowledge minus what the agent already knows. Classify every section:

- Expert: the model genuinely does not know it. Keep.
- Activation: the model knows it but may not think of it. Keep if brief.
- Redundant: the model certainly knows it. Delete; it wastes shared context.

Good ratio: more than 70% expert, under 20% activation, under 10% redundant.

Bands:
- 0-5: explains basics (what is X, standard library tutorials, generic best practices).
- 6-10: expert knowledge diluted by obvious content.
- 11-15: mostly expert, minimal redundancy.
- 16-20: every paragraph earns its tokens.

Required criteria, judged from your own knowledge (do not look anything up):
- Flag content that current harnesses (Claude Code, Codex, Cursor, opencode, pi, Copilot CLI) already do natively: plan mode, todo tracking, file search, diffing, commit and PR helpers, sub-agent dispatch, memory files, slash-command and skill discovery.
- Flag content that current models already know: library tutorials, language syntax, common CLI flags, generic engineering advice.
- Instructions to use a harness feature are not a deduction when they correct a non-obvious mistake; restating what the feature does is.

Red flags (score at most 5): "What is X" sections, step-by-step tutorials for standard operations, generic advice such as "write clean code". Green flags: decision trees for non-obvious choices, trade-offs only experience teaches, real-world edge cases, "NEVER do X because [non-obvious reason]".

## D2: Mindset, Procedures and Patterns (15)

Two parts, summed to 15: mindset and procedures score 0-11, pattern fit scores 0-4.

### Mindset and procedures (0-11)

Does the skill transfer how an expert thinks, plus domain procedures the model would not derive?

- 0-2: only generic procedures the model already knows ("open file, edit, save").
- 3-5: domain procedures but no thinking frameworks, or the reverse.
- 6-8: good balance of thinking patterns ("before X, ask: ...") and domain workflows.
- 9-11: shapes thinking and supplies sequences the model would not know (ordering such as validate before packing, easy-to-miss mandatory steps, proprietary tools).

Valuable: non-obvious ordering, critical steps that are easy to miss, workflows for new or proprietary tools. Redundant: generic file operations, loops and error handling, well-documented library usage. Prefer procedures over declarations: the skill should teach an approach that generalises, not only the answer to one instance.

### Pattern fit (0-4)

Which established design pattern does the skill follow, and is it the right one for its task?

- Mindset (about 50 lines): thinking over technique, strong NEVER list, high freedom. For creative tasks that need taste.
- Navigation (about 30 lines): minimal SKILL.md that routes to sub-files. For several distinct scenarios.
- Philosophy (about 150 lines): philosophy first, then expression. For art or creation needing originality.
- Process (about 200 lines): phased workflow with checkpoints, medium freedom. For complex multi-step projects.
- Tool (about 300 lines): decision trees, code examples, low freedom. For precise operations on a specific format.

Bands: 0 = no recognisable pattern, chaotic structure; 1-2 = partial pattern with significant deviations; 3 = clear pattern, minor deviations; 4 = masterful application of the right pattern.

## D3: Anti-Pattern Quality (15)

Half of expert knowledge is what NOT to do, learned by stepping on landmines. Does the skill state specific NEVER items with reasons?

- 0-3: none.
- 4-7: generic warnings ("be careful", "consider edge cases").
- 8-11: specific NEVER list with some reasoning.
- 12-15: expert-grade anti-patterns with WHY, including a Gotchas section of environment-specific facts that defy assumptions.

The test: would an expert say "I learned this the hard way" or "this is obvious to everyone"?

## D4: Specification Compliance, including the description (15)

Check against `specification.md`: `name` is 1-64 characters, lowercase letters, digits and single hyphens, no leading or trailing hyphen, and equals the parent directory name; `description` is 1-1024 characters; optional fields (`license`, `compatibility` up to 500 characters, `metadata` string map, `allowed-tools`) are valid when present; the file starts with valid YAML frontmatter.

This repo allowlists the Claude Code-only top-level fields `user-invocable`, `disable-model-invocation` and `argument-hint` (this repo's frontmatter allowlist); they never lower D4. Any other unknown top-level field still does.

The description is the only text an agent sees before loading the skill, so it decides whether the skill is ever used. It must give WHAT (specific capabilities), WHEN (trigger scenarios, including cases where the user does not name the domain) and KEYWORDS (file extensions, domain terms), and say what it is not for when a near-miss neighbour exists (`optimizing-descriptions.md`: imperative phrasing, focus on user intent, concise).

- 0-5: missing or invalid frontmatter, name that breaks a hard rule, or description over 1024 characters.
- 6-7: valid frontmatter, but the description has no WHEN and no keywords ("Handles document stuff", "A helpful skill for various tasks").
- 8-10: WHAT is specific, but WHEN or keywords are missing or incomplete.
- 11-13: WHAT and WHEN present; keywords thin or boundaries missing.
- 14-15: specific description with WHAT, WHEN, keywords and boundaries.

Never accept "when to use" guidance that exists only in the body; the agent cannot see it before triggering.

## D5: Progressive Disclosure (15)

Three layers: metadata (name and description, about 100 tokens), SKILL.md body (under 500 lines and about 5000 tokens), resources loaded on demand (`scripts/`, `references/`, `assets/`). File references are relative to the skill root and one level deep.

- 0-5: everything in SKILL.md (over 500 lines is a finding at least high), no structure.
- 6-10: references exist but it is unclear when to load them.
- 11-13: good layering; loading triggers embedded in workflow steps.
- 14-15: decision tree plus explicit triggers, with every optional reference gated by a condition.

Loading criteria apply to optional references only. A reference that the skill's own protocol requires on every run (for example a judge that must read its rubric and the spec files the rubric cites) is read unconditionally by design; such reads are required, are not a trigger-quality problem and never lower D5. For optional references, the best triggers state the scenario and, where over-loading is a real risk, name the files not to load for it ("Do NOT Load `x.md` for this task"). A skill with no optional references needs no such guidance. Judge simple skills (no references, under 100 lines) on conciseness and self-containment.

## D6: Freedom Calibration (15)

Does specificity match fragility? Ask: if the agent errs, what is the consequence? High consequence means low freedom (exact scripts, exact steps); low consequence means high freedom (principles, not steps). Creative work gets principles; file-format operations and destructive actions get exact commands; reviews get prioritised criteria. Prefer a clear default with an escape hatch over a menu of equal options.

- 0-5: severely mismatched (rigid scripts for creative work, vague guidance for fragile operations).
- 6-10: partially appropriate.
- 11-13: good calibration for most scenarios.
- 14-15: calibrated throughout.

## D7: Tests and Evals (15)

Does the skill ship evidence that it works? Output evals and trigger queries live in the skill's `evals/` (eval input files in `evals/files/`). The runnable script test lives in the repository's `tests/skills/<name>/`, not in the skill (it is not shipped with it). Judge only files that are present. When `scripts/` exists, look for the script test in `tests/skills/<name>/`. Never guess at a test you cannot see.

Three sub-checks. With `scripts/`, each is worth 5 points. Without `scripts/`, the split is a fixed integer one: output evals 8, trigger queries 7 (the script-test share is redistributed) and the bands below apply to their combined quality:
- Output evals (`evals/evals.json`, per `evaluating-skills.md`): realistic prompts (casual and precise phrasings, at least one edge case), expected output, input files, and verifiable assertions rather than vague ones.
- Trigger queries (`evals/trigger-queries.json`, per `optimizing-descriptions.md`): about 20 queries, 8-10 should-trigger and 8-10 should-not-trigger, with near-misses among the negatives and realistic context.
- A runnable test in `tests/skills/<name>/` when `scripts/` exists (per `using-scripts.md`): scripts are runnable non-interactively, document usage with `--help`, emit structured output and have at least a smoke test. When `scripts/` exists but `tests/skills/<name>/` was not checked (only the skill directory was supplied), keep the 5/5/5 allocation, score this sub-check on what `scripts/` shows (runs non-interactively, documents `--help`, emits structured output), do not deduct for the smoke test you could not see, and state that limit in the D7 finding. When judging a skill outside this repository, a script test the skill ships with it counts the same, wherever its repository keeps it. A skill without `scripts/` is never penalised for lacking script tests; see the allocation above.

Bands: 0-3 no tests; 4-8 partial (only one sub-check, or placeholder assertions); 9-11 solid evals and queries with minor gaps; 12-15 complete, realistic, verifiable and maintained alongside the skill.

## D8: Practical Usability (15)

Can an agent act on this skill without guessing?

- 0-5: confusing, incomplete, contradictory.
- 6-10: usable with noticeable gaps.
- 11-13: clear for common cases.
- 14-15: covers edge cases, error handling and fallbacks.

Check: decision trees for multi-path scenarios, code examples that actually work, fallbacks when the main approach fails, realistic edge cases, validation loops and checklists for multi-step work, and immediate actionability. Mentally run each decision tree to see whether it reaches the right choice.

## Common failure patterns

1. The Tutorial: explains basics the model knows. Fix: delete; keep expert decisions and anti-patterns.
2. The Dump: SKILL.md of 800+ lines. Fix: routing and decision trees in SKILL.md, detail in `references/`.
3. The Orphan References: reference files nothing loads. Fix: add a scenario-triggered read ("read X when Y") at the workflow step that needs it; add "Do NOT Load" only where an optional file would waste context for that scenario.
4. The Checkbox Procedure: mechanical steps with no reasoning. Fix: "before X, ask yourself", decision principles.
5. The Vague Warning: "be careful", "avoid errors". Fix: specific NEVER items with non-obvious reasons.
6. The Invisible Skill: good body, vague description. Fix: WHAT, WHEN, KEYWORDS in the description.
7. The Wrong Location: "when to use" section in the body only. Fix: move trigger information to the description.
8. The Redundant Extras: `CHANGELOG.md`, `INSTALLATION_GUIDE.md`, `CONTRIBUTING.md` and similar files that duplicate or document the skill without helping the agent. The repository-required `README.md`, `evals/`, `references/` bundled files and `SOURCE.json` are never part of this pattern. Fix: delete the extras.
9. The Freedom Mismatch: rigid scripts for creative tasks, vague guidance for fragile ones. Fix: match freedom to fragility.

## Quick checklist

- D1: no "what is X"; no tutorials; no native-harness restatements; decision trees, trade-offs, edge cases present.
- D2: thinking frameworks plus domain procedures; the pattern fits the task.
- D3: explicit NEVER or Gotchas list with reasons.
- D4: valid name equal to directory; description 1-1024 characters with WHAT, WHEN, keywords.
- D5: SKILL.md under 500 lines; optional references gated by conditions; one level deep.
- D6: freedom matches fragility; defaults over menus.
- D7: evals.json, trigger-queries.json in `evals/`; script smoke test in `tests/skills/<name>/` when scripts exist.
- D8: decision trees, working examples, fallbacks, edge cases.
