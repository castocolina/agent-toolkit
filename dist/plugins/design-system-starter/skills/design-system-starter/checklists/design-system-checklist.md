# Design System Checklist

Audit an existing UI or gate a release. Mark every item `pass`, `fail` or `N/A: <reason>`; an unexplained N/A counts as a fail. Component inventories, publication platforms (npm, Figma, Storybook) and numeric budgets are project decisions: record the chosen ones in the scope line, then audit against those, not against a universal list.

**Scope:** pilot pattern and consuming screen ____ ; themes/brands ____ ; frameworks ____ ; distribution channels ____

---

## Audit an existing UI

- [ ] **Value inventory**: every hardcoded color, size, spacing and radius in the audited screens is listed with its file and count, and mapped to an existing or proposed token (or marked as a deliberate exception with an owner).
- [ ] **Pattern inventory**: each repeated pattern lists its variants, consuming screens and owning team, so the pilot choice is evidence-based.
- [ ] **Accessibility failures**: contrast failures (measured pair and ratio), controls without an accessible name (icon-only buttons), mouse-only interactions and color-only status are listed per pattern.
- [ ] **Migration constraints**: which consumers cannot take a breaking change, and when each can.

## Tokens

- [ ] Every alias resolves; no cycles; no reference to a missing path.
- [ ] Components and product code reference semantic roles only; no primitive palette name reaches a component prop.
- [ ] Every declared foreground/background pair passes in every theme and state (SKILL.md step 4), including hover, focus, disabled, error and selected.
- [ ] Each theme or brand file defines the same semantic paths; a path missing from one theme fails.

## Components (for the components in scope)

- [ ] Native element for the role (`<button>`, `<a href>`, `<input>`), with children that fit that element's own HTML content model (SKILL.md nesting gotcha).
- [ ] Keyboard operation, visible focus, accessible name, and every documented state rendered.
- [ ] Props documented with types, defaults and states, not by example alone.
- [ ] Components that own focus or color roles take no root `className`/`style`; layout goes on an outer wrapper or a documented slot.

## Release gate

- [ ] The pilot screen ships on the system with no consumer workaround left in place (or the API was revised first).
- [ ] Each distribution channel in scope builds from the same token source.
- [ ] Changed token meanings ship only in a major release; deprecated names keep working for the stated compatibility window, with the removal version announced.
- [ ] Migration notes list every renamed or removed token and prop with its replacement.

---

**Checklist Version**: 1.0.0
**Skill**: design-system-starter v1.0.0
**Last Updated**: 2025-10-31
