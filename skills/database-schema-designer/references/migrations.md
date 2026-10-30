# Safe live schema changes

Label every migration with engine and version. Before DDL, inspect table size, lock/rewrite behavior, replication lag, rollback options, and application compatibility. A transaction does not make all DDL reversible: MySQL DDL commonly implicitly commits; PostgreSQL supports transactional DDL for many operations, but `CREATE INDEX CONCURRENTLY` is an exception.

## Expand-contract column change

For a live rename/retype, use this order:

1. Add the new nullable column; deploy compatible code that writes both old and new fields.
2. Backfill in bounded, restartable batches. Track progress and avoid long transactions/replication spikes.
3. Reconcile concurrent writes and validate counts, nulls, and value equivalence.
4. Switch reads to the new column while dual writes remain; observe production behavior.
5. Stop old-column writes only after all old application versions/workers are gone. Keep a compatibility window.
6. Remove old-column reads and drop the old column in a later deployment after backup/rollback and dependency checks.

Never copy once and switch reads while writers still update only the old column: that leaves new data stale. Make each phase safe with both the old and new application version during rolling deploys.

## Migration review

- Make backfills bounded, idempotent, observable, and resumable.
- Add constraints in a staged manner when validation or table scans can block writes.
- Use engine/version-appropriate online DDL; verify actual lock behavior, not a generic “online” label.
- Test forward and recovery paths against production-like data volume. A down migration that discards user data is not a safe rollback; state that limitation.
- Follow `assets/templates/migration-template.sql` as a starting point, not as proof that the chosen engine supports transactional rollback.
