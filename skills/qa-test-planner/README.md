# QA Test Planner

An agent skill for manual QA deliverables: test plans, executable test cases, regression and smoke suites, Figma design-validation checklists, and bug reports. Every case traces to a requirement and a risk, expected results are observable, and facts nobody supplied are written as `Unknown` instead of guessed.

The routing table, plan branch, oracle table, priority precedence, gotchas and pre-delivery checklist live in [SKILL.md](SKILL.md); this file only covers setup.

## Activation

The skill triggers only when called by name:

```
/qa-test-planner plan the password-reset release: links expire after 30 minutes and work once
```

General testing requests without the name do not load it.

## Installation

**Claude Code:**

```bash
cp -r skills/qa-test-planner ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

## Scripts

Two optional generators write one Markdown file per run: `scripts/create_bug_report.sh` and `scripts/generate_test_cases.sh`. Pass the fields as flags for a non-interactive run, or no field flag to be asked for each field. Each prints one JSON line on stdout (`{"status":"created","id":...,"file":...}`); run either with `--help` for flags and exit codes. Tests live in `tests/skills/qa-test-planner/`.

## File Structure

```
qa-test-planner/
├── SKILL.md                         # Agent instructions
├── README.md                        # This file
├── references/
│   ├── test_case_templates.md       # Case format and per-type fields
│   ├── bug_report_templates.md      # Report format, severity and priority
│   ├── regression_testing.md        # Suite selection, release decision, run report
│   └── figma_validation.md          # Design comparison conditions and records
├── scripts/
│   ├── create_bug_report.sh
│   └── generate_test_cases.sh
└── evals/                           # Output evals, trigger queries, fixtures
```
