# C4 Diagrams

Only the Mermaid-specific facts; the C4 model itself is assumed known. Mermaid marks C4 support as experimental, so syntax and layout can change between versions.

```mermaid
C4Container
    title Library platform
    Person(reader, "Reader", "Borrows books")
    System_Ext(search, "Search Service", "External")
    Container_Boundary(platform, "Library Platform") {
        Container(mobile, "Mobile App", "React Native", "UI")
        Container(api, "Catalog API", "Node.js", "Catalog")
        ContainerDb(db, "PostgreSQL", "PostgreSQL 16", "Books")
    }
    Rel(reader, mobile, "Uses")
    Rel(mobile, api, "Calls", "HTTPS/JSON")
    Rel(api, db, "Reads/writes", "SQL")
    Rel_R(api, search, "Queries", "HTTPS")
    UpdateRelStyle(mobile, api, $offsetY="-20")
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Picking the keyword

- `C4Context` for people and whole systems, `C4Container` for the apps and stores inside one system (the default for "the architecture"), `C4Component` for the inside of one container, `C4Dynamic` for numbered interactions, `C4Deployment` for nodes. The keyword is the first line.
- Elements: `Person`, `System`, `SystemDb`, `SystemQueue`, `Container`, `ContainerDb`, `ContainerQueue`, `Component`, each with an `_Ext` variant for external ones. Boundaries: `Enterprise_Boundary`, `System_Boundary`, `Container_Boundary`, `Boundary`.
- Argument order: `Container(id, "Label", "Technology", "Description")`, `Rel(from, to, "Label", "Technology")`. `System` and `Person` take no technology: `System(id, "Label", "Description")`.

## Example: monolith with a database and a cache

One deployable (here a Rails app) plus its stores is one `C4Container` diagram with a single boundary. Every element has a description and every `Rel` reads as a verb plus an object with the technology as the fourth argument; the ids `user`, `app`, `db` and `cache` are unique. Rendered with mmdc 12.2.0 (checked 2026-11-14):

```mermaid
C4Container
    title Rails monolith with a database and a cache
    Person(user, "User", "Customer who uses the application in a browser")
    Container_Boundary(monolith, "Application") {
        Container(app, "Web Application", "Ruby on Rails", "Serves pages and runs all business logic in one deployable")
        ContainerDb(db, "Database", "PostgreSQL", "Stores application records")
        ContainerDb(cache, "Cache", "Redis", "Stores sessions")
    }
    Rel(user, app, "Browses pages and submits forms in", "HTTPS")
    Rel(app, db, "Reads and writes application records in", "SQL over TCP")
    Rel(app, cache, "Stores and reads session data in", "Redis protocol")
```

## More examples by level

Each example follows the same rules as the monolith above: every element has a description, every `Rel` is a verb plus what is sent plus a technology, ids are unique, and elements take no `{ }` body (only boundaries do). Every block below rendered with mmdc 12.2.0 (checked 2026-11-14).

### Context: online shop with its external systems

Use when the question is who uses the system and which outside services it depends on. The old `SystemQueue_Ext` for the shipping API became `System_Ext`: an HTTP API is not a queue.

```mermaid
C4Context
    title System Context - E-Commerce Platform
    Person(customer, "Customer", "Shops online")
    Person(admin, "Administrator", "Manages products and orders")
    Person_Ext(delivery, "Delivery Personnel", "Delivers orders")
    System(ecommerce, "E-Commerce Platform", "Online shopping platform")
    System_Ext(payment, "Payment Gateway", "Processes payments")
    System_Ext(email, "Email Service", "Sends notifications")
    System_Ext(sms, "SMS Service", "Sends SMS alerts")
    System_Ext(analytics, "Analytics Platform", "Tracks user behavior")
    System_Ext(shipping, "Shipping API", "Calculates shipping rates")
    Rel(customer, ecommerce, "Browses products and places orders in", "HTTPS")
    Rel(admin, ecommerce, "Manages the catalog and reviews orders in", "HTTPS")
    Rel(delivery, ecommerce, "Updates delivery status in", "HTTPS")
    Rel(ecommerce, payment, "Sends payment requests to", "HTTPS/REST")
    Rel(ecommerce, email, "Sends emails via", "SMTP")
    Rel(ecommerce, sms, "Sends SMS alerts via", "REST API")
    Rel(ecommerce, analytics, "Sends tracking events to", "JavaScript SDK")
    Rel(ecommerce, shipping, "Requests shipping rates from", "REST API")
    UpdateRelStyle(customer, ecommerce, $offsetX="-50", $offsetY="-30")
    UpdateRelStyle(admin, ecommerce, $offsetX="50", $offsetY="-30")
```

### Container: banking system with a React front end and a Node.js API

Use when the system is small (one web app, one API, one database) and a boundary around it is enough.

```mermaid
C4Container
    title Container Diagram for Banking System
    Person(customer, "Customer", "A banking customer")
    Container_Boundary(banking, "Banking System") {
        Container(web, "Web Application", "React", "Delivers static content and the banking UI")
        Container(api, "API Application", "Node.js", "Provides the banking API")
        ContainerDb(db, "Database", "PostgreSQL", "Stores account data")
    }
    Rel(customer, web, "Opens the banking site in", "HTTPS")
    Rel(web, api, "Sends account requests to", "HTTPS/JSON")
    Rel(api, db, "Reads and writes account data in", "SQL/TCP")
```

### Container: e-commerce platform with frontend, services and a data layer

Use when the system has several services and stores that read better in three layers (frontend, backend, data). Keep the three boundaries; without them the diagram becomes one unordered row.

```mermaid
C4Container
    title Container Diagram - E-Commerce Platform
    Person(customer, "Customer", "Shops online")
    Person(admin, "Admin", "Manages the catalog and orders")
    System_Ext(payment, "Payment Gateway", "Processes card payments")
    System_Ext(email, "Email Service", "Delivers email to customers")
    Container_Boundary(frontend, "Frontend") {
        Container(web, "Web App", "React", "Delivers the UI")
        Container(mobile, "Mobile App", "React Native", "Delivers the mobile UI")
    }
    Container_Boundary(backend, "Backend Services") {
        Container(api, "API Gateway", "Node.js/Express", "Routes requests to services")
        Container(auth, "Auth Service", "Node.js", "Handles authentication")
        Container(catalog, "Catalog Service", "Python/FastAPI", "Manages products")
        Container(order, "Order Service", "Java/Spring", "Processes orders")
        Container(notification, "Notification Service", "Node.js", "Sends notifications")
    }
    Container_Boundary(data, "Data Layer") {
        ContainerDb(postgres, "Main Database", "PostgreSQL", "Stores core data")
        ContainerDb(mongo, "Product DB", "MongoDB", "Stores the product catalog")
        ContainerDb(redis, "Cache", "Redis", "Stores sessions and cached data")
        ContainerQueue(queue, "Message Queue", "RabbitMQ", "Carries asynchronous events")
    }
    Rel(customer, web, "Browses products and places orders in", "HTTPS")
    Rel(customer, mobile, "Browses products and places orders in", "HTTPS")
    Rel(admin, web, "Manages the catalog through", "HTTPS")
    Rel(web, api, "Sends API requests to", "HTTPS/JSON")
    Rel(mobile, api, "Sends API requests to", "HTTPS/JSON")
    Rel(api, auth, "Sends credentials to", "gRPC")
    Rel(api, catalog, "Requests product data from", "REST")
    Rel(api, order, "Sends new orders to", "REST")
    Rel(auth, postgres, "Reads and writes user records in", "SQL")
    Rel(catalog, mongo, "Reads and writes product documents in", "MongoDB protocol")
    Rel(order, postgres, "Reads and writes orders in", "SQL")
    Rel(auth, redis, "Stores sessions in", "Redis protocol")
    Rel(api, redis, "Caches responses in", "Redis protocol")
    Rel(order, queue, "Publishes order events to", "AMQP")
    Rel(notification, queue, "Consumes order events from", "AMQP")
    Rel(notification, email, "Sends notification emails via", "SMTP")
    Rel(order, payment, "Sends payment requests to", "HTTPS/REST")
```

### Container: event-driven services around a Kafka event bus

Use when services talk through events rather than direct calls: one `ContainerQueue` for the bus, one publisher and its consumers.

```mermaid
C4Container
    title Event-driven order processing
    Person(user, "User", "Places orders")
    Container(frontend, "Frontend", "React", "Provides the user interface")
    Container(api, "API Gateway", "Kong", "Routes API requests")
    Container_Boundary(services, "Services") {
        Container(order, "Order Service", "Java", "Processes orders")
        Container(inventory, "Inventory Service", "Go", "Manages stock")
        Container(notification, "Notification Service", "Node.js", "Sends alerts")
    }
    ContainerQueue(events, "Event Bus", "Kafka", "Streams domain events")
    ContainerDb(db, "Databases", "Various", "Stores service data")
    Rel(user, frontend, "Places orders in", "HTTPS")
    Rel(frontend, api, "Sends order requests to", "HTTPS/JSON")
    Rel(api, order, "Routes order requests to", "REST")
    Rel(order, events, "Publishes OrderCreated events to", "Kafka")
    Rel(events, inventory, "Delivers OrderCreated events to", "Kafka")
    Rel(events, notification, "Delivers OrderCreated events to", "Kafka")
    Rel(order, db, "Reads and writes order records in", "Database driver")
    Rel(inventory, db, "Reads and writes stock records in", "Database driver")
```

### Component: API application with controller, service, repository and email client

Use for the inside of one container when the layers are the point (controller calls service, service calls repository and an outbound client).

```mermaid
C4Component
    title Component Diagram for API Application
    Container(web, "Web App", "React", "Delivers the UI")
    ContainerDb(db, "Database", "PostgreSQL", "Stores account data")
    System_Ext(email, "Email System", "Delivers email to customers")
    Container_Boundary(api, "API Application") {
        Component(controller, "Controller", "Express Router", "Handles HTTP requests")
        Component(service, "Business Logic", "Service Layer", "Implements the core logic")
        Component(repository, "Data Access", "Repository", "Runs database operations")
        Component(emailClient, "Email Client", "SMTP client", "Sends emails")
    }
    Rel(web, controller, "Sends API requests to", "HTTPS/JSON")
    Rel(controller, service, "Passes validated requests to", "Function call")
    Rel(service, repository, "Requests account data from", "Function call")
    Rel(repository, db, "Reads and writes account data in", "SQL/TCP")
    Rel(service, emailClient, "Sends email requests to", "Function call")
    Rel(emailClient, email, "Sends emails through", "SMTP")
```

### Component: order service with clients, repository and event publisher

Use for a service with several outbound integrations (payment, inventory, a database and a queue) behind one manager component.

```mermaid
C4Component
    title Component Diagram - Order Service
    Container(api_gateway, "API Gateway", "Node.js", "Routes client requests to services")
    ContainerDb(postgres, "Database", "PostgreSQL", "Stores orders")
    ContainerQueue(queue, "Message Queue", "RabbitMQ", "Carries domain events")
    System_Ext(payment, "Payment Gateway", "Processes card payments")
    System_Ext(inventory, "Inventory Service", "Reports and reserves stock")
    Container_Boundary(order_service, "Order Service") {
        Component(controller, "REST Controllers", "Spring MVC", "Exposes the HTTP endpoints")
        Component(order_logic, "Order Manager", "Service", "Runs the order processing logic")
        Component(payment_client, "Payment Client", "REST Client", "Integrates with the payment gateway")
        Component(inventory_client, "Inventory Client", "REST Client", "Integrates with the inventory service")
        Component(repository, "Order Repository", "JPA", "Runs database operations")
        Component(event_publisher, "Event Publisher", "Java class", "Publishes domain events")
        Component(validator, "Order Validator", "Java class", "Validates orders")
    }
    Rel(api_gateway, controller, "Routes order requests to", "HTTPS/REST")
    Rel(controller, order_logic, "Delegates order commands to", "Java call")
    Rel(controller, validator, "Sends order payloads to", "Java call")
    Rel(order_logic, payment_client, "Sends payment requests to", "Java call")
    Rel(order_logic, inventory_client, "Sends stock checks to", "Java call")
    Rel(order_logic, repository, "Sends orders to be persisted to", "Java call")
    Rel(order_logic, event_publisher, "Sends domain events to", "Java call")
    Rel(payment_client, payment, "Sends payment requests to", "HTTPS/REST")
    Rel(inventory_client, inventory, "Sends stock queries to", "HTTPS/REST")
    Rel(repository, postgres, "Reads and writes orders in", "JDBC/SQL")
    Rel(event_publisher, queue, "Publishes order events to", "AMQP")
```

## Layout (no auto-layout)

- Elements are placed in declaration order, left to right, wrapping after `$c4ShapeInRow` shapes (default 4) and `$c4BoundaryInRow` boundaries (default 2). Change both with `UpdateLayoutConfig`, and reorder declarations to untangle lines.
- `Rel_U`, `Rel_D`, `Rel_L`, `Rel_R` only hint at the direction of one arrow; they do not move elements.
- Overlapping relationship labels are moved with `UpdateRelStyle(from, to, $offsetX="...", $offsetY="...")`; element colors with `UpdateElementStyle(id, $bgColor="...", $fontColor="...")`. Set both colors together.
