# Token checks

Runnable checks for workflow step 4. Each takes its input as arguments; adjust only the arguments.

## Alias resolution

Prints `{"missing": [...], "cycles": [...]}`; both lists must be empty before component work. On the eval fixture `broken-tokens.json` it reports `color.gray.350` missing and the `brand.primary` / `action.default` cycle.

```bash
python3 - path/to/tokens.json <<'PY'
import json, re, sys
tokens = {}
def walk(node, path=''):
    if '$value' in node:
        tokens[path] = node['$value']
        return
    for k, v in node.items():
        if not k.startswith('$') and isinstance(v, dict):
            walk(v, f'{path}.{k}' if path else k)
def refs(v):
    if isinstance(v, str):
        return re.findall(r'^\{([^{}]+)\}$', v)
    items = v.values() if isinstance(v, dict) else v if isinstance(v, list) else []
    return [r for x in items for r in refs(x)]
walk(json.load(open(sys.argv[1])))
missing, cycles, done = [], [], set()
def visit(p, stack):
    if p in stack:
        cycles.append(stack[stack.index(p):] + [p])
        return
    if p in done:
        return
    for r in refs(tokens[p]):
        if r in tokens:
            visit(r, stack + [p])
        else:
            missing.append({'token': p, 'ref': r})
    done.add(p)
for p in tokens:
    visit(p, [])
print(json.dumps({'missing': missing, 'cycles': cycles}))
PY
```

## Contrast ratio

Large text for the 3:1 threshold means at least 18pt, or at least 14pt bold (or the CJK equivalent); anything smaller is normal text and needs 4.5:1 (WCAG 2.2 SC 1.4.3, https://www.w3.org/TR/WCAG22/, checked 2026-11-07). Essential UI boundaries (SC 1.4.11) also need 3:1.

Arguments: foreground, background, threshold (4.5 or 3), and (only when the background is translucent) the opaque surface beneath it. Hex as `#rgb`, `#rrggbb`, `#rgba` or `#rrggbbaa`. Foreground alpha is composited over the background; a translucent background is first composited over its own underlying surface, never assumed opaque. Pass/fail compares the unrounded ratio, so 4.499 never passes as 4.5; `display` is for the table only. This example prints `{"ratio": 2.5388, "display": 2.54, "threshold": 4.5, "pass": false}`.

```bash
python3 - '#9ca3af' '#fff' 4.5 <<'PY'
import json, sys
def rgba(h):
    h = h.lstrip('#'); h = ''.join(c * 2 for c in h) if len(h) in (3, 4) else h
    v = [int(h[i:i + 2], 16) / 255 for i in range(0, len(h), 2)]
    return v[:3], (v[3] if len(v) == 4 else 1.0)
over = lambda top, a, under: [a * x + (1 - a) * y for x, y in zip(top, under)]
(f, fa), (b, ba) = rgba(sys.argv[1]), rgba(sys.argv[2])
if ba < 1:  # translucent background: composite it over its own underlying surface first
    if len(sys.argv) < 5: sys.exit('translucent background: pass the opaque surface beneath it as a fourth argument')
    b = over(b, ba, rgba(sys.argv[4])[0])
f = over(f, fa, b)
L = lambda c: sum(w * (x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for w, x in zip((0.2126, 0.7152, 0.0722), c))
hi, lo = sorted((L(f), L(b)), reverse=True)
ratio, threshold = (hi + 0.05) / (lo + 0.05), float(sys.argv[3])
print(json.dumps({'ratio': round(ratio, 4), 'display': round(ratio, 2), 'threshold': threshold, 'pass': ratio >= threshold}))
PY
```

## Wide-gamut colors

Convert `oklch()` or `display-p3` values to sRGB before measuring, keeping alpha (`formatHex8`), then pass the 8-digit hex to the contrast script. Run in a directory with `culori@4` installed (`npm i culori@4`); this prints `#00c24899`:

```bash
node --input-type=module -e "import { parse, toGamut, formatHex8 } from 'culori'; console.log(formatHex8(toGamut('rgb', 'oklch')(parse(process.argv[1]))))" 'oklch(0.7 0.35 150 / 0.6)'
```

Out-of-gamut colors change when mapped, so report the converted hex next to the ratio: the original value's contrast is not what renders on sRGB screens.
