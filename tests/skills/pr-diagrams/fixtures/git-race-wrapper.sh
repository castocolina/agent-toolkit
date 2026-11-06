#!/bin/bash
# git wrapper: before the first push, another clone lands a commit on pr-diagrams.
# Needs REAL_GIT, RACE_BARE and RACE_MARK in the environment.
for a in "$@"; do
  if [ "$a" = push ] && [ ! -e "$RACE_MARK" ]; then
    : > "$RACE_MARK"
    o=$(mktemp -d)
    "$REAL_GIT" clone -q -b pr-diagrams "$RACE_BARE" "$o/c" 2>/dev/null
    mkdir -p "$o/c/99"; printf 'z' > "$o/c/99/z.png"
    "$REAL_GIT" -C "$o/c" add 99/z.png
    "$REAL_GIT" -C "$o/c" -c user.name=t -c user.email=t@e commit -q -m race
    "$REAL_GIT" -C "$o/c" push -q origin pr-diagrams
    rm -rf "$o"
  fi
done
exec "$REAL_GIT" "$@"
