# Road Profile Database & Upload System

> **[DE] Deutsche Version:** Für vollständige Anweisungen auf Deutsch, siehe [README.de.md](README.de.md)
> **[EN] English Version:** You are reading it!

Welcome to the Road Profile Database & Upload System exercise! This is a **group assignment** where you will extend an existing Dash application with database persistence, multi-profile selection, and file upload capabilities.

> **Note:** Error messages from automated checks (GitHub Actions workflows) appear in **both English and German**.

## 📚 Learning Objectives

By completing this exercise, you will:

1. **Integrate databases** with web applications (SQLite with FastAPI/SQLModel OR TinyDB)
2. **Design and implement REST APIs** (if using FastAPI approach)
3. **Build multi-page Dash applications** with file upload and data validation
4. **Apply Pydantic validation** for data integrity
5. **Practice collaborative development** with feature branches and code reviews
6. **Achieve high test coverage** (90%+ on new features)
7. **Document implementation decisions** and technical planning

## 🎯 Assignment Overview

You will extend the existing road profile viewer application with these features:

**Current State:**
- Single default road profile (hard-coded)
- Camera position and sight ray visualization
- Intersection calculation and display

**Your Task - Add:**
1. **Dropdown selector** to choose from multiple stored road profiles
2. **Database backend** to persist road profiles
3. **Upload page** where users can add new profiles via JSON files
4. **Profile preview** showing graph before saving
5. **Profile renaming** capability on upload page
6. **Data validation** using Pydantic models

## 🏗️ Technical Approaches

You can choose between two implementation approaches with different point values:

### Approach 1: FastAPI + SQLModel + SQLite (5 points possible)

**Architecture:**
- **Backend**: FastAPI REST API with endpoints for CRUD operations
- **Database**: SQLite with SQLModel ORM
- **Frontend**: Dash app consuming the API
- **Migration**: Database initialization and seeding scripts

**Why this approach:**
- Industry-standard architecture (separation of concerns)
- Scalable and testable
- More sophisticated, unlocks full 5 points

**Key Components:**
```
src/road_profile_viewer/
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   └── routes.py        # API endpoints
├── database/
│   ├── __init__.py
│   ├── models.py        # SQLModel database models
│   └── connection.py    # Database setup
├── models.py            # Pydantic validation models
└── visualization.py     # Updated Dash app with API calls
```

### Approach 2: TinyDB (4 points possible)

**Architecture:**
- **Database**: TinyDB (JSON-based, no separate backend needed)
- **Frontend**: Dash app directly accessing TinyDB
- **Simpler**: All code integrated in Dash application

**Why this approach:**
- Lightweight and simple
- No API layer needed
- Good for learning database basics

**Key Components:**
```
src/road_profile_viewer/
├── database/
│   ├── __init__.py
│   └── db.py            # TinyDB operations
├── models.py            # Pydantic validation models
└── visualization.py     # Updated Dash app with TinyDB
```

**Choose based on your team's:**
- Time availability
- Learning goals (want to learn FastAPI?)
- Ambition level (aiming for full 5 points?)

## 📋 Requirements

### 1. Implementation (2 points)

#### Dropdown Selector (0.8 points)
- [ ] Add dropdown component on main page to select road profiles
- [ ] Dropdown lists all available profiles by name
- [ ] Selecting a profile updates the visualization
- [ ] Default profile pre-selected on app startup

#### Upload Page (1.2 points)
- [ ] Create new page/route in Dash app (`/upload`)
- [ ] File upload component accepting JSON files
- [ ] Preview graph showing uploaded profile before saving
- [ ] Text input to rename the profile
- [ ] Confirm button to save to database
- [ ] Success/error messages after upload
- [ ] Navigation between main page and upload page

### 2. Backend & Database (1.5 points)

#### Database Schema (0.5 points)
- [ ] Road profile model with fields: `id`, `name`, `x_coordinates`, `y_coordinates`
- [ ] Unique constraint on profile names
- [ ] Proper data types (list/array for coordinates)

#### Database Operations (0.5 points)
- [ ] Create (insert new profile)
- [ ] Read (get all profiles, get by name/id)
- [ ] Update (optional, but recommended)
- [ ] Delete (optional, but recommended)

#### Migration/Seed (0.5 points)
- [ ] Script to initialize database
- [ ] Seed default profile on first run
- [ ] Database file in `.gitignore` (not committed)

**FastAPI Approach Bonus (+1 point):**
- [ ] REST API endpoints: `GET /profiles`, `POST /profiles`, `GET /profiles/{id}`
- [ ] Proper error handling (404, 409 conflict, 422 validation)
- [ ] FastAPI automatic documentation (`/docs`)
- [ ] Separation of concerns (API layer separate from Dash)

### 3. Data Validation (included in Implementation points)

- [ ] Pydantic model matching example JSON schema
- [ ] Validation rules:
  - Name: 1-100 characters, non-empty
  - `x_coordinates` and `y_coordinates`: same length, at least 2 points
  - Coordinates must be numeric (floats)
- [ ] Clear error messages on validation failure
- [ ] Example JSON file provided in `docs/example-road-profile.json`

### 4. Testing (0.5 points)

- [ ] **90%+ C1 coverage** on all new features
- [ ] Unit tests for:
  - Database operations (CRUD)
  - API endpoints (if FastAPI approach)
  - Pydantic validation (valid and invalid cases)
  - Upload functionality
  - Dropdown selection logic
- [ ] Integration tests for upload workflow
- [ ] Coverage report generated by pytest-cov

### 5. Git Workflow & Collaboration (0.5 points)

- [ ] **At least 2 feature branches** with descriptive names (e.g., `feature/database-setup`, `feature/upload-page`)
- [ ] **Multiple contributors**: Each branch has commits from at least one team member
- [ ] **Incremental commits** with descriptive messages (>20 characters)
- [ ] **Implementation plan** documented in `docs/implementation-plan.md`
- [ ] **LLM prompts** (if used) saved in `docs/llm-prompts/` folder

### 6. Code Review (0.5 points)

- [ ] All features implemented via **Pull Requests**
- [ ] PRs use the provided **PR description template**
- [ ] Each PR reviewed by at least **one other team member**
- [ ] Reviews include substantive feedback (not just "LGTM")
- [ ] All CI checks pass before merge

## 👥 Group Work

### Team Setup
- **Group size**: 2-4 students
- **Formation**: Self-organized or instructor-assigned
- **Repository**: One repository per group via GitHub Classroom

### Collaboration Requirements

1. **Implementation Plan** (`docs/implementation-plan.md`):
   ```markdown
   # Implementation Plan

   ## Team Members
   - [Name] - [Role/Responsibilities]
   - [Name] - [Role/Responsibilities]

   ## Technical Decision
   - [ ] FastAPI + SQLModel + SQLite (5 points)
   - [ ] TinyDB (4 points)

   ## Feature Breakdown
   | Feature | Branch | Assignee | Status |
   |---------|--------|----------|--------|
   | Database setup | feature/database | [Name] | ✅ |
   | Upload page | feature/upload | [Name] | 🔄 |

   ## Testing Strategy
   [How you'll achieve 90% coverage]
   ```

2. **Branch Strategy**:
   - Minimum 2 feature branches (recommendation: 3-4)
   - Suggested branches:
     - `feature/database-setup` - Database schema, models, seed script
     - `feature/dropdown-selector` - Main page dropdown integration
     - `feature/upload-page` - New upload page with preview
     - `feature/api-endpoints` - FastAPI routes (if applicable)

3. **Work Distribution**:
   - Each team member works on at least one feature branch
   - Use GitHub Issues to track tasks
   - Daily standups (document in issue comments)

4. **LLM Usage** (Optional but Encouraged):
   - If you use ChatGPT, Claude, or other LLMs, save prompts
   - Create folder: `docs/llm-prompts/`
   - File naming: `YYYY-MM-DD-feature-name.md`
   - Include both prompts and relevant responses

## 🚀 Getting Started

### Step 1: Accept Assignment & Form Team

```bash
# Each team member accepts the GitHub Classroom assignment
# First member creates a new team
# Other members join the existing team

# Clone the team repository
git clone https://github.com/hs-aalen-software-engineering/road-profile-db-TEAM-NAME.git
cd road-profile-db-TEAM-NAME
```

### Step 2: Understand Current Application

```bash
# Install dependencies
uv sync

# Run the current app to see what it does
uv run python -m road_profile_viewer

# Open browser: http://127.0.0.1:8050/
# Play with the angle input to see ray intersection
```

**Explore the code:**
- `src/road_profile_viewer/main.py` - Entry point
- `src/road_profile_viewer/visualization.py` - Dash UI
- `src/road_profile_viewer/geometry.py` - Intersection calculations
- `src/road_profile_viewer/road.py` - Current profile generation

### Step 3: Create Implementation Plan

**Team meeting to decide:**
1. Which approach? (FastAPI or TinyDB)
2. Who does what? (assign features to members)
3. What are the branch names?
4. How to achieve 90% test coverage?

**Document in** `docs/implementation-plan.md`

```bash
# Create docs folder if it doesn't exist
mkdir docs

# Create your implementation plan (use provided template)
# Commit the plan
git add docs/implementation-plan.md
git commit -m "Add implementation plan for database and upload features"
git push origin main
```

### Step 4: Set Up Development Environment

**Create starter files:**

```bash
# 1. Create Pydantic models file
# src/road_profile_viewer/models.py already has a starter!

# 2. Review example JSON format
cat docs/example-road-profile.json
```

**Example JSON format** (`docs/example-road-profile.json`):
```json
{
  "name": "mountain_road",
  "x_coordinates": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0],
  "y_coordinates": [0.0, 2.0, 5.0, 8.0, 6.0, 4.0]
}
```

### Step 5: Implement Features (Team Collaboration)

**Member 1: Database Setup**

```bash
# Create feature branch
git checkout -b feature/database-setup

# Create database module structure
# For FastAPI approach:
mkdir -p src/road_profile_viewer/database
touch src/road_profile_viewer/database/__init__.py
touch src/road_profile_viewer/database/models.py
touch src/road_profile_viewer/database/connection.py

# For TinyDB approach:
mkdir -p src/road_profile_viewer/database
touch src/road_profile_viewer/database/__init__.py
touch src/road_profile_viewer/database/db.py

# Implement database models and operations
# Add seed script to insert default profile

# Commit incrementally
git add .
git commit -m "Add database models and connection setup"

# Write tests
git add tests/test_database.py
git commit -m "Add database operation tests (90% coverage)"

# Push and create PR
git push -u origin feature/database-setup
gh pr create --title "Add database setup with seed script" \
  --body "[Use provided PR template]"
```

**Member 2: Dropdown Selector**

```bash
git checkout -b feature/dropdown-selector

# Update visualization.py to:
# 1. Add dropdown component
# 2. Fetch profiles from database
# 3. Update callback to handle profile selection
# 4. Load selected profile data

# Commit and test
# Push and create PR
```

**Member 3: Upload Page**

```bash
git checkout -b feature/upload-page

# Create new page in Dash app:
# 1. Add dcc.Upload component
# 2. Add preview graph
# 3. Add rename text input
# 4. Add confirm button
# 5. Add navigation

# Commit, test, PR
```

**Member 4 (if 4-person team): API Layer** (FastAPI only)

```bash
git checkout -b feature/api-endpoints

# Create FastAPI app:
mkdir -p src/road_profile_viewer/api
# Implement REST endpoints
# Add API tests

# Commit, test, PR
```

### Step 6: Code Review Process

**For each PR:**

1. **Author**: Ensure CI checks pass before requesting review
2. **Reviewer**: Check the PR using the template checklist
3. **Reviewer**: Test locally:
   ```bash
   git fetch origin
   git checkout feature/database-setup
   uv sync
   uv run pytest --cov=src --cov-report=term-missing
   uv run python -m road_profile_viewer
   ```
4. **Reviewer**: Leave comments, request changes, or approve
5. **Author**: Address feedback, push updates
6. **Merge**: Only after approval + all CI checks pass

### Step 7: Integration & Testing

```bash
# After all features merged, verify end-to-end:

# 1. Fresh install
uv sync

# 2. Check coverage on all new code
uv run pytest --cov=src --cov-report=html --cov-report=term
# Open htmlcov/index.html to see detailed coverage

# 3. Manual testing checklist:
# - [ ] App starts without errors
# - [ ] Dropdown shows default profile
# - [ ] Can select different profiles from dropdown
# - [ ] Upload page accessible
# - [ ] Can upload valid JSON file
# - [ ] Preview graph appears correctly
# - [ ] Can rename profile before saving
# - [ ] Profile appears in dropdown after upload
# - [ ] Invalid JSON shows error message
# - [ ] Database persists after app restart

# 4. Code quality checks
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## 🔍 Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Implementation** | 2.0 | Dropdown (0.8) + Upload page with preview/rename (1.2) |
| **Backend/Database** | 1.5 | Schema (0.5) + CRUD operations (0.5) + Seed script (0.5) |
| **Testing** | 0.5 | 90%+ C1 coverage on new features |
| **Git Workflow** | 0.5 | ≥2 branches, clear commits, implementation plan |
| **Code Review** | 0.5 | PRs with template, peer reviews, CI passes |
| **BONUS: FastAPI** | +1.0 | REST API + proper error handling + separation of concerns |
| **Total (TinyDB)** | **5.0** | Maximum achievable with TinyDB approach |
| **Total (FastAPI)** | **6.0** | Capped at 5.0 (bonus allows error margin) |

### Automated Checks

GitHub Actions will automatically verify:

- ✅ **Code Quality**: Ruff linting, Pyright type checking
- ✅ **Test Coverage**: pytest-cov with 90% threshold on new code
- ✅ **Git Workflow**: ≥2 feature branches, multiple authors, commit quality
- ✅ **PR Reviews**: All PRs approved before merge
- ✅ **Structure**: Required files exist (database/, models.py, etc.)

### Manual Evaluation

Instructor will:
- Clone your repository
- Run `uv sync` and `uv run python -m road_profile_viewer`
- Test all features (dropdown, upload, preview, persistence)
- Review implementation plan quality
- Check code architecture decisions
- Verify testing strategy

## 📄 Required Files Checklist

**Documentation:**
- [ ] `docs/implementation-plan.md` - Your team's plan
- [ ] `docs/example-road-profile.json` - Provided example (included)
- [ ] `docs/llm-prompts/` - LLM prompts (if used)

**Code (varies by approach):**

**Both approaches:**
- [ ] `src/road_profile_viewer/models.py` - Pydantic validation models
- [ ] Updated `src/road_profile_viewer/visualization.py` - Dropdown + upload page

**FastAPI approach:**
- [ ] `src/road_profile_viewer/api/main.py` - FastAPI app
- [ ] `src/road_profile_viewer/api/routes.py` - API endpoints
- [ ] `src/road_profile_viewer/database/models.py` - SQLModel models
- [ ] `src/road_profile_viewer/database/connection.py` - DB setup

**TinyDB approach:**
- [ ] `src/road_profile_viewer/database/db.py` - TinyDB operations

**Tests:**
- [ ] `tests/test_models.py` - Pydantic validation tests
- [ ] `tests/test_database.py` - Database operation tests
- [ ] `tests/test_upload.py` - Upload functionality tests
- [ ] `tests/test_api.py` - API endpoint tests (FastAPI only)

## ❓ Troubleshooting

### "How do I run both FastAPI and Dash?"

If using FastAPI approach, you have two options:

**Option 1: Separate processes** (Development)
```bash
# Terminal 1: Run FastAPI backend
uv run uvicorn road_profile_viewer.api.main:app --reload --port 8000

# Terminal 2: Run Dash frontend
uv run python -m road_profile_viewer
```

**Option 2: Integrated** (Production-like)
- Mount Dash app in FastAPI using `WSGIMiddleware`
- Single process, single port
- More complex but cleaner deployment

### "Database file not found"

Make sure your seed script runs on first startup:

```python
# In database setup
if not Path("profiles.db").exists():
    init_database()
    seed_default_profile()
```

### "Coverage below 90%"

Focus on testing YOUR new code:
```bash
# See what's not covered
uv run pytest --cov=src/road_profile_viewer/database --cov-report=term-missing

# Common untested areas:
# - Error handling paths
# - Edge cases in validation
# - Database exceptions
```

### "Import errors after adding database module"

Make sure `__init__.py` exists in all new folders:
```
src/road_profile_viewer/database/
├── __init__.py  ← MUST EXIST
├── models.py
└── connection.py
```

### "Dropdown not updating"

Check your Dash callback:
```python
@app.callback(
    Output('road-graph', 'figure'),
    Input('profile-dropdown', 'value')  # Listen to dropdown changes
)
def update_graph(selected_profile_name):
    # Fetch profile from database by name
    # Update graph with new profile
    pass
```

### "JSON validation always fails"

Verify your Pydantic model matches the example JSON:
```python
# Must handle list[float], not str
x_coordinates: list[float]  # ✅
x_coordinates: str          # ❌
```

## 📚 Technical Resources

### FastAPI + SQLModel Approach
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Validation](https://docs.pydantic.dev/latest/)

### TinyDB Approach
- [TinyDB Documentation](https://tinydb.readthedocs.io/)
- [TinyDB Tutorial](https://tinydb.readthedocs.io/en/latest/getting-started.html)

### Dash Multi-Page Apps
- [Dash Pages](https://dash.plotly.com/urls)
- [Dash Upload Component](https://dash.plotly.com/dash-core-components/upload)

### Testing
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Coverage](https://pytest-cov.readthedocs.io/)

## 🆘 Getting Help

1. **Check documentation** - Links above
2. **Review implementation plan** - Did you account for this?
3. **Ask in team chat** - Collaborate with teammates
4. **Check CI error messages** - They're detailed!
5. **Office hours** - Instructor available for questions
6. **GitHub Discussions** - Ask publicly, help others

## 🎉 Success Criteria

Your assignment is complete when:

- ✅ All features work as demonstrated in person
- ✅ All automated CI checks pass
- ✅ Test coverage ≥90% on new code
- ✅ All PRs reviewed and merged
- ✅ Implementation plan documents your decisions
- ✅ Code quality meets standards (Ruff, Pyright)

**Congratulations on building a full-stack database application!**

---

**Assignment Created**: 2025-11-19
**Course**: Software Engineering - HS Aalen
**Instructor**: Dominik Mueller
**Max Points**: 5.0 (FastAPI approach can earn bonus for margin of error)
