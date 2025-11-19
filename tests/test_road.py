"""
Unit Tests for Road Module
===========================
This module contains comprehensive unit tests for the road profile generation function.

Test Coverage:
- generate_road_profile(): Tests for various parameter combinations and output validation

Equivalence classes and boundary values are documented in each test.
"""

import sys
from pathlib import Path

import numpy as np
from pytest import approx

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from road_profile_viewer.road import generate_road_profile

# ==============================================================================
# TESTS FOR generate_road_profile()
# ==============================================================================


def test_generate_road_profile_default_parameters() -> None:
    """
    Test generate_road_profile() with default parameters.

    Equivalence class: Default parameters (num_points=100, x_max=80)
    """
    # Act
    x, y = generate_road_profile()

    # Assert
    assert isinstance(x, np.ndarray), "x should be a numpy array"
    assert isinstance(y, np.ndarray), "y should be a numpy array"
    assert len(x) == 100, "Default num_points should be 100"
    assert len(y) == 100, "y should have same length as x"
    assert x[0] == approx(0.0), "Road should start at x=0"
    assert x[-1] == approx(80.0), "Road should end at x_max=80"
    assert y[0] == approx(0.0), "Road should start at y=0 (normalized)"


def test_generate_road_profile_small_num_points() -> None:
    """
    Test generate_road_profile() with small number of points.

    Equivalence class: Small num_points (< 50)
    Boundary value: num_points = 10
    """
    # Arrange
    num_points: int = 10
    x_max: float = 50.0

    # Act
    x, y = generate_road_profile(num_points, x_max)

    # Assert
    assert len(x) == num_points, f"Should have {num_points} points"
    assert len(y) == num_points, f"y should have {num_points} points"
    assert x[0] == approx(0.0), "Road should start at x=0"
    assert x[-1] == approx(x_max), f"Road should end at x_max={x_max}"
    assert y[0] == approx(0.0), "Road should start at y=0"


def test_generate_road_profile_medium_num_points() -> None:
    """
    Test generate_road_profile() with medium number of points.

    Equivalence class: Medium num_points (50-200)
    """
    # Arrange
    num_points: int = 150
    x_max: float = 100.0

    # Act
    x, y = generate_road_profile(num_points, x_max)

    # Assert
    assert len(x) == num_points, f"Should have {num_points} points"
    assert len(y) == num_points, f"y should have {num_points} points"
    assert x[0] == approx(0.0), "Road should start at x=0"
    assert x[-1] == approx(x_max), f"Road should end at x_max={x_max}"


def test_generate_road_profile_large_num_points() -> None:
    """
    Test generate_road_profile() with large number of points.

    Equivalence class: Large num_points (> 200)
    """
    # Arrange
    num_points: int = 500
    x_max: float = 80.0

    # Act
    x, y = generate_road_profile(num_points, x_max)

    # Assert
    assert len(x) == num_points, f"Should have {num_points} points"
    assert len(y) == num_points, f"y should have {num_points} points"


def test_generate_road_profile_small_x_max() -> None:
    """
    Test generate_road_profile() with small x_max value.

    Equivalence class: Small x_max (< 50)
    Boundary value: x_max = 10
    """
    # Arrange
    num_points: int = 50
    x_max: float = 10.0

    # Act
    x, y = generate_road_profile(num_points, x_max)

    # Assert
    assert x[0] == approx(0.0), "Road should start at x=0"
    assert x[-1] == approx(x_max), f"Road should end at x_max={x_max}"
    assert np.all(x >= 0), "All x values should be non-negative"
    assert np.all(x <= x_max), f"All x values should be <= {x_max}"


def test_generate_road_profile_large_x_max() -> None:
    """
    Test generate_road_profile() with large x_max value.

    Equivalence class: Large x_max (> 100)
    """
    # Arrange
    num_points: int = 100
    x_max: float = 200.0

    # Act
    x, y = generate_road_profile(num_points, x_max)

    # Assert
    assert x[0] == approx(0.0), "Road should start at x=0"
    assert x[-1] == approx(x_max), f"Road should end at x_max={x_max}"
    assert np.all(x >= 0), "All x values should be non-negative"
    assert np.all(x <= x_max), f"All x values should be <= {x_max}"


def test_generate_road_profile_x_coordinates_monotonic() -> None:
    """
    Test that x coordinates are monotonically increasing.

    Mathematical property: x values should strictly increase
    """
    # Act
    x, y = generate_road_profile(100, 80)

    # Assert
    x_diffs = np.diff(x)
    assert np.all(x_diffs > 0), "x coordinates should be strictly increasing"


def test_generate_road_profile_output_shape_consistency() -> None:
    """
    Test that output shapes are consistent with input parameters.

    Boundary value test: Various combinations of parameters
    """
    # Test multiple combinations
    test_cases = [
        (50, 40.0),
        (100, 80.0),
        (200, 100.0),
        (75, 60.0),
    ]

    for num_points, x_max in test_cases:
        x, y = generate_road_profile(num_points, x_max)

        assert len(x) == num_points, f"x should have {num_points} points"
        assert len(y) == num_points, f"y should have {num_points} points"
        assert x.shape == y.shape, "x and y should have same shape"
        assert x[0] == approx(0.0), "Road should start at x=0"
        assert x[-1] == approx(x_max), f"Road should end at x_max={x_max}"
        assert y[0] == approx(0.0, abs=1e-10), "Road should start at y=0"


def test_generate_road_profile_minimum_viable_points() -> None:
    """
    Test generate_road_profile() with minimum number of points.

    Boundary value: num_points = 2 (minimum for a line segment)
    """
    # Arrange
    num_points: int = 2
    x_max: float = 10.0

    # Act
    x, y = generate_road_profile(num_points, x_max)

    # Assert
    assert len(x) == 2, "Should have exactly 2 points"
    assert len(y) == 2, "Should have exactly 2 points"
    assert x[0] == 0.0, "Should start at x=0"
    assert x[1] == x_max, f"Should end at x_max={x_max}"
    assert y[0] == 0.0, "Should start at y=0"


def test_generate_road_profile_y_values_reasonable() -> None:
    """
    Test that y values are within reasonable bounds.

    Mathematical property: y values should be within expected range
    based on the clothoid approximation formula
    """
    # Act
    x, y = generate_road_profile(100, 80)

    # Assert
    # Based on the formula: y contains sin terms and polynomial terms
    # y values should be reasonable relative to x_max
    assert np.all(np.abs(y) < 100), "y values should be within reasonable bounds"

    # Check that road has variation (not all zeros)
    assert not np.allclose(y, 0), "Road should have vertical variation"


if __name__ == "__main__":
    # Allow running tests directly
    print("Running road profile tests...")
    print()

    test_generate_road_profile_default_parameters()
    test_generate_road_profile_small_num_points()
    test_generate_road_profile_medium_num_points()
    test_generate_road_profile_large_num_points()
    test_generate_road_profile_small_x_max()
    test_generate_road_profile_large_x_max()
    test_generate_road_profile_x_coordinates_monotonic()
    test_generate_road_profile_output_shape_consistency()
    test_generate_road_profile_minimum_viable_points()
    test_generate_road_profile_y_values_reasonable()

    print()
    print("✅ All road profile tests passed!")
