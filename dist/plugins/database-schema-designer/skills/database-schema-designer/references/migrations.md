# Safe live schema changes

Label every migration with its engine and version. Before writing DDL, record the table size, the lock each statement takes, replication lag, the recovery path, and which app versions must run against both schemas.

## Expand-contract for a rename, retype or meaning change

1. Add the new column as nullable. Deploy readers that tolerate both columns everywhere, then deploy code that writes both the old and the new column.
2. Drain every old writer and worker (old pods, queue consumers, cron jobs, other services) before the backfill completes: they write only the old column, so rows they touch go stale behind the backfill.
3. Backfill in bounded, idempotent batches keyed by primary-key range (`WHERE id BETWEEN ? AND ? AND new_col IS NULL`), committing each batch so no long transaction holds locks or replication lag grows. A rerun then skips finished rows.
4. Reconcile: compare counts, NULLs and values between the columns, then fix the rows the old writers changed during the backfill.
5. Switch reads to the new column while dual writes continue, and watch production.
6. Contract: stop writing the old column. In a later deploy, after checking views, triggers, replicas and reports that still read it, drop the old column.

Never copy once and then switch reads while writers still update only the old column: rows written after the copy go stale. Each phase must work with both the previous and the next app version during a rolling deploy.

## Add NOT NULL to a populated column

1. Keep the column nullable. Deploy code that always writes it.
2. Backfill existing NULLs in idempotent batches (step 3 above).
3. Enforce without a long blocking scan, one phase per migration file (each its own committed transaction, each starting with `SET lock_timeout`):
   - PostgreSQL (the current ALTER TABLE page, https://www.postgresql.org/docs/current/sql-altertable.html, gives the scan skip but no version; check the release notes at https://www.postgresql.org/docs/release/ for the oldest version you must support, checked 2026-11-07):
     1. `ALTER TABLE users ADD CONSTRAINT users_phone_nn CHECK (phone IS NOT NULL) NOT VALID;` takes a brief ACCESS EXCLUSIVE lock.
     2. `ALTER TABLE users VALIDATE CONSTRAINT users_phone_nn;` scans under SHARE UPDATE EXCLUSIVE, so reads and writes continue.
     3. `ALTER TABLE users ALTER COLUMN phone SET NOT NULL;` skips the table scan because the valid CHECK proves no NULLs.
     4. `ALTER TABLE users DROP CONSTRAINT users_phone_nn;`

     Never run these phases in one transaction, such as the template's single `BEGIN ... COMMIT`. The ACCESS EXCLUSIVE lock from the first phase is then held through the whole validation scan, which blocks every read and write. PostgreSQL 18+ can skip the CHECK: `ADD CONSTRAINT users_phone_nn NOT NULL phone NOT VALID;`, then `VALIDATE CONSTRAINT users_phone_nn;`.
   - MySQL: `MODIFY` replaces the whole column definition. Anything you do not restate is dropped: DEFAULT, COMMENT, CHARACTER SET and COLLATE, generated and ON UPDATE clauses, and INVISIBLE. Before writing the statement, run `SHOW CREATE TABLE users` and copy the full definition, changing only the nullability. An existing `DEFAULT NULL` is the exception: it is invalid on a NOT NULL column, so drop it, or replace it only with a non-NULL default the owner approves, for example `ALTER TABLE users MODIFY phone VARCHAR(32) NOT NULL, ALGORITHM=INPLACE, LOCK=NONE;`. It rebuilds the table. If you leave out a non-default charset, the type changes and INPLACE is rejected.
4. Recovery, per engine. Keep the code path that tolerates NULL until the constraint has held in production.
   - PostgreSQL: one block undoes any phase, whichever one failed: `BEGIN; SET LOCAL lock_timeout = '5s'; ALTER TABLE users DROP CONSTRAINT IF EXISTS users_phone_nn; ALTER TABLE users ALTER COLUMN phone DROP NOT NULL; COMMIT;`. `DROP NOT NULL` is a no-op on a nullable column. The block changes only the catalog under a brief ACCESS EXCLUSIVE lock and loses no data.
   - MySQL: NOT NULL is a column attribute, not a droppable constraint. Rolling back is another in-place rebuild, `ALTER TABLE users MODIFY phone VARCHAR(32) NULL, ALGORITHM=INPLACE, LOCK=NONE;`, restating the full definition from `SHOW CREATE TABLE` as in the forward step. `ALGORITHM=INSTANT` is rejected, and on a large table the rollback takes about as long as the forward change, so never promise an instant rollback.

## Retrofit a tenant composite FK on a live table (PostgreSQL)

Example: make `tasks (organization_id, project_id)` reference `projects (organization_id, id)`. Put each step in its own migration, each starting with `SET lock_timeout`:

1. `CREATE UNIQUE INDEX CONCURRENTLY projects_org_id_uq ON projects (organization_id, id);` This is a non-transactional migration. A non-partial unique index is enough for an FK target, so no constraint is needed.
2. Deploy code that writes a matching `organization_id`. Then list the bad rows with `SELECT t.id FROM tasks t JOIN projects p ON p.id = t.project_id WHERE t.organization_id <> p.organization_id;`, and fix or delete them in batches. These rows are the cross-tenant leaks themselves, so each one needs an owner's decision, not a blind update.
3. `ALTER TABLE tasks ADD CONSTRAINT tasks_org_project_fk FOREIGN KEY (organization_id, project_id) REFERENCES projects (organization_id, id) ON DELETE CASCADE NOT VALID;` Keep the old FK's delete action. From this point, new writes are checked.
4. `ALTER TABLE tasks VALIDATE CONSTRAINT tasks_org_project_fk;` If it fails, step 2 missed a row; the error names the key.
5. `ALTER TABLE tasks DROP CONSTRAINT tasks_project_id_fkey;` drops the old single-column FK.

MySQL has no `NOT VALID`. Add the parent's `UNIQUE KEY (organization_id, id)` and fix the bad rows, then add the FK with `ALGORITHM=COPY`. COPY checks existing rows and fails on an orphan, but it blocks writes for the whole copy, so schedule a write window. INPLACE works only with `foreign_key_checks = 0`, which skips validation, so never use it on live data (https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html, foreign key operations, checked 2026-11-07).

## PostgreSQL lock rules

- Run `SET lock_timeout = '5s';` before DDL and retry on timeout. An `ALTER TABLE` waiting for its ACCESS EXCLUSIVE lock behind one long transaction blocks every later read and write queued behind it, so a stuck migration becomes an outage.
- Most `ALTER TABLE` forms take ACCESS EXCLUSIVE. `ADD FOREIGN KEY` takes SHARE ROW EXCLUSIVE on both tables, which blocks writes. On a big table, add the FK `NOT VALID`, then run `VALIDATE CONSTRAINT`, which takes SHARE UPDATE EXCLUSIVE (plus ROW SHARE on the referenced table). Use the same two steps for a `CHECK`. Commit the `NOT VALID` step before `VALIDATE`, for the reason given under NOT NULL above.
- `ADD COLUMN` with a non-volatile default is metadata-only from PostgreSQL 11 on (https://www.postgresql.org/docs/release/11.0/, checked 2026-11-07). A volatile default such as `clock_timestamp()` rewrites the table (https://www.postgresql.org/docs/current/sql-altertable.html). `ALTER COLUMN TYPE` usually rewrites the table and its indexes, except for binary-coercible changes such as raising a `varchar` limit or `varchar` to `text`.
- `CREATE INDEX` blocks writes but not reads. `CREATE INDEX CONCURRENTLY` blocks neither, but it cannot run inside a transaction block, so mark the migration non-transactional in your migration tool. It also waits for existing transactions that touched the table. If it fails, it leaves an INVALID index that queries ignore but every write still maintains: find it with `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;`, run `DROP INDEX CONCURRENTLY`, and retry.

## MySQL rules

- DDL commits implicitly: `ALTER TABLE`, `CREATE INDEX` and `CREATE TABLE` end the open transaction. A `BEGIN ... ROLLBACK` around a migration does not undo earlier statements, so a failure halfway leaves partial schema. Keep each migration file to one DDL statement, or make each statement idempotent. Confirm the list of statements that commit implicitly for your version in the manual's "Statements That Cause an Implicit Commit" page.
- Always write `ALGORITHM` and `LOCK` explicitly (`ALGORITHM=INSTANT`, or `ALGORITHM=INPLACE, LOCK=NONE`). The explicit clause makes the statement fail when the operation cannot honor it, instead of silently falling back to `COPY`, which blocks writes for the whole rebuild. Say this in the answer, since it is the reason for the clause.
- Even INSTANT and INPLACE take a brief exclusive metadata lock. Behind a long transaction, that wait blocks the table like the PostgreSQL case above, so set `lock_wait_timeout` low for the session. Read https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-performance.html for the lock behavior of your version.

## SQLite table rebuild

SQLite `ALTER TABLE` is limited (see the SQLite gotcha in SKILL.md). For any other change, follow the 12-step procedure at https://www.sqlite.org/lang_altertable.html, condensed here into nine steps, in this order:

1. Start the script with `.bail on` (sqlite3 CLI) so the first error stops it. Then run `PRAGMA foreign_keys = OFF;` outside any transaction, because inside one it is silently ignored.
2. `BEGIN;`, then `CREATE TEMP TABLE gate (ok INTEGER NOT NULL CHECK (ok = 1));`. Every check below (the row-count check in step 5 and the foreign-key check in step 8) inserts its result into `gate`; a failed check inserts 0, which violates the CHECK and raises an error.
3. Save the `sql` of the table's indexes and triggers, and separately of every view that reads it, from `sqlite_schema`.
4. `DROP VIEW` each of those views. `DROP TABLE` removes the table's indexes and triggers but leaves its views, and the rename in step 6 then fails with `error in view ...: no such table`.
5. `CREATE TABLE new_x (...)` in the target shape, then `INSERT INTO new_x (...) SELECT ... FROM x;`, then `INSERT INTO gate SELECT (SELECT count(*) FROM x) = (SELECT count(*) FROM new_x);`
6. `DROP TABLE x;`, then `ALTER TABLE new_x RENAME TO x;`
7. Recreate the saved indexes and triggers, then the saved views.
8. `INSERT INTO gate SELECT NOT EXISTS (SELECT 1 FROM pragma_foreign_key_check);` requires zero FK violations.
9. `COMMIT;`, then `PRAGMA foreign_keys = ON;`. If any statement or check fails, `.bail on` exits before `COMMIT` and the open transaction rolls back. In an application, wrap the same statements in a transaction and run `ROLLBACK` on the first error.

Never rename the old table first and create the new one under the old name: the rename can corrupt references to it in triggers, views and foreign keys.

## Review before shipping

- Rehearse forward and recovery steps on production-like volume, and record the elapsed time and the locks seen.
- A down migration that drops a column or table destroys data written since the up migration. Say so, and prefer a forward fix or a restore point.
