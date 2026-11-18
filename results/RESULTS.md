# Company brain: with and without Knowledge Indicators

Same questions, same data, same model. One agent reads Knowledge Indicators from the AI Index first; the baseline explores the indices by itself. "Correct" means the answer names exactly the records computed from the data files. Runs from 2026-11-18. Where a question has no baseline row, the baseline was not run for it, to save tokens.

| Question | Agent | Correct | Tool calls | LLM calls | Tokens | Seconds | Model |
|---|---|---|---|---|---|---|---|
| material (de) | Baseline, no context | no (missing OUT-006, OUT-010, OUT-019; wrong OUT-021) | 5 | 10 | 87,557 | 33 | Claude Sonnet 4.5 (project default) |
| material (de) | With Knowledge Indicators | yes | 2 | 3 | 33,226 | 20 | Claude Sonnet 4.5 (project default) |
| reportable (en) | Baseline, no context | no (missing INC-2026-001, INC-2026-004, INC-2026-021; wrong INC-2026-017, INC-2026-020, INC-2026-022) | 11 | 15 | 349,907 | 74 | Claude Sonnet 5 |
| reportable (en) | With Knowledge Indicators | yes | 2 | 3 | 43,971 | 15 | Claude Sonnet 5 |
| location (en) | Baseline, no context | yes | 10 | 27 | 348,407 | 77 | Claude Sonnet 4.5 (project default) |
| location (en) | With Knowledge Indicators | yes | 3 | 4 | 48,474 | 21 | Claude Sonnet 4.5 (project default) |
| overdue (de) | Baseline, no context | yes | 2 | 7 | 56,617 | 34 | Claude Sonnet 4.5 (project default) |
| overdue (de) | With Knowledge Indicators | yes | 2 | 3 | 31,558 | 20 | Claude Sonnet 4.5 (project default) |
| late-breaches (fr) | Baseline, no context | yes | 6 | 14 | 123,958 | 43 | Claude Sonnet 4.5 (project default) |
| late-breaches (fr) | With Knowledge Indicators | yes | 8 | 8 | 99,134 | 35 | Claude Sonnet 4.5 (project default) |

## Per agent (averages per question)

| Agent | Correct | Tool calls | Tokens | Seconds |
|---|---|---|---|---|
| Baseline, no context | 3 of 5 | 6.8 | 193,289 | 52 |
| With Knowledge Indicators | 5 of 5 | 3.4 | 51,272 | 22 |

## The questions

- **material**: Welche unserer Auslagerungen gelten als wesentliche Auslagerungen? Liste die IDs auf.  
  Expected: OUT-001, OUT-002, OUT-003, OUT-004, OUT-006, OUT-007, OUT-008, OUT-010, OUT-011, OUT-016, OUT-019, OUT-024. The bank's own definition: active, client data, and criticality high or cost of CHF 200,000 or more. Criticality alone gives a different list.
- **reportable**: Which reportable incidents did we have in the third quarter of 2026? List the ids.  
  Expected: INC-2026-001, INC-2026-004, INC-2026-021, INC-2026-031. The bank's own definition: data breaches of medium or high severity, and all access violations. Phishing and outages do not count.
- **location**: Which outsourcing arrangements store client data outside Switzerland, and does our directive allow each of them?  
  Expected: OUT-003, OUT-004, OUT-014, OUT-019. Not allowed: OUT-003, OUT-014, OUT-019. Allowed (EU with board approval): OUT-004.
- **overdue**: Bei welchen aktiven Auslagerungen ist die jährliche Überprüfung überfällig?  
  Expected: OUT-002, OUT-007, OUT-010. Overdue means last review more than 12 months ago (W-12 v3.0, section 8).
- **late-breaches**: Quelles violations de la sécurité des données ont été annoncées en retard cette année, et lesquelles concernent un prestataire externe ?  
  Expected: INC-2026-023, INC-2026-043. Late means not reported within 24 hours (P-11). With a provider: INC-2026-043 (OUT-019).

Agents are not deterministic. One run per question shows direction, not proof. The full answers are in `results/answers/`.
