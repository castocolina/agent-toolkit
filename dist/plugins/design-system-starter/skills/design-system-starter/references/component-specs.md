# Component specs

One row per component for workflow step 5: what each documentation guide entry must cover (variants and sizes, States line, accessibility). Rows are a checklist to select from, not a universal inventory: include only the components the scope line and the pilot need, and keep the names `intent`, `size`, `disabled` the same across them. Every state maps to its own semantic role (step 3). Code shapes live in `references/component-examples.md`.

Requirement sources, checked 2026-11-07: WCAG 2.2 (W3C Recommendation, 12 Dec 2024) https://www.w3.org/TR/WCAG22/ ; HTML Standard https://html.spec.whatwg.org/multipage/ ; WAI-ARIA Authoring Practices patterns https://www.w3.org/WAI/ARIA/apg/patterns/ (read the pattern page for the exact keyboard map before building a custom widget).

## Interactive target size

Every pointer target (buttons, icon buttons, checkbox and radio hit areas, pagination links, the badge remove button) meets WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA: at least 24x24 CSS px, unless spacing or an equivalent control exempts it (https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html). 44x44 CSS px is the Level AAA criterion, SC 2.5.5 Target Size (Enhanced) (https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html); use it as the default for touch-first products, and say which level the system targets in the scope line. Never describe 44x44 as the AA minimum.

The groups below are by shape; the level (primitive, composed pattern, product module) is derived from use (step 5), so a navigation bar or table may be a product module in one system and a composed pattern in another.

## Primitives

| Component | Variants and sizes | States | Accessibility |
| --- | --- | --- | --- |
| Button | `intent`: primary, secondary, outline, ghost, danger; `size`: sm, md, lg; optional left and right icon; `fullWidth` boolean (a prop, since there is no root `className`) | default, hover, active, focus-visible, disabled, loading | Native `<button>` with `type` defaulting to `button`; icon-only buttons need an accessible name; loading and disabled keep focus via `aria-disabled` and `aria-busy` (see `templates/component-template.tsx`, which ships the minimal subset `intent` primary, secondary, danger and `size` sm, md; add outline, ghost, `lg`, icons and `fullWidth` additively when the scope needs them, keeping the defaults `primary` and `md` unchanged) |
| Input | `type`: text, email, password, number, search (use the native type and `autocomplete`); `size`: sm, md, lg; optional left and right icon | default, focus, error, disabled | Visible `<label>`; helper and error text linked with `aria-describedby`; error sets `aria-invalid` and shows message text, never a red border alone; icons are decorative (`aria-hidden="true"`) |
| Checkbox and Radio | `size`: sm, md, lg | default, checked, indeterminate (checkbox only), disabled | Native `<input>` with an associated `<label>` (the label is part of the hit area); radios share a `name` inside `<fieldset>` and `<legend>`; set `indeterminate` through the DOM property, there is no HTML attribute |
| Select | single, multi, searchable | default, open, disabled | Prefer native `<select>`. A custom control follows the APG combobox pattern: `role="combobox"`, `aria-expanded`, `aria-controls` the listbox, `aria-activedescendant` on the active `role="option"`, Arrow keys move, Enter selects, Escape closes; multi-select adds `aria-multiselectable` on the listbox |
| Badge | `intent`: default, success, warning, error, info; `size`: sm, md, lg; removable | default, removable | Status is text or an icon plus text, never color alone (WCAG SC 1.4.1); the remove control is a native button named "Remove <label>" |
| Avatar | `size`: xs, sm, md, lg, xl | image, fallback (initials or a default icon), with status | `alt` is the person's name, or empty when the name is shown next to it; a status dot (online, offline) needs a visually hidden text alternative, not color alone |
| Icon | `size`: 16, 20, 24, 32 px; one icon set per system (a project decision) | none | Decorative icons use `aria-hidden="true"`; an icon that is the only content of a control gives the control the name (`aria-label` or visually hidden text), not the icon |

## Composed patterns

| Component | Variants and sizes | States | Accessibility |
| --- | --- | --- | --- |
| Form field | label, control, hint, error | default, error, disabled, required | See the FormField example: `controlId`, `aria-describedby`, `aria-invalid`, "(required)" text |
| Search bar | input plus submit button or icon button | empty, filled, submitting | `<form role="search">` with `type="search"`; Enter submits natively; the clear button is a native button named "Clear search" that returns focus to the input |
| Card | `variant`: default, outlined, elevated; header, body, footer slots | default, hover and focus only if interactive | Compound example in `references/component-examples.md`; one link per card (stretch it from the title), never an interactive element nested inside a `<button>` or another link (SKILL.md nesting gotcha) |
| Alert and Toast | `intent`: success, warning, error, info; dismissible; optional icon and action | visible, dismissed | Icon plus text, not color alone; use `role="status"` (polite) for success and info and `role="alert"` for errors, with the live region present in the DOM before its text changes; a dismiss button named "Dismiss"; do not auto-dismiss a message that carries an action (WCAG SC 2.2.1 Timing Adjustable) |
| Navigation bar | logo, links, actions (sign in, sign up), nested dropdown | default, menu open (small screens), link current | `<nav aria-label>` with a list of links; `aria-current="page"` on the current link; a menu button with `aria-expanded` and `aria-controls`; a dropdown is a disclosure button over a list of links, not `role="menu"`; Escape closes it and returns focus to its button |
| Modal and Dialog | `size`: sm, md, lg, full | closed, open | Build on native `<dialog>` with `showModal()` (SKILL.md gotcha); overlay is `::backdrop`; Escape and a visible close button both close it; the dialog is labelled by its heading; focus returns to the opener. Example in `references/component-examples.md`; behavior per MDN https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog |
| Table | sortable columns, selectable rows, responsive | default, sorted ascending or descending, row selected | `<table>` with `<caption>`, `<th scope>`; a sortable header holds a button and `aria-sort` sits on the one sorted `<th>`; each row checkbox is named "Select <row>"; on narrow screens scroll inside a wrapper with `tabindex="0"`, `role="region"` and a label so keyboard users can scroll, instead of restyling the table into blocks that lose its semantics |
| Pagination | page numbers (current and neighbors), previous and next, first and last, page size | current page, first or last page reached | `<nav aria-label="Pagination">` with a list; the current page has `aria-current="page"`; previous and next have text names ("Previous page"); a disabled end uses `aria-disabled` so focus is not lost; the page-size select has a visible label |

## Layout primitives

Layout components are the one place props map to spacing tokens (for example `gap="4"` resolves to `spacing.scale.4`); they consume spacing roles only and own no color.

| Pattern | Spec |
| --- | --- |
| Grid | CSS grid with a token gap; a 12-column grid only when designs need it, otherwise `repeat(auto-fit, minmax(<min>, 1fr))` |
| Container | Max-inline-size plus inline padding from the spacing scale, centered; the max width is a project decision |
| Stack | Vertical rhythm: flex column with a token `gap`, no per-child margins |
| Cluster | Horizontal wrap: flex with `flex-wrap`, a token `gap` and an alignment prop (toolbar buttons, tag lists) |
| Sidebar layout | Fixed-width sidebar track plus a fluid main track; the sidebar collapses above the main content below a breakpoint; sidebar is an `<aside>` or `<nav>` with a label and main content is `<main>` |

## Feedback patterns

| State | Spec |
| --- | --- |
| Loading | Skeleton when the layout is known, spinner for short unknown waits, progress bar (`role="progressbar"` with `aria-valuenow`) when the percentage is known; reserve the final size to avoid layout shift; mark the region `aria-busy="true"` while loading and stop animation under `prefers-reduced-motion` |
| Empty | Say what is empty and why, and offer one next action (a call to action); never reuse the error styling |
| Error | Page level (404, 500): plain language, what happened, one recovery action; inline: `role="alert"` message next to the control, with `aria-invalid`; always an icon or text next to color |
| Success confirmation | Confirm after the action in a `role="status"` region or inline message; offer undo when the action is reversible; keep the message visible long enough to read |
