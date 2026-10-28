# PR Summary: [release → staging] Export service

## Overview

Adds the export service that turns queued jobs into uploaded archives.

![export flow](https://github.com/user-attachments/assets/aaaa1111bbbb2222cccc3333)

## Changes

- adds `ExportService` with retry and backoff
- stores archives under the tenant prefix

**[TRIAGE]:** NEEDS_REVIEW
