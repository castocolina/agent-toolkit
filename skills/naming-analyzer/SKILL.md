---
name: naming-analyzer
description: Review code identifiers (variables, functions, classes, booleans, constants, fields, files) and suggest clearer names backed by the implementation and its call sites, with a confidence and a compatibility risk for each rename. Use when asked to review naming, "is this name misleading", "better name for X", to clarify abbreviations or hidden units (`timeout`, `ttl`, `delay`, `createdAt`), to check a getter that writes, to fix boolean polarity, or to check names against project conventions, even when the user only pastes code and asks if it reads well. Returns a rename table and edits nothing. Not for applying renames or codemods across a repo (an IDE rename or a codemod tool such as LibCST does that), database or API migrations, product or brand naming, or formatting and style guides.
---

# Naming Analyzer

A name is a contract with every reader and with every consumer the compiler cannot see. Compare what the name promises with what the code does, and report renames with their evidence. Never edit files: this skill reviews; renames go through the user's IDE rename or a codemod after they approve the table.

## Workflow

0. **Scope and triage.** For a folder- or repo-wide request, list first the identifiers whose behavior contradicts the name or that cross a boundary, and leave purely local abbreviations last. Report at most the top 10 issues, ranked by the order of the Decide table, then say how many more candidates you found and that the user can ask for the next batch or name a path. Cutting the list never cuts the search: every name you report still gets the repo and string-literal search of step 1, except an identifier whose definition and uses show it is a lexical local (never exported, no string-based access), which gets a scope-local search; members, exported names and anything unproven get the full search.
1. **Collect evidence for each identifier**, stopping once its meaning is settled:
   - Definition: type, unit, nullability, time basis (UTC or local, epoch seconds or milliseconds).
   - Transformations: where the value is converted (`/ 1000`, `.astimezone()`, `or None`). The name must match the value at that point, not at its source.
   - Callers: what each call site assumes. Read the callers in the file, then search the repo for the name as a symbol and as a string literal.
   - Boundaries: does the name cross serialization, persistence, a public API, a framework convention, or string-key access? See "Hidden consumers".
   - Convention: what nearby code does for the same kind of symbol. If the repo has no established pattern, follow the Convention layers order in [references/naming-guidelines.md](references/naming-guidelines.md): project first, then the framework's, then the language's dominant convention (PEP 8, Effective Go; for TypeScript, the project's lint config, the `@typescript-eslint/naming-convention` rule, else a named guide such as the [Google TypeScript style guide](https://google.github.io/styleguide/tsguide.html), checked 2026-11-07, because the TypeScript handbook prescribes no identifier naming), then an industry standard, and write "no project convention found; using <convention>" in the report.
2. **Decide**, first matching row wins:

   | Evidence | Verdict |
   |---|---|
   | Behavior contradicts the name (a getter that writes, `isValid` that throws, `count` holding a list) | Priority 1: name the effect, or split query from command |
   | Callers disagree about the meaning (one reads `timeout` as seconds, another as ms) | Report the conflict as a bug; give one candidate name per meaning; confidence `tentative` until the owner confirms. Never rename to match one caller: that hides the bug |
   | The code and tests do not establish the meaning (a name-only snippet) | Ask one focused question, or list candidates marked `tentative` with the fact that would settle each; never present one rename as settled |
   | The name crosses a contract boundary | Keep the external name; propose a local alias or mapping (see the compatibility scale) |
   | Conventional and clear in context (`i`, `x`, `id`, `ETag`, `URL`, `req`/`res` in a handler) | Keep, and say no change is warranted |
   | Violates the project's convention for its kind, or the language's when the project has none (class `user_profile`, constant `max`) | Rename to the convention's form (`UserProfile`, `MAX_RETRIES`), with its compatibility level |
   | Otherwise | Role plus unit |

   Read only the section of [references/naming-guidelines.md](references/naming-guidelines.md) for the case at hand: Priority classes when you assign a Priority class, Boolean names when you choose a boolean name, Acceptable abbreviations when you decide whether a short or abbreviated name is acceptable, Convention fallback tree when you name a symbol with no project convention, Convention splits when you find a convention split across the repo, What not to flag or suggest before you propose a vague-name, single-letter or class-suffix rename, What to look for as the issue list when the user asks for a broad review. Do not load it when the Decide row already keeps the name.

3. **Rate** confidence and compatibility from the evidence you actually gathered, using the scales below, then **report** and end with the counts line from that reference (it drops its last clause when nothing was cut). Report the table with the columns of the worked example below (Priority, Location, Current → proposed, Evidence, Confidence, Compatibility); a keep row has an em dash (—) in Priority. Before reporting a rename that is only less clear, not misleading, ask: does the clarity gain justify the churn at this compatibility level? A `local` rename usually does; a `hidden` or `contract` one rarely does, so keep it and note why.

## Cases where the evidence changes the answer

| Code shows | Naive verdict | Correct verdict |
|---|---|---|
| `expiresAt = 3600`, later `now + expiresAt` | rename to `expiryTime` | it is a duration, not an instant: `ttlSeconds` if `now` is established as seconds, `ttlMs` if milliseconds; otherwise name it `ttl` tentatively and ask the unit |
| `createdAt` written with `datetime.now()` (naive local) and compared with UTC timestamps elsewhere | keep | flag the time-basis bug; `created_at_local` only if the value stays local, otherwise fix the write |
| `getUser(id)` returns `None` when missing, beside `findOrder` that also returns `None` | keep `get` | follow the repo's pairing (`find*` may be absent, `get*` raises): `findUser`; with no such pairing, keep `get` and suggest a return-type annotation |
| `tempDir` that is never deleted and is reused across runs | keep | `cacheDir` only if the contents are shown disposable or reconstructible (rebuilt on a miss, safe to delete); persistence alone is not enough. Otherwise ask what it stores, or offer `stateDir` (durable app state) or `workspaceDir` (persistent working files), each tied to that evidence |
| `isNotHidden`, or `disableRetry = false` defaults | add `is` | flip to positive polarity: `isNotHidden` → `isVisible` is a spelling-only change (same truth value), but `disableRetry` → `retryEnabled` inverts meaning, so every default, read, write and test must flip (`retryEnabled = !disableRetry`; default `false` becomes `true`). State that mapping and list those sites; this is not safe as a symbol-only IDE rename, which would turn `disableRetry = false` into `retryEnabled = false`. Map external config or wire keys at the boundary |
| `active` field without `is` | rename to `isActive` | keep: a missing prefix is a convention, not a defect, and the field is often a column or JSON key |
| `userId` that some callers fill with an email | rename to `userKey` | report competing meanings first; the rename depends on which one wins |

## Hidden consumers

These consumers miss ordinary symbol search and IDE rename, so an identifier that looks private can still be a runtime contract. Search for the string, not only the symbol.

- **Serialized fields** (JSON, GraphQL schema, OpenAPI, message queues): clients outside the repo read the key. Protobuf wire format uses field numbers, so a field rename is binary-safe but changes the JSON mapping and every generated client.
- **ORM mappings:** a Django field name is the column name unless `db_column` is set. Non-interactive `makemigrations --noinput` cannot confirm a rename, so it emits RemoveField plus AddField, which drops the column's data. That outcome is Django's non-interactive autodetection ([Django makemigrations](https://docs.djangoproject.com/en/stable/ref/django-admin/#makemigrations), checked 2026-11-07); name Django before applying it, because other ORMs differ, and confirm with `python manage.py makemigrations --dry-run` in the project. In SQLAlchemy `amount = Column("amt", Integer)` maps attribute `amount` to column `amt`.
- **String-key and reflective access:** `getattr(obj, name)`, `obj[key]`, `**kwargs` forwarding, template variables (`{{ user.usr_nm }}`), i18n message keys, feature-flag and env-var names, CSS classes and `data-testid` used by tests, log and metric field names that dashboards query. The rename compiles, and the failure shows up at runtime or in another repo.
- **Dependency injection by name:** Spring derives the default bean name from the class name (`UserService` becomes `userService`) and `@Qualifier("userService")` matches it as a string ([Spring naming autodetected components](https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html#beans-scanning-name-generator), checked 2026-11-07); pytest injects fixtures by parameter name, so renaming either side fails (run `pytest --fixtures` and read the live error); NestJS string tokens (`@Inject('CONNECTION')`) are matched as strings, so renaming the string breaks injection ([NestJS custom providers](https://docs.nestjs.com/fundamentals/custom-providers), checked 2026-11-07). An Angular `InjectionToken` is different: its string is only a debug description and identity is the token instance, so rename the token constant and its imports, and the string does not break injection ([Angular InjectionToken](https://angular.dev/api/core/InjectionToken), checked 2026-11-07).
- **Framework-reserved file names:** pytest collects only `test_*.py` or `*_test.py` by default ([pytest python_files](https://docs.pytest.org/en/stable/reference/reference.html#confval-python_files), checked 2026-11-07), so `user_tests.py` is silently skipped; the project may override it: read `python_files` in pytest.ini, tox.ini, setup.cfg or `[tool.pytest.ini_options]`, or run `pytest --collect-only -q`; `conftest.py`, `__init__.py`, Next.js `page.tsx`/`layout.tsx`/`route.ts`, and Rails Zeitwerk (`app/models/user_account.rb` must define `UserAccount`) are discovered by name.
- **Generated code** (`*_pb2.py`, OpenAPI or GraphQL clients): the name comes from the schema. Rename in the schema or not at all; the next generation reverts hand edits.
- **Go visibility and tags:** changing the first letter's case (`userID` to `UserID`) exports or unexports the symbol, and `encoding/json` uses the Go field name as the key unless a `json:"..."` tag is set.
- **String import paths in tests and task queues:** `mock.patch("billing.tasks.send_reminder")` and `monkeypatch.setattr("pkg.mod.func", ...)` name the target as a string, so after a rename the patch fails to resolve or targets a name nothing calls. Celery task names default to `module.function` ([Celery task names](https://docs.celeryq.dev/en/stable/userguide/tasks.html#names), checked 2026-11-07), so jobs already queued under the old name fail after deploy (Celery logs "Received unregistered task"); check explicit `name=` arguments first, and `celery inspect registered` lists the live names. RQ workers must import the function's module and jobs can be enqueued by dotted path, so check `job.func_name` in the project's RQ version to see what a queued job holds before assuming the same failure.
- **Python `__all__`, `importlib` strings, and entry points** in `pyproject.toml`: the import path is the contract.

## Gotchas

- Celery's unregistered-task failure is not assumed for RQ: check the live `job.func_name` first, and do not rate an RQ rename `contract` until that value shows the queued name.
- A plain IDE rename is unsafe for a boolean polarity flip (`isDisabled` to `isEnabled`): the rename keeps every caller's condition, so each one reads the opposite of what it did. Follow the `disableRetry` row of the Cases table and invert every default, read, write and test.
- A symbol rename misses a name read through a string key (`getattr`, `obj[key]`, templates, serializers): nothing links the string to the symbol. Search for the string as listed under "String-key and reflective access" in Hidden consumers.
- A generated client (OpenAPI, protobuf) renames only when the schema changes, and the next generation reverts a hand edit. Change the schema and regenerate, as stated under "Generated code" in Hidden consumers.

## Scales

Confidence:
- `high`: the implementation and every caller found agree with the proposed meaning.
- `medium`: the implementation is read, but caller coverage is partial (dynamic access is possible, or the search was limited).
- `tentative`: name-only or conflicting evidence. Pair it with the question that would settle it.

Compatibility:
- `local`: only in its own scope; any rename tool is safe.
- `repo`: referenced across the repo by symbol; an IDE rename plus a string search is enough.
- `hidden`: a hidden consumer exists; name it, and the rename needs a string search and a test run.
- `contract`: wire, database, public API, generated, or published-package name. Keep the external name and propose an alias (`Field(alias=...)`, a `json:"usr_nm"` tag, `db_column="usr_nm"`, `@JsonProperty`, a deprecated re-export) or a versioned migration; never a plain rename.

## Worked example

```python
class Invoice(Base):
    __tablename__ = "invoices"
    amt = Column(Integer)  # cents

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def get_total(invoice):
    invoice.viewed_at = utcnow()
    session.commit()
    return invoice.amt / 100

for inv in overdue:
    send_reminder(inv.customer, get_total(inv))
```

Evidence: `get_total` writes `viewed_at` and commits, and the reminder loop calls it, so every reminder marks the invoice viewed and commits once per row. `amt` holds cents, maps to column `amt`, and `to_dict` reads attributes by column name, so `amount_cents = Column("amt", Integer)` would keep the column but raise `AttributeError` in `to_dict`; changing `to_dict` to attribute keys would rename the JSON key instead. The safe change is a local alias, not a contract change.

| Priority | Location | Current → proposed | Evidence | Confidence | Compatibility |
|---|---|---|---|---|---|
| 1 | billing.py:8 | `get_total` → split into `mark_viewed(invoice)` and `total_dollars(invoice)` | writes `viewed_at` and commits inside a getter; the reminder loop commits once per invoice | high | repo |
| 2 | billing.py:3 | `amt` → keep; add a read-only `amount_cents` property | unit is cents per the comment; `to_dict` reads `getattr(self, "amt")`, and the column and JSON key are `amt` | medium (JSON consumers outside the repo unknown) | contract |
| — | billing.py:2 | `__tablename__ = "invoices"` → keep | conventional table name, database contract | high | contract |

When nothing warrants a change, say so in one line and list what you checked.
