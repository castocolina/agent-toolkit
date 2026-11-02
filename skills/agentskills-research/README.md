# agentskills-research

Maintainer-only: this skill works only from a checkout of this repo, because it drives `scripts/audit/audit.py` and repo paths. It is deliberately not in the marketplace or the README skills table.

It ingests the Agent Skills docs and the `skills-ref` reference validator from [agentskills/agentskills](https://github.com/agentskills/agentskills) (CC-BY-4.0) into `skills/skill-judge/references/agentskills/`, pinned by commit SHA in `SOURCE.json`, and tells you when `skill-judge`'s rubric needs updating.

A second fetcher, `scripts/fetch-claude-specs.sh`, pins the Claude Code `skills`, `sub-agents` and `plugins-reference` pages (code.claude.com, no license grant: only hashes are stored) into `skills/skill-judge/references/claude-code/SOURCE.json` and reports which command and agent profiles are stale. Scope is Claude Code plugins; other hosts (opencode, Codex, Cursor) are a later extension. Detection needs a fetcher run: nothing notices a changed page until someone runs it (`rubric-check` then fails on the digest mismatch).

## Usage

```bash
bash skills/agentskills-research/scripts/fetch-spec.sh [--dest DIR] [--ref REF] [--rubric FILE] [--pages-dir DIR] [-h|--help]
```

Run from the repo root; `-h` prints usage, env vars, prerequisites, JSON fields and exit codes. stdout is one JSON object (`ref`, `resolved`, `sha`, `changed`, `unchanged`, `rubric_stale`, `structure_changed`, `new_pages`, `removed_pages`); status goes to stderr. Use `--pages-dir DIR` to pre-download current in-scope raw pages for structural repairs. Exit 0 on success, 1 on any failure (references are rolled back if the failure happened during publish; a later failure leaves the new references in place; a failed rollback is reported on stderr with the backup path). `AGENTSKILLS_SHA` pins a commit; `AGENTSKILLS_RAW_BASE` overrides the download base (used by the tests).

`fetch-spec.sh` needs bash 4+ (see Gotchas in `SKILL.md`), GNU coreutils `sha256sum`, `curl`, `git` and `jq`.

## Tests

Routine check after any change to `scripts/fetch-spec.sh`:

```bash
bash tests/skills/agentskills-research/test-fetch-spec.sh
```

`evals/evals.json` and `evals/trigger-queries.json` hold the behaviour and trigger evals. See `SKILL.md` for the refresh workflow.
