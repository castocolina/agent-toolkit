# Layout guidelines

Read from SKILL.md when drawing an AWS architecture or a diagram with several flow types. Arrow targets, routing, containment, labels and background live in SKILL.md; this file only adds group nesting, line meaning and placement direction.

## 1. AWS group nesting

AWS Cloud is the outermost group. Inside it, subgroups follow function, and sibling groups sit side by side in data-flow order. Each level is the `parent` of the next.

```text
AWS Cloud (outermost)
├── VPC
│   ├── Public Subnet
│   │   └── ALB, NAT Gateway, and similar
│   └── Private Subnet
│       └── ECS, RDS, and similar
├── S3
├── CloudWatch
└── other regional services
```

Regional services with no VPC attachment (S3, CloudWatch, DynamoDB) sit in AWS Cloud, beside the VPC, not inside it.

## 2. Line meaning

Line style carries the kind of flow; the route (straight or orthogonal) is decided separately in SKILL.md.

| Flow | Line | Style fragment | Use |
|------|------|----------------|-----|
| Ingestion | dashed | `dashed=1;` | data intake |
| Query | solid | (default) | query, read |
| Control | dotted | `dashed=1;dashPattern=1 4;` | control, management |

Arrows follow the direction of the data. Add a legend when more than one line style appears.

## 3. Placement direction

Default left to right, in data-flow order:

```text
[data source] -> [process] -> [storage] -> [analysis / display]
```

Top to bottom when the flow is request-shaped (a client calling down a stack):

```text
[user / client]
        |
[load balancer]
        |
[application]
        |
[database]
```

Pick one direction per diagram and keep it; a flow that doubles back forces arrows to cross.
