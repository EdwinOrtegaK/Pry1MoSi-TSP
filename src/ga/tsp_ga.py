# src/ga/tsp_ga.py
from __future__ import annotations
import argparse, json, random, time
from pathlib import Path
from typing import Dict, Any, List
import numpy as np

from src.io.tsplib import read_tsplib
from src.common.metrics import tour_length
from src.io.seeded_rng import set_seeds
from .operators import ox, pmx, mutate_inversion, mutate_swap, tournament_select

def _make_initial_population(n: int, pop_size: int) -> List[List[int]]:
    base = list(range(n))
    return [random.sample(base, n) for _ in range(pop_size)]

def _crossover(name: str, p1: List[int], p2: List[int]) -> List[int]:
    if name.upper() == "PMX":
        return pmx(p1, p2)
    return ox(p1, p2)

def run_ga(coords, N: int, max_iter: int, crossover: str, pmut: float,
           elitism: float, seed: int, mut_kind: str = "invert",
           tournament_k: int = 3) -> Dict[str, Any]:
    """
    Devuelve:
      {
        "best": {"cost": float, "tour": list[int]},
        "top3": [{"cost": float, "tour": list[int]}, ...],
        "best_history": list[float],
        "time_s": float,
        "params": {...}
      }
    """
    set_seeds(seed)
    n = len(coords)
    elite_k = max(1, int(elitism * N))
    pop = _make_initial_population(n, N)
    fitness = [tour_length(ind, coords) for ind in pop]
    best_hist: List[float] = []
    t0 = time.time()

    for it in range(max_iter):
        # elitismo
        elite_idx = np.argsort(fitness)[:elite_k]
        elites = [pop[i][:] for i in elite_idx]

        # reproducción
        children: List[List[int]] = []
        while len(children) < N - elite_k:
            p1 = tournament_select(pop, fitness, k=tournament_k)
            p2 = tournament_select(pop, fitness, k=tournament_k)
            c = _crossover(crossover, p1, p2)
            if mut_kind == "swap":
                c = mutate_swap(c, p=pmut)
            else:
                c = mutate_inversion(c, p=pmut)
            children.append(c)

        pop = elites + children
        fitness = [tour_length(ind, coords) for ind in pop]
        best_hist.append(min(fitness))

        # pequeña adaptación si se estanca
        if it > 50 and min(best_hist[-50:]) >= best_hist[-51]:
            pmut = min(0.6, pmut * 1.1)

    dt = time.time() - t0
    order = np.argsort(fitness)
    top3 = [{"cost": float(fitness[i]), "tour": pop[i][:]} for i in order[:3]]
    result = {
        "best": top3[0],
        "top3": top3,
        "best_history": [float(v) for v in best_hist],
        "time_s": float(dt),
        "params": {
            "N": N, "maxIter": max_iter, "crossover": crossover,
            "pmut": pmut, "elitism": elitism, "seed": seed,
            "mut_kind": mut_kind, "tournament_k": tournament_k
        }
    }
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Ruta TSPLIB .tsp")
    ap.add_argument("--N", type=int, default=300)
    ap.add_argument("--maxIter", type=int, default=2000)
    ap.add_argument("--crossover", choices=["OX", "PMX"], default="OX")
    ap.add_argument("--pmut", type=float, default=0.2)
    ap.add_argument("--elitism", type=float, default=0.03)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--mut", choices=["invert","swap"], default="invert")
    ap.add_argument("--tournament_k", type=int, default=3)
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()

    coords = read_tsplib(args.data)
    res = run_ga(coords, args.N, args.maxIter, args.crossover, args.pmut,
                 args.elitism, args.seed, mut_kind=args.mut, tournament_k=args.tournament_k)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
