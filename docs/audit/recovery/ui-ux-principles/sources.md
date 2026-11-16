# ui-ux-principles: sources, credits and registry review (recovery batch 20, facts-only)

Checked 2026-11-15. Review only: no `track` call made, `docs/audit/upstream-sources.json` and the root `README.md` not edited.

## Origin

- The skill is original to this repository: added by commit `9a4ba26c` (`feat(skills): add ui-ux-principles and skill-updater`), hardened by `46b06765`. It is not in the softaworks snapshot `3027f20f` (`git ls-tree 3027f20f skills/ui-ux-principles` is empty) and no file of the skill names softaworks, Madina Gbotoe or any other author (grep: no hit).
- Its content cites official and research pages (full list in `references/sources.md`); none of that text is copied from a credited work. The registry therefore holds one `local` row today and no source rows.
- The retired agent text (Madina Gbotoe, CC BY 4.0, softaworks `agents/ui-ux-designer.md`) is NOT in this skill. Its credit stays on `agents/ui-ux-designer.md` (batch 22) with the registry rows `ui-ux-designer` already carries. The agent preloads this skill (`skills: [ui-ux-principles]`, and the `agent-ui-ux-designer` plugin entry lists `./skills/ui-ux-principles`), so no credit line is missing here.

## Missing credit lines

None. `python3 scripts/audit/audit.py --root WT check --strict --skills ui-ux-principles` exits clean today (no registry `credit` for this skill, so no `missing_credit`).

Once the unversioned rows below are added, `credit_issues` reads `SKILL.md`, `README.md` and the top-level `references/*.md` only (not `references/rules/`). Every proposed `credit` string is already present verbatim in `references/sources.md` (checked with `grep -F`: `W3C`, `Apple`, `Nielsen Norman Group`, `web.dev`, `MDN`, `MUI`, `Tailwind CSS`, `Design Tokens Community Group`, `Material Web`), so no line has to be added. Fragility to know about: `W3C` currently occurs in `sources.md` only inside the DTCG row ("not a W3C Standard"), and `Apple` only inside the HIG rows. If the restore brief rewrites those rows, keep those words, or add the credit lines the strings need, or `check --strict` reports `missing_credit`.

## Proposed registry rows

Keep the existing `local` row as is (it is the row a source-less `track` call addresses; `local` and `unversioned` rows may coexist, `validate_entry` and `upstreams` accept both). Add one `unversioned` row per official page used. `ref` is `null` and `credit` is the publisher; `artifact_kind` is omitted because the artifact is a skill (the default). Each `source` is unique, so `track --source` addresses one row.

```json
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "W3C, Web Content Accessibility Guidelines (WCAG) 2.2: https://www.w3.org/TR/WCAG22/", "ref": null, "credit": "W3C"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "W3C, Understanding SC 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html", "ref": null, "credit": "W3C"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "W3C, Understanding SC 2.5.5 Target Size (Enhanced): https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html", "ref": null, "credit": "W3C"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "W3C, Understanding SC 2.4.13 Focus Appearance: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html", "ref": null, "credit": "W3C"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "W3C, Understanding SC 1.4.10 Reflow: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html", "ref": null, "credit": "W3C"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Apple, Human Interface Guidelines, Buttons: https://developer.apple.com/design/human-interface-guidelines/buttons", "ref": null, "credit": "Apple"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Apple, Human Interface Guidelines, Loading: https://developer.apple.com/design/human-interface-guidelines/loading", "ref": null, "credit": "Apple"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Nielsen Norman Group, Skeleton Screens 101: https://www.nngroup.com/articles/skeleton-screens/", "ref": null, "credit": "Nielsen Norman Group"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Nielsen Norman Group, Response Times: The 3 Important Limits: https://www.nngroup.com/articles/response-times-3-important-limits/", "ref": null, "credit": "Nielsen Norman Group"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Nielsen Norman Group, Visual Hierarchy: https://www.nngroup.com/articles/visual-hierarchy-ux-definition/", "ref": null, "credit": "Nielsen Norman Group"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Nielsen Norman Group, Designing Empty States: https://www.nngroup.com/articles/empty-state-interface-design/", "ref": null, "credit": "Nielsen Norman Group"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Nielsen Norman Group, Error-Message Guidelines: https://www.nngroup.com/articles/error-message-guidelines/", "ref": null, "credit": "Nielsen Norman Group"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Nielsen Norman Group, 10 Usability Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/", "ref": null, "credit": "Nielsen Norman Group"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "web.dev, Optimize Cumulative Layout Shift: https://web.dev/articles/optimize-cls", "ref": null, "credit": "web.dev"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "web.dev, Responsive web design basics: https://web.dev/articles/responsive-web-design-basics", "ref": null, "credit": "web.dev"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "web.dev, Container queries (Learn CSS): https://web.dev/learn/css/container-queries", "ref": null, "credit": "web.dev"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "web.dev, Focus: https://web.dev/articles/focus", "ref": null, "credit": "web.dev"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "web.dev, Accessible tap targets: https://web.dev/articles/accessible-tap-targets", "ref": null, "credit": "web.dev"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, CSS container queries: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, @container: https://developer.mozilla.org/en-US/docs/Web/CSS/@container", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, clamp(): https://developer.mozilla.org/en-US/docs/Web/CSS/clamp", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, :focus-visible: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, prefers-color-scheme: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, color-scheme: https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, aria-label: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-label", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, aria-invalid: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MDN, ARIA live regions: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions", "ref": null, "credit": "MDN"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, Skeleton: https://mui.com/material-ui/react-skeleton/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, ButtonBase API: https://mui.com/material-ui/api/button-base/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, Button API: https://mui.com/material-ui/api/button/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, IconButton API: https://mui.com/material-ui/api/icon-button/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, Dark mode: https://mui.com/material-ui/customization/dark-mode/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, Grid: https://mui.com/material-ui/react-grid/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, Text Field: https://mui.com/material-ui/react-text-field/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, Snackbar: https://mui.com/material-ui/react-snackbar/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "MUI, SnackbarContent API: https://mui.com/material-ui/api/snackbar-content/", "ref": null, "credit": "MUI"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Tailwind CSS, Animation: https://tailwindcss.com/docs/animation", "ref": null, "credit": "Tailwind CSS"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Tailwind CSS, Hover, focus, and other states: https://tailwindcss.com/docs/hover-focus-and-other-states", "ref": null, "credit": "Tailwind CSS"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Tailwind CSS, Responsive design: https://tailwindcss.com/docs/responsive-design", "ref": null, "credit": "Tailwind CSS"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Tailwind CSS, Dark mode: https://tailwindcss.com/docs/dark-mode", "ref": null, "credit": "Tailwind CSS"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Tailwind CSS, Upgrade guide: https://tailwindcss.com/docs/upgrade-guide", "ref": null, "credit": "Tailwind CSS"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Tailwind CSS, Display (sr-only): https://tailwindcss.com/docs/display", "ref": null, "credit": "Tailwind CSS"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Design Tokens Community Group, Design Tokens Format Module 2025.10: https://www.designtokens.org/TR/2025.10/format/", "ref": null, "credit": "Design Tokens Community Group"}
{"skill": "ui-ux-principles", "kind": "unversioned", "source": "Material Web, Progress indicator docs: https://raw.githubusercontent.com/material-components/material-web/main/docs/components/progress.md", "ref": null, "credit": "Material Web"}
```

44 rows (JSON Lines above; the registry is a JSON array, so add commas when merging). Not proposed as rows: caniuse (a data table, credit string not in `sources.md`), the MUI GitHub source files at tag `v9.5.0` (version-bound; pointer in `facts.md`), the Android and Material 3 pages (nothing used from them). The `sources.md` row for the DTCG page currently names `/TR/drafts/format/`; the registry row above uses the stable `/TR/2025.10/format/` (see facts.md).

## skill-updater style review (read-only)

Procedure followed: step 1 scope `skills/ui-ux-principles/` exists, not synced; step 2 only a `kind: local` row exists, so no `upstreams` run applies (it skips `local` rows) and the review goes to step 6 (model probe) and step 7 (the source-less `local` call, already recorded `current`, `last_reviewed` 2026-11-04). With the unversioned rows above, `track` per row would record `current` with no `--sha` (Gotchas: unversioned rows have no commit; read the source, then record `current`). I made no `track` call and no model-probe run.

Upstream-change review (what the live pages say against what the skill states), as adopt, adapt or ignore for the update brief:

| item | decision | reason |
|------|----------|--------|
| MUI is at v9.5.0, not v7 (`frameworks.md` heading) | adopt | Relabel the heading ("MUI v7 and later") or point at the repo's `package.json`; every MUI claim holds on 9.5.0. |
| MUI v9 `theme.focusVisible` (a theme key `Button` spreads under `.Mui-focusVisible`; ButtonBase `focusRipple` default false) | adapt | Add one line to the interaction Gotcha: a theme that sets `focusVisible` styles a ring; default Button and IconButton keep the focus ripple. Keep the existing verdict rules (they already say a theme override establishes nothing unless a ring is visible in source). |
| Tailwind `hover:` wrapping is a v4 behaviour (v3 restores with `@custom-variant hover (&:hover)`) | adapt | Keep the gotcha, add "Tailwind v4" so a v3 repo is not told hover never fires on touch. |
| Tailwind `aria-invalid:` is not a built-in variant; `sr-only` is documented; `motion-safe:`/`motion-reduce:` apply to any animation utility | adopt | Replace the UNVERIFIED lines in `frameworks.md`/`sources.md` with these facts. |
| MUI `SnackbarContent` default `role='alert'` | adopt | Matters for the states rule (`alert` interrupts, `status` confirms): add a `frameworks.md` bullet, "Snackbar content announces as `alert`; pass `role=\"status\"` for a confirmation". |
| DTCG 2025.10 is a Final Community Group Report ("stable"), still not a W3C Standard | adapt | Reword "draft community group report" in `tokens.md` and `sources.md`; keep "follow it only when the repo already keeps `.tokens.json` files" (the repo-use rule is a house decision, not an upstream claim). |
| NN/g visual hierarchy: "about 2 large elements" is not a complex-design cap | adopt | Fix the sentence in `hierarchy.md` Judgment aids (still a judgment aid, never a fail line). |
| `color-scheme: light dark` on `:root` is documented by MDN (Baseline Widely available since Jan 2022) | adopt | Drop the UNVERIFIED label in `consistency.md`/`frameworks.md`, cite MDN `color-scheme`. |
| Container queries are Baseline Widely available (since Feb 2023; caniuse 96.03%) | adopt | Close the "Baseline status not read" gap in `sources.md`; no rule changes, the skill already recommends them. |
| `user-scalable=no`/`maximum-scale` blocking zoom: web.dev states it | adopt | Replace "UNVERIFIED: inferred from SC 1.4.4" in `responsive.md` with the web.dev citation (keep WCAG 1.4.4 as the reason zoom matters). |
| Apple HIG Buttons: visionOS hit region is 60x60 pt (44x44 pt general rule) | ignore | The skill's fail line is WCAG 2.5.8; the HIG figure is only cited as a design target on web/iOS-style screens. |
| web.dev Focus names "Focus Appearance (Minimum)" | ignore | Old draft name; the skill's 2.4.13 AAA statement is correct. |
| M3 state layers and 48dp target | ignore | Still unreadable on the official page; the skill uses none and the NEVER rule already bars unverified figures as fail lines. Keep the "could not be read" note, update its date. |
| Model-validity pass | skipped | Not run (review only). Candidate rules that counter model habits, if the controller wants a probe: `role="status"` mounted empty, `response.ok` check before the error branch, Skeleton wrapping the real row, one filled button per view, never `pass` for an unobserved criterion. |

## Designer-flow trigger check (batch 22 background)

The `ui-ux-designer` agent preloads the skill (`skills: [ui-ux-principles]`), and a preloaded skill is injected in full whatever its `description` says. So delegation triggers (critique, "sanity-check", pushback with sources, user flow, onboarding, navigation, mockup, screenshot) are owned by the agent's description, which already lists them. The skill's description covers screen build, fix and review triggers in React, Vue, Svelte, HTML/CSS, MUI and Tailwind, "review this page" and "why does this feel off". Gaps for a stand-alone designer-flow use of the skill (optional, not required for the preload path):

- Input types the agent accepts (screenshot, mockup, URL) are not named in the skill description; Workflow step "Render" and the Review output already handle renders and screenshots (`settings.png@320px`). Optional: add "screenshot or mockup" to the description's "Use when" list.
- Workflow step 1 says the skill does not apply when no screen is built, changed or reviewed. The agent's "decision only" input (alternatives, no screen) is handled by the agent's own step 3 and Output override ("no screen, a decision only: skip it"), so there is no conflict while the agent drives; stand-alone, a pure design-decision or user-flow question is out of scope for the skill. That matches the agent's purpose split (the skill owns pass/fail rules and the table; the agent owns research checks, flow and decisions).
- No change needed to the marketplace entries: `agent-ui-ux-designer` already lists `./skills/ui-ux-principles` as a skill alongside the agent.
