# src/lp/tsp_mtz_pulp.py
from __future__ import annotations
import argparse
import json
import math
import os
import time
from typing import List, Tuple, Optional

import pulp

from src.common.metrics import tour_length

Coords = List[Tuple[float, float]]

def _euclid_dmatrix(coords: Coords) -> List[List[float]]:
    n = len(coords)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = coords[i]
        for j in range(i + 1, n):
            xj, yj = coords[j]
            dij = math.hypot(xi - xj, yi - yj)
            D[i][j] = D[j][i] = dij
    return D

def _extract_tour_from_x(x_vars, n: int) -> Optional[List[int]]:
    """
    Reconstruye el tour siguiendo sucesores desde 0.
    x_vars es un dict {(i, j): var} con valores 0/1.
    Devuelve una permutación 0..n-1 que define ciclo Hamiltoniano,
    o None si no se puede reconstruir un único ciclo de longitud n.
    """
    succ = {i: None for i in range(n)}
    for (i, j), var in x_vars.items():
        v = var.value()
        if v is None:
            continue
        if v > 0.5:
            if succ[i] is not None:
                # más de un sucesor: solución degenerada
                return None
            succ[i] = j

    # Debe haber exactamente un sucesor por nodo
    if any(succ[i] is None for i in range(n)):
        return None

    # Seguir desde 0 y verificar ciclo único de longitud n
    tour = [0]
    visited = {0}
    cur = 0
    for _ in range(n - 1):
        nxt = succ[cur]
        if nxt is None or nxt in visited:
            return None
        tour.append(nxt)
        visited.add(nxt)
        cur = nxt

    # Cerrar ciclo
    if succ[cur] != tour[0]:
        return None

    return tour

def run_mtz(coords: Coords, time_limit: Optional[int] = None) -> dict:
    """
    Resuelve TSP con modelo MTZ clásico en PuLP (CBC).
    Retorna diccionario serializable a JSON con status, objective, tour, etc.
    """
    n = len(coords)
    if n < 3:
        raise ValueError(f"Instancia inválida: se leyeron {n} nodos. "
                            "Verifica el archivo TSPLIB y el parser.")
    D = _euclid_dmatrix(coords)

    # Modelo
    prob = pulp.LpProblem("TSP_MTZ", pulp.LpMinimize)

    # Variables binarias x[i,j], i != j
    x = pulp.LpVariable.dicts("x", (range(n), range(n)), lowBound=0, upBound=1, cat=pulp.LpBinary)
    # Variables MTZ u[i] (orden de visita). Convención estándar: u[0] libre en [0, n-1] o fijo 0
    u = pulp.LpVariable.dicts("u", range(n), lowBound=0, upBound=n - 1, cat=pulp.LpContinuous)

    # Objetivo: minimizar sum d[i][j] * x[i][j]
    prob += pulp.lpSum(D[i][j] * x[i][j] for i in range(n) for j in range(n) if i != j)

    # Grado: sale uno de cada nodo, entra uno a cada nodo
    for i in range(n):
        prob += pulp.lpSum(x[i][j] for j in range(n) if j != i) == 1, f"out_{i}"
        prob += pulp.lpSum(x[j][i] for j in range(n) if j != i) == 1, f"in_{i}"

    # MTZ anti-subtours (para i,j >= 1); fijamos u[0] = 0 para anclar
    prob += u[0] == 0, "anchor_u0"
    for i in range(1, n):
        for j in range(1, n):
            if i == j:
                continue
            # u_i - u_j + n * x_ij <= n - 1
            prob += u[i] - u[j] + n * x[i][j] <= n - 1, f"mtz_{i}_{j}"

    # Resolver con CBC
    solver = pulp.PULP_CBC_CMD(
        msg=False,  # pon True si quieres ver el log
        timeLimit=int(time_limit) if time_limit else None,
    )

    t0 = time.perf_counter()
    status_code = prob.solve(solver)
    elapsed = time.perf_counter() - t0

    status = pulp.LpStatus[status_code]

    # Extraer solución (si hay incumbente)
    tour = None
    objective = None
    try:
        objective = float(pulp.value(prob.objective))
    except Exception:
        objective = None

    # Diccionario (i,j)-> var para extraer tour
    x_vars = {(i, j): x[i][j] for i in range(n) for j in range(n) if i != j}
    tour = _extract_tour_from_x(x_vars, n)

    # CBC vía PuLP no expone best bound fácilmente; lo dejamos None si no está disponible
    best_bound = None

    result = {
        "instance": None,        # lo llena la CLI (nombre del archivo)
        "solver": "CBC",
        "status": status,
        "best_bound": best_bound,
        "objective": objective,
        "time_s": elapsed,
        "tour": tour,
    }
    return result

def _infer_instance_name(path: str) -> str:
    base = os.path.basename(path)
    name, _ = os.path.splitext(base)
    return name

def main():
    ap = argparse.ArgumentParser(description="TSP ILP (MTZ) con PuLP/CBC")
    ap.add_argument("--data", required=True, help="Ruta a archivo TSPLIB .tsp (EUC_2D)")
    ap.add_argument("--time_limit", type=int, default=None, help="Límite de tiempo en segundos (opcional)")
    ap.add_argument("--out", required=True, help="Ruta de salida JSON")
    args = ap.parse_args()


    from src.io.tsplib import read_tsplib

    coords = read_tsplib(args.data)
    res = run_mtz(coords, time_limit=args.time_limit)
    res["instance"] = _infer_instance_name(args.data)

    # Si no hay tour pero sí objective, renombra mentalmente como 'mtz_bound'
    # La ruta de salida la decide el usuario; aquí siempre escribimos al --out dado.
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)

    # Mensaje corto en consola
    print(f"[MTZ] instance={res['instance']} status={res['status']} "
          f"obj={res['objective']} time_s={res['time_s']:.2f} out={args.out}")

if __name__ == "__main__":
    main()
