---
name: database-schema-designer
description: Design and review SQL/NoSQL database schemas, tables, relationships, constraints, query-aligned indexes, and staged migrations. Use when users need data models, normalization, MongoDB embedding choices, or safe schema changes, even if they only describe entities and queries. Not for designing REST API resource models, setting up ORM classes for an existing schema, building data-warehouse dashboards, database deployment, backups, or query-only tuning.
license: MIT
---

# Database Schema Designer

## Decision workflow

When requirements arrive without file/tool evidence, state the assumptions and still provide a concrete schema design from the prompt; label open decisions instead of stopping to request context. Include every named entity as an explicit table/collection unless you explain a deliberate equivalent representation. In a tenant model, define a `users` table independently from tenant membership; a join table such as `organization_users` is not a substitute for users.

1. **Establish context:** identify engine/version, workload, scale, tenancy, retention, consistency needs, and whether the schema is new or live. Default to PostgreSQL DDL unless another engine is named; label dialect-specific syntax.
2. **Model requirements:** list entities, representative reads/writes, integrity invariants, and transaction boundaries. Decide which writes must commit atomically before choosing table/document boundaries.
3. **Choose representation:** prefer SQL when relationships, cross-entity transactions, constraints, or ad hoc queries matter. Consider document storage when access is predominantly aggregate-oriented, fields vary materially, and atomic operations fit within a document. Embed bounded data read/written with its parent; reference independently updated, shared, unbounded, or high-cardinality data. For MongoDB, account for the 16 MB document limit and growth.
4. **Define integrity:** select stable keys, nullability, uniqueness, foreign-key/delete behavior, checks, tenant ownership, soft-delete semantics, and audit fields. For monetary values, use exact decimal (`DECIMAL`/`NUMERIC`) with explicit currency and scale, or integer minor units with an explicit currency and conversion rule; never use floating point. Choose the representation to match the domain and storage/query requirements.
5. **Plan indexes from queries:** map representative filters, joins, sorts, and integrity operations to existing indexes. Check selectivity, column order, write amplification, and execution plans before adding one. Do not index every foreign key or low-selectivity field by reflex; an index may already cover it as a leading composite prefix.
6. **Plan deployment before DDL:** identify lock/rewrite behavior for the specific engine/version, table size, replication impact, rollback path, and compatible application versions. For live column changes use expand-contract; read `references/migrations.md`. Start migration files from `assets/templates/migration-template.sql` and adapt the engine-specific transaction behavior.
7. **Validate:** when reviewing an existing schema or finalizing a design, read `references/schema-design-checklist.md`. Check constraints, tenant boundaries, query coverage, migration safety, and test strategy; disclose assumptions and unresolved trade-offs.

## Engine-specific gotchas

- PostgreSQL live indexes: use `CREATE INDEX CONCURRENTLY` where appropriate; it cannot run inside a transaction block. Check invalid-index cleanup and lock/deployment behavior for the deployed version.
- MySQL: verify InnoDB before relying on foreign keys. DDL commonly causes implicit commits; `BEGIN` does not make arbitrary DDL rollback-safe. Confirm online DDL algorithm/locking support for the exact version and operation.
- Nullable unique constraints differ by engine. PostgreSQL permits multiple NULLs by default; MySQL unique indexes also have NULL-specific behavior. Model whether “unknown” should be repeatable, and use partial/generated-column strategies only with engine-specific validation.
- Tenant relationships must include tenant identity in the enforced relationship or otherwise prevent cross-tenant references; application filters alone are not integrity constraints.
- Soft-delete uniqueness requires deliberate policy. A normal unique constraint still includes deleted rows; use an engine-supported partial unique index or a collision-safe active-key strategy.
- Never change token-like schema semantics silently: migrations and application rollout must preserve old readers/writers until compatibility is demonstrated.

## References

- Existing-schema/final review: `references/schema-design-checklist.md`.
- Live schema evolution: `references/migrations.md`.
- SQL normalization, NoSQL modeling, or physical-index trade-offs: load only the relevant sections of an engine-specific reference if present; keep the design tied to observed access patterns, not textbook normal forms.
