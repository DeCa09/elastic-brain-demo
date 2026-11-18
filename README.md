# Elastic company-brain demo kit

Everything for the Elastic Solutions Architect panel interview (**Tuesday 24 November 2026, 13:00 to 14:00 CET**) built around one thesis:

> **The models are smart enough. What they lack is your context. Elasticsearch can hold that context.**

**The demo:** one model answers one question twice. Without context it explores the bank's data, guesses what a bank-specific term means, and gets it wrong. With a context layer in Elasticsearch (an AI Index of Knowledge Indicators) it answers correctly in 20 seconds with a quarter of the tokens.

This kit is separate from the compliance-assistant demo in `DeCa09/elastic-search-demo`, which stays available as the safe alternative.

## Read in this order

| File | What it is |
|---|---|
| `README.md` | This page |
| `SETUP.md` | What exists on your Serverless project and what is left for you |
| `RUNBOOK.md` | The 12-minute demo, minute by minute, with talk track, German terms, queries and questions |
| `FALLBACK.md` | What to do when something fails, above all the LLM quota |
| `DECK.md` | 10-slide outline with speaker notes, timings and the cost model |
| `QA_PREP.md` | Questions per panel role, Cortex Sense, land and expand |
| `results/RESULTS.md` | The measurement, per question; full answers in `results/answers/` |
| `diagrams/architecture.svg` | Architecture diagram for slide 4 |
| `SOURCES.md` | Every fact with its source and how well it is verified |
| `TEST_LOG.md` | What was run and what is untested |

## The measurement

Five questions in German, English and French. Same data and the same query tools for both agents. "Correct" means the answer names exactly the records computed from the data files.

| | Without context | With Knowledge Indicators |
|---|---|---|
| Correct answers | 3 of 5 | 5 of 5 |
| Questions that need a bank definition | 0 of 2 | 2 of 2 |
| Tokens per question | 193,000 | 51,000 |
| Seconds per question | 52 | 22 |
| Tool calls per question | 6.8 | 3.4 |

**Read this with care.** Five questions, one run each; agents are not deterministic. I wrote the questions, the data and the context, so this is a demonstration, not an independent benchmark. Four questions ran on the project's default model and one on another managed model, because the trial's rate limit blocked the first. Where a question needed no bank-specific definition, both agents were right and context only made the answer cheaper and faster.

## What is on the project

- **Three source indices:** the knowledge base (1,255 Swiss law articles from Fedlex, 26 fictional internal documents), a fictional outsourcing inventory (24 rows) and a fictional incident register (43 rows).
- **An AI Index** with 45 Knowledge Indicators: 3 index profiles written by a Kibana Workflow with an LLM, 7 business definitions and 12 glossary entries written by hand, 23 policy register entries derived by script.
- **One tool:** a hybrid ES|QL query over the AI Index.
- **Two agents:** "Albisgrat Company Brain", which reads the indicators first, and "Albisgrat Baseline (no context)".

## Status

**Tested through the APIs on the Serverless project (Elasticsearch 9.7.0):** the indices, the AI Index and its managed mapping, the context lookup, the workflow (one run, 107 seconds), both agents, eleven agent runs for the measurement, and the Discover queries in the runbook.

**Not tested:**
- **The flow in the Kibana interface.** Nobody has clicked through it yet. Do this first (`SETUP.md` step 4).
- **The model selector in the chat,** which is your way out when the default model is rate-limited. Switching model works through the API.
- **The scripts on your Mac.**
- **Permissions on the AI Index.**

## The three biggest risks

1. **The trial's LLM quota.** It blocked me twice, for more than 20 minutes. Never run the baseline live, ask at most three live questions, and stay off the agents for an hour before the session.
2. **An unrehearsed interface.** The runbook's click names are my best reading. Your walk-through fixes that.
3. **A panel that knows the feature better.** AI Indices are Elastic's own, new, and Serverless-only. Say what you built and measured, and say what you have not tried.

## Quick start on your Mac

```bash
cp .env.example .env        # then fill it in, see SETUP.md step 2
```

```bash
scripts/preflight.sh
```

## Rules of this project

- Secrets live only in `.env`, which git ignores.
- The trial is free. Nothing here costs money unless you subscribe or connect a paid model of your own.
- The bank, its registers, its documents and its definitions are fictional. The law texts are real and keep their Fedlex source URLs.
- Numbers from Elastic's and Snowflake's articles are labelled as theirs wherever they appear.
