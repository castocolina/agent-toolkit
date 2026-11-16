# Backend Requirements: Refund requests

## Context
Support agents review customer refund requests and approve or reject them. Intended outcome: an agent can clear the daily queue without leaving the screen.

## Screens / flows
### Refund queue
- **Purpose / audience:** Support agents see pending refund requests.
- **Display needs:** requester identity, order, requested amount, reason given, age of the request.
- **Actions and outcomes:** Approve a request; the agent expects the row to leave the queue and a confirmation to appear. Rejected result and concurrent-change result: not yet described.
- **States:** loading, empty, error.
- **Permissions:** Only agents with refund rights see the approve action; server enforcement remains backend-owned.
- **Freshness/order:** Oldest request first (agreed with backend, see Discussion Log).
- **Business rules:** Refunds above a limit need a second approver (limit not yet known).

## Uncertainties
- Approval limit that triggers a second approver is unknown (refund queue, approve action).

## Questions for backend
- What is the approval limit, and should the screen show that a second approver is needed?

## Collaboration note
This is a request, not a demand. Let me know if this does not fit how refunds are modelled, and push back if it complicates things.

## Discussion Log
- 2026-11-02, backend (Dana): Oldest-first ordering is fine and stable. Decision: queue is ordered by request age, oldest first. Affects: Refund queue, Freshness/order.
