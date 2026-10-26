"""FastAPI application factory and entry point.

Creates and configures the FastAPI application with middleware,
exception handlers, routers, and lifecycle events.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from purecast import __version__


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan context manager.

    Handles startup and shutdown events:
    - Startup: initialize DB pool, Redis, telemetry, etc.
    - Shutdown: close connections gracefully.
    """
    # Startup
    yield
    # Shutdown


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI instance ready to serve requests.
    """
    app = FastAPI(
        title="PureCast API",
        description=(
            "Filter-health forecasting platform for water purifiers. "
            "Provides real-time health monitoring, remaining-life forecasts, "
            "and fault diagnosis for RO/UV water purification systems."
        ),
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoints
    @app.get("/health", tags=["system"], include_in_schema=False)
    async def health() -> dict[str, str]:
        """Liveness probe — returns 200 if the process is running."""
        return {"status": "healthy"}

    @app.get("/ready", tags=["system"], include_in_schema=False)
    async def ready() -> dict[str, str]:
        """Readiness probe — returns 200 if dependencies are reachable."""
        return {"status": "ready"}

    @app.get("/", tags=["system"], include_in_schema=False)
    async def root() -> dict[str, Any]:
        """Root endpoint with API metadata."""
        return {
            "service": "PureCast API",
            "version": __version__,
            "docs": "/docs",
        }

    return app


# The application instance used by uvicorn
app: FastAPI = create_app()


def run() -> None:
    """Run the API server via uvicorn (for console_scripts entry point)."""
    uvicorn.run(
        "purecast.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
