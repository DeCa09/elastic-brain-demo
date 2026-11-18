# Fallback plan

Rule for the day: **name the problem in one sentence, switch to the backup, keep the story and the clock.** Never debug live for more than 30 seconds.

This demo has one risk above all others: the trial's LLM quota. Plan for it.

## The backups

| Backup | What it is | Use it when |
|---|---|---|
| **Conversation history** | The agents' earlier conversations stay in Kibana. Opening one uses no LLM | Always for the baseline; for the Company Brain if the live run fails |
| **Screenshots** | Seven numbered screenshots in one PDF | A screen fails |
| **Recording** | One silent video of the 12 minutes; you narrate | Kibana, the network or the laptop fails |
| **`results/answers/`** | The agents' full answers from my test runs, as text files | Everything else fails |

## How to prepare them (45 minutes, the day before)

1. `scripts/preflight.sh` is green.
2. In Kibana, ask **Albisgrat Baseline** question 1 from the runbook. Wait 30 minutes.
3. Ask **Albisgrat Company Brain** question 1, then question 2, each in its own conversation. Do not delete these conversations: they are your live fallback.
4. Record the screen (`Shift + Command + 5`, "Record Selected Portion", microphone off) while you walk through the runbook, opening the existing conversations instead of asking again. Save as `recordings/demo-backup.mov`.
5. Take one screenshot per step:

   | File | Shows |
   |---|---|
   | `01-three-indices.png` | Query A |
   | `02-baseline-steps.png` | The baseline exploring |
   | `03-baseline-wrong.png` | The baseline's answer with ten arrangements |
   | `04-ai-index.png` | Queries B and C: the Knowledge Indicators and one definition |
   | `05-workflow.png` | The workflow and its steps |
   | `06-brain-correct.png` | The Company Brain's answer with twelve arrangements and its two steps |
   | `07-location-answer.png` | The answer to question 2 |

6. Make one PDF of the screenshots. Copy video and PDF to a second device.
7. Check that no API key or password is visible in anything you recorded.

## What to do when something fails

### Case A. The agent returns an error about a trial limit, or does not answer

Do not retry with the same model: in my test it stayed blocked for more than 20 minutes. If you found the model selector in your walk-through, switch to another managed model and ask once more. Otherwise:

Say: "The trial account limits how much I can use the model, and I have just hit that limit. Here is the same question from yesterday." Open yesterday's Company Brain conversation (or screenshot 06). Then add, because it serves your thesis: "This limit is the point of the whole talk in miniature: tokens are a budget. On my test questions the baseline used about three times as many of them."

Continue with the numbers at 9:15. Skip question 2 unless its earlier conversation is open.

### Case B. The live answer is wrong

Say so before anyone else does. Open query C, read the definition, and show that the right rule is in Elasticsearch. "The context was right; the model misapplied it. That is why every Knowledge Indicator carries the query: you can check the answer." Then show screenshot 06.

### Case C. Discover or Workflows does not load

Use the screenshots for that step and keep talking. The agent tabs are what matter.

### Case D. No network, Kibana unreachable, laptop trouble

Play the recording and narrate it. If that fails, walk through the PDF. Keep the same time checks.

### Case E. You are running over

Cut in this order: question 2 (7:30), the workflow's last run (part of 4:45), query A (0:00). Never cut: the baseline's wrong answer, the definition in the AI Index, the live correct answer, the numbers, the recap.

## The 3 biggest risks and how they are covered

| Risk | Likelihood | Cover |
|---|---|---|
| 1. The trial's LLM quota is exhausted during or just before the demo | High if you use the agents in the hour before the session; medium otherwise, because the limit is not published | No baseline runs live; at most three live questions; no agent use after 12:00; a second model as a switch; yesterday's conversations and screenshots |
| 2. The flow has not been clicked through in Kibana: a menu, a tab or the steps view is not where the runbook says | Certain to some degree until you have walked through it once | Walk through it the day before and correct the runbook; screenshots per step |
| 3. The live agent answers differently from my test (agents are not deterministic) | Medium | Expected ids are in the runbook, so you can check the answer on sight; the definition and its query are in the AI Index to show; screenshot of a correct answer |
