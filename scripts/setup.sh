#!/usr/bin/env bash
# Build the demo on the Serverless project.
# Usage: scripts/setup.sh all|sources|ai-index|definitions|agents|workflow|status|delete
#   all       sources, AI Index with hand-written Knowledge Indicators, agents (no LLM used)
#   workflow  generate the index profiles with the Kibana Workflow (uses the LLM, about 2 minutes)
set -euo pipefail
. "$(dirname "$0")/lib.sh"
need KIBANA_URL ELASTICSEARCH_URL ELASTIC_API_KEY
exec python3 "$ROOT/brain/setup_brain.py" "$@"
