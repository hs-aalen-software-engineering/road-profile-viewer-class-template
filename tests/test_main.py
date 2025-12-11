"""
Unit Tests for Main Module
===========================
This module contains unit tests for the main entry point.

Test Coverage:
- main(): Tests the application entry point with mocked dependencies
- run_fastapi(): Tests FastAPI server runner

Equivalence classes and boundary values are documented in each test.
"""

from unittest.mock import MagicMock, patch


def test_main_creates_and_runs_app() -> None:
    """
    Test that main() creates both FastAPI and Dash apps and runs them.

    Coverage: Tests main() function which starts FastAPI in background thread
    and runs Dash on main thread.
    """
    # Arrange
    mock_dash_app = MagicMock()
    mock_dash_app.run = MagicMock()
    mock_thread = MagicMock()

    # Act & Assert
    with patch("road_profile_viewer.main.create_dash_app", return_value=mock_dash_app) as mock_create:
        with patch("road_profile_viewer.main.threading.Thread", return_value=mock_thread) as mock_thread_class:
            with patch("builtins.print") as mock_print:
                from road_profile_viewer.main import main

                main()

                # Verify FastAPI thread was created and started
                mock_thread_class.assert_called_once()
                mock_thread.start.assert_called_once()

                # Verify create_dash_app was called
                mock_create.assert_called_once()

                # Verify print statements were called
                assert mock_print.call_count >= 2, "Should print startup messages"

                # Verify Dash app.run was called with correct parameters
                mock_dash_app.run.assert_called_once_with(debug=True, port=8050, use_reloader=False)


def test_run_fastapi() -> None:
    """
    Test that run_fastapi() runs uvicorn with correct configuration.

    Coverage: Tests run_fastapi() function.
    """
    with patch("road_profile_viewer.main.uvicorn.run") as mock_uvicorn:
        from road_profile_viewer.main import run_fastapi

        run_fastapi()

        mock_uvicorn.assert_called_once()
        call_kwargs = mock_uvicorn.call_args
        assert call_kwargs[1]["host"] == "127.0.0.1"
        assert call_kwargs[1]["port"] == 8000
        assert call_kwargs[1]["log_level"] == "warning"


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
    test_run_fastapi()
    test_main_function_is_callable()

    print()
    print("All main module tests passed!")
