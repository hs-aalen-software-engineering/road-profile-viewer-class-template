"""
API Routes Module
=================
REST API endpoints for road profile CRUD operations.
"""

# ruff: noqa: B008 - Depends in default args is FastAPI's standard pattern
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from road_profile_viewer.api.dependencies import get_db
from road_profile_viewer.database import crud
from road_profile_viewer.models import RoadProfile, RoadProfileResponse

router = APIRouter()


@router.get("/", response_model=list[RoadProfileResponse])
def list_profiles(session: Session = Depends(get_db)) -> list[RoadProfileResponse]:
    """
    List all road profiles.

    Returns:
        List of all road profiles in the database.
    """
    profiles = crud.get_all_profiles(session)
    return [
        RoadProfileResponse(
            id=p.id,  # type: ignore[arg-type]
            name=p.name,
            x_coordinates=p.get_x_coordinates(),
            y_coordinates=p.get_y_coordinates(),
        )
        for p in profiles
    ]


@router.post("/", response_model=RoadProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile: RoadProfile, session: Session = Depends(get_db)) -> RoadProfileResponse:
    """
    Create a new road profile.

    Args:
        profile: The road profile data to create.

    Returns:
        The created road profile with assigned ID.

    Raises:
        HTTPException: 409 Conflict if name already exists.
    """
    # Check for duplicate name
    existing = crud.get_profile_by_name(session, profile.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profile with name '{profile.name}' already exists",
        )

    try:
        db_profile = crud.create_profile(
            session=session,
            name=profile.name,
            x_coordinates=profile.x_coordinates,
            y_coordinates=profile.y_coordinates,
        )
        return RoadProfileResponse(
            id=db_profile.id,  # type: ignore[arg-type]
            name=db_profile.name,
            x_coordinates=db_profile.get_x_coordinates(),
            y_coordinates=db_profile.get_y_coordinates(),
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profile with name '{profile.name}' already exists",
        ) from e


@router.get("/{profile_id}", response_model=RoadProfileResponse)
def get_profile(profile_id: int, session: Session = Depends(get_db)) -> RoadProfileResponse:
    """
    Get a road profile by ID.

    Args:
        profile_id: The profile's database ID.

    Returns:
        The road profile with the specified ID.

    Raises:
        HTTPException: 404 Not Found if profile doesn't exist.
    """
    db_profile = crud.get_profile(session, profile_id)
    if db_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found",
        )

    return RoadProfileResponse(
        id=db_profile.id,  # type: ignore[arg-type]
        name=db_profile.name,
        x_coordinates=db_profile.get_x_coordinates(),
        y_coordinates=db_profile.get_y_coordinates(),
    )


@router.put("/{profile_id}", response_model=RoadProfileResponse)
def update_profile(
    profile_id: int,
    profile: RoadProfile,
    session: Session = Depends(get_db),
) -> RoadProfileResponse:
    """
    Update an existing road profile.

    Args:
        profile_id: The profile's database ID.
        profile: The updated profile data.

    Returns:
        The updated road profile.

    Raises:
        HTTPException: 404 Not Found if profile doesn't exist.
        HTTPException: 409 Conflict if new name already exists.
    """
    # Check if profile exists
    existing = crud.get_profile(session, profile_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found",
        )

    # Check for name conflict (if name changed)
    if profile.name != existing.name:
        name_conflict = crud.get_profile_by_name(session, profile.name)
        if name_conflict is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Profile with name '{profile.name}' already exists",
            )

    try:
        db_profile = crud.update_profile(
            session=session,
            profile_id=profile_id,
            name=profile.name,
            x_coordinates=profile.x_coordinates,
            y_coordinates=profile.y_coordinates,
        )
        if db_profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile with id {profile_id} not found",
            )

        return RoadProfileResponse(
            id=db_profile.id,  # type: ignore[arg-type]
            name=db_profile.name,
            x_coordinates=db_profile.get_x_coordinates(),
            y_coordinates=db_profile.get_y_coordinates(),
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profile with name '{profile.name}' already exists",
        ) from e


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, session: Session = Depends(get_db)) -> None:
    """
    Delete a road profile.

    Args:
        profile_id: The profile's database ID.

    Raises:
        HTTPException: 404 Not Found if profile doesn't exist.
    """
    success = crud.delete_profile(session, profile_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found",
        )
