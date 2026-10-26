# PureCast Backend

> **Filter-health forecasting platform for water purifiers** — atomQUEST 2026, Track 2

PureCast is a "weather forecast for water-purifier filters". It ingests sensor telemetry from ESP32-C3 edge nodes via MQTT, computes per-consumable Health Index (0–100%), forecasts remaining filter life with confidence bands, diagnoses failure modes, and enables one-tap cartridge reorder.

## 5-Minute Quickstart

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose v2
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.12+

### 1. Clone and install

```bash
git clone <repo-url> && cd purecast-backend
cp .env.example .env
make install
```

### 2. Start the stack

```bash
make up          # PostgreSQL + TimescaleDB, Redis, Mosquitto, Grafana, Prometheus
make db-upgrade  # Run migrations
```

### 3. Run the API

```bash
make api         # http://localhost:8000/docs
```

### 4. Run the demo

```bash
make demo        # Full demo with simulated purifier scenarios
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│  ESP32-C3   │────▶│  Mosquitto   │────▶│  MQTT Ingestor   │
│  (Sensors)  │     │  (MQTT TLS)  │     │  (aiomqtt)       │
└─────────────┘     └──────────────┘     └────────┬─────────┘
                                                   │
                    ┌──────────────┐     ┌─────────▼─────────┐
                    │  FastAPI     │◀───▶│  ARQ Workers       │
                    │  (REST + WS) │     │  (Forecast/Train)  │
                    └──────┬───────┘     └─────────┬─────────┘
                           │                       │
                    ┌──────▼───────────────────────▼─────────┐
                    │  PostgreSQL + TimescaleDB               │
                    │  Redis (cache, queue, rate-limit)       │
                    └────────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for the full system design.

## Project Structure

```
src/purecast/
├── core/          # Config, logging, security, errors, telemetry
├── domain/        # Pure Python domain logic (zero framework imports)
│   ├── signal/    # Median filter, sanity checks, temp correction
│   ├── health/    # Health index, EOL lines, mode-aware ageing
│   ├── prognostics/  # Kalman filter, remaining-life estimator
│   └── diagnosis/ # Rule engine, hysteresis, event tagging
├── application/   # Use cases, DTOs, port interfaces
├── infrastructure/# DB, MQTT, cache, ML, notifications, commerce
├── api/           # FastAPI routers, middleware, schemas
├── workers/       # ARQ tasks and schedulers
└── simulator/     # Physics-based purifier simulator
```

## Key Commands

| Command | Description |
|---|---|
| `make install` | Install all dependencies |
| `make check` | Run all linters + type checker |
| `make test` | Run unit tests |
| `make test-all` | Run all tests with coverage |
| `make up` | Start Docker dev stack |
| `make api` | Run API server (dev mode) |
| `make demo` | Full demo with scenarios |

## Documentation

- [Architecture](docs/architecture.md) — System design and data flow
- [Algorithms](docs/algorithms.md) — Signal processing, health index, Kalman filter
- [MQTT Contract](docs/mqtt-contract.md) — Topic structure, payload format, security
- [API Guide](docs/api-guide.md) — REST API reference
- [Security](docs/security.md) — Auth, encryption, tenant isolation
- [Business Model](docs/business-model.md) — Pricing, revenue, unit economics
- [Runbook](docs/runbook.md) — Deployment, monitoring, incident response

## Tech Stack

- **Runtime**: Python 3.12, FastAPI (async), Pydantic v2
- **Database**: PostgreSQL 16 + TimescaleDB (hypertables, continuous aggregates)
- **Cache/Queue**: Redis + ARQ
- **MQTT**: Eclipse Mosquitto
- **ML**: LightGBM (gradient-boosted trees)
- **Observability**: structlog, OpenTelemetry, Prometheus, Grafana
- **Auth**: JWT + Argon2id + RBAC

## License

MIT — see [LICENSE](LICENSE).
