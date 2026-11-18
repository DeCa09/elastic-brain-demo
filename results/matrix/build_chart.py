#!/usr/bin/env python3
"""Build chart.svg and MATRIX.md from runs.csv.
Cost per task is an estimate: tokens reported by Claude Code x the model's input list price."""
import csv, collections, math

PRICE = {"haiku": 0.10, "sonnet": 2.00, "opus": 4.00, "fable": 8.00}   # USD per million input tokens
NAME = {"haiku": "Haiku 5.5", "sonnet": "Sonnet 5.5", "opus": "Opus 5.5", "fable": "Fable 5.2"}
ORDER = ["haiku", "sonnet", "opus", "fable"]

runs = collections.defaultdict(list)
for r in csv.DictReader(open("runs.csv")):
    runs[(r["model"], r["condition"])].append(r)

def cell(m, c):
    v = runs[(m, c)]; n = len(v)
    tok = sum(int(x["tokens"]) for x in v) / n
    return dict(n=n, correct=sum(int(x["correct"]) for x in v),
                commands=sum(int(x["commands"]) for x in v) / n, tokens=tok,
                seconds=sum(int(x["seconds"]) for x in v) / n, cost=tok * PRICE[m] / 1e6)

S = {(m, c): cell(m, c) for m in ORDER for c in ("base", "ctx")}

W, H, L, R, T, B = 960, 600, 90, 40, 110, 80
x0, x1 = math.log10(0.004), math.log10(1.5)
X = lambda v: L + (math.log10(v) - x0) / (x1 - x0) * (W - L - R)
Y = lambda v: H - B - v / 5 * (H - T - B)
INK, MUTED, GRID, BLUE, GREY = "#1f1f1e", "#6b6a63", "#e4e2da", "#2a78d6", "#8a8980"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
     f'<text x="{L}" y="40" font-size="24" font-weight="600" fill="{INK}">Context moves every model up; the model only moves the price</text>',
     f'<text x="{L}" y="66" font-size="14" fill="{MUTED}">Correct answers out of 5 bank questions, by model, without and with the Elasticsearch context layer</text>',
     f'<rect x="{X(0.004)}" y="{Y(5.35)}" width="{X(0.03)-X(0.004)}" height="{Y(4.5)-Y(5.35)}" fill="#dff3e6"/>',
     f'<text x="{X(0.029)}" y="{Y(4.62)}" font-size="12" fill="#1c6b3c" text-anchor="end">Cheap and correct</text>']
for v in range(6):
    o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v)}" y2="{Y(v)}" stroke="{GRID}"/>')
    o.append(f'<text x="{L-12}" y="{Y(v)+5}" font-size="13" fill="{MUTED}" text-anchor="end">{v}</text>')
for v in (0.01, 0.03, 0.1, 0.3, 1):
    o.append(f'<line x1="{X(v)}" x2="{X(v)}" y1="{H-B}" y2="{H-B+6}" stroke="{MUTED}"/>')
    o.append(f'<text x="{X(v)}" y="{H-B+24}" font-size="13" fill="{MUTED}" text-anchor="middle">${v:g}</text>')
o.append(f'<text x="{(L+W-R)/2}" y="{H-22}" font-size="13" fill="{MUTED}" text-anchor="middle">Estimated cost per question (USD, log scale)</text>')
o.append(f'<text transform="translate(28,{(T+H-B)/2}) rotate(-90)" font-size="13" fill="{MUTED}" text-anchor="middle">Correct answers (of 5)</text>')
o.append(f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker></defs>')
for m in ORDER:
    b, c = S[(m, "base")], S[(m, "ctx")]
    bx, by, cx, cy = X(b["cost"]), Y(b["correct"]), X(c["cost"]), Y(c["correct"])
    o.append(f'<line x1="{bx:.1f}" y1="{by-10:.1f}" x2="{cx:.1f}" y2="{cy+13:.1f}" stroke="{BLUE}" stroke-width="2" marker-end="url(#a)"/>')
    o.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="8" fill="#fbfaf6" stroke="{GREY}" stroke-width="2.5"/>')
    o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{BLUE}" stroke="#fbfaf6" stroke-width="2"/>')
    o.append(f'<text x="{cx:.1f}" y="{cy-18:.1f}" font-size="14" font-weight="600" fill="{INK}" text-anchor="middle">{NAME[m]}</text>')
    o.append(f'<text x="{bx:.1f}" y="{by+26:.1f}" font-size="12" fill="{MUTED}" text-anchor="middle">${b["cost"]:.2g}</text>')
lx = W - R - 190
o += [f'<circle cx="{lx}" cy="{Y(1.1)}" r="7" fill="{BLUE}"/><text x="{lx+14}" y="{Y(1.1)+5}" font-size="13" fill="{INK}">With context layer</text>',
      f'<circle cx="{lx}" cy="{Y(0.6)}" r="7" fill="#fbfaf6" stroke="{GREY}" stroke-width="2.5"/><text x="{lx+14}" y="{Y(0.6)+5}" font-size="13" fill="{INK}">Without context</text>',
      f'<text x="{W-R}" y="{Y(2.35)}" font-size="11" fill="{MUTED}" text-anchor="end">One run per cell, 40 runs, 18 Nov 2026. Fictional data.</text>',
      f'<text x="{W-R}" y="{Y(2.35)+15}" font-size="11" fill="{MUTED}" text-anchor="end">Questions, data and context written by the presenter.</text>',
      f'<text x="{W-R}" y="{Y(2.35)+30}" font-size="11" fill="{MUTED}" text-anchor="end">Cost is an estimate: reported tokens x input list price.</text>',
      '</svg>']
open("chart.svg", "w").write("\n".join(o))

md = ["# Model matrix: four models, with and without the context layer", "",
      "![chart](chart.svg)", "",
      "| Model | Context | Correct (of 5) | Queries per question | Seconds | Tokens | Est. cost per question |", "|---|---|---|---|---|---|---|"]
for m in ORDER:
    for c, lab in (("base", "No"), ("ctx", "Yes")):
        s = S[(m, c)]
        md.append(f'| {NAME[m]} | {lab} | {s["correct"]} | {s["commands"]:.1f} | {s["seconds"]:.0f} | {s["tokens"]:,.0f} | ${s["cost"]:.2g} |')
md += ["", "## What it shows", "",
 "- Every model scored 3 of 5 without context and 5 of 5 with it.",
 "- Without context, all four models failed the same two questions, the ones that need a bank definition (material outsourcing, reportable incident). Each said it found no definition and guessed.",
 "- Haiku 5.5 with context was right on all five at an estimated USD 0.007 per question. Fable 5.2 without context was right on three at about USD 0.62.",
 "", "## Read this with care", "",
 "- One run per cell. Agents are not deterministic.",
 "- Five questions, written together with the data and the context by the same person. Two of them were chosen because they need a definition.",
 "- Cost is an estimate: tokens reported by Claude Code times the model's input list price (USD per million: Haiku 0.10, Sonnet 2, Opus 4, Fable 8). It ignores cache discounts and the higher output price. About 65,000 of each run's roughly 70,000 tokens are Claude Code's own overhead, so the chart shows the price gap between models, not token savings from context. For token savings use `../RESULTS.md`.",
 "- The agents ran as Claude Code subagents with `agent/baseline` and `agent/with-context` instructions. Raw rows: `runs.csv`. Rebuild: `python3 build_chart.py`."]
open("MATRIX.md", "w").write("\n".join(md) + "\n")
for k, s in S.items(): print(k, s["correct"], round(s["cost"], 4))
