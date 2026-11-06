# Customer Data Retention

It is important to note that, in order to ensure that our organisation remains compliant at all times, all customer exports must be deleted from shared storage no later than the number of days that has been set in the `RETENTION_DAYS` setting, unless the export is subject to an active legal hold, in which case it must not be deleted under any circumstances until the legal team has released the hold.

Teams should, wherever it is reasonably possible for them to do so, make use of the `export-purge` job rather than deleting exports by hand, because manual deletions are not recorded in the audit log.

Authorised staff may, if they choose to, request a one-off extension of up to 30 days by opening a ticket in the DATA queue.

When someone attempts to download an export that is under a legal hold, the portal will display the message "Export blocked: legal hold active" and the download will not proceed.
