# Skill Judge

Scores an Agent Skill against the pinned [Agent Skills](https://github.com/agentskills/agentskills) specification and best practices. It produces a percentage, an A-F grade, per-dimension scores and concrete fixes, either as a readable summary (direct use) or as machine-readable JSON-lines verdicts (driven by a prompt or a pipeline).

## Purpose

Most skills waste tokens on knowledge the model and its harness already have. Skill Judge measures the knowledge delta:

> Good skill = expert-only knowledge - what the model already knows

It also checks the structural things that stop a skill from being used: a vague description, an oversized `SKILL.md`, unloaded references, missing tests.

## When to Use

- Review a skill before publishing.
- Audit existing skills against one consistent rubric.
- Get actionable fixes for a `SKILL.md`.
- Compare skills by percentage.

Trigger phrases: "judge this skill", "review my SKILL.md", "audit this skill", "score this skill", "how can I improve this skill?".

## How It Works

1. The skill reads `references/rubric.md` (rubric v4) and every pinned spec file the rubric cites, in full. These reads are mandatory on every run.
2. It reads the target `SKILL.md` and, when a dimension needs them, `evals/` (inputs in `evals/files/`), `scripts/`, the repository's `tests/skills/<name>/` (script tests, not shipped with the skill) and referenced files.
3. It scores eight dimensions with integer bands and records a finding, with evidence and a fix, for every score below its maximum.
4. It computes the percentage and grade and prints the output.

### Rubric v4: eight dimensions, 125 points

| Dimension | Max | What it measures |
|-----------|-----|------------------|
| D1 Knowledge Delta | 20 | Expert knowledge versus what models and current harnesses already do |
| D2 Mindset, Procedures and Patterns | 15 | Thinking patterns and domain procedures (up to 11), fit to an established design pattern (up to 4) |
| D3 Anti-Pattern Quality | 15 | Specific NEVER items and gotchas, with reasons |
| D4 Specification Compliance | 15 | Frontmatter validity and a description with WHAT, WHEN and keywords |
| D5 Progressive Disclosure | 15 | Layering, size, conditional loading of optional references |
| D6 Freedom Calibration | 15 | Specificity matched to the fragility of the task |
| D7 Tests and Evals | 15 | Output evals, trigger queries, a runnable test when `scripts/` exists |
| D8 Practical Usability | 15 | Decision trees, working examples, fallbacks, edge cases |

Files the repository requires (`README.md`, `evals/`, bundled `references/` and `SOURCE.json`) are never deductions. Only redundant extras such as `CHANGELOG.md` are.

### Grades

Grades use the percentage of the total, so the total can change between rubric versions.

| Grade | Percentage |
|-------|------------|
| A | 90 or more |
| B | 80 to 89.9 |
| C | 70 to 79.9 |
| D | 60 to 69.9 |
| F | below 60 |

## Output

**Direct use** ("judge this SKILL.md"): a short summary (percent and grade, a per-dimension table, the top three findings with fixes) followed by the verdict as one JSON line in a fenced `json` block.

**Several skills or a comparison**: one short summary per skill, a ranking table (skill, percent, grade, largest per-dimension gaps), then one fenced `json` block with one verdict per line in the listed order.

**Driven by a prompt, or when only the verdict is requested**: one JSON object per line and nothing else. The shape is defined by `references/verdict.schema.json`:

```json
{"skill":"my-skill","judge":"direct","rubric_version":4,"spec_sha":"<40 hex>","scores":{"D1":16,"D2":15,"D3":15,"D4":14,"D5":15,"D6":15,"D7":3,"D8":15},"max":{"D1":20,"D2":15,"D3":15,"D4":15,"D5":15,"D6":15,"D7":15,"D8":15},"total":108,"max_total":125,"percent":86.4,"grade":"B","findings":[{"id":"D1-1","dimension":"D1","severity":"low","file":"skills/my-skill/SKILL.md","line":12,"evidence":"Explains what a PDF AcroForm is","fix":"Delete the definition"},{"id":"D4-1","dimension":"D4","severity":"low","file":"skills/my-skill/SKILL.md","line":3,"evidence":"No keyword for flattening","fix":"Add it to the description"},{"id":"D7-1","dimension":"D7","severity":"high","file":"skills/my-skill/SKILL.md","line":null,"evidence":"No evals/ directory","fix":"Add evals/evals.json"}]}
```

## Bundled files

The skill reads these at run time.

| Path | Purpose |
|------|---------|
| `references/rubric.md` | Rubric v4: version, spec commit, dimension table, scoring criteria |
| `references/verdict.schema.json` | JSON Schema for one verdict line |
| `references/judge-prompt.md` | Prompt template for judges run by a pipeline, with `{ROOT}`, `{SKILLS}` and `{JUDGE}` placeholders |
| `references/agentskills/` | Verbatim copies of the Agent Skills docs the rubric cites, pinned by commit in `SOURCE.json` (CC-BY-4.0) |

`evals/` (output evals, trigger queries and eval inputs) is for repository development and is not shipped in `dist/`.

## Usage Examples

```
Judge the skill at skills/my-new-skill
```

```
Compare the quality of skills/skill-a and skills/skill-b
```

```
How can I improve the knowledge delta in my skill?
```

## Best Practices

**Do:** check the description first; ask "does the model already know this?" for every section; look for specific anti-patterns with non-obvious reasons; mentally run the decision trees.

**Never:** reward polish, length or self-praise; forgive basics as "helpful context"; deduct for files the repository requires.

## Prerequisites

None. The skill is self-contained: the rubric and the spec copies it needs ship in `references/`.
