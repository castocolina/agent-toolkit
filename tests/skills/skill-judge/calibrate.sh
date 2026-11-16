#!/bin/bash
# Calibrate the skill, command and agent judge on a fixed set (see calibration/expected.json).
# usage: calibrate.sh [--verdicts DIR] [--out DIR] [--min-lanes N] MODEL...
#   normal mode: judge every calibration file once per MODEL in a scratch root, then score.
#   --verdicts DIR: skip dispatch and score an existing <lane-slug>/<stem>.json tree (a skill's stem is its directory name).
#   --min-lanes N: valid lanes needed (default 2); normal mode needs at least N models.
# Lane gap rule: per file, when the highest and lowest lane differ by more than 10 percentage points, the signed
# D4+D5+D7+D8 difference (higher minus lower lane, as points of the total) must not exceed half of that gap.
# It fails the round only for command and agent entries; a skill entry's gap is reported only.
# Duplicate lane slugs exit 2 before any dispatch.
# Exit 0 only when every criterion passes; 1 on a failed round or fewer than N valid lanes; 2 on usage.
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
AUDIT=$REPO/scripts/audit/audit.py
CAL=$HERE/calibration
EXPECTED=${CAL_EXPECTED:-$CAL/expected.json}

verdicts=""
out="$REPO/docs/audit/$(date +%F)-calibration"
models=()
min_lanes=2
while (($#)); do
  case $1 in
    --verdicts) verdicts=${2:?--verdicts needs a directory}; shift 2 ;;
    --out) out=${2:?--out needs a directory}; shift 2 ;;
    --min-lanes) min_lanes=${2:?--min-lanes needs a number}; shift 2 ;;
    -h|--help) sed -n 2,9p "$0"; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) models+=("$1"); shift ;;
  esac
done
if [[ ! $min_lanes =~ ^[1-9][0-9]*$ ]]; then
  echo "--min-lanes needs a positive integer: $min_lanes" >&2
  exit 2
fi
if [[ -z $verdicts && ${#models[@]} -lt $min_lanes ]]; then
  echo "usage: calibrate.sh [--verdicts DIR] [--out DIR] [--min-lanes N] MODEL...  (normal mode needs $min_lanes or more models)" >&2
  exit 2
fi

lanes=()
for m in "${models[@]}"; do lanes+=("$(python3 "$AUDIT" slug "$m")"); done
if [[ -n $(printf '%s\n' "${lanes[@]}" | sort | uniq -d) ]]; then
  echo "duplicate lane (repeated model or colliding slug): ${models[*]}" >&2
  exit 2
fi

if [[ -z $verdicts ]]; then
  SCR=$(mktemp -d) ATTROOT=$(mktemp -d) PREV=$(mktemp -d)  # attempts and previous copies live outside the judge-visible scratch root
  trap 'rm -rf "$SCR" "$ATTROOT" "$PREV"' EXIT
  # The judge sees only the judge skill, the spec notes and the calibration files; never expected.json.
  mkdir -p "$SCR/skills" "$SCR/docs/audit" "$out/judgements"
  cp -r "$REPO/skills/skill-judge" "$SCR/skills/skill-judge"
  cp "$REPO/docs/audit/artifact-specs.md" "$SCR/docs/audit/"
  cp -r "$CAL/commands" "$CAL/agents" "$SCR/"
  cp -r "$CAL/skills/." "$SCR/skills/"
  # one line per entry: <path> <kind> <previous copy relative to calibration/, or ->
  mapfile -t files < <(python3 -c 'import json,sys; [print(k, v["kind"], v.get("previous") or "-") for k, v in json.load(open(sys.argv[1]))["files"].items()]' "$EXPECTED")
  for entry in "${files[@]}"; do
    read -r rel kind prevsrc <<<"$entry"
    [[ $prevsrc == - ]] || cp -r "$CAL/$prevsrc" "$PREV/$(basename "$(dirname "$rel")")"
  done
  for i in "${!models[@]}"; do
    model=${models[$i]}; lane=${lanes[$i]}
    mapfile -d '' -t cmd < <(python3 "$AUDIT" pi-cmd judge --model "$model" --print0)
    for entry in "${files[@]}"; do
      read -r rel kind prevsrc <<<"$entry"
      if [[ $kind == skill ]]; then stem=$(basename "$(dirname "$rel")"); else stem=$(basename "$rel" .md); fi
      dest=$out/judgements/$lane/$stem.json
      rm -f "$dest"
      for attempt in 1 2; do  # a harness failure (no valid verdict) is retried once
        # an unresolvable --previous makes judge-prompt exit 2 and stops the run (set -e)
        if [[ $prevsrc == - ]]; then
          prompt=$(python3 "$AUDIT" --root "$SCR" judge-prompt --kind "$kind" --artifact "$SCR/$rel" --judge "$lane")
        else  # run from $PREV so the judge is never shown where the previous copy lives
          prompt=$(cd "$PREV" && python3 "$AUDIT" --root "$SCR" judge-prompt --kind "$kind" --artifact "$SCR/$rel" --judge "$lane" --previous "$stem")
        fi
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

MIN_LANES=$min_lanes python3 - "$EXPECTED" "$verdicts" "$AUDIT" "${lanes[@]}" <<'PY'
import json, os, subprocess, sys
from pathlib import Path

expected = json.load(open(sys.argv[1]))["files"]
vdir, audit, lanes = Path(sys.argv[2]), sys.argv[3], sys.argv[4:]
lanes = list(dict.fromkeys(lanes or sorted(p.name for p in vdir.iterdir() if p.is_dir())))
min_lanes = int(os.environ.get("MIN_LANES", "2"))
GAP_FAILS = {"D4", "D5", "D7", "D8"}  # a lane gap from these dimensions fails the round
SEV = {"low": 0, "medium": 1, "high": 2, "critical": 3}
ok = True


def stem_of(rel):  # a skill's verdict stem is its directory name, not SKILL
    return Path(rel).parent.name if expected[rel]["kind"] == "skill" else Path(rel).stem


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
        stem = stem_of(rel)
        v, why = load(lane, stem)
        if v is None:
            print(f"INVALID {lane} {stem}: {why}")
            good = False
        else:
            data[lane, rel] = v
    if good:
        valid.append(lane)
if len(valid) < min_lanes:
    word = {1: "one", 2: "two", 3: "three"}.get(min_lanes, str(min_lanes))
    print(f"FAIL: fewer than {word} lanes have valid verdicts for every file (valid: {valid or 'none'})")
    sys.exit(1)


def detects(finding, defect):
    if finding["file"] != defect["file"] or finding["dimension"] != defect["dimension"]:
        return False
    if SEV[finding["severity"]] < SEV[defect.get("severity", "low")]:  # a severity defect needs that severity or higher
        return False
    return defect["lines"] is None or (finding["line"] is not None and defect["lines"][0] <= finding["line"] <= defect["lines"][1])


print(f"{'file':<16}{'lane':<28}{'percent':>8}  band   defects detected / missed")
detected = {}
band_ok = True
every_ok = True
absent_ok = True
for rel, spec in expected.items():
    for lane in valid:
        v = data[lane, rel]
        pct = v["percent"]
        good_band = True if spec["band"] == "any" else pct >= 90 if spec["band"] == ">=90" else pct < 60
        band_ok &= good_band
        hit = [d["id"] for d in spec["defects"] if any(detects(f, d) for f in v["findings"])]
        detected.setdefault(rel, set()).update(d for d in hit if not next(x for x in spec["defects"] if x["id"] == d).get("every_lane"))
        for d in spec["defects"]:
            if d.get("every_lane") and d["id"] not in hit:
                every_ok = False
                print(f"every-lane defect {d['id']} of {stem_of(rel)} missed on {lane}")
        for a in spec.get("absent", []):
            if any(detects(f, a) for f in v["findings"]):
                absent_ok = False
                print(f"absent finding {a['id']} of {stem_of(rel)} present on {lane}")
        miss = [d["id"] for d in spec["defects"] if d["id"] not in hit]
        extra = f"{','.join(hit) or '-'} / {','.join(miss) or '-'}" if spec["defects"] else ""
        print(f"{stem_of(rel):<16}{lane:<28}{pct:>8}  {spec['band']:<5} {'ok' if good_band else 'BAD'}  {extra}")

det_ok = True
for rel, spec in expected.items():
    counted = [d for d in spec["defects"] if not d.get("every_lane")]
    if counted:  # an entry with only every-lane defects has no 80% line
        n, total = len(detected[rel]), len(counted)
        good = n / total >= 0.8
        det_ok &= good
        print(f"defects {stem_of(rel)}: {n}/{total} detected on at least one lane ({'ok' if good else 'BAD'})")

gap_ok = True
for rel, spec in expected.items():
    hi = max((data[lane, rel] for lane in valid), key=lambda v: v["percent"])
    lo = min((data[lane, rel] for lane in valid), key=lambda v: v["percent"])
    gap = hi["percent"] - lo["percent"]
    if gap > 10:
        # signed contribution (in percentage points) of the profile dimensions to the higher lane's lead
        prof = sum(hi["scores"][d] - lo["scores"][d] for d in GAP_FAILS) / hi["max_total"] * 100
        # the gap rule is a plan 12 criterion for command and agent profiles; a skill entry's gap is only reported
        fails = prof > gap / 2 + 1e-9 and spec["kind"] in ("command", "agent")
        gap_ok &= not fails
        print(f"gap {stem_of(rel)}: {gap:.1f} points, profile dimensions contribute {prof:.1f} of {gap:.1f} ({'FAIL' if fails else 'reported only'})")

print()
for name, res in (("bands (good >=90, bad <60, every lane)", band_ok),
                  ("defect detection (>=80% per bad file)", det_ok),
                  ("every-lane defects (detected on every valid lane)", every_ok),
                  ("absent findings (on no valid lane)", absent_ok),
                  ("lane gap (D4/D5/D7/D8 not over half of it, command and agent entries)", gap_ok)):
    print(f"{'PASS' if res else 'FAIL'}: {name}")
sys.exit(0 if band_ok and det_ok and every_ok and absent_ok and gap_ok else 1)
PY
