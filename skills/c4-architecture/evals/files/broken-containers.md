# Online Shop - Containers

```mermaid
C4Container
  title Containers - Online Shop
  Person(customer, "Customer", "Buys products online")
  System_Boundary(shop, "Online Shop") {
    Container(web, "Web App", "React", "Storefront in the browser")
    Container(api, "Order API", "Node.js", "Orders and checkout") {
      Component(router, "Order Router", "Express", "HTTP endpoints")
      Component(checkout, "Checkout Service", "TypeScript", "Checkout rules")
    }
    ContainerDb(db, "Orders DB", "PostgreSQL", "Orders")
  }
  Rel(customer, web, "Places orders", "HTTPS")
  Rel(web, api, "Calls", "JSON/HTTPS")
  Rel(api, db, "Reads and writes", "SQL")
  Rel(api, cache, "Caches sessions", "Redis")
```

Docs build output:

```
Error: Parse error on line 6:
...ders and checkout") {      Component(ro
-----------------------^
Expecting 'NEWLINE', 'EOF', 'RBRACE', got 'LBRACE'
```
