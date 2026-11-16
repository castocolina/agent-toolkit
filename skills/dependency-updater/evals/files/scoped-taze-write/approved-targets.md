# Targets I approved

| Package | From | To |
| --- | --- | --- |
| react | ^17.0.2 | ^18.3.1 |
| react-dom | ^17.0.2 | ^18.3.1 |

The target applies to every section that declares the package, peer ranges included:

| Manifest | Section | Packages | To |
| --- | --- | --- | --- |
| apps/web/package.json | dependencies | react, react-dom | ^18.3.1 |
| packages/ui/package.json | devDependencies | react, react-dom | ^18.3.1 |
| packages/ui/package.json | peerDependencies | react, react-dom | ^18.3.1 |

Everything else (vite, storybook, turbo, typescript) stays as it is.
