#!/usr/bin/env python3
"""The 30-question set for the model matrix. Expected answers are computed from the data files.
Run it to write questions.json (with answers) and the three batch prompts (without answers)."""
import json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data")
inv = [json.loads(l) for l in open(os.path.join(DATA, "outsourcing_inventory.jsonl"))]
inc = [json.loads(l) for l in open(os.path.join(DATA, "incidents.jsonl"))]
A = {r["arrangement_id"]: r for r in inv}
TODAY, QUARTER_START = "2026-11-18", "2026-10-01"
aid = lambda rows: sorted(r["arrangement_id"] for r in rows)
iid = lambda rows: sorted(r["incident_id"] for r in rows)

material = lambda r: r["status"] == "active" and r["contains_client_data"] and (r["criticality"] == "high" or r["annual_cost_chf"] >= 200000)
overdue = lambda r: r["status"] == "active" and r["last_review"] < "2025-11-18"
bad_loc = lambda r: r["contains_client_data"] and (r["data_location"] not in ("CH", "EU") or (r["data_location"] == "EU" and not r["board_approval_eu"]))
approved = lambda r: r["approved_management"] and r["approved_ciso"] and r["approved_compliance"]
legacy = lambda r: r["status"] == "active" and r["contract_signed"] < "2025-07-01"
large = lambda r: r["annual_cost_chf"] >= 120000
exitplan = lambda r: material(r) and r["provider_type"] == "cloud"
reportable = lambda i: (i["category"] == "data_breach" and i["severity"] in ("medium", "high")) or i["category"] == "access_violation"
serious = lambda i: i["severity"] == "high" and i["category"] in ("data_breach", "system_outage")
third = lambda i: i["related_arrangement_id"] is not None
stale = lambda i: i["status"] == "open" and i["date"] < QUARTER_START
linked = lambda i: A.get(i["related_arrangement_id"])
n_inc = collections.Counter(i["related_arrangement_id"] for i in inc if third(i))

Q = [  # (id, tier, question, expected)
 ("Q01", "lookup", "Which provider runs arrangement OUT-007? Give the provider code.", [A["OUT-007"]["provider_code"]]),
 ("Q02", "lookup", "How many incidents were recorded in the Geneva office in 2026? Give the number.", [str(sum(1 for i in inc if i["office"] == "Geneva"))]),
 ("Q03", "lookup", "Welche Auslagerungen haben den Status 'planned'?", aid(r for r in inv if r["status"] == "planned")),
 ("Q04", "lookup", "Which arrangements have their data location in the EU?", aid(r for r in inv if r["data_location"] == "EU")),
 ("Q05", "lookup", "Which phishing incidents had severity high?", iid(i for i in inc if i["category"] == "phishing" and i["severity"] == "high")),
 ("Q06", "definition", "Welche unserer Auslagerungen gelten als wesentliche Auslagerungen?", aid(r for r in inv if material(r))),
 ("Q07", "definition", "Which reportable incidents did we have in the third quarter of 2026?", iid(i for i in inc if reportable(i) and "2026-07-01" <= i["date"] <= "2026-09-30")),
 ("Q08", "definition", "Which incidents in 2026 were serious incidents?", iid(i for i in inc if serious(i))),
 ("Q09", "definition", "Welche Vorfälle sind Altfälle?", iid(i for i in inc if stale(i))),
 ("Q10", "definition", "For which arrangements is an exit plan required?", aid(r for r in inv if exitplan(r))),
 ("Q11", "two-definitions", "Which material outsourcings have an overdue review?", aid(r for r in inv if material(r) and overdue(r))),
 ("Q12", "two-definitions", "Which large contracts are not fully approved?", aid(r for r in inv if large(r) and not approved(r))),
 ("Q13", "two-definitions", "Welche Altverträge verletzen die Regeln zum Datenstandort?", aid(r for r in inv if legacy(r) and bad_loc(r))),
 ("Q14", "two-definitions", "Which incidents were both serious incidents and third-party incidents?", iid(i for i in inc if serious(i) and third(i))),
 ("Q15", "two-definitions", "Which legacy contracts need an exit plan and are also large contracts?", aid(r for r in inv if legacy(r) and exitplan(r) and large(r))),
 ("Q16", "join", "Which reportable incidents involved a material outsourcing?", iid(i for i in inc if reportable(i) and linked(i) and material(linked(i)))),
 ("Q17", "join", "Which incidents involved an arrangement whose data location breaks our directive?", iid(i for i in inc if linked(i) and bad_loc(linked(i)))),
 ("Q18", "join", "Which arrangements were involved in two or more incidents in 2026?", sorted(k for k, v in n_inc.items() if v >= 2)),
 ("Q19", "join", "Which cloud-related incidents happened in the first half of 2026?", iid(i for i in inc if linked(i) and linked(i)["provider_type"] == "cloud" and i["date"] <= "2026-06-30")),
 ("Q20", "join", "Welche wesentlichen Auslagerungen waren 2026 an keinem Vorfall beteiligt?", aid(r for r in inv if material(r) and n_inc[r["arrangement_id"]] == 0)),
 ("Q21", "superseded-rule", "How many years do we keep client files after the business relationship ends? Give the number.", ["10"]),
 ("Q22", "superseded-rule", "Which arrangements that hold client data in the EU are allowed under our directive?", aid(r for r in inv if r["contains_client_data"] and r["data_location"] == "EU" and r["board_approval_eu"])),
 ("Q23", "superseded-rule", "How many years do we keep recorded phone calls of the trading desk? Give the number.", ["2"]),
 ("Q24", "superseded-rule", "Wie viele Stellen müssen eine Auslagerung vor der Vertragsunterzeichnung genehmigen? Nenne die Zahl.", ["3"]),
 ("Q25", "superseded-rule", "For how many months do we keep application documents of candidates we did not hire? Give the number.", ["6"]),
 ("Q26", "no-definition", "Which of our providers are strategic partners?", ["UNDEFINED"]),
 ("Q27", "no-definition", "Which incidents in 2026 were near misses?", ["UNDEFINED"]),
 ("Q28", "no-definition", "Welche Auslagerungen sind Tier-1-Auslagerungen?", ["UNDEFINED"]),
 ("Q29", "no-definition", "Which arrangements are in run-off?", ["UNDEFINED"]),
 ("Q30", "no-definition", "Which incidents were client-impacting incidents?", ["UNDEFINED"]),
]
BATCHES = [[q for i, q in enumerate(Q) if (i * 7) % 3 == b] for b in range(3)]

if __name__ == "__main__":
    json.dump([dict(id=a, tier=b, question=c, expected=d) for a, b, c, d in Q],
              open(os.path.join(HERE, "questions.json"), "w"), indent=1, ensure_ascii=False)
    for n, batch in enumerate(BATCHES, 1):
        open(os.path.join(HERE, "batch%d.txt" % n), "w").write("\n".join("%s: %s" % (q[0], q[2]) for q in batch) + "\n")
    for a, b, c, d in Q: print(a, b.ljust(16), len(d), d if len(d) < 9 else d[:8] + ["..."])
    print([len(b) for b in BATCHES], [[q[0] for q in b] for b in BATCHES])
