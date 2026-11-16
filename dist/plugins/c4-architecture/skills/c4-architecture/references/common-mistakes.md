# Common C4 Mistakes: Wrong and Correct

Read the section for the model check that failed in SKILL.md step 5. The rules and their reasons live in SKILL.md; this file shows how to restructure the diagram.

## Classes or modules drawn as containers

A container is deployable; a class, module or framework inside one is a component.

```mermaid
C4Container
  title WRONG: Classes as Containers
  Container(userController, "UserController", "Java class", "Handles user requests")
  Container(userService, "UserService", "Java class", "Business logic")
  ContainerDb(db, "Database", "PostgreSQL", "User data")
  Rel(userController, userService, "Calls")
  Rel(userService, db, "Queries", "JDBC")
```

```mermaid
C4Component
  title CORRECT: Classes as Components
  ContainerDb(db, "Database", "PostgreSQL", "User data")
  Container_Boundary(api, "User API") {
    Component(userController, "UserController", "Spring MVC", "REST endpoints")
    Component(userService, "UserService", "Spring Bean", "Business logic")
    Component(userRepo, "UserRepository", "Spring Data JPA", "Data access")
  }
  Rel(userController, userService, "Delegates to")
  Rel(userService, userRepo, "Loads users with")
  Rel(userRepo, db, "Queries", "JDBC")
```

Never invent in-between levels ("subsystem", "module group", "Level 2.5"): name each box a System, a Container or a Component.

## Shared library drawn as a container

```mermaid
C4Container
  title WRONG: Library as Container
  Container(serviceA, "Service A", "Java", "Orders")
  Container(serviceB, "Service B", "Java", "Invoices")
  Container(sharedLib, "Shared Utils", "Java library", "Common utilities")
  Rel(serviceA, sharedLib, "Uses")
  Rel(serviceB, sharedLib, "Uses")
```

Omit the library from container views. Show it only in a component view, as a bundled copy inside each consumer:

```mermaid
C4Component
  title CORRECT: Library Inside Each Service
  Container_Boundary(serviceA, "Service A") {
    Component(controllerA, "Order Controller", "Spring MVC", "Order endpoints")
    Component(utilsA, "Shared Utils", "Java library", "Bundled copy")
  }
  Container_Boundary(serviceB, "Service B") {
    Component(controllerB, "Invoice Controller", "Spring MVC", "Invoice endpoints")
    Component(utilsB, "Shared Utils", "Java library", "Bundled copy")
  }
  Rel(controllerA, utilsA, "Formats amounts with")
  Rel(controllerB, utilsB, "Formats amounts with")
```

## One broker box for every message

```mermaid
C4Container
  title WRONG: Central Message Bus
  Container(orderSvc, "Order Service", "Java", "Creates orders")
  Container(inventorySvc, "Inventory Service", "Java", "Manages stock")
  Container(paymentSvc, "Payment Service", "Java", "Takes payments")
  ContainerQueue(kafka, "Kafka", "Event streaming", "Message bus")
  Rel(orderSvc, kafka, "Publishes and subscribes")
  Rel(inventorySvc, kafka, "Publishes and subscribes")
  Rel(paymentSvc, kafka, "Publishes and subscribes")
```

```mermaid
C4Container
  title CORRECT: One Queue per Topic
  Container(orderSvc, "Order Service", "Java", "Creates orders")
  Container(inventorySvc, "Inventory Service", "Java", "Manages stock")
  Container(paymentSvc, "Payment Service", "Java", "Takes payments")
  ContainerQueue(orderCreated, "order.created", "Kafka", "New orders")
  ContainerQueue(stockReserved, "stock.reserved", "Kafka", "Reservations")
  Rel(orderSvc, orderCreated, "Publishes", "Avro")
  Rel(inventorySvc, orderCreated, "Consumes", "Avro")
  Rel(inventorySvc, stockReserved, "Publishes", "Avro")
  Rel(paymentSvc, stockReserved, "Consumes", "Avro")
```

With many topics, drop the queue boxes and draw each event delivery as one arrow from producer to consumer, with a verb and the topic in the label. Say under the diagram that the arrows are event deliveries through the broker, not direct calls:

```mermaid
C4Container
  title ALTERNATIVE: Topics as Labels
  Container(orderSvc, "Order Service", "Java", "Creates orders")
  Container(inventorySvc, "Inventory Service", "Java", "Manages stock")
  Container(paymentSvc, "Payment Service", "Java", "Takes payments")
  Rel(orderSvc, inventorySvc, "Publishes order.created for", "Kafka")
  Rel(inventorySvc, paymentSvc, "Publishes stock.reserved for", "Kafka")
  Rel(paymentSvc, orderSvc, "Publishes payment.completed for", "Kafka")
```

## Internals of an external system

```mermaid
C4Container
  title WRONG: Stripe Internals
  Container(shopApi, "Shop API", "Node.js", "Checkout")
  System_Boundary(stripe, "Stripe") {
    Container(stripeApi, "Stripe API", "Ruby", "Guessed")
    ContainerDb(stripeDb, "Payment DB", "MySQL", "Guessed")
  }
  Rel(shopApi, stripeApi, "Charges cards", "HTTPS")
```

You do not control or observe those internals, so they are guesses that go stale.

```mermaid
C4Container
  title CORRECT: External System as a Black Box
  Container(shopApi, "Shop API", "Node.js", "Checkout")
  System_Ext(stripe, "Stripe", "Card payments")
  Rel(shopApi, stripe, "Charges cards", "HTTPS")
```

## Two-way or unlabeled arrows

```
BiRel(frontend, api, "Data")          WRONG: who calls whom, and what flows?
Rel(orderSvc, paymentSvc)             WRONG: no verb, no technology
Rel(frontend, api, "Fetches products, submits orders", "JSON/HTTPS")   CORRECT
Rel(orderSvc, paymentSvc, "Requests payment authorization", "gRPC")   CORRECT
```

## Infrastructure in a container view

```mermaid
C4Container
  title WRONG: Infrastructure in a Container View
  Container(lb, "Load Balancer", "HAProxy", "Distributes traffic")
  Container(api1, "API instance 1", "Java", "Primary")
  Container(api2, "API instance 2", "Java", "Replica")
  ContainerDb(primary, "Primary DB", "PostgreSQL", "Writes")
  ContainerDb(replica, "Read Replica", "PostgreSQL", "Reads")
  Rel(lb, api1, "Routes", "HTTP")
  Rel(lb, api2, "Routes", "HTTP")
```

The container view keeps one `Container(api)` and one `ContainerDb(db)`. Instances, the load balancer and the replica move to a deployment view (see advanced-patterns.md), with the replica count in the node label.

## Too many elements

"If a diagram with a dozen boxes is hard to understand, don't draw a diagram with a dozen boxes!" (Simon Brown). When a view exceeds the SKILL.md budget, split it by bounded context, or draw one service with its direct dependencies per diagram.

## Inconsistent names across views

"Payment System" in the context view, "Payment Service" in the container view and "Payment Module" in the component view read as three different things. Reuse one name and one alias per element in every view.

## Colors without a key

Mermaid C4 renders no legend (see c4-syntax.md, Not supported). If `UpdateElementStyle` colors carry meaning, explain them in a line of prose under the diagram.

## Deployment view without an environment

`title Deployment Diagram` leaves the reader guessing. Name it: `title Deployment - Production (AWS eu-west-1)`.
