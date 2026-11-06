---
name: c4-architecture
description: "Generate architecture documentation as C4 model Mermaid diagrams (context, container, component, dynamic, deployment) from a description or from repository evidence such as docker-compose, Kubernetes manifests and package files. Use when users ask to map or document a software system, its deployable applications, data stores, external actors, team boundaries, request flows or production infrastructure, even without naming C4. Not for ER diagrams, plain flowcharts or sequence diagrams, draw.io or cloud-icon diagrams, explaining C4 theory without a diagram, reviewing existing C4 diagrams without regenerating them, implementation work, or ADR prose."
---

# C4 Architecture Documentation

## Workflow

### 1. Pick the views and the scope

Default: Context + Container. Overrides, in this order:

- A named view or one flow: only that view (a flow is a Dynamic view).
- Executives: Context only. DevOps or "production infrastructure": Container + Deployment.
- Developers or architects naming a container: add its Component view. Naming none: Context + Container, then offer a Component view for the container with the most distinct responsibilities.
- Several audiences: the union of their views.
- Only a system-level description (users and "a backend"): Context only, and ask for the facts the Container and Deployment views need.

Produce a Component view when the user asks for one and the container is identifiable, or when one container holds distinct responsibilities a reader must see (about five or more modules is a hint, never a gate). If the requested container cannot be identified, say so and ask. Skip the Code level; IDEs generate it. Deployment and Dynamic are supplementary views, not levels.

Before extracting, fix the environment (production unless the user names another) and the system in scope. Every Deployment view, and every Container view that differs by environment, describes that one environment.

### 2. Extract the model from evidence

When repository files are available, reconcile the Compose, package and deployment records into logical deployable units, then map signals to elements:

| Evidence | Element |
|---|---|
| Compose service with `build:`, Dockerfile, Kubernetes Deployment, package with a `start` script | `Container`, one per independently deployable unit |
| Compose services sharing one image or build with different `command:` values | Separate containers: they run and scale separately |
| Compose `image: postgres`/`redis`/`mongo`, a managed database in IaC, `DATABASE_URL` | `ContainerDb` |
| Topic or queue name in producer and consumer config (`*_TOPIC`, queue declarations) | `ContainerQueue`, one per meaningful topic |
| Third-party SDK dependency or key (`stripe`, `STRIPE_SECRET_KEY`, `@sendgrid/mail`) | `System_Ext` |
| Workspace package with `main`/`types` but no start script, Dockerfile or service | Not a container: a component inside each consumer, or omit it |
| Replica counts, ingress, load balancers, namespaces, node pools | Deployment view only; replicas go in the node label (`shop-api x3`), not as duplicate containers |
| Compose and production manifests disagree (a dev-only service, a local database the manifests replace) | Model the manifest for the requested environment, say which one you used, and record the conflict as **Inferred** |

Relationship direction follows the initiator: client to server, producer to topic ("Publishes"), consumer to topic ("Consumes"). Label each relationship with a verb and the evidenced protocol or technology. When there are no files, model only what the user stated.

Under each diagram add an evidence table: element or relationship, source file (or "user statement"), and **Observed** or **Inferred**. Never present an unprovided cloud provider, database, language or deployment as fact; mark it unknown and ask, or state it as an assumption. A local Compose file is not evidence for production hosting.

### 3. Draw boundaries, then relationships

- Set the software-system boundary from what is meaningful outside it: the users it serves, the capability it offers, its own release lifecycle and contract, and any explicit boundary the user or the docs state. Team ownership is one signal among these, never the rule on its own: several teams can own containers inside one system.
- Promote a service to its own `System` only when that boundary is justified: other consumers beyond this system, an independent public API or release cycle, or an explicit statement that it is a separate system. Say why in one line under the diagram. Read [advanced patterns](references/advanced-patterns.md) for the multi-system layout.
- Over the element budget (step 5): split by domain, or draw one service with its direct dependencies per diagram.

### 4. Write

Default destination `docs/architecture/`: `c4-context.md`, `c4-containers.md`, `c4-components-<container>.md`, `c4-deployment-<env>.md`, `c4-dynamic-<flow>.md`. One view per file, an explicit destination wins. Before writing, ask of each element description: does it tell this audience what the element is responsible for, not only what it is built with?

### 5. Verify until it passes

1. Render every file: `mmdc -i docs/architecture/c4-containers.md -o "$(mktemp -d)/out.md"`. It renders each Mermaid block and exits 1 on a parse error or an undeclared alias. No `mmdc`, or one older than 11: `npx -y -p @mermaid-js/mermaid-cli@11.17.0 mmdc -i <file> -o <tmp>/out.md`, the version the rules here were verified with. No CLI, no network, or no browser for it to launch: check by hand against [syntax reference](references/c4-syntax.md) and tell the user the diagrams were not rendered.
2. On failure, fix the reported line, re-render, and repeat until every file exits 0.
3. Check the model, fix what fails with [common mistakes](references/common-mistakes.md), and go back to step 1:
   - Every container is independently deployable; classes, modules and libraries are components or absent.
   - External systems are one `System_Ext` each, with no internals.
   - Every relationship is one-way, with a verb and a technology.
   - Each diagram has a specific title (deployment titles name the environment) and stays under 20 elements, ideally about 15.
   - Names and aliases are identical across views.
   - The evidence table is present, and no NEVER rule is broken.

### Renderer gotchas

- `mmdc` drives headless Chromium through Puppeteer. Running as root or in some containers, it exits 1 with `Failed to launch the browser process` and `Running as root without --no-sandbox is not supported`. That is the environment, not the diagram: write `{"args":["--no-sandbox"]}` to a file and pass it with `-p <file>`.
- Exit 1 alone does not say which failure it was. Read the message: `Parse error on line N` or `references an unknown shape` is the diagram; `UnknownDiagramError: No diagram type detected` is a wrong header or a renderer without C4; a browser launch error is the environment.
- The first `npx` run downloads mermaid-cli and a headless Chrome build into `~/.cache/puppeteer`, so it fails offline.

### 6. Renderer without C4 support

If the target renderer rejects the diagram (`No diagram type detected` for `C4Context`, an old wiki or Mermaid plugin), keep the C4 file as the source of truth and add a `flowchart` translation. Translate only the notation: keep every element, the abstraction level, each boundary (as a `subgraph`), each alias (as the node id), and every relationship's direction, label and technology. Each node label carries the name plus its C4 type (Person, Software System, External System, Container: technology):

```
api["Order API<br/>[Container: Node.js]"]
customer -->|"Places orders<br/>HTTPS"| api
```

From a `C4Dynamic` view, prefix each edge label with its statement-order number (`|"1. Submits credentials<br/>HTTPS"|`): a flowchart does not number edges, so this is the one place hand numbering is right. From a `C4Deployment` view, each `Deployment_Node` becomes a `subgraph` titled with its name and type (`subgraph apiPods["shop-api x3 [Deployment]"]`), nested as the nodes are, with the container instances inside.

Say explicitly that it is a downgrade: the C4 shapes and styling are lost, and the C4 file stays the source of truth.

## NEVER

- NEVER draw a shared library as a container: it is linked into each consumer and never runs alone, so a box with arrows implies a network hop and a deployment that do not exist.
- NEVER draw one Kafka or RabbitMQ box wired to every service: the hub hides which service produces and which consumes each contract. One `ContainerQueue` per meaningful topic, or topic names on the relationship labels when there are many.
- NEVER use `BiRel`: it hides who initiates. Draw the initiator's `Rel`; add a reverse `Rel` only for a separate call.
- NEVER number labels in `C4Dynamic` ("1. Submit"): Mermaid numbers relationships itself in statement order, so the label renders as "1: 1. Submit" (a step 6 flowchart translation is the exception). The index of `RelIndex` is ignored too. Order the statements instead, and draw alternative paths as separate dynamic diagrams, because the numbering is linear.
- NEVER give a `Container` a `{...}` body: only boundaries and deployment nodes take braces, and `Container(...) {` is a parse error. Put components in a `Container_Boundary`.
- NEVER reference an undeclared alias: Mermaid 11 fails the whole diagram ("references an unknown shape").
- NEVER put replicas, load balancers or subnets in a Container view: they are deployment facts and make one deployable unit look like several.
- NEVER write `C4Landscape`: Mermaid has only `C4Context`, `C4Container`, `C4Component`, `C4Dynamic` and `C4Deployment`. A system landscape is a `C4Context` with an `Enterprise_Boundary`.

## References

- [syntax reference](references/c4-syntax.md): read for a macro signature, styling or label offsets, layout control, deployment node variants, or a render error the NEVER list does not explain. Simple context or container diagrams do not need it.
- [advanced patterns](references/advanced-patterns.md): read for several software systems or teams, event-driven flows, deployment views, a system landscape, or a failure-path dynamic diagram. Do not load it for a single-system context or container task.
- [common mistakes](references/common-mistakes.md): read when a step 5 model check fails, for the wrong and correct version of that mistake. Do not load it when the checks pass.
