"""
Módulo: plot_tour
------------------
Funciones para visualizar tours y curvas de convergencia del TSP.
"""

import matplotlib.pyplot as plt
from typing import List, Tuple


def save_tour_png(coords: List[Tuple[float, float]], order: List[int], out_path: str) -> None:
    """
    Guarda un gráfico PNG del tour.

    Args:
        coords (list[(x,y)]): lista de coordenadas
        order (list[int]): orden de visita (tour, ciclo implícito)
        out_path (str): ruta del archivo de salida
    """
    xs = [coords[i][0] for i in order] + [coords[order[0]][0]]
    ys = [coords[i][1] for i in order] + [coords[order[0]][1]]

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, "-o", markersize=4, linewidth=1.2)
    plt.title("Tour TSP")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def save_convergence_png(history: List[float], out_path: str) -> None:
    """
    Guarda la curva de convergencia (mejor costo vs iteración).

    Args:
        history (list[float]): lista de valores del mejor costo por iteración
        out_path (str): ruta del archivo de salida
    """
    plt.figure(figsize=(6, 4))
    plt.plot(history, label="Mejor costo", linewidth=1.2)
    plt.xlabel("Iteración")
    plt.ylabel("Costo")
    plt.title("Convergencia del GA")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


if __name__ == "__main__":
    # Ejemplo rápido
    coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
    order = [0, 1, 2, 3]
    save_tour_png(coords, order, "tour_demo.png")
    save_convergence_png([10, 8, 7, 6, 5], "convergence_demo.png")
