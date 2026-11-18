#!/usr/bin/env bash
# Ask the test questions to both agents and write results/RESULTS.md.
# Every run uses the LLM, and the baseline uses a lot of it. The trial limits LLM use per model
# and refills after some minutes, so run one question at a time.
# Usage: scripts/compare.sh [question-id ...] [--only-brain]
#   question ids: material reportable location overdue late-breaches
set -euo pipefail
. "$(dirname "$0")/lib.sh"
need KIBANA_URL ELASTIC_API_KEY
exec python3 "$ROOT/brain/compare.py" "$@"
