## vrp-optimization-jcci

An Vehicle Routing Problem (VRP) solver built with Google OR-Tools to optimize JCCI(Jain Carrying Corporation India) fleet logistics. It implements a Python-based operations research pipeline that handles vehicle capacity constraints, minimizes transit costs, and generates interactive route maps and executive performance reports.


## 📂 Project Structure

```text
vrp-optimization-jcci/
├── data/                      # Input files (Read-Only)
│   ├── raw_demands.csv        # Customer locations and order volumes
│   └── fleet_capacity.json    # Vehicle capacities and shift rules
├── notebooks/                 # Prototyping & Analysis
│   ├── 1.0_eda_locations.ipynb# Data validation and location plotting
│   └── 2.0_ortools_prototype.ipynb # OR-Tools constraint testing
├── src/                       # Production Engine (Importable scripts)
│   ├── __init__.py            # Package initialization
│   ├── data_loader.py         # Transforms CSV/JSON into OR-Tools data models
│   ├── distance_matrix.py     # Calculates distance/time matrices
│   ├── vrp_solver.py          # Core OR-Tools optimization engine
│   └── utils.py               # Auxiliary helpers
├── outputs/                   # Generated Machine Data
│   ├── dispatch_schedules/    # CSV/Excel sheets for drivers
│   └── route_maps/            # Interactive Folium HTML maps
├── reports/                   # Human-Readable Insights
│   └── final_conclusion.pdf   # Executive summary and operational KPIs
├── config.yaml                # Solver parameters and time limits
├── requirements.txt           # Python application dependencies
└── README.md                  # Project documentation
```


## 🧭 Repository Navigation Guide

* **`data/`**: Serves as the single source of truth for raw operational inputs. It is treated as immutable to preserve data integrity.
* **`notebooks/`**: Retains the iterative development history. Use `1.0` to audit coordinates and `2.0` to isolate and debug solver hyper-parameters line-by-line.
* **`src/`**: Houses the modular, reusable production pipeline. Decoupling the data engineering (`data_loader.py`) from the optimization logic (`vrp_solver.py`) allows for scalable solver upgrades without modifying data workflows.
* **`outputs/`**: Captures dynamic runtime data. Every execution updates the schedules and generates visual geographic routing paths.
* **`reports/`**: Holds static corporate deliverables, anchoring the technical mathematical results to direct business outcomes.


## Let's Start

### 1. Clone the Repository
```bash
git clone https://github.com
cd vrp-optimization-jcci
```

### 2. Set Up Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Solver Pipeline
```bash
python src/vrp_solver.py
```