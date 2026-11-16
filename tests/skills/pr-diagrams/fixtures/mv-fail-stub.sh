#!/bin/bash
# mv stub: fails when it would rename a staged copy onto FAIL_MV_DEST; every other mv
# (the backup rename and the restore rename carry a ".pr-diagrams.bak." name) is the real one.
# Needs REAL_MV and FAIL_MV_DEST in the environment; MV_LOG, when set, receives every call.
[ -z "${MV_LOG:-}" ] || printf '%s\n' "$*" >> "$MV_LOG"
last=${*: -1}
if [ "$last" = "$FAIL_MV_DEST" ]; then
  case "$*" in
    *.pr-diagrams.bak.*) ;;
    *) echo "mv stub: refusing to rename onto $last" >&2; exit 1 ;;
  esac
fi
exec "$REAL_MV" "$@"
