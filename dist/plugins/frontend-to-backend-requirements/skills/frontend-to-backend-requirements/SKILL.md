---
name: frontend-to-backend-requirements
description: "Document frontend data needs, user actions, UI states, permissions, and unresolved business rules for backend collaborators without prescribing API implementation. Use when teams need backend requirements, ask what a screen needs from the API, or describe UI data needs. Not for endpoint design, OpenAPI/JSON schemas, database tables, or implementing frontend/backend code."
---

# Frontend-to-Backend Requirements

Describe the user-visible contract and outcomes, not the backend mechanism. Save the artifact by default at `.claude/docs/ai/<feature>/backend-requirements.md`; honor an explicitly requested destination or inline preview. Brief chat confirmations and clarifying questions are fine.

## Gather requirements by screen and action

For each screen/flow, capture its purpose, audience/permissions, displayed information and relationships, user actions, expected completion feedback, and relevant states (loading, empty, error, success plus exceptional states).

For every action, describe what the user expects to happen, how completion is recognized, and what the UI should do when the outcome is unknown (timeout), rejected, or conflicts with a concurrent change. Distinguish hidden/disabled UI affordances from server authorization: the backend must enforce access independently.

Record data freshness requirements, ordering/pagination expectations, partial authorization (some records/actions unavailable), and whether concurrent updates can invalidate what the user sees. Do not assume these guarantees; ask for them.

## Classify uncertainty

For each unknown, record the affected screen/action and user outcome, then classify:

- **Blocking:** implementation would risk wrong behavior or data loss; ask before marking agreed.
- **Safe provisional assumption:** reversible and low-impact; label explicitly and seek confirmation.

Tie backend responses to the relevant requirement. After a response, update the requirement and mark the uncertainty resolved only when the answer covers the user-visible outcome. Preserve prior decisions and Discussion Log when editing an existing document; append new responses rather than rewriting history.

NEVER name endpoint paths, HTTP methods, or field names: prescriptive shapes can lock in a poor API. NEVER omit error/empty states: backend cannot infer UI failure modes from a happy-path data list. NEVER assume ordering, pagination, freshness, or authorization behavior without agreement. NEVER report an unknown action outcome as success.

Why these matter: an ordering, pagination, freshness, or authorization guarantee nobody agreed on produces misleading UI states (a reordered list, a missing page, stale data shown as current, an action offered that the server then refuses). An unknown action outcome reported as success can make the user repeat the action and cause a duplicate. Mark each such guarantee unresolved in the document, and ask backend how the UI should reconcile an uncertain result (for example after a timeout or a concurrent change).

## Write and check

Load [the template](templates/backend-requirements.md) at the write step. Write the document as a request, not a demand: say why each need exists and invite backend pushback or alternatives (the template's Collaboration note has the wording). Resolve feature identity from the request/repo; if the feature name is ambiguous, list the candidate screens found and ask once, and never invent a path; also ask if the destination conflicts. If a document already exists, inspect it first and preserve its discussion history. Before reporting, check every requested screen, action, outcome, state, permission, and decision against the document; any action with no rejected, timeout, or conflict outcome is explicitly unresolved, never silently marked success. Revise and repeat the check until covered or explicitly unresolved.

Write every need with a purpose and a context sentence (where it sits in the product and what the user does next), as [the examples](references/examples.md) show.
