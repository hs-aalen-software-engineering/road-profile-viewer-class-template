"""
Unit Tests for Database Seed Module
===================================
Test coverage for database initialization and seeding.

Test Coverage:
- seed_default_profile(): Default profile seeding
- initialize_database(): Full database initialization
"""

import pytest
from sqlmodel import Session

from road_profile_viewer.database.connection import create_db_and_tables, get_engine, reset_engine
from road_profile_viewer.database.crud import get_all_profiles, get_profile_by_name
from road_profile_viewer.database.seed import (
    DEFAULT_PROFILE_NAME,
    initialize_database,
    seed_default_profile,
)


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
def empty_engine():
    """
    Create an in-memory database engine without any data.

    Returns:
        Engine: A fresh database engine.
    """
    return get_engine(":memory:")


class TestSeedDefaultProfile:
    """Tests for the seed_default_profile() function."""

    def test_seed_default_profile_creates_profile(self, db_session) -> None:
        """
        Test that seed_default_profile() creates the default profile.

        Equivalence class: First-time seeding
        """
        result = seed_default_profile(db_session)

        assert result is True
        profile = get_profile_by_name(db_session, DEFAULT_PROFILE_NAME)
        assert profile is not None
        assert profile.name == DEFAULT_PROFILE_NAME

    def test_seed_default_profile_has_valid_coordinates(self, db_session) -> None:
        """
        Test that the seeded profile has valid coordinates.

        Equivalence class: Seed data quality
        """
        seed_default_profile(db_session)

        profile = get_profile_by_name(db_session, DEFAULT_PROFILE_NAME)
        x_coords = profile.get_x_coordinates()
        y_coords = profile.get_y_coordinates()

        # Should have 100 points (default from generate_road_profile)
        assert len(x_coords) == 100
        assert len(y_coords) == 100

        # x_coords should range from 0 to ~80
        assert x_coords[0] == 0.0
        assert x_coords[-1] == pytest.approx(80.0, rel=0.01)

        # y_coords should be reasonable values
        assert all(isinstance(y, float) for y in y_coords)

    def test_seed_default_profile_is_idempotent(self, db_session) -> None:
        """
        Test that seed_default_profile() is idempotent (can be called multiple times).

        Equivalence class: Idempotent operation
        """
        # First call should create
        result1 = seed_default_profile(db_session)
        assert result1 is True

        # Second call should skip (profile exists)
        result2 = seed_default_profile(db_session)
        assert result2 is False

        # Should still have only one profile
        profiles = get_all_profiles(db_session)
        assert len(profiles) == 1

    def test_seed_default_profile_returns_false_if_exists(self, db_session) -> None:
        """
        Test that seed_default_profile() returns False if profile already exists.

        Equivalence class: Existing profile detection
        """
        # Create the profile first
        seed_default_profile(db_session)

        # Second call should return False
        result = seed_default_profile(db_session)

        assert result is False


class TestInitializeDatabase:
    """Tests for the initialize_database() function."""

    def test_initialize_database_creates_tables(self, empty_engine) -> None:
        """
        Test that initialize_database() creates the necessary tables.

        Equivalence class: Table creation
        """
        initialize_database(empty_engine)

        # Should be able to query without errors
        with Session(empty_engine) as session:
            profiles = get_all_profiles(session)
            # Should have at least the default profile
            assert len(profiles) >= 1

    def test_initialize_database_seeds_default_profile(self, empty_engine) -> None:
        """
        Test that initialize_database() seeds the default profile.

        Equivalence class: Default profile seeding
        """
        initialize_database(empty_engine)

        with Session(empty_engine) as session:
            profile = get_profile_by_name(session, DEFAULT_PROFILE_NAME)
            assert profile is not None

    def test_initialize_database_is_idempotent(self, empty_engine) -> None:
        """
        Test that initialize_database() can be called multiple times safely.

        Equivalence class: Idempotent operation
        """
        # Call multiple times
        initialize_database(empty_engine)
        initialize_database(empty_engine)
        initialize_database(empty_engine)

        # Should still have only one default profile
        with Session(empty_engine) as session:
            profiles = get_all_profiles(session)
            default_profiles = [p for p in profiles if p.name == DEFAULT_PROFILE_NAME]
            assert len(default_profiles) == 1


class TestDefaultProfileName:
    """Tests for the DEFAULT_PROFILE_NAME constant."""

    def test_default_profile_name_is_non_empty(self) -> None:
        """
        Test that DEFAULT_PROFILE_NAME is a non-empty string.

        Equivalence class: Configuration validation
        """
        assert isinstance(DEFAULT_PROFILE_NAME, str)
        assert len(DEFAULT_PROFILE_NAME) > 0

    def test_default_profile_name_is_descriptive(self) -> None:
        """
        Test that DEFAULT_PROFILE_NAME is descriptive.

        Equivalence class: User experience
        """
        # Should contain meaningful words
        assert "profile" in DEFAULT_PROFILE_NAME.lower() or "clothoid" in DEFAULT_PROFILE_NAME.lower()


class TestSeedModuleScript:
    """Tests for running seed module as a script."""

    def test_seed_module_main_block_via_runpy(self, tmp_path, monkeypatch, capsys) -> None:
        """
        Test that running seed.py as __main__ initializes the database.

        This tests lines 78-80 (if __name__ == "__main__" block).
        """
        import runpy

        import road_profile_viewer.database.connection as conn_module

        # Reset any cached engine
        reset_engine()

        # Override the default database path to use temp directory
        temp_db = tmp_path / "runpy_test.db"
        monkeypatch.setattr(conn_module, "DEFAULT_DATABASE_PATH", temp_db)

        # Run the module as __main__ using runpy
        # This executes the if __name__ == "__main__" block
        runpy.run_module("road_profile_viewer.database.seed", run_name="__main__")

        # Verify output contains the expected messages
        captured = capsys.readouterr()
        assert "Initializing database" in captured.out
        assert "initialized" in captured.out

        # Verify database was created
        assert temp_db.exists()

        # Cleanup
        reset_engine()
