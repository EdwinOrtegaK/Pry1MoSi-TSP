"""
Módulo: tsplib
---------------
Funciones para leer instancias de TSP en formato TSPLIB (EUC_2D).
Devuelve una lista de coordenadas en el orden correcto (índices 0..n-1).
"""

from typing import List, Tuple


def read_tsplib(path: str) -> List[Tuple[float, float]]:
    """
    Lee un archivo TSPLIB (.tsp) y devuelve una lista de coordenadas.

    Args:
        path (str): Ruta al archivo .tsp

    Returns:
        List[Tuple[float, float]]: Lista de pares (x, y) para cada nodo
                                   con índices 0..n-1
    """
    coords = []
    with open(path, "r", encoding="utf-8") as f:
        in_node_section = False
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("NODE_COORD_SECTION"):
                in_node_section = True
                continue
            if line.startswith("EOF"):
                break
            if in_node_section:
                parts = line.split()
                if len(parts) >= 3:
                    _, x, y = parts[:3]
                    coords.append((float(x), float(y)))
    return coords


if __name__ == "__main__":
    # Ejemplo de uso rápido
    path = "data/tsplib/eil101.tsp"
    coords = read_tsplib(path)
    print(f"Leídas {len(coords)} ciudades desde {path}")
