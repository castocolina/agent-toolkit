---
name: writing-clearly-and-concisely
description: Draft or copyedit English prose for clarity and concision in READMEs, documentation, commit messages, error messages, UI copy, help text, reports, and explanations. Use when asked to tighten, rewrite, remove puffery, or improve reader-facing text, even a single sentence. Preserve meaning, quotations, technical terms, and requested style. Not for technical diagnosis, code changes, translation, or verbatim extraction.
---

# Writing Clearly and Concisely

Apply to expository and technical prose. For fiction, dialogue, or an established brand voice, flag suggestions rather than silently rewriting the voice.

## Revision sequence

1. Mark semantic invariants before editing: facts, requirements, uncertainty, quotations, identifiers, negation, qualifiers, technical terms, and normative force (`must`/`should`/`may`). Preserve each unless explicitly asked to change it.
2. Remove unsupported abstractions and repetition; never add examples, metrics, capabilities, or factual claims absent from the source. Replace vague language only with supported specifics; otherwise preserve its scope or ask for evidence.
3. Resolve ambiguity only when context establishes the intended actor, scope, timing, or condition. Otherwise retain the ambiguity or flag the missing fact; do not silently turn a possibility into a commitment or an unknown into an assertion.
4. Preserve technical distinctions and control-flow conditions when tightening. Passive voice may be essential when the actor is unknown; active voice must not invent responsibility. Historical style references are advisory: follow contemporary usage, current pronouns, and repository/user house style.
5. Compare against the original for meaning and normative force. For a requested tightening, keep the rewrite shorter without deleting a condition that changes behavior. Make the rewrite shorter than the original when the requested edit is to tighten or make prose concise, then provide the rewrite first, followed by a one-line check quoting the original and both word counts (for example “21 → 9 words”), and keep any explanation to one brief sentence, clearly separate from the rewrite. Do not shorten away a condition that changes behavior. If source text is absent, do not pretend to rewrite it; if the supplied text is too vague to support a factual rewrite, provide concise neutral wording that preserves only its verified scope and briefly note the limitation.

## High-yield reference routing

- For concision, paragraph structure, active voice, or emphatic endings, load `elements-of-style/03-elementary-principles-of-composition.md`.
- For a specific grammar or punctuation question, load `elements-of-style/02-elementary-rules-of-usage.md`.
- For headings, quotations, or formatting, load `elements-of-style/04-a-few-matters-of-form.md`.
- For disputed word choice, load `elements-of-style/05-words-and-expressions-commonly-misused.md`, but apply contemporary usage, stated pronouns, and user/repository house style over historical prescriptions.
- Load `signs-of-ai-writing.md` only for explicit AI-style/Wikipedia-pattern analysis. Ordinary copyediting should not load it; its Wikipedia-specific conventions do not transfer automatically to general prose.

## Safeguards

Never delete meaningful qualifiers or negation; they often carry the safety or legal boundary. Never alter quotations, code, API identifiers, or schema keys while editing surrounding prose. Do not treat vocabulary as proof of AI authorship; keep a precise technical term when a simpler substitute weakens meaning. Preserve modern pronouns such as singular “they” and follow the user's house style.

When context is constrained, use an available subagent only if one exists; otherwise read just the relevant section and edit locally, preserving a short list of semantic invariants.
