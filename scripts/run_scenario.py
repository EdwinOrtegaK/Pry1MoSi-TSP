"""
Script: run_scenario.py
------------------------
Orquestador general: carga datos (TSPLIB o custom), ejecuta GA y MTZ, 
genera resultados en JSON, PNG y CSV.

Uso desde CLI:
--------------
# Caso TSPLIB
python scripts/run_scenario.py --name eil101 --seeds 42 1337 2025
python scripts/run_scenario.py --name gr229 --seeds 42 1337 2025

# Caso Custom
python scripts/run_scenario.py --name custom --custom_path data/custom/mi_scenario.csv --seeds 42 1337 2025
"""

import argparse
import json
import time
from pathlib import Path

import pandas as pd

from src.io.tsplib import read_tsplib
from src.io.seeded_rng import set_seeds
from src.ga.tsp_ga import run_ga
from src.lp.tsp_mtz_pulp import run_mtz
from src.viz.plot_tour import save_tour_png, save_convergence_png
from src.viz.compare import save_summary_csv


def load_data(name: str, custom_path: str = None):
    """Carga coordenadas desde TSPLIB o un CSV custom."""
    if name in ["eil101", "gr229"]:
        path = f"data/tsplib/{name}.tsp"
        return read_tsplib(path)
    elif name == "custom":
        if not custom_path:
            raise ValueError("Debe especificar --custom_path para escenario custom")
        import pandas as pd

        df = pd.read_csv(custom_path)
        return list(zip(df["x"], df["y"]))
    else:
        raise ValueError(f"Escenario no reconocido: {name}")


def main():
    parser = argparse.ArgumentParser(description="Orquestador de escenarios TSP (GA + MTZ)")
    parser.add_argument("--name", type=str, required=True, choices=["eil101", "gr229", "custom"])
    parser.add_argument("--seeds", type=int, nargs="+", required=True, help="Lista de semillas para correr GA")
    parser.add_argument("--custom_path", type=str, default=None, help="Ruta al CSV del escenario custom")
    parser.add_argument("--time_limit", type=int, default=600, help="Tiempo límite (seg) para MTZ")
    args = parser.parse_args()

    # === Preparar carpetas de salida ===
    results_dir = Path(f"results/{args.name}")
    results_dir.mkdir(parents=True, exist_ok=True)

    # === Cargar datos ===
    coords = load_data(args.name, args.custom_path)

    summary_rows = []

    # === Ejecutar GA para cada semilla ===
    for seed in args.seeds:
        set_seeds(seed)
        print(f"[INFO] Corriendo GA para {args.name} con semilla {seed}...")

        start = time.time()
        result = run_ga(
            coords,
            N=100,
            max_iter=300,
            crossover="OX",
            pmut=0.2,
            elitism=0.03,
            seed=seed,
        )
        elapsed = time.time() - start
        result["time_s"] = elapsed

        # Guardar JSON
        out_json = results_dir / f"ga_seed{seed}.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        # Graficar tour y convergencia
        save_tour_png(coords, result["best"]["tour"], results_dir / f"{args.name}_tour_GA_seed{seed}.png")
        save_convergence_png(result["best_history"], results_dir / f"{args.name}_convergence_seed{seed}.png")

        # Agregar fila al resumen
        summary_rows.append(
            {
                "instance": args.name,
                "seed": seed,
                "N": result["params"]["N"],
                "maxIter": result["params"].get("max_iter", result["params"].get("maxIter")),
                "crossover": result["params"]["crossover"],
                "pmut": result["params"]["pmut"],
                "elitism": result["params"]["elitism"],
                "best_cost": result["best"]["cost"],
                "best_len": len(coords),
                "time_s": result["time_s"],
                "file_json": str(out_json),
            }
        )

    # === Ejecutar MTZ (solo si no es demasiado grande) ===
    if args.name in ["eil101", "gr229", "custom"]:
        try:
            print(f"[INFO] Corriendo MTZ para {args.name}...")
            mtz_result = run_mtz(coords, time_limit=args.time_limit)

            out_json = results_dir / "mtz_opt.json"
            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(mtz_result, f, indent=2)

            if mtz_result.get("tour"):
                save_tour_png(coords, mtz_result["tour"], results_dir / f"{args.name}_tour_OPT.png")

        except Exception as e:
            print(f"[WARN] MTZ falló: {e}")

    # === Guardar resumen CSV ===
    out_csv = results_dir / "summary.csv"
    save_summary_csv(summary_rows, out_csv)
    print(f"[INFO] Resumen guardado en {out_csv}")


if __name__ == "__main__":
    main()
