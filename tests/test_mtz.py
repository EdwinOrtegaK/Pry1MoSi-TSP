# tests/test_mtz.py
from __future__ import annotations
import math
from typing import List, Tuple

from src.lp.tsp_mtz_pulp import run_mtz
from src.common.metrics import tour_length

Coords = List[Tuple[float, float]]

def _tiny_square_plus() -> Coords:
    # Un cuadrado unitario + un punto arriba: solución trivial, óptimo rápido.
    return [
        (0.0, 0.0),  # 0
        (1.0, 0.0),  # 1
        (1.0, 1.0),  # 2
        (0.0, 1.0),  # 3
        (0.5, 1.8),  # 4
    ]

def test_mtz_tiny_instance_optimal():
    coords = _tiny_square_plus()
    res = run_mtz(coords, time_limit=30)

    assert res["status"] in {"Optimal", "Not Solved", "TimeLimit", "Infeasible", "Unbounded"}
    # En general debería ser Optimal en 5 nodos
    assert res["status"] == "Optimal"

    tour = res["tour"]
    assert tour is not None, "No se pudo reconstruir el tour"
    n = len(coords)
    assert len(tour) == n, "El tour no visita todos los nodos exactamente una vez"
    assert len(set(tour)) == n, "El tour tiene nodos repetidos"

    # Validar longitud > 0 y consistente
    L = tour_length(tour, coords)
    assert L > 0.0 and math.isfinite(L), "Longitud de tour inválida"

    # La solución debe cerrar ciclo: esto ya se garantiza en tour_length (usa (i+1)%n)
