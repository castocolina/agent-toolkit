---
description: Diff signals and false positives for anti-patterns a change may have introduced. Read when the candidate lesson is a warning, not a success.
---

# Anti-pattern signals

Many-file edits (shotgun surgery) live in the change-amplification row of se-principles.md, not here.

| Anti-pattern | Diff signal | Check before naming it |
|---|---|---|
| God object | One file takes many unrelated edits, or grows past ~500 lines | A router, registry or schema file is touched by every feature by design; name it only if the edits have different reasons to change. |
| Feature envy | A new function reads another module's fields more than its own | Mappers and serializers exist to read another type; that is their job, not envy. |
| Premature abstraction | An interface, factory or generic type added with one implementation | A test double or an existing plugin boundary in the diff is a second user. |
| Copy-paste | Near-identical blocks added in several places | Copies that change for different reasons are safer apart (se-principles.md DRY row). |
| Magic number | A new literal threshold, timeout or limit in a condition | A literal named by its variable, or pinned by a test that explains it, already carries its meaning. |
| Long method | A function grows past ~50 lines or gains nesting levels | Flat sequential setup, configuration or generated code is long but not complex. |
| Excessive comments | Comments that restate the code, or commented-out code left in | A comment that states a constraint or the reason for a choice is the useful kind. |
