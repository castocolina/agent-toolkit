Hotfix: null deref in the export worker when the tenant prefix is missing.

## Changes

- guard the tenant lookup against a missing prefix
- add a regression test for the empty-prefix case

**[TRIAGE]:** NEEDS_REVIEW
