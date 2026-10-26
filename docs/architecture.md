# PureCast System Architecture

## Overview

PureCast is an intelligent filter-health forecasting and diagnostics platform for water purifiers (Track 2, atomQUEST 2026). It combines physics-based priors with real-time sensor processing and ML gradient-boosted trees to predict consumable exhaustion, detect faults early, and automate supply-chain fulfillment.

```mermaid
graph TB
    subgraph Sensors["Edge Sensors"]
        P1["P1: Inlet Pressure"]
        P2["P2: Pre-filter Pressure"]
        P3["P3: Post-RO Pressure"]
        FL["Flow Meter"]
        TI["TDS In"]
        TO["TDS Out"]
        TMP["Water Temperature"]
        TURB["Turbidity Sensor"]
        UV["UV Lamp Current"]
    end

    subgraph Edge["ESP32-C3 Firmware"]
        ADC["ADC Sampling & Calibration"]
        MQTT_CLI["MQTT Client (TLS + HMAC-SHA256)"]
        Sensors --> ADC --> MQTT_CLI
    end

    subgraph Broker["Message Broker"]
        MOSQ["Mosquitto (MQTT 3.1.1 / WebSockets)"]
        MQTT_CLI -->|TLS Port 8883 / 1883| MOSQ
    end

    subgraph Ingest["Ingestion Pipeline"]
        AIOMQTT["aiomqtt Consumer Pool"]
        MOSQ --> AIOMQTT
        VAL["HMAC & Replay Validator"]
        BATCH["Timescale Batch Inserter"]
        AIOMQTT --> VAL --> BATCH
    end

    subgraph Storage["Data Tier"]
        TS[(PostgreSQL 16 + TimescaleDB)]
        REDIS[(Redis 7)]
        BATCH --> TS
    end

    subgraph Queue["Async Task Queue"]
        ARQ["ARQ Workers"]
        AIOMQTT -.->|Enqueue job| ARQ
    end

    subgraph Engine["Domain Intelligence (Pure Python)"]
        SAN["Sanity Checks & Median Filter"]
        NORM["Temperature & NDP Correction"]
        HI["Health Index Computer (0-100%)"]
        KF["Dual-State Kalman Forecaster"]
        DIAG["Explainable Diagnosis Engine"]
        ARQ --> SAN --> NORM --> HI --> KF --> DIAG
        DIAG --> TS
    end

    subgraph API["FastAPI Gateway"]
        AUTH["OAuth2 / JWT / RBAC"]
        REST["REST API v1"]
        WS["WebSocket Live Stream"]
        AUTH --> REST
        AUTH --> WS
    end

    TS --> REST
    REDIS --> REST
    REDIS --> WS
    DIAG -.->|PubSub| REDIS
```

## Architectural Layers (Hexagonal Architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                       api / workers / cli                       │  Driving Adapters
│  (FastAPI routers, WebSocket, ARQ worker tasks, CLI commands)   │
├─────────────────────────────────────────────────────────────────┤
│                          application                            │  Application Services
│       (Use cases, DTOs, Port Interfaces, Authorization)         │
├─────────────────────────────────────────────────────────────────┤
│                            domain                               │  Pure Domain Core
│   (Entities, Value Objects, Signal, Health, Kalman, Diagnosis)  │  (Zero Framework Deps)
├─────────────────────────────────────────────────────────────────┤
│                        infrastructure                           │  Driven Adapters
│ (TimescaleDB, Redis, MQTT Ingestor, LightGBM, Commerce, Notifs) │
└─────────────────────────────────────────────────────────────────┘
```

### 1. Domain Layer (`purecast.domain`)
Pure Python 3.12, strict typing, zero external framework imports (no FastAPI, no SQLAlchemy, no Pydantic in domain). Completely portable and deterministically testable.
- `enums`: Vocabulary for consumables, fault types, operating modes, tiers, roles.
- `signal`: Rolling median filters, sensor sanity checking, temperature & net driving pressure (NDP) normalization.
- `health`: Baseline-relative health index computation, mode-aware ageing models (RO vs UF vs Vacay).
- `prognostics`: Two-state Kalman filter estimating health state and rate of decay, with early warning bias and 14-day cold-start learning band.
- `diagnosis`: Hysteresis-guarded rule engine enforcing 2-indicator agreement and event tagging (power cuts, cold mornings).

### 2. Application Layer (`purecast.application`)
Orchestrates domain services, executes use cases, defines ports (interfaces) for repositories, queues, notifications, and commerce adapters.

### 3. Infrastructure Layer (`purecast.infrastructure`)
Concrete implementations of application ports:
- `db`: SQLAlchemy 2.0 async models, TimescaleDB hypertables, compression policies.
- `mqtt`: `aiomqtt` worker, HMAC-SHA256 signature verification, replay protection.
- `ml`: LightGBM training pipeline, model registry, champion/challenger promotions.
- `queue`: ARQ Redis task runner.
- `notifications`: Push / WhatsApp / Email adapters.
- `commerce`: Reorder and technician service dispatch.

### 4. API Layer (`purecast.api`)
FastAPI application with dependency injection, OpenAPI documentation, RFC 7807 problem details, rate limiting, and JWT authentication.
