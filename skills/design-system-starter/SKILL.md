---
name: design-system-starter
description: Create or evolve shared design systems with tokens, reusable component APIs, accessibility, theming, and documentation. Use when users ask for design tokens, a design system, component standards, a light/dark theme, or consistent UI rules. Not for one-off pages, ARIA how-to questions in an existing form, Storybook stories for existing components, SVG icon conversion/optimization, logos, or marketing copy.
license: MIT
metadata:
  version: "1.0.0"
  tags: "design-system, ui, components, design-tokens, accessibility, frontend"
---

# Design System Starter

Use this workflow to turn repeated product decisions into stable, adoptable shared contracts—not to redesign isolated screens.

## Workflow

When asked for a starter brand/system with little context or no repository evidence, state a reasonable labeled assumption and deliver a usable first-pass system rather than stopping to request files. Define reusable token categories explicitly—not just example values—including color, typography (font families, sizes, weights, line heights), and spacing (scale/steps); then assign values to tokens.

1. **Audit before standardizing.** Inventory repeated UI patterns across representative screens. Record frequency, user impact, accessibility failures, product exceptions, and owning teams. When auditing an existing UI, load `checklists/design-system-checklist.md`.
2. **Prioritize a pilot.** Select a high-frequency, high-failure-cost pattern with a real consuming screen. Avoid abstract primitive libraries without an immediate adopter. Capture current variants and migration constraints.
3. **Define semantic contracts.** Create primitive values, then semantic tokens (for example `text.primary`, `surface.raised`, `action.primary`). Components consume semantic roles, never raw palette values. A semantic role may map to different values by brand/theme only after validating every interaction state and contrast pair.
4. **Validate tokens before components.** Use `templates/design-tokens-template.json` for the output shape. Check alias resolution, cycles, missing targets, and contrast for each actual foreground/background pair: 4.5:1 normal text, 3:1 large text and essential UI boundaries. Fix failing pairs; do not infer accessibility from palette names.
5. **Derive a reusable component hierarchy from use.** Organize components into explicit levels: foundational primitives/tokens, composed patterns (for example form fields or cards built from primitives), and product-level modules where needed. Show how each level composes and which contracts it owns; avoid creating levels without a real reuse case. Preserve product invariants, use semantic props (`intent`, `size`, `disabled`) only where consumers need them, and provide composition/slots for genuine variation. Keep an escape hatch such as `className` or a documented slot, but do not expose internals that bypass accessibility or theme contracts. Load `references/component-examples.md` when implementing or reviewing component APIs.
6. **Choose a theme mechanism.** Default to semantic CSS custom properties switched by a `data-theme` attribute. Reuse the existing styling system where one is established; use Tailwind-specific variants or a ThemeProvider only when the project already depends on that mechanism or runtime theme objects are required. Load component examples for implementation detail.
7. **Pilot and revise.** Integrate into representative screens including the most constrained consumer. Check keyboard, focus, zoom, contrast, responsive behavior, and brand/theme variations. Revise the API before broader adoption if consumers need repeated workarounds.
8. **Adopt without breaking consumers.** Publish migration guidance and usage examples. Never silently change a token's meaning in a non-breaking release; deprecate old names, support a compatibility window, and state the removal version.

## Non-negotiable gotchas

- Never alias semantic roles across themes without checking every state (hover, focus, disabled, error, selected); a valid default color can fail in one theme or state.
- Never expose primitive palette values as product-facing component props without a migration plan; that freezes palette implementation into consumer APIs.
- Never change token meaning in a patch/minor release; consumers may depend on its visual contract even when types remain unchanged.
- Never encode state by color alone; pair it with text, iconography, or another perceivable cue.
- Use native interactive elements. A `<button>` needs `onClick`, not a duplicate Enter key handler; browsers already synthesize activation for Enter/Space.
- An `aria-modal="true"` dialog requires a tested dialog primitive or complete containment, background inertness, initial focus, Escape behavior, and focus restoration. Do not label a focusable box as an accessible modal.
- Ship a short component documentation guide with the starter: for each component, its purpose, props and variants, accessibility notes, and one usage example.

## Resources

- Token output: `templates/design-tokens-template.json`.
- When auditing an existing UI: `checklists/design-system-checklist.md`.
- When implementing component APIs, composition, or accessible interaction patterns: `references/component-examples.md`.
- Component source scaffold: `templates/component-template.tsx` (adapt semantic tokens and native semantics; do not copy blindly).
