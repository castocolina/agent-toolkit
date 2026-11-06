# Batch 07

## react-dev (skill)

### react-dev#D7-1
- severity: medium
- dimension: D7
- location: skills/react-dev/evals/evals.json:10
- fix: Grade accepted props, ref compatibility, and rejected invalid inputs rather than exact helper names. Add minimal TSX fixtures with positive and negative type checks, a router-mode case, and an SSR/storage edge case; include realistic file paths and failure context in several trigger queries.

### react-dev#D8-1
- severity: high
- dimension: D8
- location: skills/react-dev/examples/server-components.md:161
- fix: Authenticate within each Server Action and authorize the requested userId before accessing the database. Derive the identifier from the session where appropriate, otherwise check ownership or role explicitly and return a controlled authorization failure.

### react-dev#D8-2
- severity: high
- dimension: D8
- location: skills/react-dev/examples/server-components.md:464
- fix: Associate loaded state with its key and skip persistence until the current key has been read successfully. Guard both storage operations, define missing-key behavior explicitly, and verify that switching keys never writes a value belonging to another key.

### react-dev#D8-3
- severity: medium
- dimension: D8
- location: skills/react-dev/references/react-19-patterns.md:438
- fix: Check response.ok, obtain the confirmed message, and update the authoritative message state or refresh its owner before the Action completes. Use unique temporary identifiers and demonstrate distinct success-commit and failure-rollback outcomes.

### react-dev#D8-4
- severity: medium
- dimension: D8
- location: skills/react-dev/references/react-19-patterns.md:540
- fix: Keep the input update urgent and move filtering into a deferred or transition-driven render, with a memoized results boundary where needed. Use a worker for genuinely long synchronous computation; do not present wrapping the computation in startTransition as deferring that computation.

### react-dev#D7-1
- severity: medium
- dimension: D7
- location: skills/react-dev/evals/evals.json:1
- fix: Add an edge-case eval, e.g. a component that must stay React 18-compatible inside a React 19 app, asserting forwardRef is chosen over ref-as-prop

### react-dev#D8-1
- severity: low
- dimension: D8
- location: skills/react-dev/SKILL.md:28
- fix: Add a fallback branch: 'If no router is installed and the app is not greenfield, keep the existing navigation and state the limitation instead of recommending an install'

### react-dev#D1-1
- severity: medium
- dimension: D1
- location: skills/react-dev/SKILL.md:14
- fix: Reduce native-prop, ReactNode, nullable-state, and tuple reminders to a brief activation checklist. Concentrate the main instructions on correlated generics, version-sensitive Action contracts, promise ownership, and server/client execution traps.

### react-dev#D2-1
- severity: medium
- dimension: D2
- location: skills/react-dev/SKILL.md:16
- fix: Show the reusable derivation: capture K in a builder, tie its value and callback to T[K], package the renderer without widening that relationship, and demonstrate a valid pairing and a rejected mismatched pairing.

### react-dev#D1-1
- severity: low
- dimension: D1
- location: skills/react-dev/SKILL.md:15
- fix: Delete the ref-nullability sentence; keep the React 19 useRef-initializer rule, which is the non-obvious part of that bullet

### react-dev#D2-1
- severity: low
- dimension: D2
- location: skills/react-dev/SKILL.md:26
- fix: Split the router decision from the reference list and add a combined-task note (e.g. React 19 migration plus router upgrade) stating which references to load together

### react-dev#D3-1
- severity: low
- dimension: D3
- location: skills/react-dev/SKILL.md:40
- fix: Add a migration gotcha such as 'React 19 removes react-dom/test-utils.act and @types/react 19 changes ref typing; pin matching type versions or CI fails confusingly'

### react-dev#D6-1
- severity: low
- dimension: D6
- location: skills/react-dev/SKILL.md:18
- fix: Add 'Check the installed react version in package.json first; when unknown or mixed, assume React 18-compatible and say so'
