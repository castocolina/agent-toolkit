# agentskills-research

Maintainer-only: this skill works only from a checkout of this repo, because it drives `scripts/audit/audit.py` and repo paths. It is deliberately not in the marketplace or the README skills table.

It ingests the Agent Skills docs and the `skills-ref` reference validator from [agentskills/agentskills](https://github.com/agentskills/agentskills) (CC-BY-4.0) into `skills/skill-judge/references/agentskills/`, pinned by commit SHA in `SOURCE.json`, and tells you when `skill-judge`'s rubric needs updating.

## Usage

```bash
bash skills/agentskills-research/scripts/fetch-spec.sh [--dest DIR] [--ref REF] [--rubric FILE] [-h|--help]
```

Run from the repo root; `-h` prints usage, env vars, prerequisites, JSON fields and exit codes. stdout is one JSON object (`ref`, `resolved`, `sha`, `changed`, `unchanged`, `rubric_stale`); status goes to stderr. Exit 0 on success, 1 on any failure (references are rolled back if the failure happened during publish; a later failure leaves the new references in place; a failed rollback is reported on stderr with the backup path). `AGENTSKILLS_SHA` pins a commit; `AGENTSKILLS_RAW_BASE` overrides the download base (used by the tests).

`fetch-spec.sh` needs bash 4+ (it uses `declare -A`), GNU coreutils `sha256sum`, `curl`, `git` and `jq`.

## Tests

Routine check after any change to `scripts/fetch-spec.sh`:

```bash
bash tests/skills/agentskills-research/test-fetch-spec.sh
```

`evals/evals.json` and `evals/trigger-queries.json` hold the behaviour and trigger evals. See `SKILL.md` for the refresh workflow.
