# PR Summary: [release → staging] Billing export

## Overview

Bills tenants for completed exports.

## Diagram

```mermaid
flowchart LR
    Export --> Billing

## ⚙️ Detailed Changeset Breakdown

**Files Affected:**

- `src/billing/export.ts`

**Summary of Changes:**

- adds the export job that bills completed exports

**[TRIAGE]:** NEEDS_REVIEW