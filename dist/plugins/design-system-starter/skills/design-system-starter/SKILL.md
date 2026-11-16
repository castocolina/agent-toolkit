---
name: design-system-starter
description: Set up or evolve a shared design system - semantic design tokens (DTCG .tokens.json, CSS custom properties), light/dark token themes, reusable component APIs (atoms, molecules, organisms), contrast-checked token pairs, and versioned migration off scattered styles. Use when asked to create a design system or token file, convert raw values into semantic tokens, standardize UI across apps or teams, define component library conventions, or version and deprecate shared tokens and components, even when the user only says the screens look inconsistent or all over the place. Not for reviewing or fixing one screen or component against UI rules (ui-ux-principles), one-off pages, ARIA how-to questions in an existing form, Storybook stories for existing components, SVG icon optimization, logos, or marketing copy.
license: MIT
metadata:
  version: "1.0.0"
  tags: "design-system, ui, components, design-tokens, accessibility, frontend"
---

# Design System Starter

Turn repeated product decisions into stable, adoptable shared contracts, not a redesign of isolated screens.

## Workflow

With little context or no repository, state labeled assumptions and deliver a first pass instead of asking for files. Size the deliverable to the request:
- **Complete starter** ("give us a design system"): a token file with named color, typography and spacing roles (roles first, values second), theme mappings, the contrast table (step 4), a component list by level whose product level names one or two candidates marked provisional, and a component documentation guide giving every component its props with defaults, a States line (`States: none (layout only)` counts) and accessibility notes.
- **Token-only work** (a token file, a theme, a conversion): the token file, its theme mappings and the contrast table (step 4). Run steps 3, 4 and 6 (step 1 too when the values come from an existing UI); skip the pilot and component steps 2, 5 and 7. Run step 8's token rules whenever shared tokens are renamed, deprecated, published or change meaning.
- **One app, no repeated pattern yet, and no request for a full starter**: tokens plus two or three primitives; defer the hierarchy (step 5) and versioning (step 8) until a second consumer exists.

1. **Audit before standardizing.** Existing UI: load `checklists/design-system-checklist.md` and fill its audit section. Greenfield: skip the audit; in step 2 the pilot is the first screen being built, or a sample page that renders every semantic role in each theme when no screen exists yet.
2. **Pick one pilot.** Choose a high-frequency, high-failure-cost pattern with a real consuming screen. Tie-breaker: the pattern whose consuming screen is already scheduled to change this cycle, so adoption is measurable. No abstract primitive library without an adopter.
3. **Define semantic contracts.** Primitive values, then semantic roles (`text.primary`, `surface.raised`, `action.hover`); components consume roles only. Every interaction state gets its own role, so each state pair can be checked. Each theme or brand is a second value set on the same semantic paths, never a parallel set of names.
4. **Validate tokens before components (blocking).** With a shell, load `references/token-checks.md` and run its alias resolver and contrast script (it also covers translucent and wide-gamut colors). Without one, trace aliases and compute ratios by hand.
   - Every alias resolves. A cycle or a missing target is an error: name the tokens involved and fix it before any component work.
   - Contrast, per theme and state: one table row per foreground/background pair with both role names, the resolved hex of each side, the ratio and pass/fail. Label a script result "measured"; without a tool, work the ratio out with the WCAG 2.x relative-luminance formula and label it "computed by hand". Never give a role-only row or an "expected" ratio.
   - Thresholds: 4.5:1 normal text, 3:1 large text and essential UI boundaries (input borders, focus rings). Report each failing pair with its replacement value; never infer pass from palette names.
   - Write tokens in the shape of `templates/design-tokens-template.json`.
5. **Derive the component hierarchy from use.** Levels: primitives, composed patterns (form field, card), product modules; state which contracts each level owns.
   - Promotion: before moving a pattern a level up or into the shared library, ask whether two consumers already use it with the same props. If not, keep it local to the pilot; product candidates stay provisional until then.
   - Props: semantic props (`intent`, `size`, `disabled`) only where consumers need them; slots for genuine variation; no root `className` or `style` on components that own focus or color roles (a consumer class can override them); layout goes on an outer wrapper or a documented slot.
   - Scaffold: for component APIs in any framework, load `references/component-examples.md` (its CSS role and browser-check sections are framework-independent; skip the React field example outside React). For a new React component, also load `templates/component-template.tsx`; do NOT load the template for token-only work or a non-React stack.
6. **Choose the theme mechanism.** Default: semantic CSS custom properties switched by a `data-theme` attribute. Use Tailwind variants or a ThemeProvider only when the project already depends on it or needs runtime theme objects.
7. **Pilot and revise.** Integrate into the pilot screen and the most constrained consumer (oldest framework version, non-React stack or fixed release train), so API gaps show before wider adoption. With a browser test rig, run the theme-state check in `references/component-examples.md`. Without one, do a keyboard and 200%-zoom pass per theme; the usual per-theme breaks are a focus ring invisible on dark surfaces and an untested hover role. With no runnable UI or browser at all, deliver the starter, mark integration, keyboard and zoom checks "not run", and end with a short handoff checklist for whoever can run them. Revise the API before wider adoption if consumers need repeated workarounds.
8. **Adopt without breaking consumers.** Before publishing, load `checklists/design-system-checklist.md` and complete its Release gate. Keep deprecated tokens and props as aliases to the new path; default window: they work through the next major release and are removed in the one after (shorten only when every consumer lives in one repository).
   - Migration order: rank consumers by the step 1 inventory (most hardcoded values and accessibility failures first; the pilot leads).
   - Move one consumer per release onto the new tokens while the deprecated aliases keep the rest working.
   - Remove the deprecated tokens only after the last consumer has moved, and never before the window ends.

## Gotchas

- Never alias semantic roles across themes without checking every state (hover, focus, disabled, error, selected): a color that passes in the default state can fail in one theme's hover.
- Never derive state colors in components (`color-mix()`, opacity): the derived value exists in no token file, so no token-level check can see it.
- Never expose primitive palette names as component props: that freezes the palette into consumer APIs and blocks any later re-theme.
- Never change a token's meaning in a patch or minor release: consumers depend on its visual contract even when the type is unchanged.
- Never set `data-theme` only after the app boots: a stored dark choice paints light first and flashes. Set it from a small inline script in `<head>`, from the stored choice or `prefers-color-scheme`, before the first paint.
- Never ship `feedback.error` and `feedback.success` roles that differ only in hue: red and green collapse for deuteranopes even when each passes against the surface. Check them side by side under a color-vision-deficiency simulation (Chrome DevTools, Rendering > Emulate vision deficiencies) and pair each with an icon or text.
- DTCG 2025.10 (the stable format) requires object values: dimension `{"value": 16, "unit": "px"}`, color `{"colorSpace": "srgb", "components": [...]}`. Strings like `"16px"` or `"#fff"` are the older draft form; Style Dictionary reads object colors from 5.3 and object dimensions from 5.4, so on an older toolchain keep string values and do not claim 2025.10.
- The official schema (`https://www.designtokens.org/schemas/2025.10/format.json`) checks a value only when `$type` sits on the token itself; with group-level `$type`, a passing schema run proves nothing about values.
- Check nesting against each element's own HTML content model, never one rule for all interactive elements. `<button>`: phrasing content only, with no interactive descendant and no descendant with `tabindex`, so a Header/Body compound goes on a non-interactive container. `<a href>`: transparent, so a card link may wrap a heading or block content, but no interactive descendant, nested `<a>` or `tabindex` descendant.
- Build the dialog primitive on native `<dialog>` with `showModal()` or a tested library, never `aria-modal` on a styled box: the attribute only tells assistive tech the rest is inert; it traps no focus, makes nothing inert and handles no Escape or top-layer stacking, which `showModal()` does natively.

## Resources

- `checklists/design-system-checklist.md`: auditing an existing UI (step 1) or gating a release (step 8). Not for greenfield first passes.
- `templates/design-tokens-template.json`: whenever you write a token file (step 4).
- `references/token-checks.md`: whenever a shell can run the step 4 checks. Not needed for tool-less answers.
- `references/component-examples.md`: writing or reviewing component APIs, or running the theme-state check (steps 5, 7).
- `templates/component-template.tsx`: only when scaffolding a new React component (step 5).
