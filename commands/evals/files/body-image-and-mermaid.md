# PR Summary: [release → staging] Billing export

## Overview

Bills tenants for completed exports.

Keeps invoices in sync. ![billing](https://github.com/user-attachments/assets/dddd4444eeee5555ffff6666) See also ![architecture](https://static.example.com/architecture.png) for the layout.

```mermaid
flowchart LR
    Export --> Billing --> Invoice
```

**[TRIAGE]:** NEEDS_REVIEW
