#!/bin/bash
# Stub gh for related/reviewers tests: logs every invocation, serves scripted JSON
# per endpoint, and on an HTTP error writes the body to stdout and
# "gh: <message> (HTTP NNN)" to stderr (env-only: GH_STUB_FAIL_CODE/MSG/BODY).
printf '%s\n' "$*" >> "$GH_LOG"
code=${GH_STUB_FAIL_CODE:-} msg=${GH_STUB_FAIL_MSG:-} body=${GH_STUB_FAIL_BODY:-}
if [ -n "$code" ]; then
  printf '%s\n' "$body"
  printf 'gh: %s (HTTP %s)\n' "$msg" "$code" >&2
  exit 1
fi
endpoint=""
for a in "$@"; do
  case "$a" in
    repos/*) endpoint=$a ;;
  esac
done
file=${GH_FIXTURES}/${endpoint//\//__}
if [ -f "$file" ]; then cat "$file"; exit 0; fi
echo "stub: no fixture for $endpoint" >&2
exit 1
