---
name: skill-judge
description: Score an Agent Skill against the pinned Agent Skills spec and best practices. Use when asked to judge, review, audit, grade, compare or improve a SKILL.md or skill directory, or when a skill never triggers, feels bloated, wastes tokens on what the model already knows, or the user asks if it is ready to publish, even without the word "judge". Returns percent, grade, per-dimension scores and fixes, or a machine-readable verdict line; it reports fixes and never edits files. Not for writing a new skill from scratch, and not for refreshing the rubric from agentskills.io (agentskills-research).
---

# Skill Judge

Judge a skill the way an expert reviewer would: by the expert knowledge it adds beyond what the model and the harness already provide (D1), and by how well it follows the Agent Skills spec. The rubric and the spec copies it cites are bundled in `references/`; this file is the protocol and the output contract. D1 classification (expert, activation, redundant) is defined in `references/rubric.md`.

## Mandatory protocol

Follow these steps in order. Do not skip step 1 even when the request looks simple.

1. **Read the rubric and the spec, in full.** `Read` `references/rubric.md` (relative to this skill's directory) completely, then `Read` each file in the `source` column of its table; read each cited file in full. These reads are required on every run, are unconditional by design, and are exempt from the rubric's D5 loading criteria: the protocol itself needs them. Note `rubric_version` and `spec_sha` from the first two lines of the rubric.
2. **Locate the target.** The target is a directory containing `SKILL.md` (or the `SKILL.md` file itself; use its directory). List the directory. Read `SKILL.md` completely. Note its line count, the frontmatter, and which of `README.md`, `references/`, `scripts/`, `evals/` exist.
3. **Read what the score depends on.** Open an optional file only when a dimension needs it: `evals/evals.json` and `evals/trigger-queries.json` (inputs in `evals/files/`) for D7, the runnable script test in the repository's `tests/skills/<name>/` (not shipped with the skill) when `scripts/` exists, `scripts/` for D7 and D8, referenced files for D5. Read `references/agentskills/skills-ref-validator.py.txt` only when a frontmatter field's validity is unclear for D4, and `references/verdict.schema.json` only when unsure about a verdict field. Unless skill-judge itself is the target, do not read `references/judge-prompt.md` or skill-judge's own `evals/evals.json` and `evals/trigger-queries.json`. A fixture under `evals/files/` that you are asked to judge is the target and is read normally. If the request supplies only `SKILL.md` (no directory), judge from it and say so in the D7 finding; never invent files. If the skill has `scripts/` and only its directory is supplied, `tests/skills/<name>/` was not checked: keep the rubric's 5/5/5 allocation, score the script-test sub-check on what `scripts/` shows, do not deduct for the smoke test you could not see, and state that limit in the D7 finding.
4. **Score in this order**, with the integer bands in the rubric:
   - Description and D4 first: it is all an agent sees before loading, so it fixes how the body deserves to be read. A D4 finding's `fix` is the full replacement description text (WHAT it does, WHEN to trigger, keywords), not advice about it.
   - Then classify each H2 section for D1 and weight it by line count: the D1 ratio is in lines, not sections.
   - Then D8: identify the inputs, follow each decision branch and each example to its outcome, and cite the failing branch in the finding. Credit D8 only for branches you actually followed.
   - D2, D3, D5, D6, D7 in any order.

   For each score below its max, quote the line and record a finding.
5. **Deduct each defect once**, in the dimension that owns it: missing triggers in the description is D4 only; a missing Gotchas or NEVER list is D3 only; an unreferenced file is D5 only; a missing eval is D7 only. Double deductions make two judges disagree about the same flaw.
6. **Compute** `total`, `max_total`, `percent` (round to one decimal) and `grade`.
7. **Emit the output** as the contract below requires.

If a file you need cannot be read, say so in a finding (severity high), score that dimension from the evidence you do have, and never guess its content.

When asked to compare or audit several skills, run steps 2 to 6 for each skill independently; never score one relative to another. Only the ranking compares them.

## Output contract

First matching rule wins.

1. **The prompt comes from `references/judge-prompt.md`, or the request asks for only the verdict or JSON line.** Print only the verdict JSON, one object per line, one line per skill, in the listed order. No Markdown, no code fence, no commentary before or after.
2. **Otherwise, one skill** (for example "judge this SKILL.md"): print a short summary and then the verdict:
   - one line with percent and grade;
   - a per-dimension score table (`id`, `name`, `score`, `max`);
   - the top three findings, ordered by points lost, then severity, then dimension, file and line, each with its fix;
   - the same verdict as one JSON object on a single line in a fenced `json` block, last in the output.
3. **Otherwise, several skills or a comparison:**
   - one short summary per skill (percent, grade, top finding with its fix), in the listed order;
   - then a ranking table sorted by percent, highest first: skill, percent, grade, largest per-dimension gaps (for example `D7 -11, D3 -3`);
   - then one fenced `json` block, last in the output, holding one verdict per line in the listed order, not the ranked order.

## Verdict JSON

```json
{"skill":"pdf-form-filler","judge":"direct","rubric_version":4,"spec_sha":"<40 hex from rubric.md>","scores":{"D1":16,"D2":15,"D3":15,"D4":14,"D5":15,"D6":15,"D7":3,"D8":15},"max":{"D1":20,"D2":15,"D3":15,"D4":15,"D5":15,"D6":15,"D7":15,"D8":15},"total":108,"max_total":125,"percent":86.4,"grade":"B","findings":[{"id":"D1-1","dimension":"D1","severity":"low","file":"skills/pdf-form-filler/SKILL.md","line":12,"evidence":"Explains what a PDF AcroForm is","fix":"Delete the definition; the model knows it"},{"id":"D4-1","dimension":"D4","severity":"low","file":"skills/pdf-form-filler/SKILL.md","line":3,"evidence":"Description has no keyword for flattening","fix":"Add 'flatten' to the description"},{"id":"D7-1","dimension":"D7","severity":"high","file":"skills/pdf-form-filler/SKILL.md","line":null,"evidence":"No evals/ directory in the supplied files","fix":"Add evals/evals.json with 3 realistic prompts and verifiable assertions"}]}
```

Rules, enforced by a schema in `references/verdict.schema.json`:

- `skill` is the target directory name; `judge` is the slug the prompt gives (use `direct` when none).
- `rubric_version`, `spec_sha` and every value in `max` are copied from `references/rubric.md`; never recomputed or remembered. `scores` and `max` hold exactly `D1`..`D8`, integers; each score is between 0 and its max.
- `total` is the sum of `scores`, `max_total` the sum of `max`, `percent` is `round(total / max_total * 100, 1)`.
- `grade` from `percent`: A at 90 or more, B at 80, C at 70, D at 60, otherwise F.
- Each finding has a unique non-empty `id` (convention `D4-1`), a `dimension`, a `severity` of `critical`, `high`, `medium` or `low`, a `file` path relative to the root the request gives (no root: the path as the user wrote it; pasted content: `SKILL.md`), `line` as an integer of 1 or more or `null` when no line applies, quoted `evidence`, and a concrete `fix`. All four text fields are non-empty strings.
- Every score below its max has at least one finding for that dimension.

## Gotchas

- **`SKILL.md.txt` under `evals/files/`** is a fixture judged as if it were `SKILL.md`; the suffix only stops harnesses from loading decoys. It is not a skill, so its file name is never a finding.
- **Rubric exemptions are never findings**: the allowlisted Claude Code fields (`user-invocable`, `disable-model-invocation`, `argument-hint`), mandatory reads, repository-required files.
- **`findings[].file` is relative to the root the prompt gives**, not to the skill and not absolute. Findings that use different path forms for the same file are not deduplicated.
- **Trigger guidance only in the body is a D4 finding.** The body is invisible until the skill has already triggered.

## NEVER do when evaluating

- NEVER reward polish, length or self-praise ("battle-tested", "comprehensive"): formatting and size are not knowledge, and a 43-line skill can outperform a 500-line one. Score what the files show.
- NEVER forgive basics as "helpful context" or treat every procedure as valuable: if the model knows it, it is redundant; separate domain sequences from generic ones.
- NEVER invent facts about files you have not read, and NEVER mark a score up to compensate for something you could not verify: the author acts on your evidence.
- NEVER modify the skill you are judging: this skill reads and reports, and a silent edit invalidates the verdict.

## Calibration

When two scores seem equally defensible, pick the lower and write the finding; a finding with a concrete fix is worth more to the author than a point.
