# Step 3 verdicts: mermaid-diagrams (pending rows)

Test: real value, spirit, cut carelessly. Baseline description: "Comprehensive guide for creating software diagrams using Mermaid syntax" (types, classify-first); current description keeps both and adds repair and validation.

| item | decision now | verdict | restore reason class | evidence |
| --- | --- | --- | --- | --- |
| s027 Flowchart (User Journey) | drop-pending | DROP | - | old: classDef step fill:#f5f5f5 ... class Auth,Validate decision; a model writes this from the section 6 palette rule unprompted |
| s044 Complete Configuration Example | drop-pending | DROP | - | old: theme base, look handDrawn, layout dagre, themeVariables; every key is covered by the s032/s040 restore |
| s046 Sequence Diagram Styling | drop-pending | DROP | - | old: %%{init: {'theme':'forest'}}%% after the messages; mmdc 12.3 still parses it, docs call directives deprecated |
| s047 Class Diagram Styling | drop-pending | DROP | - | old: %%{init: {'theme':'dark'}}%% at the end of a classDiagram; same as s046 |
| s050 Tooltips | drop-pending | DROP | - | old: "link A: API Documentation @ https://api.example.com" in a flowchart; mmdc exit 1, Parse error on line 5 |
| s051 Subgraph Styling | drop-pending | DROP | - | old: style Frontend fill:#e3f2fd,stroke:#2196f3,stroke-width:2px; capable models produce style on a subgraph id without help |
| s053 Complex Styling Example | drop-pending | DROP | - | old: subgraph production with direction LR and edges from outside; fills #ffeb3b/#ce93d8; probe renders without error, so the trap is silent |
| s054 Responsive Sizing | drop-pending | DROP | - | old: <div style="max-width: 100%; overflow: auto;"><pre class="mermaid"> ... |
| s055 SVG Export Options | drop-pending | DROP | - | old: mmdc -i diagram.mmd -o output.svg -w 1920 -H 1080; probe: error: unknown option '-w', exit 1 |
| s056 Best Practices for Advanced Features | drop-pending | DROP | - | old: "Use ELK for complex layouts - When dagre creates crossed lines"; layouts page: ELK is bundled and default from v12.0.0 |
| s058 Performance Considerations | drop-pending | DROP | - | old: "Use ELK layout for diagrams with >20 nodes"; ELK default since 12.0.0, split rule in section 2 |
| s059 HTML Files | drop-pending | DROP | - | old: import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs'; usage page: mermaid@12 |
| s060 React Components | drop-pending | DROP | - | old: React.useEffect(() => { mermaid.contentLoaded(); }); usage page: "mermaid.run ... is the preferred way" |
| s068 Using @iconify-json Icon Packs | drop-pending | DROP | - | old table lists @iconify-json/logos, bi, mdi, simple-icons; the iconify.design link stays and the pack names are discoverable there |
| s069 Complex Example | drop-pending | DROP | - | old: service lb(load_balancer)[Load Balancer]; service api1(api)[API Server 1]; docs: five default icons |
| s072 Best Practices | drop-pending | DROP | - | old: "Label edges with protocols (HTTPS, TCP, etc.)"; the docs define no edge-label syntax, SKILL.md says put the protocol in the service title for GitHub |
| s098 Microservices Architecture Example | drop-pending | DROP | - | old: 7 services plus data layer for a streaming platform; a model composes this from the element list |
| s101 Three-Tier Architecture | drop-pending | DROP | - | Three-tier container example (Nginx, Node, Java, MySQL); trivial composition of the element macros. |
| s104 Defining Classes with Members | drop-pending | DROP | - | old: + public, - private, # protected, ~ package; any capable model writes members like this unprompted |
| s105 Association (`--`) | drop-pending | DROP | - | old: "Loose relationship where entities use each other but exist independently" |
| s106 Composition (`*--`) | drop-pending | DROP | - | old: "Strong ownership - child cannot exist without parent" |
| s107 Aggregation (`o--`) | drop-pending | DROP | - | old: "Weaker ownership - child can exist independently" |
| s108 Inheritance (`</--`) | drop-pending | DROP | - | old: Animal </-- Dog; Animal </-- Cat |
| s109 Dependency (`<..`) | drop-pending | DROP | - | old: "One class depends on another" with OrderProcessor <.. PaymentGateway; docs table lists ..> |
| s112 Class Stereotypes | drop-pending | DROP | - | old: <<service>>, <<dataclass>>; docs: annotation text describes the nature of the class |
| s115 Comprehensive Example: E-Commerce Domain | drop-pending | DROP | - | old: 6 classes plus <<enumeration>> OrderStatus; relationship forms are in the current example |
| s116 Value Objects | drop-pending | DROP | - | Value-object stereotype example (<<value object>>: Money, Address); DDD stereotype names are free text. |
| s117 Aggregates | drop-pending | DROP | - | Aggregate-root stereotype example (<<aggregate root>> on Order); same free-text annotation. |
| s118 Tips for Effective Class Diagrams | drop-pending | DROP | - | old tips 1-6 are generic modeling advice; "add multiplicity" is in Traps |
| s120 Factory Pattern | drop-pending | DROP | - | Factory pattern example (ShapeFactory ..> Shape : creates); a GoF pattern a model draws unprompted. |
| s121 Strategy Pattern | drop-pending | DROP | - | Strategy pattern example (PaymentProcessor, PaymentStrategy interface, two implementations); a GoF pattern a model draws unprompted. |
| s127 Data Types | drop-pending | DROP | - | old: int, bigint, varchar, text, decimal, boolean, date, json, uuid, blob |
| s128 Comprehensive Example: E-Commerce Database | drop-pending | DROP | - | old: CUSTOMER/ORDER/LINE_ITEM/PRODUCT/... with "DEFAULT NOW()" comments; comment syntax is in Traps |
| s131 Best Practices | drop-pending | DROP | - | old: "Include timestamps", "Show indexes", "Use appropriate types"; singular UPPER_SNAKE is step 1 of Schema to diagram |
| s132 Self-Referencing (Hierarchical) | drop-pending | DROP | - | old: CATEGORY //--o{ CATEGORY : "parent of" with parent_id FK "NULLABLE" |
| s136 Audit Trail | drop-pending | DROP | - | Document and DOCUMENT_VERSION audit example; a one-to-many with a version table, nothing Mermaid-specific. |
| s139 Basic Syntax | drop-pending | DROP | - | Direction list (TD/TB, BT, LR, RL); authoring-rules.md section 2 covers TD versus LR. |
| s142 Nested Subgraphs | drop-pending | DROP | - | Nested subgraph example (Outer containing Inner); nested syntax is plain `subgraph ... end`. |
| s144 Individual Node Styling | drop-pending | DROP | - | Per-node `style B fill:...` example; section 6 requires fill, stroke and color together. |
| s145 Class-based Styling | drop-pending | DROP | - | The `:::className` shorthand with classDef; section 6 shows `class A,B svc` and section 3 names `classDef + :::` for ER and class diagrams. |
| s147 Comprehensive Example: User Registration Flow | drop-pending | DROP | - | old: 15-node registration flow with style Start fill:#e8f5e9,stroke:#333; styles omit color against the contrast rule |
| s149 CI/CD Pipeline | drop-pending | DROP | - | old: Development, CI, QA, Production subgraphs with rollback branch; architecture-diagrams.md carries a CI/CD architecture-beta |
| s151 Decision Matrix Example | drop-pending | DROP | - | old: Env, Change type, Approval status decisions into Block and Monitor nodes |
| s154 Branching Decision | drop-pending | DROP | - | Branching decision example (diamond with True and False paths); section 5 gives the diamond rule. |
| s155 Loop Pattern | drop-pending | DROP | - | old: C{Continue?} -->/Yes/ B back-edge |
| s157 Sequence Diagrams | drop-pending | DROP | - | Intro sentence ("sequence diagrams show interactions between participants over time"). |
| s158 Participants and Actors | drop-pending | DROP | - | old: participant = system components, actor = external entities |
| s169 Right/Left notes | drop-pending | DROP | - | old: Note right of System: Logs to database; Note left of User: Updates UI |
| s172 Comprehensive Example: User Authentication Flow | drop-pending | DROP | - | old: 6 participants, alt inside alt, opt, par, activations; every construct is in the current example |
| s173 API Request/Response Example | drop-pending | DROP | - | API request/response sequence with nested alt blocks and activations (gateway, auth, user service). |
| s174 Microservices Communication | drop-pending | DROP | - | old: break Insufficient stock, alt Payment successful, par ... and; constructs are in Blocks |
