# design-system-starter sources (plan 14 Task 3 Step 4, review only, 2026-11-07)

## Origins found

1. Original author: ArieGoldkin/ai-agent-hub (MIT, default branch main), path `skills/design-system-starter/`. Verified with `gh api`: its tree holds the same six files (SKILL.md, checklists/design-system-checklist.md, references/component-examples.md, templates/component-template.tsx, templates/design-tokens-template.json). Git blob shas of the checklist, component-examples, component-template.tsx and design-tokens-template.json equal the softaworks copy at `3027f20f`; SKILL.md differs (softaworks edited the frontmatter) and the README was written by softaworks. The four-principle wording ("Consistency Over Creativity" ...) also matches it. Upstream last commit for the path: 75a3d12128, 2025-11-01.
2. Distributor: softaworks/agent-toolkit (the fork's root README line 5 credits it; the registry already holds the `repo` row `softaworks/agent-toolkit`, `skill: null`).
3. Scale values (typography xs-5xl, spacing 0-24, radius, shadows, palette ramps) match the Tailwind CSS default theme (MIT, https://tailwindcss.com/docs/theme). No credit line exists. Treated as a reference origin, not a copy source.

## Missing credit

`skills/design-system-starter/README.md` has no credit line, and the root README row for this skill carries none. Proposed line for the README (add under License, controller or fixer applies it; nothing was edited here):

`Adapted from [ArieGoldkin/ai-agent-hub](https://github.com/ArieGoldkin/ai-agent-hub/tree/main/skills/design-system-starter) by Arie Goldkin (MIT), through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit).`

Optional second line once token-scales.md is restored: `Scale values follow the Tailwind CSS default theme (MIT): https://tailwindcss.com/docs/theme.`

## Proposed registry rows (docs/audit/upstream-sources.json; fields skill, kind, source, ref, credit)

```json
{"skill": "design-system-starter", "kind": "github-path", "source": "ArieGoldkin/ai-agent-hub:skills/design-system-starter/SKILL.md", "ref": "main", "credit": "@ArieGoldkin"}
{"skill": "design-system-starter", "kind": "unversioned", "source": "Web Content Accessibility Guidelines (WCAG) 2.2: https://www.w3.org/TR/WCAG22/", "ref": null, "credit": "W3C"}
{"skill": "design-system-starter", "kind": "unversioned", "source": "Design Tokens Format Module 2025.10: https://www.designtokens.org/tr/2025.10/format/", "ref": null, "credit": "Design Tokens Community Group"}
{"skill": "design-system-starter", "kind": "unversioned", "source": "MDN, the dialog element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog", "ref": null, "credit": "MDN Web Docs"}
{"skill": "design-system-starter", "kind": "unversioned", "source": "HTML Standard, the button element: https://html.spec.whatwg.org/multipage/form-elements.html#the-button-element", "ref": null, "credit": "WHATWG"}
{"skill": "design-system-starter", "kind": "unversioned", "source": "React 19 release post: https://react.dev/blog/2024/12/05/react-19", "ref": null, "credit": "React team"}
{"skill": "design-system-starter", "kind": "unversioned", "source": "Tailwind CSS box-shadow and theme docs: https://tailwindcss.com/docs/box-shadow", "ref": null, "credit": "Tailwind Labs"}
{"skill": "design-system-starter", "kind": "github", "source": "style-dictionary/style-dictionary", "ref": "main", "credit": "Style Dictionary maintainers"}
{"skill": "design-system-starter", "kind": "unversioned", "source": "Chrome DevTools accessibility reference: https://developer.chrome.com/docs/devtools/accessibility/reference", "ref": null, "credit": "Google Chrome DevTools"}
```

The two W3C pages for target size (2.5.8, 2.5.5) are subpages of the WCAG row and need no row of their own. `github-path` was picked for the upstream row over `github` because only this one path is the origin; if the controller prefers repo-level tracking use `ArieGoldkin/ai-agent-hub` with kind `github`.

## Skill-updater style review (REVIEW ONLY, no track call, no edit)

`upstreams` was not run (no rows exist yet); upstream state was read with `gh api`.

- Upstream drift: 4 of 5 shared files are byte-identical to the original; upstream has had no commit to the path since 2025-11-01. Nothing upstream to adopt.
- Adopt: none.
- Adapt (for the restore brief):
  - token-scales.md: typography, spacing, radius, shadow, z-index and easing scales in DTCG 2025.10 object form (no strings), as a Tailwind-style scale to replace per brand; shadows as DTCG `shadow` objects; do not copy old shadow names (see facts.md); add warning and info feedback roles with a contrast-checked step (old yellow-600 is 2.94:1); keep the credit line.
  - component-specs.md: one table row per component (variants, sizes, states, accessibility) covering s064-s070, s072-s078, plus layout (Stack, Cluster, container, sidebar) and feedback states (loading, empty, error); Select as combobox, Table with sortable `aria-sort`, Alert with live region and non-color status, Navigation with nav landmark and `aria-current`, Modal on native dialog.
  - component-examples.md: compound Card (no root className, role tokens), polymorphic component (React 19 ref-as-prop), skip link in plain CSS, theme toggle that reads the head-script value, responsive navigation with `aria-expanded` and `aria-controls`, a props-conventions note (s046), and a native-dialog Modal example to take the slot of the unsafe old one (new content, row s110 is intended-change).
  - token-checks.md: large-text definition (18pt, or 14pt bold).
  - README: list the new references, add the credit line above.
- Ignore: the old Button, Input and Modal code, the keyboard example, the old tokens template and its schema URL (rows s106, s109, s110, s050, file rows), WCAG 2.1 wording, 44px touch target as an AA rule, and the 100KB budget.
- Pending user decision (not adapt): s083-s086, a general WCAG POUR checklist, recorded as `purpose-change-pending`.
- Model-validity pass: the rules that counter model habits (semantic roles, no color-mix derivation, no aria-modal div, head-script theme) stay valid; no model IDs or model-specific defaults appear in this skill.
