"""
Road Profile Viewer - Interactive 2D Visualization
===================================================
Main entry point for the road profile viewer application.

This application visualizes a road profile with camera ray intersection
using an interactive Dash interface. It runs both a FastAPI backend (for
the REST API) and a Dash frontend (for visualization).
"""

import threading

import uvicorn

from road_profile_viewer.api.main import app as fastapi_app
from road_profile_viewer.visualization import create_dash_app


def run_fastapi() -> None:
    """Run the FastAPI server in a background thread."""
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000, log_level="warning")


def main() -> None:
    """
    Main function to run both the FastAPI API and Dash application.

    Starts the FastAPI server in a background thread on port 8000,
    then runs the Dash application on the main thread on port 8050.
    """
    # Start FastAPI in background thread
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()

    print("=" * 60)
    print("Road Profile Viewer")
    print("=" * 60)
    print()
    print("Starting services:")
    print("  - FastAPI API:    http://127.0.0.1:8000")
    print("  - API Docs:       http://127.0.0.1:8000/docs")
    print("  - Dash Viewer:    http://127.0.0.1:8050")
    print()
    print("Open your browser and navigate to: http://127.0.0.1:8050/")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)

    # Create and run Dash app on main thread
    # Note: use_reloader=False prevents Werkzeug from spawning a second process
    # which would cause port 8000 conflict with the FastAPI server
    dash_app = create_dash_app()
    dash_app.run(debug=True, port=8050, use_reloader=False)


if __name__ == "__main__":
    main()
