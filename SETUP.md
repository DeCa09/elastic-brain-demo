# Setup

**Where things stand (18 November 2026).** Your Serverless project `albisgrat-brain` already holds the finished demo. I built and tested it there through the APIs. What is left for you: get the project on your Mac, walk through the flow in Kibana once, and record the backups.

## What exists on the project

| Piece | Name |
|---|---|
| Source index | `albisgrat-knowledge`: 1,255 Swiss law articles and 26 fictional internal documents |
| Source index | `albisgrat-outsourcing-inventory`: 24 fictional outsourcing arrangements |
| Source index | `albisgrat-incidents`: 43 fictional incidents |
| AI Index | `ai-index-idx-albisgrat`: 45 Knowledge Indicators |
| Workflow | `albisgrat-index-profile-ki` |
| Tool | `albisgrat.brain.query_ki`: one hybrid ES\|QL query over the AI Index |
| Agents | "Albisgrat Company Brain" and "Albisgrat Baseline (no context)" |

## 0. The trial clock and the LLM quota

- The trial started on 14 November and runs to about **28 November**. The interview is on the 24th.
- LLM use is limited per model. When the limit is hit, agents return an error; in my test it lasted more than 20 minutes. Baseline runs are what exhaust it. Another managed model keeps working. See "The one rule" in `RUNBOOK.md`.

## 1. Get the project

```bash
git clone https://github.com/DeCa09/elastic-brain-demo.git
```

```bash
cd elastic-brain-demo
```

You need `python3` (3.9 or newer, standard library only) and `curl`. No Docker.

## 2. Fill in `.env`

```bash
cp .env.example .env
```

| Variable | Value |
|---|---|
| `KIBANA_URL` | The Serverless project's Kibana endpoint, no trailing slash |
| `ELASTICSEARCH_URL` | The project's Elasticsearch endpoint, without `:443` |
| `ELASTIC_API_KEY` | An API key created in that project (encoded value). Create a fresh one named `brain-setup-mac` |

## 3. Check

```bash
scripts/preflight.sh
```

It checks the indices, the agents and the context lookup. It does not use the LLM.

## 4. Walk through it in Kibana

Follow `RUNBOOK.md`, "Before the session, the day before". This is the first time anyone clicks through the flow, so allow 45 minutes and correct the click names in the runbook as you go.

## 5. Rebuild, if you ever need to

```bash
scripts/setup.sh all
```

Creates the three source indices, the AI Index with hand-written Knowledge Indicators, the tool and both agents. No LLM is used. Then, to replace the three hand-written index profiles with generated ones (about two minutes, uses the LLM):

```bash
scripts/setup.sh workflow
```

Other commands: `scripts/setup.sh status`, `definitions` (rewrite only the business definitions), `delete`.

On a new project, create it as **Elasticsearch Serverless**. AI Indices do not exist on Hosted deployments today: the index would be created, but without Elastic's managed mapping.

## 6. Repeat the measurement

```bash
scripts/compare.sh material
```

One question id at a time: `material`, `reportable`, `location`, `overdue`, `late-breaches`. Each call runs the question on both agents and updates `results/RESULTS.md`; earlier runs are kept. Add `--only-brain` to skip the expensive baseline. Leave at least half an hour between baseline runs. To use another managed model when the default is blocked, put `LLM_INFERENCE_ID=.anthropic-claude-5-sonnet-chat_completion` in `.env`.

## 7. Change what the brain knows

The business definitions and the glossary are in `brain/setup_brain.py` (`DEFINITIONS`, `GLOSSARY`). Edit, then:

```bash
scripts/setup.sh definitions
```

To change the data, edit `data/generate_registers.py`, run it, and run `scripts/setup.sh sources`.

## 8. After the interview

```bash
scripts/setup.sh delete
```

Then delete the project in the Elastic Cloud console.

## Files

| File | Purpose |
|---|---|
| `data/public/fedlex.jsonl`, `data/internal/` | Law articles (with source URLs) and fictional bank documents |
| `data/outsourcing_inventory.jsonl`, `data/incidents.jsonl` | The two fictional registers |
| `brain/knowledge_index.py` | Mapping and ingest pipeline of the knowledge index |
| `brain/setup_brain.py` | Sources, AI Index, Knowledge Indicators, tool, agents, workflow |
| `brain/workflow-index-profiles.yaml` | The Kibana Workflow |
| `brain/compare.py` | The measurement |
| `results/` | `RESULTS.md` and the agents' full answers |
