---
name: c4-architecture
description: "Generate architecture documentation with C4 model Mermaid diagrams (context, container, component, dynamic, deployment). Use when users map software systems, deployable applications, external actors, ownership boundaries, or production infrastructure, even without naming C4. Not for ER diagrams, plain flowcharts or sequence diagrams, implementation work, or ADR prose without diagrams."
---

# C4 Architecture Documentation

Create evidence-backed C4 views. A diagram is a model of boundaries and responsibilities, not an inventory of every package.

## Extract the model before drawing

1. Identify executable/deployable units from build files, Dockerfiles, service manifests, and package configuration; these establish candidate containers.
2. Trace runtime dependencies from configuration, API clients, database clients, and message subscriptions. Label relationships with evidenced protocol or event, and use direction/action that reflects actual flow.
3. Establish the system boundary, external actors/systems, and team ownership. Promote independently owned systems to system-level elements; keep shared libraries inside their consuming container.
4. Keep stable aliases/identities across views so diagrams can be compared. Separate observed facts from inferred architecture.
5. Select only requested/useful views. Default broad overview: Context + Container. Context-only requests get Context only. Component view only when a container has 5+ meaningful internal modules or requester names a specific container. Deployment and Dynamic are supplementary views, not abstraction levels.

| C4 abstraction | View | Use |
|---|---|---|
| Level 1 | Context | System, users, external systems |
| Level 2 | Container | Independently runnable/deployable applications and data stores |
| Level 3 | Component | Internal responsibilities within one container |
| Level 4 | Code | Classes/functions, rarely useful as architecture documentation |
| Supplementary | Dynamic / Deployment | A focused interaction or runtime placement, not extra hierarchy levels |

## Modeling rules

- A container is independently runnable/deployable; a framework, library, or state manager inside an SPA is not a container.
- Draw ownership boundaries before relationships. Use actual service/topic/database boundaries rather than generic technology boxes.
- Show event topics/queues separately when they are meaningful contracts; label publish/subscribe direction.
- Keep each diagram focused (under ~20 elements), with a title and useful descriptions. Split rather than flattening distinct concerns.
- Honor requested views and audience. Do not force Context + Container when the user asked for one focused flow.
- If the renderer rejects `C4*`, offer a flowchart/subgraph translation that preserves Person/System/Container vocabulary and explicitly note the renderer downgrade.

## Write and verify

Default destination: `docs/architecture/` with names such as `c4-context.md`, `c4-containers.md`, `c4-components-<feature>.md`, `c4-deployment.md`, or `c4-dynamic-<flow>.md`. Honor an explicit destination. Validate element category, boundaries, direction, and evidence before delivery. GitHub-flavored Mermaid may reject `UpdateRelStyle` with `C4Dynamic` and deeply nested deployment nodes; avoid these constructs there.

Read [syntax reference](references/c4-syntax.md) when using unfamiliar constructs or diagnosing renderer errors. Read [advanced patterns](references/advanced-patterns.md) for microservices, events, or deployment views; simple context-only tasks do not need it. Before finalizing any diagram, check [common mistakes](references/common-mistakes.md).
