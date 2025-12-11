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
"""

import pytest
from fastapi.testclient import TestClient
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


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_api_info(self, client) -> None:
        """Test that root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "profiles" in data


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_healthy(self, client) -> None:
        """Test that health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestListProfiles:
    """Tests for GET /profiles endpoint."""

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


class TestCreateProfile:
    """Tests for POST /profiles endpoint."""

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

    def test_create_profile_duplicate_name_conflict(self, client, sample_profile_data) -> None:
        """Test that duplicate name returns 409 Conflict."""
        # Create first profile
        client.post("/profiles", json=sample_profile_data)

        # Try to create duplicate
        response = client.post("/profiles", json=sample_profile_data)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_create_profile_invalid_coordinates_length(self, client) -> None:
        """Test that mismatched coordinates return 422."""
        invalid_data = {
            "name": "invalid",
            "x_coordinates": [0.0, 1.0, 2.0],
            "y_coordinates": [0.0, 1.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422

    def test_create_profile_too_few_points(self, client) -> None:
        """Test that fewer than 2 points returns 422."""
        invalid_data = {
            "name": "invalid",
            "x_coordinates": [0.0],
            "y_coordinates": [0.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422

    def test_create_profile_empty_name(self, client) -> None:
        """Test that empty name returns 422."""
        invalid_data = {
            "name": "",
            "x_coordinates": [0.0, 1.0],
            "y_coordinates": [0.0, 1.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422

    def test_create_profile_whitespace_name(self, client) -> None:
        """Test that whitespace-only name returns 422."""
        invalid_data = {
            "name": "   ",
            "x_coordinates": [0.0, 1.0],
            "y_coordinates": [0.0, 1.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422

    def test_create_profile_name_too_long(self, client) -> None:
        """Test that name over 100 chars returns 422."""
        invalid_data = {
            "name": "a" * 101,
            "x_coordinates": [0.0, 1.0],
            "y_coordinates": [0.0, 1.0],
        }
        response = client.post("/profiles", json=invalid_data)
        assert response.status_code == 422


class TestGetProfile:
    """Tests for GET /profiles/{id} endpoint."""

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


class TestUpdateProfile:
    """Tests for PUT /profiles/{id} endpoint."""

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


class TestDeleteProfile:
    """Tests for DELETE /profiles/{id} endpoint."""

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
