# Road Profile Viewer - Requirements Specification

## 1. Introduction

### 1.1 Purpose

This document defines the requirements for the Road Profile Viewer application, an interactive tool for visualizing road profiles and calculating camera ray intersections. Requirements are organized following IEEE/ISO 29148 guidelines, distinguishing between stakeholder-level and implementation-level (derived) requirements.

### 1.2 Scope

The Road Profile Viewer is a full-stack web application consisting of:
- **Frontend**: Dash/Plotly interactive visualization (port 8050)
- **Backend**: FastAPI REST API (port 8000)
- **Database**: SQLite with SQLModel ORM

### 1.3 Stakeholders

| Stakeholder | Role | Primary Concerns |
|-------------|------|------------------|
| Road Engineer | End User | Accuracy of intersection calculations, ease of use |
| Lab Manager | Customer | Training time, reliability |
| IT Administrator | Operations | Installation, maintenance, deployment |
| Developer | Internal | Code quality, testability, maintainability |
| QA Engineer | Internal | Test coverage, requirement traceability |

### 1.4 Document Conventions

#### Requirement ID Formats

| Format | Type | Description |
|--------|------|-------------|
| **FR-XXX** | Functional Requirement | What the system does (stakeholder level) |
| **NFR-XXX** | Non-Functional Requirement | Quality attributes (performance, maintainability) |
| **REQ-GEOM-XXX** | Derived - Geometry | Implementation requirements for geometry module |
| **REQ-ROAD-XXX** | Derived - Road | Implementation requirements for road generation |
| **REQ-API-XXX** | Derived - API | Implementation requirements for REST API |
| **REQ-DB-XXX** | Derived - Database | Implementation requirements for database layer |
| **REQ-VAL-XXX** | Derived - Validation | Implementation requirements for data validation |
| **REQ-VIS-XXX** | Derived - Visualization | Implementation requirements for UI |

---

## 2. Functional Requirements (FR-*)

Functional requirements define **what** the system does from the stakeholder's perspective.

### FR-001: Interactive Road Profile Visualization

**Description**: The system shall display an interactive road profile visualization showing the road surface, camera position, camera ray, and intersection point.

**Acceptance Criteria**:
- Chart displays road profile as a continuous line
- Camera position is shown as a distinct marker
- Camera ray is displayed at the configured angle
- Intersection point (when found) is highlighted
- Graph updates dynamically when parameters change

**Priority**: High
**Related Tests**: `tests/test_visualization.py`

---

### FR-002: Camera Ray-Road Intersection Calculation

**Description**: The system shall calculate the intersection point between the camera ray and the road profile, returning coordinates and distance.

**Acceptance Criteria**:
- Returns (x, y, distance) when intersection exists
- Returns (None, None, None) when no intersection
- Distance is the Euclidean distance from camera to intersection
- Handles edge cases (vertical rays, parallel segments)

**Priority**: High
**Related Tests**: `tests/test_geometry.py`

---

### FR-003: Road Profile Generation

**Description**: The system shall generate realistic road profiles using clothoid (Euler spiral) approximation.

**Acceptance Criteria**:
- Profiles start at origin (0, 0)
- X-coordinates are monotonically increasing
- Profile ends at specified x_max value
- Generates specified number of points

**Priority**: Medium
**Related Tests**: `tests/test_road.py`

---

### FR-004: Profile Selection

**Description**: The system shall allow users to select road profiles from a dropdown menu.

**Acceptance Criteria**:
- Dropdown displays all available profiles from database
- "Default (Generated)" option always available
- Selection updates visualization immediately
- Refresh button reloads profiles from API

**Priority**: High
**Related Tests**: `tests/test_visualization.py`

---

### FR-005: JSON File Upload

**Description**: The system shall allow users to upload road profile data from JSON files.

**Acceptance Criteria**:
- Accepts JSON files with x_coordinates and y_coordinates arrays
- Validates file format before processing
- Displays preview of uploaded profile
- Allows renaming profile before saving
- Shows clear error messages for invalid files

**Priority**: Medium
**Related Tests**: `tests/test_visualization.py`

---

### FR-006: Database Persistence

**Description**: The system shall persist road profiles in a database for retrieval across sessions.

**Acceptance Criteria**:
- Profiles stored with unique name identifier
- Coordinates preserved with full precision
- Profiles retrievable by ID or name
- Supports create, read, update, delete operations

**Priority**: High
**Related Tests**: `tests/database/test_crud.py`, `tests/database/test_connection.py`

---

### FR-007: REST API for Profile Management

**Description**: The system shall provide RESTful API endpoints for profile CRUD operations.

**Acceptance Criteria**:
- `GET /profiles/` returns list of all profiles
- `POST /profiles/` creates new profile (201 response)
- `GET /profiles/{id}` returns specific profile or 404
- `PUT /profiles/{id}` updates existing profile
- `DELETE /profiles/{id}` removes profile (204 response)
- OpenAPI documentation available at `/docs`

**Priority**: High
**Related Tests**: `tests/api/test_routes.py`

---

### FR-008: Profile Data Validation

**Description**: The system shall validate profile data before storage, rejecting invalid inputs with clear error messages.

**Acceptance Criteria**:
- Profile name: 1-100 characters, non-empty after trimming
- Coordinates: minimum 2 points required
- X and Y arrays must have equal length
- Invalid data returns 422 with validation errors

**Priority**: High
**Related Tests**: `tests/api/test_validation.py`

---

### FR-009: Default Profile Seeding

**Description**: The system shall seed a default road profile on first run for immediate use.

**Acceptance Criteria**:
- Default profile created automatically on first startup
- Profile named "Default Clothoid Profile"
- Contains 100 points of clothoid-generated data
- Seeding is idempotent (safe to call multiple times)

**Priority**: Medium
**Related Tests**: `tests/database/test_seed.py`

---

### FR-010: Intersection Information Display

**Description**: The system shall display intersection distance and coordinates to the user.

**Acceptance Criteria**:
- Shows "Intersection found at (x, y)" when intersection exists
- Displays "Distance: X units" with calculated distance
- Shows "No intersection found" when ray doesn't intersect

**Priority**: Medium
**Related Tests**: `tests/test_visualization.py`

---

## 3. Non-Functional Requirements (NFR-*)

Non-functional requirements define **quality attributes** - how well the system performs its functions.

### NFR-001: Test Coverage

**Description**: The system shall maintain test coverage above 90% for all source code.

**Measurable Criteria**: pytest-cov reports >= 90% line coverage
**Related Tests**: All test files

---

### NFR-002: Type Safety

**Description**: The system shall use type hints for all public functions, passing strict type checking.

**Measurable Criteria**: Pyright passes in strict mode with no errors
**Verification**: `pyright src/`

---

### NFR-003: Code Style

**Description**: The system shall follow PEP8 style guidelines with consistent formatting.

**Measurable Criteria**: Ruff linting passes with no errors
**Verification**: `ruff check src/`

---

### NFR-004: HTTP Status Codes

**Description**: The API shall return semantically correct HTTP status codes for all operations.

**Measurable Criteria**:
- 200: Successful GET/PUT
- 201: Successful POST (created)
- 204: Successful DELETE
- 404: Resource not found
- 409: Conflict (duplicate name)
- 422: Validation error

**Related Tests**: `tests/api/test_routes.py`

---

### NFR-005: Idempotency

**Description**: Database initialization and seeding operations shall be idempotent.

**Measurable Criteria**: Repeated calls produce same result without errors
**Related Tests**: `tests/database/test_seed.py`, `tests/database/test_connection.py`

---

### NFR-006: Unique Profile Names

**Description**: Profile names shall be unique within the system.

**Measurable Criteria**: Duplicate names rejected with 409 Conflict
**Related Tests**: `tests/database/test_crud.py`, `tests/api/test_routes.py`

---

## 4. Derived Requirements

Derived requirements emerge from implementation decisions and are tested at the unit level. They trace back to parent functional/non-functional requirements.

### 4.1 Geometry Module (REQ-GEOM-*)

| ID | Requirement | Parent | Test |
|----|-------------|--------|------|
| REQ-GEOM-001 | `calculate_ray_line()` shall handle vertical rays (angle=90) by limiting ray length to 20 units | FR-002 | `test_calculate_ray_line_vertical_ray` |
| REQ-GEOM-002 | `calculate_ray_line()` shall limit upward rays (angle < 0 or > 90) to 20 units | FR-002 | `test_calculate_ray_line_upward_ray_*` |
| REQ-GEOM-003 | `calculate_ray_line()` shall extend downward rays to x_max | FR-002 | `test_calculate_ray_line_downward_ray` |
| REQ-GEOM-004 | `find_intersection()` shall return (None, None, None) for non-intersecting rays | FR-002 | `test_find_intersection_*` |
| REQ-GEOM-005 | `find_intersection()` shall skip road segments behind the camera | FR-002 | `test_find_intersection_skips_segments_behind_camera` |
| REQ-GEOM-006 | `find_intersection()` shall handle parallel ray and road segment | FR-002 | `test_find_intersection_parallel_ray_and_segment` |
| REQ-GEOM-007 | Intersection distance shall be positive when found | FR-002 | `test_find_intersection_finds_intersection_for_normal_angle` |

### 4.2 Road Module (REQ-ROAD-*)

| ID | Requirement | Parent | Test |
|----|-------------|--------|------|
| REQ-ROAD-001 | `generate_road_profile()` shall return arrays of exactly num_points length | FR-003 | `test_generate_road_profile_*` |
| REQ-ROAD-002 | Road profile shall start at coordinates (x=0, y=0) | FR-003 | `test_generate_road_profile_default_parameters` |
| REQ-ROAD-003 | Road profile x-coordinates shall be monotonically increasing | FR-003 | `test_generate_road_profile_x_coordinates_monotonic` |
| REQ-ROAD-004 | Road profile shall end at x=x_max | FR-003 | `test_generate_road_profile_*_x_max` |

### 4.3 API Module (REQ-API-*)

| ID | Requirement | Parent | Test |
|----|-------------|--------|------|
| REQ-API-001 | `GET /profiles/` shall return list of all profiles with correct schema | FR-007 | `TestListProfiles` |
| REQ-API-002 | `POST /profiles/` shall create profile and return 201 with created resource | FR-007 | `TestCreateProfile` |
| REQ-API-003 | `GET /profiles/{id}` shall return profile or 404 for non-existent ID | FR-007 | `TestGetProfile` |
| REQ-API-004 | `PUT /profiles/{id}` shall update profile or return 404/409 | FR-007 | `TestUpdateProfile` |
| REQ-API-005 | `DELETE /profiles/{id}` shall delete profile and return 204, or 404 | FR-007 | `TestDeleteProfile` |
| REQ-API-006 | Duplicate profile names shall return 409 Conflict | NFR-006 | `test_create_profile_duplicate_name_conflict` |
| REQ-API-007 | IntegrityError race conditions shall be handled and return 409 | NFR-006 | `TestIntegrityErrorHandling` |

### 4.4 Database Module (REQ-DB-*)

| ID | Requirement | Parent | Test |
|----|-------------|--------|------|
| REQ-DB-001 | `create_profile()` shall return profile with assigned auto-increment ID | FR-006 | `test_create_profile_returns_profile_with_id` |
| REQ-DB-002 | `create_profile()` shall raise IntegrityError for duplicate names | NFR-006 | `test_create_profile_duplicate_name_raises_error` |
| REQ-DB-003 | `get_profile()` shall return None for non-existent IDs | FR-006 | `test_get_profile_returns_none_for_nonexistent_id` |
| REQ-DB-004 | `get_profile_by_name()` shall be case-sensitive | FR-006 | `test_get_profile_by_name_is_case_sensitive` |
| REQ-DB-005 | `delete_profile()` shall return False for non-existent profiles | FR-006 | `test_delete_profile_returns_false_for_nonexistent` |
| REQ-DB-006 | `RoadProfileDB` shall serialize/deserialize coordinates via JSON | FR-006 | `test_get_*_coordinates_deserializes_json` |
| REQ-DB-007 | Database engine creation shall be cached for performance | FR-006 | `test_reset_engine_clears_cache` |
| REQ-DB-008 | `seed_default_profile()` shall be idempotent | NFR-005 | `test_seed_default_profile_is_idempotent` |

### 4.5 Validation Module (REQ-VAL-*)

| ID | Requirement | Parent | Test |
|----|-------------|--------|------|
| REQ-VAL-001 | Profile name shall be 1-100 characters | FR-008 | `test_invalid_empty_name`, `test_invalid_name_too_long` |
| REQ-VAL-002 | Profile name shall be stripped of leading/trailing whitespace | FR-008 | `test_name_gets_stripped` |
| REQ-VAL-003 | Whitespace-only names shall be rejected | FR-008 | `test_invalid_whitespace_name` |
| REQ-VAL-004 | Coordinates shall have minimum 2 points | FR-008 | `test_invalid_single_point`, `test_invalid_empty_coordinates` |
| REQ-VAL-005 | x and y coordinate arrays shall have equal length | FR-008 | `test_invalid_mismatched_lengths` |

### 4.6 Visualization Module (REQ-VIS-*)

| ID | Requirement | Parent | Test |
|----|-------------|--------|------|
| REQ-VIS-001 | Dash app shall have URL routing for home (/) and upload (/upload) pages | FR-001, FR-005 | `test_create_dash_app_*` |
| REQ-VIS-002 | Graph shall update when angle input changes | FR-001 | `test_update_graph_*` |
| REQ-VIS-003 | Graph shall show "No intersection found" for non-intersecting angles | FR-010 | `test_update_graph_with_angle_no_intersection` |
| REQ-VIS-004 | Profile dropdown shall refresh from API on button click | FR-004 | `test_load_profiles_api_*` |
| REQ-VIS-005 | Upload preview shall display profile before saving | FR-005 | `test_update_preview` |

---

## 5. Traceability Matrix

### 5.1 Functional Requirements to Tests

| Requirement | Test File(s) | Test Count |
|-------------|--------------|------------|
| FR-001 | `test_visualization.py` | ~8 |
| FR-002 | `test_geometry.py` | ~13 |
| FR-003 | `test_road.py` | ~11 |
| FR-004 | `test_visualization.py` | ~5 |
| FR-005 | `test_visualization.py` | ~4 |
| FR-006 | `test_crud.py`, `test_connection.py`, `test_models.py` | ~46 |
| FR-007 | `test_routes.py` | ~30 |
| FR-008 | `test_validation.py` | ~20 |
| FR-009 | `test_seed.py` | ~9 |
| FR-010 | `test_visualization.py` | ~3 |

### 5.2 Non-Functional Requirements to Tests

| Requirement | Verification Method |
|-------------|---------------------|
| NFR-001 | `pytest --cov` (automated in CI) |
| NFR-002 | `pyright src/` (automated in CI) |
| NFR-003 | `ruff check src/` (automated in CI) |
| NFR-004 | `test_routes.py` (status code assertions) |
| NFR-005 | `test_seed.py`, `test_connection.py` |
| NFR-006 | `test_crud.py`, `test_routes.py` |

---

## 6. GitHub Issues Suggestions

The following issues are suggested for future requirements engineering and feature development work.

### 6.1 Documentation & Traceability

- **Add requirements coverage report to CI**: Generate a report showing which requirements have tests and identify gaps
- **Create traceability matrix automation**: Script to extract `@pytest.mark.requirement` markers and generate traceability table
- **Add requirement IDs to source code docstrings**: Link implementation functions to their derived requirements in code

### 6.2 Feature Enhancements

- **FR-011: Profile export functionality**: Allow users to export profiles as JSON/CSV files
- **FR-012: Profile deletion from UI**: Add delete button to profile management interface
- **FR-013: Profile editing capability**: Allow modifying existing profile coordinates
- **NFR-007: Response time monitoring**: Add performance metrics for API calls (<100ms target)

### 6.3 Testing Improvements

- **Add E2E tests for full user workflows**: Selenium/Playwright tests for complete upload-to-visualization flow
- **Add performance benchmarks for geometry calculations**: Verify calculation performance with large profiles
- **Create mutation testing baseline**: Establish test quality metrics using mutmut or similar tools

### 6.4 Requirements Gaps Identified

- **Document camera position requirements**: Define valid ranges for camera_x and camera_y parameters
- **Specify coordinate precision requirements**: Define acceptable float precision for profile coordinates
- **Define maximum profile size limit**: Add NFR for maximum number of points allowed in a profile

---

## 7. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-17 | Claude Code | Initial requirements specification |
