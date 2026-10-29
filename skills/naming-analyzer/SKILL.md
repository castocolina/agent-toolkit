---
name: naming-analyzer
description: Review code identifiers and suggest clearer variable, function, class, boolean, constant, or file names consistent with project conventions. Use when asked to review naming, clarify abbreviations, identify misleading getters, or improve vague identifiers in code. Return suggestions and rationale; not for automatic repository-wide renames, database migrations, or product/brand naming.
---

# Naming Analyzer

Review names as semantic contracts, not style preferences. Do not apply renames unless separately authorized.

## Evidence-first review

Before proposing a rename, inspect the implementation and its call sites. Establish:

- What value or effect does it represent, including units, nullability, and time basis?
- What is its scope and lifecycle? Does it mutate, cache, persist, retry, or perform I/O?
- Is it used in serialized data, database columns, public APIs, generated code, or external protocols?
- What naming patterns does the surrounding project actually use? Treat boolean prefixes and casing as defaults, not automatic defects.

Only call a name misleading when behavior contradicts the promise it makes. For constants, retain the project's casing convention and make the constant descriptive enough to identify the value or constraint (for example, `MAX_RETRIES` rather than `MAX`). If code context cannot resolve meaning, ask a focused question or label candidate names as tentative; never infer domain intent from spelling alone. Keep conventional mathematical and protocol names (`i`, `x`, `ETag`, `URL`) when their local context is clear.

## Review sequence

1. Check behavior mismatch first (for example, a `get*` method that writes persistent state). These are higher risk than abbreviations or stylistic inconsistency.
2. Check ambiguous domain terms, hidden units/time zones, overloaded abbreviations, and boolean polarity/meaning.
3. Check project consistency only after confirming the local convention; do not impose a language-wide preference over a repository's established API.
4. Check public/serialized names before recommending changes. A rename may break clients or persisted data even if the identifier is internal-looking; distinguish an internal alias from a wire/database contract and propose a compatibility migration where needed.
5. Return a prioritized rename table with current name, proposed name, evidence/rationale, confidence, and compatibility risk. Include only useful changes. State when no change is warranted.

## Gotchas

- Never rename serialized fields, public API symbols, database columns, or protocol identifiers without checking compatibility and migration/versioning requirements.
- Never infer business meaning from a name when behavior and tests do not establish it; ask rather than invent intent.
- A getter that writes or triggers expensive effects misleads callers into using it in read paths; name the effect explicitly or separate query from command.
- Do not flag `active` as defective merely for lacking `is`; fix polarity ambiguity or unclear lifecycle semantics, not prefix preference.
- Preserve established mathematical, standards, and protocol identifiers when changing them would reduce recognizability.

## Reference

For the report structure, use this compact shape:

| Priority | Location | Current → proposed | Evidence and rationale | Confidence / compatibility |
|---|---|---|---|---|

Natural-language examples: “Review naming in `src/services`”; “Is `ttl` precise here?” Do not imply a nonexistent `--fix-all` command or make edits without authorization.
