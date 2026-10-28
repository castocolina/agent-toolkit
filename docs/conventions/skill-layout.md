# Skill, eval and test layout

Where skill files, evals and tests live, what ships in `dist/`, and how to run each layer.

## What lives in `skills/<name>/`

- `SKILL.md` and `README.md` (both required).
- `references/` for detail loaded on demand.
- `scripts/` for scripts the skill runs.
- `evals/` with `evals.json` (output evals), `trigger-queries.json` (activation queries) and `files/` (input files the evals use).

Nothing else test-related goes in a skill. Script tests and their fixtures live under `tests/`.

## Command evals

Command output evals live in `commands/evals/<command>.json` and use the evals.json shape with `skill_name`, `subject`, optional `context`, and `evals` headers. Their fixture files live in `commands/evals/files/`. Run one with `audit.py run-evals --eval-file commands/evals/<command>.json --runner CMD`; command evals do not support trigger queries. For diagnosis, add `--only ID[,ID...]` to run selected ids only. This writes `summary-output.only.json` instead of `summary-output.json`, so a partial run cannot be mistaken for a full gate result; `--only` is not supported with `--skills`. A diagnosis run still rewrites the per-eval `output/` files under the same `--out` tree, so give it a different `--out` directory than the gate run to keep the committed gate summary consistent with its per-eval files.

## What lives in `tests/`

- `tests/skills/<name>/`: runnable script tests (`test-*.sh` or `test_*.py`) and their fixtures, for example `fixtures/`. Fixtures that need a mutable copy are copied into a `mktemp -d` directory at run time.
- `tests/audit/`: tests for `scripts/audit/audit.py` (`test_audit.py`) and `fixtures/stub-runner.sh`.
- `tests/scripts/`: tests for repo scripts, such as `test_build_plugins.py`.

## What ships in `dist/`

`python3 scripts/build_plugins.py` copies each listed skill directory, agent file and command file into `dist/plugins/<plugin>/`. It excludes `evals/`, `tests/` and `__pycache__/` at any depth, so evals and tests are not shipped. `dist/` is rebuilt and committed; CI fails when it is stale.

## Where eval run outputs go

Never inside a skill. `audit.py run-evals` writes to its `--out` directory, for example `docs/audit/<date>-<plan>/evals/<skill>/`. Under `docs/audit/` only `summary-*.json`, `prompt-*.txt`, `merged.json`, `report.md`, `check.json` and `judgements/` are committed. Per-eval `output/` trees are git-ignored (`docs/audit/**/output/`).

## How to run each layer

Audit tool tests:

```bash
python3 -m unittest discover -s tests/audit -v
```

Repo script tests:

```bash
python3 -m unittest discover -s tests/scripts -v
```

Skill script tests (one skill at a time):

```bash
bash tests/skills/<name>/test-*.sh
python3 -m unittest discover -s tests/skills/<name> -p 'test_*.py'
```

For example:

```bash
bash tests/skills/agentskills-research/test-fetch-spec.sh
```

Presence checks (`missing_evals`, `missing_script_tests`):

```bash
python3 scripts/audit/audit.py check --strict
```

`missing_script_tests` fires when a skill has files under `scripts/` but `tests/skills/<name>/` has no `test-*.sh` or `test_*.py`.

Output evals and trigger queries (see `python3 scripts/audit/audit.py run-evals -h`):

```bash
python3 scripts/audit/audit.py run-evals --skills <a,b> --runner "$(python3 scripts/audit/audit.py pi-cmd runner)" [--triggers] [--runs N] [--timeout S] [--out DIR] [--fail-under 0.8]
```

`run-evals --skills` looks for an eval's `files` under `skills/<name>/`, then under `skills/<name>/evals/files/`. `run-evals --eval-file` resolves fixture files only under `commands/evals/files/` and inlines its declared subject and context documents.

Build check:

```bash
python3 scripts/build_plugins.py
git status   # must be clean
```
