#!/bin/bash
# Offline tests for calibrate.sh: replay mode on synthetic verdicts, normal mode with a stub `pi`.
set -u
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
CAL="$ROOT/tests/skills/skill-judge/calibrate.sh"
EXP="$ROOT/tests/skills/skill-judge/calibration/expected.json"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
fail=0
check() { # name, ok(0/1)
  if [ "$2" = 0 ]; then echo "PASS $1"; else echo "FAIL $1" >&2; fail=1; fi
}

# gen DIR LANE... : write a passing verdict tree; MUT is python code run on (lane, stem, v, exp) before writing.
gen() {
  python3 - "$ROOT" "$EXP" "$@" <<'PY'
import json, os, re, sys
from pathlib import Path
root, exp, out, *lanes = sys.argv[1:]
rubric = Path(root, "skills/skill-judge/references/rubric.md").read_text()
version = int(re.search(r"rubric_version:\s*(\d+)", rubric).group(1))
sha = re.search(r"spec_sha:\s*([0-9a-f]{40})", rubric).group(1)
MAX = dict(D1=20, D2=15, D3=15, D4=15, D5=15, D6=15, D7=15, D8=15)
files = json.load(open(exp))["files"]
mut = os.environ.get("MUT", "")
for lane in lanes:
    for rel, spec in files.items():
        stem = Path(rel).parent.name if spec["kind"] == "skill" else Path(rel).stem
        bad = spec["band"] == "<60"
        scores = {d: (m * 3 // 10 if bad else m) for d, m in MAX.items()}
        findings = [dict(id=d["id"], dimension=d["dimension"], severity=d.get("severity", "medium"), file=d["file"],
                         line=(d["lines"][0] if d["lines"] else None), evidence="e", fix="f") for d in spec["defects"]]
        v = dict(scores=scores, findings=findings)
        exec(mut, dict(lane=lane, stem=stem, v=v, MAX=MAX))
        total = sum(v["scores"].values()); pct = round(total / 125 * 100, 1)
        grade = next((g for g, f in (("A", 90), ("B", 80), ("C", 70), ("D", 60)) if pct >= f), "F")
        verdict = dict(skill=stem, judge=lane, rubric_version=version, spec_sha=sha, scores=v["scores"], max=MAX,
                       total=total, max_total=125, percent=pct, grade=grade, findings=v["findings"])
        p = Path(out, lane, stem + ".json"); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(verdict))
PY
}
run() { bash "$CAL" "$@" 2>&1; }

# ---- replay mode
gen "$T/ok" lane-a lane-b
out=$(run --verdicts "$T/ok"); rc=$?
check "replay: a clean set passes" $([ $rc = 0 ] && grep -q 'PASS: defect detection' <<<"$out"; echo $?)

MUT='
if stem=="cal-b": 
    for f in v["findings"]: f["file"]="commands/cal-a.md"' gen "$T/wrongfile" lane-a lane-b
out=$(run --verdicts "$T/wrongfile"); rc=$?
check "replay: a wrong-file finding detects nothing" $([ $rc = 1 ] && grep -q 'defects cal-b: 0/6' <<<"$out"; echo $?)

MUT='
if stem=="cal-b":
    v["findings"]=[f for f in v["findings"] if f["dimension"] in ("D5","D1")]
    for f in v["findings"]: f["line"]=None' gen "$T/nullline" lane-a lane-b
out=$(run --verdicts "$T/nullline"); rc=$?
check "replay: a null-line finding detects a lines:null defect but not a ranged one" \
  $(grep -q 'defects cal-b: 1/6' <<<"$out"; echo $?)

MUT='
if stem=="cal-b": v["scores"].update(D1=20, D2=15, D3=15, D4=15, D5=10, D6=0, D7=0, D8=0)' gen "$T/b60" lane-a lane-b   # 75/125 = 60.0
out=$(run --verdicts "$T/b60"); rc=$?
check "replay: a bad file at 60.0 percent fails the band" $([ $rc = 1 ] && grep -q 'FAIL: bands' <<<"$out"; echo $?)

MUT='
if stem=="cal-c": v["scores"]["D1"]=14' gen "$T/g89" lane-a lane-b   # 119/125 -> still >=90
out=$(run --verdicts "$T/g89"); check "replay: a good file at 95.2 passes the band" $([ $? = 0 ]; echo $?)
MUT='
if stem=="cal-c": v["scores"]["D1"]=7' gen "$T/g89b" lane-a lane-b   # 112/125 = 89.6
out=$(run --verdicts "$T/g89b"); rc=$?
check "replay: a good file at 89.6 percent fails the band" $([ $rc = 1 ] && grep -q 'FAIL: bands' <<<"$out"; echo $?)

MUT='
if stem=="cal-d": v["findings"]=v["findings"][:5]' gen "$T/d5" lane-a lane-b
out=$(run --verdicts "$T/d5"); rc=$?
check "replay: 5 of 6 defects (83 percent) passes" $([ $rc = 0 ] && grep -q 'defects cal-d: 5/6' <<<"$out"; echo $?)
MUT='
if stem=="cal-d": v["findings"]=v["findings"][:4]' gen "$T/d4" lane-a lane-b
out=$(run --verdicts "$T/d4"); rc=$?
check "replay: 4 of 6 defects (67 percent) fails" $([ $rc = 1 ] && grep -q 'FAIL: defect detection' <<<"$out"; echo $?)
MUT='
if stem=="cal-d" and lane=="lane-b": v["findings"]=v["findings"][:3]' gen "$T/union" lane-a lane-b
out=$(run --verdicts "$T/union"); rc=$?
check "replay: defects count on at least one lane" $([ $rc = 0 ]; echo $?)

MUT='
if stem=="cal-b": v["scores"]["D7"]=15 if lane=="lane-b" else 0' gen "$T/gapd7" lane-a lane-b   # 12 points of gap from D7
out=$(run --verdicts "$T/gapd7"); rc=$?
check "replay: a lane gap over 10 from D7 fails" $([ $rc = 1 ] && grep -q 'profile dimensions contribute 12.0 of 12.0 (FAIL)' <<<"$out"; echo $?)
MUT='
if stem=="cal-b" and lane=="lane-b": v["scores"]["D1"]=20' gen "$T/gapd1" lane-a lane-b   # 12.8 points from D1
out=$(run --verdicts "$T/gapd1"); rc=$?
check "replay: a lane gap over 10 from D1 is reported, not failed" $([ $rc = 0 ] && grep -q 'profile dimensions contribute 0.0 of 11.2 (reported only)' <<<"$out"; echo $?)

MUT='
if stem=="cal-b" and lane=="lane-b": v["scores"].update(D4=12, D5=12, D7=12, D8=12, D1=6)
if stem=="cal-b" and lane=="lane-a": v["scores"]["D1"]=20' gen "$T/gapmix" lane-a lane-b   # +25.6 from profile, -11.2 from D1: gap 14.4
out=$(run --verdicts "$T/gapmix"); rc=$?
check "replay: a mixed gap mostly from the profile dimensions fails" $([ $rc = 1 ] && grep -q 'profile dimensions contribute 25.6 of 14.4 (FAIL)' <<<"$out"; echo $?)
MUT='
if stem=="cal-b" and lane=="lane-b": v["scores"].update(D1=20, D2=15)
if stem=="cal-b" and lane=="lane-a": v["scores"]["D7"]=12' gen "$T/gapoff" lane-a lane-b   # +20 from D1/D2, -6.4 from D7
out=$(run --verdicts "$T/gapoff"); rc=$?
check "replay: a profile contribution against the gap direction is reported only" $([ $rc = 0 ] && grep -q 'profile dimensions contribute -6.4 of 13.6 (reported only)' <<<"$out"; echo $?)
MUT='
if stem=="cal-b" and lane=="lane-b": v["scores"].update(D7=12, D1=0)
if stem=="cal-b" and lane=="lane-a": v["scores"]["D1"]=0' gen "$T/gaptie" lane-a lane-b
out=$(run --verdicts "$T/gaptie"); rc=$?
check "replay: tied lanes have no gap" $([ $rc = 0 ] && ! grep -q '^gap cal-b' <<<"$out"; echo $?)
out=$(run --verdicts "$T/ok"); rc=$?
check "replay: a skill entry is scored by its directory name and an every-lane-only entry prints no 80% line" \
  $([ $rc = 0 ] && grep -q '^cal-e ' <<<"$out" && ! grep -q 'INVALID' <<<"$out" && ! grep -q '^defects cal-f' <<<"$out" && grep -q '^defects cal-b' <<<"$out"; echo $?)
check "replay: the summary has an every-lane and an absent-findings line" \
  $(grep -q 'PASS: every-lane defects' <<<"$out" && grep -q 'PASS: absent findings' <<<"$out"; echo $?)

MUT='
if stem=="cal-f":
    v["scores"]={d: 0 for d in MAX}
    v["scores"]["D1"]=0' gen "$T/bandany" lane-a lane-b
out=$(run --verdicts "$T/bandany"); rc=$?
check "replay: band any skips the band check" $([ $rc = 0 ] && ! grep -q 'BAD' <<<"$out"; echo $?)

MUT='
if stem=="cal-f" and lane=="lane-b": v["findings"]=[]' gen "$T/everymiss" lane-a lane-b
out=$(run --verdicts "$T/everymiss"); rc=$?
check "replay: an every-lane defect missed on one lane fails" $([ $rc = 1 ] && grep -q 'FAIL: every-lane defects' <<<"$out"; echo $?)

MUT='
if stem=="cal-f":
    for f in v["findings"]: f["severity"]="medium"' gen "$T/sevlow" lane-a lane-b
out=$(run --verdicts "$T/sevlow"); rc=$?
check "replay: a severity defect matched only by a lower severity fails" $([ $rc = 1 ] && grep -q 'FAIL: every-lane defects' <<<"$out"; echo $?)

MUT='
if stem=="cal-f":
    for f in v["findings"]: f["severity"]="critical"' gen "$T/sevhigh" lane-a lane-b
out=$(run --verdicts "$T/sevhigh"); rc=$?
check "replay: a severity defect is matched by a higher severity" $([ $rc = 0 ]; echo $?)

MUT='
if stem=="cal-g" and lane=="lane-b":
    v["findings"]=[dict(id="X", dimension="D1", severity="high", file="skills/cal-g/SKILL.md", line=None, evidence="e", fix="f")]' gen "$T/absent" lane-a lane-b
out=$(run --verdicts "$T/absent"); rc=$?
check "replay: an absent finding present on one lane fails" $([ $rc = 1 ] && grep -q 'FAIL: absent findings' <<<"$out"; echo $?)

MUT='
if stem=="cal-g" and lane=="lane-b":
    v["findings"]=[dict(id="X", dimension="D1", severity="medium", file="skills/cal-g/SKILL.md", line=None, evidence="e", fix="f")]' gen "$T/absentlow" lane-a lane-b
out=$(run --verdicts "$T/absentlow"); rc=$?
check "replay: an absent finding of a lower severity does not fail" $([ $rc = 0 ]; echo $?)

MUT='
if stem=="cal-f" and lane=="lane-b": v["scores"]["D7"]=0' gen "$T/gapskill" lane-a lane-b   # 12 points of gap from D7
out=$(run --verdicts "$T/gapskill"); rc=$?
check "replay: a lane gap from D7 on a skill entry is reported only" \
  $([ $rc = 0 ] && grep -q '^gap cal-f.*(reported only)' <<<"$out"; echo $?)

gen "$T/one" lane-a
out=$(run --verdicts "$T/one" --min-lanes 1); rc=$?
check "replay: --min-lanes 1 accepts one valid lane" $([ $rc = 0 ] && grep -q 'PASS: bands' <<<"$out"; echo $?)
out=$(run --verdicts "$T/one"); rc=$?
check "replay: the default rejects one valid lane" $([ $rc = 1 ] && grep -q 'fewer than two lanes' <<<"$out"; echo $?)

gen "$T/dup" lane-a
out=$(run --verdicts "$T/dup" Lane/A lane-a); rc=$?
check "replay: repeated lane slugs are rejected" $([ $rc = 2 ] && grep -q 'duplicate lane' <<<"$out"; echo $?)

gen "$T/inv" lane-a lane-b
python3 - "$T/inv/lane-b/cal-a.json" <<'PY'
import json, sys
p = sys.argv[1]; v = json.load(open(p)); v["percent"] = 12.3; json.dump(v, open(p, "w"))
PY
out=$(run --verdicts "$T/inv"); rc=$?
check "replay: an invalid verdict is reported and leaves one valid lane" \
  $([ $rc = 1 ] && grep -q 'INVALID lane-b cal-a' <<<"$out" && grep -q 'fewer than two lanes' <<<"$out"; echo $?)

# ---- normal mode with a stub pi
mkdir -p "$T/bin"
cat > "$T/bin/pi" <<'STUB'
#!/bin/bash
# Records cwd, args and stdin; prints the canned verdict of the lane/stem named in the prompt; fails on request.
n=$(ls "$STUB_LOG" | wc -l); d="$STUB_LOG/call-$n"; mkdir -p "$d"
pwd > "$d/cwd"; printf '%s\n' "$@" > "$d/args"; cat > "$d/stdin"
find . -type f | sort > "$d/tree"
stem=$(sed -n -e 's/^You are judge .*Judge this [a-z]*: \(.*\)$/\1/p' -e 's/^You are judge .*Judge these skills: \(.*\)$/\1/p' "$d/stdin" | head -1)
model=$(grep -A1 -x -- '--model' "$d/args" | tail -1)
lane=$(echo "$model" | tr 'A-Z' 'a-z' | sed 's/[^a-z0-9]\+/-/g; s/^-//; s/-$//')
echo "$lane $stem" > "$d/who"
f="$STUB_FAIL/$lane-$stem"
if [ -f "$f" ] && [ "$(cat "$f")" -gt 0 ]; then echo $(( $(cat "$f") - 1 )) > "$f"; echo "stub failure" >&2; exit 1; fi
python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))))' "$STUB_VERDICTS/$lane/$stem.json"
x="$STUB_EXTRA/$lane-$stem"  # an unsolicited verdict for another stem
[ -f "$x" ] && python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))))' "$STUB_VERDICTS/$lane/$(cat "$x").json"
STUB
chmod +x "$T/bin/pi"
L1=router-env-lane-one; L2=router-env-lane-two
gen "$T/canned" $L1 $L2
export STUB_VERDICTS="$T/canned" STUB_EXTRA="$T/extra"; mkdir -p "$T/extra"
nrun() { # logdir failcounts-dir
  rm -rf "$1" "$T/out"; mkdir -p "$1" "$2"
  STUB_LOG="$1" STUB_FAIL="$2" PATH="$T/bin:$PATH" run --out "$T/out" router-env/lane-one router-env/lane-two
}

out=$(nrun "$T/log1" "$T/fail1"); rc=$?
check "normal: two good lanes pass" $([ $rc = 0 ] && grep -q 'PASS: bands' <<<"$out"; echo $?)
check "normal: fourteen judge calls, one per lane and file (seven entries on two lanes)" $([ "$(ls "$T/log1" | wc -l)" = 14 ]; echo $?)
cwd=$(cat "$T/log1/call-0/cwd")
check "normal: the cwd is a scratch root outside the repository" $([ -n "$cwd" ] && [ "${cwd#"$ROOT"}" = "$cwd" ]; echo $?)
bad=0
for d in "$T"/log1/call-*; do
  [ "$(cat "$d/cwd")" = "$cwd" ] || bad=1
  grep -q '^skills/skill-judge/SKILL.md$\|^./skills/skill-judge/SKILL.md$' "$d/tree" || bad=1
  grep -q 'expected.json' "$d/tree" "$d/stdin" "$d/args" && bad=1
  grep -q 'tests/' "$d/tree" && bad=1
  # every absolute path in the prompt is inside the scratch root
  while read -r p; do case $p in "$cwd"|"$cwd"/*) ;; *) bad=1 ;; esac; done < <(grep -o '/[A-Za-z0-9_./-]*' "$d/stdin" | grep -E '^/(tmp|var|home)' )
done
check "normal: scratch tree and prompt hold no answer key and every prompt path is inside the scratch root" $bad
bad=0
for d in "$T"/log1/call-*; do
  grep -q 'tests/skills/skill-judge/calibration' "$d/stdin" "$d/args" && bad=1
  grep -q '^\./previous\|^previous' "$d/tree" && bad=1
  [ -f "$d/cwd" ] || bad=1
  read -r _ stem < "$d/who"
  case $stem in
    cal-f|cal-g) grep -q "^=== previous-version digest: $stem at $stem ===$" "$d/stdin" || bad=1 ;;
    *) grep -q '^=== previous-version digest' "$d/stdin" && bad=1 ;;
  esac
  case $stem in
    cal-f) grep -q '^- para:' "$d/stdin" || bad=1 ;;
    cal-g) grep -q '^- para:' "$d/stdin" && bad=1 ;;
  esac
done
check "normal: skills are copied into the scratch root, a previous digest (relative SRC) is passed only for entries that have one, and no prompt shows the fixture tree" $bad
check "normal: every skill entry gets a call named by its directory (cal-e, cal-f, cal-g on each lane)" \
  $([ "$(grep -l -x -e "$L1 cal-e" -e "$L2 cal-e" -e "$L1 cal-f" -e "$L2 cal-f" -e "$L1 cal-g" -e "$L2 cal-g" "$T"/log1/call-*/who | wc -l)" = 6 ]; echo $?)
check "normal: an every-lane-only entry prints no 80% line in a normal round" $(! grep -q '^defects cal-f' <<<"$out"; echo $?)
check "normal: the judge command is the audit pi-cmd judge line" \
  $(grep -qx -- '--tools' "$T/log1/call-0/args" && grep -qx -- 'read,grep,find,ls' "$T/log1/call-0/args"; echo $?)

out=$(rm -rf "$T/log2" "$T/out"; mkdir -p "$T/log2" "$T/fail2"; echo 1 > "$T/fail2/$L1-cal-a"
      STUB_LOG="$T/log2" STUB_FAIL="$T/fail2" PATH="$T/bin:$PATH" run --out "$T/out" router-env/lane-one router-env/lane-two); rc=$?
n=$(grep -l "^$L1 cal-a$" "$T"/log2/call-*/who | wc -l)
check "normal: one harness failure is retried once and the round passes" $([ $rc = 0 ] && [ "$n" = 2 ]; echo $?)

out=$(rm -rf "$T/log3" "$T/out"; mkdir -p "$T/log3" "$T/fail3"; echo 5 > "$T/fail3/$L1-cal-a"
      STUB_LOG="$T/log3" STUB_FAIL="$T/fail3" PATH="$T/bin:$PATH" run --out "$T/out" router-env/lane-one router-env/lane-two); rc=$?
n=$(grep -l "^$L1 cal-a$" "$T"/log3/call-*/who | wc -l)
check "normal: a persistent failure is retried exactly once, then fewer than two lanes exits 1" \
  $([ $rc = 1 ] && [ "$n" = 2 ] && grep -q 'fewer than two lanes' <<<"$out"; echo $?)

out=$(rm -rf "$T/log5" "$T/out"; mkdir -p "$T/log5" "$T/fail5"; echo 5 > "$T/fail5/$L1-cal-a"; echo cal-a > "$T/extra/$L1-cal-b"
      STUB_LOG="$T/log5" STUB_FAIL="$T/fail5" PATH="$T/bin:$PATH" run --out "$T/out" router-env/lane-one router-env/lane-two); rc=$?
check "normal: an unsolicited verdict does not resurrect a failed artifact" \
  $([ $rc = 1 ] && [ ! -e "$T/out/judgements/$L1/cal-a.json" ] && grep -q "INVALID $L1 cal-a" <<<"$out"; echo $?)
rm -f "$T/extra/$L1-cal-b"
out=$(run --verdicts "$T/canned" router-env/lane-one router-env/lane-one); rc=$?
check "replay: a repeated model id is rejected" $([ $rc = 2 ] && grep -q 'duplicate lane' <<<"$out"; echo $?)
out=$(rm -rf "$T/log6" "$T/out"; mkdir -p "$T/log6" "$T/fail6"
      STUB_LOG="$T/log6" STUB_FAIL="$T/fail6" PATH="$T/bin:$PATH" run --out "$T/out" router-env/lane-one Router-Env/Lane_One); rc=$?
check "normal: a slug collision is rejected without any judge call" $([ $rc = 2 ] && [ -z "$(ls "$T/log6")" ]; echo $?)

out=$(rm -rf "$T/log4" "$T/out"; mkdir -p "$T/log4" "$T/fail4"; for s in cal-a cal-b cal-c cal-d; do echo 9 > "$T/fail4/$L2-$s"; done
      STUB_LOG="$T/log4" STUB_FAIL="$T/fail4" PATH="$T/bin:$PATH" run --out "$T/out" router-env/lane-one router-env/lane-two); rc=$?
check "normal: only one successful lane exits 1" $([ $rc = 1 ]; echo $?)

out=$(rm -rf "$T/log7" "$T/out"; mkdir -p "$T/log7" "$T/fail7"
      STUB_LOG="$T/log7" STUB_FAIL="$T/fail7" PATH="$T/bin:$PATH" run --out "$T/out" router-env/lane-one); rc=$?
check "normal: one model is a usage error by default" $([ $rc = 2 ] && [ -z "$(ls "$T/log7")" ]; echo $?)
out=$(rm -rf "$T/log8" "$T/out"; mkdir -p "$T/log8" "$T/fail8"
      STUB_LOG="$T/log8" STUB_FAIL="$T/fail8" PATH="$T/bin:$PATH" run --min-lanes 1 --out "$T/out" router-env/lane-one); rc=$?
check "normal: --min-lanes 1 runs one model (seven calls) and passes" $([ $rc = 0 ] && [ "$(ls "$T/log8" | wc -l)" = 7 ]; echo $?)

[ "$fail" = 0 ] && echo "PASS calibrate.sh"
exit "$fail"
