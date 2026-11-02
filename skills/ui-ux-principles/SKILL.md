---
name: ui-ux-principles
description: "Use when building, changing, or reviewing any UI screen or component in React, Vue, Svelte, HTML/CSS, MUI, or Tailwind: skeleton vs spinner loading, empty and error states, mobile-first responsive layout, visual hierarchy, design tokens, dark mode, WCAG contrast, focus rings, tap targets, aria-label on icon buttons, and hover/focus-visible/active/disabled states. Trigger even when the user only says review this page, make this look polished, why does this feel off, or fix the layout, without naming UX. Not for backend or API work, copywriting, brand or logo design, choosing or scaffolding a design-system product, or implementing the MUI theme API and Grid migration (use the mui skill)."
---

# UI/UX principles

Eight rules decide whether a screen is done. Each `## <id>` section is the whole pass line for that rule plus the trap that breaks it; nothing else fails a rule.

## Workflow

1. No screen is built, changed or reviewed (backend, API, data pipeline, copy only): say this skill does not apply and do the task without it.
2. Find the theme the repo already has (CSS custom properties, MUI `createTheme`, Tailwind theme) before writing a style. Every new value goes there.
3. Write the pending, empty, error and success branches before visual polish: they change the layout the polish sits on.
4. Build or fix: apply the rules the change touches. Three block every hand-over because the code alone proves them: an accessible name on each control, a keyboard path to each action, no new color, type or spacing literal. The rest need a render; say which ones you did not render.
5. Review or verdict: emit the table under Review output. Never emit it on a build.
6. After an edit, re-check each failed rule against the code or the render, not against your intent.

## loading

**Rule.** A pending read shows nothing under about 1 s, a skeleton of the final layout from about 1 to 10 s (a spinner only inside one module), and progress with cancel beyond that. A pending submit disables its button at once and shows the indicator inside it, whatever the wait: the guard is against a double submit. CLS stays at 0.1 or less. With only code in hand the wait is unknown: decide by scope, not by guessing latency (`references/rules/loading.md`).
**Trap.** One page-level spinner standing in for several regions, or skeleton blocks sized differently from the content, so the page jumps.
Detail: `references/rules/loading.md`

## responsive

**Rule.** The base style is the small layout; breakpoints sit where this content breaks. Verify at 360, 768, 1280 and 1920 px (a test matrix, not the breakpoint list): no page-level horizontal scroll, primary action reachable.
**Trap.** Fixed container widths, or `overflow-x: auto` on the page to hide them. A table, map or code block may scroll inside its own container.
Detail: `references/rules/responsive.md`

## hierarchy

**Rule.** At most one filled button per view; outlined and text buttons never count. When two actions finish the same job, fill the likelier one and outline the other; on a tie, fill the one Enter triggers (the form submit), else the first in reading order. A destructive action is never filled. An open dialog is its own view.
**Trap.** A second filled button, even for the same job; a filled button repeated on every row or card; a destructive action styled as primary.
Detail: `references/rules/hierarchy.md`

## tokens

**Rule.** Components read semantic roles (`color-danger`, `space-4`) from the theme the repo has. A missing role is added to that theme.
**Trap.** A hex or rgb color, or a raw font size, spacing, radius or shadow, in a component; a value name (`blue-500`) used as a role. A fixed container width is a responsive defect, not this one. No theme in the repo: flag the missing role and stop.
Detail: `references/rules/tokens.md`

## consistency

**Rule.** One shared component per role, varied by props. Dark mode is a second value set on the same tokens, switched at the root.
**Trap.** A one-off styled control; a `<style>` element inside a component, which restyles every matching element in the document; `dark:` patches on components while the tokens stay light-only.
Detail: `references/rules/consistency.md`

## a11y

**Rule.** Every control has an accessible name that contains its visible text and is keyboard-operable. Text 4.5:1; non-text UI 3:1 (input borders, icons, focus rings) in every theme; pointer targets 24 by 24 CSS px. 44 px is a design target, not the fail line.
**Trap.** An `aria-label` that drops the visible word (SC 2.5.3); a light-gray input border (`#ccc` on white is 1.6:1); contrast checked in light mode only.
Detail: `references/rules/a11y.md`

## states

**Rule.** Once the request resolves: empty renders only on a successful zero-item response and says why plus the next action; error names the problem, keeps the input and offers a retry; success is confirmed near the action and announced (`role="status"`).
**Trap.** A fetch with no error branch, so a failure renders as the empty list; "No results" while the request is pending; a delete that changes nothing on screen.
Detail: `references/rules/states.md`

## interaction

**Rule.** The focus ring sits on `:focus-visible`, so a mouse click does not show it. Custom controls have hover and pressed states; hover carries nothing a touch user needs.
**Trap.** `outline: none` with no replacement, or a control that looks disabled and still submits. Imperfect disabled colors are not a fail: no fetched source sets a number.
Detail: `references/rules/interaction.md`

## Review output

Exactly this header, then eight rows in this order: loading, responsive, hierarchy, tokens, consistency, a11y, states, interaction. After the table, one summary line. No other prose unless the user also asks for an explanation or a fix; an edit they ask for comes after the summary line.

| rule | pass/fail/na | evidence file:line | fix |
|------|--------------|--------------------|-----|

- **Verdict cell**: exactly `pass`, `fail` or `na`.
  - `fail`: the code breaks that rule's Rule line in `SKILL.md` or shows its Trap.
  - `pass`: the rule applies and nothing breaks it.
  - `na`: the file holds nothing the rule applies to (no request for loading or states, no button for hierarchy).
- **Evidence cell**: `file:line` or `file:start-end` of the code the verdict rests on, for a pass too. An `na` names what is absent (`about.tsx: no request`). Append `not rendered` when the verdict needs a render you did not do (widths, computed contrast, the focus ring).
- **Fix cell**: one imperative change for a `fail`; `-` for `pass` and `na`.

### Mandatory versus judgment

Every row is mandatory and is decided by its Rule line and Trap alone, hierarchy included: two filled buttons fail even when the screen looks fine. Judgment never moves a verdict: grouping, spacing rhythm, type-scale count, the squint test and wording stay out of the table. Mention them after the summary line only when the user asks for polish notes.

### One defect, one row

A defect that touches two rules is reported once, in the row below, so the table does not double-count it.

| defect | row |
|--------|-----|
| fixed container width | responsive, not tokens |
| `outline: none`, missing focus ring | interaction, not a11y |
| icon-only control without a name | a11y, not hierarchy |
| submit with no pending state | loading, not states |
| color, type or spacing literal | tokens; the contrast of that color is a separate a11y defect |
| `<style>` element or one-off styled control | consistency |
| no empty, error or success branch | states |

### Missing input

The file is not provided and nothing is rendered: all eight rows are `na`, each evidence cell is `<file> not provided`, no line numbers, and the summary line asks for the file or a render.

## NEVER

- NEVER add a second theme, token file or color to pass a rule: two sources of truth drift apart on the next rebrand.
- NEVER invent a line number, width or screenshot for a file or render you do not have: the evidence is the verdict.
- NEVER use a figure marked UNVERIFIED in `references/sources.md` as a fail line: nothing read supports it.

## References

- `references/rules/<id>.md`: load the file for each rule whose fix you are writing or whose verdict turns on an exception there; do not load it for a rule the Rule line already decides.
- `references/frameworks.md`: load when the changed files use MUI, Tailwind or plain CSS and you need the construct; do not load it for Vue, Svelte or any other framework.
- `references/sources.md`: load only when a rule file and this file disagree, or before using a figure as a fail line; a fetched figure wins over both.
