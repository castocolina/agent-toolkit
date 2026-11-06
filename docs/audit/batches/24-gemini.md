# Batch 24

## gemini (skill)

### gemini#D8-1
- severity: medium
- dimension: D8
- location: skills/gemini/SKILL.md:36
- fix: Pass the supplied plan text directly, copy it into an authorized scoped workspace, or explicitly include its containing directory after checking the expanded access boundary. Correct both plan-review examples.

### gemini#D7-1
- severity: medium
- dimension: D7
- location: skills/gemini/evals/evals.json:7
- fix: Make proposal-only intent explicit in proposal tests. Add fixtures for successful and failed CLI responses, timeout handling, and unsupported findings, with assertions distinguishing verified results from incomplete or rejected analysis.

### gemini#D7-2
- severity: low
- dimension: D7
- location: skills/gemini/evals/trigger-queries.json:3
- fix: Replace some explicit-name positives with realistic second-opinion and big-context requests that do not name Gemini, including a contextual multi-directory request.

### gemini#D7-1
- severity: medium
- dimension: D7
- location: skills/gemini/evals/evals.json:3
- fix: Vary the eval set: two prompts share near-identical yolo phrasing and all three are command-proposal tasks; add one eval that tests claim verification (workflow step 4) and one casual phrasing

### gemini#D8-1
- severity: medium
- dimension: D8
- location: skills/gemini/SKILL.md:28
- fix: Enumerate the valid approval-mode values (default, plan, auto_edit, yolo) with one-line meaning and a default, so the placeholder is fillable without guessing

### gemini#D1-1
- severity: medium
- dimension: D1
- location: skills/gemini/SKILL.md:21
- fix: Consolidate directory-access guidance into one authoritative rule and shorten familiar execution/reporting advice. Preserve the non-interactive approval trap, owned-process cleanup, and source-verification requirements.

### gemini#D6-1
- severity: medium
- dimension: D6
- location: skills/gemini/SKILL.md:28
- fix: Use an explicit escalation bound such as timeout --signal=TERM --kill-after=10s 300, and document owned-process-group handling for background execution.

### gemini#D1-1
- severity: low
- dimension: D1
- location: skills/gemini/SKILL.md:12
- fix: Replace the generic exclusion with concrete items (.env, key/token files, credentials dirs) and a quick grep the agent runs before sending context

### gemini#D1-2
- severity: low
- dimension: D1
- location: skills/gemini/SKILL.md:20
- fix: State the --include-directories rule once (here) and cross-reference from step 1 instead of restating it in both workflow steps

### gemini#D2-1
- severity: low
- dimension: D2
- location: skills/gemini/SKILL.md:17
- fix: Merge the overlapping steps 4 and 5 (substantiate claims / report verified findings) into one verify-then-report step with an explicit go/no-go gate

### gemini#D3-1
- severity: low
- dimension: D3
- location: skills/gemini/SKILL.md:10
- fix: Extract a Gotchas list of CLI-specific traps with reasons (approval-mode default hang, pkill blast radius, partial output mistaken for results) instead of burying them in prose bullets

### gemini#D6-1
- severity: low
- dimension: D6
- location: skills/gemini/SKILL.md:14
- fix: State the default bound (timeout 300 as in the command shape) and when to raise it, so the timeout is a default rather than a per-run guess
