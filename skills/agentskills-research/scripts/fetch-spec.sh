#!/bin/bash
# Fetch the Agent Skills docs + reference validator at one commit SHA into DEST,
# with rollback. stdout: one JSON object; status/errors: stderr. Run from the repo root.
set -e
set -o pipefail

usage() {
  cat <<'USAGE'
usage: fetch-spec.sh [--dest DIR] [--ref REF] [--rubric FILE] [-h|--help]

Fetch the Agent Skills docs and the skills-ref validator at one commit into
DEST (default skills/skill-judge/references/agentskills), with rollback.
Run from the repo root. Normally run with no options.

Options:
  --ref REF      upstream branch to resolve to a commit (default main)
  --dest DIR     reference directory (tests only)
  --rubric FILE  rubric whose spec_sha is compared with the pin (tests only;
                 default DEST/../rubric.md)

Environment:
  AGENTSKILLS_SHA       use this 40-hex commit instead of resolving --ref
  AGENTSKILLS_RAW_BASE  download base URL (tests only; default
                        https://raw.githubusercontent.com/agentskills/agentskills)

Prerequisites: bash 4+ (declare -A), curl, jq, git, GNU sha256sum.

stdout: one JSON object with these fields
  ref           the --ref used
  resolved      the commit fetched
  sha           the pin recorded in SOURCE.json (stays the old sha when nothing changed)
  changed       reference files rewritten (new upstream, missing or hand-edited)
  unchanged     reference files already matching upstream
  rubric_stale  true when the rubric's spec_sha differs from sha, or the rubric is missing
stderr: status and errors.

Exit codes: 0 success; 1 any failure (references are rolled back if the failure happened during
publish; a later failure leaves the new references in place; a failed rollback
is reported on stderr with the backup directory).
USAGE
}

DEST=
REF=main
RUBRIC=
while [ $# -gt 0 ]; do
  case $1 in
    --dest) DEST=$2; shift 2 ;;
    --ref) REF=$2; shift 2 ;;
    --rubric) RUBRIC=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "usage: fetch-spec.sh [--dest DIR] [--ref REF] [--rubric FILE] [-h|--help]" >&2; exit 1 ;;
  esac
done
if [ -z "$DEST" ]; then # the default is cwd-relative: refuse to build a fresh tree elsewhere
  [ -f scripts/build_plugins.py ] || { echo "fetch-spec: run from the repo root (or pass --dest)" >&2; exit 1; }
  DEST=skills/skill-judge/references/agentskills
fi
RUBRIC=${RUBRIC:-$DEST/../rubric.md}
RAW_BASE=${AGENTSKILLS_RAW_BASE:-https://raw.githubusercontent.com/agentskills/agentskills}
REPO_URL=https://github.com/agentskills/agentskills
MD_HEADER='<!-- Source: https://github.com/agentskills/agentskills (CC-BY-4.0), verbatim copy, see SOURCE.json -->'
TXT_HEADER='# Source: https://github.com/agentskills/agentskills (CC-BY-4.0), verbatim copy, see SOURCE.json'

# name|upstream path
FILES=(
  "specification.md|docs/specification.mdx"
  "quickstart.md|docs/skill-creation/quickstart.mdx"
  "best-practices.md|docs/skill-creation/best-practices.mdx"
  "evaluating-skills.md|docs/skill-creation/evaluating-skills.mdx"
  "optimizing-descriptions.md|docs/skill-creation/optimizing-descriptions.mdx"
  "using-scripts.md|docs/skill-creation/using-scripts.mdx"
  "skills-ref-validator.py.txt|skills-ref/src/skills_ref/validator.py"
)

die() { echo "fetch-spec: $*" >&2; exit 1; }

STAGE=$(mktemp -d)
MOVING=false # true while publish may have modified DEST: any exit then restores it first
on_exit() {
  trap '' INT TERM
  if $MOVING; then
    if ! restore; then
      echo "fetch-spec: recovery failed; previous references are kept in $STAGE/backup" >&2
      return # keep $STAGE: it holds the only copy
    fi
    echo "fetch-spec: restored previous references" >&2
  fi
  rm -rf "$STAGE"
}
trap on_exit EXIT
trap 'echo "fetch-spec: interrupted" >&2; exit 1' INT TERM

RESOLVED=${AGENTSKILLS_SHA:-}
if [ -z "$RESOLVED" ]; then
  LS=$(git ls-remote "$REPO_URL" "refs/heads/$REF") || die "git ls-remote failed for ref '$REF'"
  RESOLVED=$(printf '%s\n' "$LS" | cut -f1 | head -1)
fi
[[ $RESOLVED =~ ^[0-9a-f]{40}$ ]] || die "could not resolve a 40-hex sha for ref '$REF' (got '$RESOLVED')"

# Stage: download every file, prepend the header, hash.
mkdir "$STAGE/new" "$STAGE/backup"
declare -A NEWHASH
for entry in "${FILES[@]}"; do
  name=${entry%%|*}; path=${entry#*|}
  curl -fsSL --max-time 60 --retry 2 "$RAW_BASE/$RESOLVED/$path" -o "$STAGE/raw" || die "download failed: $path @ $RESOLVED"
  header=$MD_HEADER; [[ $name == *.txt ]] && header=$TXT_HEADER
  { printf '%s\n\n' "$header"; cat "$STAGE/raw"; } > "$STAGE/new/$name"
  NEWHASH[$name]=$(sha256sum < "$STAGE/new/$name" | cut -d' ' -f1)
done

# Changed = staged differs from recorded, or dest missing/edited.
META=$DEST/SOURCE.json
OLD_SHA=
if [ -f "$META" ]; then OLD_SHA=$(jq -r '.sha // empty' "$META") || die "cannot read $META"; fi
CHANGED=()
for entry in "${FILES[@]}"; do
  name=${entry%%|*}
  old=; if [ -f "$META" ]; then old=$(jq -r --arg n "$name" '.files[$n] // empty' "$META") || die "cannot read $META"; fi
  cur=; [ -f "$DEST/$name" ] && cur=$(sha256sum < "$DEST/$name" | cut -d' ' -f1)
  if [ -z "$old" ] || [ "${NEWHASH[$name]}" != "$old" ] || [ "$cur" != "$old" ]; then
    CHANGED+=("$name")
  fi
done

PINNED=$OLD_SHA
[ ${#CHANGED[@]} -gt 0 ] && PINNED=$RESOLVED

publish() {
  local name
  mkdir -p "$DEST" || return 1
  for name in "${CHANGED[@]}" SOURCE.json; do
    [ -f "$DEST/$name" ] && { cp -p "$DEST/$name" "$STAGE/backup/$name" || { rmdir "$DEST" 2>/dev/null; return 2; }; }
    # status 2 = nothing modified yet, so the caller must not restore
    [ "$FETCH_SPEC_FAIL_AT" = backup ] && { rmdir "$DEST" 2>/dev/null; return 2; }
  done
  MOVING=true
  for name in "${CHANGED[@]}"; do
    mv "$STAGE/new/$name" "$DEST/$name" || return 1
    [ "$FETCH_SPEC_FAIL_AT" = term ] && kill -TERM $$
  done
  [ "$FETCH_SPEC_FAIL_AT" = metadata ] && return 1
  {
    for entry in "${FILES[@]}"; do printf '%s\t%s\n' "${entry%%|*}" "${NEWHASH[${entry%%|*}]}"; done
  } | jq -Rn --arg ref "$REF" --arg sha "$PINNED" --arg at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{repo:"agentskills/agentskills",ref:$ref,sha:$sha,fetched_at:$at,license:"CC-BY-4.0",
      files:([inputs|split("\t")|{(.[0]):.[1]}]|add)}' > "$DEST/SOURCE.json.tmp" || return 1
  mv "$DEST/SOURCE.json.tmp" "$DEST/SOURCE.json" || return 1
  MOVING=false
}

restore() { # non-zero when any step fails
  local name rc=0
  for name in "${CHANGED[@]}" SOURCE.json; do
    if [ -f "$STAGE/backup/$name" ]; then cp -p "$STAGE/backup/$name" "$DEST/$name" || rc=1; else rm -f "$DEST/$name" || rc=1; fi
  done
  rm -f "$DEST/SOURCE.json.tmp" || rc=1
  rmdir "$DEST" 2>/dev/null || : # succeeds only when DEST is empty (a first run)
  return $rc
}

if [ ${#CHANGED[@]} -gt 0 ]; then
  publish || { [ $? = 2 ] && die "backup failed, references untouched"; die "publish failed"; }
fi

STALE=true
if [ -f "$RUBRIC" ]; then
  rubric_sha=$(sed -n 's/^spec_sha:[[:space:]]*//p' "$RUBRIC" | head -1 | tr -d '[:space:]') || die "cannot read $RUBRIC"
  [ "$rubric_sha" = "$PINNED" ] && STALE=false
fi

CH=$(printf '%s\n' "${CHANGED[@]}" | jq -R 'select(length>0)' | jq -s .) || die "cannot build changed list"
UN=$(for entry in "${FILES[@]}"; do n=${entry%%|*}; [[ " ${CHANGED[*]} " == *" $n "* ]] || echo "$n"; done | jq -R . | jq -s .) || die "cannot build unchanged list"
jq -n --arg ref "$REF" --arg resolved "$RESOLVED" --arg sha "$PINNED" --argjson stale "$STALE" \
  --argjson changed "$CH" --argjson unchanged "$UN" \
  '{ref:$ref,resolved:$resolved,sha:$sha,changed:$changed,unchanged:$unchanged,rubric_stale:$stale}' || die "cannot print result"
