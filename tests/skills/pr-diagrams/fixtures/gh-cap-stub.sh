#!/bin/bash
# Stub gh for capability/publish tests. Output and failure are env-driven:
# CAP_VERSION / CAP_URL are printed; CAP_MODE_V / CAP_MODE_U = fail|hang|"".
case "$1" in
  --version) mode=${CAP_MODE_V:-}; out=${CAP_VERSION-gh version 2.101.0 (2026-09-15)} ;;
  repo) mode=${CAP_MODE_U:-}; out=${CAP_URL-https://github.com/acme/widgets} ;;
  *) exit 1 ;;
esac
case "$mode" in
  fail) echo "stub failure" >&2; exit 1 ;;
  hang) exec sleep 20 ;;
esac
printf '%s\n' "$out"
