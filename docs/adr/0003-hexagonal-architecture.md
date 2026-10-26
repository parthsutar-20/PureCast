# ADR 0003: Hexagonal Architecture and Framework-Free Domain Core

## Status
Accepted

## Context
PureCast's core business value lies in its proprietary signal processing, physical normalization models, dual-state Kalman filter, and explainable diagnosis rule engine. If these algorithms are tightly coupled to web frameworks (e.g. FastAPI, Starlette) or ORMs (e.g. SQLAlchemy, Pydantic DB models), unit testing becomes cumbersome, simulator execution requires mock databases, and portability is severely degraded.

## Decision
We enforce a strict **Hexagonal (Ports and Adapters)** architecture:
- `src/purecast/domain/`: Pure Python 3.12 standard library only. Absolutely zero imports from FastAPI, SQLAlchemy, or Pydantic.
- `src/purecast/application/`: Defines abstract ports (repositories, notification senders, payment gateways) and orchestrates use cases.
- `src/purecast/infrastructure/`: Concrete adapters implementing the application ports.

## Rationale
1. **Mathematical Testability**: Algorithm tests can run in sub-second property tests (via Hypothesis) and golden numeric regression tests without database fixtures or network IO.
2. **Edge Portability**: The same pure Python algorithms can be compiled or packaged for edge microcontrollers or test bench rigs without refactoring.
