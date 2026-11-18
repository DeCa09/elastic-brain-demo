#!/usr/bin/env bash
# Run one ES|QL query against the Elasticsearch project and print the result as text.
# Usage: agent/esql.sh 'FROM albisgrat-incidents | LIMIT 3'
# This is the only way the outside agents touch Elastic. No LLM runs on the Elastic side.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
set -a; . "$ROOT/.env"; set +a
body="$(python3 -c 'import json,sys; print(json.dumps({"query": sys.argv[1]}))' "$1")"
curl -sS -X POST "${ELASTICSEARCH_URL%/}/_query?format=txt" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" -H "Content-Type: application/json" \
  -d "$body" | cut -c1-6000
