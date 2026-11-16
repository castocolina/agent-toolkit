# react-useeffect: sources

Checked 2026-11-15 at BASE 10117452dca20caa535f5523046a3690a0c3cd21.

## Origins found

1. react.dev, "You Might Not Need an Effect" (https://react.dev/learn/you-might-not-need-an-effect). The current README Resources section credits it and two sibling pages ("Synchronizing with Effects", "Lifecycle of Reactive Effects"); SKILL.md ends with "Based on react.dev". Registry already has the row (see below).
2. softaworks/agent-toolkit, `skills/react-useeffect` (fork origin). The upstream skill exists at `3027f20f` (commit `1ef06f0a`, "feat: add react-useeffect skill", 2026-01-21, one commit, never changed since). Its SKILL.md, README.md, alternatives.md and anti-patterns.md carry no credit, author or license line, and the baseline `dbff837f` shows none either. The repo-level credit is the root README line "Fork of softaworks/agent-toolkit by @leonardocouy" and the `kind: repo` registry row (skill null). Other softaworks skills (for example naming-analyzer) carry a per-skill README credit and a per-skill `github-path` row; react-useeffect has neither.
3. Official pages used to verify facts (all `unversioned`, see facts.md): React API pages and blog posts listed below, plus MDN for `fetch`.
4. Distinctive-phrase web search was not needed: every example in the baseline text (Taylor Swift `fullName`, `isInCart` toast, `Game` gold-card chain, `didInit`) is react.dev's own.

## Missing credit line

Yes, the softaworks per-skill credit. Proposed line for `skills/react-useeffect/README.md` (the form naming-analyzer's README uses, line 38: "Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy."), placed after the Resources section:

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The existing react.dev credit text ("React Official Docs") stays untouched. The row's `credit` field `react.dev` already appears verbatim in README.md (URLs), so `missing_credit` stays clear. I did not edit README.md (brief).

## Proposed registry rows

Existing row (kept, no change): `reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md`, `ref: main`, `last_reviewed: 2026-11-04`, `status: current`.

New rows (verbatim JSON, same shape as the neighboring rows; `last_reviewed`/`status` are set by `track`, not by hand):

```json
{
  "skill": "react-useeffect",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/react-useeffect",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "Synchronizing with Effects, React learn (https://react.dev/learn/synchronizing-with-effects)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "useEffectEvent, React reference (https://react.dev/reference/react/useEffectEvent)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "experimental_useEffectEvent, React 18 reference (https://18.react.dev/reference/react/experimental_useEffectEvent)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "Separating Events from Effects, React learn (https://react.dev/learn/separating-events-from-effects)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "useSyncExternalStore, React reference (https://react.dev/reference/react/useSyncExternalStore)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "useMemo, React reference (https://react.dev/reference/react/useMemo)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "useRef, React reference (https://react.dev/reference/react/useRef)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "StrictMode, React reference (https://react.dev/reference/react/StrictMode)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "exhaustive-deps, eslint-plugin-react-hooks reference (https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps)",
  "ref": null,
  "credit": "react.dev"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "React 19.2 release post (https://react.dev/blog/2025/10/01/react-19-2)",
  "ref": null,
  "credit": "React team"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "React Compiler v1.0 release post (https://react.dev/blog/2025/10/07/react-compiler-1)",
  "ref": null,
  "credit": "React team"
}
```

```json
{
  "skill": "react-useeffect",
  "kind": "unversioned",
  "source": "MDN, Window: fetch() method (https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch)",
  "ref": null,
  "credit": "Mozilla"
}
```

Note: `check --strict` `missing_credit` requires each row's `credit` text to appear verbatim in SKILL.md, README.md or references/*.md. `react.dev` appears (README URLs, SKILL.md "Based on react.dev"). `React team` and `Mozilla` do not appear in the current files; either the restore adds natural references to them (for example "React Compiler 1.0 release post" or "MDN" in a facts or sources sentence) or those rows use credit `react.dev` and `MDN` where the page already names them. Check with `audit.py check --strict` after the registry edit. The existing registry already uses `React team` as a credit for the react-dev skill's React 19 row, so the first form is the repo's precedent.

## `upstreams` result (read-only run, 2026-11-15)

Row `reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md`: `error: null`, `stale: false`, `source_updated: 2025-11-10T19:22:50Z`, `ours_updated: 2026-11-06`. No `track` call made.

## skill-updater style review (review only)

Upstream changes to the react.dev page since the stored review (2026-11-04), read from the commits:

- `d271a7ac` (2025-11-06), "Fix incorrect condition in Chains of computations example (#8109)": `goldCardCount <= 3` became `< 3` in the event-handler fix. Decision: ignore. This skill's chains smell row has no card-count code, and the baseline text this recovery reads already used `< 3`.
- `b440d669` (2025-11-10), "update internal links (#8136)": only link targets changed (`/learn/start-a-new-react-project` to `/learn/creating-a-react-app`). Decision: ignore (no link to those pages in the skill).
- `8d73630a` (2025-10-07), "Upgrade to stable react compiler (#8058)": the page now says React Compiler can memoize automatically and so removes the need for manual `useMemo` in many cases. Decision: adopt, through the s037 restore (one sentence plus the escape-hatch caveat from the Compiler 1.0 post); this is the only upstream change that matters for this skill.

Adopt/adapt/ignore items for the restore brief:

- ADOPT (s037): measuring procedure for "measured cost" (console.time around the calculation, about 1ms or more per interaction, test on a throttled CPU and a production build, `useMemo` does not speed the first render) plus the React Compiler sentence (manual `useMemo` needed less in many cases; remains an escape hatch for values used as Effect dependencies; leave existing memoization in place or test before removing). Put it in references/anti-patterns.md next to the first smell row or in a short "Caching expensive calculations" note, and add one trigger in SKILL.md section 4 only if the file would not already be loaded for a useMemo question (the routing table row currently points at no file for it). Write the Compiler claim as a pointer to the live React Compiler docs, with the version-sensitive status dated.
- ADAPT (s040): add to the isInCart smell row (or a new row) the react.dev rule for the case of two handlers sharing logic: extract one function that both handlers call. Keep this skill's existing note that the Effect also fires on reload.
- ADAPT (s053): in "Initialization that must run once", add the module-level alternative `if (typeof window !== 'undefined') { ... }` with the SSR consequence (top-level code also runs on import and, in a server-rendered app, on the server unless guarded), keeping this skill's stricter rule that fallible work must not be marked done early and the "app entry module only" limit. Do not restore react.dev's unconditional `didInit` endorsement.
- IGNORE: the s042 lifting-state-up section (pending drop, generic model knowledge); the React 18-only wording of the old Strict Mode README text.

Model-validity pass: not run. The skill's rules are factual React rules and routing, not habit-countering rules (no banned words or substitutions to undo), so there is no behavior to elicit; it would only be needed if the restore adds a model-habit rule. No `track` call was made, per the brief.

Optional note for the facts reviewer: the repo's react-dev skill already cites the React 19 post and upgrade guide; it holds no `useMemo`, `didInit` or Effect-routing content (its description defers Effect questions to react-useeffect), so nothing moved there.
