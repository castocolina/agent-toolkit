| item | fate | value | decision | reason class | reason |
| --- | --- | --- | --- | --- | --- |
| s005 1. Design Tokens | removed-on-merit | low | drop-pending | superseded-by token template and the token-scales restore | README overview of token kinds; the actual scales are tracked in rows s038-s041 |
| s006 2. Component Architecture | removed-on-merit | low | drop-pending | superseded-by SKILL.md step 5 (levels derived from use) | README atomic-design list replaced by primitives/composed patterns/product modules; examples return via component-specs |
| s007 3. Accessibility | not-lost | real | none | text-present | contrast thresholds in step 4, keyboard/focus/name in the checklist Components section; broader WCAG list is row s083-s086 |
| s008 4. Theming | not-lost | low | none | text-present | step 6 names CSS custom properties, Tailwind variants and ThemeProvider |
| s010 Design Token System | not-lost | low | none | text-present | DTCG format and primitive/semantic split are in README and template; shadow scale tracked in s041 |
| s011 Component Templates | removed-to-fit | real | restore-references | users-ask-by-name | README advertised polymorphic and compound patterns; restored via s108 and s111, README resource line should mention them |
| s012 Bundled Resources | not-lost | low | none | text-present | README Bundled resources lists the current files |
| s013 Accessibility First | removed-on-merit | low | intended-change | fact-update | "WCAG 2.1 AA by default" claim dropped; W3C WCAG 2.2 is a Recommendation (12 Dec 2024) and the skill now says WCAG 2.x without pinning |
| s015 Example 2: Add Design Tokens | removed-on-merit | low | drop-pending | generic-model-knowledge | sample prompt plus deliverable bullets; 8px scale returns in token-scales, Style Dictionary caveats are in the gotchas |
| s016 Example 3: Component Architecture | removed-on-merit | low | drop-pending | generic-model-knowledge | sample prompt plus deliverable bullets; README keeps three usage prompts |
| s018 Example 5: Theming Implementation | removed-on-merit | low | drop-pending | generic-model-knowledge | sample prompt plus bullets; theming is covered by step 6 and component-examples |
| s019 Triggers | removed-on-merit | low | drop-pending | superseded-by frontmatter description | trigger phrases now live in the description |
| s020 Design Tokens Output | removed-on-merit | low | drop-pending | superseded-by token-scales restore (s038-s041) | list of output scales duplicates the detailed scale sections |
| s022 Theming Output | removed-on-merit | low | drop-pending | generic-model-knowledge | bullet list of theming deliverables |
| s023 Accessibility Checklist Output | removed-on-merit | low | drop-pending | generic-model-knowledge | bullet list of a11y deliverables |
| s024 Design Philosophy | removed-on-merit | low | drop-pending | generic-model-knowledge | four generic principles |
| s025 Integration | removed-on-merit | low | drop-pending | out-of-scope | capability claims (Tailwind mapping, Figma naming, Storybook) with no backing content; Storybook is now explicitly out of scope |
| s026 Related Skills | removed-on-merit | low | drop | stale | landing-page-guide-v2 and nextjs15-init do not exist in this repo; mui pointer is low value |
| s027 (preamble) | removed-on-merit | low | drop | superseded-by current frontmatter | old description and tag list replaced by a trigger-rich description, license and metadata kept |
| s028 Design System Starter | removed-on-merit | low | drop | superseded-by current intro line | one-line tagline |
| s030 Triggers | removed-on-merit | low | drop | superseded-by frontmatter description | trigger table replaced by description |
| s031 Quick Reference | removed-on-merit | low | drop | superseded-by SKILL.md Workflow deliverable sizing | task to output table |
| s033 What is a Design System? | removed-on-merit | low | drop | generic-model-knowledge | generic definition |
| s034 Core Principles | removed-on-merit | low | drop | generic-model-knowledge | generic principles |
| s035 Design Tokens | removed-on-merit | low | drop | generic-model-knowledge | one-line definition of tokens |
| s037 1. Color Tokens | not-lost | real | none | text-present | 4.5:1, 3:1 thresholds in step 4; large-text definition restored via s049 |
| s038 2. Typography Tokens | removed-to-fit | real | restore-references | reusable-template | full font family, xs-5xl size, weight, line-height, letter-spacing scale; current template has only 3 sizes and 2 roles; restore in DTCG 2025.10 object form |
| s039 3. Spacing Tokens | removed-to-fit | real | restore-references | reusable-template | 0-24 spacing scale plus component spacing tokens; template has 5 steps |
| s040 4. Border Radius Tokens | removed-to-fit | real | restore-references | reusable-template | none-to-full radius scale; template has one control radius |
| s041 5. Shadow Tokens | removed-to-fit | real | restore-references | reusable-template | elevation scale; no shadow token exists now; restore as DTCG shadow objects, note Tailwind v4 renamed its own steps |
| s042 Atoms (Primitive Components) | not-lost | real | none | text-present | Button contract in component-template.tsx, level definition in step 5; atom examples return via component-specs |
| s043 Molecules (Simple Compositions) | not-lost | real | none | text-present | accessible FormField in component-examples, Card nesting gotcha; SearchBar via component-specs |
| s044 Organisms (Complex Compositions) | removed-on-merit | low | drop | superseded-by SKILL.md step 5 (product modules) | example list only |
| s045 Templates (Page Layouts) | removed-on-merit | low | drop | generic-model-knowledge | three page layout names |
| s046 Props Best Practices | removed-to-fit | real | restore-references | reusable-template | cross-component prop naming consistency, defaults and composition-over-configuration rule are decision rules; current text keeps only semantic props and slots; restore in component-examples |
| s047 Theme Structure | removed-on-merit | low | drop-pending | superseded-by SKILL.md step 6 (CSS custom properties by default) | TypeScript Theme interface for runtime theme objects |
| s048 Dark Mode Implementation | removed-on-merit | low | drop-pending | generic-model-knowledge | three approaches; CSS variables approach is richer in component-examples, Tailwind dark: and ThemeProvider are named in step 6 |
| s049 Color Contrast | removed-to-fit | real | restore-references | reusable-template | thresholds present but the large-text definition (18pt, or 14pt bold) is gone; verified on w3.org WCAG 2.2; add to token-checks.md |
| s050 Keyboard Navigation | removed-on-merit | real | intended-change | safety-fix | example adds onKeyDown Enter to a native button (double activation) and a FocusTrap; superseded by native elements and native dialog |
| s051 ARIA Attributes | removed-on-merit | low | drop-pending | generic-model-knowledge | four ARIA attributes list |
| s052 Screen Reader Support | not-lost | low | none | text-present | native element for the role in the checklist and nesting gotcha |
| s053 Component Documentation Template | not-lost | real | none | text-present | step Workflow requires props with defaults, States line and accessibility notes per component |
| s054 1. Design Phase | not-lost | real | none | text-present | audit in step 1, tokens in step 3, inventory in checklist; Figma library dropped as project decision |
| s055 2. Development Phase | removed-on-merit | low | intended-change | scope-change | atoms-first build order contradicts step 2 (pilot with a real consumer, no abstract primitive library without an adopter) |
| s056 3. Adoption Phase | removed-on-merit | low | drop-pending | generic-model-knowledge | codemods, workshops, feedback; migration guide and one-consumer-per-release are in step 8 |
| s057 4. Maintenance Phase | not-lost | real | none | text-present | semver and deprecation window in step 8, changelog covered by release-gate migration notes; adoption monitoring tracked in s102 |
| s059 Design Principles | removed-on-merit | low | drop-pending | generic-model-knowledge | principles, values and design language documented |
| s060 Color Tokens | not-lost | real | none | text-present | semantic roles, contrast, per-theme parity, naming are in Tokens checklist and steps 3-4 |
| s061 Typography Tokens | removed-to-fit | real | restore-references | reusable-template | font families, scale, at least 3 weights, line-height and letter-spacing guidance; restore with the typography scale (s038) |
| s062 Spacing Tokens | removed-to-fit | real | restore-references | reusable-template | scale and component spacing guidance; restore with s039 |
| s063 Other Tokens | removed-to-fit | real | restore-references | reusable-template | radius, shadow, transition (easing) and z-index tokens; only duration exists now; restore with s040-s041 |
| s064 Button | removed-to-fit | real | restore-references | reusable-template | variants, sizes, states, icons, full-width spec; restore as a row of component-specs.md |
| s065 Input | removed-to-fit | real | restore-references | reusable-template | types, states, helper text, a11y spec; component-specs.md |
| s066 Checkbox & Radio | removed-to-fit | real | restore-references | reusable-template | states incl. indeterminate, label association; component-specs.md |
| s067 Select / Dropdown | removed-to-fit | real | restore-references | reusable-template | single/multi/search and combobox keyboard spec; component-specs.md |
| s068 Badge | removed-to-fit | real | restore-references | reusable-template | variants, sizes, removable; status variants need the not-color-only rule; one more row of component-specs.md |
| s069 Avatar | removed-to-fit | real | restore-references | reusable-template | sizes, fallback, status indicator spec; component-specs.md |
| s070 Icon | removed-to-fit | real | restore-references | reusable-template | sizes and aria-label vs aria-hidden rule; component-specs.md |
| s072 Search Bar | removed-to-fit | real | restore-references | reusable-template | composition, clear button, Enter to submit; component-specs.md |
| s073 Card | removed-to-fit | real | restore-references | reusable-template | variants, header/body/footer, clickable area; component-specs.md plus s108 |
| s074 Alert / Toast | removed-to-fit | real | restore-references | reusable-template | variants, dismissible, icons, actions; add live-region and not-color-only notes; component-specs.md |
| s075 Navigation Bar | removed-to-fit | real | restore-references | reusable-template | responsive menu, dropdown and nav landmark spec; component-specs.md |
| s076 Modal / Dialog | removed-to-fit | real | restore-references | reusable-template | overlay, close, sizes, focus spec; restore built on native dialog to match the gotcha |
| s077 Table | removed-to-fit | real | restore-references | reusable-template | header, sortable, selectable, responsive, semantics spec; component-specs.md |
| s078 Pagination | removed-to-fit | real | restore-references | reusable-template | page numbers, prev/next, first/last, page size; component-specs.md |
| s079 Layout Patterns | removed-to-fit | real | restore-references | reusable-template | grid, container, Stack, Cluster, sidebar layout primitives; component-specs.md |
| s080 Form Patterns | removed-on-merit | low | drop | generic-model-knowledge | validation, wizard, inline edit, autosave names only |
| s081 Navigation Patterns | removed-on-merit | low | drop | generic-model-knowledge | breadcrumbs, tabs, sidebar, mega menu names only |
| s082 Feedback Patterns | removed-to-fit | real | restore-references | reusable-template | loading, empty, error and success state patterns; component-specs.md |
| s083 Perceivable | removed-to-fit | real | purpose-change-pending | scope-change | generic WCAG audit checklist (alt text, captions, color independence); current description sends ARIA how-to and single-screen a11y review elsewhere; restoring brings back a general a11y purpose |
| s084 Operable | removed-to-fit | real | purpose-change-pending | scope-change | keyboard, focus, skip link, touch targets; the 44x44 px figure is WCAG 2.2 AAA 2.5.5, AA 2.5.8 is 24x24 CSS px, so fix on restore; same purpose question |
| s085 Understandable | removed-to-fit | real | purpose-change-pending | scope-change | lang attribute, labels, error messages; same purpose question |
| s086 Robust | removed-to-fit | real | purpose-change-pending | scope-change | valid HTML, ARIA, name/role/value; same purpose question |
| s087 Component Documentation | not-lost | real | none | text-present | Components checklist: props with types, defaults and states; do/don't lines are low value |
| s088 Design Guidelines | removed-on-merit | low | drop-pending | generic-model-knowledge | when-to-use, content and spacing guideline prompts |
| s089 Getting Started | removed-on-merit | low | drop-pending | generic-model-knowledge | install, setup, theming docs prompts; migration notes kept in release gate |
| s090 Development Tools | removed-on-merit | low | intended-change | scope-change | checklist now states publication platforms (Storybook etc.) are project decisions recorded in the scope line |
| s091 Build & Distribution | removed-on-merit | low | intended-change | scope-change | channels and numeric budgets are project decisions; semver and changelog kept in release gate |
| s092 Design Tools | removed-on-merit | low | intended-change | scope-change | Figma library is a project decision per the current checklist intro |
| s093 Theme Support | not-lost | real | none | text-present | step 6 and the head-script gotcha cover light/dark, system preference, stored choice |
| s094 Customization | removed-on-merit | low | drop-pending | generic-model-knowledge | token override and theme API prompts; CSS variables and brand variants covered by step 3 and 6 |
| s095 Visual Testing | removed-on-merit | low | drop-pending | generic-model-knowledge | Chromatic/Percy and cross-browser prompts; theme-state browser check exists |
| s096 Functional Testing | not-lost | real | none | text-present | axe automated check in component-examples theme-state validation; unit and integration prompts are generic |
| s097 Performance | removed-on-merit | low | intended-change | scope-change | current checklist says numeric budgets are project decisions; the 100KB figure was arbitrary |
| s098 Contribution Guidelines | removed-on-merit | low | drop | generic-model-knowledge | CONTRIBUTING, code of conduct, PR template |
| s100 Roadmap | removed-on-merit | low | drop | generic-model-knowledge | public roadmap prompts |
| s101 Onboarding | removed-on-merit | low | drop-pending | generic-model-knowledge | getting-started guide, tutorial, support channel |
| s102 Metrics | removed-on-merit | low | drop-pending | generic-model-knowledge | adoption and component usage tracking prompts |
| s103 Iteration | removed-on-merit | low | drop | generic-model-knowledge | quarterly review prompts |
| s104 Pre-Launch Checklist | removed-on-merit | low | intended-change | scope-change | universal atom/molecule list and "100% pass" replaced by a scope-based Release gate |
| s105 Post-Launch | removed-on-merit | low | drop-pending | generic-model-knowledge | announce, training, office hours prompts |
| s106 Button Component (Complete Implementation) | removed-on-merit | real | intended-change | safety-fix | disabled attribute drops keyboard focus, emoji spinner, palette-named classes; replaced by component-template.tsx |
| s107 Form Field Component (Molecule) | not-lost | real | none | text-present | accessible FormField in component-examples with aria-describedby and aria-invalid |
| s108 Card Component (Compound Component Pattern) | removed-to-fit | real | restore-references | users-ask-by-name | compound Header/Title/Body/Footer pattern; restore rewritten with role tokens, no root className, nesting gotcha |
| s109 Input Component with Variants | removed-on-merit | real | intended-change | safety-fix | error state by border color only with no aria-invalid, palette classes, root className |
| s110 Modal Component (Organism) | removed-on-merit | real | intended-change | safety-fix | role=dialog div with aria-modal and hand-rolled focus and Escape; the gotcha now requires native dialog. A native-dialog Modal example is an adapt item, not a restore |
| s111 Polymorphic Component Example | removed-to-fit | real | restore-references | users-ask-by-name | typed `as` prop pattern, advertised in README; restore in React 19 form with ref as prop |
| s112 Accessibility Example - Skip Link | removed-to-fit | real | restore-references | reusable-template | skip link and sr-only CSS; restore as plain CSS, WCAG 2.4.1 Bypass Blocks is Level A |
| s113 Theme Switching Example | removed-to-fit | real | restore-references | reusable-template | toggle with stored choice; old version sets data-theme after mount (flash), restore reading the head-script value |
| s114 Responsive Navigation Example | removed-to-fit | real | restore-references | reusable-template | responsive nav with mobile menu; restore with aria-controls, aria-current and nav landmark |
| file:skills/design-system-starter/templates/component-template.tsx | removed-on-merit | real | intended-change | safety-fix | div role=button with className and hand-made Enter/Space replaced by native button; lost outline/ghost/lg variants, JSDoc @default docs, compound scaffold and usage examples (compound returns via s108) |
| file:skills/design-system-starter/templates/design-tokens-template.json | removed-on-merit | real | intended-change | safety-fix | rewritten to DTCG 2025.10 object values with contrast-checked pairs (old gray.400 disabled text is 2.54:1, gray.200 borders fail 3:1) and a correct schema URL (old design-tokens.org v1.0.0 URL is not the DTCG schema); full ramps, scales and component tokens return via s038-s041 and warning/info roles are an adapt item |
| s001 Design System Starter | not-lost | low | none | text-present | README intro rewritten; "comprehensive/production-ready" tagline dropped |
| s002 Purpose | not-lost | low | none | text-present | tokens, theming, workflow bullets are in README When to use and SKILL.md; WCAG 2.1 claim tracked in s013, atomic-design wording in s006 |
| s003 When to Use | not-lost | low | none | text-present | README When to use lists the same needs; WCAG 2.1 AA bullet tracked in s013 |
| s004 How It Works | not-lost | low | none | text-present | five-area intro replaced by the package description; areas covered by Bundled resources |
| s009 5. Documentation | not-lost | low | none | text-present | props with defaults, States and a11y notes are required by the Workflow documentation guide |
| s014 Example 1: Create a New Design System | not-lost | low | none | text-present | prompt kept in README Usage examples; the numbered deliverable list is superseded by the Workflow |
| s017 Example 4: Accessibility Audit | removed-on-merit | low | intended-change | scope-change | generic WCAG 2.1 audit prompt dropped with the narrowed purpose (description routes single-component UI review to ui-ux-principles); see s083-s086 |
| s021 Component Architecture Output | not-lost | low | none | text-present | props with defaults, States and accessibility notes per component are required by the Workflow |
| s029 Quick Start | not-lost | low | none | text-present | README Usage examples keeps the prompt |
| s032 Bundled Resources | not-lost | low | none | text-present | resource list is now in the SKILL.md Resources section with loading triggers |
| s036 1. Color Tokens | not-lost | real | none | text-present | semantic text/surface/action/feedback roles are in the template; warning/info roles, brand active state and the 50-950 ramp are adapt items for the token-scales restore |
| s058 Quick Start Checklist | not-lost | real | none | text-present | Workflow Complete starter deliverables, steps 1-8 and the Release gate cover each item; principles line is generic |
| s071 Form Field | not-lost | real | none | text-present | FormField example renders "(required)", error state and label association |
| s099 Versioning & Deprecation | not-lost | real | none | text-present | step 8 and Release gate state the deprecation window, migration notes and removal version |
| para:03567550 checklist intro line | removed-on-merit | low | drop | superseded-by the current checklist intro | old "comprehensive checklist" sentence replaced by the scope-based intro |
| para:0ce096f0 Atoms to Pages arrow line | removed-on-merit | low | drop | superseded-by SKILL.md step 5 levels | five-level atomic hierarchy replaced by three levels derived from use |
| para:799de137 component-examples intro | removed-on-merit | low | drop | superseded-by the current component-examples intro | one-line intro rewritten |
| para:1b2a58f1 Pages definition | removed-on-merit | low | drop | generic-model-knowledge | one-line definition of atomic-design Pages |
