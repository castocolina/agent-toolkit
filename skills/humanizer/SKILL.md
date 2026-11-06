---
name: humanizer
metadata:
  version: "2.1.1"
description: Edit existing drafts to remove formulaic AI-like prose, promotional puffery and hype, vague attributions, inflated significance and repetitive sentence patterns while preserving facts, quotations, author voice and house style. Use when a draft sounds robotic, generic, salesy or breathless, or the user asks to humanize text, tone down hype, make copy more natural or factual, or remove AI writing patterns, chatbot phrasing, clichés or em-dash overuse, even without mentioning AI. Not for authorship detection, factual research, translation, spelling-only proofreading, or writing from scratch.
allowed-tools: Read Write Edit Grep Glob AskUserQuestion
---

# Humanizer

Edit existing prose, not its evidence. AI-writing cues are symptoms, not proof of authorship and not the defect itself: human editorials, blogs and marketing copy share them. Swapping cue words while the unsupported claim stays only hides the problem, so fix what the cue points at (a vague source, an inflated claim, an empty sentence) or leave it alone.

## Workflow

1. Brief: take audience, genre, stance, house style and edit depth from the request and source; ask only for missing information that changes the edit. When depth is unspecified, default to the minimal consequential edit and state that scope in the change note.
2. Protect: mark quotations, exact-match text and fixed wording (see Never alter evidence) before editing anything.
3. Diagnose in priority order: evidence risks (vague attribution, unsupported claims) first, then inflation and promotion, then structure, then vocabulary and mechanics. Polishing the mechanics of a sentence whose claim is unsupported cements the claim. Gate: count distinct cues per paragraph; with fewer than three, fix only the evidence and inflation cues and skip the style pass.
4. Edit, then run the Deliver check against the original.

Preserve the author's register. Formal prose need not gain first person or contractions; casual prose may keep deliberate em-dash rhythm, fragments and humor. If the user asks to keep a pattern, exempt it and say so in the change note.

## Core diagnostics

- **Evidence:** claims credited to "experts", "observers" or "several sources" when one is cited; importance proved by describing coverage instead of its content ("profiled in trade publications", "active social media presence"); "records list her as" or "associated with" standing in for the plain relation (founder, CEO). Name the source or relation only when the supplied text gives it; otherwise cut the claim to what is supported.
- **Inflation:** pivotal, testament, turning point, broader trend, "sparked debate", "left a lasting mark", or a preamble that concedes the topic is minor and then claims importance anyway. Keep only significance the text supports.
- **Superficial analysis:** trailing participles ("highlighting the importance", "ensuring a seamless experience") that restate the previous sentence, and a gloss pinned on a named source ("the critic highlighted its lasting influence") that the source does not support. Keep causal details that add information.
- **Promotion:** seamless, powerful, innovative, vibrant, nestled, stacked praise. Blatant press-release tone is mostly an older-model (2023-2025) signal; current output promotes through content (award and coverage lists). Replace only unsupported evaluation; keep sourced, intentional positioning.
- **Structure:** copula avoidance ("serves as", "stands as", "features", "boasts" where is/has fits; one of the most reliable current cues, so restore the plain verb); negative parallelism ("not just X but Y", "it's not X, it's Y", "no X, no Y, just Z", and reversed "Y rather than X"); a rule of three that makes thin analysis look thorough; the outline ending "Despite its strengths, X faces challenges..." followed by an upbeat future (the formula is the cue, not a mention of challenges). Fix only where the pattern blurs the argument or repeats.

Not tells on their own, so never edit for them alone: perfect grammar, formal or academic register, bland prose, mixed registers, transition words ("Additionally", "Moreover") in isolation, or one or two listed "AI words". Never replace every em dash or flagged word mechanically: uniform 8-20-word sentences with dense commas and periods are themselves a current cue, so vary the fix or keep the original.

Load `references/pattern-catalog.md` when the text shows chatbot correspondence, disclaimers, hedging, filler, vocabulary clusters, em dashes or other mechanics, or when the core diagnostics find nothing and the text still reads machine-made; it labels which cues are current and which are older-model. Do not load it for a narrow edit whose issue is already listed above.

## Never alter evidence

- Never silently rewrite direct quotations or primary-source excerpts: a reworded quote puts words in someone's mouth. Flag them or ask permission.
- Never humanize code, API identifiers, schema keys, error strings or other exact-match text: grep, tests, API contracts and search match the literal string, so even a case or quote-style change breaks them.
- Get permission before changing legally or editorially fixed wording.
- Never replace a deleted cliché with unsupported features, measurements, dates, sources, research provenance, quotations or sentiments: a concrete-sounding invention is worse than the vague original because readers trust it. When specificity is unavailable, delete the inflation, keep the uncertainty, or ask for evidence. Delete an empty conclusion; never substitute an event.
- Never add "human" flourishes (invented anecdotes, forced contractions, planted typos) or rewrite to beat an AI detector: detectors and cue-masking are unreliable, and hiding cues leaves the substance problem in place.

## Deliver

Check before returning: every factual claim in the revision appears in the source; qualifiers survive, and an unmeasured benefit stays intent ("intended to speed access"), never an established result; protected text is character-identical. If a check fails, revert that sentence to the original or cut the unsupported part, then re-run the check.

Return the edited text and a brief neutral, mechanical change note (scope, patterns changed, exemptions), with no opinions about the text's quality. For a narrowly scoped edit, change only the requested passage. If the passage is already natural or the requested style uses a flagged pattern, leave it intact and say so.

File input: when the user gives a file path, Read it and edit it in place with Edit, then reply with the change note and a diff summary of each changed sentence; never overwrite the file with Write. If the file is outside the workspace or not writable, return the edited text instead.

## Credits

Original skill by @blader: https://github.com/blader/humanizer. Patterns based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.
