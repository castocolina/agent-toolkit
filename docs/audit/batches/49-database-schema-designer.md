# Batch 49

## database-schema-designer (skill)

### database-schema-designer#D7-1
- severity: low
- dimension: D7
- location: skills/database-schema-designer/evals/trigger-queries.json
- fix: Rewrite the negatives as realistic near-misses that include file paths and context, for example "this query in reports/monthly.sql takes 9s on prod, here's the EXPLAIN, can you speed it up without migrations?". Add an output eval for a SQLite column-type change that needs the 12-step rebuild.

### database-schema-designer#D8-1
- severity: medium
- dimension: D8
- location: skills/database-schema-designer/SKILL.md:24
- fix: Change step 3 to: "Start PostgreSQL and MySQL migration files from assets/templates/migration-template.sql. For SQLite, skip the template and write the rebuild in the order given in references/migrations.md#sqlite-table-rebuild, with the PRAGMA outside the transaction." Alternatively, add a SQLite variant to the template.

### database-schema-designer#D8-2
- severity: low
- dimension: D8
- location: skills/database-schema-designer/SKILL.md:25
- fix: Add a minimal self-check for sketches: "Before answering, confirm every named entity has a table, every FK has an ON DELETE, money and instant columns use the gotcha types, and each index names its query."

### database-schema-designer#D8-1
- severity: high
- dimension: D8
- location: skills/database-schema-designer/SKILL.md:43
- fix: Default to non-executing EXPLAIN for MySQL UPDATE/DELETE. Permit EXPLAIN ANALYZE for DML only on disposable production-like data, or inside an explicit transaction followed by ROLLBACK after confirming that all affected tables and trigger effects are transactional. Warn that non-transactional side effects cannot be undone.

### database-schema-designer#D1-1
- severity: low
- dimension: D1
- location: skills/database-schema-designer/SKILL.md:39
- fix: Delete these two sentences, because the model already knows them. Keep the expert part: SQLite DECIMAL gets NUMERIC affinity and stores 0.1 as REAL, so use INTEGER minor units with a CHECK; MongoDB uses Decimal128; always store a currency column.

### database-schema-designer#D1-2
- severity: low
- dimension: D1
- location: skills/database-schema-designer/SKILL.md:36
- fix: Cut this to one clause and keep only the non-obvious fix: "For a nullable column that must be unique when missing too, use PostgreSQL 15+ UNIQUE NULLS NOT DISTINCT or make it NOT NULL."

### database-schema-designer#D2-1
- severity: medium
- dimension: D2
- location: skills/database-schema-designer/SKILL.md:3
- fix: Add a brief embed-or-reference rule to workflow step 1. Embed when the child is read with the parent, bounded in size, owned only by that parent and must update atomically with it. Reference when the child is shared across parents, grows without bound, is queried on its own or is updated independently at high rates.

### database-schema-designer#D1-1
- severity: medium
- dimension: D1
- location: skills/database-schema-designer/SKILL.md:39
- fix: Compress the familiar portion to “PostgreSQL/MySQL: fixed-scale NUMERIC/DECIMAL, never floating point.” Retain the SQLite NUMERIC-affinity counterexample, integer-minor-unit requirements, MongoDB Decimal128 guidance and currency requirement.

### database-schema-designer#D6-1
- severity: medium
- dimension: D6
- location: skills/database-schema-designer/SKILL.md:11
- fix: Limit the no-question rule to the four routine design defaults. For live changes, require owner-confirmed facts before generating executable transformations whose correctness depends on unknown data meaning, such as a historical time zone or NULL replacement. Until confirmed, provide diagnostic SQL and a staged plan rather than an invented mutating statement.
