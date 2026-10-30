# Recommend whether stale upstream sources merit review

Assess stale upstream changes for the audit-upstream issue. Make recommendations only; this does not authorize applying any update.

## Evidence you may use

- `.audit-upstream/` change text and links prepared for each stale row.
- The matching rows from `upstreams.json`, including each row's exact `skill|source` key, source kind, source and freshness dates.
- The associated repository skill files, solely to explain relevance to that skill.

Do not use network access, general recollection, or facts absent from these files. A recommendation of `update` is not approval; only a later explicit `approved_upstreams` dispatch authorizes a row to be applied.

## Exact output

Print exactly one JSON array on stdout with one object for every stale row; the caller captures stdout and saves it as `recommendations.json`:

```json
[{"key":"skill-name|source-name","recommendation":"update","reason":"Evidence-based reason"}]
```

Each object has exactly `key`, `recommendation`, and `reason`; `recommendation` is `update` or `ignore`, and `reason` is a concise non-empty evidence-based string. Preserve the key exactly from `upstreams.json`, include each stale row once, and do not include non-stale rows. For no stale rows, print `[]`. Do not add markdown fences or prose around the array, and do not write files.
