"""
CRUD Operations Module
======================
Create, Read, Update, Delete operations for road profiles in the database.
"""

import json

from sqlmodel import Session, select

from road_profile_viewer.database.models import RoadProfileDB


def create_profile(
    session: Session,
    name: str,
    x_coordinates: list[float],
    y_coordinates: list[float],
) -> RoadProfileDB:
    """
    Create a new road profile in the database.

    Parameters:
    -----------
    session : Session
        The database session.
    name : str
        Unique name for the road profile.
    x_coordinates : list[float]
        List of x-axis coordinates.
    y_coordinates : list[float]
        List of y-axis coordinates.

    Returns:
    --------
    RoadProfileDB
        The created road profile with assigned ID.

    Raises:
    -------
    IntegrityError
        If a profile with the same name already exists.
    """
    profile = RoadProfileDB.from_coordinates(name, x_coordinates, y_coordinates)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def get_profile(session: Session, profile_id: int) -> RoadProfileDB | None:
    """
    Get a road profile by its ID.

    Parameters:
    -----------
    session : Session
        The database session.
    profile_id : int
        The profile's database ID.

    Returns:
    --------
    RoadProfileDB | None
        The road profile if found, None otherwise.
    """
    return session.get(RoadProfileDB, profile_id)


def get_profile_by_name(session: Session, name: str) -> RoadProfileDB | None:
    """
    Get a road profile by its name.

    Parameters:
    -----------
    session : Session
        The database session.
    name : str
        The profile's name.

    Returns:
    --------
    RoadProfileDB | None
        The road profile if found, None otherwise.
    """
    statement = select(RoadProfileDB).where(RoadProfileDB.name == name)
    return session.exec(statement).first()


def get_all_profiles(session: Session) -> list[RoadProfileDB]:
    """
    Get all road profiles from the database.

    Parameters:
    -----------
    session : Session
        The database session.

    Returns:
    --------
    list[RoadProfileDB]
        List of all road profiles in the database.
    """
    statement = select(RoadProfileDB)
    return list(session.exec(statement).all())


def update_profile(
    session: Session,
    profile_id: int,
    name: str | None = None,
    x_coordinates: list[float] | None = None,
    y_coordinates: list[float] | None = None,
) -> RoadProfileDB | None:
    """
    Update an existing road profile.

    Parameters:
    -----------
    session : Session
        The database session.
    profile_id : int
        The profile's database ID.
    name : str | None
        New name for the profile (optional).
    x_coordinates : list[float] | None
        New x-axis coordinates (optional).
    y_coordinates : list[float] | None
        New y-axis coordinates (optional).

    Returns:
    --------
    RoadProfileDB | None
        The updated road profile if found, None otherwise.

    Raises:
    -------
    IntegrityError
        If the new name conflicts with an existing profile.
    """
    profile = session.get(RoadProfileDB, profile_id)
    if profile is None:
        return None

    if name is not None:
        profile.name = name
    if x_coordinates is not None:
        profile.x_coordinates = json.dumps(x_coordinates)
    if y_coordinates is not None:
        profile.y_coordinates = json.dumps(y_coordinates)

    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def delete_profile(session: Session, profile_id: int) -> bool:
    """
    Delete a road profile from the database.

    Parameters:
    -----------
    session : Session
        The database session.
    profile_id : int
        The profile's database ID.

    Returns:
    --------
    bool
        True if the profile was deleted, False if not found.
    """
    profile = session.get(RoadProfileDB, profile_id)
    if profile is None:
        return False

    session.delete(profile)
    session.commit()
    return True
