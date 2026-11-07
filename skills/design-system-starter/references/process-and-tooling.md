# Process and tooling notes

Short checklists for workflow steps 6 to 8: theming approaches, testing, documentation and rollout. Choices of platform, tool and numeric budget (documentation site, visual-regression service, bundle size) are project decisions: record the chosen ones in the checklist's scope line instead of adopting a default from here.

## Principles to state in the starter

Write these into the system's own documentation as the rules a reviewer applies:
- **Consistency over creativity**: predictable patterns reduce cognitive load, so users learn once and apply everywhere.
- **Accessible by default**: WCAG 2.x Level AA as the minimum (WCAG 2.2 is the current W3C Recommendation, https://www.w3.org/TR/WCAG22/, checked 2026-11-07), keyboard operation and screen-reader support designed in from the first component.
- **Scalable and maintainable**: tokens allow global changes, composition reduces duplication.
- **Developer-friendly**: clear API contracts, documentation next to the component, easy to adopt and customize.
Also record the design language (tone, personality) and the values behind decisions, so later choices stay consistent with them.

## Theming approaches (step 6)

The default is semantic CSS custom properties switched by `data-theme` (see `references/component-examples.md`). The two alternatives apply only when the project already uses them:

```css
:root { --color-bg: #ffffff; --color-text: #000000; }
[data-theme="dark"] { --color-bg: #1a1a1a; --color-text: #ffffff; }
```

- **Tailwind `dark:` variants**: `<div className="bg-white dark:bg-gray-900">`; map the Tailwind palette to the same semantic roles, and keep the `data-theme` or media-query switch consistent with the head script (read the Tailwind dark-mode docs for the installed version's selector configuration).
- **A ThemeProvider** (styled-components or similar) for runtime theme objects: mirror the semantic paths exactly, one object per theme, so a path missing from one theme fails at type level.

```ts
interface Theme {
  color: { text: Record<string, string>; surface: Record<string, string>; action: Record<string, string>; feedback: Record<string, string> };
  font: { family: Record<string, string>; size: Record<string, string> };
  spacing: Record<string, string>;
  radius: Record<string, string>;
  shadow: Record<string, string>;
}
```

Customization to document for consumers: which tokens they may override (as CSS variables), how a second brand is supplied (a second value set on the same paths), and any programmatic theme API.

## ARIA attributes that components commonly need

- `aria-label` or `aria-labelledby`: an accessible name where no visible text names the control.
- `aria-expanded` with `aria-controls`: a control that shows or hides a region (menu button, disclosure).
- `aria-live` (or `role="status"` and `role="alert"`): announce content that changes after load.
- Prefer the native element or attribute first; add ARIA only for what HTML cannot express.

## Testing (step 7)

- Visual regression: capture each component per theme and state with whichever visual-regression service the project uses.
- Cross-browser and responsive: check the browsers and viewports the project supports, and check every component in dark mode (the theme-state check in `references/component-examples.md` automates the contrast part).
- Functional: unit and integration tests for behavior; automated contrast and axe checks need a real browser, not jsdom.

## Documentation and rollout (step 8)

Deliverables a design-system release or starter typically names:
- Token output: color primitives and semantic roles, typography, spacing, radius and shadow scales (`references/token-scales.md`).
- Theming output: theme structure, light and dark value sets, the CSS variable mapping and component integration notes.
- Accessibility output: contrast results per theme (measured or computed by hand), keyboard requirements, ARIA recommendations, screen-reader test notes and focus management.

Component guidance pages cover when to use which component, how components combine, content guidelines for labels and messages, how to apply the spacing tokens, and responsive behavior (mobile first).

Getting-started documentation: installation, setup and configuration, theming, and a migration guide for upgrading from earlier versions (the release gate requires migration notes).

Adoption support: ship codemods when a migration can be automated, run a short training or walkthrough for each consuming team, publish a getting-started guide with a tutorial, and name a support channel.

After launch: announce the release, hold early office hours, collect feedback from early adopters and fix issues in patch releases. Track adoption across products, which components are used most, and incoming bug and feature requests (the metrics are inputs to step 8's migration order, not targets).
