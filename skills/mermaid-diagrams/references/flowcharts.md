# Flowcharts

Flowcharts visualize a process someone walks, with decisions. They are not the default diagram. If the question is a call chain, schema, domain model, lifecycle, or architecture, use sequence, ERD, class, state, or C4 instead. Rules for proportion, connections, shapes, and color: [authoring-rules.md](authoring-rules.md).

## Basic Syntax

```mermaid
flowchart TD
    A --> B
```

**Directions:**
- `TD` or `TB` - Top to Bottom (default)
- `BT` - Bottom to Top
- `LR` - Left to Right
- `RL` - Right to Left

## Node Shapes

### Rectangle (default)
```mermaid
flowchart LR
    A[Process step]
```

### Rounded Rectangle
```mermaid
flowchart LR
    B([Rounded process])
```

### Stadium/Pill Shape
```mermaid
flowchart LR
    C(Start or End)
```

### Subroutine (Double Border)
```mermaid
flowchart LR
    D[[Subroutine]]
```

### Cylindrical (Database)
```mermaid
flowchart LR
    E[(Database)]
```

### Circle
```mermaid
flowchart LR
    F((Circle node))
```

### Asymmetric/Flag
```mermaid
flowchart LR
    G>Flag node]
```

### Rhombus (Decision)
```mermaid
flowchart LR
    H{Decision?}
```

### Hexagon
```mermaid
flowchart LR
    I{{Hexagon}}
```

### Parallelogram (Input/Output)
```mermaid
flowchart LR
    J[/Input or Output/]
    K[\Alternative IO\]
```

### Trapezoid
```mermaid
flowchart LR
    L[/Trapezoid\]
    M[\Alt trapezoid/]
```

## Connections

### Basic Arrow
```mermaid
flowchart LR
    A --> B
```

### Open Link (No Arrow)
```mermaid
flowchart LR
    A --- B
```

### Text on Links
```mermaid
flowchart LR
    A -->|Label text| B
    C ---|"Text with spaces"| D
```

### Dotted Links
```mermaid
flowchart LR
    A -.-> B
    C -.- D
    E -.Label.-> F
```

### Thick Links
```mermaid
flowchart LR
    A ==> B
    C === D
    E ==Label==> F
```

### Chaining
```mermaid
flowchart LR
    A --> B --> C --> D
    E --> F & G --> H
```

### Multi-directional
```mermaid
flowchart LR
    A --> B & C & D
    B & C & D --> E
```

## Subgraphs

A flowchart is only the right type when someone walks a process with decisions. If the picture is a call chain, a schema, a domain model, or an architecture, stop and use sequence, ERD, class, or C4 instead. See [authoring-rules.md](authoring-rules.md).

Group related nodes once there are about ten or more. Connect groups at the boundary. Do not link a node inside one subgraph to a node inside another: Mermaid then ignores that subgraph's `direction` and inherits the parent's, with no error.

```mermaid
flowchart TD
    subgraph SG_INGEST
        direction TB
        NODE_INGEST_fetch[Fetch]
        NODE_INGEST_parse[Parse]
        NODE_INGEST_fetch --> NODE_INGEST_parse
    end

    subgraph SG_STORE
        direction TB
        NODE_STORE_write[(Write)]
    end

    SG_INGEST --> SG_STORE
```

### Nested Subgraphs
```mermaid
flowchart TB
    subgraph Outer
        A[Node A]
        
        subgraph Inner
            B[Node B]
            C[Node C]
        end
    end
```

### Subgraph Direction
```mermaid
flowchart LR
    subgraph one
        direction TB
        A1 --> A2
    end
    
    subgraph two
        direction TB
        B1 --> B2
    end
    
    one --> two
```

## Styling

### Individual Node Styling
```mermaid
flowchart LR
    A[Normal]
    B[Styled]
    
    style B fill:#fff8e1,stroke:#b26a00,color:#111111
```

### Class-based Styling
```mermaid
flowchart LR
    A[Node 1]:::className
    B[Node 2]:::className
    C[Node 3]
    
    classDef className fill:#ede7f6,stroke:#4527a0,color:#111111
```

### Link Styling
```mermaid
flowchart LR
    A --> B
    linkStyle 0 stroke:#1565c0,stroke-width:2px
```

## Comprehensive Example: User Registration Flow

```mermaid
flowchart TD
    Start([User visits registration page]) --> Form[Show registration form]
    Form --> Input[User enters details]
    Input --> Validate{Valid input?}
    
    Validate -->|No| ShowError[Show validation errors]
    ShowError --> Form
    
    Validate -->|Yes| CheckEmail{Email exists?}
    
    CheckEmail -->|Yes| EmailError[Show 'Email already registered']
    EmailError --> Form
    
    CheckEmail -->|No| CreateAccount[Create user account]
    CreateAccount --> Hash[Hash password]
    Hash --> SaveDB[(Save to database)]
    SaveDB --> GenerateToken[Generate verification token]
    GenerateToken --> SendEmail[Send verification email]
    SendEmail --> ShowSuccess[Show success message]
    ShowSuccess --> End([Redirect to login])
    
    style Start fill:#e8f5e9,stroke:#333,stroke-width:2px
    style End fill:#e8f5e9,stroke:#333,stroke-width:2px
    style CreateAccount fill:#e3f2fd,stroke:#333,stroke-width:2px
    style SaveDB fill:#fff8e1,stroke:#333,stroke-width:2px
```

## Algorithm Example: Binary Search

```mermaid
flowchart TD
    Start([Start Binary Search]) --> Init[Set low = 0, high = array.length - 1]
    Init --> Check{low <= high?}
    
    Check -->|No| NotFound[Return -1: Not found]
    NotFound --> End([End])
    
    Check -->|Yes| CalcMid[mid = low + (high - low) / 2]
    CalcMid --> Compare{array[mid] == target?}
    
    Compare -->|Yes| Found[Return mid: Found]
    Found --> End
    
    Compare -->|No| CheckLess{array[mid] < target?}
    
    CheckLess -->|Yes| MoveLow[low = mid + 1]
    MoveLow --> Check
    
    CheckLess -->|No| MoveHigh[high = mid - 1]
    MoveHigh --> Check
    
    style Start fill:#e8f5e9
    style End fill:#e8f5e9
    style Found fill:#fff8e1
    style NotFound fill:#fdecea,stroke:#c62828,color:#111111
```

## CI/CD Pipeline

```mermaid
flowchart LR
    subgraph Development
        Commit[Developer commits code] --> Push[Push to repository]
    end
    
    subgraph CI
        Push --> Trigger[Trigger CI pipeline]
        Trigger --> Checkout[Checkout code]
        Checkout --> Install[Install dependencies]
        Install --> Lint[Run linters]
        Lint --> Test[Run tests]
        Test --> Build[Build application]
    end
    
    subgraph QA
        Build --> DeployStaging[Deploy to staging]
        DeployStaging --> E2E[Run E2E tests]
        E2E --> ManualQA{Manual QA approval?}
    end
    
    subgraph Production
        ManualQA -->|Approved| DeployProd[Deploy to production]
        DeployProd --> HealthCheck{Health check passed?}
        HealthCheck -->|Yes| Success([Deployment successful])
        HealthCheck -->|No| Rollback[Rollback deployment]
        Rollback --> Alert[Alert team]
    end
    
    ManualQA -->|Rejected| FixIssues[Fix issues]
    FixIssues --> Development
    
    Test -->|Failed| NotifyDev[Notify developer]
    NotifyDev --> FixIssues
```

## E-Commerce Checkout Flow

```mermaid
flowchart TD
    Start([User clicks Checkout]) --> Auth{Authenticated?}
    
    Auth -->|No| Login[Redirect to login]
    Login --> Auth
    
    Auth -->|Yes| Cart{Cart empty?}
    Cart -->|Yes| EmptyCart[Show empty cart message]
    EmptyCart --> Browse[Redirect to products]
    
    Cart -->|No| Address[Show shipping address form]
    Address --> ValidateAddr{Valid address?}
    ValidateAddr -->|No| Address
    ValidateAddr -->|Yes| Shipping[Select shipping method]
    
    Shipping --> Payment[Enter payment details]
    Payment --> ValidatePayment{Valid payment info?}
    ValidatePayment -->|No| Payment
    
    ValidatePayment -->|Yes| Review[Show order review]
    Review --> Confirm{Confirm order?}
    
    Confirm -->|No| Edit{Edit what?}
    Edit -->|Address| Address
    Edit -->|Shipping| Shipping
    Edit -->|Payment| Payment
    
    Confirm -->|Yes| ProcessPayment[Process payment]
    ProcessPayment --> PaymentResult{Payment successful?}
    
    PaymentResult -->|No| PaymentError[Show payment error]
    PaymentError --> RetryPayment{Retry?}
    RetryPayment -->|Yes| Payment
    RetryPayment -->|No| Cancel([Order cancelled])
    
    PaymentResult -->|Yes| CreateOrder[(Create order record)]
    CreateOrder --> ReduceStock[Reduce inventory]
    ReduceStock --> SendConfirmation[Send confirmation email]
    SendConfirmation --> Success([Order complete - Show confirmation])
    
    style Start fill:#e8f5e9
    style Success fill:#e8f5e9
    style Cancel fill:#fdecea,stroke:#c62828,color:#111111
    style CreateOrder fill:#fff8e1
```

## Decision Matrix Example

```mermaid
flowchart TD
    Start([Select deployment strategy]) --> Env{Environment?}
    
    Env -->|Development| DevDecision{Automated tests?}
    DevDecision -->|Pass| DevDeploy[Auto-deploy to dev]
    DevDecision -->|Fail| Block[Block deployment]
    
    Env -->|Staging| StageDecision{All checks pass?}
    StageDecision -->|Yes| StageDeploy[Deploy to staging]
    StageDecision -->|No| Block
    
    Env -->|Production| ProdDecision{Change type?}
    
    ProdDecision -->|Hotfix| Urgent{Critical bug?}
    Urgent -->|Yes| FastTrack[Emergency approval + deploy]
    Urgent -->|No| NormalProcess
    
    ProdDecision -->|Feature| NormalProcess{Approval status?}
    NormalProcess -->|Approved| Schedule{Deploy window?}
    NormalProcess -->|Pending| Wait[Wait for approval]
    NormalProcess -->|Rejected| Block
    
    Schedule -->|Now| ImmediateDeploy[Deploy immediately]
    Schedule -->|Scheduled| QueueDeploy[Queue for deploy window]
    
    DevDeploy --> Monitor[Monitor metrics]
    StageDeploy --> Monitor
    FastTrack --> Monitor
    ImmediateDeploy --> Monitor
    QueueDeploy --> Monitor
    
    Monitor --> End([Deployment complete])
    Block --> End
    Wait --> End
```

## Best Practices

1. **Confirm this is a flowchart** - A walked process with decisions. Otherwise switch type.
2. **Fit the reading column** - Prefer `TD`. Height/width at least 0.4. Do not switch to `LR` to uncrowd a diagram; the column will shrink the text.
3. **Shapes are roles** - Rectangle = step, diamond = any node with two or more outgoing branches, cylinder = store, stadium = start/end.
4. **Connect subgraphs at the boundary** - Never inner node to inner node. See [authoring-rules.md](authoring-rules.md).
5. **Color by role** - Copy palette A, B, or C from `authoring-rules.md`. Six or more nodes need a `classDef`. No more than six fills.
6. **One process** - Split a diagram taller than about three pages.

## Common Patterns

### Simple Linear Flow
```mermaid
flowchart LR
    A[Step 1] --> B[Step 2] --> C[Step 3] --> D[Step 4]
```

### Branching Decision
```mermaid
flowchart TD
    A[Input] --> B{Condition?}
    B -->|True| C[Path 1]
    B -->|False| D[Path 2]
    C --> E[Merge]
    D --> E
```

### Loop Pattern
```mermaid
flowchart TD
    A[Initialize] --> B[Process]
    B --> C{Continue?}
    C -->|Yes| B
    C -->|No| D[Exit]
```

### Error Handling
```mermaid
flowchart TD
    A[Try operation] --> B{Success?}
    B -->|Yes| C[Continue]
    B -->|No| D[Handle error]
    D --> E{Retry?}
    E -->|Yes| A
    E -->|No| F[Abort]
```
