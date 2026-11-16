# Upstream review, 2026-11-04 (plan 8 Task 6)

`audit.py upstreams --registry docs/audit/upstream-sources.json` was run over every row, and each result was recorded with `audit.py track` (`last_reviewed` 2026-11-04). The `kind: repo` row (`softaworks/agent-toolkit`, the fork origin) is not an artifact and is not tracked. Decisions are the user's rulings of 2026-11-02 and 2026-11-03.

| artifact | source | status | decision |
|----------|--------|--------|----------|
| humanizer | blader/humanizer | current | current (user ruling); credit kept |
| humanizer | Wikipedia:Signs of AI writing | current (revision 1383638008) | adapt (user ruling): the skill was adapted to that revision in batch 46 with a CC BY-SA 4.0 note; credits kept |
| react-useeffect | reactjs/react.dev:…/you-might-not-need-an-effect.md | current | current (user ruling) |
| agent-md-refactor | Matt Pocock, Prompt Idea | current | unversioned; read once, nothing to compare |
| domain-name-brainstormer | Ben Aiad, Lenny's Newsletter | current | unversioned; credit restored in plan 8 |
| writing-clearly-and-concisely | joshuadavidthomas/agent-skills:writing | current | current (user ruling); the Orwell material is **not ported** (user ruling), so no `references/` file and no content change |
| writing-clearly-and-concisely | obra/the-elements-of-style | current | ignore (user ruling): status only, no content change |
| reducing-entropy | joshuadavidthomas/agent-skills:reducing-entropy | current | ignore (user ruling): status only, no content change |
| crafting-effective-readmes | joshuadavidthomas/agent-skills:crafting-effective-readmes | current | ignore (user ruling): status only, no content change |
| crafting-effective-readmes | hackergrrl/art-of-readme | unreachable | `gh api repos/hackergrrl/art-of-readme` and `repos/noffle/art-of-readme` return 404 on 2026-11-04; the credit stays as provenance |
| crafting-effective-readmes | RichardLitt/standard-readme | current | first review; credit kept |
| crafting-effective-readmes | Danny Guo, Make a README | current | first review; unversioned |
| 13 commands and agents, ui-ux-principles, skill-updater | local | current | no upstream; reviewed with their plan 8 batches |

## Checks

- Every non-repo row has `status` and `last_reviewed` (`jq` count of rows missing either: 0).
- No credit, source or license line was removed.
