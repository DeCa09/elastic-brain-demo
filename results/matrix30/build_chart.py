#!/usr/bin/env python3
"""Build chart.svg and MATRIX30.md from graded.csv and usage.csv.
Cost per question is an estimate: session tokens / 10 questions x the model's input list price."""
import csv, collections, math, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PRICE = {"haiku": 0.10, "sonnet": 2.00, "opus": 4.00, "fable": 8.00}
NAME = {"haiku": "Haiku 5.5", "sonnet": "Sonnet 5.5", "opus": "Opus 5.5", "fable": "Fable 5.2"}
ORDER = ["haiku", "sonnet", "opus", "fable"]
TIERS = [("lookup", "Plain lookup"), ("definition", "One bank definition"), ("two-definitions", "Two definitions combined"),
         ("join", "Join across registers"), ("superseded-rule", "Rule from the version in force"), ("no-definition", "Term the bank has not defined")]
score = collections.Counter(); tier = collections.Counter()
for r in csv.DictReader(open("graded.csv")):
    score[(r["model"], r["condition"])] += int(r["correct"]); tier[(r["tier"], r["model"], r["condition"])] += int(r["correct"])
tok = collections.Counter(); sec = collections.Counter(); cmd = collections.Counter()
for r in csv.DictReader(open("usage.csv")):
    k = (r["model"], r["condition"]); tok[k] += int(r["tokens"]); sec[k] += int(r["seconds"]); cmd[k] += int(r["commands"])
cost = lambda m, c: tok[(m, c)] / 30 * PRICE[m] / 1e6

W, H = 1280, 680
PL, PR, T, B = 80, 600, 170, 80
x0, x1 = math.log10(0.0006), math.log10(0.15)
X = lambda v: PL + (math.log10(v) - x0) / (x1 - x0) * (PR - PL)
Y = lambda v: H - B - v / 30 * (H - T - B)
INK, MUTED, GRID, BLUE, GREY, BG = "#1f1f1e", "#6b6a63", "#e4e2da", "#2a78d6", "#8a8980", "#fbfaf6"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="{BG}"/>',
     f'<text x="{PL}" y="42" font-size="26" font-weight="600" fill="{INK}">Context lifts every model to the top; without it, none gets past 19 of 30</text>',
     f'<text x="{PL}" y="70" font-size="15" fill="{MUTED}">30 bank questions per model, without and with the Elasticsearch context layer. Left: total score against cost. Right: score by kind of question.</text>',
     f'<rect x="{X(0.0006)}" y="{Y(31.5)}" width="{X(0.007)-X(0.0006)}" height="{Y(27)-Y(31.5)}" fill="#dff3e6"/>',
     f'<text x="{X(0.0066)}" y="{Y(27.6)}" font-size="12" fill="#1c6b3c" text-anchor="end">Cheap and correct</text>']
for v in (0, 10, 20, 30):
    o.append(f'<line x1="{PL}" x2="{PR}" y1="{Y(v)}" y2="{Y(v)}" stroke="{GRID}"/>')
    o.append(f'<text x="{PL-12}" y="{Y(v)+5}" font-size="13" fill="{MUTED}" text-anchor="end">{v}</text>')
for v in (0.001, 0.01, 0.1):
    o.append(f'<line x1="{X(v)}" x2="{X(v)}" y1="{H-B}" y2="{H-B+6}" stroke="{MUTED}"/>')
    o.append(f'<text x="{X(v)}" y="{H-B+24}" font-size="13" fill="{MUTED}" text-anchor="middle">${v:g}</text>')
o.append(f'<text x="{(PL+PR)/2}" y="{H-28}" font-size="13" fill="{MUTED}" text-anchor="middle">Estimated cost per question (USD, log scale)</text>')
o.append(f'<text transform="translate(26,{(T+H-B)/2}) rotate(-90)" font-size="13" fill="{MUTED}" text-anchor="middle">Correct answers (of 30)</text>')
o.append(f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker></defs>')
for m in ORDER:
    bx, by, cx, cy = X(cost(m, "base")), Y(score[(m, "base")]), X(cost(m, "ctx")), Y(score[(m, "ctx")])
    o.append(f'<line x1="{bx:.1f}" y1="{by-10:.1f}" x2="{cx:.1f}" y2="{cy+13:.1f}" stroke="{BLUE}" stroke-width="2" marker-end="url(#a)"/>')
    o.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="8" fill="{BG}" stroke="{GREY}" stroke-width="2.5"/>')
    o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{BLUE}" stroke="{BG}" stroke-width="2"/>')
    o.append(f'<text x="{cx:.1f}" y="{cy-(56 if m=="opus" else 34):.1f}" font-size="14" font-weight="600" fill="{INK}" text-anchor="middle">{NAME[m]}</text>')
    o.append(f'<text x="{cx:.1f}" y="{cy-17:.1f}" font-size="13" fill="{INK}" text-anchor="middle">{score[(m,"ctx")]}</text>')
    o.append(f'<text x="{bx:.1f}" y="{by+27:.1f}" font-size="13" fill="{MUTED}" text-anchor="middle">{score[(m,"base")]}</text>')
ly = Y(6)
o += [f'<circle cx="{PL+20}" cy="{ly}" r="7" fill="{BLUE}"/><text x="{PL+34}" y="{ly+5}" font-size="13" fill="{INK}">With context layer</text>',
      f'<circle cx="{PL+20}" cy="{ly+26}" r="7" fill="{BG}" stroke="{GREY}" stroke-width="2.5"/><text x="{PL+34}" y="{ly+31}" font-size="13" fill="{INK}">Without context</text>']
# tier grid
GX, GY, LW, CW, RH = 660, 170, 230, 92, 58
for j, m in enumerate(ORDER):
    o.append(f'<text x="{GX+LW+j*CW+CW/2}" y="{GY-14}" font-size="13" font-weight="600" fill="{INK}" text-anchor="middle">{NAME[m]}</text>')
for i, (t, label) in enumerate(TIERS):
    y = GY + i * RH
    o.append(f'<line x1="{GX}" x2="{GX+LW+4*CW}" y1="{y}" y2="{y}" stroke="{GRID}"/>')
    o.append(f'<text x="{GX}" y="{y+RH/2+5}" font-size="14" fill="{INK}">{label}</text>')
    for j, m in enumerate(ORDER):
        b, c = tier[(t, m, "base")], tier[(t, m, "ctx")]
        cx = GX + LW + j * CW + CW / 2
        if c > b: o.append(f'<rect x="{cx-CW/2+4}" y="{y+8}" width="{CW-8}" height="{RH-16}" rx="4" fill="#dbe9fb"/>')
        o.append(f'<text x="{cx}" y="{y+RH/2+6}" font-size="16" text-anchor="middle"><tspan fill="{MUTED}">{b}</tspan><tspan fill="{MUTED}"> → </tspan><tspan fill="{INK}" font-weight="600">{c}</tspan></text>')
o.append(f'<line x1="{GX}" x2="{GX+LW+4*CW}" y1="{GY+6*RH}" y2="{GY+6*RH}" stroke="{GRID}"/>')
o.append(f'<text x="{GX}" y="{GY+6*RH+24}" font-size="12" fill="{MUTED}">Correct of 5, without → with context. Shaded where context changed the score.</text>')
o += [f'<text x="{GX}" y="{H-58}" font-size="11.5" fill="{MUTED}">One run per cell, 240 answers in 24 sessions of ten questions, 18 Nov 2026. Fictional data.</text>',
      f'<text x="{GX}" y="{H-42}" font-size="11.5" fill="{MUTED}">Questions, data and context written by the presenter; answers graded against the data files.</text>',
      f'<text x="{GX}" y="{H-26}" font-size="11.5" fill="{MUTED}">Cost is an estimate: tokens reported by Claude Code x input list price.</text>', '</svg>']
open("chart.svg", "w").write("\n".join(o))

md = ["# Model matrix, 30 questions", "", "![chart](chart.png)", "",
      "| Model | Context | Correct (of 30) | Queries per question | Seconds per question | Est. cost per question |", "|---|---|---|---|---|---|"]
for m in ORDER:
    for c, lab in (("base", "No"), ("ctx", "Yes")):
        k = (m, c)
        md.append(f"| {NAME[m]} | {lab} | {score[k]} | {cmd[k]/30:.1f} | {sec[k]/30:.1f} | ${cost(m,c):.2g} |")
md += ["", "## By kind of question (correct of 5, without → with context)", "", "| Kind | " + " | ".join(NAME[m] for m in ORDER) + " |", "|---|---|---|---|---|"]
for t, label in TIERS:
    md.append(f"| {label} | " + " | ".join(f'{tier[(t,m,"base")]} → {tier[(t,m,"ctx")]}' for m in ORDER) + " |")
open("MATRIX30.md", "w").write("\n".join(md) + "\n")
for m in ORDER: print(m, score[(m,"base")], score[(m,"ctx")], round(cost(m,"base"),4), round(cost(m,"ctx"),4), round(cmd[(m,"base")]/30,1), round(cmd[(m,"ctx")]/30,1))

notes = """
## What it shows

- Without context every model scored 18 or 19 of 30. With context every model scored 29 or 30.
- The gap is entirely in questions that need a bank definition: alone, combined, or inside a join. Lookups, rules from the policy in force and undefined terms were answered correctly either way.
- Of the 45 baseline misses, 41 were the answer UNDEFINED and 4 were wrong records. The prompt told both agents not to guess, so the baseline mostly declined instead of guessing.
- With context no model invented a meaning for the five terms the bank has not defined.
- The one miss with context: Haiku 5.5 answered UNDEFINED for the retention period of recorded trading calls (Q23).
- The four models still do not separate. On this set the context layer decides the score and the model decides the price.

## Read this with care

- One run per cell. Agents are not deterministic.
- 30 questions, written together with the data and the context by the same person. 15 of the 30 depend on a definition that exists only in the context layer, so the baseline score mostly reflects that share.
- Ten questions per session. A baseline session explores once and reuses what it learned, so queries, seconds and cost per question are lower than in the 5-question run (`../matrix/`) and not comparable with it.
- Cost is an estimate: session tokens / 10 x the model's input list price (USD per million: Haiku 0.10, Sonnet 2, Opus 4, Fable 8). It ignores cache discounts and the output price. Most tokens are Claude Code's own overhead.
- Six of the definitions give the rule in words only, with no ready query; the agent composed the query itself.

Files: `questions.py` (questions and how each expected answer is computed), `answers/` (raw answers), `graded.csv`, `usage.csv`, `grade.py`, `build_chart.py`.
"""
open("MATRIX30.md", "a").write(notes)
