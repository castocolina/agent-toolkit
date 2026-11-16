# Batch 18

## requirements-clarity (skill)

### requirements-clarity#D7-1
- severity: medium
- dimension: D7
- location: skills/requirements-clarity/evals/evals.json:22
- fix: Add end-to-end cases for a clarified feature and an explicitly approved low-score draft. Assert the PRD path/version, preserved decisions, testable acceptance criteria, labelled assumptions and open questions, and actual artifact creation; include a chat-only variant.

### requirements-clarity#D7-2
- severity: medium
- dimension: D7
- location: skills/requirements-clarity/evals/trigger-queries.json:3
- fix: Replace several stubs with realistic requests containing repository paths, existing behavior, stakeholder context, and incomplete product choices. Pair an ambiguous request naming a file with a fully specified change in that same file to test that paths alone do not determine routing.

### requirements-clarity#D8-1
- severity: medium
- dimension: D8
- location: skills/requirements-clarity/SKILL.md:16
- fix: Before saving, check each acceptance criterion against a supported decision, detect contradictions between rounds, and verify that unresolved consequential choices remain visibly labelled. Revise or return to focused clarification when that check fails.

### requirements-clarity#D7-1
- severity: medium
- dimension: D7
- location: skills/requirements-clarity/evals/trigger-queries.json:11
- fix: Rewrite 4-6 queries as full realistic user messages with context and casual phrasing, e.g. 'leadership wants better onboarding by Q3 and eng keeps asking me what that means - help me pin down scope', per the realism guidance (paths, personal context, varied formality)

### requirements-clarity#D8-1
- severity: medium
- dimension: D8
- location: skills/requirements-clarity/SKILL.md:27
- fix: Add per-category score anchors (e.g. 'Functional 15/30 = behavior named but boundaries and failure states unspecified') or require each clarification response to list per-category earned and lost points so two agents cannot score the same brief 55 and 75 while both following the skill

### requirements-clarity#D1-1
- severity: medium
- dimension: D1
- location: skills/requirements-clarity/SKILL.md:12
- fix: Compress routine requirements-gathering and PRD-inventory guidance. Retain the repository-facts/product-decisions distinction and advisory-score override; add worked decisions for conflicting requirements or stakeholder priorities instead of repeating familiar principles.

### requirements-clarity#D1-1
- severity: low
- dimension: D1
- location: skills/requirements-clarity/SKILL.md:12
- fix: Drop the YAGNI/KISS acronym labels and keep only the non-obvious rule that follows them ('do not infer business value from a technical proposal'); naming the frameworks is activation content the model already applies

### requirements-clarity#D2-1
- severity: low
- dimension: D2
- location: skills/requirements-clarity/SKILL.md:38
- fix: Replace the Output section with a pointer to the already-loaded template plus the mandatory footer ('Generate from references/prd-template.md; always fill version, date, clarification rounds, advisory score') and delete the duplicated section list

### requirements-clarity#D3-1
- severity: medium
- dimension: D3
- location: skills/requirements-clarity/SKILL.md:31
- fix: Add environment-specific gotchas from real runs, e.g. 'If answers conflict between rounds, surface the conflict and re-confirm the earlier decision instead of silently keeping the newest' and what to do when docs/prds/ cannot be created
