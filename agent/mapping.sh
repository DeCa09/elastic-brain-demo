#!/usr/bin/env bash
# Print the field names and types of an index (what an agent without context has to read first).
# Usage: agent/mapping.sh albisgrat-incidents     or     agent/mapping.sh 'albisgrat-*'
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
set -a; . "$ROOT/.env"; set +a
curl -sS "${ELASTICSEARCH_URL%/}/$1/_mapping" -H "Authorization: ApiKey $ELASTIC_API_KEY" |
  python3 -c '
import json, sys
for index, body in json.load(sys.stdin).items():
    print(index)
    for name, spec in body["mappings"].get("properties", {}).items():
        print("  %-28s %s" % (name, spec.get("type", "object")))'
