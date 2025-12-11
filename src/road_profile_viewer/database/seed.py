"""
Database Seed Module
====================
Seeds the database with default road profile data on first run.
"""

from sqlalchemy import Engine
from sqlmodel import Session

from road_profile_viewer.database.connection import create_db_and_tables, get_engine
from road_profile_viewer.database.crud import create_profile, get_profile_by_name
from road_profile_viewer.road import generate_road_profile

DEFAULT_PROFILE_NAME = "Default Clothoid Profile"


def seed_default_profile(session: Session) -> bool:
    """
    Seed the database with the default clothoid road profile.

    This function is idempotent - it checks if the default profile
    already exists before creating it.

    Parameters:
    -----------
    session : Session
        The database session.

    Returns:
    --------
    bool
        True if the profile was created, False if it already existed.
    """
    # Check if default profile already exists
    existing = get_profile_by_name(session, DEFAULT_PROFILE_NAME)
    if existing is not None:
        return False

    # Generate the default road profile using the existing function
    x_coords, y_coords = generate_road_profile(num_points=100, x_max=80)

    # Create the profile in the database
    create_profile(
        session=session,
        name=DEFAULT_PROFILE_NAME,
        x_coordinates=x_coords.tolist(),
        y_coordinates=y_coords.tolist(),
    )

    return True


def initialize_database(engine: Engine | None = None) -> None:
    """
    Initialize the database with tables and seed data.

    This function creates all tables and seeds the default profile.
    Safe to call multiple times - it's idempotent.

    Parameters:
    -----------
    engine : Engine | None
        Database engine to use. If None, uses the default engine.
    """
    if engine is None:
        engine = get_engine()

    # Create tables
    create_db_and_tables(engine)

    # Seed default profile
    with Session(engine) as session:
        seed_default_profile(session)


if __name__ == "__main__":
    # Allow running as a script: python -m road_profile_viewer.database.seed
    print("Initializing database...")
    initialize_database()
    print("Database initialized with default profile.")
