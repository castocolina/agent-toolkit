# loading

The wait thresholds, the submit rule and the decide-by-scope rule live in `SKILL.md` `## loading`. Timing from the NN/g skeleton and response-time pages; the in-button indicator from Apple HIG Buttons; the layout-shift target from web.dev, Optimize CLS.

## Decisions

- Why nothing under about 1 s: a placeholder that flashes on a fast load is noise. Past about 10 s the progress is a percent or estimate, not an indeterminate bar.
- Content that arrives later reserves its space up front, sized to the final content and adjusted per screen size (web.dev). Removing reserved space shifts the layout as much as inserting content does.
- A skeleton never replaces performance work (NN/g).

## Gotchas

- Wrapping the real component in MUI `Skeleton` infers its size, which keeps CLS near 0; a free-standing `Skeleton` needs explicit width and height.
- A skeleton still on screen after the request failed is a broken handoff: swap to the error state.
- Turn the pulse off under `prefers-reduced-motion` (NN/g says skeleton animation can cause accessibility problems; the pairing itself is UNVERIFIED).
- Check the skeleton color against the dark surface, not only the light one.

## Fix pattern

The list skeleton is in the passing example in `SKILL.md`; the pending submit:

```tsx
<button type="submit" disabled={saving} aria-busy={saving}>
  {saving ? <><Spinner aria-hidden /> Saving</> : 'Save'}
</button>
```
