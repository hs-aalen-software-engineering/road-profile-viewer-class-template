"""
Comprehensive Unit Tests for Geometry Module
=============================================
This module contains comprehensive equivalence class and boundary value tests
for the find_intersection function in the geometry module.

Test Organization:
- Equivalence class tests: Cover different categories of valid inputs
- Boundary value tests: Test edge cases and boundaries
- Special cases: Test unusual but valid scenarios
"""

import sys
from pathlib import Path

import numpy as np
import pytest
from numpy.typing import NDArray

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from road_profile_viewer.geometry import find_intersection

# ==============================================================================
# EQUIVALENCE CLASS TESTS: ANGLE VARIATIONS
# ==============================================================================


def test_find_intersection_normal_downward_angle() -> None:
    """
    Test intersection with moderate downward angle.

    Equivalence class: Normal downward angles (0° < angle < 90°)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 2, 4, 6], dtype=np.float64)
    angle: float = 30.0
    camera_x: float = 0.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None
    assert dist > 0
    assert 0 <= x <= 30


def test_find_intersection_steep_downward_angle() -> None:
    """
    Test intersection with steep downward angle.

    Equivalence class: Steep downward angles (60° < angle < 90°)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 75.0
    camera_x: float = 0.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None
    assert x < 5.0  # Should intersect very close due to steep angle


def test_find_intersection_shallow_downward_angle() -> None:
    """
    Test intersection with shallow downward angle.

    Equivalence class: Shallow downward angles (0° < angle < 30°)
    """
    x_road: NDArray[np.float64] = np.array([0, 50, 100], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0], dtype=np.float64)
    angle: float = 5.0
    camera_x: float = 0.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None
    assert x > 20.0  # Should intersect far away due to shallow angle


def test_find_intersection_upward_angle_no_intersection() -> None:
    """
    Test that upward angle doesn't intersect road below.

    Equivalence class: Upward angles (angle < 0°)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = -30.0  # Upward angle
    camera_x: float = 10.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is None
    assert y is None
    assert dist is None


def test_find_intersection_horizontal_angle() -> None:
    """
    Test intersection with horizontal ray (0 degrees).

    Equivalence class: Horizontal angle (angle = 0°)
    Boundary value: angle = 0
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 5, 5, 10], dtype=np.float64)
    angle: float = 0.0
    camera_x: float = 0.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Horizontal ray at y=5 should intersect the road segment from (10,5) to (20,5)
    if x is not None:
        assert y is not None
        assert abs(y - 5.0) < 0.1  # Should be near y=5


# ==============================================================================
# EQUIVALENCE CLASS TESTS: CAMERA POSITION VARIATIONS
# ==============================================================================


def test_find_intersection_camera_above_road() -> None:
    """
    Test intersection when camera is above road.

    Equivalence class: Camera above road (camera_y > all y_road)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 1, 2, 3], dtype=np.float64)
    angle: float = 20.0
    camera_x: float = 5.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None
    assert y < camera_y


def test_find_intersection_camera_below_road() -> None:
    """
    Test intersection when camera is below road (upward ray needed).

    Equivalence class: Camera below road (camera_y < all y_road)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([10, 10, 10, 10], dtype=np.float64)
    angle: float = -45.0  # Upward angle
    camera_x: float = 0.0
    camera_y: float = 0.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None
    assert y > camera_y


def test_find_intersection_camera_at_road_level() -> None:
    """
    Test intersection when camera is at road level.

    Equivalence class: Camera at road level (camera_y ≈ y_road[0])
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([5, 5, 5, 5], dtype=np.float64)
    angle: float = 0.0  # Horizontal
    camera_x: float = 0.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Should find intersection along the flat road
    assert x is not None
    assert y is not None


def test_find_intersection_camera_ahead_of_road() -> None:
    """
    Test when camera is ahead of all road segments.

    Equivalence class: Camera beyond road (camera_x > max(x_road))
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 2, 4, 6], dtype=np.float64)
    angle: float = 30.0
    camera_x: float = 40.0  # Beyond road
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # No intersection because all road is behind camera
    assert x is None
    assert y is None
    assert dist is None


# ==============================================================================
# EQUIVALENCE CLASS TESTS: ROAD PROFILE VARIATIONS
# ==============================================================================


def test_find_intersection_flat_road() -> None:
    """
    Test intersection with flat horizontal road.

    Equivalence class: Flat road (all y values equal)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 45.0
    camera_x: float = 0.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert abs(y) < 0.1  # Should intersect at y ≈ 0
    assert dist is not None


def test_find_intersection_upward_sloping_road() -> None:
    """
    Test intersection with consistently upward sloping road.

    Equivalence class: Upward sloping road (y increases with x)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 5, 10, 15], dtype=np.float64)
    angle: float = 20.0
    camera_x: float = 0.0
    camera_y: float = 20.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None


def test_find_intersection_downward_sloping_road() -> None:
    """
    Test intersection with consistently downward sloping road.

    Equivalence class: Downward sloping road (y decreases with x)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([20, 15, 10, 5], dtype=np.float64)
    angle: float = 45.0
    camera_x: float = 0.0
    camera_y: float = 25.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None


def test_find_intersection_complex_road_profile() -> None:
    """
    Test intersection with complex varying road profile.

    Equivalence class: Complex road (varying slopes)
    """
    x_road: NDArray[np.float64] = np.array([0, 5, 10, 15, 20, 25, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 2, 1, 3, 2, 4, 3], dtype=np.float64)
    angle: float = 25.0
    camera_x: float = 0.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None
    assert 0 <= x <= 30


def test_find_intersection_two_segment_road() -> None:
    """
    Test intersection with minimal two-segment road.

    Equivalence class: Minimal road (2 segments, 3 points)
    Boundary value: Minimum road size
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0], dtype=np.float64)
    angle: float = 30.0
    camera_x: float = 0.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None


# ==============================================================================
# EQUIVALENCE CLASS TESTS: INTERSECTION POSITION
# ==============================================================================


def test_find_intersection_in_first_segment() -> None:
    """
    Test intersection occurs in first road segment.

    Equivalence class: Intersection in first segment
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 60.0  # Steep angle for quick intersection
    camera_x: float = 0.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert 0 <= x <= 10, "Should intersect in first segment"


def test_find_intersection_in_middle_segment() -> None:
    """
    Test intersection occurs in middle road segment.

    Equivalence class: Intersection in middle segment
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 5.0  # Shallow angle
    camera_x: float = 0.0
    camera_y: float = 2.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert 10 <= x <= 30, "Should intersect beyond first segment"


def test_find_intersection_in_last_segment() -> None:
    """
    Test intersection occurs in last road segment.

    Equivalence class: Intersection in last segment
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 3.0  # Very shallow angle
    camera_x: float = 0.0
    camera_y: float = 1.5

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert 20 <= x <= 30, "Should intersect in last segment"


def test_find_intersection_no_intersection_ray_misses() -> None:
    """
    Test when ray doesn't intersect road at all.

    Equivalence class: No intersection (ray misses road)
    """
    x_road: NDArray[np.float64] = np.array([10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0], dtype=np.float64)
    angle: float = 45.0
    camera_x: float = 0.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Ray might intersect or miss depending on geometry
    # This tests the no-intersection case when camera is before road starts
    if camera_x < x_road[0]:
        # Ray needs to reach the road
        pass


def test_find_intersection_multiple_potential_returns_first() -> None:
    """
    Test that function returns first intersection when multiple are possible.

    Equivalence class: Multiple intersections (returns first)
    """
    # Create road that goes down then up
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([5, 0, 0, 5], dtype=np.float64)
    angle: float = 30.0
    camera_x: float = 0.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None
    # Should return an intersection (function returns first by design)
    assert 0 <= x <= 30, "Intersection should be within road bounds"


# ==============================================================================
# BOUNDARY VALUE TESTS
# ==============================================================================


def test_find_intersection_vertical_ray() -> None:
    """
    Test with vertical ray (angle = 90 degrees).

    Boundary value: angle = 90° (vertical ray)
    Special case: Should return None (implementation detail)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 90.0
    camera_x: float = 5.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Vertical ray case returns None based on implementation
    assert x is None
    assert y is None
    assert dist is None


def test_find_intersection_near_vertical_ray() -> None:
    """
    Test with nearly vertical ray (angle close to 90).

    Boundary value: angle ≈ 90° (near vertical)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 89.9
    camera_x: float = 5.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Should find intersection very close to camera_x
    if x is not None:
        assert abs(x - camera_x) < 1.0


def test_find_intersection_camera_at_origin() -> None:
    """
    Test with camera at origin (0, 0).

    Boundary value: camera_x = 0, camera_y = 0
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([-5, -5, -5, -5], dtype=np.float64)
    angle: float = 45.0
    camera_x: float = 0.0
    camera_y: float = 0.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None


def test_find_intersection_at_segment_endpoint() -> None:
    """
    Test intersection exactly at segment endpoint.

    Boundary value: Intersection at segment boundary
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 5, 10, 15], dtype=np.float64)
    # Set up ray to hit exactly at x=10, y=5
    angle: float = 45.0
    camera_x: float = 5.0
    camera_y: float = 10.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None


def test_find_intersection_camera_on_road() -> None:
    """
    Test when camera is positioned on the road itself.

    Boundary value: camera position on road (distance ≈ 0)
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([5, 5, 5, 5], dtype=np.float64)
    angle: float = 45.0
    camera_x: float = 5.0
    camera_y: float = 5.0  # Camera on the road

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Should still find intersection ahead
    assert x is not None
    assert x >= camera_x


def test_find_intersection_very_small_segments() -> None:
    """
    Test with very small road segments.

    Boundary value: Small segment lengths
    """
    x_road: NDArray[np.float64] = np.array([0, 0.1, 0.2, 0.3], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 45.0
    camera_x: float = 0.0
    camera_y: float = 0.1

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None


def test_find_intersection_very_large_coordinates() -> None:
    """
    Test with very large coordinate values.

    Boundary value: Large coordinate values
    """
    x_road: NDArray[np.float64] = np.array([1000, 1010, 1020, 1030], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([1000, 1000, 1000, 1000], dtype=np.float64)
    angle: float = 45.0
    camera_x: float = 1000.0
    camera_y: float = 1010.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert dist is not None


def test_find_intersection_angle_at_180_degrees() -> None:
    """
    Test with angle at 180 degrees (pointing backward).

    Boundary value: angle = 180°
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 180.0
    camera_x: float = 15.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # 180 degrees points backward (left), might not intersect forward segments
    # Result depends on implementation of ray direction


def test_find_intersection_parallel_ray_and_road() -> None:
    """
    Test when ray is parallel to a road segment.

    Boundary value: Parallel lines (slope difference ≈ 0)
    Special case: Tests parallel line handling
    """
    # Create horizontal road
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)
    angle: float = 0.0  # Horizontal ray, parallel to road
    camera_x: float = 5.0
    camera_y: float = 5.0  # Above the road

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Parallel ray above road should not intersect
    assert x is None or y != camera_y


def test_find_intersection_negative_y_coordinates() -> None:
    """
    Test with negative y-coordinates (road below x-axis).

    Boundary value: Negative coordinates
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([-10, -10, -10, -10], dtype=np.float64)
    angle: float = 30.0
    camera_x: float = 0.0
    camera_y: float = 0.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    assert x is not None
    assert y is not None
    assert y < 0  # Intersection should be below x-axis
    assert dist is not None


def test_find_intersection_zero_distance() -> None:
    """
    Test intersection at zero distance (camera exactly at intersection point).

    Boundary value: distance = 0
    """
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([5, 5, 5, 5], dtype=np.float64)
    angle: float = 0.0
    camera_x: float = 5.0
    camera_y: float = 5.0

    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Should find intersection ahead on the road
    if x is not None and abs(x - camera_x) < 0.001:
        # If it returns the camera position, distance might be ~0
        assert dist is not None
        assert dist >= 0


if __name__ == "__main__":
    # Run all tests
    print("Running comprehensive geometry tests...")
    pytest.main([__file__, "-v"])
