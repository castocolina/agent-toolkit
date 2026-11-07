# Database Schema Designer

Designs and reviews SQL and MongoDB schemas: tables or collections, keys, constraints, multi-tenant isolation, query-aligned indexes and staged live migrations. PostgreSQL is the default engine. MySQL, SQLite and MongoDB differences are called out where they change the design.

## When to use

- Sketching tables for a new app from a list of entities or screens
- Choosing between embedding and referencing in MongoDB
- Reviewing an existing schema for integrity, tenancy and index gaps
- Planning a change to a live table (NOT NULL, rename, retype, new index)

It is not for REST or GraphQL API models, ORM classes for an existing schema, BI dashboards, database deployment, backups or connection pooling, or tuning a query without a schema change.

## Example requests

```
design the tables for a tiny online shop
review this schema for a multi-tenant SaaS
make users.phone NOT NULL on a live table with millions of rows
should MongoDB comments be embedded in the post document?
```

Include the engine and version, rough row counts, whether the data is live, and the queries that matter. When these are missing, the skill states labeled assumptions instead of asking.

## What is in the skill

| File | Purpose |
|------|---------|
| `SKILL.md` | Defaults, the design workflow and engine gotchas |
| `references/migrations.md` | Expand-contract, NOT NULL on live tables, PostgreSQL and MySQL lock rules |
| `references/schema-design-checklist.md` | Review checks and report format |
| `references/schema-fundamentals.md` | Normal forms, keys, foreign-key actions, junction tables, MongoDB index syntax, MySQL EXPLAIN reading and a basic-design checklist |
| `assets/templates/migration-template.sql` | PostgreSQL migration skeleton with a MySQL variant (SQLite uses the rebuild order in `migrations.md`) |

## Install

Claude Code: `cp -r skills/database-schema-designer ~/.claude/skills/`

claude.ai: add `SKILL.md` to project knowledge or paste it into the conversation.

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Engine facts were checked against the official documentation of PostgreSQL (PostgreSQL Global Development Group), MySQL (Oracle MySQL), SQLite and MongoDB.

## License

MIT
