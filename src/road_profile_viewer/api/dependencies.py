"""
API Dependencies Module
=======================
Dependency injection for FastAPI endpoints.
"""

from collections.abc import Generator

from sqlmodel import Session

from road_profile_viewer.database.connection import get_engine


def get_db() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.

    This is used with FastAPI's Depends() to provide
    database sessions to route handlers.

    Yields:
    -------
    Session
        A SQLModel session for database operations.
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session
