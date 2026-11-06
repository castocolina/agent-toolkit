# Batch 39

## react-dev (skill)

### react-dev#D7-1
- severity: low
- dimension: D7
- location: skills/react-dev/evals/evals.json
- fix: Replace the assertions that a baseline model passes without the skill with ones that test skill-specific knowledge. For example, in submit-handler, assert that the submitter is read from `e.nativeEvent.submitter` (or `new FormData(form, submitter)`) when a form has several submit buttons. In typed-button, add an edge case with no package.json and no stated major, and assert that the answer falls back to React 18-compatible code and says so.

### react-dev#D8-1
- severity: medium
- dimension: D8
- location: skills/react-dev/SKILL.md:95
- fix: Export the contract function (`export function columnContract() { ... }`), and say so in Validate step 3. A non-exported, never-called function in a module fails `tsc --noEmit` with TS6133 under `noUnusedLocals`, which most strict tsconfigs enable. When that happens the type-test file breaks the typecheck for the wrong reason.

### react-dev#D8-1
- severity: high
- dimension: D8
- location: skills/react-dev/SKILL.md:35
- fix: Do not infer browser-only execution from React Router's ssr:false setting. Classify build-time-rendered roots and prerendered routes alongside SSR components: browser globals only after mount and hydration-stable initial output. Reserve the browser-only branch for confirmed client-only subtrees; distinguish SPA mode from prerender configuration.

### react-dev#D8-2
- severity: medium
- dimension: D8
- location: skills/react-dev/SKILL.md:16
- fix: Make installed runtime/type-major consistency a preflight before the first-match API-compatibility table. After resolving mismatches, apply the peerDependencies rule to decide whether the emitted API must remain React 18-compatible.

### react-dev#D8-3
- severity: high
- dimension: D8
- location: skills/react-dev/references/event-handlers.md:48
- fix: Prefer native form submission when no custom Enter behavior is needed. If this handler must submit explicitly, guard non-Enter/composing events, call e.preventDefault() for the handled Enter event, and then call requestSubmit() exactly once.

### react-dev#D1-1
- severity: low
- dimension: D1
- location: skills/react-dev/SKILL.md:105
- fix: Cut these lines to the parts current models get wrong. Keep the pointer to the submitter and IME traps in event-handlers.md. Drop the restatement of ChangeEvent/currentTarget, which the activation checklist and event-handlers.md already cover, and merge the use() try/catch point into the use() promise gotcha as one clause.

### react-dev#D3-1
- severity: low
- dimension: D3
- location: skills/react-dev/SKILL.md:113
- fix: Replace this with the trap it hides: an action whose success path falls through and returns `undefined` widens the state to `State | undefined`, so the error appears where `state.errors` is read, not in the action. Tell the agent to annotate the action's return type as `Promise<State>` so the missing return fails at the action itself.

### react-dev#D1-1
- severity: medium
- dimension: D1
- location: skills/react-dev/references/event-handlers.md:28
- fix: Compress routine handler aliases, inline inference and basic native-input reads into a short activation checklist. Retain the higher-delta material about submitter extraction, passive listeners, focus movement and custom-event producer typing.

### react-dev#D1-2
- severity: medium
- dimension: D1
- location: skills/react-dev/references/react-19-patterns.md:32
- fix: Reduce this example to the explicitly typed state/action signature and hook call. Keep the migration differences and Server Action authorization reference, but omit the standard input/form/button scaffold that adds no new typing decision.
