# src/common/metrics.py
from __future__ import annotations
import math
from typing import List, Tuple

Coords = List[Tuple[float, float]]
Tour = List[int]

def tour_length(order: Tour, coords: Coords) -> float:
    n = len(order)
    d = 0.0
    for i in range(n):
        a = order[i]
        b = order[(i + 1) % n]
        ax, ay = coords[a]
        bx, by = coords[b]
        d += math.hypot(ax - bx, ay - by)
    return d

def percent_error(value: float, optimum: float) -> float:
    if optimum <= 0:
        return float("nan")
    return (value - optimum) * 100.0 / optimum

def checksum(order: Tour) -> str:
    # hash simple para detectar duplicados de tours
    # (independiente del punto de inicio del ciclo)
    n = len(order)
    if n == 0:
        return "0"
    # normaliza rotando para que empiece en el menor índice
    k = order.index(min(order))
    norm = order[k:] + order[:k]
    return str(hash(tuple(norm)))
