"""
Unit Tests for API Routes
=========================
Test coverage for FastAPI REST endpoints.

Test Coverage:
- GET /profiles: List all profiles
- POST /profiles: Create profile
- GET /profiles/{id}: Get profile by ID
- PUT /profiles/{id}: Update profile
- DELETE /profiles/{id}: Delete profile
- Error cases: 404, 409, 422
- Dependencies: get_db function
"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, create_engine

from road_profile_viewer.api.dependencies import get_db
from road_profile_viewer.api.main import app
from road_profile_viewer.database.models import RoadProfileDB  # noqa: F401 - Required for table creation


@pytest.fixture
def test_db_path(tmp_path):
    """Create a temporary database file path."""
    return tmp_path / "test.db"


@pytest.fixture
def test_engine(test_db_path):
    """Create a test database engine with a file-based SQLite database."""
    engine = create_engine(f"sqlite:///{test_db_path}", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def client(test_engine):
    """Create a test client with overridden database dependency."""

    def override_get_db():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_profile_data():
    """Sample valid profile data."""
    return {
        "name": "test_profile",
        "x_coordinates": [0.0, 10.0, 20.0, 30.0],
        "y_coordinates": [0.0, 2.5, 5.0, 3.5],
    }


@pytest.mark.requirement("FR-007")
class TestRootEndpoint:
    """Tests for the root endpoint.

    Requirement: FR-007 - Provide REST API for profile management
    """

    def test_root_returns_api_info(self, client) -> None:
        """Test that root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "profiles" in data


@pytest.mark.requirement("FR-007")
class TestHealthEndpoint:
    """Tests for the health check endpoint.

    Requirement: FR-007 - Provide REST API for profile management
    """

    def test_health_check_returns_healthy(self, client) -> None:
        """Test that health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.requirement("FR-007")
@pytest.mark.requirement("REQ-API-001")
class TestListProfiles:
    """Tests for GET /profiles endpoint.

    Requirements:
    - FR-007: Provide REST API for profile management
    - REQ-API-001: GET /profiles shall return list of all profiles
    """

    def test_list_profiles_empty(self, client) -> None:
        """Test listing profiles when database is empty."""
        response = client.get("/profiles")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_profiles_with_data(self, client, sample_profile_data) -> None:
        """Test listing profiles with data."""
        # Create a profile first
        client.post("/profiles", json=sample_profile_data)

        response = client.get("/profiles")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == sample_profile_data["name"]

    def test_list_profiles_multiple(self, client) -> None:
        """Test listing multiple profiles."""
        profiles = [
            {"name": "profile1", "x_coordinates": [0.0, 1.0], "y_coordinates": [0.0, 1.0]},
            {"name": "profile2", "x_coordinates": [0.0, 2.0], "y_coordinates": [0.0, 2.0]},
            {"name": "profile3", "x_coordinates": [0.0, 3.0], "y_coordinates": [0.0, 3.0]},
        ]

        for profile in profiles:
            client.post("/profiles", json=profile)

        response = client.get("/profiles")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3


@pytest.mark.requirement("FR-007")
@pytest.mark.requirement("REQ-API-002")
class TestCreateProfile:
    """Tests for POST /profiles endpoint.

    Requirements:
    - FR-007: Provide REST API for profile management
    - REQ-API-002: POST /profiles shall create profile and return 201
    """

    def test_create_profile_success(self, client, sample_profile_data) -> None:
        """Test creating a valid profile."""
        response = client.post("/profiles", json=sample_profile_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_profile_data["name"]
        assert data["x_coordinates"] == sample_profile_data["x_coordinates"]
        assert data["y_coordinates"] == sample_profile_data["y_coordinates"]
        assert "id" in data

    def test_create_profile_returns_id(self, client, sample_profile_data) -> None:
        """Test that created profile has an ID."""
        response = client.post("/profiles", json=sample_profile_data)
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["id"] > 0

    @pytest.mark.requirement("REQ-API-006")
    @pytest.mark.requirement("NFR-006")
    def test_create_profile_duplicate_name_conflict(self, client, sample_profile_data) -> None:
        """Test that duplicate name returns 409 Conflict.

        Requirements:
        - REQ-API-006: Duplicate profile names shall return 409 Conflict
        - NFR-006: Profile names shall be unique
        """
        # Create first profile
        client.post("/profiles", json=sample_profile_data)

        # Try to create duplicate
        response = client.post("/profiles", json=sample_profile_data)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    @pytest.mark.requirement("FR-008")
    def test_create_profile_invalid_coordinates_length(self, client) -> None:
        """Test that mismatched coordinates return 422.

        Requirement: FR-008 - Validate profile data before storage
        """
        invalid_data = {
            "name": "invalid",
            "x_coordinates": [0.0, 1.0, 2.0],
            "y_coordinates": [0.0, 1.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422

    @pytest.mark.requirement("FR-008")
    def test_create_profile_too_few_points(self, client) -> None:
        """Test that fewer than 2 points returns 422.

        Requirement: FR-008 - Validate profile data before storage
        """
        invalid_data = {
            "name": "invalid",
            "x_coordinates": [0.0],
            "y_coordinates": [0.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422

    @pytest.mark.requirement("FR-008")
    def test_create_profile_empty_name(self, client) -> None:
        """Test that empty name returns 422.

        Requirement: FR-008 - Validate profile data before storage
        """
        invalid_data = {
            "name": "",
            "x_coordinates": [0.0, 1.0],
            "y_coordinates": [0.0, 1.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422

    @pytest.mark.requirement("FR-008")
    def test_create_profile_whitespace_name(self, client) -> None:
        """Test that whitespace-only name returns 422.

        Requirement: FR-008 - Validate profile data before storage
        """
        invalid_data = {
            "name": "   ",
            "x_coordinates": [0.0, 1.0],
            "y_coordinates": [0.0, 1.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422

    @pytest.mark.requirement("FR-008")
    def test_create_profile_name_too_long(self, client) -> None:
        """Test that name over 100 chars returns 422.

        Requirement: FR-008 - Validate profile data before storage
        """
        invalid_data = {
            "name": "a" * 101,
            "x_coordinates": [0.0, 1.0],
            "y_coordinates": [0.0, 1.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422


@pytest.mark.requirement("FR-007")
@pytest.mark.requirement("REQ-API-003")
class TestGetProfile:
    """Tests for GET /profiles/{id} endpoint.

    Requirements:
    - FR-007: Provide REST API for profile management
    - REQ-API-003: GET /profiles/{id} shall return profile or 404
    """

    def test_get_profile_success(self, client, sample_profile_data) -> None:
        """Test getting an existing profile by ID."""
        # Create a profile
        create_response = client.post("/profiles", json=sample_profile_data)
        profile_id = create_response.json()["id"]

        response = client.get(f"/profiles/{profile_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == profile_id
        assert data["name"] == sample_profile_data["name"]

    def test_get_profile_not_found(self, client) -> None:
        """Test getting a nonexistent profile returns 404."""
        response = client.get("/profiles/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_get_profile_invalid_id(self, client) -> None:
        """Test getting with invalid ID returns 422."""
        response = client.get("/profiles/invalid")
        assert response.status_code == 422


@pytest.mark.requirement("FR-007")
@pytest.mark.requirement("REQ-API-004")
class TestUpdateProfile:
    """Tests for PUT /profiles/{id} endpoint.

    Requirements:
    - FR-007: Provide REST API for profile management
    - REQ-API-004: PUT /profiles/{id} shall update profile or return 404/409
    """

    def test_update_profile_success(self, client, sample_profile_data) -> None:
        """Test updating an existing profile."""
        # Create a profile
        create_response = client.post("/profiles", json=sample_profile_data)
        profile_id = create_response.json()["id"]

        # Update it
        updated_data = {
            "name": "updated_profile",
            "x_coordinates": [0.0, 5.0, 10.0],
            "y_coordinates": [0.0, 2.0, 4.0],
        }
        response = client.put(f"/profiles/{profile_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "updated_profile"
        assert data["x_coordinates"] == [0.0, 5.0, 10.0]

    def test_update_profile_not_found(self, client, sample_profile_data) -> None:
        """Test updating a nonexistent profile returns 404."""
        response = client.put("/profiles/9999", json=sample_profile_data)
        assert response.status_code == 404

    def test_update_profile_name_conflict(self, client) -> None:
        """Test updating to an existing name returns 409."""
        # Create two profiles
        profile1 = {"name": "profile1", "x_coordinates": [0.0, 1.0], "y_coordinates": [0.0, 1.0]}
        profile2 = {"name": "profile2", "x_coordinates": [0.0, 2.0], "y_coordinates": [0.0, 2.0]}

        client.post("/profiles", json=profile1)
        create2_response = client.post("/profiles", json=profile2)
        profile2_id = create2_response.json()["id"]

        # Try to rename profile2 to profile1
        updated_data = {"name": "profile1", "x_coordinates": [0.0, 2.0], "y_coordinates": [0.0, 2.0]}
        response = client.put(f"/profiles/{profile2_id}", json=updated_data)
        assert response.status_code == 409

    def test_update_profile_same_name_allowed(self, client, sample_profile_data) -> None:
        """Test updating without changing name is allowed."""
        # Create a profile
        create_response = client.post("/profiles", json=sample_profile_data)
        profile_id = create_response.json()["id"]

        # Update with same name but different coordinates
        updated_data = {
            "name": sample_profile_data["name"],  # Same name
            "x_coordinates": [0.0, 5.0, 10.0],
            "y_coordinates": [0.0, 2.0, 4.0],
        }
        response = client.put(f"/profiles/{profile_id}", json=updated_data)
        assert response.status_code == 200


@pytest.mark.requirement("FR-007")
@pytest.mark.requirement("REQ-API-005")
class TestDeleteProfile:
    """Tests for DELETE /profiles/{id} endpoint.

    Requirements:
    - FR-007: Provide REST API for profile management
    - REQ-API-005: DELETE /profiles/{id} shall delete profile and return 204
    """

    def test_delete_profile_success(self, client, sample_profile_data) -> None:
        """Test deleting an existing profile."""
        # Create a profile
        create_response = client.post("/profiles", json=sample_profile_data)
        profile_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/profiles/{profile_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/profiles/{profile_id}")
        assert get_response.status_code == 404

    def test_delete_profile_not_found(self, client) -> None:
        """Test deleting a nonexistent profile returns 404."""
        response = client.delete("/profiles/9999")
        assert response.status_code == 404

    def test_delete_profile_does_not_affect_others(self, client) -> None:
        """Test deleting one profile doesn't affect others."""
        # Create multiple profiles
        profiles = [
            {"name": "keep1", "x_coordinates": [0.0, 1.0], "y_coordinates": [0.0, 1.0]},
            {"name": "delete_me", "x_coordinates": [0.0, 2.0], "y_coordinates": [0.0, 2.0]},
            {"name": "keep2", "x_coordinates": [0.0, 3.0], "y_coordinates": [0.0, 3.0]},
        ]

        ids = []
        for profile in profiles:
            response = client.post("/profiles", json=profile)
            ids.append(response.json()["id"])

        # Delete the middle one
        client.delete(f"/profiles/{ids[1]}")

        # Others should still exist
        assert client.get(f"/profiles/{ids[0]}").status_code == 200
        assert client.get(f"/profiles/{ids[2]}").status_code == 200

        # List should have 2 profiles
        list_response = client.get("/profiles")
        assert len(list_response.json()) == 2


@pytest.mark.requirement("FR-006")
class TestGetDbDependency:
    """Tests for the get_db dependency function.

    Requirement: FR-006 - Persist profiles in database
    """

    def test_get_db_yields_session(self, test_engine) -> None:
        """Test that get_db yields a database session."""
        with patch("road_profile_viewer.api.dependencies.get_engine", return_value=test_engine):
            gen = get_db()
            session = next(gen)
            assert isinstance(session, Session)
            # Clean up generator
            try:
                next(gen)
            except StopIteration:
                pass

    def test_get_db_session_is_usable(self, test_engine) -> None:
        """Test that the yielded session can be used for queries."""
        with patch("road_profile_viewer.api.dependencies.get_engine", return_value=test_engine):
            gen = get_db()
            session = next(gen)
            # Should be able to execute queries
            from road_profile_viewer.database import crud

            profiles = crud.get_all_profiles(session)
            assert isinstance(profiles, list)
            # Clean up generator
            try:
                next(gen)
            except StopIteration:
                pass


@pytest.mark.requirement("REQ-API-007")
@pytest.mark.requirement("NFR-006")
class TestIntegrityErrorHandling:
    """Tests for IntegrityError handling in routes (race condition paths).

    Requirements:
    - REQ-API-007: IntegrityError race conditions shall return 409
    - NFR-006: Profile names shall be unique
    """

    def test_create_profile_integrity_error_race_condition(self, client, test_engine) -> None:
        """Test that IntegrityError during create returns 409."""
        # Mock create_profile to raise IntegrityError (simulating race condition)
        with patch("road_profile_viewer.api.routes.crud.create_profile") as mock_create:
            mock_create.side_effect = IntegrityError(
                statement="INSERT",
                params={},
                orig=Exception("UNIQUE constraint failed"),
            )
            # Also mock get_profile_by_name to return None (check passes)
            with patch("road_profile_viewer.api.routes.crud.get_profile_by_name") as mock_get:
                mock_get.return_value = None

                profile_data = {
                    "name": "race_condition_test",
                    "x_coordinates": [0.0, 1.0],
                    "y_coordinates": [0.0, 1.0],
                }
                response = client.post("/profiles", json=profile_data)

                # Should return 409 Conflict
                assert response.status_code == 409
                assert "already exists" in response.json()["detail"]

    def test_update_profile_integrity_error_race_condition(self, client, sample_profile_data) -> None:
        """Test that IntegrityError during update returns 409."""
        # First create a profile
        create_response = client.post("/profiles", json=sample_profile_data)
        profile_id = create_response.json()["id"]

        # Mock update_profile to raise IntegrityError
        with patch("road_profile_viewer.api.routes.crud.update_profile") as mock_update:
            mock_update.side_effect = IntegrityError(
                statement="UPDATE",
                params={},
                orig=Exception("UNIQUE constraint failed"),
            )

            updated_data = {
                "name": "race_name",
                "x_coordinates": [0.0, 1.0],
                "y_coordinates": [0.0, 1.0],
            }
            response = client.put(f"/profiles/{profile_id}", json=updated_data)

            # Should return 409 Conflict
            assert response.status_code == 409
            assert "already exists" in response.json()["detail"]

    def test_update_profile_returns_none_race_condition(self, client, sample_profile_data) -> None:
        """Test when update_profile returns None (profile deleted during update)."""
        # First create a profile
        create_response = client.post("/profiles", json=sample_profile_data)
        profile_id = create_response.json()["id"]

        # Mock update_profile to return None (profile was deleted)
        with patch("road_profile_viewer.api.routes.crud.update_profile") as mock_update:
            mock_update.return_value = None

            updated_data = {
                "name": sample_profile_data["name"],
                "x_coordinates": [0.0, 1.0],
                "y_coordinates": [0.0, 1.0],
            }
            response = client.put(f"/profiles/{profile_id}", json=updated_data)

            # Should return 404 Not Found
            assert response.status_code == 404
            assert "not found" in response.json()["detail"]
