# reportable

Agent: With Knowledge Indicators

Question: Which reportable incidents did we have in the third quarter of 2026? List the ids.

Expected records: INC-2026-001, INC-2026-004, INC-2026-021, INC-2026-031

Tools called: albisgrat.brain.query_ki, platform.core.execute_esql

---

Im dritten Quartal 2026 (Juli–September) gab es folgende meldepflichtige Vorfälle:

| Incident-ID | Datum | Kategorie | Schweregrad | Status | Büro |
|---|---|---|---|---|---|
| INC-2026-021 | 10.07.2026 | data_breach | medium | closed | Geneva |
| INC-2026-031 | 18.07.2026 | access_violation | high | closed | Zurich |
| INC-2026-001 | 27.07.2026 | access_violation | low | closed | Zurich |
| INC-2026-004 | 22.09.2026 | data_breach | medium | open | Geneva |

Definition "meldepflichtiger Vorfall": data_breach mit Schweregrad medium/high, oder access_violation jeder Schweregradstufe (Phishing und system_outage sind nicht meldepflichtig).

Based on: albisgrat-incidents index, Knowledge Indicators (index_metadata_entry "Privatbank Albisgrat Security & Operational Incidents (2026)", business_definition "Reportable incident (meldepflichtiger Vorfall)").
