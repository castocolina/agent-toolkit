# react-dev sources (plan 14, batch 6)

## Origin

- Upstream: `softaworks/agent-toolkit`, path `skills/react-dev`. The tree at the fork point `3027f20f` is byte-identical to the baseline `dbff837f` (`git diff --stat 3027f20f dbff837f -- skills/react-dev` prints nothing), so every baseline section recorded in `record.md` is upstream text, and the current files are a local rewrite.
- Upstream today: `gh api repos/softaworks/agent-toolkit/contents/skills/react-dev?ref=main` exits 0; the only commit touching the path is `e051bb4a48` (2026-01-20, "feat: add react-dev skill"). Nothing changed upstream since the fork point.
- Web search on the opening line ("Type-safe React = compile-time guarantees = confident refactoring") finds `react-dev` listings on skills.sh (davila7/claude-code-templates, chidekina/aria-superpowers, ma1orek/replay) with the same text. They are copies of the softaworks skill, not origins; their dates were not checked. No other origin.
- Credits found: the README footer "Maintained by: Softaworks Agent Skills" (kept) and the root README line "Fork of softaworks/agent-toolkit ... by @leonardocouy". No credit line names the upstream in the skill's own README, and no registry row exists for `react-dev`.

## Missing credit line

The registry row below carries the credit text `softaworks/agent-toolkit`, and `audit.py check --strict` fails with `missing_credit` unless that text appears in SKILL.md, README.md or references/*.md. `skills/react-dev/README.md` does not contain it (only "Softaworks Agent Skills"). Add this line to `skills/react-dev/README.md`, in the same form as the sibling skills (`naming-analyzer`, `mui`, `commit-work`), before the closing footer rule and without touching the footer lines:

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The docs rows below each carry a short vendor credit that must also appear in the README. Add one line with all of them:

```text
Facts are checked against the official documentation: react.dev (including legacy.reactjs.org), nextjs.org, reactrouter.com, tanstack.com, typescriptlang.org, zod.dev and developer.mozilla.org, and against the README of eps1lon/types-react-codemod.
```

## Proposed registry rows (docs/audit/upstream-sources.json)

```json
{"skill": "react-dev", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/react-dev", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "react-dev", "kind": "github-path", "source": "eps1lon/types-react-codemod:README.md", "ref": "main", "credit": "eps1lon/types-react-codemod"}
{"skill": "react-dev", "kind": "unversioned", "source": "React 19 Upgrade Guide (https://react.dev/blog/2024/04/25/react-19-upgrade-guide)", "ref": null, "credit": "react.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "useActionState, React reference (https://react.dev/reference/react/useActionState)", "ref": null, "credit": "react.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "useOptimistic, React reference (https://react.dev/reference/react/useOptimistic)", "ref": null, "credit": "react.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "startTransition, React reference (https://react.dev/reference/react/startTransition)", "ref": null, "credit": "react.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "use, React reference (https://react.dev/reference/react/use)", "ref": null, "credit": "react.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "forwardRef, React reference (https://react.dev/reference/react/forwardRef)", "ref": null, "credit": "react.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "useDeferredValue, React reference (https://react.dev/reference/react/useDeferredValue)", "ref": null, "credit": "react.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "useFormStatus, React DOM reference (https://react.dev/reference/react-dom/hooks/useFormStatus)", "ref": null, "credit": "react.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "React v17.0 release post (https://legacy.reactjs.org/blog/2020/10/20/react-v17.html)", "ref": null, "credit": "legacy.reactjs.org"}
{"skill": "react-dev", "kind": "unversioned", "source": "Next.js page.js file convention (https://nextjs.org/docs/app/api-reference/file-conventions/page)", "ref": null, "credit": "nextjs.org"}
{"skill": "react-dev", "kind": "unversioned", "source": "Next.js CLI, next typegen (https://nextjs.org/docs/app/api-reference/cli/next)", "ref": null, "credit": "nextjs.org"}
{"skill": "react-dev", "kind": "unversioned", "source": "Next.js data security guide (https://nextjs.org/docs/app/guides/data-security)", "ref": null, "credit": "nextjs.org"}
{"skill": "react-dev", "kind": "unversioned", "source": "Next.js 15.5 release post (https://nextjs.org/blog/next-15-5)", "ref": null, "credit": "nextjs.org"}
{"skill": "react-dev", "kind": "github-path", "source": "remix-run/react-router:CHANGELOG.md", "ref": "main", "credit": "reactrouter.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "React Router, Middleware how-to (https://reactrouter.com/how-to/middleware)", "ref": null, "credit": "reactrouter.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "React Router, Route module type safety (https://reactrouter.com/how-to/route-module-type-safety)", "ref": null, "credit": "reactrouter.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "React Router, Type safety explanation (https://reactrouter.com/explanation/type-safety)", "ref": null, "credit": "reactrouter.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "React Router, Error boundaries how-to (https://reactrouter.com/how-to/error-boundary)", "ref": null, "credit": "reactrouter.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "React Router, Using handle how-to (https://reactrouter.com/how-to/using-handle)", "ref": null, "credit": "reactrouter.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "TanStack Router, Search params guide (https://tanstack.com/router/latest/docs/framework/react/guide/search-params)", "ref": null, "credit": "tanstack.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "TanStack Router, Type safety guide (https://tanstack.com/router/latest/docs/framework/react/guide/type-safety)", "ref": null, "credit": "tanstack.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "TanStack Router, Type utilities guide (https://tanstack.com/router/latest/docs/framework/react/guide/type-utilities)", "ref": null, "credit": "tanstack.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "TanStack Router, Router context guide (https://tanstack.com/router/latest/docs/framework/react/guide/router-context)", "ref": null, "credit": "tanstack.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "TanStack Router, Install with the Router CLI (https://tanstack.com/router/latest/docs/framework/react/installation/with-router-cli)", "ref": null, "credit": "tanstack.com"}
{"skill": "react-dev", "kind": "unversioned", "source": "TypeScript 5.4 release notes (https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html)", "ref": null, "credit": "typescriptlang.org"}
{"skill": "react-dev", "kind": "unversioned", "source": "TypeScript 5.0 release notes (https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html)", "ref": null, "credit": "typescriptlang.org"}
{"skill": "react-dev", "kind": "unversioned", "source": "TypeScript TSConfig reference, strictFunctionTypes (https://www.typescriptlang.org/tsconfig/#strictFunctionTypes)", "ref": null, "credit": "typescriptlang.org"}
{"skill": "react-dev", "kind": "unversioned", "source": "Zod, Formatting errors (https://zod.dev/error-formatting)", "ref": null, "credit": "zod.dev"}
{"skill": "react-dev", "kind": "unversioned", "source": "MDN, FormData constructor (https://developer.mozilla.org/en-US/docs/Web/API/FormData/FormData)", "ref": null, "credit": "developer.mozilla.org"}
```

Notes for the controller on these rows:

- `skill` is `react-dev`, a skill, so no `artifact_kind`. `ref` is `main` for `github-path` and `null` for `unversioned`, as `validate_entry` requires.
- The `github-path` rows for the codemod README and the React Router changelog are versioned, so `upstreams` can report a stale commit for them. The remaining pages are `unversioned` and `upstreams` always prints `stale: false` for them (known limit, plan 14 Task 3 Step 5).
- Two of the TanStack and React Router doc sets also live in public repos (`TanStack/router:docs/router/guide/...`, `remix-run/react-router:docs/...`). They were read from there with `gh api` where the site fetch failed. Switching a row to `github-path` is an option if staleness tracking matters more than the page URL.
- The `reactrouter.com` credit on the `CHANGELOG.md` row is chosen so the single README line above covers it; a `remix-run/react-router` credit would need its own README text.
- `gepetto` and `datadog-cli` are not touched.

## skill-updater style review (REVIEW ONLY; no `track` call made)

Procedure steps 1 to 5 of `skills/skill-updater/SKILL.md`, read-only:

1. Scope: `skills/react-dev/`, not a synced skill.
2. Rows: none for `react-dev` today. A credit line naming the upstream does not exist either, so the first step is the missing credit line and the row above; `track` cannot create a source row (skill-updater step 2), so the controller adds the row by hand.
3. Upstream state: the path exists on `main`, one commit (2026-01-20), identical to the fork point. The contents test and compare steps have nothing to classify.
4. Adopt, adapt, ignore for the restore brief:
   - Upstream changes: none to adopt, adapt or ignore.
   - Recovered baseline text (the three `restore-references` rows): adapt. `s115` (v7 `AppLoadContext` augmentation plus the incremental migration to `RouterContextProvider`), `s154` (typed route `handle` and `useMatches` breadcrumbs) and `s177` (typed search updater with `useNavigate({ from })`) are rewritten in the current style, with the verified facts in `facts.md`, and not pasted.
   - Source conflict to carry into the skill: the React 19 upgrade guide says `no-implicit-ref-callback-return` is part of the preset, the codemod README says both extra transforms are off by default in `preset-19`. SKILL.md follows the README (the tool wins); keep it.
   - Optional wording, not required: SKILL.md pins `types-react-codemod@3.5.3`, the guide uses `@latest`. The pin is verified current (v3.5.3 is the latest release on 2026-11-07); no edit needed unless a newer release appears.
5. Model-validity pass (step 6): not run, because it needs the repo's tool-less probe lane and this analyst brief forbids an LLM lane. Rules that exist to counter a model habit, for the controller to probe if wanted: annotate the `useActionState` action as `Promise<State>`; never read `window` or `localStorage` during render; correlated column builder instead of `keyof T` plus `T[keyof T]`; Next 15 `params` as Promises; TanStack `beforeLoad` output is context, not loader data; no `AppLoadContext` augmentation on React Router v8; `use()` promises never created in client render.
