# Sources

Checked on 18 November 2026. Verification levels:

- **Tested**: I ran it on the Serverless project. See `TEST_LOG.md`.
- **Article**: taken from the text of an article you pasted into our conversation. I did not open the page myself, so check the wording against the live page before you quote it.
- **Page / Docs**: read on elastic.co on 13 or 14 November for the first two demos.
- **Opinion**: your thesis. Present it as your view.

## Elastic: AI Indices and Knowledge Indicators

| Fact | Level | Source |
|---|---|---|
| An AI Index is a regular index or data stream whose name starts with `ai-index-idx-` or `ai-index-ds-`; the prefix triggers component templates that configure the mapping. | Article + Tested (the templates exist on the project and applied the mapping) | Elasticsearch Labs, "Building context in Elasticsearch: how AI Indices power smarter agents using fewer tokens", 11 August 2026 |
| The mapping gives `title`, `description` and `content` a `semantic_text` sub-field on `.jina-embeddings-v5-text-small`, plus `type`, `tags`, `attributes`, `references.uri`. | Article + Tested | same |
| "While AI indices will be included in future Stack releases, today we recommend using Serverless." | Article + Tested (no such templates on the Hosted 9.5.6 deployment) | same |
| Kibana Workflows can read mappings, sample documents, call an LLM step (`ai.agent`) with a schema, and write the result to an index. | Article + Tested (one run, 107 seconds) | same |
| In the article's example, the agent with Knowledge Indicators used 92,711 tokens against 167,763 without (about 45% fewer), with 8 tool calls against 12, and the same correct answer. | Article | same |
| The article says that in production "a setup agent would generate" the workflows "and a feedback loop would refine KIs from the agent's own traces". Not part of this demo. | Article | same |
| ES\|QL `FORK` and `FUSE` run a keyword and a semantic search and fuse them in one query. | Article + Tested | same |
| Agent Builder: custom agents, custom ES\|QL tools with parameters, the `converse` API. | Docs + Tested | Kibana API reference |
| Workflows API: `POST /api/workflows/workflow`, `/run`, `GET /api/workflows/executions/{id}`. | Docs + Tested | Kibana API reference |
| The trial limits LLM use per model; when reached, the error says the quota refills after some minutes. | Tested (error message on 18 November) | the project itself |

## Snowflake: Cortex Sense

All from Snowflake's blog post "Introducing Cortex Sense: Grounded Context for the Data You Never Modeled" (30 June 2026), as you pasted it. These are Snowflake's own claims about its own product and internal tests. The post carries a forward-looking-statements notice.

| Claim in the post | Level |
|---|---|
| Without a context layer, agents answered Snowflake's internal product analytics questions with about 25% accuracy; the post says Anthropic independently measured 21%. | Article |
| On Snowflake's benchmark of hard questions, Cortex Sense improved accuracy from 24.1% to 86.3% and reduced cost per query from $1.76 to $0.59 against a frontier agent. | Article |
| Semantic views covered under 5% of Snowflake's 9,685 tables. | Article |
| Cortex Sense ingests metadata and usage patterns, not data rows; it ranks signals by relevance, authority, popularity and freshness; it surfaces conflicting definitions to a human. | Article |
| Private preview was announced for mid July 2026. | Article |

Use these as "the industry sees the same problem", with the source named. Do not present them as Elastic results or as independently verified.

## The thesis

| Statement | Level |
|---|---|
| "The models are good enough; context is the missing piece." | Opinion |
| That named people have announced AGI, or what any CEO said about a specific model. | Not verified by me. Quote only what you have a link for, or leave it out |

## Data

| Fact | Level | Source |
|---|---|---|
| Law texts come from Fedlex, the publication platform for Swiss federal law, with source URLs per article. | Tested | `data/fetch_public.py` |
| FINMA circulars are not in the dataset: FINMA's site terms require written consent for reproduction. | Page | https://www.finma.ch/de/rechtliches/ |
| The bank, its documents, the outsourcing inventory and the incident register are fictional. The bank's definitions of "material outsourcing" and "reportable incident" are invented for the demo and are not regulatory definitions. | | `data/`, `brain/setup_brain.py` |

## Customer stories

Quoted from elastic.co on 14 November 2026. Read the pages again before the interview.

| Customer | What the page says | Source |
|---|---|---|
| EY | "EY puts Elastic at the heart of GenAI experience for financial sector". "Elastic's RAG setup was able to produce results 3 times faster when compared to Native RAG approaches". | https://www.elastic.co/customers/ey |
| Docusign | "Traditionally, this could take hours. With Navigator and Elasticsearch, it now takes less than a minute". | https://www.elastic.co/customers/docusign |
| BBVA | "BBVA transforms global banking operations with Elasticsearch". A search story, not a GenAI story. | https://www.elastic.co/customers/bbva |
