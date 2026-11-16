# Plan 10 acceptance

Judged artifacts changed by plan 10. Lane one left after round 1, so the final round pairs lane two with lane three (merged, two judges).

| Artifact | Round 1 (lanes one + two) | Round 2 (lane two) | Final (lanes two + three) | Evals | Triggers |
|---|---|---|---|---|---|
| pr-diagrams | 94.4 A, 3 high | 95.2 A, no high | 94.0 A, no high (lane three 92.8) | 36/36 | 21/21 |
| explain-pr-changes | 92.8 A, 1 high | 93.6 A, no high | 90.4 A, no high (lane three 87.2) | 86/86 scenarios at gate 1.0 (lane three) | n/a |

Round 1 found 4 highs, and fix commits fixed all of them along with every round 1 medium:

- pr-diagrams: `publish` resolves origin's repository and refuses a mismatch, and it keeps images published earlier for the same PR.
- pr-diagrams: the skill now documents partial-attach recovery and has a caveat for squash and rebase history.
- explain-pr-changes: images published to the `pr-diagrams` branch now count as diagrams in the shared definition, the none-mode filter and reuse detection.

## Second-lane confirmation

Lane three first scored pr-diagrams at 79.2 C (merged with lane two: 87.2 B). Two more rounds fixed that:

- A holistic rewrite added a Setup block, an ordered workflow (including branch mode for a new PR), one Gotchas section, a gated reference load list, a checkable merge-history test, `pr-diagrams.sh help`, and a tighter "Not for" clause. The clause fixes the one trigger miss ("list the reviewers already requested on PR 12").
- The next round left one high: `repo` is github.com only. SKILL.md now tells a GHE caller to set `REPO=<host>/<owner>/<repo>` by hand, and says that `related` and `reviewers` (promotion reuse) support github.com only.
- Two new evals pin branch mode for a new PR and partial-attach recovery.

Because the command's eval context includes pr-diagrams' SKILL.md and `references/pr-body.md`, the full explain-pr-changes gate ran again. It passed 276 of 277 assertions in the first pass. The one miss was `drawio-old-gh-branch-mode`, where the final message named the gh version. That scenario passed 3/3 in each of two reruns. It is recorded as runner variance, not a regression.

## Waived mediums (final round)

- **explain-pr-changes D5/D1:** the judge wanted the phase-2 final-message ordering and the two-candidate path rule moved into a reference, and phases 1 and 3 reduced to pointers. Waived because these rules apply to every run mode. Moving them would make every run load the reference, and the drawio-only recipe is already there.
- **explain-pr-changes D8:**
  - Progressive `state.env` across several phase-3 calls: waived because the single-call phase 3 is the command's existing contract, which plan 10 does not change.
  - A named stop when neither `pr-body.md` exists: waived because the plugin always bundles `pr-body.md`.
- **pr-diagrams D8 (standalone variables):** waived because the Setup block now defines `AD`, `REPO`, `BASE`, `HEAD`, `TITLE` and `N`.
- **pr-diagrams D4 and D8 (reviewers):** waived. The first wanted a longer description; it is already at 715 characters. The second wanted a joined `--add-reviewer` call guarded for an empty list. That is a low-impact wording nit: an empty `reviewers` array leaves nothing to request.
