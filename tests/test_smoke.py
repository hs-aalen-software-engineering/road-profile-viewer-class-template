"""
Smoke Tests: Verify basic application structure

These tests check that:
1. All modules can be imported without errors
2. Pydantic models are correctly defined
3. Basic module structure is correct

Note: These are NOT comprehensive unit tests.
These are just "smoke tests" to verify basic structure and imports.
Your comprehensive unit tests should be in separate test files.
"""


def test_imports_work():
    """Test that all core modules can be imported."""
    try:
        from road_profile_viewer import geometry, main, road, visualization
    except ImportError as e:
        raise AssertionError(f"Import failed: {e}") from e

    # Verify modules are actually imported
    assert geometry is not None
    assert road is not None
    assert visualization is not None
    assert main is not None

    print("✅ All core modules import successfully!")


def test_models_exist():
    """Test that Pydantic models module exists and can be imported."""
    try:
        from road_profile_viewer import models
    except ImportError as e:
        raise AssertionError(f"models.py import failed: {e}") from e

    assert models is not None
    print("✅ models.py exists and imports successfully!")


def test_pydantic_model_exists():
    """Test that RoadProfile Pydantic model is defined."""
    try:
        from road_profile_viewer.models import RoadProfile
    except ImportError as e:
        raise AssertionError(f"RoadProfile model import failed: {e}") from e

    # Verify it's a Pydantic model
    assert hasattr(RoadProfile, "model_validate"), "RoadProfile should be a Pydantic model"

    print("✅ RoadProfile Pydantic model exists!")


def test_geometry_functions_exist():
    """Test that geometry module has expected functions."""
    from road_profile_viewer.geometry import calculate_ray_line, find_intersection

    assert callable(calculate_ray_line), "calculate_ray_line should be callable"
    assert callable(find_intersection), "find_intersection should be callable"

    print("✅ geometry.py exports correct functions!")


def test_main_function_exists():
    """Test that main module has main() function."""
    from road_profile_viewer.main import main

    assert callable(main), "main() should be callable"

    print("✅ main.py has main() function!")


if __name__ == "__main__":
    # Allow running tests directly
    print("Running smoke tests...")
    print()

    test_imports_work()
    test_models_exist()
    test_pydantic_model_exists()
    test_geometry_functions_exist()
    test_main_function_exists()

    print()
    print("🎉 All smoke tests passed!")
    print("Your basic application structure is correct!")
