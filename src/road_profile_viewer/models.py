"""
Pydantic Models for Road Profile Data Validation
==================================================

⚠️ IMPORTANT: This is a STARTER SUGGESTION, not a requirement!
---------------------------------------------------------------

You are COMPLETELY FREE to:
- Design your own Pydantic models from scratch
- Modify this structure to fit your architecture
- Use different field names or validation approaches
- Add or remove validators as needed

REMEMBER TO MOVE THIS FILE:
---------------------------
This file must be relocated based on your chosen architecture:

FastAPI approach:
  src/road_profile_viewer/models.py (for validation)
  src/road_profile_viewer/database/models.py (for SQLModel)

TinyDB approach:
  src/road_profile_viewer/models.py (can stay here)
  OR move to: src/road_profile_viewer/database/models.py

The structure below is ONE possible implementation. Feel free to improve it!
"""

from pydantic import BaseModel, Field, field_validator


class RoadProfile(BaseModel):
    """
    Road profile data model for JSON file validation.

    This model ensures that uploaded road profile data meets the required format
    and constraints before being saved to the database.

    Attributes:
        name: Unique identifier for the road profile (1-100 characters)
        x_coordinates: List of x-axis coordinates (floats, at least 2 points)
        y_coordinates: List of y-axis coordinates (floats, same length as x_coordinates)

    Example JSON:
        {
            "name": "mountain_road",
            "x_coordinates": [0.0, 10.0, 20.0, 30.0],
            "y_coordinates": [0.0, 2.5, 5.0, 3.5]
        }
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique name for the road profile",
        examples=["mountain_road", "highway_profile", "test_track"],
    )

    x_coordinates: list[float] = Field(
        ...,
        min_length=2,
        description="List of x-axis coordinates (at least 2 points required)",
        examples=[[0.0, 10.0, 20.0, 30.0]],
    )

    y_coordinates: list[float] = Field(
        ...,
        min_length=2,
        description="List of y-axis coordinates (must match length of x_coordinates)",
        examples=[[0.0, 2.5, 5.0, 3.5]],
    )

    @field_validator("x_coordinates", "y_coordinates")
    @classmethod
    def validate_coordinates_not_empty(cls, v: list[float]) -> list[float]:
        """
        Ensure coordinate lists contain at least 2 points.

        Args:
            v: List of coordinates to validate

        Returns:
            The validated list

        Raises:
            ValueError: If list contains fewer than 2 points
        """
        if len(v) < 2:
            raise ValueError("Coordinate lists must contain at least 2 points")
        return v

    @field_validator("y_coordinates")
    @classmethod
    def validate_coordinates_same_length(cls, v: list[float], info) -> list[float]:
        """
        Ensure x and y coordinate lists have the same length.

        Args:
            v: The y_coordinates list being validated
            info: Validation context containing other field values

        Returns:
            The validated y_coordinates list

        Raises:
            ValueError: If x and y coordinate lists have different lengths
        """
        # Access x_coordinates from the validation context
        if "x_coordinates" in info.data:
            x_coords = info.data["x_coordinates"]
            if len(v) != len(x_coords):
                raise ValueError(
                    f"x_coordinates and y_coordinates must have the same length. Got x={len(x_coords)}, y={len(v)}"
                )
        return v

    @field_validator("name")
    @classmethod
    def validate_name_not_only_whitespace(cls, v: str) -> str:
        """
        Ensure name is not just whitespace.

        Args:
            v: The name string to validate

        Returns:
            The validated and stripped name

        Raises:
            ValueError: If name is only whitespace
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError("Profile name cannot be empty or only whitespace")
        return stripped

    # TODO (Students): Add additional validators as needed
    # Examples:
    # - Validate that coordinates are not all the same (monotonic check)
    # - Validate reasonable coordinate ranges
    # - Check for NaN or infinity values
    # - Validate name doesn't contain special characters (if needed)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "mountain_road",
                    "x_coordinates": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0],
                    "y_coordinates": [0.0, 2.5, 5.0, 7.5, 5.0, 2.0],
                },
                {
                    "name": "flat_highway",
                    "x_coordinates": [0.0, 25.0, 50.0, 75.0, 100.0],
                    "y_coordinates": [0.0, 0.1, 0.0, -0.1, 0.0],
                },
            ]
        }
    }


# TODO (Students): Add additional models if needed
# Examples:
# - RoadProfileCreate (for API POST requests)
# - RoadProfileUpdate (for API PUT/PATCH requests)
# - RoadProfileResponse (for API GET responses with additional metadata)


class RoadProfileCreate(BaseModel):
    """
    Model for creating a new road profile.

    This is used when uploading a new profile via the API or upload page.
    Inherits all validation from RoadProfile.
    """

    # TODO: Decide if this should be different from RoadProfile
    # Currently, they're the same, but you might want different validation
    # or additional fields for creation (e.g., created_by, tags, etc.)
    pass


class RoadProfileResponse(RoadProfile):
    """
    Model for road profile responses from the API.

    Extends RoadProfile with additional metadata fields that are
    generated by the system (e.g., ID, timestamps).
    """

    id: int = Field(..., description="Unique database ID")
    # TODO (Students): Add additional response fields as needed
    # Examples:
    # created_at: datetime
    # updated_at: datetime
    # point_count: int (computed from len(x_coordinates))

    model_config = {
        "from_attributes": True,  # Allow creation from SQLModel objects
    }
