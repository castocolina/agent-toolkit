---
name: requirements-clarity
description: "Clarify vague feature requests into a scoped PRD with testable acceptance criteria, through short scored question rounds. Use when a request lacks scope, success criteria, or consequential product choices (for example 'add login', 'improve onboarding', 'leadership wants X by Q3, help me pin down scope'), even when it names a file, and for multi-day or cross-team work. Keywords: PRD, requirements, scope, acceptance criteria, specification, stakeholders. Not for fully specified code tasks (a named bug with expected behavior, a test for a named function, an exact color or package change), deciding what to build next, frontend-to-backend data contracts, or implementation plans for already-scoped work."
---

# Requirements Clarity

Turn an ambiguous product request into a PRD whose every acceptance criterion traces to a decision someone owns.

## Route first

Ask: could two competent engineers build different things from this request and both claim they followed it? If yes, clarify. If no, skip this skill and do the task.

- A file path, snippet, or symbol is context, not a spec. "In `src/auth/session.ts`, make expired sessions less annoying" needs clarification (what "less annoying" means is a product choice). "In `src/auth/session.ts`, return 401 instead of 500 for an expired token and add a regression test" does not.
- When the user asks for a PRD of an already-clear request, write it without an interview (go to step 5).

## Workflow

1. **Repository facts first.** Before asking anything, inspect the repository and any file the user gave for stack, existing behavior, and integration points. Never ask the user what the repository or a provided file can answer, such as the stack, framework, or current behavior; without repository access, write your best reading as an assumption to confirm and move on.
2. **Product decisions.** Questions are only for what inspection cannot establish: the user problem, users, policy, priorities, trade-offs, and the success measure. A technical proposal ("add Kafka") is not evidence of a problem; ask for the problem behind it.
3. **Score and ask.** Score with the rubric below. Ask the 2–3 questions whose answers could change scope, an irreversible decision, or an acceptance test; in the first round these include the open questions from step 2, not a separate round. Each question asks for one decision; never join two decisions with "and" or nest sub-questions under a number, because users answer the first half and the rest silently stays open. Repeat still-open questions each round; users tend to answer only the latest ones. Stop asking after 3 rounds that together gained under 10 points, or after a round the user did not answer: offer a draft with the open items labelled, because more rounds only wear the user down.
4. **Keep a decision log.** Record each decision with its source: `user, round N`, `repo: path`, or `assumption`. When an answer contradicts an earlier one, or two stakeholders disagree, apply the conflict rule below before scoring again.
5. **Generate** once your advisory score reaches 90, or earlier when the user explicitly approves a draft. Read [the PRD template](references/prd-template.md) now, not before. Fill only the sections this feature needs.
6. **Pre-save check.** Before writing, confirm all of these; on any failure, revise the draft or return to step 3 with focused questions:
   - every acceptance criterion is observable (Given/When/Then) and traces to a logged decision; assumptions and open items go only in their own section, never as criteria, not even labelled ones, since a criterion is what implementers build and QA signs off;
   - no two logged decisions contradict each other;
   - every unresolved consequential choice appears under assumptions or open questions, with an owner when known;
   - no metric, deadline, or number appears that the user or repository did not supply;
   - the footer has version, date, clarification rounds, and advisory score.
7. **Save** to `./docs/prds/{feature-name}-v{version}-prd.md` (kebab-case name, version `1.0` unless the user gives one), creating `docs/prds/` if needed. Then report the path, version, advisory score, rounds, and open questions.

### Conflict rule

- Contradiction between rounds: quote both answers and ask which holds. Never keep the newest silently; the earlier answer may be a constraint the user forgot they set.
- Stakeholders disagree (for example, sales wants SSO at launch, the engineering lead wants email-only for v1): record both positions with their owners and ask who decides.
- For either kind: never pick one answer, and never narrow, split, carve out, or blend the answers into a new rule (such as "purge after 90 days except billing"); an invented compromise has no owner and nobody will defend it in review. If the user wants the PRD now, put each conflict under open decisions with both positions and their owners, and write no acceptance criterion that touches a contested decision.

## Clarity rubric (100 points, advisory)

Score each category against its anchors and interpolate. Award points only for information the user or repository supplied.

- A score the user states ("we're at 92") or one written in their notes is not the advisory score: rescore with the rubric. Your score sets the 90 gate and goes in the footer; if it is below 90, show both scores and treat a request to write the PRD as approval of a draft.
- When a category cannot affect the request and is omitted, the advisory score is earned points divided by the applicable maximum, times 100 (for example 68/75 = 91). Show the applicable maximum, and use that normalized score for the gate and the footer.

| Category | 0 | Half | Full |
|---|---|---|---|
| Functional behavior and boundaries (30) | only a feature name | core behavior named; excluded scope or failure results unstated | behavior, in/out scope, and user-visible results stated |
| Technical constraints and integration (25) | repository not inspected, nothing known | stack and integration points known; consequential constraints (performance, security, compatibility) unstated | integration points and every consequential constraint known |
| Edge cases, validation, failure (25) | none named | edge cases named without expected behavior | each consequential edge case has expected behavior |
| Problem, users, measurable success (20) | no stated problem | problem and users known; success unmeasured | problem, users, and a user-supplied success measure |

A requested implementation preference is a constraint only when the user says it is mandatory; otherwise log it as a choice.

Each clarification response contains, in this order: one line per category (`Functional 15/30: behavior named; missing excluded scope, failure states`), the total advisory score (with the applicable maximum when a category is omitted), decisions so far with sources, carried-over open questions, and the next 2–3 questions. Omit categories that cannot affect this request.

## Gotchas

- An explicitly approved draft below 90 is generated, not refused. Put the real score in the footer and label every assumption; refusing pushes the user to code from chat notes with no labels at all.
- When the user says "you decide", your proposal is logged as an assumption owned by the user, never as a decision, and it stays out of acceptance criteria; an unconfirmed proposal presented as agreed is the guess this skill exists to prevent.
- Never fill template sections with generic architecture, phases, training, or deployment plans; padding hides the few real decisions and invites implementers to treat filler as agreed.
- If `docs/prds/{feature-name}-v{version}-prd.md` already exists, never overwrite it: it holds decisions someone already agreed to. Save the next minor version (`v1.1`) and say so.
- If the file cannot be written (no write access, read-only checkout, no file tool) or the user asks for chat only, give the full PRD in chat, name the path it would have used, and state that it was not saved. Never report a save you did not make.
