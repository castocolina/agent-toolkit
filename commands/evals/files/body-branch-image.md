# PR Summary: [release → staging] Export service

## Overview

Adds the export service that turns queued jobs into uploaded archives.

![pr-41](https://github.com/acme/widgets/blob/pr-diagrams/41/diagram.drawio.png?raw=true)

See the ![runbook](https://github.com/acme/widgets/blob/main/docs/runbook.png) for operations.

## Changes

- adds `ExportService` with retry and backoff
- stores archives under the tenant prefix

**[TRIAGE]:** NEEDS_REVIEW
