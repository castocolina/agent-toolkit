## c4-architecture: 87.2%

- [medium] D1 skills/c4-architecture/references/advanced-patterns.md:175: Remove or sharply compress generic CQRS, API gateway, and cloud-deployment walkthroughs and basic C4 definitions. Retain non-obvious boundary decisions, evidence-extraction rules, and Mermaid-specific incompatibilities, with minimal examples for those issues.
- [medium] D6 skills/c4-architecture/SKILL.md:16: Make module count an optional complexity hint, not a restriction. Select component views according to the requested question, audience, meaningful responsibility boundaries, and available evidence; honor explicit component-view requests when the container can be identified.
- [medium] D7 skills/c4-architecture/evals/evals.json:1: Add a small repository fixture with build configuration, deployment manifests, runtime dependencies, and a shared library. Assert that generated views distinguish containers from libraries and attach evidence to inferred boundaries and relationships.
- [high] D8 skills/c4-architecture/references/advanced-patterns.md:436: Use Container_Boundary for the API's internal components, add a handler component as the relationship endpoint, and connect that handler to the circuit breaker. Validate the corrected example with the target Mermaid renderer.
- [low] D1 skills/c4-architecture/SKILL.md:18: The Level 1-4 rows restate the C4 hierarchy the model knows; keep only the non-obvious rows (Level 4 rarely useful; Dynamic/Deployment are supplementary, not levels).
- [low] D1 skills/c4-architecture/SKILL.md:30: State the rule once here; drop the duplicate 'Always model message topics/queues as separate containers' directive in references/advanced-patterns.md and keep only common-mistakes.md's wrong/correct example.
- [medium] D2 skills/c4-architecture/SKILL.md:37: Make verification a loop, not a clause: 'fix failing elements, re-render, and re-validate until the diagram passes'; currently nothing says what to do when validation fails.
- [low] D3 skills/c4-architecture/SKILL.md:37: This is the only in-body environment fact; inline two or three highest-cost mistakes (shared library as container, single broker box, bidirectional arrows) as a short NEVER list in SKILL.md, keeping the full catalogue in common-mistakes.md.
- [low] D6 skills/c4-architecture/SKILL.md:32: Add the default for the common unknown-audience case (e.g., 'audience unstated: Levels 1-2'); otherwise this bullet is a menu with no default.
- [medium] D7 skills/c4-architecture/evals/evals.json:-: Add one or two evals with a small fixture tree (build files, docker-compose, service manifests) so 'evidence-backed' assertions grade real extraction, plus an eval for the renderer-downgrade fallback branch.
- [medium] D8 skills/c4-architecture/SKILL.md:31: Align the element threshold across files: c4-syntax.md says 'under 15 elements' and common-mistakes.md says 'under 20 (ideally under 15)'; pick one rule ('under 20, ideally 15') so an agent following the syntax reference does not reject diagrams the main skill allows.
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## command-creator: 86.0%

- [medium] D1 skills/command-creator/references/patterns.md:9: Collapse generic workflow tutorials and native planning, todo, and delegation explanations. Keep command-specific field semantics, argument boundaries, environment constraints, and concrete failure-recovery decisions.
- [medium] D2 skills/command-creator/SKILL.md:14: Treat plan–approval–execution as an approval-gated workflow independent of delegation. Choose delegation only when specialization, isolation, or parallel work provides a concrete benefit.
- [medium] D3 skills/command-creator/SKILL.md:33: Add concise Gotchas explaining that argument-hint is display metadata rather than validation and that pre-run ! shell blocks execute during prompt expansion, before written workflow inspection or approval steps. Prohibit state-changing pre-run blocks and require explicit body-level argument validation.
- [medium] D6 skills/command-creator/references/examples.md:113: Replace the blanket prohibition with bounded inspection criteria: permit checks necessary to establish prerequisites, intended changes, authorization, and verification, while requiring approval before unrelated or open-ended exploration.
- [medium] D7 skills/command-creator/evals/evals.json:1: Add assertions for maximum attempts and stuck detection, plus edge cases covering shell-special characters in arguments and a timed-out publication that may already have succeeded. Verify validation, state inspection before retry, and explicit authorization boundaries.
- [high] D8 skills/command-creator/references/patterns.md:202: Apply the registered-agent check to every delegation example. Select an actually available suitable agent, and otherwise continue directly while preserving the planning and approval boundary; remove unconditional references to the custom subagent type.
- [low] D1 skills/command-creator/SKILL.md:14: Keep these four expert patterns in references/patterns.md; drop the generic Advanced Patterns section (context-file priority, conditional tool selection, progressive disclosure, makefile wrapper) that the model derives on its own.
- [low] D2 skills/command-creator/SKILL.md:16: State the validation loop explicitly: draft, check against the best-practices checklist, fix, re-check until it passes; step 5 names validation without the loop.
- [low] D3 skills/command-creator/SKILL.md:33: Add the why: a global override silently changes behavior for every future invocation in every project, not just this command run.
- [low] D6 skills/command-creator/SKILL.md:15: Define the one ambiguous case concretely (a repo exists but the user says 'for all my projects'); 'meaningful ambiguity' otherwise leaves a default-vs-ask boundary to judgment.
- [low] D7 skills/command-creator/evals/evals.json:-: Add a fixture transcript of a user's manual release procedure so the underspecified-workflow eval can grade requirement extraction against real input.
- [medium] D8 skills/command-creator/SKILL.md:16: Add an adaptation caveat when examples load: their tools (Graphite gt, make all-ci, .PLAN.md, TodoWrite) are project-specific; map them to the user's toolchain before reusing the skeleton.
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## commit-work: 90.0%

- [medium] D1 skills/commit-work/SKILL.md:17: Compress standard Git and Conventional Commit instructions. Prioritize the non-obvious constraints: user-owned index content, non-interactive mixed-hunk staging, index-versus-worktree verification, hook mutations, and stopping at the approved change set.
- [medium] D6 skills/commit-work/SKILL.md:25: Specify a safe verification branch when index and working tree differ: export the index tree to a disposable directory, run applicable checks there without changing the user's index or worktree, or stop and explicitly report that the staged version could not be verified. Do not silently stash or reset user changes.
- [medium] D7 skills/commit-work/evals/evals.json:6: Add disposable-repository or explicit state fixtures with pre-existing unrelated staged content, mixed intended and unrelated hunks, and a hook that changes the index. Assert that unrelated state is preserved and that retries require a fresh index review.
- [high] D8 skills/commit-work/SKILL.md:14: Route by requested intent before the workflow: message-only returns a proposed message without mutation; review-only reports findings without mutation; staging-only stops after index review; only an authorized commit request proceeds to git commit.
- [low] D1 skills/commit-work/SKILL.md:15: Ground the generic parts: check staged paths against .gitignore and the build outputs the CI config produces; keep lockfile-churn and scope-accuracy, the checks the model actually skips.
- [low] D2 skills/commit-work/SKILL.md:12: Split into 1a inspect, 1b ownership rule, 1c stop rule; one 60-word step hides the stop condition an agent must not miss.
- [low] D3 skills/commit-work/SKILL.md:24: Extend to the rebase case: during a rebase git status shows 'rebasing' and a commit silently continues it; check status in step 1, not just for conflict markers.
- [medium] D6 skills/commit-work/SKILL.md:12: Name the default tactic after authorization (e.g., stash unrelated staged content with git stash push --keep-index, or build the commit from a temporary index); 'an index-isolation strategy' leaves the fragile step to invention.
- [low] D7 skills/commit-work/evals/evals.json:-: Add evals/files fixtures (a status/diff snapshot with mixed staged and unstaged content) so selective-staging assertions grade real command sequences.
- [medium] D8 skills/commit-work/references/commit-message-template.md:3: SKILL.md step 6 never states the shape; add the minimal template there (type(scope)!: subject, blank line, body, footer) or move the shape into this reference so the cross-reference resolves.
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## crafting-effective-readmes: 82.0%

- [medium] D1 skills/crafting-effective-readmes/SKILL.md:12: Delete the verb-classification router and trim generic style reminders and template boilerplate. Concentrate the skill on evidence-backed first-use paths, generated content ownership, published-versus-checkout instructions, and concrete documentation drift traps.
- [medium] D2 skills/crafting-effective-readmes/SKILL.md:16: Add a clean-environment validation sequence: derive prerequisites from manifests and CI, exercise the documented first-use path without maintainer-local state, compare actual output with the README, and explicitly distinguish executed checks from static verification when execution is unavailable.
- [medium] D3 skills/crafting-effective-readmes/SKILL.md:21: Add concise, reasoned README traps: repository-root commands may not target the published workspace package; default-branch examples may not match released APIs; generated regions are overwritten by their owning tool. Gate each warning on repository evidence.
- [medium] D5 skills/crafting-effective-readmes/SKILL.md:27: Expose direct, scenario-gated links in SKILL.md: the formal specification for explicit Standard README compliance, its examples only when needed, and the reader-funnel article for audience-ordering problems. Keep supporting documents one navigation level from the entry point.
- [medium] D8 skills/crafting-effective-readmes/SKILL.md:13: Treat an absent remote as unknown, not Personal. Prefer the user's stated audience and project purpose; inspect available evidence and ask one consequential clarification when the project type remains unresolved.
- [medium] D1 skills/crafting-effective-readmes/templates/oss.md:1: Trim each template to the sections that differ per project type (the checklist matrix already carries the shared shape); full standard README skeletons are content the model already generates
- [low] D2 skills/crafting-effective-readmes/SKILL.md:12: Replace the verb mapping with a decision question ('Will the reader's first success change?') and state that combined update+audit requests run the audit before edits
- [medium] D3 skills/crafting-effective-readmes/SKILL.md:21: Add environment-specific gotchas: npm renders a subset of README HTML, GitHub anchor slugs differ from other renderers (punctuation stripping), and shields.io badges are blocked in some corporate networks
- [low] D5 skills/crafting-effective-readmes/references/using-references.md:32: Fold the two example links into the standard-readme-spec entry and state 'load at most one guide'; the current chain routes two levels deep from SKILL.md with no load limit
- [low] D6 skills/crafting-effective-readmes/SKILL.md:16: State the fallback for items source cannot confirm (e.g., external links, CI badges): label them 'unverified' in the output instead of asserting them
- [medium] D8 skills/crafting-effective-readmes/SKILL.md:13: Add a monorepo branch: confirm whether the target is the root README or a package README before inferring type, since signals frequently conflict across packages
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## daily-meeting-update: 88.8%

- [medium] D1 skills/daily-meeting-update/SKILL.md:33: Compress the standard questions and output headings into a compact contract. Retain the higher-value consent ordering, day filtering, unresolved-path handling, privacy safeguards, and cross-source deduplication.
- [medium] D2 skills/daily-meeting-update/SKILL.md:38: Add a provenance gate before drafting: require user confirmation or explicit completion evidence for outcome claims; treat read/edit/command counts as activity only, and ask for confirmation before promoting them to completed work.
- [low] D7 skills/daily-meeting-update/evals/evals.json:1: Add an approved-integration case with scoped activity fixtures. Assert from the tool trace that authentication/history access occurs only after approval, only approved scope or sessions are used, duplicate work is merged, and raw session text is not exposed.
- [medium] D8 skills/daily-meeting-update/scripts/claude_digest.py:257: Preserve cwd and branch on individual messages, filter by the requested day first, and derive metadata from those filtered messages. Split or explicitly represent sessions that change project or branch.
- [medium] D8 skills/daily-meeting-update/scripts/claude_digest.py:220: Convert each timestamp with the system's date-aware local conversion, such as timestamp.astimezone() without the captured fixed-offset argument, or use an explicit ZoneInfo timezone. Add deterministic tests on both sides of a DST transition.
- [low] D1 skills/daily-meeting-update/SKILL.md:29: Compress the four interview questions into a single line and keep only the expert rules (grouping, outcome-vs-investigation distinction)
- [low] D2 skills/daily-meeting-update/SKILL.md:38: Add: if approved activity contradicts an answer (e.g. user says no blockers but commits suggest stalled work), surface the discrepancy and ask before including it
- [low] D3 skills/daily-meeting-update/SKILL.md:73: Append a one-clause reason to each item (e.g. investigations reported as done inflate status and mislead sprint tracking)
- [low] D6 skills/daily-meeting-update/SKILL.md:22: State: always run claude_digest.py with --format json and render the summary yourself
- [medium] D8 skills/daily-meeting-update/SKILL.md:22: Add: if the digest reports zero sessions, say so once and continue with the interview
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## database-schema-designer: 88.4%

- [medium] D1 skills/database-schema-designer/references/schema-design-checklist.md:19: Replace the generic checklist content with compact, decision-oriented checks for tenant isolation, nullable uniqueness, soft deletes, query-prefix coverage, lock behavior, concurrent writes during backfill, and recovery limitations.
- [medium] D7 skills/database-schema-designer/evals/evals.json:20: Assert that tenant-inconsistent user/project/task relationships are rejected by the generated constraints or an explicitly justified equivalent. Add a MongoDB case involving unbounded growth or the document-size boundary and verify the embedding/reference decision.
- [high] D8 skills/database-schema-designer/references/schema-design-checklist.md:57: Replace the blanket requirement with an engine- and workload-specific check of existing leading-prefix coverage, join and parent-delete costs, and write amplification. Explicitly allow a documented decision not to add an index.
- [high] D8 skills/database-schema-designer/references/schema-design-checklist.md:39: Distinguish instants from civil dates and local wall-clock times. Default PostgreSQL instant fields to TIMESTAMPTZ with an explicit input/output timezone policy, update the template accordingly, and document engine-specific alternatives rather than equating TIMESTAMP with UTC.
- [medium] D1 skills/database-schema-designer/references/schema-design-checklist.md:107: Prune the Security, Performance and Documentation sections to schema-relevant checks only
- [low] D2 skills/database-schema-designer/SKILL.md:13: Add default labeled assumptions (e.g. single-tenant, moderate scale, new schema) to state when context is missing
- [low] D3 skills/database-schema-designer/SKILL.md:28: Define it (columns whose values are opaque tokens or secrets) and add a one-line example
- [medium] D5 skills/database-schema-designer/SKILL.md:34: Delete the pointer or add the engine-specific reference files it names
- [low] D6 skills/database-schema-designer/SKILL.md:17: Default to EXPLAIN (ANALYZE) on PostgreSQL and name the per-engine equivalents
- [high] D8 skills/database-schema-designer/references/schema-design-checklist.md:57: Reword to 'FK indexes justified by join/parent-delete cost and write impact' to match the SKILL.md policy
- Reason it ships: 3 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## design-system-starter: 89.2%

- [medium] D1 skills/design-system-starter/SKILL.md:16: Compress the standard token-category and documentation inventories into short output requirements. Keep the substantive guidance on selecting an adopter, validating theme-state pairs, limiting escape hatches, and preserving token meaning.
- [medium] D5 skills/design-system-starter/SKILL.md:42: Load templates/component-template.tsx only when implementing a React component scaffold; explicitly skip it for token-only deliverables and other frameworks.
- [medium] D6 skills/design-system-starter/checklists/design-system-checklist.md:365: Make the checklist scope-dependent, allow justified N/A entries, and gate release on the chosen pilot and supported distribution channels. Treat component inventories, publication platforms, and numeric budgets as project decisions rather than universal requirements.
- [medium] D7 skills/design-system-starter/evals/evals.json:16: Add a token fixture with a cycle, a missing alias target, and an actual failing foreground/background pair. Assert that each defect is identified and corrected or explicitly blocks component implementation.
- [medium] D7 skills/design-system-starter/evals/trigger-queries.json:23: Label the standalone modal audit as a near-miss negative, or rewrite the positive to specify reviewing a shared modal primitive used across the design system.
- [high] D8 skills/design-system-starter/templates/component-template.tsx:38: Keep the button scaffold limited to valid phrasing content and remove its Header/Body members, or provide a separate non-interactive container scaffold for compound Header/Body composition. Validate the resulting DOM structure in a rendered example.
- [medium] D1 skills/design-system-starter/checklists/design-system-checklist.md:312: Cut Governance, Adoption & Maintenance, Pre-Launch and Post-Launch (lines 312-386) to the few items that gate design-system correctness; the model already knows generic program management, and by line count this dilutes the expert SKILL.md.
- [low] D2 skills/design-system-starter/SKILL.md:19: Add a tie-breaker: when several patterns qualify equally, pick the one whose consuming screen is already scheduled for change this cycle, so adoption is measurable.
- [low] D3 skills/design-system-starter/SKILL.md:35: Move this to-do into workflow step 8; a gotchas entry should be a mistake with a reason, e.g. "Never document a component by example alone — list props and states, or consumers copy the example's exact prop set."
- [low] D5 skills/design-system-starter/SKILL.md:42: Gate it like the other three resources: "Load templates/component-template.tsx only when scaffolding a brand-new component; otherwise compose from the existing hierarchy."
- [low] D6 skills/design-system-starter/SKILL.md:21: Name the verification method for this fragile check: computed-style assertions per theme and state (as in references/component-examples.md) or an axe contrast-rule run; thresholds alone leave the agent guessing how to measure.
- [low] D7 skills/design-system-starter/evals/evals.json:26: Add a small legacy-UI fixture under evals/files/ (a page with hardcoded hex values and icon-only buttons) and reference it in the eval's files so audit assertions are checkable against an actual input.
- [low] D8 skills/design-system-starter/SKILL.md:24: State the no-rig fallback: when the project has no component test setup, do a keyboard-only and 200%-zoom pass on the pilot screen and say so, instead of leaving the check undefined.
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## difficult-workplace-conversations: 84.8%

- [medium] D1 skills/difficult-workplace-conversations/references/emotional-regulation.md:210: Remove general wellness instruction and repetitive paraphrase menus. Keep concise workplace-specific procedures for evidence quality, power, disputed facts, pauses with reconvening times, reporting boundaries, and safe escalation.
- [medium] D2 skills/difficult-workplace-conversations/SKILL.md:17: Add a short negotiation decision procedure: make the concrete request, distinguish evidence objections from budget/process/authority constraints, identify tradable versus fixed terms, and close with a decision owner, criteria, and dated checkpoint or explicit fallback.
- [medium] D6 skills/difficult-workplace-conversations/references/conversation-framework.md:90: Present duration and timing as adjustable defaults based on participant availability, urgency, topic, and follow-up access. Replace the Friday prohibition with a requirement to arrange appropriate support and a concrete follow-up opportunity.
- [low] D7 skills/difficult-workplace-conversations/evals/evals.json:5: Add a multi-party boundary case where authority or consent is absent, and a suitable facilitated case with conflicting accounts. Assert that the first avoids a joint meeting and the second preserves disputed facts, gives each participant a voice, and records explicit agreements.
- [medium] D8 skills/difficult-workplace-conversations/SKILL.md:40: Add a dedicated facilitation section or reference covering separate preparation, confidentiality limits, consent and ground rules, balanced speaking turns, reconciliation of shared versus disputed facts, stop/escalation conditions, and participant-specific commitments. Keep the two-person guide routed to direct conversations.
- [medium] D1 skills/difficult-workplace-conversations/references/emotional-regulation.md:214: Prune the file to the regulation worksheet, trigger inventory, and workplace day-of preparation
- [medium] D1 skills/difficult-workplace-conversations/references/conversation-framework.md:1: Cut the textbook explanation and keep the expert deltas: time/place rules, agreement and email templates, success measures
- [low] D2 skills/difficult-workplace-conversations/SKILL.md:24: Add a negotiation default: purpose + evidence + specific ask + openness to alternatives
- [low] D3 skills/difficult-workplace-conversations/SKILL.md:33: Add: assume any written summary may be reviewed in a formal HR/legal process; keep records factual and shared only need-to-know
- [low] D4 skills/difficult-workplace-conversations/SKILL.md:4: Change to `allowed-tools: Read Glob Grep`
- [low] D5 skills/difficult-workplace-conversations/SKILL.md:13: Reference the sibling skill by name ('route to the feedback-mastery skill') rather than a file path
- [low] D5 skills/difficult-workplace-conversations/SKILL.md:40: Reword the trigger to 'for full three-phase preparation or a facilitated multi-party plan'
- [low] D6 skills/difficult-workplace-conversations/SKILL.md:24: Default to formal-neutral, short sentences with senior stakeholders unless the user signals otherwise
- [medium] D8 skills/difficult-workplace-conversations/references/emotional-regulation.md:228: Add a usage note at the top: offer at most one in-the-moment technique when the user asks; never lecture on sleep or therapy
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## domain-name-brainstormer: 88.4%

- [medium] D1 skills/domain-name-brainstormer/SKILL.md:13: Compress the common naming-pattern recipe and routine output guidance. Preserve the less-obvious multilingual, registration-status, renewal-cost, and deployment constraints.
- [medium] D2 skills/domain-name-brainstormer/SKILL.md:15: Apply hard language, confusion, and budget constraints before ranking. Then rank surviving candidates using the user's stated priorities, explicitly explaining any trade-off between memorability, descriptiveness, spelling reliability, and recurring cost.
- [low] D7 skills/domain-name-brainstormer/evals/evals.json:19: Require exactly 12 distinct candidates in this test and separately verify the requested grouping and top-three explanations.
- [medium] D8 skills/domain-name-brainstormer/SKILL.md:16: Define failed or inconclusive lookups as unknown/unverified, never available. Explain when to retry through a registrar, and distinguish an authoritative registration result from confirmed purchase availability.
- [low] D1 skills/domain-name-brainstormer/SKILL.md:13: Compress the naming-pattern catalog the model already knows to one line and spend the tokens on the screening, registry-status, and legal-risk rules that are the skill's real value
- [low] D2 skills/domain-name-brainstormer/SKILL.md:13: Fold the derivable generate-then-screen steps 2-3 into a single generate-and-screen step and lead the procedure with the claim-discipline rules that distinguish the skill
- [low] D3 skills/domain-name-brainstormer/SKILL.md:23: Replace the hand-wavy escape hatch (no audience expects homographs) with a hard rule: reject confusable characters outright, and if a lookalike is ever proposed require a confusables check before shortlisting
- [low] D6 skills/domain-name-brainstormer/SKILL.md:12: State a default assumption set (short, English, .com-first) so a casual ask can proceed without questions, and ask only when a answer would change the shortlist
- [low] D7 skills/domain-name-brainstormer/evals/evals.json:-: Add an eval with an RDAP-response fixture in evals/files/ asserting that the source and check time are recorded and unchecked candidates are labeled unverified
- [low] D8 skills/domain-name-brainstormer/SKILL.md:16: Name a fallback for when RDAP is rate-limited or a TLD lacks it (registrar search page) and require recording which source was checked
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## draw-io: 85.6%

- [medium] D4 skills/draw-io/SKILL.md:3: Create and edit uncompressed .drawio/mxGraph XML diagrams and export editable PNGs. Use for draw.io files, AWS architecture diagrams with mxgraph.aws4 icons, connector or container layout fixes, and diagram figures for Quarto/reveal.js, including requests for an editable architecture diagram without naming draw.io. Not for Mermaid, Excalidraw, Graphviz, general slide styling, or OCR.
- [medium] D1 skills/draw-io/SKILL.md:84: Delete elementary coordinate explanations and generic clarity/consistency advice. Retain mxGraph-specific containment, connector routing, font propagation, and export constraints.
- [high] D8 skills/draw-io/scripts/convert-drawio-to-png.sh:59: Make staging an explicit opt-in or place it in a separate pre-commit wrapper. Standalone conversion should succeed without Git and leave the index unchanged.
- [high] D8 skills/draw-io/scripts/convert-drawio-to-png.sh:39: Export to a temporary PNG, validate it, and atomically replace the destination only after success. On failure, remove only temporary artifacts and preserve the previous PNG.
- [medium] D2 skills/draw-io/SKILL.md:73: Add a short creation sequence: establish topology and output constraints, initialize the document, create parent containers before children, connect and route edges, export, inspect, and repeat corrections until the checklist passes.
- [medium] D5 skills/draw-io/SKILL.md:41: Use skill-root-relative script references and resolve the installed skill directory at runtime. Preserve the target project's working directory or pass absolute diagram paths.
- [medium] D6 skills/draw-io/SKILL.md:236: Apply 16:9 proportions and slide-specific sizing only to slide figures. Otherwise preserve the user's intended medium, canvas, and aspect ratio.
- [medium] D7 skills/draw-io/evals/evals.json:7: Require an actual parseable .drawio document and assertions for its root cells, requested nodes, edges, and background rather than accepting a plan.
- [medium] D7 skills/draw-io/scripts/find_aws_icon.py:61: Implement --help for both scripts and machine-readable result modes, with diagnostics on stderr. Extend the existing tests to verify those interfaces and background-selection branches.
- [medium] D1 skills/draw-io/SKILL.md:114: Replace the 5.4 diagram-type taxonomy table (model-known) with expert guidance on when to split one system into staged diagrams and the staging order to use
- [low] D1 skills/draw-io/SKILL.md:84: Delete the center-coordinate arithmetic; keep only the rule to match centers when aligning elements
- [low] D2 skills/draw-io/SKILL.md:72: Compress 4.1 to a diagnostic principle (find the misaligned pair by value, fix geometry as a child of its container, re-export and verify) and drop the editor mechanics
- [low] D3 skills/draw-io/SKILL.md:152: Consolidate the NEVER items scattered across sections 2-6.9 (back-layer arrows, -t misuse, sibling labels) into one Gotchas list with reasons
- [low] D4 skills/draw-io/SKILL.md:3: Append a boundary to the description: 'Not for Mermaid, Excalidraw, Graphviz/DOT, or generic image editing.'
- [low] D7 skills/draw-io/scripts/find_aws_icon.py:57: Handle -h/--help explicitly (print usage, exit 0); a '--help' query currently falls through to 'No icons found'. Add the same to convert-drawio-to-png.sh
- [medium] D8 skills/draw-io/SKILL.md:35: State prerequisites (mise, the repo's convert-drawio-to-png pre-commit hook) and give the direct script invocation as the fallback when they are absent
- [low] D8 skills/draw-io/SKILL.md:41: Use the spec's relative convention 'bash scripts/convert-drawio-to-png.sh' so commands work outside the Claude Code skills layout
- Reason it ships: 2 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## excalidraw: 85.2%

- [low] D1 skills/excalidraw/SKILL.md:24: Keep one precise ID invariant and one validation check, and consolidate repeated preservation instructions while retaining the explanations of binding and image-loss hazards.
- [low] D4 skills/excalidraw/SKILL.md:3: Create, inspect, modify, and compare editable Excalidraw diagrams. Use when the user supplies .excalidraw, .excalidraw.json, or source-embedded .excalidraw.png files, asks to change diagram labels or connections, or requests Excalidraw flowcharts or architecture sketches. Keep scene JSON out of the main conversation context. Not for Mermaid, draw.io, PlantUML, Graphviz, ordinary PNG editing, or text-only architecture explanations.
- [medium] D6 skills/excalidraw/SKILL.md:8: Default to bounded structured extraction for small read-only lookups without exposing scene JSON. Require isolation for large scenes and substantial edits, and reserve status announcements for cases where delegation materially affects execution.
- [medium] D7 skills/excalidraw/evals/evals.json:7: Supply real scene fixtures and require created or edited artifacts. Assert parseability, editor acceptance, preserved unrelated elements, unique IDs, reciprocal bindings, and the requested label or connection changes.
- [medium] D7 skills/excalidraw/evals/trigger-queries.json:31: Give these positives explicit Excalidraw file paths or prior-context cues. Add format-unspecified diagram requests as boundary cases rather than assuming every flowchart uses Excalidraw.
- [medium] D8 skills/excalidraw/SKILL.md:12: Document a supported PNG round-trip tool and exact validation steps, or explicitly request a plain .excalidraw export before editing when that capability is unavailable.
- [medium] D8 skills/excalidraw/SKILL.md:28: Provide a known-good minimal scene template or a pinned creation tool, document required fields, and add an editor-open or render validation step with a repair-and-recheck loop.
- [low] D1 skills/excalidraw/SKILL.md:8: State the delegation rule once and cut the repeated restatements within the same paragraph; the rule is expert, the triple repetition is token waste.
- [low] D2 skills/excalidraw/SKILL.md:10: Add a short entry-point decision above the procedure (create / inspect / modify / compare) so each advertised mode routes to its own workflow instead of all modes funneling into the editing steps.
- [low] D3 skills/excalidraw/SKILL.md:12: Add a Format-gotchas entry for .excalidraw.png naming the specific loss (image editors that re-encode the PNG strip the embedded scene chunk) so the hazard lives with the other gotchas.
- [medium] D6 skills/excalidraw/SKILL.md:12: Name the default tool or exact operation for editing .excalidraw.png; vague guidance on a fragile, loss-prone operation invites corruption.
- [medium] D7 skills/excalidraw/evals/evals.json:16: Bundle a small evals/files/architecture.excalidraw.json fixture so the modify path runs against a real scene; the referenced file does not exist.
- [medium] D8 skills/excalidraw/SKILL.md:3: Add a compare workflow (delegate a pairwise label/binding diff to the worker and report differences textually) or drop 'compare' from the description; the body defines no comparison procedure.
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## feedback-mastery: 83.2%

- [medium] D1 skills/feedback-mastery/references/feedback-sbi-model.md:8: Remove the SBI primer and generic coaching material. Keep concise examples that demonstrate disputed evidence, power asymmetry, confidentiality, recognition without corrective add-ons, and other consequential distinctions.
- [high] D8 skills/feedback-mastery/references/feedback-sbi-model.md:88: Replace the asserted motive with an open question about their perspective. Audit the examples for inferred feelings presented as observations, including "made Alex visibly frustrated," and distinguish observable behavior from interpretation.
- [medium] D2 skills/feedback-mastery/SKILL.md:14: Add a compact recipient workflow: acknowledge the concern without accepting an unsupported conclusion, request a specific example and impact, reflect back what is understood, separate disputed claims, and agree on a next step only after clarification.
- [medium] D7 skills/feedback-mastery/evals/trigger-queries.json:15: Use this as a near-miss negative, or rewrite it to make a concrete feedback or expectation-setting goal explicit. Add a positive that tests the role, neutrality, and consent prerequisites for joint facilitation.
- [medium] D1 skills/feedback-mastery/references/feedback-sbi-model.md:3: Delete the model exposition and 'Why SBI Works' tutorial; keep only the worked examples and calibration notes the model would not produce on its own
- [low] D1 skills/feedback-mastery/references/difficult-conversation-scripts.md:238: Trim the phrase banks ('You always...' -> 'I've noticed a pattern...') to the few substitutions that fix non-obvious failures; the model generates the rest unprompted
- [low] D1 skills/feedback-mastery/references/expectation-alignment.md:127: Cut the RACI table and vague/explicit pairs (standard PM content) down to the trade-off framing and scope-change template this skill actually routes to
- [low] D2 skills/feedback-mastery/SKILL.md:11: Add the non-obvious ordering decisions (when to skip steps, which evidence to gather before drafting, when one example beats dated history) instead of the generic prepare-deliver-agree-follow-up arc
- [low] D3 skills/feedback-mastery/SKILL.md:26: Add 1-2 environment-specific traps with consequences (e.g., HR processes that require contemporaneous documentation, channels with retention/legal discovery)
- [low] D6 skills/feedback-mastery/SKILL.md:16: Give a concrete test for 'appropriate' (role need-to-know, policy check, ask the user when in doubt) so the confidentiality rule is decidable
- [low] D7 skills/feedback-mastery/evals/evals.json:9: Drop 'or equivalent' and require situation, behavior, and impact to be separately identifiable so the assertion is verifiable
- [medium] D8 skills/feedback-mastery/SKILL.md:15: State a default check-in cadence and a one-line summary template for step 4 so follow-up is actionable without guessing
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## game-changing-features: 89.2%

- [medium] D1 skills/game-changing-features/SKILL.md:17: Define recommendation fields once and compress familiar strategy guidance into brief activation cues. Concentrate the remaining content on non-obvious opportunity diagnostics, worked trade-offs, and product-specific failure modes.
- [medium] D2 skills/game-changing-features/SKILL.md:16: Add a reusable discovery procedure: identify the underlying job and binding constraint, distinguish symptom fixes from removing a workflow step or unlocking access, articulate the value mechanism, and formulate a falsifiable opportunity hypothesis before ranking it.
- [low] D3 skills/game-changing-features/SKILL.md:25: Add a reasoned gotcha that feature flags, entitlements, incomplete rollout, or unreleased code can separate implementation from user availability. Require release or exposure evidence before treating a capability as part of the current customer baseline.
- [medium] D7 skills/game-changing-features/evals/evals.json:9: Add an evidence-backed fixture containing product facts, an existing or unreleased feature, and conflicting feedback. Assert correct citations, explicit treatment of unknowns, no falsely novel recommendation, and creation of a new session without overwriting an existing report.
- [low] D2 skills/game-changing-features/SKILL.md:32: Define the tiering condition once (step 3 already gates it on evidence and user context) and reference that single condition instead of restating a slightly different one.
- [medium] D3 skills/game-changing-features/SKILL.md:15: Add a Gotchas list for evidence-source landmines, e.g. roadmap docs often list shipped or abandoned items as planned (check git history before citing them) and signup counts overstate reach versus active use.
- [medium] D8 skills/game-changing-features/SKILL.md:15: Add a pre-save validation step: re-check that every cited location resolves (file path, issue number, telemetry query) before writing session-N.md.
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## gemini: 88.8%

- [medium] D1 skills/gemini/SKILL.md:21: Consolidate directory-access guidance into one authoritative rule and shorten familiar execution/reporting advice. Preserve the non-interactive approval trap, owned-process cleanup, and source-verification requirements.
- [medium] D8 skills/gemini/SKILL.md:36: Pass the supplied plan text directly, copy it into an authorized scoped workspace, or explicitly include its containing directory after checking the expanded access boundary. Correct both plan-review examples.
- [medium] D6 skills/gemini/SKILL.md:28: Use an explicit escalation bound such as timeout --signal=TERM --kill-after=10s 300, and document owned-process-group handling for background execution.
- [medium] D7 skills/gemini/evals/evals.json:7: Make proposal-only intent explicit in proposal tests. Add fixtures for successful and failed CLI responses, timeout handling, and unsupported findings, with assertions distinguishing verified results from incomplete or rejected analysis.
- [low] D7 skills/gemini/evals/trigger-queries.json:3: Replace some explicit-name positives with realistic second-opinion and big-context requests that do not name Gemini, including a contextual multi-directory request.
- [low] D1 skills/gemini/SKILL.md:12: Replace the generic exclusion with concrete items (.env, key/token files, credentials dirs) and a quick grep the agent runs before sending context
- [low] D1 skills/gemini/SKILL.md:20: State the --include-directories rule once (here) and cross-reference from step 1 instead of restating it in both workflow steps
- [low] D2 skills/gemini/SKILL.md:17: Merge the overlapping steps 4 and 5 (substantiate claims / report verified findings) into one verify-then-report step with an explicit go/no-go gate
- [low] D3 skills/gemini/SKILL.md:10: Extract a Gotchas list of CLI-specific traps with reasons (approval-mode default hang, pkill blast radius, partial output mistaken for results) instead of burying them in prose bullets
- [low] D6 skills/gemini/SKILL.md:14: State the default bound (timeout 300 as in the command shape) and when to raise it, so the timeout is a default rather than a per-run guess
- [medium] D7 skills/gemini/evals/evals.json:3: Vary the eval set: two prompts share near-identical yolo phrasing and all three are command-proposal tasks; add one eval that tests claim verification (workflow step 4) and one casual phrasing
- [medium] D8 skills/gemini/SKILL.md:28: Enumerate the valid approval-mode values (default, plan, auto_edit, yolo) with one-line meaning and a default, so the placeholder is fillable without guessing
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## humanizer: 91.2%

- [medium] D1 skills/humanizer/SKILL.md:35: Condense familiar cliché, filler, rhythm, and mechanics inventories. Retain the contextual exemptions, exact-match protections, author-register preservation, and distinction between intended and measured benefits, supported by a few fact-preserving examples.
- [high] D8 skills/humanizer/references/pattern-catalog.md:159: Rewrite the catalog's before/after pairs so every factual claim in an after-text is supported by its before-text. Delete empty conclusions rather than inventing a replacement event, and preserve stated preferences without inventing research provenance. Audit the remaining examples with the same claim-by-claim comparison.
- [low] D1 skills/humanizer/references/pattern-catalog.md:7: Compress the mechanical-cue entries to a one-line checklist and keep full before/after blocks only for entries that encode judgment (sycophancy, knowledge-cutoff residue, generic positive conclusions).
- [low] D2 skills/humanizer/SKILL.md:11: Add the priority order: evidence risks first (vague attribution, unsupported claims), then inflation, then structure, then mechanics.
- [low] D3 skills/humanizer/SKILL.md:46: Name the concrete failure: exact-match consumers (grep, tests, API contracts, search) match the literal string, so even case or quote-style changes break them.
- [low] D6 skills/humanizer/SKILL.md:11: Add the unspecified-depth default: "When depth is unspecified, default to the minimal consequential edit and state that scope in the change note."
- [low] D8 skills/humanizer/references/pattern-catalog.md:7: Renumber the catalog from 1, or drop the numbers, so change notes and cross-references stay unambiguous.
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## jira: 89.6%

- [medium] D1 skills/jira/references/mcp.md:154: Trim elementary JQL explanations and duplicate setup guidance. Keep backend-specific schemas, extension limitations, required-field discovery, account-ID handling, and transition/link pitfalls.
- [high] D8 skills/jira/references/commands.md:231: Use the backend's actual epic-association or parent-field operation, checking the installed CLI interface and project metadata. Reserve issue-link commands for discovered configured link types and distinguish links from hierarchy.
- [medium] D8 skills/jira/SKILL.md:36: Document supported non-interactive commands or authorized REST requests for transition and create-field discovery. If the selected CLI cannot provide that information, explicitly route to an authorized MCP/REST backend or report the blocker instead of guessing or opening a prompt.
- [medium] D7 skills/jira/evals/evals.json:7: Add an approved follow-up case with backend response fixtures and assertions for required-field discovery, the exact approved mutation, and read-back verification. Include a batch partial-failure case asserting that subsequent mutations stop.
- [medium] D1 skills/jira/references/mcp.md:149: Cut the standard JQL syntax tables (operators, functions, relative dates) the model already knows; keep only the non-obvious parts (ScriptRunner limits, 'Epic Link' quoting, link-creation gap)
- [low] D2 skills/jira/SKILL.md:34: Merge the checklist into the operation paths as one ordered procedure and say why each gate exists (one-way transitions, opaque --no-input failures) instead of repeating fetch-approve-apply
- [low] D3 skills/jira/SKILL.md:34: Extract a Gotchas list naming each trap and its consequence (no general undo, display names not valid assignee IDs, transition IDs differ per project) in one place
- [low] D6 skills/jira/SKILL.md:32: Give the rationale for the batch cap (reviewability of the change list, blast radius on partial failure) or make it a default the user can raise
- [low] D8 skills/jira/SKILL.md:14: Add a tie-break rule for when both backends exist and a capability-based choice (e.g., issue linking needs MCP/REST since the CLI table omits it), so backend selection is deterministic
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## lesson-learned: 88.4%

- [medium] D1 skills/lesson-learned/SKILL.md:51: Keep each evidence rule once, at the decision where it matters. Replace generic anti-pattern definitions and refactoring prescriptions with concise diff-specific evidence requirements and counterexamples not already covered by se-principles.md.
- [medium] D7 skills/lesson-learned/evals/evals.json:9: Add before/after code or diff fixtures and assert a concrete behavioral consequence with citations. Include an extraction that increases coupling, a mechanical multi-file rename, and partial-merge comparison evidence; allow the correct result to reject an improvement claim or decline a principle label.
- [medium] D8 skills/lesson-learned/SKILL.md:21: Inspect git status before declaring evidence absent. Include relevant untracked files as new-file additions, respecting ignore rules and scope, or explicitly ask whether they should be included.
- [medium] D1 skills/lesson-learned/references/anti-patterns.md:5: Cut the textbook definitions (God Object, Feature Envy, Magic Numbers, Long Method) the model already knows; keep only each pattern's diff-signal and false-positive mapping, which is the part the model lacks
- [low] D2 skills/lesson-learned/SKILL.md:35: Keep this rule in one place: cite se-principles.md's change-amplification row from the body instead of restating it, freeing body lines for scoping judgment the reference lacks
- [low] D3 skills/lesson-learned/SKILL.md:22: Extend the evidence-scope gotchas with the other non-obvious git traps: shallow clones have no merge-base for three-dot diffs, and `git show` on a merge commit shows only the squashed conflict resolution
- [low] D6 skills/lesson-learned/SKILL.md:39: Allow a one-paragraph conversational answer when the user asks a quick reflective question, reserving the four-field template for requested artifacts or written reports
- [medium] D7 skills/lesson-learned/evals/evals.json:5: Add fixture diffs or a small fixture repo under evals/files/ so assertions about file citations, counterfactuals and no-fabrication can be graded against real output instead of hypothetical descriptions
- [low] D8 skills/lesson-learned/SKILL.md:17: Add the fallback branch: with no remotes, compare against main/master if it exists, otherwise fall back to the last 5 commits, stating the choice instead of only asking
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## marp-slide: 89.2%

- [medium] D1 skills/marp-slide/references/best-practices.md:9: Trim the generic presentation tutorial. Retain the bundled-style decisions, Marpit-specific layout behavior, export limitations, and concrete rendering failures that the agent would otherwise miss.
- [medium] D2 skills/marp-slide/SKILL.md:14: Branch the workflow into new-deck creation and existing-deck redesign. For redesign, inspect the current deck, identify what must be preserved, diagnose its rendered problems, and apply only the necessary template or CSS changes.
- [medium] D6 skills/marp-slide/references/best-practices.md:29: Replace the character limit with a rendered-fit principle: preserve complete claims, avoid distracting wrapping, and split content when the chosen font and layout become difficult to read.
- [medium] D7 skills/marp-slide/evals/evals.json:20: Add an existing-deck fixture and a multi-variant gradient/image case. Assert preserved requested content, resolved assets, readable contrast, absence of overflow, and truthful reporting when rendering is unavailable.
- [high] D8 skills/marp-slide/assets/template-gradient.md:38: Darken the bright gradient stops or place text on a sufficiently opaque dark surface. Apply the correction to both gradient assets and verify every variant, not only the title slide.
- [high] D8 skills/marp-slide/references/advanced-features.md:336: Update the artifact upload to a supported version such as actions/upload-artifact@v4, update the checkout action as appropriate, and verify that the example successfully uploads the generated PDF.
- [low] D1 skills/marp-slide/references/marp-syntax.md:1: Trim the reference to non-obvious semantics (underscore per-slide scope, size directive, class pitfalls) and cut the directives table and basic examples the model already knows.
- [low] D2 skills/marp-slide/SKILL.md:13: Keep only the unspecified default inline and defer ambiguous cases to references/theme-selection.md with one named default when dark is requested (e.g., tech) and the other as alternate.
- [medium] D3 skills/marp-slide/SKILL.md:35: Add the missing expert gotcha: Marp CLI PDF/PPTX/image export requires Chrome/Chromium (or the official Docker image); in headless CI pass a container or --browser path, so state it in Marp gotchas.
- [low] D6 skills/marp-slide/SKILL.md:15: Give a concrete fallback heuristic for when rendering is unavailable (e.g., approximate word or bullet count per slide) so density is decidable without a render.
- [low] D8 skills/marp-slide/SKILL.md:17: Define the no-CLI path: lint frontmatter and _class directives against references/marp-syntax.md and verify image paths resolve before delivering Markdown.
- Reason it ships: 2 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## meme-factory: 89.6%

- [medium] D1 skills/meme-factory/SKILL.md:17: Compress the generic joke-writing steps and familiar template explanations into a short selector. Preserve the useful actual template IDs, two-caption capacity constraint, encoding rules, privacy boundary, and uncertain-outcome handling.
- [medium] D5 skills/meme-factory/SKILL.md:12: Reference the helper as `python3 scripts/meme_generator.py generate <template> '<top>' '<bottom>'`, relative to the skill root.
- [medium] D8 skills/meme-factory/scripts/meme_generator.py:160: Resolve negation and uncertainty before positive or negative outcome keywords, use token-aware matching, and fall back to a neutral template when the outcome is ambiguous. Add regression cases for negated success, negated failure, and substring collisions.
- [low] D1 skills/meme-factory/SKILL.md:18: Compress steps 1-2 into one line (name the contrast; draft the payoff first, then the setup) and drop the role taxonomy the model can improvise.
- [low] D2 skills/meme-factory/SKILL.md:44: Add the retry loop: if captions crop or wrap, shorten them and regenerate once, then present or report the template's limit.
- [low] D3 skills/meme-factory/SKILL.md:10: Note that an omitted caption must be the literal `_` placeholder in a hand-built URL (the helper substitutes it automatically); an empty segment breaks the URL.
- [medium] D5 skills/meme-factory/references/examples.md:1: Gate the file from SKILL.md (read references/examples.md only when the user asks for integration or CLI examples) or delete it, trim the Slack/Discord/PR-comment pseudo-code the model does not need, and remove the scripts/__pycache__ build artifacts.
- [low] D6 skills/meme-factory/SKILL.md:10: Name the parameters (`width`, `height`, `layout`, `font`) or point to the helper's --width/--height/--layout flags so sizing is not guessed.
- [low] D7 skills/meme-factory/evals/trigger-queries.json:39: Rebalance to 8-10 positives (drop or relabel the weakest positive) and add a near-miss negative such as a caption request for a photo with no URL or template.
- [low] D8 skills/meme-factory/SKILL.md:12: State the fallback when Python or the repo-relative path is unavailable: build the URL directly from the Quick reference pattern using the encoding table.
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## mermaid-diagrams: 80.8%

- [medium] D4 skills/mermaid-diagrams/SKILL.md:3: Create, edit, and repair Mermaid diagrams in Markdown or .mmd files. Use when users ask to diagram, visualize, model, map out, or show software interactions, schemas, architecture, lifecycles, processes, schedules, proportions, or Git history, even without naming Mermaid. Classify the question before choosing sequenceDiagram, classDiagram, erDiagram, C4, stateDiagram-v2, flowchart, architecture-beta, gantt, pie, or gitGraph. Not for prose-only explanations, PlantUML or draw.io editing, matplotlib data charts, or interactive diagram-canvas components.
- [high] D1 skills/mermaid-diagrams/SKILL.md:44: Remove the basic syntax introduction, four inline tutorials, and generic reasons to diagram. Keep the classification gate, host constraints, subgraph-direction trap, and renderer-specific failures; leave syntax examples in the already-gated type references.
- [medium] D2 skills/mermaid-diagrams/SKILL.md:29: Add a brief grounding checkpoint before drawing: identify the audience and abstraction level, extract entities and relationships from supplied code/schema or facts, and distinguish confirmed relationships from assumptions before choosing notation.
- [medium] D6 skills/mermaid-diagrams/SKILL.md:176: Make diagrams conditional on the user's requested deliverable or a clear explanatory benefit. Explicitly respect prose-only requests and avoid creating diagrams merely because a task involves architecture, schemas, or refactoring.
- [medium] D7 skills/mermaid-diagrams/evals/evals.json:9: Add realistic repair and renderer-boundary cases, including special-character labels, GitHub architecture icons, and a larger C4 example. Assert successful parsing/rendering and correct entity relationships, not only declaration keywords.
- [high] D8 skills/mermaid-diagrams/references/architecture-diagrams.md:64: Use built-in icons throughout default examples. Put custom icons only in a separately gated example that includes the required host registration and target-renderer verification.
- [high] D8 skills/mermaid-diagrams/references/c4-diagrams.md:279: Give every C4 element a unique identifier, such as person_user and svc_user, and update each Rel call to target the intended element. Validate identifier uniqueness across the complete example.
- [low] D1 skills/mermaid-diagrams/SKILL.md:172: Delete the section; 'Always diagram when starting new projects' and 'Align stakeholders' are generic advocacy the model already knows and they dilute the expert classification and pitfall content.
- [low] D2 skills/mermaid-diagrams/SKILL.md:143: Replace Best Practices items 2-5 (fit the column, connect at the boundary, shapes are roles, color by role) with one-line pointers to the matching authoring-rules.md sections instead of duplicating them.
- [low] D3 skills/mermaid-diagrams/SKILL.md:170: State the why explicitly (color-vision deficiency affects ~8% of men and docs often print or render in grayscale), so the rule is followed for the right reason.
- [low] D4 skills/mermaid-diagrams/SKILL.md:3: Append a boundary against near-miss neighbours the trigger queries already test as negatives, e.g., 'Mermaid text syntax only; not for PlantUML, draw.io, matplotlib charts, or image editors.'
- [low] D6 skills/mermaid-diagrams/SKILL.md:35: The shape/palette/proportion rules in authoring-rules.md are flowchart-centric; add per-type calibration notes for State, Git, Gantt, and Pie or explicitly exempt those types from the palette and shape rules.
- [low] D7 skills/mermaid-diagrams/evals/evals.json:6: Prompts are terse commands without realistic user context (file paths, backstory, casual phrasing) and no broken-syntax repair case; add a casual context-rich prompt and a malformed-source repair eval with verifiable assertions.
- [medium] D8 skills/mermaid-diagrams/SKILL.md:127: The load table has rows only for Class, Sequence, Flowchart, ERD, C4, architecture, and theming; State, Git, Gantt, and Pie are promised by the description and classification table but have no routing target. Add rows (e.g., route them to references/advanced-features.md) or inline minimal syntax.
- Reason it ships: 3 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## mui: 83.2%

- [medium] D1 skills/mui/resources/styling-guide.md:25: Remove beginner explanations and repeated basic theme configurations from the resources. Retain focused v7 decisions about slot targets, selector specificity, sx transformations, palette augmentation, public exports, and migration compatibility.
- [medium] D5 skills/mui/skill-rules-fragment.json:6: Remove the fragment if it is not consumed, or document the actual integration and route to it only when configuring that integration. Do not load activation configuration for ordinary MUI implementation tasks.
- [medium] D7 skills/mui/evals/evals.json:18: Add concrete migration inputs and assertions for controlled open/close behavior, the rendered dialog's accessible name, Escape/backdrop handling, and public-versus-private import paths. Include typechecked Grid and palette-augmentation consumers.
- [medium] D7 skills/mui/evals/trigger-queries.json:27: Make these bare requests near-miss negatives, and add positive versions with realistic MUI imports, package-version context, or existing MUI file references.
- [high] D8 skills/mui/resources/theme-customization.md:555: Build the nested theme from shared source ThemeOptions rather than a resolved theme, explicitly derive the dark palette or use the project's supported color-scheme mechanism, and verify computed background/text colors in the nested region.
- [high] D8 skills/mui/resources/theme-customization.md:101: Add an aria-label describing the target action, such as switching to dark or light mode, and assert the toggle's accessible name and state change with a role-based test.
- [medium] D1 skills/mui/resources/theme-customization.md:3: Cut the reference to v7-specific decisions: cssVariables contract, palette augmentation boundaries (Palette plus *PropsColorOverrides), enableCssLayer, and migration failure modes; delete the default-palette and provider tutorials the model already knows.
- [low] D2 skills/mui/SKILL.md:23: Add the no-script fallback: if the repo defines no typecheck/build script, run npx tsc --noEmit on the touched files or state the gap in the answer.
- [medium] D3 skills/mui/SKILL.md:10: Add a Gotchas section with each trap's concrete failure: legacy Grid props are silently ignored in v7 (no error), the wrong slotProps target typechecks but styles the wrong element, numeric borderRadius is multiplied by theme.shape.borderRadius.
- [low] D5 skills/mui/skill-rules-fragment.json:7: Delete the fragment or document its actual consumer and integration scenario in SKILL.md; the repository's documented skill layout (docs/conventions/skill-layout.md) does not include it.
- [low] D6 skills/mui/resources/styling-guide.md:3: Lead the reference with the SKILL.md default rule (sx for one-off, styled for reusable, theme overrides for system-wide) so the choice at the point of use has a default, not a menu.
- [medium] D7 skills/mui/evals/evals.json:26: Rewrite as a realistic migration request with a fixture component in evals/files/; strengthen assertions: accepts public exports such as @mui/material/Grid, uses the size prop correctly, and typechecks.
- [low] D8 skills/mui/SKILL.md:21: Give the concrete check: read node_modules/@mui/material/<Component>/<Component>.d.ts for the installed version, or the matching section of the v7 upgrade guide.
- Reason it ships: 2 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## naming-analyzer: 84.4%

- [medium] D1 skills/naming-analyzer/SKILL.md:19: Remove the elementary constant-naming example and consolidate repeated compatibility warnings. Spend the recovered space on concrete cases where units, lifecycle, nullability, or competing caller meanings change the correct naming decision.
- [medium] D2 skills/naming-analyzer/SKILL.md:27: Add an evidence-resolution procedure: trace definitions, transformations, callers, and contract boundaries; withhold a definitive rename when meanings conflict; distinguish a safe local alias from a contract change; tie confidence to the evidence actually established.
- [medium] D3 skills/naming-analyzer/SKILL.md:31: Add reasoned warnings for string-key access, reflection, dependency-injection names, framework-reserved file names, and generated identifiers: these consumers can evade ordinary static-reference searches, so an apparently private symbol may still be a runtime contract.
- [medium] D7 skills/naming-analyzer/evals/evals.json:16: Supply implementations and call sites that establish meaning, or make focused clarification questions and explicitly tentative candidates acceptable outcomes. Add a verifiable case where retaining a name is correct because its external contract is established.
- [low] D7 skills/naming-analyzer/evals/trigger-queries.json:3: Replace several generic positives and easy negatives with realistic context-rich prompts, including misleading unit/time-basis names and requests that overlap naming review but actually authorize an automatic migration.
- [medium] D1 skills/naming-analyzer/SKILL.md:31: Cut widely-known review basics (compatibility checks before public renames are standard agent behavior); keep and expand only the behavior-calibrating rules the model does not apply by default (project convention precedence, boolean polarity over prefix, ask-don't-infer)
- [low] D2 skills/naming-analyzer/SKILL.md:23: Add one worked example walking a rename from evidence to compatibility verdict so the risk ordering is trained, not just listed
- [low] D3 skills/naming-analyzer/SKILL.md:29: Add environment-specific gotchas: identifiers referenced by ORM mappings, generated code, i18n message keys, or reflection that rename tooling silently misses
- [low] D6 skills/naming-analyzer/SKILL.md:17: State the fallback when no project convention exists (default to the language's dominant convention and say so in the report)
- [medium] D7 skills/naming-analyzer/evals/evals.json:6: Add a repo-level eval with a small file fixture containing a serialized-field identifier to test the compatibility rule, and vary prompt formality and context
- [low] D8 skills/naming-analyzer/SKILL.md:41: Add one filled example row (including a no-change row) so the confidence and compatibility values are unambiguous
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## openapi-to-typescript: 86.8%

- [medium] D1 skills/openapi-to-typescript/SKILL.md:21: Consolidate repeated warnings and elementary mappings. Preserve the 3.0-specific nullable rules, named recursive references, media/status distinctions, and refusal policies; add concrete context-sensitive transformations rather than repeating basic TypeScript mappings.
- [medium] D3 skills/openapi-to-typescript/SKILL.md:36: Add explicit warnings that OpenAPI 3.0 Reference Object siblings are ignored, and that readOnly/writeOnly affect request/response projection and requiredness. Explain the incorrect contracts produced when these distinctions are ignored.
- [medium] D6 skills/openapi-to-typescript/SKILL.md:23: Provide a default representation for pure dictionaries and an explicit policy for mixed fixed/additional properties. Require a diagnostic rather than an incompatible index signature when exact representation is unavailable, and identify any deliberately approximate representation as such.
- [medium] D7 skills/openapi-to-typescript/evals/evals.json:7: Make the prompt, expected output, and assertions agree: define ApiError in the input or omit it, and explicitly request runtime guards when asserting their presence. Add complete operation and schema inputs for composition, parameter-location, and response-variant cases.
- [medium] D7 skills/openapi-to-typescript/evals/trigger-queries.json:23: Add realistic OpenAPI 3.0 context to ambiguous positives and pair them with closely matched standalone JSON Schema, non-TypeScript, and unsupported-version negatives.
- [medium] D8 skills/openapi-to-typescript/SKILL.md:32: Add a validation loop using the repository's TypeScript check, plus guard cases covering present malformed optionals, nullable branches, array elements, and compositions. Fix failures before reporting completion; explicitly report when validation cannot run.
- [low] D8 skills/openapi-to-typescript/SKILL.md:14: Define one deterministic naming algorithm, including parameter markers and any singularization policy, and make the example match it. Include a collision example demonstrating the specified disambiguation rule.
- [low] D1 skills/openapi-to-typescript/SKILL.md:12: Drop the ask-for-file clause (default agent behavior); keep the version and paths checks, which are the non-obvious part
- [low] D2 skills/openapi-to-typescript/SKILL.md:14: Give one collision example with the exact emitted names (e.g. two GET /users/{id} operations → GetUserById and GetUserByIdQueryParams) so the suffix rule is unambiguous
- [low] D3 skills/openapi-to-typescript/SKILL.md:21: Add the missing environment gotchas: oneOf without a discriminator field, and readOnly/writeOnly asymmetry between request and response types
- [low] D6 skills/openapi-to-typescript/SKILL.md:15: For large specs, summarize planned type names before writing (or support a dry run) so a naming collision does not produce a full-file rewrite
- [low] D7 skills/openapi-to-typescript/evals/evals.json:16: Add evals for recursive $ref guards (cycle safety) and operationId collisions — both rule-heavy paths no eval covers
- [low] D8 skills/openapi-to-typescript/SKILL.md:12: State the empty-schemas branch explicitly: emit only operation types and report zero named schemas, so the agent is not left guessing
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## plugin-forge: 90.0%

- [low] D1 skills/plugin-forge/SKILL.md:12: State the scaffold precondition and generated artifacts once. Keep the execution-unavailable fallback brief and refer back to that contract rather than repeating the same behavior.
- [medium] D2 skills/plugin-forge/SKILL.md:18: Order the release procedure as component changes, synchronized version bump, manifest/path validation, local installation, reload and installed-version verification, then publication.
- [high] D6 skills/plugin-forge/references/workflows.md:106: Stage only the intended plugin and marketplace changes, inspect the diff, and use the repository's actual release branch or PR workflow. Perform commits and pushes only within the user's authorized publication scope.
- [low] D7 skills/plugin-forge/scripts/bump_version.py:57: Send diagnostics to stderr and reserve stdout for structured results, or consistently emit structured error objects. Update CLI tests to check the output-channel contract and --help behavior.
- [high] D8 skills/plugin-forge/SKILL.md:15: Replace the two execution steps with one fully specified scaffold invocation. State that successful execution already registers the marketplace entry, so later edits should update that entry rather than duplicate it.
- [high] D8 skills/plugin-forge/scripts/bump_version.py:23: Validate the entire supported version string before computing or writing anything. Require three valid nonnegative SemVer core components, explicitly handle or reject prerelease/build metadata, and test that invalid versions leave both manifests unchanged.
- [low] D1 skills/plugin-forge/references/workflows.md:59: Delete the semantic-versioning tutorial and the conventional-commit examples; the model knows both. Keep the plugin-specific rule (both manifests must match) and the testing steps.
- [low] D2 skills/plugin-forge/SKILL.md:16: This script contract is stated three times (lines 8, 12, 15, 16); state it once at the scaffold step and drop the repetitions to save body tokens.
- [low] D3 skills/plugin-forge/SKILL.md:27: Add the missing gotcha: when marketplace.json sets `pluginRoot`, relative `source` values resolve against it, so create_plugin.py's unconditional `./plugins/<name>` source can double-prefix; document the interaction or make the script respect an existing pluginRoot.
- [low] D6 skills/plugin-forge/SKILL.md:15: The script mutates a shared marketplace manifest with no preview; add a --dry-run flag or instruct the agent to show the planned manifest entry before running against a shared marketplace root.
- [low] D7 skills/plugin-forge/scripts/bump_version.py:61: Error diagnostics print to stdout although SKILL.md documents stdout as the JSON channel (the test even asserts them in r.stdout); route errors to stderr like create_plugin.py does and document exit codes in --help.
- [low] D8 skills/plugin-forge/references/workflows.md:124: Name the concrete discovery method (type `/` and autocomplete the plugin-prefixed command, or inspect the installed plugin's commands directory) so the agent is not left guessing how to verify.
- Reason it ships: 3 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## qa-test-planner: 86.4%

- [medium] D1 skills/qa-test-planner/SKILL.md:23: Condense the standard input-partition and deliverable inventories. Retain the concrete safeguards, and replace generic coverage reminders with decisions for deriving observable oracles for retries, state transitions, and irreversible operations.
- [medium] D2 skills/qa-test-planner/SKILL.md:14: Add a compact plan branch: establish requirements and risk owners, select scope from changed behavior and dependencies, derive entry/exit gates from critical coverage and unresolved risk, then reconcile the plan with available environments and execution time.
- [medium] D7 skills/qa-test-planner/SKILL.md:45: Add a documented non-interactive JSON input mode, implement --help, and emit a machine-readable result manifest separately from diagnostic output. Extend the existing smoke tests to exercise those interfaces.
- [high] D8 skills/qa-test-planner/references/bug_report_templates.md:383: Remove rare crashes from the unconditional Low examples. Classify crashes by impact and recoverability, record reproduction frequency separately, and label response-time targets as organization-specific examples rather than established policy.
- [low] D1 skills/qa-test-planner/SKILL.md:23: Boundary value analysis is textbook knowledge; compress step 2 to 'partition inputs by behavior with boundaries and failure paths' and spend the tokens on the non-obvious safeguards
- [low] D2 skills/qa-test-planner/SKILL.md:15: Add a default for combined requests, e.g. 'produce the plan first, then cases that trace to its risks'
- [low] D3 skills/qa-test-planner/SKILL.md:30: Add a NEVER item such as 'Never assume deterministic clocks or timezones; freeze time or state the timezone in test data, or runs flake across machines'
- [low] D6 skills/qa-test-planner/SKILL.md:16: State a default precedence (e.g. failure impact first, then changed-code overlap) so prioritization is reproducible
- [medium] D7 skills/qa-test-planner/SKILL.md:45: Give the scripts a non-interactive mode (all fields as flags or a stdin template), add --help, and drop color codes from stdout so agents can run them directly
- [low] D8 skills/qa-test-planner/SKILL.md:26: Add 'mark unknown environment facts as Unknown; never guess them' so deliverables stay honest when the requester cannot supply the facts
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## react-dev: 85.2%

- [medium] D1 skills/react-dev/SKILL.md:14: Reduce native-prop, ReactNode, nullable-state, and tuple reminders to a brief activation checklist. Concentrate the main instructions on correlated generics, version-sensitive Action contracts, promise ownership, and server/client execution traps.
- [medium] D2 skills/react-dev/SKILL.md:16: Show the reusable derivation: capture K in a builder, tie its value and callback to T[K], package the renderer without widening that relationship, and demonstrate a valid pairing and a rejected mismatched pairing.
- [medium] D7 skills/react-dev/evals/evals.json:10: Grade accepted props, ref compatibility, and rejected invalid inputs rather than exact helper names. Add minimal TSX fixtures with positive and negative type checks, a router-mode case, and an SSR/storage edge case; include realistic file paths and failure context in several trigger queries.
- [high] D8 skills/react-dev/examples/server-components.md:161: Authenticate within each Server Action and authorize the requested userId before accessing the database. Derive the identifier from the session where appropriate, otherwise check ownership or role explicitly and return a controlled authorization failure.
- [high] D8 skills/react-dev/examples/server-components.md:464: Associate loaded state with its key and skip persistence until the current key has been read successfully. Guard both storage operations, define missing-key behavior explicitly, and verify that switching keys never writes a value belonging to another key.
- [medium] D8 skills/react-dev/references/react-19-patterns.md:438: Check response.ok, obtain the confirmed message, and update the authoritative message state or refresh its owner before the Action completes. Use unique temporary identifiers and demonstrate distinct success-commit and failure-rollback outcomes.
- [medium] D8 skills/react-dev/references/react-19-patterns.md:540: Keep the input update urgent and move filtering into a deferred or transition-driven render, with a memoized results boundary where needed. Use a worker for genuinely long synchronous computation; do not present wrapping the computation in startTransition as deferring that computation.
- [low] D1 skills/react-dev/SKILL.md:15: Delete the ref-nullability sentence; keep the React 19 useRef-initializer rule, which is the non-obvious part of that bullet
- [low] D2 skills/react-dev/SKILL.md:26: Split the router decision from the reference list and add a combined-task note (e.g. React 19 migration plus router upgrade) stating which references to load together
- [low] D3 skills/react-dev/SKILL.md:40: Add a migration gotcha such as 'React 19 removes react-dom/test-utils.act and @types/react 19 changes ref typing; pin matching type versions or CI fails confusingly'
- [low] D6 skills/react-dev/SKILL.md:18: Add 'Check the installed react version in package.json first; when unknown or mixed, assume React 18-compatible and say so'
- [medium] D7 skills/react-dev/evals/evals.json:1: Add an edge-case eval, e.g. a component that must stay React 18-compatible inside a React 19 app, asserting forwardRef is chosen over ref-as-prop
- [low] D8 skills/react-dev/SKILL.md:28: Add a fallback branch: 'If no router is installed and the app is not greenfield, keep the existing navigation and state the limitation instead of recommending an install'
- Reason it ships: 2 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## react-useeffect: 88.0%

- [medium] D1 skills/react-useeffect/SKILL.md:12: Keep the common render/event distinctions as a short activation table. Reduce duplicated basic demonstrations and devote detailed examples to partial identity resets, SSR snapshots, initialization retries, and stale asynchronous writes.
- [medium] D7 skills/react-useeffect/evals/trigger-queries.json:35: Label this standalone networking query false. Add a separate positive with realistic React context, such as an existing useEffect in SearchResults.tsx whose previous query overwrites the current results.
- [medium] D8 skills/react-useeffect/anti-patterns.md:250: Complete the example with loading and error state, guarded success/error/finally writes, and HTTP-status handling in the fetch helper. Verify obsolete failures and completions cannot overwrite the current request's state.
- [low] D8 skills/react-useeffect/anti-patterns.md:272: Close the tsx fence immediately after the App example and leave the lifetime, retry, and cache guidance as ordinary prose.
- [medium] D1 skills/react-useeffect/anti-patterns.md:6: Items 1-8 re-derive react.dev's 'You Might Not Need an Effect' examples the model already knows; compress them to one-line entries and keep the expert content (item 9's guard-lifetime analysis and alternatives.md's boundary notes)
- [low] D2 skills/react-useeffect/SKILL.md:3: The description promises RTL testing but neither the body nor the references give any RTL procedure; add a short testing step to the correctness loop (act/userEvent, assert cleanup behavior) or drop the RTL claim from the description
- [low] D3 skills/react-useeffect/SKILL.md:28: Gotchas are embedded in prose steps; extract the NEVER items (no dependency suppression, no state-to-state Effects, no asymmetric cleanup) into a scannable list under its own heading
- [low] D6 skills/react-useeffect/SKILL.md:17: State the fallback when the contract does not fit: 'otherwise use an Effect subscription with stable cleanup and identity-stable snapshots'
- [low] D7 skills/react-useeffect/evals/evals.json:1: Add an eval whose fetch rejects or whose cleanup runs twice under Strict Mode, asserting the skill's prescribed handling
- [low] D8 skills/react-useeffect/SKILL.md:16: 'scoped adjustment' is undefined until alternatives.md is loaded; link the phrase to the partial-identity-reset section or define it in one inline clause
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## reducing-entropy: 88.4%

- [medium] D1 skills/reducing-entropy/SKILL.md:29: Consolidate measurement and reporting into one contract and trim generic validation reminders. Keep the higher-value invariant-ownership comparison, consistent counting rules, complexity-displacement warning, and costly-retrofit exception.
- [low] D5 skills/reducing-entropy/adding-reference-mindsets.md:3: Move this maintenance note into repository-level contributor documentation instead of shipping a separate contributor-only file with the skill.
- [medium] D7 skills/reducing-entropy/evals/evals.json:20: Provide a concrete code fixture for measured reductions and assertions for retained behavior and counting exclusions. For evidence-unavailable reviews, assert a measurement method and explicitly pending totals rather than actual before/after measurements.
- [medium] D7 skills/reducing-entropy/evals/trigger-queries.json:3: Replace several name-matching positives with realistic requests to shrink a specified module or choose the least-code implementation without naming the skill. Add contextual near-misses that request readability or local cleanup without codebase minimization.
- [low] D1 skills/reducing-entropy/SKILL.md:12: Keep the named mindsets and the end-state rule; trim the rhetorical question, which restates the title-level intent the model already infers from the explicit request.
- [low] D2 skills/reducing-entropy/SKILL.md:28: Measure the baseline during inventory (step 1) so deletion candidates are proposed and ranked against measured sizes rather than counted after proposal.
- [low] D3 skills/reducing-entropy/SKILL.md:32: Add the why: tests and vendored/generated code are not first-party entropy, so removing them games the metric while hiding risk.
- [medium] D4 skills/reducing-entropy/SKILL.md:3: Guide deletion-biased codebase minimization: inventory deletable or mergeable code, guard behavior, public APIs, and data-retention obligations, and measure first-party line counts before and after. Use only when the user explicitly asks to reduce entropy, delete code, shrink or simplify the codebase, or choose the smallest implementation. Not for general refactoring, readability, or performance reviews.
- [low] D5 skills/reducing-entropy/adding-reference-mindsets.md:1: Move this contributor-process note to the repository's contributor documentation outside the shipped skill package; nothing in SKILL.md loads it.
- [medium] D7 skills/reducing-entropy/evals/trigger-queries.json:8: Replace several should-trigger queries with natural explicit requests that do not name the skill (e.g. 'this codebase is way too big — delete whatever we don't need'); all ten positives currently contain the literal skill name or 'entropy', so the explicitness axis is untested.
- [low] D7 skills/reducing-entropy/evals/evals.json:6: Bundle the module under evals/files/ so the measurement and merge-invariant steps run against real code instead of a described example.
- [low] D8 skills/reducing-entropy/SKILL.md:16: State what to do when several lenses apply at once (load all applicable references, with PAGNI gating deletion decisions) so the routing cannot stall on overlapping triggers.
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## requirements-clarity: 88.0%

- [medium] D1 skills/requirements-clarity/SKILL.md:12: Compress routine requirements-gathering and PRD-inventory guidance. Retain the repository-facts/product-decisions distinction and advisory-score override; add worked decisions for conflicting requirements or stakeholder priorities instead of repeating familiar principles.
- [medium] D7 skills/requirements-clarity/evals/evals.json:22: Add end-to-end cases for a clarified feature and an explicitly approved low-score draft. Assert the PRD path/version, preserved decisions, testable acceptance criteria, labelled assumptions and open questions, and actual artifact creation; include a chat-only variant.
- [medium] D7 skills/requirements-clarity/evals/trigger-queries.json:3: Replace several stubs with realistic requests containing repository paths, existing behavior, stakeholder context, and incomplete product choices. Pair an ambiguous request naming a file with a fully specified change in that same file to test that paths alone do not determine routing.
- [medium] D8 skills/requirements-clarity/SKILL.md:16: Before saving, check each acceptance criterion against a supported decision, detect contradictions between rounds, and verify that unresolved consequential choices remain visibly labelled. Revise or return to focused clarification when that check fails.
- [low] D1 skills/requirements-clarity/SKILL.md:12: Drop the YAGNI/KISS acronym labels and keep only the non-obvious rule that follows them ('do not infer business value from a technical proposal'); naming the frameworks is activation content the model already applies
- [low] D2 skills/requirements-clarity/SKILL.md:38: Replace the Output section with a pointer to the already-loaded template plus the mandatory footer ('Generate from references/prd-template.md; always fill version, date, clarification rounds, advisory score') and delete the duplicated section list
- [medium] D3 skills/requirements-clarity/SKILL.md:31: Add environment-specific gotchas from real runs, e.g. 'If answers conflict between rounds, surface the conflict and re-confirm the earlier decision instead of silently keeping the newest' and what to do when docs/prds/ cannot be created
- [medium] D7 skills/requirements-clarity/evals/trigger-queries.json:11: Rewrite 4-6 queries as full realistic user messages with context and casual phrasing, e.g. 'leadership wants better onboarding by Q3 and eng keeps asking me what that means - help me pin down scope', per the realism guidance (paths, personal context, varied formality)
- [medium] D8 skills/requirements-clarity/SKILL.md:27: Add per-category score anchors (e.g. 'Functional 15/30 = behavior named but boundaries and failure states unspecified') or require each clarification response to list per-category earned and lost points so two agents cannot score the same brief 55 and 75 while both following the skill
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## session-handoff: 86.4%

- [medium] D1 skills/session-handoff/SKILL.md:153: Remove the repeated resource catalogue and compress generic open/fill/report instructions. Keep one CREATE route, one RESUME route, exact script interfaces, the irreconstructable-context prioritization, bounded lineage, and implementation-specific safeguards.
- [high] D6 skills/session-handoff/scripts/create_handoff.py:334: Create handoff files exclusively and refuse collisions by default. Generate a unique suffix or require an explicit overwrite option before replacement, and add a deterministic same-timestamp collision test.
- [medium] D7 skills/session-handoff/scripts/validate_handoff.py:303: Use argparse consistently across the helpers, document exit codes and examples through --help, and add a JSON output mode with diagnostics on stderr. Extend the existing tests to validate help behavior and parse the JSON result.
- [medium] D8 skills/session-handoff/scripts/check_staleness.py:35: Preserve status-record whitespace and parse porcelain output without stripping its prefix, preferably using NUL-delimited status records with explicit rename handling. Add a test asserting the exact changed pathname when the first record is an unstaged tracked modification.
- [medium] D8 skills/session-handoff/scripts/validate_handoff.py:126: Validate root-relative filenames as well as paths containing slashes, filtering URLs separately. Apply the same correction to staleness reference extraction and add missing-root-file cases to both script test suites.
- [low] D1 skills/session-handoff/SKILL.md:42: The four-section list restates the structure references/handoff-template.md already defines; keep only the 'three required sections' rule and point to the template
- [low] D2 skills/session-handoff/SKILL.md:137: Step 6 edits or chains handoffs without re-validation; add 're-run validate_handoff.py after editing or chaining a handoff before finalizing'
- [medium] D3 skills/session-handoff/SKILL.md:64: Gotchas exist only on the CREATE side; add resume-side failure modes with reasons, e.g. 'FRESH only compares files and commits; after a revert or rebase, re-verify assumptions by hand'
- [low] D5 skills/session-handoff/scripts/__pycache__:-: Delete scripts/__pycache__/ and add it to .gitignore
- [low] D5 skills/session-handoff/SKILL.md:28: Use spec-relative paths (scripts/create_handoff.py) and state once that paths are relative to the skill directory, instead of placeholder prose in every command
- [low] D6 skills/session-handoff/SKILL.md:40: Give a rule of thumb, e.g. one paragraph per section for under a day of remaining work; full evidence and reproduction commands for multi-day work
- [low] D7 skills/session-handoff/scripts/validate_handoff.py:302: Usage prints only on missing arguments with no --help flag and free-form output; switch to argparse with --help and add a --json output mode so agents can consume results programmatically
- [low] D8 skills/session-handoff/SKILL.md:49: Validation is a single pass before Step 4 confirms; add 'fix reported issues and re-run until the verdict is READY' between Steps 3 and 4
- Reason it ships: 1 high finding(s) remain after the fix rounds and the single high-only wave; each judging round surfaced new highs instead of converging, so they ship documented (score above the 80 gate).

## ship-learn-next: 87.6%

- [medium] D1 skills/ship-learn-next/SKILL.md:15: Compress routine intake and repeated intent/provenance guidance while retaining safeguards. Spend the saved space on a compact worked example distinguishing artifact evidence, noisy outcomes, and the resulting next-rep decision.
- [medium] D6 skills/ship-learn-next/SKILL.md:34: Require one-variable changes when the plan makes causal comparisons. For creative or integrative practice, default to one declared learning target while permitting coordinated changes when the user’s goal or time budget requires them.
- [medium] D7 skills/ship-learn-next/evals/evals.json:7: Make the missing-source case assert a transcript/content request or an explicitly provisional plan, no fabricated source lessons, and accurate write-status reporting. Add cases for noisy outcomes, inconsistent execution, and chat-only delivery.
- [medium] D7 skills/ship-learn-next/evals/trigger-queries.json:3: Add varied casual and detailed prompts with source paths, deadlines, available time, and existing rep results. Include near-misses that request a lesson summary or project plan despite sharing implementation vocabulary.
- [medium] D8 skills/ship-learn-next/SKILL.md:30: Time-box retries within the user's budget. After a failed repeat, route to shrinking the rep, removing a blocker, or renegotiating the target rather than repeating unchanged indefinitely.
- [low] D1 skills/ship-learn-next/SKILL.md:21: Compress derivable coaching lines like this and "Be direct, question-driven"; spend the tokens on the non-obvious rules (controllable criteria, one variable per rep, the evidence decision rule).
- [low] D2 skills/ship-learn-next/SKILL.md:15: Add a prioritization rule for competing lessons: when several lessons could be Rep 1, pick the one with the smallest shippable test in the user's available time.
- [low] D3 skills/ship-learn-next/SKILL.md:51: Add a gotcha: a source's motivational claims are not lessons; extracting them produces a rep that tests nothing.
- [medium] D7 skills/ship-learn-next/evals/trigger-queries.json:2: Expand queries into full realistic messages with context, phrasing variety, and occasional typos; telegraphic phrases under-test the description.
- [medium] D8 skills/ship-learn-next/SKILL.md:45: Add a five-line example Rep 1 (deliverable, controllable criterion, steps, reflection questions) so agents copy the plan shape instead of guessing it.
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

## writing-clearly-and-concisely: 86.8%

- [medium] D1 skills/writing-clearly-and-concisely/SKILL.md:13: Consolidate ordinary preserve-meaning and remove-repetition reminders into one short checkpoint. Keep the technical semantic exceptions prominent and demonstrate the decisions with a few difficult before/after cases rather than repeating the general policy.
- [low] D1 skills/writing-clearly-and-concisely/SKILL.md:30: Remove the generic delegation instruction. Retain only the writing-specific fallback: preserve a compact invariant list and consult the relevant reference section.
- [medium] D2 skills/writing-clearly-and-concisely/SKILL.md:12: Add a short original-draft branch: identify the reader and intended action, establish supported facts and required terminology, organize information around that action, draft, then apply the existing semantic and concision checks.
- [medium] D6 skills/writing-clearly-and-concisely/SKILL.md:16: Check meaning and length internally by default and return only the requested prose. Permit unchanged or longer wording when fidelity or clarity requires it, explain that exception briefly, and show counts or comparison excerpts only when requested or materially useful.
- [medium] D7 skills/writing-clearly-and-concisely/evals/evals.json:26: Keep technical diagnosis as a trigger negative and add in-scope output cases covering must/should/may, an unless condition, embedded quotations or identifiers, an unknown actor, and already-minimal text. Assert preservation of each semantic invariant rather than requiring particular wording.
- [low] D1 skills/writing-clearly-and-concisely/SKILL.md:33: Tautological harness restatement; replace with the actual constraint: 'when context is tight, read only the relevant reference section and edit locally'
- [low] D2 skills/writing-clearly-and-concisely/SKILL.md:13: No default when the user cannot supply evidence mid-edit; default to preserving scope and flag the missing evidence at the end rather than blocking
- [low] D3 skills/writing-clearly-and-concisely/SKILL.md:28: Safeguards omit dialect/house-spelling consistency; add 'Never switch dialect (en-US/en-GB) or house spelling while tightening; keep the source's convention'
- [low] D6 skills/writing-clearly-and-concisely/SKILL.md:16: The count check is defined only for sentence-sized rewrites; extend it to documents with total or per-section word counts
- [medium] D7 skills/writing-clearly-and-concisely/evals/evals.json:1: Add an eval with a multi-paragraph README fixture and a brand-voice prompt asserting suggestions are flagged, not silently rewritten
- [low] D8 skills/writing-clearly-and-concisely/SKILL.md:16: The output format is described but never shown; add a three-line worked example (original, rewrite, check line) so the format is unambiguous
- Reason it ships: only medium/low findings remain; score is above the 80 gate and below the 90 bar, further rewrites risked regressing passing evals.

Eval gate residuals (suites below 90 percent after three fix rounds, run on referee-one): `reducing-entropy` output 6/8 (assertions need a loaded reference or a real codebase that the tool-less runner lacks), `excalidraw` output 8/9 (one assertion wants an explicit request to a delegate for labels only; the answer offered a local extraction instead), `marp-slide` output 8/9 (the bundled template is not readable by the runner), `mui` output 8/9 (the legacy-api case does not mention `slots`/`slotProps`). Details: `eval-classification.md`.
