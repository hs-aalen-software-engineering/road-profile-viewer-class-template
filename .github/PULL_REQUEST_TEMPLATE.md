# Pull Request: Road Profile Database & Upload System

## Description
<!-- Provide a clear and concise description of what this PR implements -->



## Related Feature
<!-- Which part of the assignment does this PR address? Check all that apply -->
- [ ] Database setup and schema
- [ ] Dropdown selector on main page
- [ ] Upload page with file handling
- [ ] Preview functionality
- [ ] Pydantic validation models
- [ ] API endpoints (FastAPI approach)
- [ ] Unit tests
- [ ] Other: _________________

## Implementation Approach
<!-- Check your team's chosen approach -->
- [ ] FastAPI + SQLModel + SQLite
- [ ] TinyDB

## Changes Made
<!-- List the key changes introduced in this PR -->
-
-
-

## Testing
<!-- Describe how you tested these changes -->

- [ ] Unit tests added/updated
- [ ] Coverage ≥90% for new code (`pytest --cov`)
- [ ] Manual testing completed
- [ ] All edge cases considered

**Test Coverage:**
```
# Paste coverage report here
```

**Manual Testing Checklist:**
- [ ] Feature works as expected
- [ ] No console errors
- [ ] Handles invalid input gracefully
- [ ] Database operations work correctly

## Code Quality
<!-- Confirm all quality checks pass -->

- [ ] Code follows project style (Ruff passes)
- [ ] Type hints added for all functions (Pyright passes)
- [ ] No circular dependencies
- [ ] Docstrings added for public functions
- [ ] Code is readable and well-organized

**Quality Check Results:**
```bash
# Run these commands and paste results:
# uv run ruff check .
# uv run pyright
```

## Documentation
<!-- If applicable, describe documentation updates -->

- [ ] Implementation plan updated (if needed)
- [ ] Comments added for complex logic
- [ ] README updated (if needed)
- [ ] LLM prompts documented (if used)

## Screenshots / Demo
<!-- For UI changes, add screenshots or describe the visual changes -->



## Checklist
<!-- Complete this checklist before requesting review -->

- [ ] Code builds successfully (`uv sync`)
- [ ] All tests pass locally (`uv run pytest`)
- [ ] Code quality checks pass (Ruff, Pyright)
- [ ] Branch is up to date with main
- [ ] Commit messages are descriptive (>20 characters)
- [ ] No sensitive data (API keys, passwords) in code
- [ ] Database file NOT committed (in `.gitignore`)
- [ ] Reviewed my own code before requesting review
- [ ] Ready for peer review

## Reviewer Notes
<!-- Any specific areas you'd like reviewers to focus on? -->



## How to Review
<!-- Instructions for reviewers -->

1. **Check out this branch:**
   ```bash
   git fetch origin
   git checkout [branch-name]
   uv sync
   ```

2. **Run tests:**
   ```bash
   uv run pytest --cov=src --cov-report=term-missing
   ```

3. **Run the application:**
   ```bash
   uv run python -m road_profile_viewer
   # For FastAPI: also run `uv run uvicorn road_profile_viewer.api.main:app --port 8000`
   ```

4. **Test the feature manually** according to the manual testing checklist above

5. **Review code quality:**
   ```bash
   uv run ruff check .
   uv run pyright
   ```

---

**Assignee:** @<!-- your GitHub username -->
**Reviewers:** @<!-- teammate GitHub usernames -->
**Labels:** <!-- Add relevant labels: feature, bugfix, enhancement, etc. -->
