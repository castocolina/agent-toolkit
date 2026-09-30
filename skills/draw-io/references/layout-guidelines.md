# Layout guidelines

## 1. Grouping

- AWS Cloud is the outermost group
- Create subgroups by function
- Place groups side by side, following the data flow

### 1.1. Group hierarchy

```text
AWS Cloud (outermost)
├── VPC
│   ├── Public Subnet
│   │   └── ALB, NAT Gateway, and similar
│   └── Private Subnet
│       └── ECS, RDS, and similar
├── S3
├── CloudWatch
└── other services
```

## 2. Connectors

### 2.1. Line meaning

| Flow | Line | Use |
|------|------|-----|
| Ingestion Flow | dashed | data intake |
| Query Flow | solid | query, read |
| Control Flow | dotted | control, management |

Dashed, solid, and dotted distinguish meaning. The path is separate. A straight `A -> B` is allowed only when both ends share an axis and the span is empty. Otherwise use a curved orthogonal connector:

```text
edgeStyle=orthogonalEdgeStyle;curved=1;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;
```

### 2.2. Direction and target

- The arrow follows the direction of the data
- Prefer two unidirectional arrows over one bidirectional arrow. A double-headed arrow hides which call is which.
- Choose the target per case. Block-to-block talk ends on the parent container. A call into a specific service ends on that node. Not always the container, and not always the node
- The elbow runs through the gutter between groups. Do not cut through a container
- Put the label in the gutter. Never under a container or under text. Keep it at least 20px from the line and from any box
- Do not put every arrow on the back layer. A back-layer arrow hides its label under a container

### 2.3. A group is a parent

A container is not a rectangle drawn behind siblings. Set each child's `parent` to the container. Coordinates are relative to the container origin. Keep at least 30px of inner margin. Dragging the container moves its contents.

## 3. Placement

### 3.1. Left to right

```text
[data source] -> [process] -> [storage] -> [analysis / display]
```

### 3.2. Top to bottom (alternative)

```text
[user / client]
        |
[load balancer]
        |
[application]
        |
[database]
```

## 4. Readability

- Place labels near their elements
- Adjust placement so arrows do not cross
- Group related elements and keep them close
- Keep enough whitespace to stay readable
- Judge proportion against a 16:9 slide. Do not stretch horizontally and shrink the text. One idea per diagram

## 5. Background and contrast

The user chooses the background: transparent, light (`#ffffff`), dark (`#1e1e1e`), or another color. Those values are suggestions, not a closed default. Do not strip `background` to force transparency.

Contrast is not a fixed color. It is harmony of the whole diagram.

- Text separates from its component fill
- The component separates from its container
- The container and the arrows separate from the page
- A transparent background must still read on both a light slide and a dark slide. If it will not, ask for the theme before export
