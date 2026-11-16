# Python resolver workflow

Inspect `pyproject.toml`, `requirements*.txt`, `Pipfile`, and lockfiles to identify the resolver that owns the dependency graph. Poetry, Pipenv, uv, and other lockfile owners must update both manifest and lock using their own resolver; environment-only `pip install --upgrade` does not update those lockfiles.

Resolver-specific single-package updates (checked 2026-11-15; confirm flags with each tool's `--help`):

- Poetry: `poetry update <pkg>` re-resolves the named package within the existing `pyproject.toml` constraint and rewrites `poetry.lock` (it does not change `pyproject.toml`; a constraint that excludes the newer version makes it a no-op, so edit the constraint to the approved target first). `--dry-run` outputs the operations without executing them (https://python-poetry.org/docs/cli/#update).
- Pipenv: `pipenv update <pkg>` upgrades the named package and its sub-dependencies in `Pipfile.lock`, then syncs the environment; `pipenv update --outdated` only lists what is out of date (https://pipenv.pypa.io/en/latest/commands.html).
- uv: `uv lock --upgrade-package <pkg>` upgrades one package in `uv.lock` and keeps the other locked versions; `uv lock --upgrade-package <pkg>==<version>` pins an approved target, and `uv lock --dry-run` previews without writing (https://docs.astral.sh/uv/concepts/projects/sync/#upgrading-locked-package-versions; `uv lock --help` run 2026-11-15).
- A `pyproject.toml` next to a requirements lock (`requirements*.txt` compiled by pip-tools or uv, or exported by another tool): the tool that produced the lock owns it. Do not let Poetry, Pipenv or `pip install --upgrade` rewrite it; update the declared constraint and regenerate the lock with the tool that generated it, and say which tool that is in the plan.

When plain pip/requirements files are the owner, update one approved package at a time, pin or bound the resulting version according to project policy, and regenerate any maintained lock/constraints artifact with its documented tool. `pip list --outdated` is discovery, not a compatible resolution plan. Check `pip check`, run project tests/type checks/build, and use `pip-audit` or the project's chosen security scanner.
