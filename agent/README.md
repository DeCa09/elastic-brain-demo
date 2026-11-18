# The same comparison with an agent outside Elastic

Two Claude Code sessions use the Elasticsearch project as their data and context layer. They do not use Agent Builder, so they do not touch the Elastic trial's LLM allowance. They use your own Claude plan instead.

| Folder | What the session gets |
|---|---|
| `baseline/` | The three source indices, `esql.sh` and `mapping.sh`. No context. |
| `with-context/` | The same, plus the `query-ki` skill: one hybrid ES\|QL query over the AI Index `ai-index-idx-albisgrat`, run before anything else. |

Both folders deny reading the repository's data files, results and documentation, so the session can only learn from Elasticsearch.

## Run it

Needs: Claude Code, `curl`, `python3`, and a filled `.env` in the repository root (see `SETUP.md`).

Terminal 1:

```bash
cd agent/baseline && claude
```

Terminal 2:

```bash
cd agent/with-context && claude
```

Ask both the same question:

```
Welche unserer Auslagerungen gelten als wesentliche Auslagerungen? Liste die IDs auf.
```

Expected: OUT-001, 002, 003, 004, 006, 007, 008, 010, 011, 016, 019, 024 (12 arrangements).

Approve the `../esql.sh` and `../mapping.sh` commands when asked, or allow them once for the session.

## What happened in my test

One run each, 18 November 2026, as subagents of one Claude Code session (not two separate terminals).

| | Baseline | With context |
|---|---|---|
| Answer | Wrong: 10 arrangements. Assumed "material" means high criticality. Missed OUT-006, OUT-010, OUT-019; included OUT-021 | Right: all 12 |
| Queries against Elasticsearch | 9 | 2 |
| Time | 30 s | 17 s |
| Tokens, as reported by Claude Code | 73,947 | 70,549 |

The baseline said openly that it found no definition and was guessing. That is the point of the demo: the threshold is written nowhere in the data.

**Read this with care.**
- One run each. Agents are not deterministic.
- The token figures are nearly equal and are not a fair measure of savings here. Most of each count is Claude Code's own system prompt and tools, which both sessions carry. Use the Agent Builder figures in `results/RESULTS.md` for the cost argument, and this test for the correctness argument.
- Not tested: two real terminal sessions on a Mac, and the permission prompts you will see there.

## How to use it in the interview

- Keep Agent Builder for the answer with context. It shows Elastic's own product.
- Use the `baseline/` session if you want to show the uninformed agent live. It costs no trial allowance.
- If the trial's LLM limit blocks Agent Builder, run both sessions here. The context layer is the same index; only the agent changes. That is also a fair answer to "does this lock us into your agent?": no, any agent that can run a query can read the layer.
