---
name: ui-ux-principles
description: "Apply eight pass/fail UI/UX rules (loading, responsive, hierarchy, tokens, consistency, accessibility, states, interaction) when building or changing a screen, and return a rule | pass/fail/na | evidence | fix table on review. Use when building, fixing or reviewing any UI screen or component in React, Vue, Svelte, HTML/CSS, MUI or Tailwind: loading skeletons, empty and error states, mobile layout, button emphasis, hard-coded colors, theming and dark-mode setup (adding dark mode or a theme switch without per-component overrides), WCAG contrast, focus rings, tap targets. Trigger even on 'review this page', 'make this look polished', 'why does this feel off' or 'fix the layout'. Not for backend or API work, copywriting, brand or logo design, scaffolding a design system (design-system-starter), or the MUI theme API and Grid migration (mui)."
---

# UI/UX principles

Eight rules decide whether a screen is done. Each `## <id>` section is the whole pass line (Rule) plus the defect that breaks it and why (Trap); nothing else fails a rule. Gotchas say how framework code reads against them.

## Workflow

1. No screen is built, changed or reviewed (backend, API, data pipeline, copy only): say this skill does not apply and do the task without it.
2. Before you decide, ask:
   - Actions: what is the user here to finish, which control finishes it, and what does a wrong press cost? The finishing control gets the one fill (hierarchy); a press that is costly to undo gets a confirm or undo (states) and never the fill. When the request does not say, infer the task from the screen's name and data and state the guess in one line.
   - Layout: which content breaks first at 320 px, and does it reflow or get its own container scroll (responsive)?
   - Requests: which responses can it return (zero items, 4xx, 5xx, network failure), and what does each one render (states)?
3. Take the branch the request names:
   - **Build or fix** (a build or fix request, or the fix half of review-and-fix): Build steps. Exit: the code, then the hand-over; never the review table, even when you checked every rule.
   - **Review** (a review, a verdict, or a diagnostic question such as "why does this feel off"): Review steps. Exit: the table and one summary line; for a diagnostic question the summary line leads with the answer.
   - **Review and fix**: Review steps, then Build steps on the failed rows. Exit: the table, the summary line, the code, the hand-over.
4. After an edit, re-check each failed rule against the code or the render, not against your intent: the intent is what produced the defect.

### Build steps

1. Find the theme (CSS custom properties, MUI `createTheme`, Tailwind theme; their defaults count) before the first value, so none starts as a literal.
2. When the component starts or consumes a request, write its pending, empty, error and success branches before polish: they change the layout the polish sits on. With no request, skip them and build only the local states the task needs.
3. Then fills (count every button you output, dialogs included), shared components and fluid widths per hierarchy, consistency and responsive, and a name plus keyboard path per control (a11y, interaction: source alone proves both, so they block the hand-over).
4. Render (below) only a layout or theme change to a full screen; a small component edit (one control, a color, a label) lists its gaps under `unverified` instead.
5. Hand-over, three lines:
   ```
   changed: <file>, <file>
   rules: <rule> <what the change does for it>; <rule> <...>
   unverified: needs <observation>; needs <observation>
   ```
   `rules` names only the rules the change touches (a created `:root` theme block is told here, under tokens); `unverified` lists every check you did not render or measure, or `none`, because an unlisted gap reads as a pass.

### Review steps

1. Open the stylesheets and shared components the target imports, resolve its theme references, and trace each request to its branches.
2. If the app runs, render (below) for the rows the source leaves `na`.
3. Emit the table under Review output.

### Render

Default: the app's dev server plus Playwright or the harness browser tool at 320 CSS px (the reflow check, SC 1.4.10) and at 360, 768, 1280 and 1920 px (layout checks); one Tab press to expose the focus ring; colors read from computed styles; a repeat in the dark theme when the screen ships one. CLS is the value a Lighthouse performance run reports for the screen; without Lighthouse it stays `unverified: needs CLS measurement`. Fallback: no runnable app (no dev script, a failing build, a lone file, a session without a browser): render nothing and keep each check that needed it `unverified`.

## loading

**Rule.**
1. Scope picks the indicator, because code never shows the wait: a page or several regions get a skeleton of the final layout, a spinner only inside one module, and an operation known to run past about 10 s (upload, export) gets progress with cancel. A measured wait under about 1 s needs none.
2. A pending submit is disabled at once; the in-button indicator may appear after about 1 s.
3. CLS stays at 0.1 or less, as Lighthouse reports it (Render); code and screenshots do not show it.

**Trap.** One page-level spinner standing in for several regions, or skeleton blocks sized differently from the content: the page jumps when data lands. A submit left enabled while pending: the second click sends a second request.
Detail: `references/rules/loading.md`

## responsive

**Rule.** Reflow at 320 CSS px (SC 1.4.10), with layout checks at 360, 768, 1280 and 1920 px (a test matrix, not the breakpoint list; breakpoints go where the content breaks): no page-level horizontal scroll and the primary action reachable at any of them. A table, map or code block may scroll inside its own container. The whole verdict rule:
1. `fail` from source, outside a scroll container: a declared `min-width` over 320 px (`minWidth: 960`, `48rem`) that no breakpoint lowers, since `max-width` never caps a `min-width` (`min-width: 960px; max-width: 100%` fails); or a declared `width` over 320 px (`width: 1200px`) with neither a `max-width` cap nor a breakpoint change, on an element that cannot shrink: not a flex item (the target's root counts as not one), or a flex item with `flex-shrink: 0` or `flex: none`, or with a `min-width` at least that width. A shrinkable flex item's width is rule 3.
2. `fail` or `pass` from renders: a render at any test width that shows the sideways scroll or an unreachable primary action fails; renders at 320 px and the four layout widths that show neither pass.
3. Everything else is `na` with `unverified: needs 320 px render`, including any sum of widths, padding, borders, margins or flex items, `nowrap` and intrinsic sizing: source alone never passes this row.

**Trap.** An uncapped fixed container width: below it the content is cut off or behind a sideways scroll users miss; `overflow-x: auto` on the page only moves that scroll, it does not remove it.
Detail: `references/rules/responsive.md`

## hierarchy

**Rule.** Default: at most one filled button per view; outlined and text buttons never count. A view is the page, an open dialog, or a bounded panel for an independent task (Sign in beside Create account). When two actions finish the same job, fill the likelier one and outline the other; on a tie, fill the one Enter triggers (the form submit), else the first in reading order, unless the user or the product brief names the preferred action. A destructive action is never filled, and a confirm dialog for one fills nothing: the destructive confirm outlined in the danger role, the safe action (Cancel, Keep) as text. Two exceptions, each cited in the evidence: the repo's design system documents its own emphasis rule; or a list of equal-priority independent product choices (cards rendered from one list, no recommended item, nothing else filled in the view) repeats the same filled action.
**Trap.** A second filled button in one view, even for the same job (Pay now beside Pay on invoice): the eye has no single place to land. A filled action on every record row (Edit per order): N primaries for one task, not product choices. A destructive action filled, a dialog confirm included: the fill invites the reflex press.
Detail: `references/rules/hierarchy.md`

## tokens

**Rule.** Pass: no color, type, spacing, radius or shadow literal in a component; each reads a semantic role (`color-danger`, `space-4`) from the repo's theme, and a missing role is added there. No theme at all: on a review, a literal fails tokens, the evidence names it and the fix is "add a theme role"; on a build, create one `:root` custom-property block for the new roles, tell the user, and continue.
**Trap.** A value name (`blue-500`) used as a role, or a literal that looks like a token (Gotchas): each is a value the next rebrand and the dark theme miss. A width is a responsive matter, not this one.
Detail: `references/rules/tokens.md`

## consistency

**Rule.** Pass: each control is the shared component for its role, and dark mode switches token values at the root.
**Trap.** A raw `<style>` element in React or the DOM, or a Vue `<style>` without `scoped`: it restyles every matching element in the document (Vue `<style scoped>`, Svelte component styles and CSS modules pass unless a selector escapes with `:global(...)`). `dark:` patches on components while the tokens stay light-only: every new component ships light-only. A one-off styled control drifts from the shared one on the next change.
Detail: `references/rules/consistency.md`

## a11y

**Rule.** Fail: a control with no accessible name (icon-only included) or a name that drops its visible word (SC 2.5.3); an action with no keyboard path; contrast under WCAG AA in any shipped theme, non-text included (3:1 for input borders, icons, focus rings); a pointer target under 24 by 24 CSS px (44 px is a design target, not the fail line).
**Trap.** An `aria-label` that drops the visible word (SC 2.5.3): speech users say the word they see and nothing matches. A light-gray input border (`#ccc` on white is 1.6:1): on an unfilled field the border is the only thing that marks it. Contrast checked in light mode only: inverted dark values often drop borders and focus rings under 3:1.
Detail: `references/rules/a11y.md`

## states

**Rule.** Once the request resolves: empty renders only on a successful zero-item response and says why plus the next action; error names the problem, keeps the input and offers a retry that clears the error before it refetches (or the error stays over fresh data); success is confirmed near the action and announced (`role="status"`); a destructive or costly-to-undo action gets a confirm step or an undo.
**Trap.** A fetch with no error branch, or no `response.ok` check (Gotchas): a failure renders as the empty list. "No results" while the request is pending: it tells the user their data is gone. A delete that changes nothing on screen: users press it again. A `role="status"` element mounted together with its message: screen readers announce only changes to a live region they already know, so mount it empty on the first render and put only post-action announcements in it ("Order deleted"); loading text belongs elsewhere (`aria-busy` on the loading region), or the region announces it and starts non-empty.
Detail: `references/rules/states.md`

## interaction

**Rule.** Pass: a `:focus-visible` ring on every focusable control, never suppressed for pointer focus; hover and pressed states on custom controls; nothing reachable only by hover.
**Trap.** Focus indication removed with no replacement: keyboard users lose their place. `outline: none` beside a `:focus-visible` or `.Mui-focusVisible` style that draws a ring counts as replaced; for MUI controls see Gotchas. A hover-only reveal (a row action, a tooltip): touch users never see it (Gotchas). A control that looks disabled and still submits. Imperfect disabled colors are not a fail: no fetched source sets a number.
Detail: `references/rules/interaction.md`

## Review output

Exactly one table, with exactly this header, then eight rows in this order: loading, responsive, hierarchy, tokens, consistency, a11y, states, interaction. Put everything in it: no second table, list or per-defect breakdown. After the table, one summary line. No other prose unless the user also asks for an explanation or a fix; an edit they ask for comes after the summary line.

| rule | pass/fail/na | evidence file:line | fix |
|------|--------------|--------------------|-----|

### Verdicts

One test decides every row, whatever the input (source, render, both, or a running app):

1. `fail`: the input proves a break of the Rule line or a Trap. One proven break decides the row, whatever else is missing.
2. `pass`: every criterion of the Rule line that applies is established by the input (see NEVER).
3. `na`, either way: the rule has nothing to apply to (no request for loading or states, no button for hierarchy; evidence `about.tsx:1-40 — no request`, citing the range you inspected), or a criterion is neither broken nor established (evidence `about.tsx:12 — unverified: needs <missing observation>`, or the inspected range when no single line applies, such as `needs render at 320 px`, `needs CLS measurement`, `needs source`, `needs dark-theme colors`).

The input is the target and the files it imports; a parent page you were not given is outside it, not a missing observation.

| criterion | established by |
|-----------|----------------|
| names, keyboard path, literals, request branches, button variants, style scoping, `:focus-visible`, hover and pressed states | source; a render can show these broken but cannot establish them |
| widths (responsive) | renders at 320 px and the layout widths; source can only fail it (responsive rule 1) |
| contrast | both colors in every theme the screen ships: literals or resolved theme references in source, or color values read from a render; a role name alone does not give its value |
| target size | explicit sizes in source, or a measured render |
| CLS, real wait time | a measurement only (Lighthouse for CLS) |
| one filled button per view | source, or renders of every view (an unopened dialog is unobserved) |

### Cells

- **Verdict**: exactly `pass`, `fail` or `na`.
- **Evidence**, for every verdict: the location, then ` — ` and the observed fact that decides the row (`dashboard.tsx:24 — width: 1200, uncapped`, `dashboard.tsx:31 — icon-only IconButton, no accessible name`). Location forms:
  - source: `file:line` or `file:start-end`; an absence cites the range you inspected (`ProfileCard.vue:1-18 — no request`), so every source cell starts with the file name, a colon and a line;
  - render (screenshots, viewport notes, a running app): `<render>@<width>px: <region>`, such as `settings.png@320px: toolbar`, no line numbers;
  - both: `file:line`, plus the render reference when the render decided the row;
  - neither: `<file> not provided` in every row, all eight `na`, and the summary line asks for the file or a render.
- **Fix**: the change only, one imperative per defect for a `fail` (the fact belongs in the evidence); `-` for `pass` and `na`.
- **A direct question about one rule** ("is that a responsive problem?") is answered in that row's evidence cell and the summary line, not in extra prose.
- **Several defects for one rule**: every `file:line — fact` in the one evidence cell, separated by `; ` (prefix each with its file when there are several files or renders), and one imperative fix per defect in the fix cell, in the same order and separated the same way.

### Mandatory versus judgment

Every row is mandatory and is decided by its Rule line and Trap alone, including the exceptions they name: two filled buttons in one view fail even when the screen looks fine. Judgment never moves a verdict: grouping, spacing rhythm, type-scale count, the squint test and wording stay out of the table. Mention them after the summary line only when the user asks for polish notes.

### One defect, one row

A defect that touches two rules is reported once, in the row below, so the table does not double-count it.

| defect | row |
|--------|-----|
| uncapped fixed container width | responsive, not tokens |
| `outline: none`, missing focus ring | interaction; a ring that exists but sits under 3:1 is a11y |
| icon-only control without a name | a11y, not hierarchy |
| submit with no pending state | loading, not states |
| color, type or spacing literal | tokens; the contrast of that color is a separate a11y defect |
| global `<style>` (not compiler-scoped), one-off styled control, `dark:` patches | consistency |
| no empty, error or success branch | states |

## Gotchas

- `fetch` resolves on 404 and 500: only a `response.ok` check (throw inside the chain) reaches the error branch; `.finally(() => setLoading(false))` alone renders a failure as the empty list.
- MUI `Button` with no `variant` is `text` and never counts as filled; a custom `.btn` with a background color is filled whatever its name.
- MUI `sx`: a string (`p: '9px'`, `outline: '2px solid'`) is a literal; a number on a spacing key (`p: 2`) multiplies `theme.spacing` and passes. A custom focus ring reads the theme: `outlineStyle: 'solid', outlineWidth: (t) => t.spacing(0.25), outlineColor: (t) => t.palette.primary.main`.
- MUI `Button` and `IconButton` with default props and the default theme ship a focus-visible ripple, so in source they establish the interaction ring; add none. A direct `ButtonBase`, a custom wrapper, or a theme that overrides the focusVisible styling establishes nothing: interaction is `na` unless a ring is visible in source. They lose it only with `disableRipple` (MUI: "without a ripple there is no styling for :focus-visible by default"), `disableFocusRipple`, or an `sx` override of `'&.Mui-focusVisible'` that hides it; each fails unless a ring is styled on `.Mui-focusVisible` or `focusVisibleClassName`. An `sx` `outline: none` on them removes nothing: ButtonBase draws no outline.
- Tokens exempt `0`, percentages, `auto`, `inherit`, `currentColor` and `transparent`: they carry no brand value, so a rebrand or dark theme never changes them.
- Tailwind arbitrary values (`bg-[#3b82f6]`, `p-[9px]`) are literals, not utilities.
- Tailwind `hover:` is wrapped in `@media (hover: hover)`, so a hover reveal never fires on touch.
- MUI `Skeleton` has no ARIA and is not focusable: put `aria-busy` on the loading region, or a screen reader hears nothing.

### Patterns

The three patterns models miss, as fragments of a list built to the loading and states rules:

```tsx
const retry = () => { setStatus('loading'); load(); };   // clears the error before refetching
<Typography role="status">{notice}</Typography>          // mounted empty; only post-action text ("Order deleted")
<Skeleton variant="rounded"><OrderRow order={PLACEHOLDER} /></Skeleton>  // wraps the real row, so the geometry matches
```

## NEVER

- NEVER add a second theme, token file or color to pass a rule: two sources of truth drift apart on the next rebrand.
- NEVER invent a line number, width, measurement or screenshot for a file or render you do not have: the evidence is the verdict.
- NEVER mark a row pass because you saw no defect: an unobserved criterion (a width, dark-theme contrast, CLS) is `na` with `unverified: needs <observation>`, because a silent pass ships the defect.
- NEVER use a figure marked UNVERIFIED in `references/sources.md` as a fail line: nothing read supports it.

## References

- `references/rules/<id>.md`: load the file for each rule whose fix you are writing or whose verdict turns on an exception there (2.5.8 target exceptions, container queries, worked hierarchy calls); do not load it for a rule the Rule line already decides.
- `references/frameworks.md`: load by styling stack, whatever the host framework: when the target is styled with MUI, Tailwind or plain CSS (a Vue or Svelte file styled with Tailwind counts) and you need the construct; do not load it for host-framework questions (Vue reactivity, Svelte stores) or other styling stacks.
- `references/sources.md`: load only when a rule file and this file disagree, or before using a figure as a fail line; a fetched figure wins over both. Do not load it for an ordinary review or build.
