# Process and tooling notes

Short notes for workflow step 6: theming alternatives. Choices of platform, tool and numeric budget (documentation site, visual-regression service, bundle size) are project decisions: record the chosen ones in the checklist's scope line instead of adopting a default from here.

## Theming approaches (step 6)

The default is semantic CSS custom properties switched by `data-theme` (see `references/component-examples.md`). The two alternatives apply only when the project already uses them:

- **Tailwind `dark:` variants**: `<div className="bg-white dark:bg-gray-900">`; map the Tailwind palette to the same semantic roles, and keep the `data-theme` or media-query switch consistent with the head script (read the Tailwind dark-mode docs for the installed version's selector configuration).
- **A ThemeProvider** (styled-components or similar) for runtime theme objects: mirror the semantic paths exactly, one object per theme; derive the type from one theme object (`type Theme = typeof light`) and declare the other theme as `Theme`, so a missing path fails at type level.
