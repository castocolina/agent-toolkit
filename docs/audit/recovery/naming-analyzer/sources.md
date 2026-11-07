# naming-analyzer: sources (checked 2026-11-07)

## Origin

- The skill comes from the fork origin `softaworks/agent-toolkit`, added in commit `40d4469f` (2026-01-19, Leonardo Flores, @leonardocouy), path `skills/naming-analyzer` (`README.md`, `SKILL.md`). It exists at the fork point `3027f20f` and is byte-identical to the baseline `dbff837f` (`git diff --stat 3027f20f dbff837f -- skills/naming-analyzer` is empty).
- Upstream `main` still has only that one commit for the path (`gh api repos/softaworks/agent-toolkit/commits?path=skills/naming-analyzer&sha=main`), so there is no upstream change to review.
- No other author or external source is credited in the original and none of its text is distinctive enough for a phrase search: a tagline, per-language casing lists and a report template. The current SKILL.md (evidence procedure, hidden consumers, scales) was written in this repo and cites no outside text.
- The registry has no row for `naming-analyzer` today and the skill README has no Credits section.

## Missing credit line

`skills/naming-analyzer/README.md` needs a `## Credits` section with this exact line (same wording as `skills/gemini/README.md` and `skills/database-schema-designer/README.md`):

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The facts of SKILL.md were checked against the official documentation pages listed below; the same section can carry one sentence saying so, as the two README files above do.

## Proposed registry rows (verbatim JSON)

Origin row (`credit` text appears in the line above, which `check --strict` needs):

```json
{"skill": "naming-analyzer", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/naming-analyzer", "ref": "main", "credit": "softaworks/agent-toolkit"}
```

Official documentation pages used for facts.md, one `unversioned` row each (the coordinator may merge pages of one vendor into fewer rows; `upstreams` never marks them stale):

```json
{"skill": "naming-analyzer", "kind": "unversioned", "source": "PEP 8, Style Guide for Python Code: https://peps.python.org/pep-0008/", "ref": null, "credit": "Python Software Foundation"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Effective Go: https://go.dev/doc/effective_go", "ref": null, "credit": "The Go Authors"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "The Go Programming Language Specification, Exported identifiers: https://go.dev/ref/spec", "ref": null, "credit": "The Go Authors"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Go package encoding/json: https://pkg.go.dev/encoding/json", "ref": null, "credit": "The Go Authors"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "TypeScript Handbook, Do's and Don'ts: https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html", "ref": null, "credit": "Microsoft"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "typescript-eslint rule naming-convention: https://typescript-eslint.io/rules/naming-convention/", "ref": null, "credit": "typescript-eslint"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Google TypeScript Style Guide: https://google.github.io/styleguide/tsguide.html", "ref": null, "credit": "Google"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Protocol Buffers Language Guide (proto3): https://protobuf.dev/programming-guides/proto3/", "ref": null, "credit": "Google"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "ProtoJSON Format: https://protobuf.dev/programming-guides/json/", "ref": null, "credit": "Google"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Protocol Buffers Python generated code: https://protobuf.dev/reference/python/python-generated/", "ref": null, "credit": "Google"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Django model field reference, db_column: https://docs.djangoproject.com/en/stable/ref/models/fields/", "ref": null, "credit": "Django Software Foundation"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Django django-admin makemigrations: https://docs.djangoproject.com/en/stable/ref/django-admin/", "ref": null, "credit": "Django Software Foundation"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Django migration operations, RenameField: https://docs.djangoproject.com/en/stable/ref/migration-operations/", "ref": null, "credit": "Django Software Foundation"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Django migration questioner source: https://github.com/django/django/blob/main/django/db/migrations/questioner.py", "ref": null, "credit": "Django Software Foundation"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "SQLAlchemy ORM Declarative Table: https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html", "ref": null, "credit": "SQLAlchemy authors"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Spring Framework, Classpath scanning and managed components: https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html", "ref": null, "credit": "Broadcom (Spring)"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Spring Framework, Fine-tuning annotation-based autowiring with qualifiers: https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired-qualifiers.html", "ref": null, "credit": "Broadcom (Spring)"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "pytest fixtures reference: https://docs.pytest.org/en/stable/reference/fixtures.html", "ref": null, "credit": "pytest-dev"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "pytest API reference, python_files: https://docs.pytest.org/en/stable/reference/reference.html", "ref": null, "credit": "pytest-dev"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "pytest MonkeyPatch source: https://github.com/pytest-dev/pytest/blob/main/src/_pytest/monkeypatch.py", "ref": null, "credit": "pytest-dev"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Python unittest.mock, patch and where to patch: https://docs.python.org/3/library/unittest.mock.html", "ref": null, "credit": "Python Software Foundation"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Python tutorial, Modules (__all__): https://docs.python.org/3/tutorial/modules.html", "ref": null, "credit": "Python Software Foundation"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Python Packaging User Guide, Entry points specification: https://packaging.python.org/en/latest/specifications/entry-points/", "ref": null, "credit": "Python Packaging Authority"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Python Packaging User Guide, pyproject.toml specification: https://packaging.python.org/en/latest/specifications/pyproject-toml/", "ref": null, "credit": "Python Packaging Authority"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Next.js file-system conventions, page.js: https://nextjs.org/docs/app/api-reference/file-conventions/page", "ref": null, "credit": "Vercel"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Next.js file-system conventions, route.js: https://nextjs.org/docs/app/api-reference/file-conventions/route", "ref": null, "credit": "Vercel"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Rails Guides, Autoloading and Reloading Constants: https://guides.rubyonrails.org/autoloading_and_reloading_constants.html", "ref": null, "credit": "Rails contributors"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Celery user guide, Tasks: https://docs.celeryq.dev/en/stable/userguide/tasks.html", "ref": null, "credit": "Celery Project"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Celery worker consumer source (unregistered task message): https://github.com/celery/celery/blob/main/celery/worker/consumer/consumer.py", "ref": null, "credit": "Celery Project"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "RQ documentation, Jobs: https://python-rq.org/docs/jobs/", "ref": null, "credit": "RQ"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "NestJS custom providers: https://docs.nestjs.com/fundamentals/custom-providers", "ref": null, "credit": "NestJS"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Angular API, InjectionToken: https://angular.dev/api/core/InjectionToken", "ref": null, "credit": "Google (Angular)"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Pydantic Fields: https://pydantic.dev/docs/validation/latest/concepts/fields/", "ref": null, "credit": "Pydantic Services"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "Jackson Annotations wiki, @JsonProperty: https://github.com/FasterXML/jackson-annotations/wiki/Jackson-Annotations", "ref": null, "credit": "FasterXML"}
{"skill": "naming-analyzer", "kind": "unversioned", "source": "LibCST codemods tutorial: https://libcst.readthedocs.io/en/latest/codemods_tutorial.html", "ref": null, "credit": "Instagram (Meta)"}
```

## skill-updater style review (review only, no `track` call)

The skill has no registry row yet, so `upstreams` would return nothing for it; I ran no `track`. Procedure step 2 case "credit line naming an upstream with no row" does not apply either (no credit line exists), so both the row and the line are proposals above.

Upstream change since the fork point: none (one commit, the one we already have). Adopt, adapt, ignore items for the restore brief:

- adopt: none (no upstream change).
- adapt: none.
- ignore: nothing to ignore upstream-wise. Local notes for the brief, from facts.md: (1) replace "the TypeScript handbook style" in Workflow step 1 with a pointer to the project's lint config or a named style guide (the handbook has no naming rules); (2) correct the Angular half of "Angular and NestJS string injection tokens behave the same way" in Hidden consumers (an `InjectionToken` string is only a label); (3) optional: say Effective Go is not actively updated, so the project's own Go notes come first.
- Model-validity pass: the skill's rules correct model habits only in the sense of "never present one rename as settled" and "never rename to match one caller". Its evals `name-only-ambiguity` and `conflicting-callers` already exercise them; I made no probe run (no lane dispatch is allowed to me), so the pass is left to the coordinator's skill-updater run.

Restore brief from the record: no `restore-*` rows. Pending user answers: `s008 Magic Number Detection` (purpose-change-pending) and the `drop-pending` rows `s004`, `s006`, `s007`, `s011`, `s015`, `s016`, `s021`, `s031`.
