# Batch 33

## skill-updater (skill)

### skill-updater#D8-1
- severity: high
- dimension: D8
- location: skills/skill-updater/SKILL.md:35
- fix: Require --new-path with the existing row value whenever a row already has new_path, including current, stale and unreachable recordings. Clear that mapping only through an explicit, justified source correction.

### skill-updater#D8-2
- severity: medium
- dimension: D8
- location: skills/skill-updater/SKILL.md:35
- fix: Add an explicit branch for skills with no external source rows: perform the model-validity pass and record a source-less local review using track --registry docs/audit/upstream-sources.json --artifact NAME --artifact-kind skill --status current --model MODEL. Handle existing local rows through the same branch.

### skill-updater#D8-3
- severity: medium
- dimension: D8
- location: skills/skill-updater/SKILL.md:26
- fix: Gate classification on a successful contents response. For authentication, rate-limit or network failures in this checkpoint, apply the authentication check and single retry; if verification still fails, record unreachable and do not relocate or classify unseen changes.

### skill-updater#D7-1
- severity: medium
- dimension: D7
- location: skills/skill-updater/evals/evals.json:26
- fix: Strengthen recording assertions to verify the explicit --registry path, exact artifact and copied source, and required --new-path/--sha on relocation. For the model-probe case, verify the selected model is used in both the probe and track command.

### skill-updater#D7-1
- severity: medium
- dimension: D7
- location: skills/skill-updater/evals/evals.json:6
- fix: Make the expected track command complete: --artifact writing-clearly-and-concisely --source joshuadavidthomas/agent-skills:writing --status path-moved --new-path skills/writing --sha <sha from the commits query>. Add a sha to the fixture, and add an assertion that the command includes --sha.

### skill-updater#D7-2
- severity: low
- dimension: D7
- location: skills/skill-updater/evals/evals.json
- fix: Add an eval for the `no local commit` error, where the agent must stop and must not commit to make the row pass. Add an eval for an unversioned blog-post row that expects `current` with no --sha. Rephrase one existing prompt casually, for example "hey is humanizer still up to date?".

### skill-updater#D8-1
- severity: medium
- dimension: D8
- location: skills/skill-updater/SKILL.md:15
- fix: Add a branch to step 2: "A skill with no rows: run step 6, then record with the source-less `track --artifact NAME --status current --model MODEL` (or say in updates.md that the skill has no registry row and propose one)."

### skill-updater#D8-2
- severity: medium
- dimension: D8
- location: skills/skill-updater/SKILL.md:26
- fix: Spell out how to get the diff. Example: "Diff the upstream path from `merge_base` to `ref`: `gh api 'repos/<o>/<r>/compare/<merge_base>...<ref>' --jq '.files[] | select(.filename | startswith("<path>")) | .patch'`. Classify each hunk."

### skill-updater#D1-1
- severity: low
- dimension: D1
- location: skills/skill-updater/SKILL.md:36
- fix: Keep the full explanation in one place, the step 3 table row. Shorten step 8 to: "Judge the artifact with `skill-judge` when its content changed; the commit must touch `SKILL.md` or `references/` (see step 3)."

### skill-updater#D2-1
- severity: low
- dimension: D2
- location: skills/skill-updater/SKILL.md:50
- fix: Add a short heuristic. Use the rule's own trigger task, phrased as a user would ask it, long enough for the habit to appear (for example a 150-word prose answer for an em dash rule). Count the behavior as present when it appears at least once.

### skill-updater#D3-1
- severity: medium
- dimension: D3
- location: skills/skill-updater/SKILL.md:24
- fix: Add a Gotchas bullet that gives the reason. Example: "Never run a tree search or record `path-moved` on an auth, rate-limit or repo-level error: the tree query fails the same way, and a wrong `new_path` silently redirects every future `upstreams` run."
