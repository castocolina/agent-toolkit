# Batch 19

## database-schema-designer (skill)

### database-schema-designer#D7-1
- severity: medium
- dimension: D7
- location: skills/database-schema-designer/evals/evals.json:20
- fix: Assert that tenant-inconsistent user/project/task relationships are rejected by the generated constraints or an explicitly justified equivalent. Add a MongoDB case involving unbounded growth or the document-size boundary and verify the embedding/reference decision.

### database-schema-designer#D8-1
- severity: high
- dimension: D8
- location: skills/database-schema-designer/references/schema-design-checklist.md:57
- fix: Replace the blanket requirement with an engine- and workload-specific check of existing leading-prefix coverage, join and parent-delete costs, and write amplification. Explicitly allow a documented decision not to add an index.

### database-schema-designer#D8-2
- severity: high
- dimension: D8
- location: skills/database-schema-designer/references/schema-design-checklist.md:39
- fix: Distinguish instants from civil dates and local wall-clock times. Default PostgreSQL instant fields to TIMESTAMPTZ with an explicit input/output timezone policy, update the template accordingly, and document engine-specific alternatives rather than equating TIMESTAMP with UTC.

### database-schema-designer#D8-1
- severity: high
- dimension: D8
- location: skills/database-schema-designer/references/schema-design-checklist.md:57
- fix: Reword to 'FK indexes justified by join/parent-delete cost and write impact' to match the SKILL.md policy

### database-schema-designer#D1-1
- severity: medium
- dimension: D1
- location: skills/database-schema-designer/references/schema-design-checklist.md:19
- fix: Replace the generic checklist content with compact, decision-oriented checks for tenant isolation, nullable uniqueness, soft deletes, query-prefix coverage, lock behavior, concurrent writes during backfill, and recovery limitations.

### database-schema-designer#D1-1
- severity: medium
- dimension: D1
- location: skills/database-schema-designer/references/schema-design-checklist.md:107
- fix: Prune the Security, Performance and Documentation sections to schema-relevant checks only

### database-schema-designer#D2-1
- severity: low
- dimension: D2
- location: skills/database-schema-designer/SKILL.md:13
- fix: Add default labeled assumptions (e.g. single-tenant, moderate scale, new schema) to state when context is missing

### database-schema-designer#D3-1
- severity: low
- dimension: D3
- location: skills/database-schema-designer/SKILL.md:28
- fix: Define it (columns whose values are opaque tokens or secrets) and add a one-line example

### database-schema-designer#D5-1
- severity: medium
- dimension: D5
- location: skills/database-schema-designer/SKILL.md:34
- fix: Delete the pointer or add the engine-specific reference files it names

### database-schema-designer#D6-1
- severity: low
- dimension: D6
- location: skills/database-schema-designer/SKILL.md:17
- fix: Default to EXPLAIN (ANALYZE) on PostgreSQL and name the per-engine equivalents
