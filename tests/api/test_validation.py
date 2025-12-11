"""
Unit Tests for Pydantic Validation
==================================
Test coverage for Pydantic model validation.

Test Coverage:
- RoadProfile: Valid and invalid inputs
- RoadProfileResponse: Response model with ID
- Edge cases and boundary values
"""

import pytest
from pydantic import ValidationError

from road_profile_viewer.models import RoadProfile, RoadProfileResponse


class TestRoadProfileValidation:
    """Tests for RoadProfile Pydantic model validation."""

    def test_valid_profile(self) -> None:
        """Test that valid profile data passes validation."""
        profile = RoadProfile(
            name="valid_profile",
            x_coordinates=[0.0, 10.0, 20.0],
            y_coordinates=[0.0, 2.5, 5.0],
        )
        assert profile.name == "valid_profile"
        assert profile.x_coordinates == [0.0, 10.0, 20.0]
        assert profile.y_coordinates == [0.0, 2.5, 5.0]

    def test_valid_profile_min_points(self) -> None:
        """Test minimum valid profile (2 points)."""
        profile = RoadProfile(
            name="min_profile",
            x_coordinates=[0.0, 1.0],
            y_coordinates=[0.0, 1.0],
        )
        assert len(profile.x_coordinates) == 2

    def test_valid_profile_max_name_length(self) -> None:
        """Test maximum name length (100 chars)."""
        name = "a" * 100
        profile = RoadProfile(
            name=name,
            x_coordinates=[0.0, 1.0],
            y_coordinates=[0.0, 1.0],
        )
        assert len(profile.name) == 100

    def test_invalid_empty_name(self) -> None:
        """Test that empty name fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            RoadProfile(
                name="",
                x_coordinates=[0.0, 1.0],
                y_coordinates=[0.0, 1.0],
            )
        assert "too_short" in str(exc_info.value) or "at least 1" in str(exc_info.value)

    def test_invalid_whitespace_name(self) -> None:
        """Test that whitespace-only name fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            RoadProfile(
                name="   ",
                x_coordinates=[0.0, 1.0],
                y_coordinates=[0.0, 1.0],
            )
        assert "empty or only whitespace" in str(exc_info.value)

    def test_invalid_name_too_long(self) -> None:
        """Test that name over 100 chars fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            RoadProfile(
                name="a" * 101,
                x_coordinates=[0.0, 1.0],
                y_coordinates=[0.0, 1.0],
            )
        assert "too_long" in str(exc_info.value) or "at most 100" in str(exc_info.value)

    def test_invalid_single_point(self) -> None:
        """Test that single point fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            RoadProfile(
                name="single_point",
                x_coordinates=[0.0],
                y_coordinates=[0.0],
            )
        assert "too_short" in str(exc_info.value) or "at least 2" in str(exc_info.value)

    def test_invalid_empty_coordinates(self) -> None:
        """Test that empty coordinates fail validation."""
        with pytest.raises(ValidationError) as exc_info:
            RoadProfile(
                name="empty_coords",
                x_coordinates=[],
                y_coordinates=[],
            )
        assert "too_short" in str(exc_info.value) or "at least 2" in str(exc_info.value)

    def test_invalid_mismatched_lengths(self) -> None:
        """Test that mismatched coordinate lengths fail validation."""
        with pytest.raises(ValidationError) as exc_info:
            RoadProfile(
                name="mismatched",
                x_coordinates=[0.0, 1.0, 2.0],
                y_coordinates=[0.0, 1.0],
            )
        assert "same length" in str(exc_info.value)

    def test_name_gets_stripped(self) -> None:
        """Test that name with leading/trailing whitespace gets stripped."""
        profile = RoadProfile(
            name="  trimmed  ",
            x_coordinates=[0.0, 1.0],
            y_coordinates=[0.0, 1.0],
        )
        assert profile.name == "trimmed"

    def test_valid_negative_coordinates(self) -> None:
        """Test that negative coordinates are valid."""
        profile = RoadProfile(
            name="negative",
            x_coordinates=[-10.0, -5.0, 0.0, 5.0],
            y_coordinates=[-2.0, -1.0, 0.0, 1.0],
        )
        assert profile.x_coordinates[0] == -10.0
        assert profile.y_coordinates[0] == -2.0

    def test_valid_float_precision(self) -> None:
        """Test that float precision is maintained."""
        profile = RoadProfile(
            name="precision",
            x_coordinates=[0.123456789, 1.987654321],
            y_coordinates=[0.111111111, 2.222222222],
        )
        assert abs(profile.x_coordinates[0] - 0.123456789) < 1e-9

    def test_valid_large_coordinates(self) -> None:
        """Test that large coordinate lists are valid."""
        x_coords = [float(i) for i in range(100)]
        y_coords = [float(i) * 0.1 for i in range(100)]

        profile = RoadProfile(
            name="large",
            x_coordinates=x_coords,
            y_coordinates=y_coords,
        )
        assert len(profile.x_coordinates) == 100


class TestRoadProfileResponse:
    """Tests for RoadProfileResponse Pydantic model."""

    def test_valid_response(self) -> None:
        """Test that valid response data passes validation."""
        response = RoadProfileResponse(
            id=1,
            name="response_profile",
            x_coordinates=[0.0, 10.0, 20.0],
            y_coordinates=[0.0, 2.5, 5.0],
        )
        assert response.id == 1
        assert response.name == "response_profile"

    def test_response_inherits_validation(self) -> None:
        """Test that response inherits RoadProfile validation."""
        with pytest.raises(ValidationError):
            RoadProfileResponse(
                id=1,
                name="",
                x_coordinates=[0.0, 1.0],
                y_coordinates=[0.0, 1.0],
            )

    def test_response_requires_id(self) -> None:
        """Test that response requires an ID."""
        with pytest.raises(ValidationError):
            RoadProfileResponse(
                name="no_id",
                x_coordinates=[0.0, 1.0],
                y_coordinates=[0.0, 1.0],
            )

    def test_response_id_must_be_int(self) -> None:
        """Test that response ID must be an integer."""
        with pytest.raises(ValidationError):
            RoadProfileResponse(
                id="not_an_int",  # type: ignore
                name="invalid_id",
                x_coordinates=[0.0, 1.0],
                y_coordinates=[0.0, 1.0],
            )


class TestModelConfig:
    """Tests for Pydantic model configuration."""

    def test_road_profile_has_examples(self) -> None:
        """Test that RoadProfile has JSON schema examples."""
        schema = RoadProfile.model_json_schema()
        assert "examples" in schema

    def test_response_from_attributes(self) -> None:
        """Test that RoadProfileResponse has from_attributes config."""
        config = RoadProfileResponse.model_config
        assert config.get("from_attributes") is True
