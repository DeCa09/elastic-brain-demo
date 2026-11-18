# Q&A preparation

**How to answer.** Repeat the concern in one sentence. Answer in 2 to 4 sentences, answer first. Then check: "Does that answer it?"

**When you do not know:** "I do not know that for certain and I would rather not guess. I will confirm it by tomorrow." The panel are Elastic employees and AI Indices are their new feature. Some of them will know it better than you. Say what you built and measured, and say plainly what you have not tried.

**Your strongest card:** you measured it yourself, and you state the limits before anyone asks.

---

## Chief Data and AI Officer (RVP)

**Your saving is 40 cents a question. Why should I care?**
For people asking questions, you should not: that is about twelve thousand dollars a year. The case is agents that run on every ticket, alert or file. At thousands of tasks a day the same saving is a budget line, and it grows with every agent you add. And the cost is the smaller finding. The larger one is that without context the agent was wrong on both questions that used your own terms.

**Five questions is not evidence.**
Agreed. It is five questions, one run each, and I wrote both the questions and the context. It shows direction. Elastic's published example shows the same direction on tokens, and Snowflake reports it on accuracy for its own product. The pilot replaces my five questions with fifty of yours and runs each several times.

**Won't better models make this unnecessary?**
A better model explores faster. It still cannot know that "material" at this bank includes a cost threshold, because that is written nowhere in the data. I ran the second definition question on a newer model and it guessed wrong too. Models improve at reasoning. Context is information they do not have.

**Why not just write it into the system prompt?**
For one agent, do that. For six agents it means six prompts that drift apart, and every call pays for the whole prompt whether it needs it or not. A context layer is retrieved: the agent gets the five indicators relevant to this question, and every agent reads the same source.

**Who else does this?**
The idea is common now. Snowflake announced Cortex Sense for its warehouse in June. Elastic published AI Indices and Knowledge Indicators in August. The difference is where it lives: Elastic's sits in the search engine, next to documents and their permissions.

**What does it cost to build and run?**
Building the layer for the demo took an index, one workflow and about fifty short entries. Running it adds one small query per agent task and an LLM call per index when profiles are refreshed. I did not measure the refresh cost. In a pilot I would report it next to the savings.

---

## Head of Compliance (Senior Manager SA)

**Who writes the definitions, and how much work is it?**
Your team, because they are yours. Each is three or four sentences in plain language plus a query that an engineer adds. For the pilot I would start with the twenty terms agents most often get wrong, in a half-day workshop.

**What if a definition is wrong or out of date?**
Then every agent is confidently wrong in the same way, which is the main risk of this approach. So each definition needs an owner and a review date, like a policy. The advantage over prompts is that there is one place to correct it, and the correction reaches every agent at once.

**Can it tell me where an answer came from?**
Yes. The agent's answer names the indices and the indicators it used, and each definition carries the query that computes it. In the demo you can run that query yourself and get the same twelve arrangements.

**Does it understand our three languages?**
The glossary maps each term across German, French, Italian and English, and the lookup searches by meaning as well as by word. I tested a German and a French question; both found the right definition.

**Is "material outsourcing" in the demo the regulatory definition?**
No. I invented it for the demo to stand for any term that a bank defines for itself. The real one would come from your directive and your regulator's rules.

---

## CISO (Director SA)

**Who can read the context layer?**
It is an Elasticsearch index, so the same controls apply: roles, and document-level security if some indicators are restricted. I did not test document-level security on the AI Index in this demo. In my other demo I tested it for search and for an agent on a Hosted deployment, and it held.

**Who can change it? That is a way to manipulate every agent.**
Yes, and it should be treated that way: write access for a small group, changes reviewed, and an audit trail. A poisoned definition is more dangerous than a poisoned document because agents trust it. I would not give the workflow's service account more than it needs.

**Does the context contain our data?**
Index profiles contain field names and a few example values. Definitions contain rules, not client data. In the workflow I excluded the document text from the samples. In production I would also keep client-identifying fields out of the samples.

**Where does the model run, and can an agent leak the context?**
The managed models run on the Elastic Inference Service; Elastic documents zero data retention for them, with third-party providers behind some models. If that is not acceptable, you connect your own model. The agent only has read tools, so it cannot change data.

**Serverless has no Swiss region. Is that a problem?**
Today AI Indices are Serverless-only, and Serverless offers EU regions, not a Swiss one. Elastic's article says the feature will come to stack releases. If Swiss residency is a hard requirement, the same pattern works on a Hosted deployment in Zurich with a normal index and the same mapping; you lose only the automatic setup. I checked that the templates are absent on Hosted, but I have not run the pattern there.

---

## Lead AI Platform Engineer (Principal SA)

**What exactly is an AI Index?**
An index whose name starts with `ai-index-idx-`, or a data stream with `ai-index-ds-`. The prefix applies Elastic's component templates: `title`, `description` and `content` each get a `semantic_text` sub-field on Jina v5, plus `type`, `tags`, `attributes` and `references`. I created it with one PUT and inspected the mapping.

**How does the agent retrieve from it?**
One ES|QL query, registered as a tool in Agent Builder with the question as parameter. It uses `FORK` for a keyword branch and a semantic branch, `FUSE` to merge them, and returns the top eight indicators. The agent's instructions say to call it first, once.

**How are the indicators created?**
Three ways. Index profiles by a Kibana Workflow: get the mapping, sample three documents, call an LLM step with a JSON schema, write the result. The policy register by a script from the documents' own metadata. Definitions and glossary by hand.

**Did the workflow work first time?**
No. Field descriptions in mappings are limited to 50 characters, and the search step did not accept a source filter object, so I switched that step to a plain Elasticsearch request. After that it validated and ran in 107 seconds for three indices.

**Why did the agent with context sometimes use more tool calls?**
On the French question it guessed a field name wrong and retried, eight calls against six. The profile listed the fields, so that was the model not reading closely. Tokens were still lower. It is a reminder that context reduces exploration but does not remove model error.

**How do you know the baseline is a fair comparison?**
Same model, same indices, same query tools, plus the exploration tools it needs. Its instructions say only that the bank's indices start with a prefix. It is a plain agent, not a strawman. Where no bank-specific definition was needed, it got all three questions right.

**What about a feedback loop?**
Not built. Elastic's article names it as the production path: refine indicators from the agent's traces. Today I would add a simple version: log questions where the agent explored instead of using an indicator, and review them weekly.

**How does this scale to thousands of indices?**
Retrieval scales: it is a search over short documents. The open questions are generation cost for the profiles and keeping them fresh. I would profile on change, not on a schedule, and I would not profile indices no agent has ever queried.

**What did you not test?**
The flow in the Kibana interface, document-level security on the AI Index, repeated runs per question, and the cost of regenerating profiles. And the trial's rate limit stopped me twice, which is how I learned the quota is per model.

---

## Why not Snowflake Cortex Sense?

Be fair: it is the same idea, announced earlier, with more automation. Snowflake describes mining query history, transformation models and BI metrics automatically, ranking conflicting signals and asking a human to settle conflicts. That is ahead of what I built by hand.

Three differences for this bank. Its knowledge is mostly documents in three languages, which is search-engine territory. Cortex Sense, per the announcement, works on metadata of data in Snowflake. And Elastic's version is built from open primitives you can inspect: an index, a workflow, a query.

If the panel pushes: "If your data and your analysts live in Snowflake, use theirs. If your knowledge is documents, logs and registers in Elastic, the context belongs there."

## Why not just retrieval-augmented generation?

RAG retrieves passages that look like the question. A context layer retrieves knowledge about the data: where things are, what terms mean, which version counts. They work together. My other demo is the first; this one is the second, on top of it.

---

## Social proof

Quoted from elastic.co on 14 November 2026. None of these is about AI Indices, which are new. Use them for "Elastic runs search and GenAI in regulated industries".

| Customer | What the page says | Link |
|---|---|---|
| EY | "EY puts Elastic at the heart of GenAI experience for financial sector". "Elastic's RAG setup was able to produce results 3 times faster when compared to Native RAG approaches". | https://www.elastic.co/customers/ey |
| Docusign | "Traditionally, this could take hours. With Navigator and Elasticsearch, it now takes less than a minute". | https://www.elastic.co/customers/docusign |
| BBVA | "BBVA transforms global banking operations with Elasticsearch". A search story. | https://www.elastic.co/customers/bbva |

---

## Land and expand

**Land (6 weeks):** one agent, the compliance assistant, with a context layer. Twenty definitions from a workshop with Compliance. Fifty real test questions. Success: correct on 90% of definition questions, tokens per task halved.

**Expand (two quarters):** the other agents read the same layer. Owners and review dates per definition. Profiles refreshed when an index changes. Every agent measured on correctness, tokens and time.

**Platform (later):** context as a shared service for every agent, including bought ones, through the query or an API. The same platform for search, observability and security.

**Why this order works:** the first team owns the definitions and feels the pain; each new agent reuses the layer instead of adding a prompt.

---

## Questions to ask the panel

- "As the Albisgrat team: which of your terms would an agent most likely get wrong?"
- "Where do you see AI Indices going next: the feedback loop from traces, or the setup agent?"
- Out of role: "What have customers surprised you with when they started building context layers?"
