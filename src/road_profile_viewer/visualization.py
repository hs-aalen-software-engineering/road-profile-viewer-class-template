"""
Visualization Module - Dash UI Layer
=====================================
This module contains the Dash application UI components and callbacks for
the interactive road profile viewer.
"""

import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html

from road_profile_viewer.geometry import find_intersection
from road_profile_viewer.road import generate_road_profile

# API base URL for fetching profiles
API_BASE_URL = "http://127.0.0.1:8000"


def create_dash_app() -> Dash:
    """
    Create and configure the Dash application.

    Returns:
    --------
    Dash
        Configured Dash application instance
    """
    # Initialize the Dash app
    app = Dash(__name__)

    # Define the layout
    app.layout = html.Div([
        # Store for caching profile data
        dcc.Store(id="profiles-store"),
        dcc.Store(id="selected-profile-data"),
        html.H1(
            "Road Profile Viewer with Camera Ray Intersection",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "20px",
            },
        ),
        # Profile selector section
        html.Div(
            [
                html.Label(
                    "Select Road Profile:",
                    style={"fontWeight": "bold", "marginRight": "10px"},
                ),
                dcc.Dropdown(
                    id="profile-dropdown",
                    placeholder="Select a profile...",
                    style={"width": "300px", "display": "inline-block"},
                ),
                html.Button(
                    "Refresh Profiles",
                    id="refresh-button",
                    n_clicks=0,
                    style={
                        "marginLeft": "10px",
                        "padding": "5px 15px",
                        "cursor": "pointer",
                    },
                ),
                dcc.Link(
                    "Upload New Profile",
                    href="/upload",
                    style={
                        "marginLeft": "20px",
                        "color": "#3498db",
                        "textDecoration": "none",
                        "fontWeight": "bold",
                    },
                ),
            ],
            style={
                "textAlign": "center",
                "marginBottom": "20px",
                "padding": "10px",
            },
        ),
        # Angle input section
        html.Div(
            [
                html.Label(
                    "Camera Ray Angle (degrees from horizontal):",
                    style={"fontWeight": "bold", "marginRight": "10px"},
                ),
                dcc.Input(
                    id="angle-input",
                    type="number",
                    value=-1.1,
                    step=0.1,
                    style={
                        "marginRight": "20px",
                        "padding": "5px",
                        "width": "100px",
                    },
                ),
                html.Span(
                    id="intersection-info",
                    style={"color": "#e74c3c", "fontWeight": "bold"},
                ),
            ],
            style={
                "textAlign": "center",
                "marginBottom": "20px",
                "padding": "10px",
            },
        ),
        dcc.Graph(id="road-profile-graph", style={"height": "400px"}),
        html.Div(
            [
                html.H3("Instructions:", style={"color": "#2c3e50"}),
                html.Ul([
                    html.Li("Select a road profile from the dropdown or use the default generated profile"),
                    html.Li("The dark grey line represents the road profile"),
                    html.Li("The red point at (0, 2.0) represents the camera position"),
                    html.Li("The blue line shows the camera ray at the specified angle"),
                    html.Li("The green point shows where the ray intersects the road"),
                    html.Li("Hover over the green point to see the distance from camera to intersection"),
                    html.Li("Adjust the angle to see how the intersection point changes"),
                    html.Li("Negative angles point downward, positive angles point upward"),
                ]),
            ],
            style={
                "margin": "20px",
                "padding": "20px",
                "backgroundColor": "#ecf0f1",
                "borderRadius": "5px",
            },
        ),
    ])

    @app.callback(
        Output("profile-dropdown", "options"),
        Output("profiles-store", "data"),
        Input("refresh-button", "n_clicks"),
    )
    def load_profiles(n_clicks: int) -> tuple[list[dict], list[dict]]:  # pyright: ignore[reportUnusedFunction]
        """
        Load available profiles from the API.

        Parameters:
        -----------
        n_clicks : int
            Number of times refresh button was clicked (triggers callback)

        Returns:
        --------
        tuple
            (dropdown options, profiles data)
        """
        import httpx

        try:
            response = httpx.get(f"{API_BASE_URL}/profiles", timeout=5.0)
            if response.status_code == 200:
                profiles = response.json()
                options = [{"label": p["name"], "value": p["id"]} for p in profiles]
                # Add default option
                options.insert(0, {"label": "Default (Generated)", "value": "default"})
                return options, profiles
        except Exception:
            pass

        # Fallback if API is unavailable
        return [{"label": "Default (Generated)", "value": "default"}], []

    @app.callback(
        Output("selected-profile-data", "data"),
        Input("profile-dropdown", "value"),
        State("profiles-store", "data"),
    )
    def fetch_profile_data(
        profile_id: str | int | None,
        profiles_cache: list[dict] | None,
    ) -> dict | None:  # pyright: ignore[reportUnusedFunction]
        """
        Fetch the selected profile data.

        Parameters:
        -----------
        profile_id : str | int | None
            Selected profile ID (or "default")
        profiles_cache : list[dict] | None
            Cached profiles from store

        Returns:
        --------
        dict | None
            Profile data or None for default
        """
        if profile_id is None or profile_id == "default":
            return None

        # Try to find in cache first
        if profiles_cache:
            for profile in profiles_cache:
                if profile.get("id") == profile_id:
                    return profile

        # Fetch from API if not in cache
        import httpx

        try:
            response = httpx.get(f"{API_BASE_URL}/profiles/{profile_id}", timeout=5.0)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass

        return None

    # Define the callback to update the graph
    @app.callback(
        [
            Output("road-profile-graph", "figure"),
            Output("intersection-info", "children"),
        ],
        [
            Input("angle-input", "value"),
            Input("selected-profile-data", "data"),
        ],
    )
    def update_graph(
        angle: float | None,
        profile_data: dict | None,
    ) -> tuple[go.Figure, str]:  # pyright: ignore[reportUnusedFunction]
        """
        Update the graph based on the input angle and selected profile.

        Parameters:
        -----------
        angle : float
            Camera ray angle in degrees
        profile_data : dict | None
            Selected profile data from API (or None for default)

        Returns:
        --------
        tuple
            (plotly figure, info text)
        """
        if angle is None:
            angle = -1.1

        # Get road profile coordinates
        if profile_data is not None:
            # Use profile from database
            x_road = np.array(profile_data["x_coordinates"])
            y_road = np.array(profile_data["y_coordinates"])
            profile_name = profile_data.get("name", "Selected Profile")
        else:
            # Generate default profile
            x_road, y_road = generate_road_profile(num_points=100, x_max=80)
            profile_name = "Default (Generated)"

        # Camera position
        camera_x, camera_y = 0, 2.0

        # Find intersection first to determine ray length
        x_intersect, y_intersect, distance = find_intersection(x_road, y_road, angle, camera_x, camera_y)

        # Calculate adaptive ray line based on intersection
        if x_intersect is not None:
            # Ray goes from camera to intersection point
            x_ray = np.array([camera_x, x_intersect])
            y_ray = np.array([camera_y, y_intersect])
        else:
            # No intersection - show a short ray (20 units or to edge of plot)
            angle_rad = -np.deg2rad(angle)
            if np.abs(np.cos(angle_rad)) < 1e-10:
                # Vertical line
                x_ray = np.array([camera_x, camera_x])
                y_ray = np.array([camera_y, camera_y - 10])
            else:
                slope = np.tan(angle_rad)
                x_end = min(camera_x + 20, 80)
                y_end = camera_y + slope * (x_end - camera_x)
                x_ray = np.array([camera_x, x_end])
                y_ray = np.array([camera_y, y_end])

        # Create figure
        fig = go.Figure()

        # Add road profile
        fig.add_trace(
            go.Scatter(
                x=x_road,
                y=y_road,
                mode="lines+markers",
                name=f"Road Profile: {profile_name}",
                line={"color": "#4a4a4a", "width": 3},
                marker={"size": 4, "color": "#4a4a4a"},
                hovertemplate="Road<br>x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>",
            )
        )

        # Add camera point
        fig.add_trace(
            go.Scatter(
                x=[camera_x],
                y=[camera_y],
                mode="markers",
                name="Camera",
                marker={
                    "size": 12,
                    "color": "red",
                    "symbol": "circle",
                },
                hovertemplate="Camera<br>Position: (%{x:.2f}, %{y:.2f})<extra></extra>",
            )
        )

        # Add camera ray
        fig.add_trace(
            go.Scatter(
                x=x_ray,
                y=y_ray,
                mode="lines",
                name=f"Camera Ray ({angle}°)",
                line={"color": "blue", "width": 2, "dash": "dash"},
                hovertemplate="Camera Ray<br>x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>",
            )
        )

        # Add intersection point if it exists
        info_text = ""
        if x_intersect is not None:
            hover_text = (
                f"Intersection Point<br>Position: ({x_intersect:.2f}, {y_intersect:.2f})<br>"
                f"Distance from camera: {distance:.2f}<extra></extra>"
            )
            fig.add_trace(
                go.Scatter(
                    x=[x_intersect],
                    y=[y_intersect],
                    mode="markers",
                    name="Intersection",
                    marker={"size": 15, "color": "green", "symbol": "star"},
                    hovertemplate=hover_text,
                )
            )
            info_text = f"Intersection found at ({x_intersect:.2f}, {y_intersect:.2f}) | Distance: {distance:.2f} units"
        else:
            info_text = "No intersection found with current angle"

        # Update layout
        fig.update_layout(
            xaxis_title="X Position (m)",
            yaxis_title="Y Position (m)",
            hovermode="closest",
            showlegend=True,
            legend={
                "x": 1.02,
                "y": 1,
                "xanchor": "left",
                "yanchor": "top",
                "bgcolor": "rgba(255,255,255,0.8)",
                "bordercolor": "#dee2e6",
                "borderwidth": 1,
            },
            plot_bgcolor="#f8f9fa",
            xaxis={"gridcolor": "#dee2e6", "range": [-2, 82], "constrain": "domain"},
            yaxis={
                "gridcolor": "#dee2e6",
                "scaleanchor": "x",
                "scaleratio": 1,
                "range": [-0.5, 10],
                "constrain": "domain",
            },
            margin={"l": 50, "r": 150, "t": 30, "b": 50},
        )

        return fig, info_text

    return app
