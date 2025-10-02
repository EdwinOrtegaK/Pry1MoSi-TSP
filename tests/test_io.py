"""
Tests para el módulo IO (tsplib y gen_custom).
Se ejecutan con pytest.
"""

import os
import pandas as pd

from src.io.tsplib import read_tsplib
from src.io.gen_custom import generate_custom, save_custom_csv


def test_read_tsplib_eil101():
    """Prueba que el parser de TSPLIB lea bien eil101.tsp."""
    coords = read_tsplib("data/tsplib/eil101.tsp")
    # Verifica que sea lista no vacía
    assert isinstance(coords, list)
    assert len(coords) > 0
    # Cada coordenada debe ser par (x,y)
    x, y = coords[0]
    assert isinstance(x, float) and isinstance(y, float)


def test_generate_custom_and_save(tmp_path):
    """Prueba que el generador custom cree un CSV válido."""
    n = 60
    seed = 2025
    shape = "ring_clusters"

    coords = generate_custom(n, seed, shape)
    assert len(coords) == n

    # Guardar a CSV temporal
    out_csv = tmp_path / "custom_test.csv"
    save_custom_csv(coords, out_csv)

    # Verificar que se creó el archivo
    assert out_csv.exists()

    # Leer con pandas y verificar columnas
    df = pd.read_csv(out_csv)
    assert list(df.columns) == ["id", "x", "y"]
    assert len(df) == n
    # IDs deben ser únicos y consecutivos
    assert df["id"].is_unique
    assert df["id"].iloc[0] == 0
    assert df["id"].iloc[-1] == n - 1
