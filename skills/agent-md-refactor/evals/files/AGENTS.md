# Acme Platform

Monorepo for the Acme billing platform. Be careful, write good code, and follow best practices.

## Setup

- Package manager: npm. Always install with `npm install --registry=https://npm.acme.internal/` because the public registry is blocked on our CI runners. Never remove the `--registry` flag.
- Build: `npm run build:all`
- Test: `npm test`

## Style

- Always use semicolons in TypeScript.
- Never use semicolons in TypeScript.
- Write clean, maintainable code.
- Use descriptive variable names.

## Testing

- Write unit tests for every new function.
- Run `npm test` before committing.
- Run tests before committing.
- Mock the network in unit tests.

## Git

- Use conventional commit messages.
- Squash fixup commits before opening a PR.
- Never force-push to `main`.

## API package

- Only under `packages/api/`: every handler must validate its input with the shared `zod` schemas, and the `no-console` lint rule is off there so request logs can use `console.info`.
- Everywhere else in the repo, `console.*` calls are forbidden.

## Deployment

- Deploys run from the `release` branch only.
- Run `npm run deploy:staging` before `npm run deploy:prod`.
