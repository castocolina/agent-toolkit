# Naming guidelines

Supporting rules for SKILL.md. They never override its evidence rules: a rename is proposed only after the definition, the callers and the hidden consumers are read, and this skill edits nothing. Project convention comes first; everything here that names a form is the fallback for a project that has none.

## What to look for

Names in scope: variables, constants, functions, methods, classes, interfaces, types, files and directories. Database tables and columns and API endpoint paths are reviewed too, but they are contract names: rate them `contract` and propose an alias or a versioned migration, never a plain rename.

Issues worth a row:

- A name that is vague (`data`, `info`, `temp`, `process`) in a scope where the code does not make its role obvious.
- An abbreviation that hides the meaning (`usrCfg`), or a name so long it repeats its context.
- A misleading name: it promises something the code does not do (Decide table, first row).
- Mixed casing or an inconsistent convention for the same kind of symbol.
- A boolean without a state, possession, ability or decision word, when the project's booleans have one.
- Hungarian notation, only when the project does not use it.

Convention layers, checked in this order: the project's own patterns, the framework's (React components in PascalCase, Vue props, Next.js file names), the language's dominant convention, an industry standard. The first layer that has an answer wins. When the framework's form and the project's dominant form disagree, follow the project and record the framework exception in the report.

## Priority classes

The Priority column of the report uses three classes. Assign them from the evidence, not from the shape of the name: a one-letter name that is conventional in context (`i`, `x`, `id`) gets no row at all.

| Priority | Class | Evidence |
|---|---|---|
| 1 | Misleading | Behavior contradicts the name, or callers disagree about its meaning (the first two Decide rows). The old "Critical" tier. |
| 2 | Unclear | The name is vague, abbreviated or hides a unit or time basis, and the code settles what it should say. The old "Major" tier. |
| 3 | Convention | The name is clear but breaks the project's (or the language's) convention for its kind. The old "Minor" tier. |

Inside a class, keep the Decide table order, and say when a rename is only less clear (not misleading) at `hidden` or `contract` compatibility: the clarity gain rarely pays for that churn.

## Boolean names

- Use a prefix that states what the boolean means: `is` for a state (`isActive`, `isVisible`), `has` for possession (`hasPermission`, `hasError`), `can` for ability (`canEdit`, `canDelete`), `should` for a decision (`shouldRender`, `shouldValidate`). In Python the same prefixes are `is_`, `has_`, `can_`.
- A project that already uses another prefix or form for booleans (`was`, `did`, `enable`, a suffix) keeps it: the project wins, per the Convention layers order.
- Prefer positive polarity: `isEnabled` over `isDisabled`. A polarity flip can invert meaning, so follow the `disableRetry` row of the Cases table (every default, read, write and test flips; a plain IDE rename is not enough).
- A boolean field without a prefix (`active`) is a convention gap, not a defect, and is often a column or a JSON key: keep it unless the project's other booleans all carry a prefix and the field is `local`.
- A non-boolean name that holds a boolean or a status (`login`, `status`) gets a question about its type before any rename.

## What not to flag or suggest

- Single-letter names are fine for short loops and conventional roles (`i`, `j`, `k`, `x` in a lambda); flag them only in a large scope where the role is not clear.
- Vague names (`data`, `info`, `temp`, `x`) are findings only when the code or its callers show a more specific role. With no code, ask what it holds (Decide table, third row).
- Do not mix conventions in a suggestion: a proposed name follows the project's casing for its kind.
- Do not propose a misleading name, an over-abbreviated name, or a longer name only for length.
- Do not add Hungarian notation, and do not flag it where the project's whole codebase uses it.
- Do not use vague class suffixes such as `Manager`, `Helper` or `Utility` in a proposal unless the codebase convention already uses them; a name that says what the class owns (`PaymentProcessor`, `EmailValidator`) is clearer.

## Acceptable abbreviations

Keep a well-known abbreviation and write "no change warranted": `id`, `url`/`URL`, `api`, `html`, `ETag`, `req`/`res` in a handler, `i`/`j`/`k` as short-loop counters. Anything a reader of the project could not decode without the code (`usrCfg`, `calcTtl`) is a candidate. When the project already spells a word one way, follow it.

## Convention fallback tree

Use it only for the last two Decide rows, when step 1 found no project convention. Write the casing in the language's own form (camelCase, snake_case) and say which convention you used.

```text
Is it a boolean?
├─ Yes → state, possession, ability or decision prefix
└─ No → Is it a function?
    ├─ Yes → verb phrase for the action
    └─ No → Is it a class?
        ├─ Yes → noun, in the language's type casing
        └─ No → Is it a constant?
            ├─ Yes → UPPER_SNAKE_CASE, with the unit when it has one (`CACHE_DURATION_MS`)
            └─ No → descriptive noun (`userList`, not `list`)
```

## Convention splits

A split across the repository (booleans with and without `is` in 8 files, camelCase and snake_case side by side in `src/legacy/`) is one grouped finding, not one row per identifier: name the locations, which form dominates, and the direction to converge on. Rate its compatibility by the riskiest identifier in the group and name that identifier. Rows for the same group in the table would hide the real finding.

## Counts line

End the report with one line after the table, built only from what you actually read:

```text
Reviewed 156 identifiers; 23 candidates (Priority 1: 5, 2: 12, 3: 6); 13 not shown, ask for the next batch or name a path.
```

Drop the last clause when nothing was cut. When nothing warrants a change, the one-line statement in SKILL.md replaces this line.
