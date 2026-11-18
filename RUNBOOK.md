# Demo runbook: 12 minutes

**Session:** Tuesday 24 November 2026, 13:00 to 14:00 CET.

**The thesis in one sentence:** the models are good enough; what an agent lacks is your context, and Elasticsearch can hold that context.

**The demo in one sentence:** the same model answers the same question twice; without context it explores for a minute and gets a bank-specific term wrong; with a context layer in Elasticsearch it answers correctly in 20 seconds with a third of the tokens.

**Tested or not.** Indices, the AI Index, the workflow, both agents and the measurements were tested through the APIs on the Serverless project on 18 November. **Nobody has clicked through this flow in Kibana yet.** The click names below are my best reading of Kibana 9.7 and your German interface (Agenten, Discover, Workflows, Mehr). Walk through it once and correct this file.

## The one rule: protect the LLM quota

The trial limits LLM use per model. When the limit is reached, the agent returns an error. In my test it was still blocked 20 minutes later. One baseline run can use 350,000 tokens and trigger it.

The limit is per model. If the default model is blocked, another one still works: I confirmed that through the API. In the chat, look for a model selector and pick another managed model (for example Claude Sonnet 5). I have not seen where that selector is in the interface, so find it in your walk-through.

- **Never run the baseline agent live.** Show its earlier conversation from the history.
- **Ask the live agent at most three questions** in the session.
- **No agent questions in the hour before the session.** `scripts/preflight.sh` uses no LLM and is safe at any time.

## People and pains

| Panellist | Plays | Short |
|---|---|---|
| RVP | Chief Data and AI Officer, sponsor | **CDAO** |
| Senior Manager SA | Head of Compliance, owns the bank's definitions | **HoC** |
| Director SA | CISO | **CISO** |
| Principal SA | Lead AI Platform Engineer | **ENG** |

| Pain | Short |
|---|---|
| Agents explore the data from scratch on every question: slow, and the cost is unpredictable | **P1** |
| Agents get bank-specific terms wrong, with full confidence | **P2** |
| Context lives in prompts that each team writes and nobody maintains | **P3** |
| Token cost grows with every new agent | **P4** |

## Before the session

**The day before**
- [ ] `scripts/preflight.sh` is green.
- [ ] In Kibana, as yourself: open **Agenten > Albisgrat Baseline (no context)** and ask question 1 below once. Leave that conversation in the history. This is the baseline you show on the day. Note its number of steps and the time.
- [ ] Wait 30 minutes. Then ask **Albisgrat Company Brain** question 1 once, to see the good answer and to take screenshots.
- [ ] Record the backup video and screenshots (`FALLBACK.md`).

**30 minutes before (12:30)**
- [ ] `scripts/preflight.sh` is green. Do not ask any agent anything.

**5 minutes before (12:55)**
- [ ] Browser, zoom 125%, logged in to the Serverless project's Kibana with your Elastic Cloud account. Tabs in this order:
  1. **Discover**, ES|QL mode, with query A (below) already run
  2. **Agenten > Albisgrat Baseline**: yesterday's conversation, opened
  3. **Discover**, ES|QL mode, with query B already run
  4. **Workflows > albisgrat-index-profile-ki**
  5. **Agenten > Albisgrat Company Brain**: a new, empty conversation
- [ ] A note with the questions and queries, ready to paste.
- [ ] `results/RESULTS.md` or slide 7 ready.
- [ ] Backup video and screenshots open in another window.

## The 12 minutes

| Time | Show and click | Say | Pain / role | German key terms |
|---|---|---|---|---|
| **0:00** | **Tab 1, Discover.** Query A: the three indices and their sizes. | "This is Albisgrat's data as an agent sees it. Three indices: a knowledge base with law and policies, an outsourcing register, an incident register. No documentation. This is how most enterprise data looks to an agent." | P1 / ENG | Datenbestand, Auslagerungsregister |
| **0:45** | **Tab 2, baseline conversation.** Read the question aloud. Open the reasoning or tool steps. Scroll slowly. | "Yesterday I asked a frontier model, with nothing but query tools, which of our outsourcings are 'wesentlich', material. Watch what it does. It lists indices. It reads mappings. It tries queries. It is doing what a new analyst does on day one, and it does this again for every question." | P1 / ENG, CDAO | wesentliche Auslagerung, erkunden |
| **1:45** | The baseline's answer. Point at the count and at the definition it assumed. | "It answered with full confidence: ten arrangements, those marked high criticality. That is wrong. At this bank, 'material' means something specific. [HoC] Your team defined it: client data, and either high criticality or a cost above 200,000 francs. Twelve arrangements, and one of its ten is not among them. The model is not stupid. It was never told." | P2 / HoC, CDAO | Definition, Fachbegriff, falsch aber überzeugt |
| **2:45** | Stay. | "This is my thesis for today. The models are smart enough. What they lack is context: your terms, your rules, where your data lives. The fix is not a bigger model." | all | Kontext, nicht Intelligenz |
| **3:15** | **Tab 3, Discover.** Query B: the AI Index grouped by type. Then query C: open the definition "Material outsourcing". Read its first sentence. | "This is an AI Index. It is an ordinary Elasticsearch index with a naming convention, and Elastic configures hybrid search on it for you. It holds Knowledge Indicators. Four kinds here: a profile per index, your business definitions, a register of which policy version is in force, and a glossary in four languages. This one is the definition of material outsourcing, with the query that computes it." | P2, P3 / HoC, ENG | Wissensindikator, Glossar, gültige Fassung |
| **4:45** | **Tab 4, Workflows.** Open the workflow. Point at the four steps: get mapping, sample documents, profile with the LLM, write to the AI Index. Open the last run if it is listed. | "Who writes these? The index profiles: nobody. This Kibana Workflow reads each index's mapping and a few sample documents, asks a model for a profile, and stores it. It ran in under two minutes. The definitions and the glossary are different: those your experts own. That split matters. Machines describe the data. People define the business." | P3 / ENG, HoC | Workflow, automatisch erzeugt, fachliche Hoheit |
| **6:00** | **Tab 5, Company Brain.** Paste question 1. Enter. Keep talking while it works (about 20 seconds). | "Same model. Same data. Same question. The only difference: this agent has one more tool, a single hybrid query over the AI Index, and the instruction to use it first." | P1, P2 / all | derselbe Agent, ein Werkzeug mehr |
| **6:30** | **The answer.** Count the ids: twelve. Then open the steps: one context lookup, one query. | "Twelve arrangements. Correct. Two steps: it looked up what 'wesentliche Auslagerung' means here, then ran the query from the definition. About twenty seconds." | P1, P2 / HoC, ENG | korrekt, zwei Schritte |
| **7:30** | **Same tab, new conversation.** Paste question 2. Enter. | "A second one, to show it is not a trick. This needs a register and a rule from a policy: which arrangements store client data outside Switzerland, and does our directive allow each?" | P2 / CISO, HoC | Datenstandort, Weisung |
| **8:15** | **The answer.** Point at OUT-019 (US, never allowed), OUT-003 and OUT-014 (EU without board approval), OUT-004 (EU, approved), and the cited section of W-12. | "[CISO] It found the US case, the two EU cases without board approval, and it cleared the one that has approval, citing section 5 of your directive W-12. It applied your rule to your register." | P2 / CISO | Verwaltungsrat, Abschnitt 5 |
| **9:15** | **Slide 7 or `results/RESULTS.md`.** Point at correct answers, tokens, seconds. | "I measured this on five questions, once each. Three of five correct without context, five of five with. A quarter of the tokens. Less than half the time. [CDAO] The token line is your invoice. Per question it is cents. Per agent that runs on every ticket and every alert, it is a budget line. And the first line is the one that matters most: without context, the agent was confidently wrong on your own terms." | P4 / CDAO | Kosten pro Anfrage, Skalierung |
| **10:30** | Stay on the table. | "Two honest notes. Five questions, run once: direction, not proof. And where the question needed no special definition, both agents were right; context made the answer cheaper and faster, not better. Where it needed your definition, context was the difference between right and wrong." | all | Richtung, kein Beweis |
| **11:00** | Recap. | "Four pains, four answers. Agents stop exploring: one lookup. They get your terms right: your definitions travel with every question. Context is maintained, not hand-written per team: a workflow refreshes it. And cost stops growing with every agent: the context is shared. All of it is Elasticsearch: an index, a workflow, a query." | P1 to P4 / all | Zusammenfassung |
| **11:30** | Back to the slides. | "Let me put numbers on that." | | Geschäftswert |
| **12:00** | **End of demo.** | | | |

### Hard time checks

- **6:45 and the agent has not answered, or shows an error about a trial limit:** do not retry. Say the line in `FALLBACK.md`, case A, show the screenshot of the correct answer, and continue at 7:30 only if the first answer came. Otherwise go straight to 9:15.
- **9:00 and you have not reached the numbers:** skip question 2.
- **11:30:** stop and recap.

## Queries and questions

**Query A (the data as an agent sees it):**
```
FROM albisgrat-knowledge, albisgrat-outsourcing-inventory, albisgrat-incidents METADATA _index
| STATS documents = COUNT(*) BY _index
```

**Query B (what is in the AI Index):**
```
FROM ai-index-idx-albisgrat | STATS knowledge_indicators = COUNT(*) BY type
```

**Query C (one definition):**
```
FROM ai-index-idx-albisgrat | WHERE type == "business_definition" | KEEP title, content | LIMIT 10
```

**Question 1 (German, needs the bank's definition):**
```
Welche unserer Auslagerungen gelten als wesentliche Auslagerungen? Liste die IDs auf.
```
Correct: 12 arrangements: OUT-001, 002, 003, 004, 006, 007, 008, 010, 011, 016, 019, 024.
Tested: the Company Brain named exactly these (2 tool calls, 20 seconds). The baseline listed the 10 with high criticality: it missed OUT-006, OUT-010 and OUT-019 and wrongly included OUT-021.

**Question 2 (English, a register plus a policy rule):**
```
Which outsourcing arrangements store client data outside Switzerland, and does our directive allow each of them?
```
Correct: OUT-003 and OUT-014 (EU, no board approval) and OUT-019 (US) are not allowed; OUT-004 (EU, board approval) is allowed. Rule: W-12 v3.0, section 5.
Tested: correct by both agents. The Company Brain took 3 tool calls and about 20 seconds; the baseline 10 tool calls and 77 seconds.

**Reserve question (French):**
```
Quelles violations de la sécurité des données ont été annoncées en retard cette année, et lesquelles concernent un prestataire externe ?
```
Correct: INC-2026-023 and INC-2026-043; the second involves OUT-019.

### If the answer is wrong or weak

- **Wrong ids on question 1:** say so first. "That is not the list I expect. Let me show you why I know." Run query C, read the definition, and show the query inside it. The definition is in Elasticsearch; the model misapplied it. Then: "This is why every Knowledge Indicator carries its query: the answer can be checked."
- **The agent explored instead of using the context:** open the steps and say what happened. "It skipped the lookup. The instruction says to use it first; a production setup would enforce that in the workflow, not in the prompt."
- **Trial limit error:** `FALLBACK.md`, case A.

## Numbers to fill in after your first walk-through

| Number | My API test | Your walk-through |
|---|---|---|
| Baseline, question 1: steps and seconds | 5 tool calls, 33 s | ____ |
| Company Brain, question 1: steps and seconds | 2 tool calls, 20 s | ____ |
| Company Brain, question 2: steps and seconds | 3 tool calls, 21 s | ____ |
| Minutes until the quota refilled after an error | more than 20 | ____ |
| Where the model selector is in the chat | not seen | ____ |

## German glossary

| English | German |
|---|---|
| Context | Kontext |
| Context layer | Kontextschicht |
| Knowledge Indicator | Wissensindikator (keep the English term) |
| Business definition | fachliche Definition |
| Material outsourcing | wesentliche Auslagerung |
| Reportable incident | meldepflichtiger Vorfall |
| Outsourcing register | Auslagerungsregister, Auslagerungsinventar |
| Board of directors | Verwaltungsrat |
| To explore | erkunden |
| Token cost | Tokenkosten |
| Agent | Agent, KI-Agent |
| Confidently wrong | falsch, aber überzeugt |
| Maintained, not hand-written | gepflegt statt handgeschrieben |
| Data location | Datenstandort |
| Directive | Weisung |
