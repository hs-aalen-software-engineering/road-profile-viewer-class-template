"""
Visualization Module - Dash UI Layer
=====================================
This module contains the Dash application UI components and callbacks for
the interactive road profile viewer.
"""

import base64
import json

import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html

from road_profile_viewer.geometry import find_intersection
from road_profile_viewer.road import generate_road_profile

# API base URL for fetching profiles
API_BASE_URL = "http://127.0.0.1:8000"


def create_upload_layout() -> html.Div:
    """Create the upload page layout."""
    return html.Div(
        [
            html.H1(
                "Upload Road Profile",
                style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "20px"},
            ),
            html.Div(
                [
                    dcc.Link(
                        "< Back to Viewer",
                        href="/",
                        style={
                            "color": "#3498db",
                            "textDecoration": "none",
                            "fontWeight": "bold",
                        },
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            # Upload component
            html.Div(
                [
                    dcc.Upload(
                        id="upload-json",
                        children=html.Div([
                            "Drag and Drop or ",
                            html.A("Select a JSON File", style={"color": "#3498db"}),
                        ]),
                        style={
                            "width": "100%",
                            "height": "100px",
                            "lineHeight": "100px",
                            "borderWidth": "2px",
                            "borderStyle": "dashed",
                            "borderRadius": "10px",
                            "textAlign": "center",
                            "backgroundColor": "#f8f9fa",
                            "cursor": "pointer",
                        },
                        accept=".json",
                        multiple=False,
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            # Profile name input
            html.Div(
                [
                    html.Label(
                        "Profile Name:",
                        style={"fontWeight": "bold", "marginRight": "10px"},
                    ),
                    dcc.Input(
                        id="profile-name-input",
                        type="text",
                        placeholder="Enter profile name...",
                        style={
                            "width": "300px",
                            "padding": "8px",
                            "marginRight": "10px",
                        },
                    ),
                    html.Button(
                        "Save Profile",
                        id="save-button",
                        n_clicks=0,
                        style={
                            "padding": "8px 20px",
                            "backgroundColor": "#27ae60",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "5px",
                            "cursor": "pointer",
                        },
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            # Status message
            html.Div(
                id="upload-status",
                style={
                    "marginBottom": "20px",
                    "padding": "10px",
                    "borderRadius": "5px",
                },
            ),
            # Preview graph
            html.Div(
                [
                    html.H3("Preview:", style={"color": "#2c3e50"}),
                    dcc.Graph(id="preview-graph", style={"height": "400px"}),
                ],
                style={
                    "padding": "20px",
                    "backgroundColor": "#ecf0f1",
                    "borderRadius": "5px",
                },
            ),
            # Store for parsed upload data
            dcc.Store(id="parsed-upload-data"),
            # Instructions
            html.Div(
                [
                    html.H3("JSON Format:", style={"color": "#2c3e50"}),
                    html.Pre(
                        """{
    "name": "My Profile",
    "x_coordinates": [0.0, 10.0, 20.0, 30.0],
    "y_coordinates": [0.0, 1.5, 2.0, 1.0]
}""",
                        style={
                            "backgroundColor": "#2c3e50",
                            "color": "#ecf0f1",
                            "padding": "15px",
                            "borderRadius": "5px",
                            "overflow": "auto",
                        },
                    ),
                ],
                style={"marginTop": "20px"},
            ),
        ],
        style={"maxWidth": "800px", "margin": "0 auto", "padding": "20px"},
    )


def create_home_layout() -> html.Div:
    """Create the home page layout (main viewer)."""
    return html.Div([
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


def create_dash_app() -> Dash:
    """
    Create and configure the Dash application.

    Returns:
    --------
    Dash
        Configured Dash application instance
    """
    # Initialize the Dash app with URL routing support
    app = Dash(__name__, suppress_callback_exceptions=True)

    # Define the main layout with URL routing
    app.layout = html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ])

    # Page routing callback
    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname: str | None) -> html.Div:  # pyright: ignore[reportUnusedFunction]
        """Route to the appropriate page based on URL."""
        if pathname == "/upload":
            return create_upload_layout()
        return create_home_layout()

    # Upload page callbacks
    @app.callback(
        Output("parsed-upload-data", "data"),
        Output("profile-name-input", "value"),
        Output("upload-status", "children"),
        Output("upload-status", "style"),
        Input("upload-json", "contents"),
        State("upload-json", "filename"),
        prevent_initial_call=True,
    )
    def parse_upload(  # pyright: ignore[reportUnusedFunction]
        contents: str | None,
        filename: str | None,
    ) -> tuple[dict | None, str, str, dict]:
        """Parse uploaded JSON file and show preview."""
        if contents is None:
            return None, "", "", {"display": "none"}

        try:
            # Decode base64 content
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            data = json.loads(decoded.decode("utf-8"))

            # Validate structure
            if "x_coordinates" not in data or "y_coordinates" not in data:
                return (
                    None,
                    "",
                    "Error: JSON must contain 'x_coordinates' and 'y_coordinates'",
                    {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
                )

            if len(data["x_coordinates"]) != len(data["y_coordinates"]):
                return (
                    None,
                    "",
                    "Error: x_coordinates and y_coordinates must have the same length",
                    {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
                )

            if len(data["x_coordinates"]) < 2:
                return (
                    None,
                    "",
                    "Error: Profile must have at least 2 points",
                    {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
                )

            # Use filename or provided name as default
            default_name = data.get("name", filename.replace(".json", "") if filename else "Uploaded Profile")

            return (
                data,
                default_name,
                f"File '{filename}' loaded successfully. Review the preview and click 'Save Profile'.",
                {"backgroundColor": "#27ae60", "color": "white", "padding": "10px"},
            )
        except json.JSONDecodeError:
            return (
                None,
                "",
                "Error: Invalid JSON format",
                {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
            )
        except Exception as e:
            return (
                None,
                "",
                f"Error parsing file: {e!s}",
                {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
            )

    @app.callback(
        Output("preview-graph", "figure"),
        Input("parsed-upload-data", "data"),
    )
    def update_preview(data: dict | None) -> go.Figure:  # pyright: ignore[reportUnusedFunction]
        """Update the preview graph with uploaded data."""
        fig = go.Figure()

        if data is None:
            # Empty preview
            fig.update_layout(
                title="Upload a JSON file to preview",
                xaxis_title="X Position (m)",
                yaxis_title="Y Position (m)",
                plot_bgcolor="#f8f9fa",
            )
            return fig

        x_coords = data.get("x_coordinates", [])
        y_coords = data.get("y_coordinates", [])

        fig.add_trace(
            go.Scatter(
                x=x_coords,
                y=y_coords,
                mode="lines+markers",
                name="Road Profile",
                line={"color": "#4a4a4a", "width": 3},
                marker={"size": 6, "color": "#4a4a4a"},
            )
        )

        fig.update_layout(
            title="Preview: Road Profile",
            xaxis_title="X Position (m)",
            yaxis_title="Y Position (m)",
            plot_bgcolor="#f8f9fa",
            xaxis={"gridcolor": "#dee2e6"},
            yaxis={"gridcolor": "#dee2e6", "scaleanchor": "x", "scaleratio": 1},
        )

        return fig

    @app.callback(
        Output("upload-status", "children", allow_duplicate=True),
        Output("upload-status", "style", allow_duplicate=True),
        Input("save-button", "n_clicks"),
        State("parsed-upload-data", "data"),
        State("profile-name-input", "value"),
        prevent_initial_call=True,
    )
    def save_profile(  # pyright: ignore[reportUnusedFunction]
        n_clicks: int,
        data: dict | None,
        name: str | None,
    ) -> tuple[str, dict]:
        """Save the profile to the database via API."""
        if n_clicks == 0:
            return "", {"display": "none"}

        if data is None:
            return (
                "Please upload a valid JSON file first",
                {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
            )

        if not name or not name.strip():
            return (
                "Please enter a profile name",
                {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
            )

        import httpx

        try:
            profile_data = {
                "name": name.strip(),
                "x_coordinates": data["x_coordinates"],
                "y_coordinates": data["y_coordinates"],
            }

            response = httpx.post(f"{API_BASE_URL}/profiles/", json=profile_data, timeout=5.0)

            if response.status_code == 201:
                return (
                    f"Profile '{name}' saved successfully! Go back to the viewer to use it.",
                    {"backgroundColor": "#27ae60", "color": "white", "padding": "10px"},
                )
            elif response.status_code == 409:
                return (
                    f"Error: A profile with name '{name}' already exists",
                    {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
                )
            elif response.status_code == 422:
                error_detail = response.json().get("detail", "Validation error")
                return (
                    f"Validation error: {error_detail}",
                    {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
                )
            else:
                return (
                    f"Error: Server returned status {response.status_code}",
                    {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
                )
        except httpx.ConnectError:
            return (
                "Error: Cannot connect to API server. Is it running?",
                {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
            )
        except Exception as e:
            return (
                f"Error saving profile: {e!s}",
                {"backgroundColor": "#e74c3c", "color": "white", "padding": "10px"},
            )

    # Home page callbacks (load_profiles, fetch_profile_data, update_graph)
    @app.callback(
        Output("profile-dropdown", "options"),
        Output("profiles-store", "data"),
        Input("refresh-button", "n_clicks"),
        Input("url", "pathname"),
    )
    def load_profiles(n_clicks: int, pathname: str | None) -> tuple[list[dict], list[dict]]:  # pyright: ignore[reportUnusedFunction]
        """Load available profiles from the API. Triggers on page load and refresh button."""
        import httpx

        try:
            response = httpx.get(f"{API_BASE_URL}/profiles/", timeout=5.0)
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
        """Fetch the selected profile data."""
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
        """Update the graph based on the input angle and selected profile."""
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
                name=f"Camera Ray ({angle})",
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
