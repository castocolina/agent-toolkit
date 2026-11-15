# Sources: ship-learn-next (skill), checked 2026-11-13

## Origins found

1. **Direct upstream: softaworks/agent-toolkit `skills/ship-learn-next`** (added in commit 40d4469f, 2026-01-20, "feat: add naming-analyzer, ship-learn-next, and skill-judge skills"). The baseline `dbff837f` SKILL.md and README.md are identical to the fork point `3027f20f` (`git diff --stat 3027f20f dbff837f -- skills/ship-learn-next` is empty, so no local change existed before October; the whole rewrite came after `dbff837f`). No credit line in README.md or in the root README row ("Turn learning into actionable reps").
2. **Original upstream: michalparkola/tapestry-skills-for-claude-code `ship-learn-next/SKILL.md`** (MIT; repo default branch `main`, head 80e1dc56df74d1cb849ad649c7ead9756e7929bb on 2026-11-13; the skill file was last changed 2025-10-24, commit c85d2bc1). The baseline SKILL.md equals that file except the frontmatter `allowed-tools` (upstream `Read,Write`, softaworks and our baseline a YAML list). The softaworks copy is therefore a copy of michalparkola's skill, and this is the real origin. Credit line for the framework itself, from the upstream README Acknowledgments: "Ship-Learn-Next framework: Inspired by the ShipLearnNext GPT methodology" (no originator named).
3. **No primary source for the framework or the slogan.** Web searches for the framework, "100 reps beats 100 hours of study" and "ShipLearnNext" found only agent-skill listings (michalparkola, softaworks, davila7 and other forks), no book, newsletter or author. The Pat Flynn and Ben Franklin attributions that circulate informally have no source and the artifact makes neither claim, so no line is added for them. Nothing else in the artifact (no quote, statistic or named person) needs a source.

## Missing credit line (README.md has none)

Add to `skills/ship-learn-next/README.md` (end of file, after the closing line):

```text
Based on the original skill in [michalparkola/tapestry-skills-for-claude-code](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/ship-learn-next) (MIT), via [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/main/skills/ship-learn-next); this version is rewritten. The upstream README says the framework is inspired by the "ShipLearnNext GPT methodology" and names no originator.
```

## Proposed registry rows (docs/audit/upstream-sources.json; I did not edit the registry)

```json
{
  "skill": "ship-learn-next",
  "kind": "github-path",
  "source": "michalparkola/tapestry-skills-for-claude-code:ship-learn-next",
  "ref": "main",
  "credit": "michalparkola/tapestry-skills-for-claude-code (MIT), via softaworks/agent-toolkit"
}
```

```json
{
  "skill": "ship-learn-next",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/ship-learn-next",
  "ref": "main",
  "credit": "softaworks"
}
```

Docs pages used for Step 5 (proposed `unversioned` rows; the controller may merge them into one row per vendor):

```json
{
  "skill": "ship-learn-next",
  "kind": "unversioned",
  "source": "Claude Code Docs, Extend Claude with skills (https://code.claude.com/docs/en/skills)",
  "ref": null,
  "credit": "Anthropic"
}
```

```json
{
  "skill": "ship-learn-next",
  "kind": "unversioned",
  "source": "Agent Skills specification (https://agentskills.io/specification)",
  "ref": null,
  "credit": "Agent Skills (agentskills.io)"
}
```

Check: both github-path rows use `owner/repo:path` and `ref` "main" (`validate_entry` rules); the path `ship-learn-next` (michalparkola) and `skills/ship-learn-next` (softaworks) both exist on `main` (`gh api` listing 2026-11-13).

## Skill-updater style review (review only; no `track` call, no registry write)

No registry row exists for this skill and no credit line named an upstream, so per skill-updater step 2 the rows above are proposals only and `upstreams` has nothing to report for it yet.

- michalparkola `ship-learn-next/SKILL.md`: only two commits (2025-10-17 initial, 2025-10-24 "Update SKILL.md"), both before softaworks copied it on 2026-01-20. The baseline equals the current upstream (only `allowed-tools` format differs). Nothing upstream is newer than our baseline.
- softaworks `skills/ship-learn-next`: one commit (40d4469f); same text as the baseline.

Adopt, adapt, ignore list for the restore brief:

- **adopt** s038: the closing questions "What's the one thing that might stop you? How will you handle it?" and "Come back after you ship and we'll reflect + plan Rep 2", rewritten into Workflow step 5 (one or two sentences; the record row is `restore-main`, `procedure-depends`).
- **adapt** (only if the controller wants README consistent): README "Plan Structure" (s013) and the "Rep 1" fields (Ship Goal, Success Criteria checkboxes, What You'll Practice, Minimal Resources) still describe the superseded template, and README "Quest Framing" / "Quest Overview: Goal (4-8 week target)" describe a step SKILL.md no longer performs. Align README wording to the Rep 1 shape without removing README content that remains true (a README fix, not a content recovery).
- **ignore**: everything else upstream (3-6 word titles, key phrases, conversation style, success checklist, the fixed 1-7 day and 2-5 rep sizes, "always save"): each was replaced by a deliberate rule in the rewritten SKILL.md or is generic model behavior (see record.md).
- Model-validity pass: not run. It needs the tool-less probe lane, and the brief forbids judging with an LLM lane. The rules that counter a model habit (no fabricated timestamps, no gating on market response, no "saved" claim before the write) are the artifact's own and are exercised by evals `tutorial-to-action`, `noisy-outcome` and `chat-only`; recommend the controller run the pass if wanted.
