"""
Unit Tests for CRUD Operations
==============================
Test coverage for Create, Read, Update, Delete operations on road profiles.

Test Coverage:
- create_profile(): Profile creation with various inputs
- get_profile(): Profile retrieval by ID
- get_profile_by_name(): Profile retrieval by name
- get_all_profiles(): Listing all profiles
- update_profile(): Profile updates
- delete_profile(): Profile deletion
"""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from road_profile_viewer.database.connection import create_db_and_tables, get_engine
from road_profile_viewer.database.crud import (
    create_profile,
    delete_profile,
    get_all_profiles,
    get_profile,
    get_profile_by_name,
    update_profile,
)
from road_profile_viewer.database.models import RoadProfileDB


@pytest.fixture
def db_session():
    """
    Create an in-memory database session for testing.

    Yields:
        Session: A fresh database session with tables created.
    """
    engine = get_engine(":memory:")
    create_db_and_tables(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def sample_coordinates():
    """Sample coordinate data for testing."""
    return {
        "x": [0.0, 10.0, 20.0, 30.0, 40.0],
        "y": [0.0, 2.5, 5.0, 3.5, 1.0],
    }


class TestCreateProfile:
    """Tests for the create_profile() function."""

    def test_create_profile_returns_profile_with_id(self, db_session, sample_coordinates) -> None:
        """
        Test that create_profile() returns a profile with an assigned ID.

        Equivalence class: Successful profile creation
        """
        profile = create_profile(
            db_session,
            name="test_profile",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        assert profile.id is not None
        assert profile.id > 0
        assert profile.name == "test_profile"

    def test_create_profile_stores_coordinates(self, db_session, sample_coordinates) -> None:
        """
        Test that create_profile() correctly stores coordinates.

        Equivalence class: Coordinate storage
        """
        profile = create_profile(
            db_session,
            name="coords_test",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        assert profile.get_x_coordinates() == sample_coordinates["x"]
        assert profile.get_y_coordinates() == sample_coordinates["y"]

    def test_create_profile_persists_to_database(self, db_session, sample_coordinates) -> None:
        """
        Test that create_profile() persists the profile to the database.

        Equivalence class: Database persistence
        """
        profile = create_profile(
            db_session,
            name="persisted",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        # Query it back
        retrieved = db_session.get(RoadProfileDB, profile.id)
        assert retrieved is not None
        assert retrieved.name == "persisted"

    def test_create_profile_duplicate_name_raises_error(self, db_session, sample_coordinates) -> None:
        """
        Test that creating a profile with a duplicate name raises IntegrityError.

        Equivalence class: Unique constraint violation
        """
        create_profile(
            db_session,
            name="duplicate",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        with pytest.raises(IntegrityError):
            create_profile(
                db_session,
                name="duplicate",  # Same name
                x_coordinates=[0.0, 1.0],
                y_coordinates=[0.0, 1.0],
            )

    def test_create_multiple_profiles(self, db_session) -> None:
        """
        Test that multiple profiles can be created.

        Equivalence class: Multiple profile creation
        """
        profile1 = create_profile(db_session, "profile1", [0.0, 1.0], [0.0, 1.0])
        profile2 = create_profile(db_session, "profile2", [0.0, 2.0], [0.0, 2.0])
        profile3 = create_profile(db_session, "profile3", [0.0, 3.0], [0.0, 3.0])

        assert profile1.id != profile2.id != profile3.id
        assert profile1.name == "profile1"
        assert profile2.name == "profile2"
        assert profile3.name == "profile3"


class TestGetProfile:
    """Tests for the get_profile() function."""

    def test_get_profile_returns_existing_profile(self, db_session, sample_coordinates) -> None:
        """
        Test that get_profile() returns an existing profile by ID.

        Equivalence class: Successful retrieval
        """
        created = create_profile(
            db_session,
            name="retrievable",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        retrieved = get_profile(db_session, created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "retrievable"

    def test_get_profile_returns_none_for_nonexistent_id(self, db_session) -> None:
        """
        Test that get_profile() returns None for a nonexistent ID.

        Equivalence class: Profile not found
        """
        result = get_profile(db_session, 9999)

        assert result is None

    def test_get_profile_returns_none_for_zero_id(self, db_session) -> None:
        """
        Test that get_profile() returns None for ID 0.

        Boundary value: ID boundary (0)
        """
        result = get_profile(db_session, 0)

        assert result is None

    def test_get_profile_returns_none_for_negative_id(self, db_session) -> None:
        """
        Test that get_profile() returns None for negative IDs.

        Boundary value: Negative ID
        """
        result = get_profile(db_session, -1)

        assert result is None


class TestGetProfileByName:
    """Tests for the get_profile_by_name() function."""

    def test_get_profile_by_name_returns_existing_profile(self, db_session, sample_coordinates) -> None:
        """
        Test that get_profile_by_name() returns an existing profile.

        Equivalence class: Successful retrieval by name
        """
        create_profile(
            db_session,
            name="named_profile",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        retrieved = get_profile_by_name(db_session, "named_profile")

        assert retrieved is not None
        assert retrieved.name == "named_profile"

    def test_get_profile_by_name_returns_none_for_nonexistent(self, db_session) -> None:
        """
        Test that get_profile_by_name() returns None for nonexistent names.

        Equivalence class: Profile not found
        """
        result = get_profile_by_name(db_session, "nonexistent")

        assert result is None

    def test_get_profile_by_name_is_case_sensitive(self, db_session, sample_coordinates) -> None:
        """
        Test that get_profile_by_name() is case-sensitive.

        Equivalence class: Case sensitivity
        """
        create_profile(
            db_session,
            name="CaseSensitive",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        # Exact match should work
        assert get_profile_by_name(db_session, "CaseSensitive") is not None

        # Different case should not match
        assert get_profile_by_name(db_session, "casesensitive") is None
        assert get_profile_by_name(db_session, "CASESENSITIVE") is None


class TestGetAllProfiles:
    """Tests for the get_all_profiles() function."""

    def test_get_all_profiles_returns_empty_list_initially(self, db_session) -> None:
        """
        Test that get_all_profiles() returns empty list when no profiles exist.

        Boundary value: Empty database
        """
        result = get_all_profiles(db_session)

        assert result == []

    def test_get_all_profiles_returns_all_profiles(self, db_session) -> None:
        """
        Test that get_all_profiles() returns all created profiles.

        Equivalence class: Multiple profiles retrieval
        """
        create_profile(db_session, "profile1", [0.0, 1.0], [0.0, 1.0])
        create_profile(db_session, "profile2", [0.0, 2.0], [0.0, 2.0])
        create_profile(db_session, "profile3", [0.0, 3.0], [0.0, 3.0])

        result = get_all_profiles(db_session)

        assert len(result) == 3
        names = {p.name for p in result}
        assert names == {"profile1", "profile2", "profile3"}

    def test_get_all_profiles_returns_single_profile(self, db_session, sample_coordinates) -> None:
        """
        Test that get_all_profiles() returns a list with one profile.

        Boundary value: Single profile
        """
        create_profile(
            db_session,
            name="only_one",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        result = get_all_profiles(db_session)

        assert len(result) == 1
        assert result[0].name == "only_one"


class TestUpdateProfile:
    """Tests for the update_profile() function."""

    def test_update_profile_changes_name(self, db_session, sample_coordinates) -> None:
        """
        Test that update_profile() can change the profile name.

        Equivalence class: Name update
        """
        profile = create_profile(
            db_session,
            name="original_name",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        updated = update_profile(db_session, profile.id, name="new_name")

        assert updated is not None
        assert updated.name == "new_name"

    def test_update_profile_changes_coordinates(self, db_session, sample_coordinates) -> None:
        """
        Test that update_profile() can change coordinates.

        Equivalence class: Coordinate update
        """
        profile = create_profile(
            db_session,
            name="coords_update",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        new_x = [0.0, 5.0, 10.0]
        new_y = [0.0, 2.0, 4.0]

        updated = update_profile(db_session, profile.id, x_coordinates=new_x, y_coordinates=new_y)

        assert updated is not None
        assert updated.get_x_coordinates() == new_x
        assert updated.get_y_coordinates() == new_y

    def test_update_profile_partial_update(self, db_session, sample_coordinates) -> None:
        """
        Test that update_profile() can update only some fields.

        Equivalence class: Partial update
        """
        profile = create_profile(
            db_session,
            name="partial",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )

        # Only update name
        updated = update_profile(db_session, profile.id, name="partial_updated")

        assert updated is not None
        assert updated.name == "partial_updated"
        # Coordinates should be unchanged
        assert updated.get_x_coordinates() == sample_coordinates["x"]
        assert updated.get_y_coordinates() == sample_coordinates["y"]

    def test_update_profile_returns_none_for_nonexistent(self, db_session) -> None:
        """
        Test that update_profile() returns None for nonexistent profile.

        Equivalence class: Profile not found
        """
        result = update_profile(db_session, 9999, name="new_name")

        assert result is None

    def test_update_profile_duplicate_name_raises_error(self, db_session, sample_coordinates) -> None:
        """
        Test that updating to a duplicate name raises IntegrityError.

        Equivalence class: Unique constraint violation on update
        """
        profile1 = create_profile(db_session, "profile1", sample_coordinates["x"], sample_coordinates["y"])
        create_profile(db_session, "profile2", [0.0, 1.0], [0.0, 1.0])

        with pytest.raises(IntegrityError):
            update_profile(db_session, profile1.id, name="profile2")


class TestDeleteProfile:
    """Tests for the delete_profile() function."""

    def test_delete_profile_removes_profile(self, db_session, sample_coordinates) -> None:
        """
        Test that delete_profile() removes the profile from the database.

        Equivalence class: Successful deletion
        """
        profile = create_profile(
            db_session,
            name="to_delete",
            x_coordinates=sample_coordinates["x"],
            y_coordinates=sample_coordinates["y"],
        )
        profile_id = profile.id

        result = delete_profile(db_session, profile_id)

        assert result is True
        assert get_profile(db_session, profile_id) is None

    def test_delete_profile_returns_false_for_nonexistent(self, db_session) -> None:
        """
        Test that delete_profile() returns False for nonexistent profile.

        Equivalence class: Profile not found
        """
        result = delete_profile(db_session, 9999)

        assert result is False

    def test_delete_profile_does_not_affect_other_profiles(self, db_session) -> None:
        """
        Test that delete_profile() only removes the specified profile.

        Equivalence class: Deletion isolation
        """
        profile1 = create_profile(db_session, "keep1", [0.0, 1.0], [0.0, 1.0])
        profile2 = create_profile(db_session, "delete_me", [0.0, 2.0], [0.0, 2.0])
        profile3 = create_profile(db_session, "keep2", [0.0, 3.0], [0.0, 3.0])

        delete_profile(db_session, profile2.id)

        # Other profiles should still exist
        assert get_profile(db_session, profile1.id) is not None
        assert get_profile(db_session, profile3.id) is not None
        assert len(get_all_profiles(db_session)) == 2
