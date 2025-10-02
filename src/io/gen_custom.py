"""
Módulo: gen_custom
-------------------
Generador de instancias TSP personalizadas (custom).
Produce un CSV con columnas: id,x,y
"""

import argparse
import csv
import math
import random
from typing import List, Tuple

import numpy as np

from .seeded_rng import set_seeds


def _generate_ring_clusters(n: int, seed: int) -> List[Tuple[float, float]]:
    """Genera puntos agrupados en clusters circulares."""
    rng = np.random.default_rng(seed)
    coords = []
    clusters = max(3, n // 20)  # número de clusters aproximado
    radius = 50
    for c in range(clusters):
        cx, cy = rng.uniform(0, 500), rng.uniform(0, 500)
        for _ in range(n // clusters):
            angle = rng.uniform(0, 2 * math.pi)
            r = rng.uniform(0, radius)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            coords.append((x, y))
    return coords[:n]


def generate_custom(n: int, seed: int, shape: str) -> List[Tuple[float, float]]:
    """
    Genera coordenadas según un patrón.

    Args:
        n (int): número de nodos
        seed (int): semilla para reproducibilidad
        shape (str): tipo de patrón (ring_clusters, islands, uniform)

    Returns:
        List[Tuple[float, float]]: coordenadas generadas
    """
    set_seeds(seed)
    if shape == "ring_clusters":
        return _generate_ring_clusters(n, seed)
    elif shape == "uniform":
        return [(random.uniform(0, 500), random.uniform(0, 500)) for _ in range(n)]
    elif shape == "islands":
        return [(random.gauss(250, 80), random.gauss(250, 80)) for _ in range(n)]
    else:
        raise ValueError(f"Forma no reconocida: {shape}")


def save_custom_csv(coords: List[Tuple[float, float]], out_path: str) -> None:
    """Guarda coordenadas en CSV con formato id,x,y."""
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "x", "y"])
        for i, (x, y) in enumerate(coords):
            writer.writerow([i, x, y])


def main():
    parser = argparse.ArgumentParser(description="Generador de instancias custom para TSP")
    parser.add_argument("--n", type=int, required=True, help="Número de nodos")
    parser.add_argument("--seed", type=int, required=True, help="Semilla para reproducibilidad")
    parser.add_argument("--shape", type=str, required=True, choices=["ring_clusters", "uniform", "islands"])
    parser.add_argument("--out", type=str, default="data/custom/mi_scenario.csv", help="Ruta del CSV de salida")
    args = parser.parse_args()

    coords = generate_custom(args.n, args.seed, args.shape)
    save_custom_csv(coords, args.out)
    print(f"Instancia custom guardada en {args.out} con {len(coords)} nodos.")


if __name__ == "__main__":
    main()
