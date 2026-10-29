---
name: requirements-clarity
description: "Clarify vague feature requests into scoped product requirements with measurable acceptance criteria. Use when a request lacks scope, success criteria, or consequential constraints (for example, ‘add login’ or ‘improve onboarding’), especially for multi-day work or cross-team dependencies. Keywords: PRD, requirements, scope, acceptance criteria, specification. Not for fully specified code tasks such as adding a unit test to a named function, setting up React from an exact package list, changing a specified button color, or fixing reproducible bugs."
---

# Requirements Clarity

Use this for ambiguous product work, not as a mandatory interview before every code change. A file path, snippet, or existing symbol is context—not proof that behavior and acceptance criteria are specified. Bypass clarification only when the desired behavior and acceptance criteria are clear enough to implement or verify.

## Workflow

1. **Establish the outcome.** Ask what user problem or outcome justifies the request (YAGNI), then whether an existing capability or smaller change would solve it (KISS). Record the answers; do not infer business value from a technical proposal.
2. **Separate unknowns.** Inspect the repository for technical facts, conventions, existing behavior, and integration points. Ask the user about product choices that code cannot reveal: users, policy, priorities, acceptable trade-offs, and success measures. Never ask the user to supply facts discoverable in the repo.
3. **Rank gaps.** Score clarity with the rubric below. Ask 2–3 highest-impact questions per round, prioritizing answers that could change scope, an irreversible decision, or acceptance tests. Restate still-open questions each round; users may answer only the latest.
4. **Keep the score advisory.** Normally generate after reaching 90/100. The user may approve an earlier draft; mark its score, assumptions, open questions, and owners explicitly. Scale the PRD to the feature—do not invent architecture, training, deployment, or business metrics to fill a template.
5. **Write the PRD** to `./docs/prds/{feature-name}-v{version}-prd.md`; create the directory if needed. Use kebab-case feature names and version `1.0` unless the user specifies another version. Load [the PRD template](references/prd-template.md) when generating the document. If the user requests chat-only output or file writing is unavailable, provide it in chat and state that it was not saved.

A useful clarification response contains: current advisory score, known decisions, consequential unknowns, and the next 2–3 questions. Be concise; omit categories that do not affect this request.

## Clarity rubric (100 points)

- Functional behavior and boundaries: 30
- Technical constraints and integration points: 25
- Edge cases, validation, and failure behavior: 25
- Problem, users, and measurable success: 20

Award points only for supported information. A requested implementation preference is not automatically a requirement; identify whether it is a constraint or a choice. Never invent target metrics to make the score or PRD look complete.

## Gotchas

- Do not treat a named file or code snippet as a clear product requirement; ambiguous behavior can still need clarification.
- Do not ask for stack or repository facts before inspecting available files; this creates unnecessary interviews and false uncertainty.
- Do not present guesses as user-approved decisions. Record assumptions and unresolved decisions so downstream implementers can distinguish facts from proposals.
- Do not let the 90-point target block an explicitly approved early draft; premature certainty ossifies guesses, so label uncertainty visibly.

## Output

Write a focused PRD with problem/users, behavior and boundaries, decisions/constraints, measurable acceptance criteria, and risks or delivery notes only where relevant. Preserve agreed decisions and identify open questions rather than fabricating completeness. Include version, date, clarification rounds, and advisory score.
