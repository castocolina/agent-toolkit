# Source registry backfill, 2026-10-31

Run with `audit.py track` (plan 6 Task 3 Step 9). `status` is the comparison state `audit.py upstreams` reports; the adopt, adapt or ignore decision is written here. `last_reviewed` is 2026-10-31 on every row. `reviewed_for_model` and `last_upstream_sha` stay null: no model pass and no SHA were recorded in this backfill.

| artifact | source | kind | status | decision |
|----------|--------|------|--------|----------|
| humanizer | blader/humanizer | github | current | none needed (`stale: false`) |
| humanizer | Wikipedia:Signs of AI writing | wikipedia | stale | open: `upstreams` prints `stale: true`; plan 8 Task 6 decides adopt, adapt or ignore |
| react-useeffect | reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md | github-path | current | none needed |
| agent-md-refactor | Matt Pocock, Prompt Idea | unversioned | current | read once; cannot be compared (no commit) |
| domain-name-brainstormer | Ben Aiad, Lenny's Newsletter | unversioned | current | read once; cannot be compared (no commit) |
| writing-clearly-and-concisely | joshuadavidthomas/agent-skills:writing | github-path | current | `upstreams` prints `stale: false`; the plan expected `stale` with an open decision (plan 8 Task 6 Step 2). Open question for plan 8: the user's Orwell port ruling |
| reducing-entropy | joshuadavidthomas/agent-skills:reducing-entropy | github-path | current | none needed |
| crafting-effective-readmes | joshuadavidthomas/agent-skills:crafting-effective-readmes | github-path | current | none needed |
| writing-clearly-and-concisely | obra/the-elements-of-style | github | current | none needed (`stale: false`) |

The `kind: repo` row (softaworks/agent-toolkit, the fork origin) is not an artifact and was not tracked.

## Path probes

The plan expected the two joshuadavidthomas rows `reducing-entropy` and `crafting-effective-readmes` to have moved. Probed with `gh api 'repos/joshuadavidthomas/agent-skills/contents/<name>?ref=main'` on 2026-10-31:

- `writing`: directory, 3 entries
- `reducing-entropy`: directory, 3 entries
- `crafting-effective-readmes`: directory, 6 entries

All three paths exist, so no row is `path-moved` and no `new_path` was recorded. The earlier "No commit found" reading came from a query the old code did not handle; with the current `upstreams` every row returns a commit.

## Checks

- `audit.py upstreams --registry docs/audit/upstream-sources.json` exits 0 and prints no failure row.
- `audit.py detect --state '' --spec-changed false --upstreams <that output>` exits 0.
