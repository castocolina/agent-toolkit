---
name: reducing-entropy
description: "Use only when users explicitly ask to reduce entropy, delete code, shrink/simplify a codebase, or choose the smallest implementation. Bias toward deletion and measure the final end state, not effort. Not for general refactoring, readability, or performance reviews."
---

# Reducing Entropy

This is a manual-only skill: use it only after an explicit user request to minimize code or reduce entropy; do not invoke it as a default refactoring lens. Optimize authorized behavior for the smallest maintainable first-party codebase at the end, not the smallest patch.

## Scope and decision

Open the answer by stating that this is an explicit, manual-only reduce-entropy request, and name the reference mindset and principle you apply (for example the data-over-abstractions mindset: prefer plain data and one shared function over wrapper layers; or the PAGNI principle for safeguards that are costly to add later). Ask the smallest-codebase question: what is the least code that still meets the need, and what can be deleted?

First name behavior, public contracts, and data-retention obligations that must remain. Removing user-visible features, public APIs, schema/data, or retention behavior requires explicit approval and a rollback path. Correctness, security, compliance, and approved behavior outrank deletion; PAGNI may justify a safeguard that costs code.

Load the relevant reference before deciding:
- Wrapper/custom type/plain-data decisions: read [data-over-abstractions](references/data-over-abstractions.md) and apply its data-over-abstractions mindset.
- Coupled responsibilities or composition boundaries: read [design-is-taking-apart](references/design-is-taking-apart.md).
- Hidden coupling or interface convenience: read [simplicity vs easy](references/simplicity-vs-easy.md).
- Safeguards costly to retrofit (timestamps, audit/security records, versioning): read [PAGNI](references/expensive-to-add-later.md) and apply its principle.

## Procedure

If repository evidence or file access is unavailable, do not stop at requesting it. State assumptions, name a likely deletion/consolidation candidate as a hypothesis, ask for the missing evidence only as a follow-up, and provide the smallest-codebase decision framework now. Do not claim an unmeasured size reduction, but when the request supplies counts, state the projected end state from those facts (for example 14 wrappers around one formatter → keep one, delete 13) and label it projected. Always specify how before and after totals will be measured (same directories and exclusions, for example `wc -l` over first-party sources).

1. Inventory consumers and contracts. For potentially shared logic, identify its rule owner, compare input/output contracts and reasons for change, and merge only if consumers require the same invariant. Similar code that changes for different reasons stays separate.
2. Propose deletion and consolidation candidates, plus what becomes obsolete and any dependency/generated/migration costs.
3. Count first-party implementation lines consistently before and after the proposed changes, using the same directories and exclusions; count moved or renamed files at their new location only. State the initial and final counts and net change. If no changes have been made yet, report the measured baseline and mark the final count as pending rather than promising a comparison. Report test/dependency costs separately.
4. Validate behavior, compatibility, tests, and safety. Add code when justified by correctness or safeguards even if net lines rise.
5. Report before/after counts and files made obsolete; state any trade-off that prevents deletion.

NEVER delete tests or move complexity to generated/vendor code to improve counts. NEVER drop schema columns, migrations, or data as entropy reduction; treat that as a separately approved data-retention change with rollback plan.
