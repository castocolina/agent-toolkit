#!/bin/bash
# mv stub: does the real mv, and right after the backup rename of TERM_AFTER_BAK_OF (a
# destination PNG) sends TERM to its parent, the render script. Bash runs the script's trap
# when this stub returns, so the signal lands between that backup rename and the install of
# the staged copy. Needs REAL_MV and TERM_AFTER_BAK_OF in the environment.
"$REAL_MV" "$@" || exit $?
last=${*: -1}
case "$last" in
  *.pr-diagrams.bak.*) [ "${*: -2:1}" != "$TERM_AFTER_BAK_OF" ] || kill -TERM "$PPID" ;;
esac
exit 0
