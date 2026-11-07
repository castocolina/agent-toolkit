# Token scales

Starter scales for workflow step 3, written in the DTCG 2025.10 object form that `templates/design-tokens-template.json` uses (dimension `{"value", "unit"}`, color `{"colorSpace", "components"}`, `$type` on every token; format: https://www.designtokens.org/tr/2025.10/format/, checked 2026-11-07). The values are a Tailwind-style starting scale: replace them per brand. For the live Tailwind values read https://tailwindcss.com/docs/theme (checked 2026-11-07) instead of copying numbers from here. Scale values follow the Tailwind CSS default theme (MIT). Components consume the semantic roles built on these scales (typography roles, spacing roles, `radius.control`), never the raw steps. On a toolchain that predates object values (SKILL.md DTCG gotcha), write the same numbers as strings.

Token kinds: color (primitive 50-950 ramps plus semantic roles), typography (families, sizes, weights, line heights, letter spacing), spacing, radius, shadow (elevation), plus duration, easing and layering below.

## Color: ramp, brand states and feedback roles

One primitive ramp (blue shown); repeat per hue the product needs. Add the 50-950 ramp only for hues a role uses.

```json
{
  "color": {
    "primitive": {
      "blue": {
        "50": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.9373, 0.9647, 1.0], "hex": "#eff6ff"}},
        "100": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.8588, 0.9176, 0.9961], "hex": "#dbeafe"}},
        "200": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.749, 0.8588, 0.9961], "hex": "#bfdbfe"}},
        "300": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.5765, 0.7725, 0.9922], "hex": "#93c5fd"}},
        "400": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.3765, 0.6471, 0.9804], "hex": "#60a5fa"}},
        "500": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.2314, 0.5098, 0.9647], "hex": "#3b82f6"}},
        "600": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.1451, 0.3882, 0.9216], "hex": "#2563eb"}},
        "700": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.1137, 0.3059, 0.8471], "hex": "#1d4ed8"}},
        "800": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.1176, 0.251, 0.6863], "hex": "#1e40af"}},
        "900": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.1176, 0.2275, 0.5412], "hex": "#1e3a8a"}},
        "950": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.0902, 0.1451, 0.3294], "hex": "#172554"}}
      },
      "yellow": {
        "700": {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0.6314, 0.3843, 0.0275], "hex": "#a16207"}}
      }
    }
  }
}
```

Semantic additions to the template's `color.semantic` (aliases only):

```json
{
  "color": {
    "semantic": {
      "action": {"active": {"$type": "color", "$value": "{color.primitive.blue.800}"}},
      "feedback": {
        "warning": {"$type": "color", "$value": "{color.primitive.yellow.700}"},
        "info": {"$type": "color", "$value": "{color.primitive.blue.600}"}
      }
    }
  }
}
```

Measured on white with the step 4 script (WCAG relative luminance, checked 2026-11-07; source https://www.w3.org/TR/WCAG22/):

| Role | Value | Ratio on #ffffff | Result |
| --- | --- | --- | --- |
| feedback.warning | yellow-700 `#a16207` | 4.9232 | passes 4.5 and 3 |
| feedback.warning (do not use) | yellow-600 `#ca8a04` | 2.9377 | fails 3 as text or icon |
| feedback.info | blue-600 `#2563eb` | 5.1686 | passes 4.5 and 3 |
| feedback.success | green-700 `#15803d` | 5.0156 | passes 4.5 and 3 (green-600 is 3.2957: icon only) |
| border.default | gray-500 `#6b7280` | 4.8345 | passes the 3 UI-boundary threshold |
| border (do not use) | gray-200 `#e5e7eb` | 1.2381 | fails the 3 UI-boundary threshold |

Decorative dividers that carry no meaning may use a lighter step; an input border or a focus ring may not. Re-measure every pair per theme and state; a warning pair on a tinted surface needs its own row (yellow-700 on yellow-50 is 4.7599).

## Typography

```json
{
  "font": {
    "family": {
      "sans": {"$type": "fontFamily", "$value": ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"]},
      "serif": {"$type": "fontFamily", "$value": ["Georgia", "Times New Roman", "serif"]},
      "mono": {"$type": "fontFamily", "$value": ["Fira Code", "Courier New", "monospace"]}
    },
    "size": {
      "xs": {"$type": "dimension", "$value": {"value": 0.75, "unit": "rem"}},
      "sm": {"$type": "dimension", "$value": {"value": 0.875, "unit": "rem"}},
      "base": {"$type": "dimension", "$value": {"value": 1, "unit": "rem"}},
      "lg": {"$type": "dimension", "$value": {"value": 1.125, "unit": "rem"}},
      "xl": {"$type": "dimension", "$value": {"value": 1.25, "unit": "rem"}},
      "2xl": {"$type": "dimension", "$value": {"value": 1.5, "unit": "rem"}},
      "3xl": {"$type": "dimension", "$value": {"value": 1.875, "unit": "rem"}},
      "4xl": {"$type": "dimension", "$value": {"value": 2.25, "unit": "rem"}},
      "5xl": {"$type": "dimension", "$value": {"value": 3, "unit": "rem"}}
    },
    "weight": {
      "normal": {"$type": "fontWeight", "$value": 400},
      "medium": {"$type": "fontWeight", "$value": 500},
      "semibold": {"$type": "fontWeight", "$value": 600},
      "bold": {"$type": "fontWeight", "$value": 700}
    },
    "lineHeight": {
      "tight": {"$type": "number", "$value": 1.25},
      "normal": {"$type": "number", "$value": 1.5},
      "relaxed": {"$type": "number", "$value": 1.75},
      "loose": {"$type": "number", "$value": 2}
    },
    "letterSpacing": {
      "tight": {"$type": "dimension", "$value": {"value": -0.4, "unit": "px"}},
      "normal": {"$type": "dimension", "$value": {"value": 0, "unit": "px"}},
      "wide": {"$type": "dimension", "$value": {"value": 0.4, "unit": "px"}}
    }
  }
}
```

The sizes are 12, 14, 16, 18, 20, 24, 30, 36 and 48 px at a 16 px root. Guidance for the roles built on them:
- Pick the families the product uses (sans for UI, serif and mono only when needed) and give each a fallback chain ending in a generic family.
- Define at least three weights (normal, medium, bold) and use them through roles (`font.role.body`, `font.role.label`), not per component.
- Line height: tight for headings, normal for body, relaxed for long paragraphs.
- Letter spacing: tighten large headings and loosen uppercase labels. DTCG dimensions allow only `px` and `rem`, so an `em` tracking value cannot be a token: the values above are `em` figures (-0.025em, 0.025em) converted at 16 px; define tracking per role when a heading size differs much.

## Spacing

Use one scale on a 4 px unit, so 8 px steps are every second entry.

```json
{
  "spacing": {
    "scale": {
      "0": {"$type": "dimension", "$value": {"value": 0, "unit": "px"}},
      "1": {"$type": "dimension", "$value": {"value": 0.25, "unit": "rem"}},
      "2": {"$type": "dimension", "$value": {"value": 0.5, "unit": "rem"}},
      "3": {"$type": "dimension", "$value": {"value": 0.75, "unit": "rem"}},
      "4": {"$type": "dimension", "$value": {"value": 1, "unit": "rem"}},
      "5": {"$type": "dimension", "$value": {"value": 1.25, "unit": "rem"}},
      "6": {"$type": "dimension", "$value": {"value": 1.5, "unit": "rem"}},
      "8": {"$type": "dimension", "$value": {"value": 2, "unit": "rem"}},
      "10": {"$type": "dimension", "$value": {"value": 2.5, "unit": "rem"}},
      "12": {"$type": "dimension", "$value": {"value": 3, "unit": "rem"}},
      "16": {"$type": "dimension", "$value": {"value": 4, "unit": "rem"}},
      "20": {"$type": "dimension", "$value": {"value": 5, "unit": "rem"}},
      "24": {"$type": "dimension", "$value": {"value": 6, "unit": "rem"}}
    }
  }
}
```

Component spacing aliases the scale; components read these, not the numbered steps:

```json
{
  "component": {
    "button": {
      "paddingX": {"$type": "dimension", "$value": "{spacing.scale.4}"},
      "paddingY": {"$type": "dimension", "$value": "{spacing.scale.2}"},
      "gap": {"$type": "dimension", "$value": "{spacing.scale.2}"}
    },
    "card": {
      "padding": {"$type": "dimension", "$value": "{spacing.scale.6}"},
      "gap": {"$type": "dimension", "$value": "{spacing.scale.4}"}
    }
  }
}
```

## Radius

```json
{
  "radius": {
    "none": {"$type": "dimension", "$value": {"value": 0, "unit": "px"}},
    "sm": {"$type": "dimension", "$value": {"value": 0.125, "unit": "rem"}},
    "base": {"$type": "dimension", "$value": {"value": 0.25, "unit": "rem"}},
    "md": {"$type": "dimension", "$value": {"value": 0.375, "unit": "rem"}},
    "lg": {"$type": "dimension", "$value": {"value": 0.5, "unit": "rem"}},
    "xl": {"$type": "dimension", "$value": {"value": 0.75, "unit": "rem"}},
    "2xl": {"$type": "dimension", "$value": {"value": 1, "unit": "rem"}},
    "full": {"$type": "dimension", "$value": {"value": 9999, "unit": "px"}}
  }
}
```

The template's `radius.control` aliases one of these steps per brand.

## Shadow (elevation)

DTCG `shadow` objects take `color`, `offsetX`, `offsetY`, `blur`, `spread`; a token whose `$value` is an array stacks several layers. The steps below (`2xs`, `xs`, `sm`, `md`, `lg`, `xl`, `2xl`) use Tailwind CSS v4's own names and values (https://tailwindcss.com/docs/box-shadow, checked 2026-11-07). Tailwind v3 (https://v3.tailwindcss.com/docs/box-shadow, checked 2026-11-07) already used `shadow-md` `0 4px 6px -1px`, `shadow-lg` `0 10px 15px -3px`, `shadow-xl` `0 20px 25px -5px` and `shadow-2xl` `0 25px 50px -12px`. Tailwind v4 (https://tailwindcss.com/docs/box-shadow, checked 2026-11-07) renamed only the two smallest steps (v3 `shadow-sm` became `shadow-xs`, v3 `shadow` became `shadow-sm`) and added `shadow-2xs`, so do not copy a v3 table for those. The `base` label the old skill used for the 4px/6px layer was its own and not a Tailwind name. Every layer here is black at the alpha shown in the table.

```json
{
  "shadow": {
    "2xs": {
      "$type": "shadow",
      "$value": {"color": {"colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.05}, "offsetX": {"value": 0, "unit": "px"}, "offsetY": {"value": 1, "unit": "px"}, "blur": {"value": 0, "unit": "px"}, "spread": {"value": 0, "unit": "px"}}
    },
    "xs": {
      "$type": "shadow",
      "$value": {"color": {"colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.05}, "offsetX": {"value": 0, "unit": "px"}, "offsetY": {"value": 1, "unit": "px"}, "blur": {"value": 2, "unit": "px"}, "spread": {"value": 0, "unit": "px"}}
    },
    "sm": {
      "$type": "shadow",
      "$value": [
        {"color": {"colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.1}, "offsetX": {"value": 0, "unit": "px"}, "offsetY": {"value": 1, "unit": "px"}, "blur": {"value": 3, "unit": "px"}, "spread": {"value": 0, "unit": "px"}},
        {"color": {"colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.1}, "offsetX": {"value": 0, "unit": "px"}, "offsetY": {"value": 1, "unit": "px"}, "blur": {"value": 2, "unit": "px"}, "spread": {"value": -1, "unit": "px"}}
      ]
    }
  }
}
```

Write `md`, `lg`, `xl` and `2xl` the same way from these layers (offsetX 0, offsetY / blur / spread in px, alpha 0.1 except `2xl` layer alpha 0.25):

| Step | Layer 1 | Layer 2 |
| --- | --- | --- |
| md | 0 4px 6px -1px, alpha 0.1 | 0 2px 4px -2px, alpha 0.1 |
| lg | 0 10px 15px -3px, alpha 0.1 | 0 4px 6px -4px, alpha 0.1 |
| xl | 0 20px 25px -5px, alpha 0.1 | 0 8px 10px -6px, alpha 0.1 |
| 2xl | 0 25px 50px -12px, alpha 0.25 | none |

Map steps to roles by elevation: `raised` (cards) `sm`, `overlay` (menus, popovers) `lg`, `modal` `xl`. A shadow never carries state on its own; pair a focus or selected state with an outline or border role.

## Duration, easing and layering

```json
{
  "duration": {
    "fast": {"$type": "duration", "$value": {"value": 150, "unit": "ms"}},
    "normal": {"$type": "duration", "$value": {"value": 200, "unit": "ms"}},
    "slow": {"$type": "duration", "$value": {"value": 300, "unit": "ms"}}
  },
  "easing": {
    "standard": {"$type": "cubicBezier", "$value": [0.4, 0, 0.2, 1]}
  },
  "layer": {
    "dropdown": {"$type": "number", "$value": 1000},
    "sticky": {"$type": "number", "$value": 1100},
    "toast": {"$type": "number", "$value": 1200}
  }
}
```

- Transition tokens are duration plus easing; add `ease-in` and `ease-out` curves only when a component needs them, and honor `prefers-reduced-motion` by setting the durations to 0 in that media query.
- The layer numbers are an example ordering (a named scale beats ad hoc `z-index` values); keep the scale small and name layers by role. A native `<dialog>` opened with `showModal()` sits in the top layer and needs no layer token.
