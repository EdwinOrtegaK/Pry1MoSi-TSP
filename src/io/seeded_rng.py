"""
Módulo: seeded_rng
-------------------
Maneja la fijación de semillas para reproducibilidad.
"""

import random
import numpy as np


def set_seeds(seed: int) -> None:
    """
    Fija las semillas de random y numpy para reproducibilidad.

    Args:
        seed (int): semilla
    """
    random.seed(seed)
    np.random.seed(seed)


if __name__ == "__main__":
    set_seeds(42)
    print("Semillas fijadas con 42")
    print("Random:", random.randint(0, 100))
    print("Numpy :", np.random.randint(0, 100))
