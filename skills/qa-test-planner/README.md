# QA Test Planner

A Claude Code skill for creating risk-traceable manual QA plans, test cases, regression suites, Figma validation checklists, and bug reports when explicitly invoked by name.

## Purpose

The QA Test Planner creates manual QA deliverables from requirements and evidence, with explicit coverage, risk, and execution criteria.

## When to Use This Skill

Use the QA Test Planner skill when you need to:

- Create a comprehensive test plan for a new feature or release
- Generate manual test cases with step-by-step instructions
- Build regression test suites (smoke, targeted, or full)
- Validate UI implementation against Figma designs
- Document bugs with clear reproduction steps


### Activation

This skill uses **explicit triggering** - it must be called by name:

```
/qa-test-planner
qa-test-planner
use the skill qa-test-planner
```

## How It Works

The QA Test Planner follows a three-phase workflow:

### 1. Identify the deliverable
Choose a test plan, manual cases, regression/smoke suite, Figma comparison, or bug report based on the explicit request.

### 2. Build from evidence
Map requirements and risks to observable pass/fail criteria, executable cases, and test data. State uncovered requirements and blocked tests.

### 3. Review
Check that cases are standalone, reproducible, and prioritized by risk.

## Key Features

### 1. Test Plan Generation
Creates complete test plans including:
- Executive summary with objectives and risks
- Clear scope definition (in-scope and out-of-scope)
- Testing strategy and approach
- Environment requirements
- Entry and exit criteria
- Risk assessment with mitigations
- Timeline and deliverables

### 2. Manual Test Case Creation
Generates structured test cases with:
- Step-by-step test instructions
- Expected results for each step
- Preconditions and test data requirements
- Priority and severity assignments
- Post-conditions and cleanup steps
- Edge cases and variations

### 3. Regression Test Suites
Builds prioritized regression and smoke suites based on changed code, critical journeys, failure impact, and execution cost.

### 4. Figma Design Validation
When Figma MCP is available, compare the matching frame and implementation context. Otherwise, request screenshots or specifications and state the limitation.

### 5. Bug Report Documentation
Generates structured bug reports with:
- Clear reproduction steps
- Environment details (OS, browser, device, build)
- Expected vs actual behavior
- Visual evidence (screenshots, videos, console logs)
- Severity and priority classification
- Impact assessment and workarounds

## Usage Examples

### Example 1: Create Test Plan

**Input:**
```
/qa-test-planner
Create a test plan for the user authentication feature
```

**Output:**
A complete test plan document including:
- Testing objectives for login, registration, password reset
- Scope definition (web and mobile apps)
- Test strategy (manual, exploratory, security testing)
- Environment requirements (browsers, devices, test data)
- Entry/exit criteria with measurable thresholds
- Risk assessment (security vulnerabilities, third-party auth)
- Timeline with milestones

### Example 2: Generate Test Cases

**Input:**
```
/qa-test-planner
Generate 5 manual test cases for the checkout flow
```

**Output:**
Five numbered test cases covering:
1. Valid checkout with credit card
2. Invalid credit card handling
3. Empty cart checkout attempt
4. Promo code application
5. Guest vs. logged-in checkout

Each includes preconditions, step-by-step instructions, expected results, test data, and edge cases.

### Example 3: Build Regression Suite

**Input:**
```
/qa-test-planner
Build a smoke test suite for the payment module
```

**Output:**
A prioritized smoke suite that focuses on critical journeys and states its pass/fail criteria, dependencies, and any coverage gaps.

### Example 4: Validate Against Figma

**Input:**
```
/qa-test-planner
Compare the login page against the Figma design at [Figma URL]
```

**Output:**
A validation checklist comparing:
- Button dimensions, colors, and states
- Typography (fonts, sizes, weights)
- Spacing and layout
- Responsive behavior
- Interactive states (hover, focus, disabled)

Plus test cases to verify each element and document discrepancies.

### Example 5: Create Bug Report

**Input:**
```
/qa-test-planner
Create a bug report for: Form validation doesn't prevent submission when email field is empty
```

**Output:**
A structured bug report with:
- Clear title: "[Contact Form] Submission allowed with empty email field"
- Severity: High (data quality issue)
- Reproduction steps (numbered, specific actions)
- Expected behavior: Form submission blocked with error message
- Actual behavior: Form submits without email
- Environment details
- Visual evidence placeholder
- Impact assessment

## Interactive Scripts

Optional local document generators are available; they are not test automation. Inspect before use, and do not invoke them in a non-interactive session:

### Generate Test Cases Script
```bash
./scripts/generate_test_cases.sh
```
Prompts for a single test case: ID and title, priority (P0-P3), test type, estimated time, objective, preconditions, steps with expected results, and test data. It writes one test-case file per run.

### Create Bug Report Script
```bash
./scripts/create_bug_report.sh
```
Prompts for:
- Bug title
- Severity and priority
- Reproduction steps
- Environment details
- Expected vs actual behavior

## Reference Documentation

Use only these shipped references for additional detail:

- `references/test_case_templates.md` - Manual test case formats
- `references/bug_report_templates.md` - Bug report formats
- `references/regression_testing.md` - Regression suite selection and gating
- `references/figma_validation.md` - Design comparison guidance

## Quality Standards

### Test Plan Checklist
- Scope clearly defined (in/out)
- Entry/exit criteria specified
- Risks identified with mitigations
- Timeline is realistic and achievable

### Test Case Checklist
- Each step has an expected result
- Preconditions documented
- Test data available or specified
- Priority assigned (P0-P3)
- Edge cases included

### Bug Report Checklist
- Reproducible steps provided
- Environment documented completely
- Screenshots or evidence attached
- Severity and priority set appropriately

## Anti-Patterns to Avoid

The skill helps you avoid common testing mistakes:

| Avoid | Why It's Bad | What to Do Instead |
|-------|--------------|-------------------|
| Vague test steps | Can't reproduce consistently | Use specific actions with expected results |
| Missing preconditions | Tests fail unexpectedly | Document all setup requirements |
| No test data | Testers get blocked | Provide sample data or generation instructions |
| Generic bug titles | Hard to track and prioritize | Be specific: "[Feature] issue when [action]" |
| Skipping edge cases | Miss critical bugs | Include boundary values, nulls, empty states |

## Figma Design Validation

Use Figma MCP only when it is available. Confirm the frame/version, viewport, theme, and device-pixel ratio before assessing visual differences. Without MCP access, request screenshots or specifications and state the limitation.

## Best Practices

### Test Case Writing
- Be specific and unambiguous
- Include expected results for each step
- Test one thing per test case
- Use consistent naming conventions (TC-MODULE-###)
- Keep test cases maintainable (update as features change)

### Bug Reporting
- Provide clear reproduction steps anyone can follow
- Include screenshots, videos, or console logs
- Specify exact environment details
- Describe impact on users
- Link to Figma designs for UI bugs

### Regression Testing
- Maintain regression suite regularly
- Prioritize critical paths
- Run smoke tests frequently (daily/per build)
- Update suite after each release
- Make uncovered requirements and blocked tests explicit

## Skill Structure

```
qa-test-planner/
├── README.md
├── SKILL.md
├── references/
│   ├── bug_report_templates.md
│   ├── figma_validation.md
│   ├── regression_testing.md
│   └── test_case_templates.md
└── scripts/
    ├── create_bug_report.sh
    └── generate_test_cases.sh
```

## Output Formats

All deliverables are generated in **Markdown format** for easy copy-paste into:
- Jira, Linear, GitHub Issues
- Confluence, Notion
- TestRail, Zephyr
- Google Docs, Word

The structured format ensures consistency across your team and makes test documentation searchable and maintainable.

## Time Savings

The skill does not prescribe fixed authoring-time or pass-rate targets. Set release gates from critical requirements, unresolved risk, blocked coverage, and stakeholder acceptance.

## Getting Started

1. Activate the skill: `/qa-test-planner`
2. Describe what you need (test plan, test cases, bug report, etc.)
3. Review and customize the generated documentation
4. Copy to your tracking system (Jira, Linear, etc.)

## Support

See `SKILL.md` for the workflow and safeguards. Use the reference files listed above for deliverable-specific formats and guidance.

---
