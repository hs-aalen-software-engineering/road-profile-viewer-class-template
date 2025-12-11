"""
FastAPI Main Application Module
===============================
FastAPI application for the Road Profile API.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from road_profile_viewer.api.routes import router
from road_profile_viewer.database.seed import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Initializes the database and seeds default data on startup.

    Args:
        app: The FastAPI application instance.
    """
    # Startup: Initialize database and seed default profile
    initialize_database()
    yield
    # Shutdown: Nothing to clean up


app = FastAPI(
    title="Road Profile API",
    description="REST API for managing road profiles",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/profiles", tags=["profiles"])


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint returning API information."""
    return {
        "message": "Road Profile API",
        "docs": "/docs",
        "profiles": "/profiles",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
