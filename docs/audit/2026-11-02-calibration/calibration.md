# Calibration of the command and agent profiles (plan 12 Task 3)

"Calibrated" means exactly this: on the four-file set under `tests/skills/skill-judge/calibration/` (`cal-a` and `cal-c` good, `cal-b` and `cal-d` bad, answer key in `expected.json`), two lanes put the good files at 90 percent or more and the bad ones under 60, found every planted defect, and stayed within the lane-gap rule. Nothing more is claimed.

Lanes: `router-env/my-referee-one` and `router-env/my-referee-three` (`my-referee-two` returned 503 all day, so lane three replaced it). Harness: `tests/skills/skill-judge/calibrate.sh`, judges run in a scratch root without the answer key.

## Rounds

| round | profile_version | cal-a (one / three) | cal-b | cal-c | cal-d | defects | result |
|---|---|---|---|---|---|---|---|
| r1 | 2 | 80.0 / 92.0 | 31.2 / 21.6 | 80.0 / 90.4 | 26.4 / 14.4 | 12/12 | FAIL: bands; gap cal-a 12.0 (D4), cal-d 12.0 (D5) |
| r2 | 3 | 95.2 / 93.6 | 28.8 / 24.0 | 89.6 / 91.2 | 16.0 / 15.2 | 12/12 | FAIL: cal-c lane one 89.6 |
| r3 | 3 | 94.4 / 92.0 | 28.8 / 25.6 | 96.8 / 95.2 | 21.6 / 17.6 | 12/12 | PASS |

Verdicts and scores per round: `r1/`, `r2/`, `r3/`.

## What changed between rounds

- r1 → r2, good files (legitimate findings against the pinned spec): `cal-a` used `$1`/`$2` although positions are zero-based, had invalid YAML in `argument-hint`, a tag glob that matched pre-releases, and a `git fetch` that contradicted "read-only"; `cal-c` had a loose flake rule, no Inconclusive outcome and an unverified revision-mismatch claim. Both were fixed.
- r1 → r2, profiles (v2 → v3): D5 "at most 10" for an over-200-line file with nothing split out gave a 6-point lane spread on `cal-d`; it became an exact rung (4 of 15).
- r2 → r3, good file: `cal-c` condensed familiar class definitions and treated its error markers as hints with a case-insensitive fallback.
- No defect was remapped in `expected.json`; no bad file changed.

## Sanity check outside the set (Step 4, no gate)

`commands/explain-pr-changes.md` (505 lines, full eval suite) with profile v3: lane one 87.2, lane three 72.0. The 15-point gap came from D5 (12 versus 4) and D4: lane three read "nothing split out" although the command keeps its diagram rules in skills its plugin bundles and loads by path. Profile v4 (both kinds) settles it with explicit rungs on the file's own length: 200 lines or fewer 15; over 200 with material moved to a bundled or preloaded skill 10; over 200 with nothing split out 4. The calibration set is unaffected (`cal-a` 92 lines, `cal-b` 226 lines with nothing split out, `cal-c` 49 lines, `cal-d` 231 lines with no preload), so v4 was not rerun on it. The missing frontmatter `description` (D4) of `explain-pr-changes` is a real finding for plan 8.

Final profile versions: command 4, agent 4.
