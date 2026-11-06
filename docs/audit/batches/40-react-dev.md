# Batch 40

## react-dev (skill)

### react-dev#D7-1
- severity: medium
- dimension: D7
- location: skills/react-dev/evals/evals.json:30
- fix: Replace the submit-handler and typed-button evals with prompts that need the skill, since the model passes both without it. For example: a form with two submit buttons that must read which one was clicked (assert (e.nativeEvent as SubmitEvent).submitter is passed to FormData), and a Button request with no package.json and no stated major (assert React 18-compatible forwardRef and that the response states the assumed version).

### react-dev#D8-1
- severity: low
- dimension: D8
- location: skills/react-dev/references/react-19-patterns.md:131
- fix: Point to the right place: "Run the codemods exactly as SKILL.md step 1 lists them". The React 19 gotcha only refers back to step 1, so an agent following this pointer reaches a bullet that has no commands.

### react-dev#D8-2
- severity: low
- dimension: D8
- location: skills/react-dev/SKILL.md:83
- fix: Show the import the type-test file needs, for example `import { col } from './columns';`, or say that the column builder must be exported. As written, the snippet puts the contract in a separate file but uses `col` from the component module, and that file will not compile.

### react-dev#D8-1
- severity: high
- dimension: D8
- location: skills/react-dev/references/react-router.md:53
- fix: Split the middleware instructions at v7.9: use the unprefixed APIs for v7.9+ and v8; for earlier middleware-capable v7 releases, show unstable_createContext, unstable_RouterContextProvider and the corresponding unstable middleware exports/types with future.unstable_middleware. Alternatively, explicitly require upgrading to v7.9+ before applying this example.

### react-dev#D1-1
- severity: low
- dimension: D1
- location: skills/react-dev/SKILL.md:63
- fix: Keep only the item the model often misses (an explicit useState type when the initializer is null, [] or a single literal) and delete ComponentPropsWithoutRef, discriminated-union variants and children: ReactNode, which current models already apply.

### react-dev#D5-1
- severity: low
- dimension: D5
- location: skills/react-dev/examples/server-components.md:121
- fix: Add references/hooks.md to the Server Components row of the SKILL.md load table ("plus hooks.md when the component reads browser storage") and drop the link from the example file, so every file reference stays one level deep from SKILL.md.

### react-dev#D1-1
- severity: low
- dimension: D1
- location: skills/react-dev/references/react-19-patterns.md:128
- fix: Replace the repeated checklist with a short pointer to SKILL.md steps 1 and 5; retain the reference's worked examples and any migration details not already covered there.
