# Batch 17

## react-useeffect (skill)

### react-useeffect#D7-1
- severity: medium
- dimension: D7
- location: skills/react-useeffect/evals/trigger-queries.json:35
- fix: Label this standalone networking query false. Add a separate positive with realistic React context, such as an existing useEffect in SearchResults.tsx whose previous query overwrites the current results.

### react-useeffect#D8-1
- severity: medium
- dimension: D8
- location: skills/react-useeffect/anti-patterns.md:250
- fix: Complete the example with loading and error state, guarded success/error/finally writes, and HTTP-status handling in the fetch helper. Verify obsolete failures and completions cannot overwrite the current request's state.

### react-useeffect#D8-2
- severity: low
- dimension: D8
- location: skills/react-useeffect/anti-patterns.md:272
- fix: Close the tsx fence immediately after the App example and leave the lifetime, retry, and cache guidance as ordinary prose.

### react-useeffect#D7-1
- severity: low
- dimension: D7
- location: skills/react-useeffect/evals/evals.json:1
- fix: Add an eval whose fetch rejects or whose cleanup runs twice under Strict Mode, asserting the skill's prescribed handling

### react-useeffect#D8-1
- severity: low
- dimension: D8
- location: skills/react-useeffect/SKILL.md:16
- fix: 'scoped adjustment' is undefined until alternatives.md is loaded; link the phrase to the partial-identity-reset section or define it in one inline clause

### react-useeffect#D1-1
- severity: medium
- dimension: D1
- location: skills/react-useeffect/SKILL.md:12
- fix: Keep the common render/event distinctions as a short activation table. Reduce duplicated basic demonstrations and devote detailed examples to partial identity resets, SSR snapshots, initialization retries, and stale asynchronous writes.

### react-useeffect#D1-1
- severity: medium
- dimension: D1
- location: skills/react-useeffect/anti-patterns.md:6
- fix: Items 1-8 re-derive react.dev's 'You Might Not Need an Effect' examples the model already knows; compress them to one-line entries and keep the expert content (item 9's guard-lifetime analysis and alternatives.md's boundary notes)

### react-useeffect#D2-1
- severity: low
- dimension: D2
- location: skills/react-useeffect/SKILL.md:3
- fix: The description promises RTL testing but neither the body nor the references give any RTL procedure; add a short testing step to the correctness loop (act/userEvent, assert cleanup behavior) or drop the RTL claim from the description

### react-useeffect#D3-1
- severity: low
- dimension: D3
- location: skills/react-useeffect/SKILL.md:28
- fix: Gotchas are embedded in prose steps; extract the NEVER items (no dependency suppression, no state-to-state Effects, no asymmetric cleanup) into a scannable list under its own heading

### react-useeffect#D6-1
- severity: low
- dimension: D6
- location: skills/react-useeffect/SKILL.md:17
- fix: State the fallback when the contract does not fit: 'otherwise use an Effect subscription with stable cleanup and identity-stable snapshots'
