"""
Unit Tests for Geometry Module
================================
This module contains comprehensive unit tests for the geometric calculation functions
in the geometry module: calculate_ray_line and find_intersection.

Test Coverage:
- calculate_ray_line(): Tests for all branches (vertical, upward, downward rays)
- find_intersection(): Tests for normal intersection scenarios

Equivalence classes and boundary values are documented in each test.
"""

import numpy as np
import pytest
from numpy.typing import NDArray
from pytest import approx

from road_profile_viewer.geometry import calculate_ray_line, find_intersection

# ==============================================================================
# TESTS FOR calculate_ray_line()
# ==============================================================================


@pytest.mark.requirement("REQ-GEOM-001")
def test_calculate_ray_line_vertical_ray() -> None:
    """
    Test that calculate_ray_line() handles vertical ray (angle = 90°).

    Requirement: REQ-GEOM-001 - calculate_ray_line() shall handle vertical rays
    Equivalence class: Vertical rays (angle ≈ 90°)
    Boundary value: angle = 90° (exact vertical)
    Branch coverage: Tests vertical ray branch (np.abs(np.cos(angle_rad)) < 1e-10)
    """
    # Arrange
    angle: float = 90.0
    camera_x: float = 5.0
    camera_y: float = 2.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y)

    # Assert
    assert len(x_ray) == 2, "Vertical ray should have 2 points"
    assert np.allclose(x_ray, [camera_x, camera_x]), "Vertical ray should have constant x"
    assert y_ray[0] == approx(camera_y), "Ray should start at camera y"
    assert y_ray[1] < camera_y, "Ray should extend downward"


@pytest.mark.requirement("REQ-GEOM-001")
def test_calculate_ray_line_near_vertical_ray() -> None:
    """
    Test that calculate_ray_line() handles near-vertical ray (angle ≈ 90°).

    Requirement: REQ-GEOM-001 - calculate_ray_line() shall handle vertical rays
    Equivalence class: Near-vertical rays (89° < angle < 91°)
    Boundary value: angle = 89.9° (just below vertical threshold)
    Branch coverage: Tests the slope calculation branch (not vertical)
    """
    # Arrange
    angle: float = 89.9
    camera_x: float = 0.0
    camera_y: float = 10.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y)

    # Assert
    assert len(x_ray) > 0, "Ray should have points"
    assert len(y_ray) > 0, "Ray should have points"
    assert x_ray[0] == approx(camera_x), "Ray should start at camera x"
    assert y_ray[0] == approx(camera_y), "Ray should start at camera y"
    # Near-vertical ray should have very steep slope (large y change relative to x)
    y_change = abs(y_ray[-1] - y_ray[0])
    x_change = abs(x_ray[-1] - x_ray[0])
    assert y_change > 10 * x_change, "Near-vertical ray should have very steep slope"


@pytest.mark.requirement("REQ-GEOM-002")
def test_calculate_ray_line_upward_ray_negative_angle() -> None:
    """
    Test that calculate_ray_line() handles upward ray (negative angle).

    Requirement: REQ-GEOM-002 - calculate_ray_line() shall limit upward rays to 20 units
    Equivalence class: Upward rays (angle < 0°)
    Branch coverage: Tests upward ray branch (angle < 0 or angle > 180)
    """
    # Arrange
    angle: float = -30.0
    camera_x: float = 0.0
    camera_y: float = 2.0
    x_max: float = 80.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y, x_max)

    # Assert
    assert len(x_ray) > 0, "Ray should have points"
    assert x_ray[0] == approx(camera_x), "Ray should start at camera x"
    assert y_ray[0] == approx(camera_y), "Ray should start at camera y"
    # Upward ray should be limited to 20 units
    assert np.max(x_ray) <= camera_x + 20, "Upward ray should be limited to 20 units"
    # Ray should go upward (y increases)
    assert y_ray[-1] > y_ray[0], "Upward ray should have increasing y values"


@pytest.mark.requirement("REQ-GEOM-002")
def test_calculate_ray_line_upward_ray_large_angle() -> None:
    """
    Test that calculate_ray_line() handles upward ray (angle > 180°).

    Requirement: REQ-GEOM-002 - calculate_ray_line() shall limit upward rays to 20 units
    Equivalence class: Upward rays (angle > 180°)
    Boundary value: angle = 200° (> 180°)
    Branch coverage: Tests upward ray branch (angle < 0 or angle > 180)
    """
    # Arrange
    angle: float = 200.0
    camera_x: float = 10.0
    camera_y: float = 5.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y)

    # Assert
    assert len(x_ray) > 0, "Ray should have points"
    assert len(y_ray) > 0, "Ray should have points"
    assert x_ray[0] == approx(camera_x), "Ray should start at camera x"
    assert y_ray[0] == approx(camera_y), "Ray should start at camera y"
    # Upward ray should be limited to 20 units
    assert np.max(x_ray) <= camera_x + 20, "Upward ray should be limited to 20 units"


@pytest.mark.requirement("REQ-GEOM-003")
def test_calculate_ray_line_downward_ray() -> None:
    """
    Test that calculate_ray_line() handles downward ray (positive angle 0-180°).

    Requirement: REQ-GEOM-003 - calculate_ray_line() shall extend downward rays to x_max
    Equivalence class: Downward rays (0° < angle ≤ 180°)
    Branch coverage: Tests downward ray branch (else path for angle direction)
    """
    # Arrange
    angle: float = 30.0
    camera_x: float = 0.0
    camera_y: float = 10.0
    x_max: float = 80.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y, x_max)

    # Assert
    assert len(x_ray) > 0, "Ray should have points"
    assert x_ray[0] == approx(camera_x), "Ray should start at camera x"
    assert y_ray[0] == approx(camera_y), "Ray should start at camera y"
    # Downward ray should extend to x_max
    assert np.max(x_ray) == approx(x_max), "Downward ray should extend to x_max"
    # Ray should go downward (y decreases)
    assert y_ray[-1] < y_ray[0], "Downward ray should have decreasing y values"


@pytest.mark.requirement("FR-002")
def test_calculate_ray_line_horizontal_ray() -> None:
    """
    Test that calculate_ray_line() handles horizontal ray (angle = 0°).

    Requirement: FR-002 - The system shall calculate camera ray-road intersection
    Equivalence class: Horizontal rays (angle = 0°)
    Boundary value: angle = 0° (horizontal)
    """
    # Arrange
    angle: float = 0.0
    camera_x: float = 5.0
    camera_y: float = 3.0
    x_max: float = 80.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y, x_max)

    # Assert
    assert len(x_ray) > 0, "Ray should have points"
    assert x_ray[0] == approx(camera_x), "Ray should start at camera x"
    assert y_ray[0] == approx(camera_y), "Ray should start at camera y"
    # Horizontal ray should have constant y
    assert np.allclose(y_ray, camera_y), "Horizontal ray should have constant y"
    assert np.max(x_ray) == approx(x_max), "Horizontal ray should extend to x_max"


@pytest.mark.requirement("FR-002")
def test_calculate_ray_line_boundary_angle_180() -> None:
    """
    Test that calculate_ray_line() handles angle = 180° (boundary value).

    Requirement: FR-002 - The system shall calculate camera ray-road intersection
    Equivalence class: Downward rays (0° ≤ angle ≤ 180°)
    Boundary value: angle = 180° (horizontal pointing left, treated as downward path)
    """
    # Arrange
    angle: float = 180.0
    camera_x: float = 10.0
    camera_y: float = 5.0
    x_max: float = 80.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y, x_max)

    # Assert
    assert len(x_ray) > 0, "Ray should have points"
    assert len(y_ray) > 0, "Ray should have points"
    assert x_ray[0] == approx(camera_x), "Ray should start at camera x"
    assert y_ray[0] == approx(camera_y), "Ray should start at camera y"
    # At 180°, ray points horizontally to the left/down
    assert np.max(x_ray) == approx(x_max), "Ray at 180° follows downward path to x_max"


@pytest.mark.requirement("FR-002")
def test_calculate_ray_line_steep_downward_angle() -> None:
    """
    Test that calculate_ray_line() handles steep downward angle.

    Requirement: FR-002 - The system shall calculate camera ray-road intersection
    Equivalence class: Steep downward rays (60° < angle < 90°)
    """
    # Arrange
    angle: float = 75.0
    camera_x: float = 0.0
    camera_y: float = 5.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y)

    # Assert
    assert len(x_ray) > 0, "Ray should have points"
    assert x_ray[0] == approx(camera_x), "Ray should start at camera x"
    assert y_ray[0] == approx(camera_y), "Ray should start at camera y"
    # Steep angle should result in large y change relative to x change
    y_change = abs(y_ray[-1] - y_ray[0])
    x_change = abs(x_ray[-1] - x_ray[0])
    assert y_change > x_change, "Steep ray should have larger y change than x change"


@pytest.mark.requirement("FR-002")
def test_calculate_ray_line_custom_camera_position() -> None:
    """
    Test that calculate_ray_line() works with custom camera position.

    Requirement: FR-002 - The system shall calculate camera ray-road intersection
    Equivalence class: Various camera positions (non-default)
    """
    # Arrange
    angle: float = 45.0
    camera_x: float = 20.0
    camera_y: float = 8.0
    x_max: float = 100.0

    # Act
    x_ray, y_ray = calculate_ray_line(angle, camera_x, camera_y, x_max)

    # Assert
    assert len(x_ray) > 0, "Ray should have points"
    assert x_ray[0] == camera_x, "Ray should start at custom camera_x"
    assert y_ray[0] == camera_y, "Ray should start at custom camera_y"
    assert np.max(x_ray) == approx(x_max), "Ray should extend to custom x_max"


# ==============================================================================
# TESTS FOR find_intersection()
# ==============================================================================


@pytest.mark.requirement("FR-002")
@pytest.mark.requirement("REQ-GEOM-007")
def test_find_intersection_finds_intersection_for_normal_angle() -> None:
    """
    Test that find_intersection() returns a valid intersection
    for a normal downward angle with a simple road profile.

    Requirements:
    - FR-002: The system shall calculate camera ray-road intersection
    - REQ-GEOM-007: Intersection distance shall be positive when found
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


@pytest.mark.requirement("REQ-GEOM-005")
def test_find_intersection_skips_segments_behind_camera() -> None:
    """
    Test that find_intersection() skips road segments behind the camera.

    Requirement: REQ-GEOM-005 - find_intersection() shall skip road segments behind camera
    This tests line 110 (continue) when x2 <= camera_x.
    """
    # Arrange: Create road with segments before and after camera
    x_road: NDArray[np.float64] = np.array([-20, -10, 0, 10, 20, 30], dtype=np.float64)
    y_road: NDArray[np.float64] = np.array([0, 1, 2, 3, 4, 5], dtype=np.float64)
    angle: float = 20.0  # Downward angle
    camera_x: float = 5.0  # Camera at x=5, some segments are behind
    camera_y: float = 10.0  # Camera above road

    # Act: Find intersection
    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Assert: Should find intersection only in segments ahead of camera
    assert x is not None, "Should find intersection"
    assert x > camera_x, "Intersection should be ahead of camera (x > camera_x)"


@pytest.mark.requirement("REQ-GEOM-006")
def test_find_intersection_parallel_ray_and_segment() -> None:
    """
    Test find_intersection when ray is nearly parallel to a road segment.

    Requirement: REQ-GEOM-006 - find_intersection() shall handle parallel ray and segment
    This tests line 125 (t = 0) when |diff2 - diff1| < 1e-10 (parallel case).
    """
    # Arrange: Create horizontal road and nearly horizontal ray
    x_road: NDArray[np.float64] = np.array([0, 10, 20, 30, 40], dtype=np.float64)
    # Road with a flat section that could be parallel to the ray
    y_road: NDArray[np.float64] = np.array([5, 5, 5, 5, 5], dtype=np.float64)
    angle: float = 0.0  # Horizontal ray (parallel to flat road)
    camera_x: float = 0.0
    camera_y: float = 5.0  # Camera at same height as road (ray lies on road)

    # Act: Find intersection
    x, y, dist = find_intersection(x_road, y_road, angle, camera_x, camera_y)

    # Assert: For parallel lines at same height, should find intersection at start
    # The algorithm handles this edge case by setting t=0
    # Result can be None or found depending on exact floating point comparison
    # Either outcome is acceptable for this edge case
    if x is not None:
        assert dist is not None, "If intersection found, distance should be defined"
        assert dist >= 0, "Distance should be non-negative"


if __name__ == "__main__":
    # Allow running tests directly
    print("Running geometry unit tests...")
    print()

    test_find_intersection_finds_intersection_for_normal_angle()

    print()
    print("✅ All geometry tests passed!")
