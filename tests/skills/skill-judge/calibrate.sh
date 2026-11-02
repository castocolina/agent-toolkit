#!/bin/bash
# Calibrate the command and agent judge profiles on a fixed four-file set.
# usage: calibrate.sh [--verdicts DIR] [--out DIR] MODEL...
#   normal mode: judge every calibration file once per MODEL in a scratch root, then score.
#   --verdicts DIR: skip dispatch and score an existing <lane-slug>/<stem>.json tree.
# Lane gap rule: per file, when the highest and lowest lane differ by more than 10 percentage points, the signed
# D4+D5+D7+D8 difference (higher minus lower lane, as points of the total) must not exceed half of that gap.
# Duplicate lane slugs exit 2 before any dispatch.
# Exit 0 only when every criterion passes; 1 on a failed round or fewer than two valid lanes; 2 on usage.
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
AUDIT=$REPO/scripts/audit/audit.py
CAL=$HERE/calibration
EXPECTED=${CAL_EXPECTED:-$CAL/expected.json}

verdicts=""
out="$REPO/docs/audit/$(date +%F)-calibration"
models=()
while (($#)); do
  case $1 in
    --verdicts) verdicts=${2:?--verdicts needs a directory}; shift 2 ;;
    --out) out=${2:?--out needs a directory}; shift 2 ;;
    -h|--help) sed -n 2,6p "$0"; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) models+=("$1"); shift ;;
  esac
done
if [[ -z $verdicts && ${#models[@]} -lt 2 ]]; then
  echo "usage: calibrate.sh [--verdicts DIR] [--out DIR] MODEL...  (normal mode needs two or more models)" >&2
  exit 2
fi

lanes=()
for m in "${models[@]}"; do lanes+=("$(python3 "$AUDIT" slug "$m")"); done
if [[ -n $(printf '%s\n' "${lanes[@]}" | sort | uniq -d) ]]; then
  echo "duplicate lane (repeated model or colliding slug): ${models[*]}" >&2
  exit 2
fi

if [[ -z $verdicts ]]; then
  SCR=$(mktemp -d) ATTROOT=$(mktemp -d)  # attempts live outside the judge-visible scratch root
  trap 'rm -rf "$SCR" "$ATTROOT"' EXIT
  # The judge sees only the judge skill, the spec notes and the calibration files; never expected.json.
  mkdir -p "$SCR/skills" "$SCR/docs/audit" "$out/judgements"
  cp -r "$REPO/skills/skill-judge" "$SCR/skills/skill-judge"
  cp "$REPO/docs/audit/artifact-specs.md" "$SCR/docs/audit/"
  cp -r "$CAL/commands" "$CAL/agents" "$SCR/"
  mapfile -t files < <(python3 -c 'import json,sys; [print(k, v["kind"]) for k, v in json.load(open(sys.argv[1]))["files"].items()]' "$EXPECTED")
  for i in "${!models[@]}"; do
    model=${models[$i]}; lane=${lanes[$i]}
    mapfile -d '' -t cmd < <(python3 "$AUDIT" pi-cmd judge --model "$model" --print0)
    for entry in "${files[@]}"; do
      rel=${entry% *}; kind=${entry##* }; stem=$(basename "$rel" .md)
      dest=$out/judgements/$lane/$stem.json
      rm -f "$dest"
      for attempt in 1 2; do  # a harness failure (no valid verdict) is retried once
        prompt=$(python3 "$AUDIT" --root "$SCR" judge-prompt --kind "$kind" --artifact "$SCR/$rel" --judge "$lane")
        att=$(mktemp -d -p "$ATTROOT")  # only the requested stem is published from an attempt
        (cd "$SCR" && "${cmd[@]}" <<<"$prompt") 2>>"$out/harness.log" \
          | python3 "$AUDIT" split-verdicts --judge "$model" --out "$att" 2>>"$out/harness.log" || true
        if [[ -f $att/$lane/$stem.json ]] && python3 "$AUDIT" validate-verdict "$att/$lane/$stem.json" 2>/dev/null; then
          mkdir -p "$(dirname "$dest")" && mv "$att/$lane/$stem.json" "$dest"; rm -rf "$att"; break
        fi
        rm -rf "$att"
        echo "lane $lane $stem: no valid verdict (attempt $attempt)" >&2
      done
    done
  done
  verdicts=$out/judgements
fi

python3 - "$EXPECTED" "$verdicts" "$AUDIT" "${lanes[@]}" <<'PY'
import json, subprocess, sys
from pathlib import Path

expected = json.load(open(sys.argv[1]))["files"]
vdir, audit, lanes = Path(sys.argv[2]), sys.argv[3], sys.argv[4:]
lanes = list(dict.fromkeys(lanes or sorted(p.name for p in vdir.iterdir() if p.is_dir())))
GAP_FAILS = {"D4", "D5", "D7", "D8"}  # a lane gap from these dimensions fails the round
ok = True


def load(lane, stem):
    path = vdir / lane / f"{stem}.json"
    if not path.is_file():
        return None, "missing"
    r = subprocess.run([sys.executable, audit, "validate-verdict", str(path)], capture_output=True, text=True)
    if r.returncode:
        return None, "invalid: " + (r.stderr.strip().splitlines() or ["?"])[0]
    return json.loads(path.read_text()), ""


data, valid = {}, []
for lane in lanes:
    good = True
    for rel in expected:
        stem = Path(rel).stem
        v, why = load(lane, stem)
        if v is None:
            print(f"INVALID {lane} {stem}: {why}")
            good = False
        else:
            data[lane, rel] = v
    if good:
        valid.append(lane)
if len(valid) < 2:
    print(f"FAIL: fewer than two lanes have valid verdicts for every file (valid: {valid or 'none'})")
    sys.exit(1)


def detects(finding, defect):
    if finding["file"] != defect["file"] or finding["dimension"] != defect["dimension"]:
        return False
    return defect["lines"] is None or (finding["line"] is not None and defect["lines"][0] <= finding["line"] <= defect["lines"][1])


print(f"{'file':<16}{'lane':<28}{'percent':>8}  band   defects detected / missed")
detected = {}
band_ok = True
for rel, spec in expected.items():
    for lane in valid:
        v = data[lane, rel]
        pct = v["percent"]
        good_band = pct >= 90 if spec["band"] == ">=90" else pct < 60
        band_ok &= good_band
        hit = [d["id"] for d in spec["defects"] if any(detects(f, d) for f in v["findings"])]
        detected.setdefault(rel, set()).update(hit)
        miss = [d["id"] for d in spec["defects"] if d["id"] not in hit]
        extra = f"{','.join(hit) or '-'} / {','.join(miss) or '-'}" if spec["defects"] else ""
        print(f"{Path(rel).stem:<16}{lane:<28}{pct:>8}  {spec['band']:<5} {'ok' if good_band else 'BAD'}  {extra}")

det_ok = True
for rel, spec in expected.items():
    if spec["defects"]:
        n, total = len(detected[rel]), len(spec["defects"])
        good = n / total >= 0.8
        det_ok &= good
        print(f"defects {Path(rel).stem}: {n}/{total} detected on at least one lane ({'ok' if good else 'BAD'})")

gap_ok = True
for rel in expected:
    hi = max((data[lane, rel] for lane in valid), key=lambda v: v["percent"])
    lo = min((data[lane, rel] for lane in valid), key=lambda v: v["percent"])
    gap = hi["percent"] - lo["percent"]
    if gap > 10:
        # signed contribution (in percentage points) of the profile dimensions to the higher lane's lead
        prof = sum(hi["scores"][d] - lo["scores"][d] for d in GAP_FAILS) / hi["max_total"] * 100
        fails = prof > gap / 2 + 1e-9
        gap_ok &= not fails
        print(f"gap {Path(rel).stem}: {gap:.1f} points, profile dimensions contribute {prof:.1f} of {gap:.1f} ({'FAIL' if fails else 'reported only'})")

print()
for name, res in (("bands (good >=90, bad <60, every lane)", band_ok),
                  ("defect detection (>=80% per bad file)", det_ok),
                  ("lane gap (D4/D5/D7/D8 not over half of it)", gap_ok)):
    print(f"{'PASS' if res else 'FAIL'}: {name}")
sys.exit(0 if band_ok and det_ok and gap_ok else 1)
PY
