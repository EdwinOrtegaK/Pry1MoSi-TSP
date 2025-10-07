# Proyecto: GA + LP (MTZ) para TSP

Este repositorio implementa y compara **Algoritmos Genéticos (GA)** y un modelo **Lineal Entero (MTZ con CBC/PuLP)** para resolver el **Traveling Salesman Problem (TSP)** en 3 escenarios:
- **Caso A:** `eil101` (TSPLIB)  
- **Caso B:** `gr229` (TSPLIB)  
- **Caso C:** `custom` (dataset CSV propio)

Incluye scripts para ejecutar experimentos, calcular resúmenes (% error vs óptimo/LP) y generar figuras (convergencia y tours).

## Tabla de contenido
- [Estructura del repo](#estructura-del-repo)
- [Requisitos y entorno](#requisitos-y-entorno)
- [Cómo correr *tests*](#cómo-correr-tests)
- [Cómo correr cada caso (paso a paso)](#cómo-correr-cada-caso-paso-a-paso)
  - [Caso A – `eil101` (TSPLIB)](#caso-a--eil101-tsplib)
  - [Caso B – `gr229` (TSPLIB)](#caso-b--gr229-tsplib)
  - [Caso C – `custom` (CSV propio)](#caso-c--custom-csv-propio)
- [Orquestador: todo en un comando](#orquestador-todo-en-un-comando)
- [Figuras (convergencia y tour)](#figuras-convergencia-y-tour)
- [Buenas prácticas y *gotchas*](#buenas-prácticas-y-gotchas)
- [Créditos](#créditos)

## Estructura del repo

```
Proyecto-GA-LP-TSP/
├─ data/
│  ├─ tsplib/
│  │  ├─ eil101.tsp
│  │  └─ gr229.tsp
│  └─ custom/
│     ├─ mi_scenario.csv
│     ├─ test5.csv
│     └─ test30.csv
├─ src/
│  ├─ ga/
│  │  ├─ tsp_ga.py           # main GA (CLI)
│  │  └─ operators.py        # OX, PMX, mutaciones, selección
│  ├─ lp/
│  │  └─ tsp_mtz_pulp.py     # modelo MTZ con PuLP/CBC (TSPLIB y CSV)
│  ├─ io/
│  │  ├─ tsplib.py           # parser TSPLIB EUC_2D
│  │  └─ gen_custom.py       # utilidades para datasets propios
│  ├─ viz/
│  │  ├─ plot_tour.py        # helpers para graficar tours y convergencia
│  │  └─ compare.py          # comparaciones GA vs LP (si aplica)
│  └─ common/
│     └─ metrics.py          # distancia euclídea y métricas
├─ scripts/
│  ├─ run_scenario.py        # orquestador (GA + MTZ + figuras + summary)
│  ├─ make_summary_eil101.py # resume GA vs MTZ (eil101)
│  └─ (opcional) plot_*.py   # scripts de plots (si el equipo los añade)
├─ tests/
│  ├─ test_ga.py
│  ├─ test_io.py
│  └─ conftest.py
├─ results/
│  ├─ eil101/
│  ├─ gr229/
│  └─ custom/
├─ requirements.txt
└─ README.md
```

## Instalación

1. Clona el repositorio:

```bash
git clone <url del repo>
cd Pry1MoSi-TSP
```

2. Crear y activar un entorno virtual:

```bash
python -m venv .venv

# Para Linux/macOS
source .venv/bin/activate

# Para Windows (PowerShell)
.venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt

# Verificar que CBC esté disponible:
python -c "from pulp import listSolvers; print(listSolvers(onlyAvailable=True))"
# Debe listar: ['PULP_CBC_CMD']
```

> **PowerShell (Windows)** — usa el *backtick* `` ` `` para saltos de línea. **No** uses `>>` (eso es redirección a archivo).

## Cómo correr *tests*

```powershell
# desde la raíz del repo
pytest -q tests/test_io.py
pytest -q tests/test_ga.py

# (opcional) excluir tests lentos marcados como 'slow'
# pytest -q -m "not slow"
```

## Cómo correr cada caso

### Caso A – `eil101` (TSPLIB)

**1) GA con 3 semillas** (genera JSON por corrida)
```powershell
python -m src.ga.tsp_ga `
  --data data/tsplib/eil101.tsp `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 42 `
  --out results/eil101/ga_seed42.json

python -m src.ga.tsp_ga `
  --data data/tsplib/eil101.tsp `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 1337 `
  --out results/eil101/ga_seed1337.json

python -m src.ga.tsp_ga `
  --data data/tsplib/eil101.tsp `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 2025 `
  --out results/eil101/ga_seed2025.json
```

**2) LP/MTZ (óptimo/cota con límite de tiempo)**  
> MTZ soporta **TSPLIB** y **CSV** (ver Caso C).

```powershell
python -m src.lp.tsp_mtz_pulp `
  --data data/tsplib/eil101.tsp `
  --time_limit 120 `
  --out results/eil101/mtz_opt.json
```

**3) Resumen (% error GA vs MTZ)**
```powershell
python scripts\make_summary_eil101.py
# -> results/eil101/ga_runs.csv
```

### Caso B – `gr229` (TSPLIB)

Mismos comandos cambiando el dataset y la carpeta de salida:

**1) GA con 3 semillas** (genera JSON por corrida)
```powershell
python -m src.ga.tsp_ga `
  --data data/tsplib/gr229.tsp `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 42 `
  --out results/gr229/ga_seed42.json

python -m src.ga.tsp_ga `
  --data data/tsplib/gr229.tsp `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 1337 `
  --out results/gr229/ga_seed1337.json

python -m src.ga.tsp_ga `
  --data data/tsplib/gr229.tsp `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 2025 `
  --out results/gr229/ga_seed2025.json
```

**2) LP/MTZ (óptimo/cota con límite de tiempo)**  
> MTZ soporta **TSPLIB** y **CSV** (ver Caso C).

```powershell
python -m src.lp.tsp_mtz_pulp `
  --data data/tsplib/gr229.tsp `
  --time_limit 600 `
  --out results/gr229/mtz_opt.json
```
> **Nota:** `gr229` es más grande; puedes necesitar mayor `time_limit` y/o reducir `N`/`maxIter` si no buscas resultados finales.

**3) Resumen (% error GA vs MTZ)**
```powershell
python scripts\make_summary_gr229.py
# -> results/gr229/ga_runs.csv
```

### Caso C – `custom` (CSV propio)

**Formato CSV esperado:** encabezado con columnas `id,x,y` en cualquier orden.  
Ejemplo:
```
id,x,y
0,10.0,5.0
1,13.5,9.2
...
```

**1) GA con 3 semillas (sobre CSV)**
```powershell
python -m src.ga.tsp_ga `
  --data data/custom/mi_scenario.csv `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 42 `
  --out results/custom/ga_seed42.json

python -m src.ga.tsp_ga `
  --data data/custom/mi_scenario.csv `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 1337 `
  --out results/custom/ga_seed1337.json

python -m src.ga.tsp_ga `
  --data data/custom/mi_scenario.csv `
  --N 300 --maxIter 2000 `
  --crossover OX --pmut 0.2 --elitism 0.03 `
  --seed 2025 `
  --out results/custom/ga_seed2025.json
```

**2) LP/MTZ sobre CSV** (soportado por `tsp_mtz_pulp.py`)
```powershell
python -m src.lp.tsp_mtz_pulp `
  --data data/custom/mi_scenario.csv `
  --time_limit 300 `
  --out results/custom/mtz_opt.json
```

**3) Resumen**  
Crea un script `scripts/make_summary_custom.py` análogo al de `eil101` para consolidar `% error`.
```powershell
python scripts\make_summary_custom.py
# -> results/custom/ga_runs.csv
```

## Orquestador:

`run_scenario.py` ejecuta **GA multi-semilla + MTZ + (figuras y summary si están soportados)**.
> PowerShell: usa el backtick ` para saltos de línea (no >>).

### Caso A — `eil101` (TSPLIB)
```powershell
python -m scripts.run_scenario `
  --name eil101 `
  --seeds 42 1337 2025 `
  --time_limit 120
```

### Caso B — `gr229` (TSPLIB)
```powershell
python -m scripts.run_scenario `
  --name gr229 `
  --seeds 42 1337 2025 `
  --time_limit 600
```
> Nota: gr229 es más grande. Si tu máquina sufre, sube --time_limit o luego corre GA/MTZ por separado.

### Caso C — `custom` (CSV propio)
Si tu run_scenario.py soporta el nombre custom (o equivalente en tu script):
```powershell
python -m scripts.run_scenario `
  --name custom `
  --seeds 42 1337 2025 `
  --time_limit 300
```
> Si tu versión de run_scenario.py no mapea --name custom a data/custom/mi_scenario.csv, corre GA y MTZ manualmente (como ya tienes en el README) o ajusta el script para aceptar --data explícito.

Parámetros típicos:
- `--name eil101|gr229|custom_name`
- `--seeds ...` lista de semillas
- `--time_limit N` segundos para MTZ  
> Si parece “congelado” en MTZ, es normal que no veas logs desde el orquestador. Corre MTZ **aparte** para ver progreso o asegúrate de que `tsp_mtz_pulp.py` use `PULP_CBC_CMD(msg=True, timeLimit=..., maxSeconds=...)`.

Esto:
- Corre GA con todas las semillas
- Corre MTZ
- Guarda resumen `summary.csv`
- Genera gráficas de convergencia y tours automáticamente en `results/eil101/`


## Figuras (convergencia y tour)

Dependiendo de la versión del orquestador, las figuras pueden generarse automáticamente. Si no, puedes usar:

- **Helpers en** `src/viz/plot_tour.py` (por ejemplo `save_tour_png(coords, tour, out_png)` y `save_convergence_png(history, out_png)`).
- O crear scripts simples en `scripts/plot_*.py` que lean los JSON del GA y guarden PNG en `results/<caso>/`.

*Ejemplo (pseudo):*
```python
# scripts/plot_tour_from_ga.py
from src.io.tsplib import read_tsplib
from src.viz.plot_tour import save_tour_png, save_convergence_png
# ... leer results/<caso>/ga_seed*.json y graficar tour + history
```


## Buenas prácticas y *gotchas*
- **Ejecuta desde la raíz** del repo. Usa `python -m paquete.modulo` (evita `python archivo.py` con rutas relativas).
- **PowerShell:** usa salto de línea con **backtick** `` ` ``. **No uses `>>`** (eso redirige a archivo).
- **Paquete `src/` accesible:** ya existen `__init__.py` para tratar carpetas como paquetes. Si ejecutas scripts sueltos fuera de la raíz, podrías necesitar un “path fix”.
- **CBC disponible:** `pip install coin-or-cbc` y verifica con `listSolvers`.
- **Parámetros GA:** para “smoke tests” usa `N=120, maxIter=400`. Para reporte final, `N=300–400, maxIter=2000–2500`.
- **CSV custom:** `tsp_mtz_pulp.py` soporta `.csv` (lee `id,x,y`). Para GA también puedes usar `.csv` vía `--data`.


## Créditos
- Equipo: experimentos y análisis para `eil101`, `gr229`, y `custom`.
- Implementación GA + MTZ + utilidades de IO/visualización desarrolladas en conjunto para el curso de **Modelación y Simulación**.

