# Sources: difficult-workplace-conversations

Reviewed 2026-11-07 (review only: no `track` call, no edit of the artifact, no probe lane).

## Origins found

1. **softaworks/agent-toolkit, `skills/difficult-workplace-conversations`** (fork point `3027f20f`, the upstream `main` head, 2026-03-05). The directory was added upstream in one commit (`011baf4a`, "feat: add 7 new skills", 2026-01-18). All six upstream files (SKILL.md, README.md, four references) are byte-identical to the copies at `3027f20f` and at the baseline `dbff837f`, so upstream has not changed since the fork and nothing remains to adopt. No credit, author or license line exists in the upstream skill, in the baseline, or in the current README. No registry row exists for it today. The root README already says "Fork of softaworks/agent-toolkit by @leonardocouy", but a per-skill credit line is the repo's convention for skills that came through the fork (`skills/database-schema-designer/README.md`, `skills/gemini/README.md`).
2. **Conceptual lineage, not copied text.** A web search for the distinctive phrases ("Preparation-Delivery-Followup", "40% of Success", outcome/relationship/identity goals) found only copies of the softaworks skill (a tessl registry page, an npm mirror `claude-code-skills`, skillselion, hackernoon) and no earlier source; the "40%" figure has no source anywhere, which is why s043 and s004 are recorded as unsourced. The outcome, relationship and identity goals echo the identity conversation in Stone, Patton and Heen, *Difficult Conversations* (a three-conversations model: what happened, feelings, identity), which `skills/feedback-mastery/README.md` already credits. The skill never claims it, so this is an optional credit, not a missing one.
3. **Facts pages used** (facts.md): the Gottman Institute article on flooding and breaks, and the NHS breathing page.

## Proposed registry rows (docs/audit/upstream-sources.json)

Checked against `validate_entry`: `github-path` takes `owner/repo:path` and a non-empty ref; `unversioned` takes a non-empty source string, `ref: null` and a credit.

```json
{
  "skill": "difficult-workplace-conversations",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/difficult-workplace-conversations",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

```json
{
  "skill": "difficult-workplace-conversations",
  "kind": "unversioned",
  "source": "The Gottman Institute, Conversational Boundaries without Stonewalling: https://www.gottman.com/blog/conversational-boundaries-without-stonewalling",
  "ref": null,
  "credit": "The Gottman Institute"
}
```

```json
{
  "skill": "difficult-workplace-conversations",
  "kind": "unversioned",
  "source": "NHS, Breathing exercises for stress: https://www.nhs.uk/mental-health/self-help/guides-tools-and-activities/breathing-exercises-for-stress/",
  "ref": null,
  "credit": "NHS"
}
```

No row for the Stone, Patton and Heen book: no official URL was verified, so it would not meet the `unversioned` rule (title and URL).

## Missing credit line

`skills/difficult-workplace-conversations/README.md` has none. Add at the end (same wording as `skills/database-schema-designer/README.md`):

`Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.`

Optional, only if the restore of s049 (relationship and identity goal) keeps the "who do I want to be in this conversation" prompt: a further-reading line in the same README, `The identity-goal prompt follows the identity conversation in *Difficult Conversations* by Douglas Stone, Bruce Patton and Sheila Heen.` The author names match `skills/feedback-mastery/README.md` line 53 ("Stone, Patton, and Heen"); the first names are from the book's cover and were not re-fetched here.

## skill-updater style review (review only)

- Step 2: no registry row for the artifact, so no `upstreams` output exists to read (`upstreams` skips an artifact with no row, so it was not run). The upstream was read directly with `gh api`: tree listing of the path and a byte comparison of each of the six files against `3027f20f` (all identical, upstream head is `3027f20f`).
- Step 4 equivalent: upstream change since the fork: none. Adopt: none. Adapt: none. Ignore: none. Once the row above exists, the first `track` call should record `current` with `--sha 3027f20f3181758385a1bb8c022d4041dfb4de84`.
- Model-validity pass: not probed (the rails forbid running a judgment lane in this task). The rules that counter a model habit, for a later probe: "state the decision in the first two sentences" (models open with warm-up), "no feedback sandwich", "state the figure, then stop talking", "never promise absolute confidentiality", "never put the topic in a calendar title", "do not load emotional-regulation.md for negotiation or bad news". Each should be kept unless a probe shows the habit absent.
- Restore brief items (from record.md), all into `references/`, none into SKILL.md:
  - PB `references/phrase-bank.md` (new): s051, s066, para:50715b7a, s056, s068, s069, s070, s071, s100, s077, s079, s080.
  - CF `references/closing-and-followup.md` (new): s025, s057, s058, s081, s083, s085.
  - PT `references/preparation-template.md` (extend): s039, s049, s050, s113, s115, s116, s117, s121, s122, s123, s124.
  - ER `references/emotional-regulation.md` (extend the technique picker, still offer one technique): s013, s028, s095, s097, s118, s119, s120, s106.
  - `drop-pending` rows (restore to references in the interim unless the class is wrong or stale; all five are `superseded-by` or `generic-model-knowledge`, so the controller decides): s004, s008, s060, s067, s111.
  - Constraints for the dispatch: add triggers in SKILL.md Conditional references for PB and CF (and keep the existing gating text: emotional-regulation only when asked, one technique); update the README references table; use the verified values in facts.md (20-minute break, NHS-style breathing, no fixed 24-hour wait, no Friday ban); keep the credits.

## Registry rows applied (one line each, the same rows as above)

{"skill": "difficult-workplace-conversations", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/difficult-workplace-conversations", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "difficult-workplace-conversations", "kind": "unversioned", "source": "The Gottman Institute, Conversational Boundaries without Stonewalling: https://www.gottman.com/blog/conversational-boundaries-without-stonewalling", "ref": null, "credit": "The Gottman Institute"}
{"skill": "difficult-workplace-conversations", "kind": "unversioned", "source": "NHS, Breathing exercises for stress: https://www.nhs.uk/mental-health/self-help/guides-tools-and-activities/breathing-exercises-for-stress/", "ref": null, "credit": "NHS"}
