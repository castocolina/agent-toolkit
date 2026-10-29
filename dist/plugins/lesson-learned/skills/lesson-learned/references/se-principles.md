---
description: Diff signals for mapping observed changes to defensible engineering lessons.
---

# Diff-to-lesson lookup

Use these as hypotheses, not labels. A pattern name is earned only when the diff shows the relevant consequence.

| Diff signal | Candidate lesson | Evidence needed / false positive |
|---|---|---|
| Logic extracted into a shared module | Cohesion, reuse, or coupling | Check whether callers now depend on a stable contract. Extraction that spreads knowledge of internals increases coupling; fewer lines alone is not modularity. |
| Similar blocks consolidated | DRY / shared knowledge | Confirm both blocks encode the same rule and change for the same reason. Intentional duplication is safer when copies evolve independently, have different owners, or protect availability across boundaries. |
| Call sites altered across many modules | Change amplification / boundary quality | Trace whether one policy change required coordinated edits. File count alone is not shotgun surgery: mechanical renames, generated output, and API migrations create the same surface signal. |
| Tests added, removed, or changed with behavior | Feedback and regression boundary | Compare assertions and production behavior. A larger test suite is not proof of stronger coverage; identify the formerly unprotected outcome now asserted. |
| New dependency or abstraction | Complexity transfer | Identify what first-party code disappeared, what new runtime/build/security surface appeared, and whether consumers gained a real capability. |
| Branches/guards moved toward input boundary | Fail-fast / invariant ownership | Verify invalid states are now rejected before side effects, not merely translated into another error later. |
| State or data representation changed | Information ownership / migration risk | Compare readers, writers, persistence, and compatibility. A cleaner local representation may impose migration or coordination cost elsewhere. |
| Behavior removed or simplified | YAGNI / scope discipline | Verify the removed behavior was unused or explicitly out of scope; absence from current tests is not evidence that users do not rely on it. |

## Evidence standard for before/after claims

A claimed improvement needs an observable consequence: changed output, eliminated failure path, fewer coordinated edits for the same future change, or a new test protecting a previously exposed behavior. Quote or point to the relevant code/test on both sides when available. If only the after-state exists, describe the change, not an unproven improvement. Commit intent is context, never proof.
