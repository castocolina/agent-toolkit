# tokens

## Decisions

- Where a value goes, in order: the role already in the theme; a new role added to that theme; the no-theme default in `SKILL.md` `## tokens`. Never the component.
- A z-index, duration or breakpoint used twice becomes a role in the same theme; a one-off is flagged, not inlined.
- Check contrast once per role pair per theme (`color-text` on `color-surface`), not once per component.

## Gotchas

- MUI `sx` color keys accept a theme path (`color: 'error.main'`), which is a token read; a hex string in the same key is a literal.
- The DTCG format is a final community group report (2025.10), not a W3C standard (https://www.designtokens.org/TR/2025.10/format/, checked 2026-11-15); follow it only when the repo already keeps `.tokens.json` files.
