# Refactoring Exercise: From Monolith to Modules

> **[DE] Deutsche Version:** Für vollständige Anweisungen auf Deutsch, siehe [README.de.md](README.de.md)
> **[EN] English Version:** You are reading it!

Welcome to the refactoring exercise! This assignment reinforces the concepts from **Lecture 4: Refactoring - From Monolith to Modules**.

> **Note:** Error messages from automated checks (GitHub Actions workflows) appear in **both English and German**.

## 📚 Learning Objectives

By completing this exercise, you will:

1. **Apply the refactoring workflow** from Lecture 4 to transform monolithic code into modular components
2. **Use feature branch development** (Lecture 3 Part 1) with proper Git workflow
3. **Follow CI/CD practices** (Lecture 3 Part 2) with automated quality checks
4. **Practice incremental commits** showing step-by-step refactoring progression
5. **Participate in peer code review** to learn from each other

## 🎯 Assignment Overview

You will refactor the monolithic `src/road_profile_viewer/main.py` (390 lines) into four focused modules:

- `geometry.py` - Pure math functions (ray intersection calculations)
- `road.py` - Road profile generation
- `visualization.py` - Dash UI layer
- `main.py` - Simplified entry point (~20 lines)

**This is exactly what you learned in Lecture 4!** Follow the lecture step-by-step.

## 📋 Requirements

### 1. Git Workflow (25 points)

- [ ] Create feature branch: `feature/refactor-to-modules`
- [ ] Make **at least 3 incremental commits** (one per module extraction)
- [ ] Write **descriptive commit messages** (> 10 characters)
- [ ] Create a **Pull Request** from your feature branch to `main`
- [ ] **Do NOT merge** until all checks pass and you have peer approval

### 2. Code Structure (35 points)

- [ ] Create `geometry.py` with:
  - `calculate_ray_line()` function
  - `find_intersection()` function
  - Proper docstrings and type hints

- [ ] Create `road.py` with:
  - `generate_road_profile()` function
  - Proper docstrings

- [ ] Create `visualization.py` with:
  - `create_dash_app()` function
  - All Dash UI code
  - Imports from `geometry` and `road`

- [ ] Simplify `main.py` to:
  - **Less than 30 lines**
  - Only imports from `visualization`
  - Only contains `main()` function and `if __name__ == '__main__'`

### 3. Code Quality (25 points)

- [ ] **Ruff linting** passes (no style violations)
- [ ] **Ruff formatting** passes (code is properly formatted)
- [ ] **Pyright** passes (no type errors)
- [ ] **Proper imports** with no circular dependencies
- [ ] **Dependency flow**: `main → visualization → geometry/road`

### 4. Peer Review (15 points)

- [ ] **Request review** from a classmate
- [ ] **Receive approval** before merging
- [ ] **Review another student's PR** and provide constructive feedback

## 🚀 Step-by-Step Instructions

### Step 1: Clone Your Repository

```bash
# GitHub Classroom creates a repo for you - clone it
git clone https://github.com/hs-aalen-software-engineering/refactoring-YOUR-USERNAME.git
cd refactoring-YOUR-USERNAME
```

### Step 2: Create Feature Branch

```bash
# Make sure you're on main and up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/refactor-to-modules

# Verify you're on the new branch
git branch
```

### Step 3: Extract Geometry Module

**Follow Lecture 4, Section 6.2**

1. Create `geometry.py` in the **src/road_profile_viewer/ directory** (same level as `src/road_profile_viewer/main.py`)
2. Copy `calculate_ray_line()` and `find_intersection()` from `src/road_profile_viewer/main.py`
3. Add proper imports: `import numpy as np`
4. Add type hints (see Lecture 4 example)
5. Test that it works (no errors when importing)

**Commit your progress:**

```bash
git add src/road_profile_viewer/geometry.py
git commit -m "Extract geometry functions to geometry.py

- Move calculate_ray_line() and find_intersection()
- Add type hints and docstrings
- Prepare for modular testing"
```

### Step 4: Extract Road Module

**Follow Lecture 4, Section 6.3**

1. Create `road.py` in the **src/road_profile_viewer/ directory**
2. Copy `generate_road_profile()` from `src/road_profile_viewer/main.py`
3. Add proper imports and docstrings

**Commit your progress:**

```bash
git add src/road_profile_viewer/road.py
git commit -m "Extract road generation to road.py

- Move generate_road_profile()
- Separate data generation from geometry and UI"
```

### Step 5: Extract Visualization Module

**Follow Lecture 4, Section 6.4**

1. Create `visualization.py` in the **src/road_profile_viewer/ directory**
2. Copy `create_dash_app()` and all UI code from `src/road_profile_viewer/main.py`
3. **Add imports using absolute imports:**
   ```python
   import numpy as np
   import plotly.graph_objects as go
   from dash import Dash, Input, Output, dcc, html

   from road_profile_viewer.geometry import find_intersection
   from road_profile_viewer.road import generate_road_profile
   ```

   **⚠️ IMPORTANT:** Use **absolute imports** (not relative imports with `.`) to avoid `ImportError: attempted relative import with no known parent package` when running the module directly.

   **Why absolute imports?** When you run a Python file directly as a script, Python doesn't recognize it as part of a package, so relative imports (with `.`) fail. Absolute imports always work.

**Commit your progress:**

```bash
git add src/road_profile_viewer/visualization.py
git commit -m "Extract UI layer to visualization.py

- Move create_dash_app() and all Dash code
- Import from geometry and road modules using absolute imports
- Complete separation of concerns"
```

### Step 6: Simplify main.py

**Follow Lecture 4, Section 6.4 (end)**

1. The monolithic `main.py` already exists in `src/road_profile_viewer/`
2. Replace it with a simplified version (~20 lines):

```python
"""
Road Profile Viewer - Interactive 2D Visualization
===================================================
Main entry point for the road profile viewer application.

This application visualizes a road profile with camera ray intersection
using an interactive Dash interface.
"""

from road_profile_viewer.visualization import create_dash_app


def main():
    """
    Main function to run the Dash application.
    """
    app = create_dash_app()
    print("Starting Road Profile Viewer...")
    print("Open your browser and navigate to: http://127.0.0.1:8050/")
    print("Press Ctrl+C to stop the server.")
    app.run(debug=True)


if __name__ == "__main__":
    main()
```

**⚠️ IMPORTANT:** Use **absolute imports** (`from road_profile_viewer.visualization`) instead of relative imports (`from .visualization`). This allows the module to be run directly with `python -m road_profile_viewer.main` or `uv run main.py` without import errors.

**Commit your progress:**

```bash
git add src/road_profile_viewer/main.py
git commit -m "Simplify main.py to entry point only

- Only imports from visualization module using absolute imports
- Acts as entry point (~20 lines)
- Completes refactoring to modular structure"
```

### Step 7: Run Local Checks

**Test everything works before pushing!**

```bash
# Install dependencies
uv sync

# Test that the application runs without import errors
uv run python -m road_profile_viewer.main

# Stop the server with Ctrl+C, then run quality checks
uv run ruff check .
uv run ruff format --check .
uv run pyright

# If you see errors, fix them and commit the fixes
```

### Step 8: Push and Create Pull Request

```bash
# Push your feature branch
git push -u origin feature/refactor-to-modules

# Create PR using GitHub CLI (recommended)
gh pr create --title "Refactor: Split monolith into focused modules" \
  --body "Refactored src/road_profile_viewer/main.py into modular structure:

- geometry.py: Ray intersection math
- road.py: Road generation
- visualization.py: Dash UI
- main.py: Entry point (~20 lines)

All code quality checks pass.
Ready for review!"

# Or create PR manually on GitHub web interface
```

### Step 9: Wait for CI Checks

**GitHub Actions will automatically run:**

- ✅ Structure Check (verifies files exist, imports correct, etc.)
- ✅ Git Workflow Check (verifies feature branch, incremental commits)
- ✅ Code Quality Check (Ruff, Pyright)

**Check the "Actions" tab on GitHub to see results.**

If any checks fail, read the error messages, fix the issues, commit, and push again.

### Step 10: Get Peer Review

**Share your PR link with a classmate:**

```
Hey! Can you review my refactoring PR?
https://github.com/hs-aalen-software-engineering/refactoring-YOUR-USERNAME/pull/1
```

**As a reviewer, check:**

- [ ] PR is from `feature/refactor-to-modules` branch
- [ ] At least 3 incremental commits exist
- [ ] All 4 files exist (`geometry.py`, `road.py`, `visualization.py`, `main.py`)
- [ ] `main.py` is simplified (< 30 lines)
- [ ] Functions are in correct modules
- [ ] Imports flow correctly (no circular dependencies)
- [ ] All CI checks pass (green checkmarks)

**How to approve:**

1. Go to the PR
2. Click "Files changed" tab
3. Review the code
4. Click "Review changes" → "Approve" → "Submit review"

### Step 11: Merge Your PR

**Once you have:**
- ✅ All CI checks passing
- ✅ Peer review approval

**Merge your PR:**

```bash
# Using GitHub CLI
gh pr merge --squash

# Or click "Merge pull request" on GitHub web interface
```

**Congratulations! You've completed the refactoring exercise! 🎉**

## 🔍 How You're Graded

### Automated Checks (85 points)

GitHub Actions automatically verify:

| Check | Points | What's Verified |
|-------|--------|-----------------|
| **Structure Check** | 35 | All files exist, functions in correct modules, imports correct |
| **Git Workflow** | 25 | Feature branch, 3+ commits, descriptive messages |
| **Code Quality** | 25 | Ruff, Pyright pass; no circular dependencies |

### Manual Check (15 points)

Instructor verifies:

- You received peer review approval
- The review was substantive (not just "LGTM")

## ❓ Troubleshooting

### "ImportError: attempted relative import with no known parent package"

This is the most common error! It occurs when using relative imports (`.module`) in files that are run directly as scripts.

**Problem:**
```python
# ❌ This fails when running main.py directly:
from .visualization import create_dash_app
from .geometry import find_intersection
```

**Solution:**
```python
# ✅ Use absolute imports instead:
from road_profile_viewer.visualization import create_dash_app
from road_profile_viewer.geometry import find_intersection
```

**Why?** Python only recognizes relative imports when a file is imported as part of a package. When you run a file directly (`python main.py` or `uv run main.py`), Python doesn't know it's part of a package.

**Apply this fix to:**
- `src/road_profile_viewer/main.py`: Import from `visualization` module
- `src/road_profile_viewer/visualization.py`: Import from `geometry` and `road` modules

**Verification:**
```bash
# This should work without errors:
uv run python -m road_profile_viewer.main
# You should see: "Starting Road Profile Viewer..."
```

### "Import errors when running locally"

Make sure you create all modules in the **src/road_profile_viewer/ directory**. This is the proper Python package structure!

```
✅ Correct structure:
road-profile-viewer-YOUR-USERNAME/
├── README.md
├── pyproject.toml
├── tests/
│   └── test_smoke.py
└── src/
    └── road_profile_viewer/       ← All modules go HERE
        ├── __init__.py
        ├── geometry.py            ← CREATE THIS
        ├── road.py                ← CREATE THIS
        ├── visualization.py       ← CREATE THIS
        └── main.py                ← SIMPLIFY THIS (originally 390 lines → ~20 lines)

❌ Wrong structure:
road-profile-viewer-YOUR-USERNAME/
├── geometry.py                    ← WRONG! Not in src/
├── road.py                        ← WRONG! Not in src/
└── src/
    └── road_profile_viewer/
        └── main.py
```

### "Ruff errors"

If you get Ruff errors, fix them! The monolithic `main.py` already follows PEP 8, but when you extract code you might introduce issues:

```python
# ❌ Common mistakes when extracting:
def generate_road_profile(num_points=100,x_max=80):  # Missing space after comma
    y=0.015 * x_norm**3 * x_max                      # Missing spaces around =
    return x,y                                        # Missing space after comma

# ✅ Correct:
def generate_road_profile(num_points=100, x_max=80):
    y = 0.015 * x_norm**3 * x_max
    return x, y
```

**Auto-fix most issues:**
```bash
uv run ruff check --fix .
uv run ruff format .
```

### "Structure check fails: main.py too long"

Your `main.py` should be **~20 lines**, not 390! You should create a **new** `main.py` with just the entry point, not copy the entire original file.

The simplified `main.py` should only:
1. Import from `visualization` module
2. Define `main()` function
3. Have `if __name__ == "__main__":` block

Everything else goes to other modules!

### "Circular dependency detected"

Make sure dependencies flow in one direction:

```
✅ Correct:
main.py → visualization.py → geometry.py, road.py

❌ Wrong:
geometry.py → visualization.py → geometry.py (CIRCULAR!)
```

**Rule:** Lower-level modules (`geometry.py`, `road.py`) should NOT import from higher-level modules (`visualization.py`, `main.py`).

### "No peer review approval"

Ask a classmate! Share your PR link in the course chat or during class.

If you need help finding a reviewer, contact the instructor.

### "CI checks not running"

Make sure:
1. You created a PR (not just pushed to main)
2. The PR is from your feature branch to `main`
3. Check the "Actions" tab for errors

## 📚 Reference

- **Lecture 4**: Full refactoring tutorial
- **Lecture 3 Part 1**: Feature branch workflow
- **Lecture 3 Part 2**: CI/CD automation
- **Lecture 2**: Code quality (PEP 8, Ruff)

## 🆘 Getting Help

1. **Re-read Lecture 4** - It has step-by-step instructions!
2. **Check CI error messages** - They tell you exactly what's wrong
3. **Ask in class chat** - Help each other!
4. **Office hours** - Instructor is available for questions

## 📝 Quick Reference: Complete Import Structure

Here's what your imports should look like in each file:

**geometry.py:**
```python
import numpy as np
# No imports from other project modules
```

**road.py:**
```python
import numpy as np
# No imports from other project modules
```

**visualization.py:**
```python
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

from road_profile_viewer.geometry import find_intersection
from road_profile_viewer.road import generate_road_profile
```

**main.py:**
```python
from road_profile_viewer.visualization import create_dash_app
```

Good luck! 🚀

---

**Assignment Created**: 2025-10-29
**Course**: Software Engineering - HS Aalen
**Instructor**: Dominik Mueller
**Last Updated**: 2025-10-29 (Fixed import structure)
