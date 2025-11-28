#!/bin/bash
set -euo pipefail

if [ -f /etc/svf_version ]; then
  echo "===== SvF container version ====="
  cat /etc/svf_version
  echo "================================="
fi

exec "$@"


