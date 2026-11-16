# Sources: database-schema-designer (skill)

Checked 2026-11-07.

## Origin

- The skill is byte-identical at the fork point and at the baseline: `git diff 3027f20f dbff837f -- skills/database-schema-designer` is empty. Its origin is softaworks/agent-toolkit (author @leonardocouy, upstream commit 011baf4a "feat: add 7 new skills", 2026-01-18). Catalog listings (mcpservers.org, skills.sh, tessl.io, skillselion) all attribute it to softaworks; none shows an earlier origin, and no distinctive phrase pointed to any other author.
- Credit state: `skills/database-schema-designer/README.md` and `SKILL.md` have no credit line. The root `README.md` line 5 credits the fork ("Fork of softaworks/agent-toolkit by @leonardocouy."). The registry already holds the fork-origin `repo` row (`skill: null`, `softaworks/agent-toolkit`, `main`), and no row names this skill.
- Current text is a near-total rewrite (SKILL.md 732 to 59 lines), so most of today's content is repo-original. The credit is still owed for the baseline structure and the rewritten sections' origin.

## Proposed registry rows

Origin row (a `github-path` row for the upstream skill directory):

```json
{"skill": "database-schema-designer", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/database-schema-designer", "ref": "main", "credit": "softaworks/agent-toolkit"}
```

Official documentation pages used for facts.md (each an `unversioned` row; `source` is title and URL, `credit` is the vendor):

```json
{"skill": "database-schema-designer", "kind": "unversioned", "source": "PostgreSQL documentation, ALTER TABLE: https://www.postgresql.org/docs/current/sql-altertable.html", "ref": null, "credit": "PostgreSQL Global Development Group"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "PostgreSQL documentation, CREATE TABLE: https://www.postgresql.org/docs/current/sql-createtable.html", "ref": null, "credit": "PostgreSQL Global Development Group"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "PostgreSQL documentation, CREATE INDEX: https://www.postgresql.org/docs/current/sql-createindex.html", "ref": null, "credit": "PostgreSQL Global Development Group"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "PostgreSQL documentation, Multicolumn Indexes: https://www.postgresql.org/docs/current/indexes-multicolumn.html", "ref": null, "credit": "PostgreSQL Global Development Group"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "PostgreSQL documentation, Constraints: https://www.postgresql.org/docs/current/ddl-constraints.html", "ref": null, "credit": "PostgreSQL Global Development Group"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "PostgreSQL documentation, Table Partitioning: https://www.postgresql.org/docs/current/ddl-partitioning.html", "ref": null, "credit": "PostgreSQL Global Development Group"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "PostgreSQL documentation, Row Security Policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html", "ref": null, "credit": "PostgreSQL Global Development Group"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "PostgreSQL release notes 11, 15 and 18: https://www.postgresql.org/docs/release/", "ref": null, "credit": "PostgreSQL Global Development Group"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "SQLite documentation, ALTER TABLE: https://www.sqlite.org/lang_altertable.html", "ref": null, "credit": "SQLite"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "SQLite documentation, Foreign Key Support: https://www.sqlite.org/foreignkeys.html", "ref": null, "credit": "SQLite"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "SQLite documentation, Datatypes In SQLite: https://www.sqlite.org/datatype3.html", "ref": null, "credit": "SQLite"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "SQLite release 3.53.0: https://www.sqlite.org/releaselog/3_53_0.html", "ref": null, "credit": "SQLite"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "MySQL 8.4 Reference Manual, Online DDL Operations: https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html", "ref": null, "credit": "Oracle MySQL"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "MySQL 8.4 Reference Manual, FOREIGN KEY Constraints: https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html", "ref": null, "credit": "Oracle MySQL"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "MySQL 8.4 Reference Manual, EXPLAIN: https://dev.mysql.com/doc/refman/8.4/en/explain.html", "ref": null, "credit": "Oracle MySQL"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "MySQL 8.4 Reference Manual, Date and Time Data Types: https://dev.mysql.com/doc/refman/8.4/en/datetime.html", "ref": null, "credit": "Oracle MySQL"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "MySQL 8.4 Reference Manual, FOREIGN KEY Differences: https://dev.mysql.com/doc/refman/8.4/en/ansi-diff-foreign-keys.html", "ref": null, "credit": "Oracle MySQL"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "MongoDB Manual, MongoDB Limits and Thresholds: https://www.mongodb.com/docs/manual/reference/limits/", "ref": null, "credit": "MongoDB"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "MongoDB Manual, BSON Types: https://www.mongodb.com/docs/manual/reference/bson-types/", "ref": null, "credit": "MongoDB"}
{"skill": "database-schema-designer", "kind": "unversioned", "source": "MongoDB Manual, Modify Schema Validation: https://www.mongodb.com/docs/manual/core/schema-validation/update-schema-validation/", "ref": null, "credit": "MongoDB"}
```

Pages listed as pointers in facts.md but not read this session (functions-comparison, create-table-generated-columns, innodb-online-ddl-performance, use-json-schema-query-conditions, sql-explain, integer-types, numeric-type-syntax, support/versioning) are not proposed as rows until read.

## Missing credit line

Yes. Neither `skills/database-schema-designer/README.md` nor `SKILL.md` credits softaworks. Proposed line for `skills/database-schema-designer/README.md` (a new section before `## License`, nothing else touched):

```
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

`audit.py check --strict` compares a row's `credit` verbatim against SKILL.md, README.md and references/*.md; the line contains `softaworks/agent-toolkit`, so the proposed origin row's `credit` matches.

## skill-updater style review (review only, no `track` call)

- Rows: none existed for this skill, so there is nothing for `upstreams` to report. Upstream state read with `gh api repos/softaworks/agent-toolkit/commits?path=skills/database-schema-designer&sha=main`: one commit only (011baf4a, 2026-01-18, the initial add). The upstream skill has not changed since the fork point.
- adopt: none. adapt: none. ignore: the whole upstream text. It is the baseline text, which the repo's judged rewrite replaced on purpose (generic textbook material removed, gotchas and live-migration procedure added), and nothing upstream is newer than that baseline.
- Model-validity pass: not run (this review makes no LLM probe and no `track` call). Rules that exist to counter a model habit and would need a probe in the restore brief: the four `Assumption:` lines, "do not stop to ask", the complete-DDL-per-finding report rule, named placeholders for facts about existing data. Propose the probe at the restore step, not now.
- Restore brief items: the 21 `drop-pending` rows whose reason class is not `wrong` or `stale` go to `references/` as the Step 3 safe default. Rows s013 and s043 stay out (`stale`, `wrong`). Several carry caveats the fixer must apply: s019, s020, s030 (absolute "index every FK" and "always reversible" must not be restored as written), s066 (TIMESTAMP-as-UTC advice superseded), s068 ("ON UPDATE usually CASCADE"), s070 ("most selective column first"), s060 (f-string SQL sample).
- Purpose question for the user: the baseline offered `normalize {table}` and "normalize an existing table" as a purpose; the current description names no normalization. Rows s032, s035, s036 and s064 hold that content. If the user wants the purpose back, those rows become restores and the description needs a normalization trigger.
