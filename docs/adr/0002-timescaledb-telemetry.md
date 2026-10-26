# ADR 0002: Utilization of TimescaleDB for High-Frequency Telemetry

## Status
Accepted

## Context
A fleet of 10,000 smart water purifiers transmitting 1 message per minute yields ~14.4 million rows per day (~167 msg/sec). Telemetry requires high-throughput continuous batch insertion, automatic partition pruning by time, continuous downsampled rollups (hourly and daily), and automated compression policies to conserve disk space.

## Decision
We select **TimescaleDB** on top of PostgreSQL 16.

## Rationale
1. **Unified Relational & Time-Series Data**: Relational domain data (tenants, users, devices, cartridges, service orders) and time-series telemetry live within the same database engine, avoiding dual-write distributed transaction complexities.
2. **Hypertables & Native Compression**: Hypertables transparently partition data by time and space. Columnar compression reduces telemetry storage footprint by 85–90%.
3. **Continuous Aggregates**: TimescaleDB continuous aggregates automatically maintain hourly rollups used for ML feature extraction and fleet dashboards without manual batch query overhead.
