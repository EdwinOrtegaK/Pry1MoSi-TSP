"""
Módulo: compare
----------------
Funciones para generar comparaciones y resúmenes de resultados GA vs LP.
"""

import csv
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt


def save_summary_csv(rows: List[Dict], out_csv: str) -> None:
    """
    Guarda un CSV con resumen de corridas GA.

    Args:
        rows (list[dict]): lista de diccionarios con resultados
        out_csv (str): ruta del archivo de salida
    """
    if not rows:
        raise ValueError("No hay filas para escribir en el summary.")

    # Usamos las llaves del primer dict como cabecera
    fieldnames = list(rows[0].keys())

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def save_side_by_side(
    coords: List[Tuple[float, float]],
    ga_order: List[int],
    lp_order: List[int],
    out_png: str,
) -> None:
    """
    Grafica lado a lado los tours de GA y LP/MTZ para comparación.

    Args:
        coords (list[(x,y)]): lista de coordenadas
        ga_order (list[int]): tour generado por GA
        lp_order (list[int]): tour generado por LP/MTZ
        out_png (str): ruta del archivo de salida
    """
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Tour GA
    xs_ga = [coords[i][0] for i in ga_order] + [coords[ga_order[0]][0]]
    ys_ga = [coords[i][1] for i in ga_order] + [coords[ga_order[0]][1]]
    axs[0].plot(xs_ga, ys_ga, "-o", markersize=3)
    axs[0].set_title("Tour GA")
    axs[0].set_xlabel("X")
    axs[0].set_ylabel("Y")

    # Tour LP
    xs_lp = [coords[i][0] for i in lp_order] + [coords[lp_order[0]][0]]
    ys_lp = [coords[i][1] for i in lp_order] + [coords[lp_order[0]][1]]
    axs[1].plot(xs_lp, ys_lp, "-o", markersize=3, color="orange")
    axs[1].set_title("Tour LP/MTZ")
    axs[1].set_xlabel("X")
    axs[1].set_ylabel("Y")

    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()


if __name__ == "__main__":
    # Ejemplo rápido
    coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
    ga_order = [0, 1, 2, 3]
    lp_order = [0, 3, 2, 1]
    save_side_by_side(coords, ga_order, lp_order, "compare_demo.png")

    rows = [
        {
            "instance": "demo",
            "seed": 42,
            "N": 100,
            "maxIter": 200,
            "crossover": "OX",
            "pmut": 0.2,
            "elitism": 0.05,
            "best_cost": 1234.5,
            "best_len": 4,
            "time_s": 1.23,
            "file_json": "results/demo/ga_seed42.json",
        }
    ]
    save_summary_csv(rows, "summary_demo.csv")
