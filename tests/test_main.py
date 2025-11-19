"""
Unit Tests for Main Module
===========================
This module contains unit tests for the main entry point.

Test Coverage:
- main(): Tests the application entry point with mocked dependencies

Equivalence classes and boundary values are documented in each test.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_main_creates_and_runs_app() -> None:
    """
    Test that main() creates a Dash app and runs it in debug mode.

    Coverage: Tests lines 17-21 (app creation, printing, and running)
    """
    # Arrange
    mock_app = MagicMock()
    mock_app.run = MagicMock()

    # Act & Assert
    with patch("road_profile_viewer.main.create_dash_app", return_value=mock_app) as mock_create:
        with patch("builtins.print") as mock_print:
            # Import and call main
            from road_profile_viewer.main import main

            main()

            # Verify create_dash_app was called
            mock_create.assert_called_once()

            # Verify print statements were called
            assert mock_print.call_count >= 2, "Should print startup messages"

            # Verify app.run was called with debug=True
            mock_app.run.assert_called_once_with(debug=True)


def test_main_function_is_callable() -> None:
    """
    Test that the main function is callable and can be imported.

    This verifies the module structure is correct.
    """
    # Act & Assert
    from road_profile_viewer.main import main

    # Verify main is callable
    assert callable(main), "main should be a callable function"


if __name__ == "__main__":
    # Allow running tests directly
    print("Running main module tests...")
    print()

    test_main_creates_and_runs_app()
    test_main_function_is_callable()

    print()
    print("✅ All main module tests passed!")
