---
name: humanizer
metadata:
  version: "2.1.1"
description: Edit existing drafts to remove formulaic AI-like prose, promotional filler, vague attributions, and repetitive sentence patterns while preserving facts, author voice, and house style. Use when a draft sounds robotic or the user asks to humanize text or remove AI writing patterns. Not for authorship detection, factual research, translation, spelling-only proofreading, or writing from scratch.
allowed-tools: Read Write Edit Grep Glob AskUserQuestion
---

# Humanizer

Edit existing prose, not its evidence. First establish audience, genre, intended stance, house style, and requested edit depth from the request and source; ask only for missing information that changes the edit. Diagnose the most consequential prose issue, make targeted changes, then compare the revision with the brief and original.

Preserve the author's register. Formal prose need not gain first person or contractions; casual prose may keep deliberate em-dash rhythm, fragments, and humor. Cues below are diagnostic, not categorical bans: retain typography, heading conventions, technical vocabulary, and rhetoric when they fit the voice or house style. If the user asks to preserve a pattern, exempt it and mention that in the summary.

## Core diagnostics

### Inflated significance

Watch for generic claims that an event is pivotal, a testament, a turning point, or part of a broader trend. Keep only significance supported by the text and relevant to the reader.

### Vague importance and attribution

Replace claims attributed to "experts," "observers," or "many" only when the supplied source identifies who, what they said, and why it matters. Never invent a source to make prose sound concrete.

### Superficial analysis

Remove empty participial explanations ("highlighting the importance", "ensuring a seamless experience") when they merely restate the preceding sentence. Keep causal or consequential details that add information.

### Promotional language

Treat "seamless," "powerful," "innovative," and stacked praise as prompts to look for evidence, not banned words. Replace only unsupported evaluation; preserve a product's stated positioning when it is intentional and sourced.

### Formulaic structure

Check repeated rule-of-three phrasing, "not just X but Y" contrasts, synonym cycling, false ranges, and repeated transition words. Fix only patterns that make the argument less precise or monotonous.

### Vocabulary and mechanics

Words like "delve," "leverage," or "multifaceted" are not proof of AI authorship. Keep precise terms when alternatives weaken meaning. Mechanical cues (emoji, title case, curly quotation marks, excessive bold, em dashes) are house-style choices, not defects by themselves.

For additional style, communication, and filler diagnostics, load `references/pattern-catalog.md` when core content patterns are absent or the user's concern points there.

## Never alter evidence

- Never silently rewrite direct quotations or primary-source excerpts; that changes evidence. Flag them or ask permission.
- Never humanize code, API identifiers, schema keys, or other exact-match text; stylistic changes can break behavior.
- Get permission before changing legally or editorially fixed wording.
- Never add unsupported features, measurements, dates, sources, quotations, or sentiments. When specificity is unavailable, remove inflation, preserve uncertainty, or request evidence.
- Before finalizing, compare each factual claim in the revision with the supplied text/source. Keep necessary qualifiers and uncertainty: phrase an unmeasured benefit as intent (for example “intended to speed access”), never as an established result. Keep the change note neutral and mechanical; do not add opinions about the text's quality.

## Deliver

Return the edited text and a brief change note when useful. For a narrowly scoped edit, change only the requested passage. If the passage is already natural or the requested style uses a flagged pattern, leave it intact.
