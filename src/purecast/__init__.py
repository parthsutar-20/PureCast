"""PureCast — Filter-health forecasting platform for water purifiers.

This is the top-level package. The application is structured using
hexagonal (ports and adapters) architecture:

- ``domain``: Pure Python business logic, no framework imports
- ``application``: Use cases, DTOs, port interfaces
- ``infrastructure``: Adapters for DB, MQTT, cache, ML, external services
- ``api``: FastAPI routers, middleware, schemas
- ``workers``: Background task definitions
- ``simulator``: Physics-based purifier simulator
"""

__version__ = "0.1.0"
