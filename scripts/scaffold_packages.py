"""Create all package directories and __init__.py files for PureCast scaffold."""

from pathlib import Path

BASE = Path(r"c:\Users\Samruddhi\OneDrive\Desktop\PureCast")

# All Python package directories
PACKAGES = [
    "src/purecast",
    "src/purecast/core",
    "src/purecast/domain",
    "src/purecast/domain/entities",
    "src/purecast/domain/value_objects",
    "src/purecast/domain/signal",
    "src/purecast/domain/health",
    "src/purecast/domain/prognostics",
    "src/purecast/domain/diagnosis",
    "src/purecast/domain/services",
    "src/purecast/application",
    "src/purecast/application/ports",
    "src/purecast/application/use_cases",
    "src/purecast/application/dtos",
    "src/purecast/infrastructure",
    "src/purecast/infrastructure/db",
    "src/purecast/infrastructure/mqtt",
    "src/purecast/infrastructure/cache",
    "src/purecast/infrastructure/queue",
    "src/purecast/infrastructure/ml",
    "src/purecast/infrastructure/notifications",
    "src/purecast/infrastructure/commerce",
    "src/purecast/infrastructure/billing",
    "src/purecast/api",
    "src/purecast/api/v1",
    "src/purecast/api/v1/routers",
    "src/purecast/api/middleware",
    "src/purecast/api/schemas",
    "src/purecast/workers",
    "src/purecast/simulator",
    "tests",
    "tests/unit",
    "tests/unit/domain",
    "tests/unit/domain/signal",
    "tests/unit/domain/health",
    "tests/unit/domain/prognostics",
    "tests/unit/domain/diagnosis",
    "tests/unit/api",
    "tests/unit/core",
    "tests/integration",
    "tests/e2e",
    "tests/property",
    "tests/load",
    "tests/fixtures",
    "tests/golden",
]

# Non-Python directories (no __init__.py)
DIRS_ONLY = [
    "migrations/versions",
    "scripts",
    "docs/adr",
    "models",
]

# Package docstrings
DOCSTRINGS = {
    "src/purecast": '"""PureCast — Filter-health forecasting platform for water purifiers."""\n',
    "src/purecast/core": '"""Core infrastructure: config, logging, security, errors, telemetry."""\n',
    "src/purecast/domain": '"""Pure domain logic — zero framework imports allowed."""\n',
    "src/purecast/domain/entities": '"""Domain entities representing core business objects."""\n',
    "src/purecast/domain/value_objects": '"""Immutable value objects for the domain layer."""\n',
    "src/purecast/domain/signal": '"""Signal processing: median filter, sanity checks, normalization."""\n',
    "src/purecast/domain/health": '"""Health index computation, EOL lines, mode-aware ageing."""\n',
    "src/purecast/domain/prognostics": '"""Prognostics: Kalman filter, remaining-life estimator, priors."""\n',
    "src/purecast/domain/diagnosis": '"""Diagnosis engine: rules, hysteresis, event tagging."""\n',
    "src/purecast/domain/services": '"""Domain services orchestrating cross-entity business logic."""\n',
    "src/purecast/application": '"""Application layer: use cases, DTOs, port interfaces."""\n',
    "src/purecast/application/ports": '"""Port interfaces (driven/driving) for hexagonal architecture."""\n',
    "src/purecast/application/use_cases": '"""Application use cases orchestrating domain logic."""\n',
    "src/purecast/application/dtos": '"""Data transfer objects for application boundaries."""\n',
    "src/purecast/infrastructure": '"""Infrastructure adapters: DB, MQTT, cache, ML, notifications."""\n',
    "src/purecast/infrastructure/db": '"""Database models, repositories, unit of work, TimescaleDB setup."""\n',
    "src/purecast/infrastructure/mqtt": '"""MQTT ingestion: topic router, payload validation, connection."""\n',
    "src/purecast/infrastructure/cache": '"""Redis cache adapter for forecasts and sessions."""\n',
    "src/purecast/infrastructure/queue": '"""ARQ task queue configuration and utilities."""\n',
    "src/purecast/infrastructure/ml": '"""ML pipeline: feature engineering, training, registry, prediction."""\n',
    "src/purecast/infrastructure/notifications": '"""Notification adapters: push, email, WhatsApp."""\n',
    "src/purecast/infrastructure/commerce": '"""Commerce adapters: cartridge catalog, reorder, service requests."""\n',
    "src/purecast/infrastructure/billing": '"""Billing: usage metering, invoices, payment gateway adapters."""\n',
    "src/purecast/api": '"""FastAPI application: routers, middleware, schemas."""\n',
    "src/purecast/api/v1": '"""API version 1 router aggregation."""\n',
    "src/purecast/api/v1/routers": '"""V1 API route handlers."""\n',
    "src/purecast/api/middleware": '"""Request/response middleware: auth, rate limiting, correlation IDs."""\n',
    "src/purecast/api/schemas": '"""Pydantic request/response schemas for the API layer."""\n',
    "src/purecast/workers": '"""ARQ background workers: forecast recompute, training, notifications."""\n',
    "src/purecast/simulator": '"""Physics-based purifier simulator for demos and testing."""\n',
}


def main() -> None:
    created = 0

    # Create Python packages with __init__.py
    for pkg in PACKAGES:
        pkg_path = BASE / pkg
        pkg_path.mkdir(parents=True, exist_ok=True)
        init_file = pkg_path / "__init__.py"
        if not init_file.exists():
            content = DOCSTRINGS.get(pkg, "")
            init_file.write_text(content, encoding="utf-8")
            created += 1
            print(f"  + {pkg}/__init__.py")

    # Create non-Python directories
    for d in DIRS_ONLY:
        dir_path = BASE / d
        dir_path.mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to empty dirs
        gitkeep = dir_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

    print(f"\nCreated {created} __init__.py files")
    print(f"Created {len(DIRS_ONLY)} non-Python directories")


if __name__ == "__main__":
    main()
