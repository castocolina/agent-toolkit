#!/bin/bash
set -u
export PYTHONDONTWRITEBYTECODE=1

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TEST_ROOT="$ROOT/tests/skills"
status=0

shopt -s nullglob
found=0
for test_file in "$TEST_ROOT"/*/test-*.sh; do
  found=1
  if output=$(bash "$test_file" 2>&1); then
    while IFS= read -r line; do printf '  %s\n' "$line"; done <<< "$output"
    printf 'PASS %s\n' "${test_file#"$ROOT/"}"
  else
    while IFS= read -r line; do printf '  %s\n' "$line"; done <<< "$output"
    printf 'FAIL %s\n' "${test_file#"$ROOT/"}"
    status=1
  fi
done

for test_dir in "$TEST_ROOT"/*; do
  [[ -d "$test_dir" ]] || continue
  python_tests=("$test_dir"/test_*.py)
  ((${#python_tests[@]})) || continue
  for test_file in "${python_tests[@]}"; do
    found=1
    if output=$(cd "$ROOT" && python3 -m unittest discover -s "${test_dir#"$ROOT/"}" -p "$(basename "$test_file")" 2>&1); then
      while IFS= read -r line; do printf '  %s\n' "$line"; done <<< "$output"
      printf 'PASS %s\n' "${test_file#"$ROOT/"}"
    else
      while IFS= read -r line; do printf '  %s\n' "$line"; done <<< "$output"
      printf 'FAIL %s\n' "${test_file#"$ROOT/"}"
      status=1
    fi
  done
done

((found)) || status=1
exit "$status"
