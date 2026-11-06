# Batch 50

## database-schema-designer (skill)

### database-schema-designer#D7-1
- severity: low
- dimension: D7
- location: skills/database-schema-designer/evals/evals.json
- fix: Remove the skill's own reference files from each eval's `files` list and keep only user inputs under evals/files/. Add an assertion that the run read references/migrations.md, or references/schema-design-checklist.md for the review eval. That tests whether the skill's loading triggers fire rather than handing the reference to the agent.

### database-schema-designer#D8-1
- severity: low
- dimension: D8
- location: skills/database-schema-designer/references/migrations.md:12
- fix: Rewrite as: 'Contract: stop writing the old column; in a later deploy, after checking views, triggers, replicas and reports that still read it, drop the old column.'

### database-schema-designer#D8-2
- severity: low
- dimension: D8
- location: skills/database-schema-designer/references/migrations.md:31
- fix: Use the section's running example so that the forward and recovery steps match: give the MySQL forward statement `ALTER TABLE users MODIFY phone VARCHAR(32) NOT NULL, ALGORITHM=INPLACE, LOCK=NONE;` and the rollback `ALTER TABLE users MODIFY phone VARCHAR(32) NULL, ALGORITHM=INPLACE, LOCK=NONE;`. Note that the column's full type and attributes must be restated.

### database-schema-designer#D8-1
- severity: high
- dimension: D8
- location: skills/database-schema-designer/references/migrations.md:31
- fix: Replace the preservation claim with a warning that MODIFY requires the complete column definition. Require SHOW CREATE TABLE before forward and recovery statements, then repeat the existing type and all attributes except the nullability being changed. For example, preserve an existing DEFAULT 0.00 with `ALTER TABLE orders MODIFY COLUMN total DECIMAL(12,2) NULL DEFAULT 0.00, ALGORITHM=INPLACE, LOCK=NONE;`, also carrying forward any existing COMMENT or other attributes.

### database-schema-designer#D1-1
- severity: low
- dimension: D1
- location: skills/database-schema-designer/SKILL.md:41
- fix: Delete the PostgreSQL/MySQL 'never floating point' clause, because the model already knows it. Keep the expert parts: SQLite DECIMAL affinity storing 0.1 as REAL, INTEGER minor units with a CHECK, Decimal128 on MongoDB and the currency column.

### database-schema-designer#D2-1
- severity: low
- dimension: D2
- location: skills/database-schema-designer/SKILL.md:42
- fix: Move the five-step MongoDB shape-change procedure into a '## MongoDB shape change' section of references/migrations.md. Keep only the one-line gotcha (no FKs, tenantId in every filter and reference, collMod does not re-check existing docs) in SKILL.md. Then the Gotchas list stays facts, and the procedures stay in the Process layer.

### database-schema-designer#D1-1
- severity: low
- dimension: D1
- location: skills/database-schema-designer/SKILL.md:20
- fix: Remove that generic sentence while retaining the specific users-versus-membership guard and the workflow's concrete MongoDB embedding criteria.
