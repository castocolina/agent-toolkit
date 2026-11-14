---
name: reducing-entropy
description: "Deletion-biased codebase minimization: inventory code to delete or merge, guard behavior, public APIs and data-retention obligations, and measure first-party line counts before and after. Use only when the user explicitly asks to reduce entropy, delete code, shrink or simplify a codebase or module, rip out what is not needed, or pick the smallest (least-code) implementation. Not for general refactoring, readability or local cleanups, or performance reviews."
---

# Reducing Entropy

Manual-only: apply this lens only when the user asked to minimize code. Without that request, review normally: propose no deletions, require no change for size, and mention duplication only as optional advice. Success is the smallest maintainable first-party codebase at the end, not the smallest patch: writing 50 lines that delete 200 is a win.

## Procedure

1. **Fix the boundary.** List the behavior, public contracts (exported names, CLI flags, routes, schemas) and data-retention obligations that must survive. Removing any of them needs explicit user approval and a rollback path. Correctness, security and compliance outrank line count; add code they need even if the net rises.
2. **Measure the baseline** with one working-tree counter. The rule: NUL-safe, counts untracked files, skips deleted paths, surfaces unreadable ones (cat prints a diagnostic on stderr and the pipeline still exits 0, so treat any diagnostic as an unverified count), and excludes tests, vendored and generated code. The command below is the default for a git repo whose code lives under `src`; for any other layout, retarget the pathspec (`src`) and the exclude globs once. `xargs -0 -r` runs nothing on an empty file list, so an empty tree prints 0 (checked 2026-11-14):
   `git ls-files -z --cached --others --exclude-standard -- src ':(exclude,glob)**/tests/**' ':(exclude,glob)**/test_*.py' ':(exclude,glob)**/*_test.*' ':(exclude,glob)**/vendor/**' ':(exclude,glob)**/generated/**' | xargs -0 -r sh -c 'for f; do [ ! -e "$f" ] || cat -- "$f"; done' sh | wc -l`
   Record it; the after count reruns it unchanged.
3. **Rank candidates by lines removed.** Deletions first, then what each deletion makes obsolete, then merges.
   - 3b. For each candidate, check the lens triggers and read the matching reference before deciding; name each lens used and its principle. Load no other reference.
     - Wrappers, custom types, lookalike code: [data-over-abstractions](references/data-over-abstractions.md).
     - Coupled responsibilities, a boundary to split or keep: [design-is-taking-apart](references/design-is-taking-apart.md).
     - A smaller version that may hide coupling: [simplicity-vs-easy](references/simplicity-vs-easy.md).
     - Timestamps, audit or security records, API versioning, pagination: [PAGNI](references/expensive-to-add-later.md). PAGNI decides whether that safeguard may go; any other lens decides the rest.
     - An argument for keeping code ("keep what exists", flexibility, separation of concerns, type safety, readability), or nothing that seems worth deleting: [red-flags-and-stop-conditions](references/red-flags-and-stop-conditions.md).
4. **Decide merges** with this table:

   | Invariant evidence | Compatibility boundary | Decision |
   |---|---|---|
   | Same rule, consumers change together | internal only | Merge into one; delete the rest |
   | Same rule | public name or import path | Merge the body; keep the public name as an alias |
   | Different rule (rounding, validation, format version), even if the code is identical | any | Keep separate; a merge would force unrelated consumers to change together |
   | Unknown | any | Keep; list as a hypothesis until tests or owners confirm |

5. **Check displacement.** A deletion that moves complexity into config, a new dependency, generated code or runtime behavior is not a reduction; count what moved or drop the candidate.
6. **Verify.** Run the existing tests, any available build or type checks, and a smoke import of every public name from step 1. If anything fails, restore the candidate or fix forward, then re-measure with the step-2 counter. Compare each candidate's after count with its before count: reject a candidate whose after count exceeds its before count unless a step-1 need requires the extra code (say which), and read [red-flags-and-stop-conditions](references/red-flags-and-stop-conditions.md) for the arguments and stop conditions. If checks cannot run, report the reduction as unverified.
7. **Report.** Baseline, after count, net change, files made obsolete, each retained item with its reason (contract, invariant or PAGNI), verification result, and test or dependency cost listed separately.

Without file access or measured counts, do not stop to ask: state the scope and counter you would run, name the likely candidate as a hypothesis, and mark totals pending. When the user supplies counts (14 wrappers around one formatter), give the end state from them labelled projected (keep one, delete 13). Never present an unmeasured number as measured.

## Gotchas

- NEVER call code dead from an empty caller search. Names in `__all__`, package entry points, plugin and route registries, `getattr`/`importlib` string lookups, templates, config files and external consumers all reach code with no textual call site. Treat each one found as a step-1 contract.
- NEVER delete or rename a class, enum member or function whose name stored data or deployed config holds (pickled objects, ORM polymorphic identities, Celery task names, entry points): no code search finds that reference, and the failure appears in production when old data or config loads.
- NEVER delete tests or move code into vendored or generated paths to cut the count: those paths sit outside the measured scope, so the number drops while risk rises and nothing got simpler.
- NEVER drop schema columns, migrations or stored data as entropy reduction: data cannot be regenerated from code. It is a separate data-retention change that needs approval and a rollback plan.
