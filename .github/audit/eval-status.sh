#!/usr/bin/env bash
# Combine the two run-evals exit statuses of the evals job into one verdict.
#
# Usage: eval-status.sh STATUS1 STATUS2
#
# stdout: "quality_failed=true" or "quality_failed=false" (the caller appends it
#   to $GITHUB_OUTPUT); printed only when the combined run is tolerated.
# stderr: the reason when the job must fail.
# exit:   2 when a leg reported a harness error,
#         the first leg's other nonzero status (crash, OOM kill, missing runner)
#         when any leg exited with something other than 0, 1 or 2,
#         0 otherwise (quality_failed=true when any leg exited 1).
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "usage: eval-status.sh STATUS1 STATUS2" >&2
  exit 64
fi
for value in "$1" "$2"; do
  [[ "$value" =~ ^[0-9]+$ ]] || { echo "statuses must be non-negative integers, got: $value" >&2; exit 64; }
done
left=$1
right=$2
if [ "$left" -eq 2 ] || [ "$right" -eq 2 ]; then
  echo "eval harness error: run-evals exited 2" >&2
  exit 2
fi
for value in "$left" "$right"; do
  if [ "$value" -ne 0 ] && [ "$value" -ne 1 ]; then
    printf 'run-evals crashed with unexpected exit status %d\n' "$value" >&2
    exit "$value"
  fi
done
if [ "$left" -eq 1 ] || [ "$right" -eq 1 ]; then
  echo 'quality_failed=true'
  exit 0
fi
echo 'quality_failed=false'
