# Layout guidelines

Read from SKILL.md when drawing an AWS architecture or a diagram with several flow types. Arrow targets, routing, containment, labels and background live in SKILL.md; this file only adds group nesting, line meaning, placement direction and one containment bad example (an inset that is still not grouped).

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

### 2.1 Accessibility

Accessibility: never carry a meaning by color alone. Back each color with a second cue so the diagram reads in grayscale and for color-blind readers: the line style above (`dashed=1`), a text label on the line or group, or a different shape. The legend lists both the color and the cue.

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

## 4. Inset is not grouping

The 30px inset rule in SKILL.md (Containers are parents) is about space; the `parent` rule is about grouping, and each needs its own check. A title inset 30px from a frame but still parented to the page looks right and still cannot be dragged with the block.

Bad (the `label` is 30px below the frame top, `y=50` against the frame's `y=20`, but its `parent` is the page `1`):

```xml
<mxCell id="bg" value="VPC" style="rounded=1;strokeWidth=3;" vertex="1" parent="1">
  <mxGeometry x="500" y="20" width="560" height="430" as="geometry"/>
</mxCell>
<mxCell id="label" value="Title" style="text;html=1;" vertex="1" parent="1">
  <mxGeometry x="510" y="50" width="540" height="35" as="geometry"/>
</mxCell>
```

Fix: set `parent="bg"` and convert the geometry to the frame's origin (`x = 510 - 500 = 10`, `y = 50 - 20 = 30`), so the label moves with the frame:

```xml
<mxCell id="label" value="Title" style="text;html=1;" vertex="1" parent="bg">
  <mxGeometry x="10" y="30" width="540" height="35" as="geometry"/>
</mxCell>
```
