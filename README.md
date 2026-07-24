# ☀️ Solar Energy Monitoring System

A backend system for ingesting, storing, and analyzing solar power generation
data. Raw CSV readings are cleaned and aggregated into daily energy totals,
stored in SQLite, exposed through a FastAPI REST API, flagged for anomalies,
and visualized on an interactive Streamlit dashboard.

## Features

- **Data pipeline** – loads raw generation CSVs, cleans and aggregates them into daily energy totals
- **REST API** (FastAPI) – serves daily energy, aggregated metrics, and anomaly data as JSON
- **Anomaly detection** – pluggable threshold-based and z-score detectors
- **Interactive dashboard** (Streamlit) – date filtering, KPI cards, trend chart, anomaly table
- **Automated tests** (pytest) run in CI on every push
- **Containerized** with Docker Compose (API + dashboard)

## Architecture

```
Raw CSV data
     │
     ▼
Data cleaning & daily aggregation (pandas)
     │
     ▼
SQLite database
     │
     ▼
Repository layer  →  Service layer (anomaly detection, metrics)
     │
     ▼
FastAPI REST API
     │
     ▼
Streamlit dashboard
```

## Tech Stack

| Layer            | Technology                     |
|-------------------|--------------------------------|
| Data processing   | Python, pandas                 |
| Database          | SQLite                         |
| API               | FastAPI, Pydantic, Uvicorn     |
| Dashboard         | Streamlit, Plotly, requests    |
| Testing           | pytest, `fastapi.testclient`   |
| Code quality      | Ruff, Black                    |
| CI/CD             | GitHub Actions                 |
| Containerization  | Docker, Docker Compose         |

## Project Structure

```
Solar-Energy-Monitoring-System/
├── backend/
│   ├── api/            # FastAPI routes
│   ├── services/       # Business logic (metrics, anomaly orchestration)
│   ├── repositories/    # Data access layer (SQLite queries)
│   ├── anomaly/         # Anomaly detection strategies (threshold, z-score)
│   ├── models/          # Pydantic schemas
│   ├── core/            # Config & logging
│   └── main.py          # FastAPI app entrypoint
├── dasboard/
│   └── app.py           # Streamlit dashboard
├── scripts/
│   └── populate_db.py   # ETL: CSV -> SQLite
├── src/                  # Original analysis scripts (cleaning, viz, metrics)
├── data/raw/             # Raw generation & weather CSVs
├── test/                 # Pytest test suite
├── output/               # Generated charts
├── Dockerfile             # API container
├── Dockerfile.dashboard   # Dashboard container
├── docker-compose.yml
└── requirements.txt
```

## Getting Started

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Populate the database

Loads `data/raw/Plant_1_Generation_Data.csv`, aggregates it daily, and writes
to `backend/energy.db`.

```bash
python scripts/populate_db.py
```

### 4. Run the API

```bash
python -m uvicorn backend.main:app --reload --port 8002
```

API docs: http://127.0.0.1:8002/docs

### 5. Run the dashboard

```bash
streamlit run dasboard/app.py
```

Dashboard: http://localhost:8501

## Running with Docker

```bash
docker compose up --build
```

- API docs: http://localhost:8002/docs
- Dashboard: http://localhost:8501

## API Reference

| Method | Endpoint            | Description                                   |
|--------|---------------------|------------------------------------------------|
| GET    | `/health`           | Service health check                          |
| GET    | `/energy/daily`     | Daily energy totals (optional `start`/`end`)  |
| GET    | `/energy/metrics`   | Aggregated statistics (avg, min, max, total)  |
| GET    | `/energy/anomalies` | Anomalous days (`method=threshold\|zscore`)   |

**`GET /energy/daily`**

```json
[
  {
    "day": "2020-05-15",
    "energy": 5627239.14,
    "is_anomaly": false
  }
]
```

**`GET /energy/metrics`**

```json
{
  "day": 34,
  "avg_energy": 5678123.45,
  "min_energy": 5208696.38,
  "max_energy": 7898965.11,
  "total_energy": 192345678.23,
  "anomaly_days": 2,
  "anomaly_pct": 5.88
}
```

## Configuration

Settings are read from environment variables (see `backend/core/config.py`),
with sensible defaults:

| Variable    | Default              | Description            |
|-------------|----------------------|-------------------------|
| `API_HOST`  | `127.0.0.1`           | API bind host           |
| `API_PORT`  | `8002`                | API bind port           |
| `DB_PATH`   | `backend/energy.db`   | SQLite database path    |
| `LOG_LEVEL` | `INFO`                | Logging verbosity       |

## Testing

```bash
pytest
```

Tests cover the API endpoints and anomaly detection logic.

## Continuous Integration

GitHub Actions runs on every push/PR: installs dependencies and runs the
`pytest` suite (see `.github/workflows/ci.yml`).

## Roadmap

- [ ] Deploy to the cloud (Render/Railway)
- [ ] Add authentication
- [ ] Rolling averages & forecasting
- [ ] Additional anomaly detection methods
