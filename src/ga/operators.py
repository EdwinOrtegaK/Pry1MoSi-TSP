# src/ga/operators.py
from __future__ import annotations
import random
from typing import List

Tour = List[int]

def ox(parent1: Tour, parent2: Tour) -> Tour:
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[a:b+1] = parent1[a:b+1]
    fill = [g for g in parent2 if g not in child]
    j = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[j]; j += 1
    return child  # type: ignore

def pmx(parent1: Tour, parent2: Tour) -> Tour:
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n

    # Copiar segmento de parent1
    child[a:b+1] = parent1[a:b+1]

    # Para cada gen en el segmento de parent2, mapear si no está ya en el hijo
    for i in range(a, b+1):
        if parent2[i] not in child:
            pos = i
            val = parent2[i]
            # Seguir el ciclo de mapeo hasta encontrar hueco
            while True:
                pos = parent1.index(val)
                if child[pos] is None:
                    child[pos] = parent2[i]
                    break
                val = parent2[pos]

    # Rellenar los huecos restantes con genes de parent2
    for i in range(n):
        if child[i] is None:
            child[i] = parent2[i]

    return child  # type: ignore




def mutate_inversion(order: Tour, p: float = 0.2) -> Tour:
    if random.random() > p:
        return order[:]
    i, j = sorted(random.sample(range(len(order)), 2))
    return order[:i] + list(reversed(order[i:j+1])) + order[j+1:]

def mutate_swap(order: Tour, p: float = 0.1) -> Tour:
    if random.random() > p:
        return order[:]
    i, j = random.sample(range(len(order)), 2)
    out = order[:]
    out[i], out[j] = out[j], out[i]
    return out

def tournament_select(pop: List[Tour], fitness: List[float], k: int = 3) -> Tour:
    idx = random.sample(range(len(pop)), k)
    best = min(idx, key=lambda i: fitness[i])
    return pop[best][:]
