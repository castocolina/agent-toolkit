# Python resolver workflow

Inspect `pyproject.toml`, `requirements*.txt`, `Pipfile`, and lockfiles to identify the resolver that owns the dependency graph. Poetry, Pipenv, uv, and other lockfile owners must update both manifest and lock using their own resolver; environment-only `pip install --upgrade` does not update those lockfiles.

When plain pip/requirements files are the owner, update one approved package at a time, pin or bound the resulting version according to project policy, and regenerate any maintained lock/constraints artifact with its documented tool. `pip list --outdated` is discovery, not a compatible resolution plan. Check `pip check`, run project tests/type checks/build, and use `pip-audit` or the project's chosen security scanner.
