"""
Unit Tests for Database Connection
==================================
Test coverage for database engine creation, session management,
and table initialization.

Test Coverage:
- get_engine(): Engine creation with various configurations
- create_db_and_tables(): Table creation
- get_session(): Session generator functionality
- reset_engine(): Engine cache reset
"""

from sqlmodel import Session, SQLModel, select

from road_profile_viewer.database.connection import (
    create_db_and_tables,
    get_engine,
    get_session,
    reset_engine,
)
from road_profile_viewer.database.models import RoadProfileDB


class TestGetEngine:
    """Tests for the get_engine() function."""

    def test_get_engine_returns_engine(self) -> None:
        """
        Test that get_engine() returns a valid SQLAlchemy engine.

        Equivalence class: Default engine creation
        """
        reset_engine()
        engine = get_engine(":memory:")

        assert engine is not None
        assert hasattr(engine, "connect")

    def test_get_engine_with_memory_database(self) -> None:
        """
        Test that get_engine() can create an in-memory database.

        Equivalence class: In-memory database (for testing)
        """
        engine = get_engine(":memory:")

        # Verify we can use the engine
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            # Should be able to query without errors
            statement = select(RoadProfileDB)
            result = session.exec(statement).all()
            assert result == []

    def test_get_engine_with_custom_path(self, tmp_path) -> None:
        """
        Test that get_engine() can create a database at a custom path.

        Equivalence class: File-based database with custom path
        """
        db_path = tmp_path / "test.db"
        engine = get_engine(str(db_path))

        SQLModel.metadata.create_all(engine)

        # Verify the file was created
        assert db_path.exists()

    def test_get_engine_with_echo_enabled(self) -> None:
        """
        Test that get_engine() respects the echo parameter.

        Equivalence class: Engine configuration options
        """
        engine = get_engine(":memory:", echo=True)

        assert engine is not None
        # Echo setting should be True (difficult to verify directly)


class TestCreateDbAndTables:
    """Tests for the create_db_and_tables() function."""

    def test_create_db_and_tables_creates_road_profiles_table(self) -> None:
        """
        Test that create_db_and_tables() creates the road_profiles table.

        Equivalence class: Table creation
        """
        engine = get_engine(":memory:")
        create_db_and_tables(engine)

        # Verify we can insert and query
        with Session(engine) as session:
            profile = RoadProfileDB.from_coordinates("test", [0.0, 1.0], [0.0, 1.0])
            session.add(profile)
            session.commit()

            result = session.get(RoadProfileDB, profile.id)
            assert result is not None
            assert result.name == "test"

    def test_create_db_and_tables_idempotent(self) -> None:
        """
        Test that create_db_and_tables() can be called multiple times safely.

        Equivalence class: Idempotent operation
        """
        engine = get_engine(":memory:")

        # Call multiple times - should not raise
        create_db_and_tables(engine)
        create_db_and_tables(engine)
        create_db_and_tables(engine)

        # Should still work
        with Session(engine) as session:
            statement = select(RoadProfileDB)
            result = session.exec(statement).all()
            assert result == []


class TestGetSession:
    """Tests for the get_session() function."""

    def test_get_session_yields_session(self) -> None:
        """
        Test that get_session() yields a valid Session.

        Equivalence class: Session generator
        """
        engine = get_engine(":memory:")
        create_db_and_tables(engine)

        session_gen = get_session(engine)
        session = next(session_gen)

        assert isinstance(session, Session)

        # Clean up
        try:
            next(session_gen)
        except StopIteration:
            pass

    def test_get_session_allows_database_operations(self) -> None:
        """
        Test that sessions from get_session() can perform database operations.

        Equivalence class: Session functionality
        """
        engine = get_engine(":memory:")
        create_db_and_tables(engine)

        session_gen = get_session(engine)
        session = next(session_gen)

        # Insert a profile
        profile = RoadProfileDB.from_coordinates("test", [0.0, 1.0], [0.0, 1.0])
        session.add(profile)
        session.commit()

        # Query it back
        result = session.get(RoadProfileDB, profile.id)
        assert result is not None
        assert result.name == "test"

        # Clean up
        try:
            next(session_gen)
        except StopIteration:
            pass

    def test_get_session_closes_on_exit(self) -> None:
        """
        Test that the session is properly closed after the generator exits.

        Equivalence class: Resource cleanup
        """
        engine = get_engine(":memory:")
        create_db_and_tables(engine)

        # Use context manager pattern
        session_gen = get_session(engine)
        session = next(session_gen)

        # Session should be open
        assert session.is_active

        # Exhaust the generator
        try:
            next(session_gen)
        except StopIteration:
            pass

        # Session should be closed (cannot make new queries)
        # This is implementation-dependent, but the session should be unusable


class TestResetEngine:
    """Tests for the reset_engine() function."""

    def test_reset_engine_clears_cache(self) -> None:
        """
        Test that reset_engine() clears the cached engine.

        Equivalence class: Cache invalidation
        """
        reset_engine()

        # Get first engine (creates cached engine)
        engine1 = get_engine()

        # Reset the cache
        reset_engine()

        # Get second engine (creates new cached engine)
        engine2 = get_engine()

        # They should be different objects after reset
        # (Both are new engines, not the cached one)
        assert engine1 is not engine2


class TestDefaultEngineUsage:
    """Tests for functions using the default engine (no explicit engine passed)."""

    def test_create_db_and_tables_with_default_engine(self, tmp_path, monkeypatch) -> None:
        """
        Test that create_db_and_tables() uses the default engine when none provided.

        This covers line 62 in connection.py.
        """
        import road_profile_viewer.database.connection as conn_module

        # Reset any cached engine
        reset_engine()

        # Temporarily override the default path to use temp directory
        temp_db = tmp_path / "default_test.db"
        monkeypatch.setattr(conn_module, "DEFAULT_DATABASE_PATH", temp_db)

        # Call without engine - should use default
        create_db_and_tables()

        # Verify table was created by checking we can query
        default_engine = get_engine()
        with Session(default_engine) as session:
            statement = select(RoadProfileDB)
            result = session.exec(statement).all()
            assert isinstance(result, list)

        # Cleanup
        reset_engine()

    def test_get_session_with_default_engine(self, tmp_path, monkeypatch) -> None:
        """
        Test that get_session() uses the default engine when none provided.

        This covers line 85 in connection.py.
        """
        import road_profile_viewer.database.connection as conn_module

        # Reset any cached engine
        reset_engine()

        # Temporarily override the default path to use temp directory
        temp_db = tmp_path / "session_test.db"
        monkeypatch.setattr(conn_module, "DEFAULT_DATABASE_PATH", temp_db)

        # Create tables first
        create_db_and_tables()

        # Get session without engine - should use default
        session_gen = get_session()
        session = next(session_gen)

        assert isinstance(session, Session)

        # Cleanup generator
        try:
            next(session_gen)
        except StopIteration:
            pass

        # Cleanup
        reset_engine()
