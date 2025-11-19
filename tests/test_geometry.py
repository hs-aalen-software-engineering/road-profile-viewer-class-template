"""
Unit Tests for Geometry Module
================================
This module contains unit tests for the geometric calculation functions
in the geometry module, specifically testing the find_intersection function.
"""

import sys
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from road_profile_viewer.geometry import find_intersection


def test_find_intersection_finds_intersection_for_normal_angle() -> None:
    """
    Test that find_intersection() returns a valid intersection
    for a normal downward angle with a simple road profile.

    Equivalence class: Normal downward angles (-90° < angle < 0°)
    """
    # Arrange: Create simple road going upward
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 2, 4, 6], dtype=np.float64)
    angle: float = 10.0  # Downward angle (positive = downward from horizontal)
    camera_x: float = 0.0
    camera_y: float = 10.0  # Camera above road

    # Act: Find intersection
    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Assert: Should find an intersection
    assert x is not None, "x coordinate should not be None"
    assert y is not None, "y coordinate should not be None"
    assert dist is not None, "distance should not be None"
    assert dist > 0, "distance should be positive"
    assert 0 <= x <= 30, "intersection x should be within road bounds"


if __name__ == "__main__":
    # Allow running tests directly
    print("Running geometry unit tests...")
    print()

    test_find_intersection_finds_intersection_for_normal_angle()

    print()
    print("✅ All geometry tests passed!")
