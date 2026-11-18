# Deck outline: 10 slides, 30 minutes

**The thesis:** the models are good enough. What an agent lacks is your context. Elasticsearch can hold that context.

Headlines are full sentences. Someone who reads only the headlines should get the argument.

**Every number about Privatbank Albisgrat AG is an assumption**, marked *(A)*; the bank is invented. **The measurements are real**: five questions, each run once per agent on your Serverless project (`results/RESULTS.md`). Third-party numbers are attributed on the slide where they appear.

## Time plan

| # | Slide | Minutes | Running total |
|---|---|---|---|
| 1 | Title, thesis and panel roles | 2:00 | 2:00 |
| 2 | Customer and pain | 2:30 | 4:30 |
| 3 | Desired outcomes | 1:30 | 6:00 |
| 4 | Architecture | 3:00 | 9:00 |
| 5 | Why Elastic | 2:00 | 11:00 |
| 6 | Live demo | 12:00 | 23:00 |
| 7 | Business value | 3:00 | 26:00 |
| 8 | Roadmap | 2:00 | 28:00 |
| 9 | Next steps | 1:00 | 29:00 |
| | Buffer | 1:00 | 30:00 |
| 10 | Appendix | Q&A only | |

Checkpoints: **in the demo by 11:00, out by 23:00.**

**How to open, before slide 1 (30 seconds, your own words):** "I prepared two demos. One is a safe agentic search story, and I am happy to show it afterwards. But I was told the best demos are the ones where you learn something. So I would rather show you the one I learned the most from building."

---

## Slide 1. Title, thesis and roles (2:00)

**Headline:** The models are smart enough. What they lack is your context.

**Visual:** The headline large. Under it one line: "A context layer for the agents of Privatbank Albisgrat, on Elasticsearch." Four role cards.

| Panellist | Role today | You will see |
|---|---|---|
| [RVP name] | Chief Data and AI Officer | What agents cost, and what makes them right |
| [Senior Manager SA name] | Head of Compliance | Your definitions, used by every agent |
| [Director SA name] | CISO | Who may read and change the context |
| [Principal SA name] | Lead AI Platform Engineer | How it is built: an index, a workflow, a query |

**Speaker notes:** "My view, after five years of building AI systems for enterprises: the models stopped being the bottleneck. Give a current model the right context and it does the job. Give it none and it guesses, expensively. So the question for a bank is not which model. It is where its context lives. I will argue it can live in Elasticsearch, and I will show a measurement. To make it concrete, you are the Albisgrat team: [roles]. Is that all right?"

Say the thesis as your opinion. Do not attribute claims about AGI or about specific models to named people unless you have the link in the appendix.

**German:** Kontext statt Intelligenz, Kontextschicht, Rollenverteilung.

---

## Slide 2. Customer and pain (2:30)

**Headline:** Albisgrat's agents re-learn the bank on every question, and guess what its terms mean

**Visual:** Left, the agent's loop as a circle: question → list indices → read mappings → sample documents → try queries → answer. A counter under it: "up to 11 tool calls and 350,000 tokens for one question (measured)". Right, one example in a box:

> Question: "Which of our outsourcings are material?"
> The agent's answer: the 10 marked high criticality.
> The bank's definition: client data, and high criticality **or** cost of CHF 200,000 or more. 12 arrangements.
> Confidently wrong.

Under both, three numbers:
- **2 of 5** test questions answered wrongly without context (measured)
- **6 pilot agents** planned for next year: compliance, service desk, onboarding *(A)*
- **Each team** writes its own prompt to explain the same data *(A)*

**Speaker notes:** "What we heard. You have a successful assistant pilot and six agents planned. You noticed two things. First, cost per question swings wildly, because the agent explores your data from scratch every time. Second, and worse: [HoC] when a question uses one of your terms, the agent guesses. 'Material outsourcing' is your definition, used for board reporting. It is not written in any table. The agent answered with full confidence and was wrong. And today the only fix is a longer prompt, written per team, out of date the day after. Did I get that right?"

**German:** erkunden, wesentliche Auslagerung, falsch aber überzeugt, Prompt-Wildwuchs.

---

## Slide 3. Desired outcomes (1:30)

**Headline:** Four outcomes, one for each pain

| Pain today | Outcome you asked for |
|---|---|
| ❌ Agents explore the data on every question | ✅ An agent knows where to look before it starts |
| ❌ Bank-specific terms are guessed | ✅ Your definitions are applied, and can be checked |
| ❌ Context lives in prompts per team | ✅ One maintained context layer, shared by all agents |
| ❌ Cost grows with every new agent | ✅ Predictable cost per task |

One line underneath: "Without changing the model."

**Speaker notes:** "So success is: agents that start informed, use your definitions, share one maintained layer of context, and cost a predictable amount. And none of it should depend on which model you use next year."

**German:** Zielbild, nachvollziehbar, gepflegt, planbare Kosten.

---

## Slide 4. Architecture (3:00)

**Headline:** An index for context, a workflow that fills it, one query that reads it

**Visual:** `diagrams/architecture.svg`, with the four ❌ → ✅ callouts.

**Speaker notes:** Left to right.
- "The bank's data, in Elasticsearch: the knowledge base with law and policies, searchable across four languages, and two registers."
- "In the middle, how context is made. A Kibana Workflow reads each index's mapping and a few samples, asks a model for a profile, and stores it. That part is automatic. Below it, what no machine can know: your definitions. Your experts write those, once, in plain language with the query that computes them."
- "The yellow box is the AI Index. An ordinary Elasticsearch index with a naming convention; Elastic configures hybrid search on it. It holds Knowledge Indicators: index profiles, business definitions, a policy register, a glossary."
- "On the right, the agent. One extra tool: a single hybrid query over the AI Index. It looks up context first, then queries the right index."
- "[ENG] Nothing here is a new system. An index, a workflow, a query. The agent could be Elastic's Agent Builder, as in the demo, or any other harness that can run ES|QL."

Features to name: AI Index and Knowledge Indicators, Kibana Workflows, `semantic_text`, ES|QL with `FORK` and `FUSE`, Agent Builder, Elastic Inference Service.

**German:** Kontextschicht, Wissensindikatoren, automatisch erzeugt, fachliche Hoheit.

---

## Slide 5. Why Elastic (2:00)

**Headline:** Why Elastic: context is a search problem, and it belongs next to the data and its permissions

**Visual:** Three columns.

| Alternative | Good at | The gap for Albisgrat |
|---|---|---|
| Longer prompts and hand-written instructions | Quick for one agent | Not shared, not searchable, out of date; every agent pays for the whole prompt on every call |
| A context layer inside a data warehouse (for example Snowflake's Cortex Sense, announced June 2026) | Structured data that already lives in that warehouse; it mines query history automatically | Albisgrat's knowledge is mostly documents in three languages; the automatic mining is the vendor's preview, not something you control |
| A separate vector store for "agent memory" | Storing embeddings | No keyword search, no permissions per document, no workflow, another system to run |

Bottom line: "Elastic: documents and registers, keyword and semantic search, permissions, workflows and the agent in one platform."

**Speaker notes:** "Three alternatives. Longer prompts: everyone starts there, and it does not scale past one agent. A context layer in the warehouse: Snowflake announced one this summer. It is a good idea, and they report strong numbers on their own data. It fits when your knowledge is tables in that warehouse. Yours is policies in German, French and Italian plus a few registers. A vector store for agent memory: one more system without search or permissions. My argument for Elastic is simple: picking the right context for a question is a retrieval problem, and that is what this engine does. I will be fair about the stage: what I show is built by hand from Elastic's primitives. The automatic refinement Elastic describes is the next step, not part of today."

**German:** Kontext ist ein Suchproblem, eine Plattform, Berechtigungen.

---

## Slide 6. Live demo (12:00)

**Headline:** One model, one question, asked twice

**Visual:** Two columns: "Without context" and "With a context layer", empty, to be filled by the demo. One sentence:

> "You will see the same model answer the same question twice: once exploring and guessing, once informed."

**Speaker notes:** Say the sentence. "Everything runs on an Elasticsearch Serverless project. The law texts are real Swiss federal law. The bank, its registers and its definitions are fictional." Follow `RUNBOOK.md`.

---

## Slide 7. Business value (3:00)

**Headline:** With context: right on the bank's own terms, a quarter of the tokens, less than half the time

**Visual:** The measured table, large.

| Five questions, same data, once each | Without context | With Knowledge Indicators |
|---|---|---|
| Correct answers | 3 of 5 | 5 of 5 |
| Questions that need a bank definition | 0 of 2 | 2 of 2 |
| Tokens per question | 193,000 | 51,000 |
| Seconds per question | 52 | 22 |
| Tool calls per question | 6.8 | 3.4 |

Next to it, the cost model in three lines:

- Saved per agent task: about **142,000 tokens** (measured)
- At USD 3 per million tokens *(A)*: about **USD 0.43 per task**
- 150 staff asking 4 questions a week: USD 12,000 a year. **Agents handling 5,000 tasks a day *(A)*: about USD 780,000 a year**

Small print: "Our own measurement: five questions, one run each. For comparison, Elastic reports 45% fewer tokens in its published example, and Snowflake reports 24% to 86% accuracy on its own benchmark with its context layer (vendor claims, June and August 2026)."

**Speaker notes:** "[CDAO] Three results. Correctness: on the two questions that depended on your definitions, the agent without context was wrong both times, with two different models. With context it was right. Cost: about a quarter of the tokens. Speed: less than half the time. Now the money, honestly. Per question the saving is about 40 cents at an assumed price. For people asking questions, that is twelve thousand dollars a year: not a business case. The business case is agents. Once agents triage every ticket and check every onboarding file, you have thousands of tasks a day, and the same saving is a budget line. And the first row is not about money at all: a confidently wrong answer in a board report is a different kind of cost."

Be the first to say the caveat: five questions, one run each, and I built both the questions and the context. Direction, not proof.

**German:** Geschäftswert, Kosten pro Aufgabe, Skalierung mit Agenten, Richtung statt Beweis.

---

## Slide 8. Roadmap (2:00)

**Headline:** Land with one agent and twenty definitions, then make context a shared service

| Land: pilot (6 weeks) | Expand (two quarters) | Platform (later) |
|---|---|---|
| The compliance assistant, with a context layer | The other five agents read the same layer | Context for every agent, including ones you buy |
| 20 definitions written with Compliance; index profiles generated | Owners and review dates per definition; refresh on a schedule | Refinement from agent traces; the same platform for search, observability and security |
| A test set of 50 real questions | Measured per agent: correctness, tokens, time | |
| **Success:** correct on 90% of definition questions; tokens per task halved | **Success:** no agent ships with a private prompt for shared data | **Success:** agreed later |

**Speaker notes:** "Start small: one agent, twenty definitions your compliance team writes in a workshop, and fifty real questions to measure against. Six weeks. Then the other agents use the same layer instead of their own prompts. Each definition gets an owner and a review date, because a wrong definition makes an agent confidently wrong. Later, the layer serves every agent you run, and the same platform covers search, observability and security."

**German:** Pilot, Erfolgskriterien, Verantwortliche je Definition, gemeinsamer Dienst.

---

## Slide 9. Next steps (1:00)

**Headline:** Three decisions today start the pilot in two weeks

1. **Pick the first agent and its 50 test questions.** Chief Data and AI Officer and me. This week.
2. **Definition workshop, half a day:** the 20 terms that agents get wrong. Head of Compliance. Next week.
3. **Security review of the context layer:** who may read it, who may change it, which model. CISO and Lead AI Platform Engineer. Next week.

**Speaker notes:** "Three things. The first agent and fifty real questions. Half a day with compliance to write down the twenty terms. And a security review of who may read and change the context. Can we agree on these today? What would stop us?" Stop talking.

---

## Slide 10. Appendix for Q&A (not presented)

| Slide | Content |
|---|---|
| A1 The measurement | Per-question table from `results/RESULTS.md`: correct, tool calls, tokens, seconds, model. The caveats. |
| A2 The two definition questions | The question, the bank's definition, what each agent answered, and why the baseline's guess was reasonable and still wrong. |
| A3 What a Knowledge Indicator looks like | One index profile, one definition with its query, one glossary entry. |
| A4 Cost model | Tokens saved per task, the assumed price, the two volume scenarios, and what is not counted (the workflow's own LLM use, the embedding of the indicators). |
| A5 Governance and security | Owner and review date per definition; permissions on the AI Index; where the model runs. |
| A6 Limits | Built by hand; AI Indices are Serverless-only today; no automatic refinement yet; a wrong indicator misleads every agent. |
| A7 The other demo | The compliance assistant: multilingual hybrid search, citations, document-level security. Available on request. |
| A8 Sources | Elastic's article, Snowflake's announcement, customer stories, with links. |

---

## All assumptions in one place

| Assumption | Value | Used on |
|---|---|---|
| Agents planned at the bank | 6 | 2, 8 |
| Price per million tokens | USD 3 | 7 |
| Staff asking questions | 150, four questions a week, 46 weeks | 7 |
| Agent tasks per day at scale | 5,000 | 7 |
| Definitions in the pilot | 20 | 8 |
| The bank's definitions of "material outsourcing" and "reportable incident" | Invented for the demo | 2, 6 |

Measured, not assumed: everything in the table on slide 7. Arithmetic: 193,289 − 51,272 = 142,017 tokens per task; × USD 3 per million = USD 0.43; × 27,600 tasks = USD 11,800; × 1,825,000 tasks = USD 778,000.
