# agentskills-research

Maintainer-only: this skill works only from a checkout of this repo, because it drives `scripts/audit/audit.py` and repo paths. It is deliberately not in the marketplace or the README skills table.

It ingests verbatim copies of the Agent Skills docs (CC-BY-4.0) and of the `skills-ref` validator (Apache-2.0) from [agentskills/agentskills](https://github.com/agentskills/agentskills) into `skills/skill-judge/references/agentskills/`, pinned by commit SHA in `SOURCE.json`, and tells you when `skill-judge`'s rubric needs updating.

A second fetcher, `scripts/fetch-claude-specs.sh`, pins the Claude Code `skills`, `sub-agents` and `plugins-reference` pages (code.claude.com, no license grant: only hashes are stored) into `skills/skill-judge/references/claude-code/SOURCE.json` and reports which command and agent profiles are stale. Scope is Claude Code plugins; other hosts (opencode, Codex, Cursor) are a later extension. Detection needs a fetcher run: nothing notices a changed page until someone runs it (`rubric-check` then fails on the digest mismatch).

The Claude Code pages (skills, sub-agents, plugins-reference) are documentation by Anthropic at code.claude.com; this repo stores only their URLs and SHA-256 hashes, never copies.

## Usage

```bash
bash skills/agentskills-research/scripts/fetch-spec.sh [--dest DIR] [--ref REF] [--rubric FILE] [--pages-dir DIR] [-h|--help]
```

Run from the repo root; `-h` prints usage, env vars, prerequisites, JSON fields and exit codes. stdout is one JSON object (`ref`, `resolved`, `sha`, `changed`, `unchanged`, `rubric_stale`, `structure_changed`, `new_pages`, `removed_pages`); status goes to stderr. Use `--pages-dir DIR` to pre-download current in-scope raw pages for structural repairs. Exit 0 on success, 1 on any failure (references are rolled back if the failure happened during publish; a later failure leaves the new references in place; a failed rollback is reported on stderr with the backup path). `AGENTSKILLS_SHA` pins a commit; `AGENTSKILLS_RAW_BASE` overrides the download base (used by the tests).

`fetch-spec.sh` needs bash 4+ (see Gotchas in `SKILL.md`), GNU coreutils `sha256sum`, `curl`, `git` and `jq`.

`fetch-claude-specs.sh` needs more than that (checked 2026-11-15): bash 4.4+ (`mapfile -d` arrived in 4.4, per the [bash NEWS](https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/NEWS)), git 2.36+ (`git worktree list --porcelain -z`, see [git-worktree](https://git-scm.com/docs/git-worktree)) and git 2.31+ (`git rev-parse --path-format`), plus GNU `realpath`, `sha256sum`, `curl` and `jq`. Its `-h` text does not list these.

`skills-ref validate` (the validator the pin SHA feeds, see `SKILL.md`) needs Python 3.11+ (`requires-python = ">=3.11"` in [`skills-ref/pyproject.toml`](https://github.com/agentskills/agentskills/blob/main/skills-ref/pyproject.toml), checked 2026-11-15); `uvx` fetches a matching interpreter itself.

## Tests

Routine check after any change to `scripts/fetch-spec.sh`:

```bash
bash tests/skills/agentskills-research/test-fetch-spec.sh
```

`evals/evals.json` and `evals/trigger-queries.json` hold the behaviour and trigger evals. See `SKILL.md` for the refresh workflow.
