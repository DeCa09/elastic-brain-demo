#!/usr/bin/env bash
# Check that the demo is ready. Uses no LLM, so it is safe to run right before the session.
set -uo pipefail
. "$(dirname "$0")/lib.sh"
need KIBANA_URL ELASTICSEARCH_URL ELASTIC_API_KEY
fails=0
say "1. Indices and agents"
out="$(python3 "$ROOT/brain/setup_brain.py" status)"; echo "$out"
echo "$out" | grep -q "missing" && { bad "something is missing: run scripts/setup.sh all"; fails=$((fails + 1)); }
say "2. The Knowledge Indicator lookup"
if python3 "$ROOT/brain/setup_brain.py" lookup "Welche Auslagerungen gelten als wesentliche Auslagerungen?" | tee /dev/stderr | grep -q "Material outsourcing"; then
  ok "the definition of 'wesentliche Auslagerung' is found"
else
  bad "the definition of 'wesentliche Auslagerung' is not found"; fails=$((fails + 1))
fi
say "3. Check by hand"
note "No agent question in the hour before the session: the trial's LLM quota refills slowly"
note "The earlier baseline conversation is open in a tab (RUNBOOK.md)"
note "Backup recording and screenshots are open in another window (FALLBACK.md)"
echo
if [ "$fails" -eq 0 ]; then printf '\033[32mPREFLIGHT PASSED\033[0m\n'; else printf '\033[31mPREFLIGHT FAILED\033[0m  %s check(s) failed\n' "$fails"; exit 1; fi
