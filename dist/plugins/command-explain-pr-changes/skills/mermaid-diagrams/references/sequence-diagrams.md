# Sequence Diagrams

Only non-obvious facts. `#`, `;`, and lowercase `end` traps are in [authoring-rules.md](authoring-rules.md) section 7 ("Labels that break the parser").

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant API
    participant DB as Database

    U->>+API: POST /login
    API->>+DB: find credentials
    DB-->>-API: user row
    alt valid
        API-->>U: 200 + token
    else invalid
        API-->>U: 401
    end
    deactivate API
    Note over U,API: token expires in 1h
    par notify
        API-)DB: log attempt
    and audit
        API-)DB: write audit
    end
```

## Arrows

Beyond `->>` and `-->>`: `-)` / `--)` is async fire-and-forget (open arrowhead), and `-x` / `--x` marks a lost or failed message.

## Blocks

`alt/else`, `opt`, `loop`, `par/and`, `critical/option`, `break`, `rect rgb(...)`, `box`: each closes with its own `end`. One missing `end` shifts every later message into the wrong block before the parser fails at the bottom, so the reported line is not where the error is.

## Participant links

`link A: Dashboard @ https://dashboard.example.com` adds a link to participant A's menu, and `links A: {"Dashboard": "https://dashboard.example.com", "Docs": "https://docs.example.com"}` adds several at once; declare the participant first. Only sequence diagrams have this syntax: `link` is not a flowchart keyword (it fails with a parse error), and a flowchart tooltip is the third argument of `click NODE "url" "tooltip"` (advanced-features.md, Interaction). The menu is interactive, so it shows only where the host allows it; do not rely on it in docs.

```mermaid
sequenceDiagram
    participant A as Service A
    participant B as Service B
    link A: Dashboard @ https://dashboard.example.com
    links B: {"Docs": "https://docs.example.com", "Runbook": "https://runbook.example.com"}
    A->>B: Message
    B-->>A: Reply
```

Source: https://mermaid.js.org/syntax/sequenceDiagram.html (links), checked 2026-11-13.

## Silent failures

- `+`/`-` activation shorthand must balance per participant: every `->>+` needs a later `-->>-` from the activated participant, or the bar runs to the bottom; an extra `-` is an error.
- A participant alias is `participant ID as Label`; later lines use the ID. Writing the label creates a second participant with no error.
- `autonumber` numbers only the messages after it; put it on the line after `sequenceDiagram`.
- Undeclared participants appear in first-use order; declare them all at the top to control left-to-right order.
