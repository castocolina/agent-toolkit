# PR Summary: Rework auth flow

## Overview

Reworks the login flow.

```mermaid
sequenceDiagram
    participant U
    participant API
    U->>API: POST /login
    API-->>U: token
```

**[TRIAGE]:** NEEDS_REVIEW
