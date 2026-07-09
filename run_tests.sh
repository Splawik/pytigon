#!/bin/bash
set -euo pipefail

echo "=== pytigon ptig @pytest ==="
ptig @pytest tests/ -m "$@"
echo
