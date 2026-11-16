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
  Rel(orderApi, orderDb, "Reads and writes", "JDBC")
  Rel(orderApi, orderPlaced, "Publishes", "AMQP")
  Rel(orderWorker, orderPlaced, "Consumes", "AMQP")
  Rel(orderApi, identity, "Validates tokens", "HTTPS")
  Rel(orderApi, catalog, "Reserves stock", "HTTPS")
  Rel(orderWorker, stripe, "Charges cards", "HTTPS")
```

In one system's container view, the other internal systems use `System_Ext`: outside this diagram's scope, not outside the company. Keep the same alias (`catalog`, `identity`) as in the context view.

## Event-driven flows

The container view shows which service publishes and consumes each topic (see common-mistakes.md for the single-broker mistake). A dynamic view shows one event chain in order. Mermaid numbers the relationships itself, so write them in sequence without numbers:

```mermaid
C4Dynamic
  title Order Placement - Event Chain
  Container(orderSvc, "Order Service", "Java")
  ContainerQueue(orderCreated, "order.created", "Kafka")
  Container(inventorySvc, "Inventory Service", "Go")
  ContainerQueue(stockReserved, "inventory.reserved", "Kafka")
  Container(paymentSvc, "Payment Service", "Node.js")
  Rel(orderSvc, orderCreated, "Publishes order", "Avro")
  Rel(inventorySvc, orderCreated, "Consumes order", "Avro")
  Rel(inventorySvc, stockReserved, "Publishes reservation", "Avro")
  Rel(paymentSvc, stockReserved, "Consumes reservation", "Avro")
```

## Failure paths

The numbering is linear, so a success path and a failure path cannot share one dynamic diagram. Draw the failure path on its own, with the internal components inside a `Container_Boundary`:

```mermaid
C4Dynamic
  title Checkout - Payment Provider Timeout
  Container(web, "Web App", "React")
  Container_Boundary(api, "Payments API") {
    Component(checkout, "Checkout Handler", "Express route")
    Component(breaker, "Circuit Breaker", "opossum")
  }
  System_Ext(stripe, "Stripe", "Card payments")
  ContainerDb(cache, "Fallback Cache", "Redis")
  Rel(web, checkout, "Submits payment", "JSON/HTTPS")
  Rel(checkout, breaker, "Requests charge")
  Rel(breaker, stripe, "Forwards charge, times out", "HTTPS")
  Rel(breaker, cache, "Reads last known payment status", "Redis protocol")
```

## Deployment views

A deployment view places container instances on infrastructure. Replicas go in the node label (SKILL.md step 2), as the official Mermaid example does (`bigbank-api x8`). Draw separate instances only when they differ in role, such as a database primary and replica. Name the environment in the title.

```mermaid
C4Deployment
  title Production - Kubernetes (EKS, eu-west-1)
  Deployment_Node(cluster, "Kubernetes cluster", "EKS 1.30") {
    Deployment_Node(ingress, "ingress-nginx", "Ingress controller") {
      Container(nginx, "Ingress", "nginx", "TLS termination, routing")
    }
    Deployment_Node(appNs, "shop namespace", "Kubernetes namespace") {
      Deployment_Node(apiPods, "shop-api x3", "Deployment") {
        Container(api, "Order API", "Node.js 20")
      }
      Deployment_Node(workerPods, "shop-worker x2", "Deployment") {
        Container(worker, "Order Worker", "Node.js 20")
      }
    }
  }
  Deployment_Node(rds, "Amazon RDS", "Multi-AZ") {
    ContainerDb(primary, "Order DB primary", "PostgreSQL 16")
    ContainerDb(replica, "Order DB replica", "PostgreSQL 16")
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
  Person(customer, "Customer")
  Person(employee, "Employee")
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
  Rel(customer, shop, "Buys products")
  Rel(customer, support, "Opens tickets")
  Rel(employee, erp, "Manages stock")
  Rel(shop, erp, "Sends orders", "HTTPS")
  Rel(support, crm, "Reads customer history", "HTTPS")
  Rel(shop, stripe, "Charges cards", "HTTPS")
```

## Linking decisions

Diagrams show the chosen architecture; the reasons belong in ADRs. Reference an ADR in a `%%` comment or in the element description (`"Kafka, see ADR-003"`), never as "option A versus option B" boxes in the diagram.
