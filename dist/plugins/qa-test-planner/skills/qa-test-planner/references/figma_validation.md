# Figma Design Validation

How to compare an implementation with a Figma design so that each reported mismatch is a product defect, not an artifact of the comparison.

## 1. Pin the reference

- Get a link to the exact frame (the URL carries `node-id`), not the file. A file-level link lets you compare against the wrong frame or variant.
- Note the file's last-edited date or version and the frame's dev status. A design edited after the build was cut is a design change, not a bug; ask which version the build targeted.
- With a Figma MCP server available, list its tools first (names differ between server versions), then pull the frame's variables or tokens, a screenshot and the layer properties. Without one, ask for a 1x frame export plus the inspect values, and state in the deliverable that values come from the requester, not from Figma.

## 2. Match the rendering conditions

Record these for both sides before judging any difference:

| Condition | Why a mismatch here is not a defect |
| :- | :- |
| Viewport width | Layout breakpoints change spacing and wrapping |
| Device-pixel ratio | Figma values are CSS pixels at 1x; a DPR 2 screenshot shows every size doubled. Measure computed styles in DevTools, not screenshot pixels |
| Theme and locale | Dark tokens and longer translated strings change color and wrapping |
| Content | Figma placeholder text is shorter than real data; compare with the same content |
| Fonts | A failed web-font load falls back silently; check the rendered font in DevTools, not the declared `font-family` |
| Color profile | A Figma file set to Display P3 shows hex values that differ from the sRGB the browser renders; screenshots also carry compression and profiles. Compare tokens or computed values, never sampled screenshot pixels |

## 3. Measure, then compare

- Compare tokens first (`--color-primary` against the Figma variable): a token mismatch is one bug however many components show it.
- Translate units before calling a mismatch: Figma letter spacing is often in percent and CSS uses `em` or `px`; Figma "auto" line height is not CSS `normal`; Figma layer opacity and a CSS alpha color look alike but give different hex values.
- Force interactive states (hover, focus, active, disabled) in DevTools and compare each against its Figma variant; untested states are listed as not covered, not as passing.
- Agree a tolerance before you start (for example 1px for subpixel rounding) and state it in the report, so "close enough" is decided once, not per element.

## 4. Record each discrepancy

| Element | Property | Design value (source) | Implementation value (how measured) | Conditions | Verdict |
| :- | :- | :- | :- | :- | :- |
| Primary button | background | `#0066FF`, variable `primary/500` | `#0052CC`, computed style | 1440px, DPR 1, light | Defect: wrong token |
| Card title | font weight | 600 | 400, rendered font Inter Regular | 1440px, DPR 2, light | Defect, or font not loaded: check the network panel |

File one bug per root cause (a wrong token, a missing state), listing every affected element, with the frame link and conditions from section 2.
