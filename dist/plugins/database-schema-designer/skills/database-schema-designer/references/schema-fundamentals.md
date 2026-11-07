# Schema design fundamentals

Background the user may ask for by name: a basic-design checklist for a sketch. It restates textbook rules in this skill's terms. Where SKILL.md has an engine-specific gotcha, the gotcha wins; this file points to it instead of repeating it. Examples are PostgreSQL unless a line says otherwise.

Two old absolutes are deliberately not restored: "index every foreign key" is replaced by the per-engine FK indexing gotcha, and "always write a DOWN migration" by the down-migration data-loss warning in `references/migrations.md`.

## Basic-design checklist for a sketch

Keys and relationships:

- [ ] Every relationship has an FK, and each FK has a deliberate `ON DELETE`
- [ ] Each FK is indexed or its skip is explained (FK indexing gotcha)

Types and constraints:

- [ ] Column types fit the data: exact type for money, integers for counts, `VARCHAR` sized for the data
- [ ] Instants, civil dates and local times follow the Time types gotcha; timestamps in UTC means `timestamptz`, not plain `timestamp`
- [ ] `NOT NULL` on required fields, `UNIQUE` where the domain needs it, `CHECK` for validation
- [ ] `created_at` and `updated_at` where the table needs history

Indexes:

- [ ] Each index names a query: WHERE columns, ORDER BY columns, or an FK path. Composite order is equality columns first, then range or sort (checklist check 6)

Delivery:

- [ ] Migration scripts have a recovery path, and a down script that drops data says so
- [ ] Tested on staging with production-like volume

For a review of an existing schema, use `references/schema-design-checklist.md` instead.
