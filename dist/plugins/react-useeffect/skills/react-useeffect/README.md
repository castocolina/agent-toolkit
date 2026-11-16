# React useEffect Best Practices

A skill that decides when React code needs `useEffect` and when it does not, then checks the Effects that remain: dependencies, symmetric cleanup, stale or out-of-order async writes, the Strict Mode development replay, and once-per-app initialization. This skill is based on official React documentation and provides practical alternatives to common useEffect anti-patterns.

The routing table, correctness loop and NEVER list live in [SKILL.md](SKILL.md); this file only covers what the skill is for and how to install it.

## What it does

- Moves derived values into render, user-caused work into event handlers, and full resets onto a `key`.
- Handles the cases where the obvious fix is wrong: a partial reset that must keep sibling state, a `useSyncExternalStore` snapshot that must stay cached, a value an Effect reads without reacting to (`useEffectEvent`, React 19.2+, with a fallback for older versions).
- Hardens hand-rolled fetch Effects: every success, error and `finally` write guarded, HTTP errors kept apart from network failures, aborted requests ignored.
- Scopes "run once" initialization to a named lifetime, with retry after failure.

## Files

- `SKILL.md`: routing table, correctness and test loop, NEVER list, and which reference to load when.
- `references/anti-patterns.md`: smell catalog for audits (each row links its react.dev section), a complete fetch hook, the initialization cache.
- `references/alternatives.md`: partial identity reset, external store snapshots, non-reactive reads.

## Example prompts

- "Should this filtered list live in state with an Effect?"
- "Search results sometimes show the previous query after fast typing."
- "Our auth refresh runs twice in development; can I add a ref so it only runs once?"

## Installation

**Claude Code:**

```bash
cp -r skills/react-useeffect ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste the contents of `SKILL.md` into the conversation.

## Evals

`evals/evals.json` holds output evals (fixtures in `evals/files/`), and `evals/trigger-queries.json` holds trigger queries, including near-miss requests about data libraries, routing and testing that should not load this skill.

## Resources

This skill is based on:
- [React Official Docs: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [React Official Docs: Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)
- [React Official Docs: Lifecycle of Reactive Effects](https://react.dev/learn/lifecycle-of-reactive-effects)
