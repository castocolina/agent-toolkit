# React TypeScript Development Skill

A skill for Claude Code and claude.ai that types React 18 and 19 code in TypeScript: component props and refs, event handlers, generic components, React 19 Actions, Server Components and Server Actions, and TanStack Router or React Router v7/v8.

It checks the installed React, `@types/react` and router versions before choosing an API, loads only the reference the task needs, and proves type contracts with the type checker. The version tables, decision tables, gotchas and load list live in [SKILL.md](SKILL.md); this file only covers what the skill is for and how to install it.

## What it does

- Picks the ref, form-state and router API that matches the installed versions, falling back to React 18-compatible code when versions are unknown.
- Designs generic APIs that keep correlated types (a column key and its renderer) checked, with a `@ts-expect-error` line for the rejected case.
- Flags server/client traps: unauthorized Server Actions, browser globals during server render, unstable promises passed to `use()`.
- Covers React 19 and React Router v8 upgrade breaks in the type definitions.

Effect design (whether a `useEffect` is needed, dependencies, cleanup) is left to the `react-useeffect` skill.

## Example prompts

- "Type this Button so it takes every native button prop and a ref."
- "My generic table lets a Date column get a string renderer; fix the types."
- "We're upgrading to React 19; replace `useFormState` in `ProfileForm.tsx`."
- "Type the loader context in our React Router v8 app."

## Installation

**Claude Code:**

```bash
cp -r skills/react-dev ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste the contents of `SKILL.md` into the conversation.

## Evals

`evals/evals.json` holds output evals (fixtures in `evals/files/`), and `evals/trigger-queries.json` holds trigger queries, including near-miss requests that belong to `react-useeffect`, React Native or styling.

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Facts are checked against the official documentation: react.dev (including legacy.reactjs.org), nextjs.org, reactrouter.com, tanstack.com, typescriptlang.org, zod.dev and developer.mozilla.org, and against the README of eps1lon/types-react-codemod.

---

**Version:** 1.0.0
**Last Updated:** 2026-01-20
**Maintained by:** Softaworks Agent Skills
