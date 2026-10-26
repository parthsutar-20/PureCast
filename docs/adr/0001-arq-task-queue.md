# ADR 0001: Selection of ARQ as the Asynchronous Task Queue

## Status
Accepted

## Context
PureCast requires an asynchronous task processing engine for:
1. Incremental Kalman filter and Health Index forecast recomputations.
2. Training gradient-boosted ML models on historical telemetry rollups.
3. Automated push / email / WhatsApp notification dispatch.
4. Generating daily and weekly fleet analytical aggregations.

The primary candidates considered were **Celery** and **ARQ**.

## Decision
We select **ARQ** (Async Redis Queue) over Celery for all background task orchestration.

## Rationale
1. **Native Asyncio Alignment**: PureCast is built on async Python 3.12 and FastAPI. ARQ is natively async, running on top of `asyncio` and `aioredis` without thread-pool workarounds or event-loop conflicts.
2. **Reduced Infrastructure Surface**: ARQ relies exclusively on Redis, which is already a core component of our stack for caching, rate limiting, and MQTT idempotency keys. Celery often requires AMQP (RabbitMQ) for optimal performance.
3. **Simpler Configuration & Deployment**: ARQ tasks are standard async Python functions with typed signatures, cron scheduling decorators, and low operational overhead.
