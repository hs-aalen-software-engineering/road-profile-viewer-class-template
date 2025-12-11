"""
Unit Tests for Database Models
==============================
Test coverage for SQLModel database models.

Test Coverage:
- RoadProfileDB: Field types, constraints, serialization methods
"""

import json

from road_profile_viewer.database.models import RoadProfileDB


class TestRoadProfileDB:
    """Tests for the RoadProfileDB SQLModel."""

    def test_create_profile_with_all_fields(self) -> None:
        """
        Test that RoadProfileDB can be instantiated with all fields.

        Equivalence class: Valid profile with all required fields
        """
        profile = RoadProfileDB(
            id=1,
            name="test_profile",
            x_coordinates=json.dumps([0.0, 10.0, 20.0]),
            y_coordinates=json.dumps([0.0, 2.5, 5.0]),
        )

        assert profile.id == 1
        assert profile.name == "test_profile"
        assert profile.x_coordinates == json.dumps([0.0, 10.0, 20.0])
        assert profile.y_coordinates == json.dumps([0.0, 2.5, 5.0])

    def test_create_profile_without_id(self) -> None:
        """
        Test that RoadProfileDB can be created without an ID (auto-generated).

        Equivalence class: Profile creation before database insertion
        """
        profile = RoadProfileDB(
            name="test_profile",
            x_coordinates=json.dumps([0.0, 10.0]),
            y_coordinates=json.dumps([0.0, 2.0]),
        )

        assert profile.id is None
        assert profile.name == "test_profile"

    def test_get_x_coordinates_deserializes_json(self) -> None:
        """
        Test that get_x_coordinates() properly deserializes JSON to list.

        Equivalence class: Coordinate deserialization
        """
        coords = [0.0, 10.0, 20.0, 30.0]
        profile = RoadProfileDB(
            name="test",
            x_coordinates=json.dumps(coords),
            y_coordinates=json.dumps([0.0, 1.0, 2.0, 3.0]),
        )

        result = profile.get_x_coordinates()

        assert result == coords
        assert isinstance(result, list)
        assert all(isinstance(x, float) for x in result)

    def test_get_y_coordinates_deserializes_json(self) -> None:
        """
        Test that get_y_coordinates() properly deserializes JSON to list.

        Equivalence class: Coordinate deserialization
        """
        coords = [0.0, 2.5, 5.0, 3.5]
        profile = RoadProfileDB(
            name="test",
            x_coordinates=json.dumps([0.0, 10.0, 20.0, 30.0]),
            y_coordinates=json.dumps(coords),
        )

        result = profile.get_y_coordinates()

        assert result == coords
        assert isinstance(result, list)

    def test_from_coordinates_class_method(self) -> None:
        """
        Test that from_coordinates() creates a profile with serialized coordinates.

        Equivalence class: Factory method for profile creation
        """
        x_coords = [0.0, 10.0, 20.0]
        y_coords = [0.0, 2.5, 5.0]

        profile = RoadProfileDB.from_coordinates("my_profile", x_coords, y_coords)

        assert profile.name == "my_profile"
        assert profile.get_x_coordinates() == x_coords
        assert profile.get_y_coordinates() == y_coords
        assert profile.id is None  # Not yet persisted

    def test_from_coordinates_roundtrip(self) -> None:
        """
        Test that coordinates survive a round-trip through serialization.

        Equivalence class: Data integrity through serialization
        """
        x_coords = [0.0, 5.5, 11.2, 22.7, 45.0]
        y_coords = [0.0, 1.1, 2.3, 4.6, 9.2]

        profile = RoadProfileDB.from_coordinates("roundtrip", x_coords, y_coords)

        assert profile.get_x_coordinates() == x_coords
        assert profile.get_y_coordinates() == y_coords

    def test_empty_coordinates(self) -> None:
        """
        Test that empty coordinate lists can be stored and retrieved.

        Boundary value: Empty lists (edge case)
        Note: Validation should prevent this in production, but the model allows it.
        """
        profile = RoadProfileDB.from_coordinates("empty", [], [])

        assert profile.get_x_coordinates() == []
        assert profile.get_y_coordinates() == []

    def test_single_point_coordinates(self) -> None:
        """
        Test that single-point coordinate lists can be stored and retrieved.

        Boundary value: Single point (minimum minus one for validation)
        """
        profile = RoadProfileDB.from_coordinates("single", [5.0], [2.0])

        assert profile.get_x_coordinates() == [5.0]
        assert profile.get_y_coordinates() == [2.0]

    def test_large_coordinate_lists(self) -> None:
        """
        Test that large coordinate lists can be stored and retrieved.

        Boundary value: Large dataset (stress test)
        """
        x_coords = [float(i) for i in range(1000)]
        y_coords = [float(i) * 0.1 for i in range(1000)]

        profile = RoadProfileDB.from_coordinates("large", x_coords, y_coords)

        assert len(profile.get_x_coordinates()) == 1000
        assert len(profile.get_y_coordinates()) == 1000
        assert profile.get_x_coordinates() == x_coords
        assert profile.get_y_coordinates() == y_coords

    def test_negative_coordinates(self) -> None:
        """
        Test that negative coordinate values are handled correctly.

        Equivalence class: Negative values
        """
        x_coords = [-10.0, -5.0, 0.0, 5.0, 10.0]
        y_coords = [-2.0, -1.0, 0.0, 1.0, 2.0]

        profile = RoadProfileDB.from_coordinates("negative", x_coords, y_coords)

        assert profile.get_x_coordinates() == x_coords
        assert profile.get_y_coordinates() == y_coords

    def test_float_precision(self) -> None:
        """
        Test that float precision is maintained through serialization.

        Equivalence class: Floating point precision
        """
        x_coords = [0.123456789, 1.987654321]
        y_coords = [0.111111111, 2.222222222]

        profile = RoadProfileDB.from_coordinates("precision", x_coords, y_coords)

        # JSON maintains reasonable float precision
        retrieved_x = profile.get_x_coordinates()
        retrieved_y = profile.get_y_coordinates()

        assert abs(retrieved_x[0] - x_coords[0]) < 1e-9
        assert abs(retrieved_x[1] - x_coords[1]) < 1e-9
        assert abs(retrieved_y[0] - y_coords[0]) < 1e-9
        assert abs(retrieved_y[1] - y_coords[1]) < 1e-9
