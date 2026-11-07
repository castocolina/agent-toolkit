# mui: sources

Checked 2026-11-07. Review only: no `track` call was made and no registry or README edit was done.

## Origin

- The skill comes from softaworks/agent-toolkit, commit `011baf4a` "feat: add 7 new skills" (2026-01-18, Leonardo Flores), which added `skills/mui/` with README.md, SKILL.md, `resources/{component-library,styling-guide,theme-customization}.md` and `skill-rules-fragment.json`. It is in this repo's fork point `3027f20f` unchanged.
- Upstream today: `gh api repos/softaworks/agent-toolkit/contents/skills/mui` lists README.md, SKILL.md, resources and skill-rules-fragment.json; `commits?path=skills/mui` returns only `011baf4a`. Upstream has not changed since the fork point.
- No credit line exists anywhere for mui: not in `skills/mui/README.md`, not in the root README (its mui row only names the skill), and no registry row has `"skill": "mui"`. The only softaworks row that reaches it is the whole-repo `repo` row (`skill: null`), which `upstreams` does not map to mui.
- Everything else in the current files is original to this repo (rewritten against the MUI docs), so no other origin was found. A web search on distinctive phrases was not needed: the old text is the softaworks text, and the current text states MUI's own documented behavior.

## Proposed registry rows (one object per line)

```json
{"skill": "mui", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/mui", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, Upgrade to v7: https://mui.com/material-ui/migration/upgrade-to-v7/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, Upgrade to v9: https://mui.com/material-ui/migration/upgrade-to-v9/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, Palette: https://mui.com/material-ui/customization/palette/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, Dark mode: https://mui.com/material-ui/customization/dark-mode/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, CSS theme variables usage: https://mui.com/material-ui/customization/css-theme-variables/usage/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, CSS theme variables configuration: https://mui.com/material-ui/customization/css-theme-variables/configuration/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, CSS theme variables native color: https://mui.com/material-ui/customization/css-theme-variables/native-color/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, CSS layers: https://mui.com/material-ui/customization/css-layers/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "MUI System, The sx prop: https://mui.com/system/getting-started/the-sx-prop/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, Grid: https://mui.com/material-ui/react-grid/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, Skeleton: https://mui.com/material-ui/react-skeleton/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "Material UI, Dialog: https://mui.com/material-ui/react-dialog/", "ref": null, "credit": "MUI"}
{"skill": "mui", "kind": "unversioned", "source": "npm registry, @mui/material (dist-tags, peerDependencies, publish times): https://www.npmjs.com/package/@mui/material", "ref": null, "credit": "MUI"}
```

The first row is `github-path` like the sibling `database-schema-designer` row; `ref` `main` resolves (the path exists upstream). `upstreams` will report `stale` once upstream changes `skills/mui`; the unversioned rows are never reported stale (known limit in plan 14 Step 5).

## Missing credit line

`skills/mui/README.md` has none. Add this section at its end, the same wording as `skills/database-schema-designer/README.md`:

```text
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

(A softaworks row exists for the whole repo but names no author; the README line above is the credit this skill lacks.)

## skill-updater style review (review only)

- Rows: none for mui, so `upstreams` has nothing to read; the proposed rows above must be added first (the controller does it). With the `github-path` row in place, upstream has no change after `011baf4a`, so the adopt/adapt/ignore list from upstream is empty:
  - ignore: upstream `skill-rules-fragment.json` (activation config for a hook system this repo does not use; the 2026-10-28 audit asked for its removal).
  - ignore: upstream `component-library.md` and the snippet-style SKILL.md sections (generic model knowledge, see record.md; the user gate on the `purpose-change-pending` rows decides whether the cookbook returns).
  - ignore: upstream "all components use slots/slotProps" and `item xs` Grid examples (contradicted by the v7 upgrade guide).
- Items for the restore brief (from the docs, not from upstream):
  - adapt: the version scope. npm `latest` is 9.5.0 (2026-10-09), `latest-v7` is 7.3.11, and there is no v8 tag. The skill says v7 throughout. A user decision is needed: keep it v7-only (add a pointer to the installed major and to `https://mui.com/material-ui/migration/upgrade-to-v9/`), or add v8/v9 notes. Facts that differ in v9: GridLegacy removed; the system props (mt, color, ...) removed from Box, Grid, Stack and Typography (use sx); `disableEscapeKeyDown` removed from Dialog and Modal (check `reason === 'escapeKeyDown'`); `TextField` slot names unchanged from v7 per the v9 guide; deprecated Button/Chip/Alert class keys in `styleOverrides` moved into `variants`; 23 `...Outline` icon exports removed from `@mui/icons-material` (use `...Outlined`); browser targets raised (Chrome 117+, Firefox 121+, Safari 17+); `@mui/icons-material` and `@mui/system` bump to 9.0.0.
  - adapt: README Prerequisites "React 18 or later" should read as a pointer to the installed `peerDependencies` (React 17, 18 and 19 are accepted by both 7.3.11 and 9.5.0).
  - adapt: SKILL.md says CSS layers are `enableCssLayer` "in 7.3"; the docs name the same props (`enableCssLayer`, `modularCssLayers`) without a minimum version, so keep the grep-the-d.ts instruction and drop or soften the version number.
  - adapt: add a one-line pointer to the native-color helpers (`theme.alpha`, `theme.lighten`, `theme.darken` with `cssVariables.nativeColor`) next to the existing `alpha()` caveat in styling-guide.md.
- Model-validity pass: not run. The rails forbid an LLM lane for analysts. The rules that exist to counter a model habit, for the controller's probe (one prompt each, no skill loaded): `Grid item xs/md` instead of `size` (v7); `onBackdropClick` and `components={{ Backdrop }}` on Dialog; deep `@mui/material/Dialog/Dialog` imports; spreading `useTheme()` into `createTheme`; a lone `CircularProgress` for content loading; `IconButton` without `aria-label`.
- Judge on change: needed for the restore dispatch (Step 7), not for this analysis.
