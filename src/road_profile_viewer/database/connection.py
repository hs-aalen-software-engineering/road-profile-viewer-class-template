"""
Database Connection Module
==========================
Provides SQLite database engine creation, session management,
and table initialization for the road profile database.
"""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

# Default database path - use absolute path relative to project root
# This ensures the database is always in the same location regardless of working directory
_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DEFAULT_DATABASE_PATH = _PROJECT_ROOT / "road_profiles.db"

# Module-level engine (lazy initialization)
_engine: Engine | None = None


def get_engine(database_path: Path | str | None = None, echo: bool = False) -> Engine:
    """
    Get or create the database engine.

    Parameters:
    -----------
    database_path : Path | str | None
        Path to the SQLite database file. If None, uses the default path.
        Use ":memory:" for in-memory database (useful for testing).
    echo : bool
        If True, log all SQL statements to stdout.

    Returns:
    --------
    Engine
        SQLAlchemy/SQLModel database engine instance.
    """
    global _engine

    if database_path is not None:
        # Create a new engine with custom path (for testing)
        db_url = f"sqlite:///{database_path}" if database_path != ":memory:" else "sqlite:///:memory:"
        return create_engine(db_url, echo=echo)

    # Use cached default engine
    if _engine is None:
        _engine = create_engine(f"sqlite:///{DEFAULT_DATABASE_PATH}", echo=echo)

    return _engine


def create_db_and_tables(engine: Engine | None = None) -> None:
    """
    Create all database tables defined by SQLModel models.

    Parameters:
    -----------
    engine : Engine | None
        Database engine to use. If None, uses the default engine.
    """
    if engine is None:
        engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_session(engine: Engine | None = None) -> Generator[Session, None, None]:
    """
    Get a database session.

    This is a generator function that yields a session and ensures
    proper cleanup after use. Designed to work with FastAPI's
    dependency injection.

    Parameters:
    -----------
    engine : Engine | None
        Database engine to use. If None, uses the default engine.

    Yields:
    -------
    Session
        A SQLModel session for database operations.
    """
    if engine is None:
        engine = get_engine()
    with Session(engine) as session:
        yield session


def reset_engine() -> None:
    """
    Reset the module-level engine cache.

    Useful for testing to ensure a fresh database connection.
    """
    global _engine
    _engine = None
