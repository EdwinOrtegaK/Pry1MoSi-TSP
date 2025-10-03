# scripts/make_summary_eil101.py
import json, glob, csv

GA_GLOBS = ["results/eil101/ga_seed*.json", "results/eil101/ga_*strong*.json"]
paths = []
for pat in GA_GLOBS:
    paths.extend(glob.glob(pat))
paths = sorted(set(paths))
assert paths, "No GA JSONs found in results/eil101"

# lee óptimo MTZ
with open("results/eil101/mtz_opt.json", "r", encoding="utf-8") as f:
    mtz = json.load(f)
opt = float(mtz["objective"])

rows = []
for p in paths:
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    best_cost = float(data["best"]["cost"])
    prms = data["params"]
    rows.append({
        "instance": "eil101",
        "seed": prms.get("seed"),
        "N": prms.get("N"),
        "maxIter": prms.get("maxIter"),
        "crossover": prms.get("crossover"),
        "pmut": prms.get("pmut"),
        "elitism": prms.get("elitism"),
        "best_cost": best_cost,
        "opt_mtz": opt,
        "pct_error": 100.0 * (best_cost - opt) / opt,
        "time_s": data.get("time_s"),
        "file_json": p
    })

with open("results/eil101/ga_runs.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

print("Wrote results/eil101/ga_runs.csv with", len(rows), "rows; opt=", opt)
