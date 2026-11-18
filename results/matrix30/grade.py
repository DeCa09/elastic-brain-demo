#!/usr/bin/env python3
"""Grade answers/<model>-<base|ctx>-<batch>.txt against questions.json. Writes graded.csv."""
import json, re, os, glob, csv, collections
HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "questions.json")))}
IDS = re.compile(r"(?:OUT-\d{3}|INC-2026-\d{3})")

def correct(q, ans):
    exp = q["expected"]
    if exp == ["UNDEFINED"]:
        return "UNDEFINED" in ans.upper() and not IDS.findall(ans)
    if IDS.match(exp[0]):
        return sorted(set(IDS.findall(ans))) == exp
    if exp[0].isdigit():
        m = re.search(r"\d+", ans)
        return bool(m) and m.group() == exp[0]
    return exp[0].lower() in ans.lower()

rows = []
for path in sorted(glob.glob(os.path.join(HERE, "answers", "*.txt"))):
    model, cond, _ = os.path.basename(path)[:-4].split("-")
    seen = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\s*(Q\d{2})\s*:\s*(.*)", line)
        if m: seen[m.group(1)] = m.group(2).strip()
    batch_ids = [l.split(":")[0] for l in open(os.path.join(HERE, "batch%s.txt" % path[-5]))]
    for qid in batch_ids:
        ans = seen.get(qid, "")
        rows.append(dict(model=model, condition=cond, question=qid, tier=QS[qid]["tier"],
                         correct=int(correct(QS[qid], ans)), answer=ans))
csv.DictWriter(open(os.path.join(HERE, "graded.csv"), "w", newline=""), fieldnames=list(rows[0])).writeheader()
w = csv.DictWriter(open(os.path.join(HERE, "graded.csv"), "a", newline=""), fieldnames=list(rows[0])); w.writerows(rows)
tot = collections.Counter(); n = collections.Counter()
for r in rows: tot[(r["model"], r["condition"])] += r["correct"]; n[(r["model"], r["condition"])] += 1
for k in sorted(tot): print(k, "%d/%d" % (tot[k], n[k]))
