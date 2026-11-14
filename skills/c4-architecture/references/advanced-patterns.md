# Advanced C4 Patterns

Layouts for several software systems, event-driven flows and deployment views, with one rendered example each. The modeling rules and the NEVER list live in SKILL.md; the wrong-versus-correct examples live in common-mistakes.md.

## Several software systems

SKILL.md step 3 decides where system boundaries go; ownership alone never does. In this example Catalog and Identity are separate systems because each has consumers beyond the order flow and its own API and release cycle; the Order API and Order Worker stay containers of one Order System even if two teams own them.

Draw the context view first, then one container view per system:

```mermaid
C4Context
  title Commerce - System Context
  Person(customer, "Customer", "Online shopper")
  Enterprise_Boundary(acme, "Acme Corp") {
    System(orders, "Order System", "Order lifecycle")
    System(catalog, "Catalog System", "Products and stock, also serves the partner portal")
    System(identity, "Identity System", "Accounts and tokens for every Acme product")
  }
  System_Ext(stripe, "Stripe", "Card payments")
  Rel(customer, orders, "Places orders", "HTTPS")
  Rel(customer, catalog, "Browses products", "HTTPS")
  Rel(orders, identity, "Validates tokens", "HTTPS")
  Rel(orders, catalog, "Reserves stock", "HTTPS")
  Rel(orders, stripe, "Charges cards", "HTTPS")
```

```mermaid
C4Container
  title Order System - Containers
  System_Ext(catalog, "Catalog System", "Products and stock")
  System_Ext(identity, "Identity System", "Accounts and tokens")
  System_Ext(stripe, "Stripe", "Card payments")
  System_Boundary(orders, "Order System") {
    Container(orderApi, "Order API", "Spring Boot", "REST endpoints")
    Container(orderWorker, "Order Worker", "Spring Boot", "Payment and fulfilment jobs")
    ContainerDb(orderDb, "Order DB", "PostgreSQL", "Orders")
    ContainerQueue(orderPlaced, "order.placed", "RabbitMQ", "New order jobs")
  }
  Rel(orderApi, orderDb, "Reads and writes order data in", "JDBC")
  Rel(orderApi, orderPlaced, "Publishes new order jobs to", "AMQP")
  Rel(orderWorker, orderPlaced, "Consumes new order jobs from", "AMQP")
  Rel(orderApi, identity, "Validates tokens", "HTTPS")
  Rel(orderApi, catalog, "Reserves stock", "HTTPS")
  Rel(orderWorker, stripe, "Charges cards", "HTTPS")
```

In one system's container view, the other internal systems use `System_Ext`: outside this diagram's scope, not outside the company. Keep the same alias (`catalog`, `identity`) as in the context view.

## Microservices of one system

Microservices that one system owns, with a datastore each, are containers inside one `System_Boundary`. Inter-service messages go through one queue per topic. A customer enters through the service that takes the request (example e-commerce platform, rendered with mermaid-cli 12.2.0, checked 2026-11-14):

```mermaid
C4Container
  title E-commerce Platform - Containers
  Person(customer, "Customer", "Online shopper")
  System_Boundary(platform, "E-commerce Platform") {
    Container(orderApi, "Order Service", "Spring Boot", "Accepts and processes orders")
    ContainerDb(orderDb, "Order DB", "PostgreSQL", "Order data")
    Container(inventoryApi, "Inventory Service", "Node.js", "Tracks and reserves stock")
    ContainerDb(inventoryDb, "Inventory DB", "MongoDB", "Stock data")
    ContainerQueue(orderPlaced, "order.placed", "RabbitMQ", "Placed orders awaiting a stock reservation")
  }
  Rel(customer, orderApi, "Submits orders to", "JSON/HTTPS")
  Rel(orderApi, orderDb, "Reads and writes orders", "JDBC")
  Rel(orderApi, orderPlaced, "Publishes placed orders to", "AMQP")
  Rel(inventoryApi, orderPlaced, "Consumes placed orders from", "AMQP")
  Rel(inventoryApi, inventoryDb, "Reads and writes stock levels", "MongoDB wire protocol")
```

## Components of one container

A component view opens one container. The container is a `Container_Boundary`, its neighbours stay outside it, and each relationship names what the caller asks of the callee. In-process calls say so in the technology (example Order API, rendered with mermaid-cli 12.2.0, checked 2026-11-14):

```mermaid
C4Component
  title Order API - Components
  Container(gateway, "API Gateway", "Kong", "Routes and authenticates API traffic")
  ContainerDb(db, "Order DB", "PostgreSQL", "Orders")
  ContainerQueue(events, "Order Events", "Kafka", "Order domain events")
  System_Ext(payment, "Payment Service", "Stripe card payments")
  Container_Boundary(orderApi, "Order API") {
    Component(controller, "Order Controller", "Spring MVC", "REST endpoints for orders")
    Component(validator, "Request Validator", "Bean Validation", "Validates order requests")
    Component(service, "Order Service", "Spring Service", "Order business logic")
    Component(paymentClient, "Payment Client", "Feign", "Calls the Stripe API")
    Component(repository, "Order Repository", "Spring Data JPA", "Reads and writes orders")
    Component(publisher, "Event Publisher", "Spring Kafka", "Publishes order events")
  }
  Rel(gateway, controller, "Forwards order requests to", "JSON/HTTPS")
  Rel(controller, validator, "Validates requests with", "Java method call")
  Rel(controller, service, "Delegates order handling to", "Java method call")
  Rel(service, paymentClient, "Requests charges through", "Java method call")
  Rel(service, repository, "Persists orders through", "Java method call")
  Rel(service, publisher, "Publishes order events through", "Java method call")
  Rel(paymentClient, payment, "Charges cards at", "REST/HTTPS")
  Rel(repository, db, "Reads and writes orders", "JDBC")
  Rel(publisher, events, "Produces order events to", "Avro/Kafka")
```

## Event-driven flows

The container view shows which service publishes and consumes each topic (see common-mistakes.md for the single-broker mistake). A dynamic view shows one event chain in order. Mermaid numbers the relationships itself, so write them in sequence without numbers:

```mermaid
C4Dynamic
  title Order Placement - Event Chain
  Container(orderSvc, "Order Service", "Java", "Creates orders")
  ContainerQueue(orderCreated, "order.created", "Kafka", "New orders")
  Container(inventorySvc, "Inventory Service", "Go", "Reserves stock for orders")
  ContainerQueue(stockReserved, "inventory.reserved", "Kafka", "Stock reservations")
  Container(paymentSvc, "Payment Service", "Node.js", "Charges reserved orders")
  Rel(orderSvc, orderCreated, "Publishes created orders to", "Avro")
  Rel(inventorySvc, orderCreated, "Consumes created orders from", "Avro")
  Rel(inventorySvc, stockReserved, "Publishes stock reservations to", "Avro")
  Rel(paymentSvc, stockReserved, "Consumes stock reservations from", "Avro")
```

## Failure paths

The numbering is linear, so a success path and a failure path cannot share one dynamic diagram. Draw the failure path on its own, with the internal components inside a `Container_Boundary`:

```mermaid
C4Dynamic
  title Checkout - Payment Provider Timeout
  Container(web, "Web App", "React", "Checkout UI in the browser")
  Container_Boundary(api, "Payments API") {
    Component(checkout, "Checkout Handler", "Express route", "Receives payment requests")
    Component(breaker, "Circuit Breaker", "opossum", "Stops calls to a failing provider")
  }
  System_Ext(stripe, "Stripe", "Card payments")
  ContainerDb(cache, "Fallback Cache", "Redis", "Last known payment status")
  Rel(web, checkout, "Submits payment", "JSON/HTTPS")
  Rel(checkout, breaker, "Requests charge", "in-process call")
  Rel(breaker, stripe, "Forwards charge, times out", "HTTPS")
  Rel(breaker, cache, "Reads last known payment status", "Redis protocol")
```

## Deployment views

A deployment view places container instances on infrastructure. Replicas go in the node label (SKILL.md step 2), as the official Mermaid example does (`bigbank-api*** x8`, https://mermaid.js.org/syntax/c4.html, checked 2026-11-13). Draw separate instances only when they differ in role, such as a database primary and replica. Name the environment in the title.

Version labels are illustrative: read each from the user's Dockerfile, `package.json` or infrastructure code, and give no number when none is evidenced, as the cluster node below does (EKS versions change often, https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html, checked 2026-11-13). `Node.js 22` stands for the user's own version (Node.js 22 is an LTS release, https://nodejs.org/en/about/previous-releases, checked 2026-11-13).

```mermaid
C4Deployment
  title Production - Kubernetes (EKS, eu-west-1)
  Deployment_Node(cluster, "Kubernetes cluster", "EKS") {
    Deployment_Node(ingress, "ingress-nginx", "Ingress controller") {
      Container(nginx, "Ingress", "nginx", "TLS termination, routing")
    }
    Deployment_Node(appNs, "shop namespace", "Kubernetes namespace") {
      Deployment_Node(apiPods, "shop-api x3", "Deployment") {
        Container(api, "Order API", "Node.js 22", "REST endpoints for orders")
      }
      Deployment_Node(workerPods, "shop-worker x2", "Deployment") {
        Container(worker, "Order Worker", "Node.js 22", "Payment and fulfilment jobs")
      }
    }
  }
  Deployment_Node(rds, "Amazon RDS", "Multi-AZ") {
    ContainerDb(primary, "Order DB primary", "PostgreSQL 16", "Accepts all writes")
    ContainerDb(replica, "Order DB replica", "PostgreSQL 16", "Standby copy of the primary")
  }
  Rel(nginx, api, "Routes /api", "HTTP")
  Rel(api, primary, "Reads and writes", "SQL")
  Rel(worker, primary, "Updates orders", "SQL")
  Rel(primary, replica, "Replicates to", "Streaming replication")
```

## System landscape

Mermaid has no landscape diagram type. Draw an enterprise-wide view as a `C4Context` with an `Enterprise_Boundary`, grouping systems with `Boundary` when the groups carry meaning:

```mermaid
C4Context
  title Acme - System Landscape
  Person(customer, "Customer", "Buys products and asks for support")
  Person(employee, "Employee", "Runs stock and customer records")
  Enterprise_Boundary(acme, "Acme Corp") {
    Boundary(front, "Customer-facing", "Group") {
      System(shop, "Online Shop", "Catalog and checkout")
      System(support, "Support Portal", "Tickets")
    }
    Boundary(back, "Back office", "Group") {
      System(erp, "ERP", "Finance and stock")
      System(crm, "CRM", "Customer records")
    }
  }
  System_Ext(stripe, "Stripe", "Card payments")
  Rel(customer, shop, "Buys products", "HTTPS")
  Rel(customer, support, "Opens tickets", "HTTPS")
  Rel(employee, erp, "Manages stock", "HTTPS")
  Rel(shop, erp, "Sends orders", "HTTPS")
  Rel(support, crm, "Reads customer history", "HTTPS")
  Rel(shop, stripe, "Charges cards", "HTTPS")
```

## Linking decisions

Diagrams show the chosen architecture; the reasons belong in ADRs. Reference an ADR in a `%%` comment or in the element description (`"Kafka, see ADR-003"`), never as "option A versus option B" boxes in the diagram.

```mermaid
C4Container
  title Containers - Order Platform
  %% See ADR-001 for API Gateway selection
  %% See ADR-002 for database choice
  %% See ADR-003 for event-driven approach

  Container(gateway, "API Gateway", "Kong", "Routes client requests to the Order API; see ADR-001 (selected for its plugin ecosystem)")
  Container(api, "Order API", "Spring Boot", "Creates and tracks orders")
  ContainerDb(db, "Order DB", "PostgreSQL", "Stores orders; see ADR-002 (ACID compliance required)")
  ContainerQueue(events, "Order Events", "Kafka", "Carries order events; see ADR-003 (event sourcing pattern)")

  Rel(gateway, api, "Routes order requests to", "HTTP")
  Rel(api, db, "Persists orders in", "JDBC")
  Rel(api, events, "Publishes order events to", "Avro over Kafka")
```

Key: rectangles are containers, the cylinder is a database, the pipe is a queue; each arrow is one-way and reads "initiator, action, technology"; the ADR numbers name the decision records behind each element.
