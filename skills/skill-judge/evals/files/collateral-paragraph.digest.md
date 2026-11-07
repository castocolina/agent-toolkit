=== previous-version digest: collateral-paragraph at evals/files/collateral-paragraph.previous ===
sections:
- evals/files/collateral-paragraph/SKILL.md.txt: # Credential Rotation | Replace the password of one database role without dropping live connections.
- evals/files/collateral-paragraph/SKILL.md.txt: ## Workflow | 1. Create the new password in the secret store and keep the old one active.
- evals/files/collateral-paragraph/SKILL.md.txt: ## Rollback | Restore the previous secret version within 15 minutes of the first connection error. Then restart the pods again to drop
- evals/files/collateral-paragraph/SKILL.md.txt: ## Verification | After the last pod restarts, query `pg_stat_activity` for sessions that still authenticate with the old password. The li
removed units (1, showing 1):
- para:d822fccf evals/files/collateral-paragraph/SKILL.md.txt: If the error rate stays above 1% after the restore, page the database on-call and keep both passwords valid until they confirm. Never delete the old secret version before the on-call confirms, because the audit trail needs it for 90 days.
removed or reduced files:
- none
record: none
