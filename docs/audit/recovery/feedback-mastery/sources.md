# Sources for feedback-mastery

Reviewed 2026-11-13 against baseline dbff837f and BASE 473a2da6. Nothing here edits the artifact, the registry or README; the controller applies the rows and the credit line.

## Origins found

1. softaworks/agent-toolkit, `skills/feedback-mastery` (author Leonardo Flores, @leonardocouy, commits 011baf4a and ebb0419d, January 2026). The skill at baseline dbff837f and at the softaworks snapshot 3027f20f are byte-identical (`git diff --stat 3027f20f dbff837f -- skills/feedback-mastery` is empty), and upstream main's `SKILL.md` has the same blob hash as the baseline (`4f2c6adb3af9`). No registry row exists for `feedback-mastery` (it is covered only by the whole-repo `kind: repo` row), and the README has no credit line, so the origin is uncredited and untracked.
2. Center for Creative Leadership (CCL), the SBI model and its SBII extension. The README and `references/feedback-sbi-model.md` already name CCL ("The SBI model was developed by the Center for Creative Leadership"); that credit stays untouched. CCL's own page supplies the facts for the SBII restore.
3. Recommended-reading books and Edmondson's research are references the README lists, not content origins: no row.
4. The removed unsourced statistics (60% more likely, 30% cognitive processing) have no origin: searched 2026-11-13, nothing found; they are dropped, not credited.

## Proposed registry rows (verbatim JSON)

```json
{
  "skill": "feedback-mastery",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/feedback-mastery",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

```json
{
  "skill": "feedback-mastery",
  "kind": "unversioned",
  "source": "Center for Creative Leadership, Use Situation-Behavior-Impact (SBI) To Understand Intent: https://www.ccl.org/articles/leading-effectively-articles/closing-the-gap-between-intent-vs-impact-sbii/",
  "ref": null,
  "credit": "Center for Creative Leadership"
}
```

Facts.md pages that count as official docs and would each be an `unversioned` row if the controller wants the books tracked (optional, low churn): Penguin Random House, Difficult Conversations (https://www.penguinrandomhouse.com/books/722989/difficult-conversations-by-douglas-stone-bruce-patton-and-sheila-heen-foreword-by-roger-fisher/, credit "Penguin Random House"), Radical Candor, the book (https://www.radicalcandor.com/the-book, credit "Radical Candor, LLC"), and HBS Working Knowledge, psychological safety (https://www.library.hbs.edu/working-knowledge/psychological-safety-is-an-asset-not-a-luxury, credit "Harvard Business School"). The CCL row above is the one the restore depends on.

## Missing credit line

`skills/feedback-mastery/README.md` has no Credits section. Its siblings use this form (`difficult-workplace-conversations`, `professional-communication`, `naming-analyzer`). Add at the end of the README, below Recommended Reading, with the CCL sentence staying where it is:

```markdown
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The registry `credit` value `softaworks/agent-toolkit` then appears verbatim in the README, which `audit.py check --strict` (`missing_credit`) needs.

## Skill-updater style review (review only, no `track` call)

- Upstream drift: none. Upstream's feedback-mastery path was last touched by ebb0419d (January 2026) and its `SKILL.md` equals the baseline. There is no upstream change to adopt, adapt or ignore; every difference from the baseline is a local rewrite (plans 8 and 13), so all recovery comes from the baseline, not from upstream.
- Adopt: none. Adapt: none. Ignore: none (no upstream change).
- Adapt items for the restore brief that come from sources, not upstream: (a) restore SBI-I as CCL's SBII, naming CCL's page, asking about intent and never asserting it; (b) add the missing Crucial Conversations co-authors to the README reading list (Ron McMillan, Al Switzler); (c) add the Credits section above. Credit lines that exist (CCL sentence, Recommended Reading) are untouched.
- Model-validity pass: not run. It needs the `pi-cmd` probe lane, which the analyst rails exclude from implementers; the rules that counter a model habit (never open with "I feel like you...", draft for private delivery even when a channel post is asked for, separate recognition from correction) should be probed by the controller if wanted. Evals in `skills/feedback-mastery/evals/evals.json` already exercise the split of recognition and correction, the checked-out impression, the channel call-out and the vague-criticism reply.
- `audit.py upstreams` was not needed: no registry row exists for this artifact other than the repo row, and the direct gh checks above gave the same result.
