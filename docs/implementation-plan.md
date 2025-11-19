# Implementation Plan: Road Profile Database & Upload System

> **Note:** This is a template. Fill in your team's specific details, decisions, and strategy.

## Team Members

| Name | GitHub Username | Role/Responsibilities |
|------|-----------------|----------------------|
| [Student Name 1] | @username1 | Database setup, backend development |
| [Student Name 2] | @username2 | Frontend (Dropdown selector) |
| [Student Name 3] | @username3 | Upload page development |
| [Student Name 4] | @username4 | Testing, API endpoints (optional) |

## Technical Decision

**Selected Approach:** (choose one)

- [ ] **FastAPI + SQLModel + SQLite** (5 points possible)
  - Reason for choice: _______________________________________
  - Expected challenges: ____________________________________

- [ ] **TinyDB** (4 points possible)
  - Reason for choice: _______________________________________
  - Expected challenges: ____________________________________

## Architecture Overview

### High-Level Architecture

```
[Describe your architecture here]

Example for FastAPI approach:
┌─────────────────┐
│   Dash Frontend │
│  (visualization) │
└────────┬────────┘
         │ HTTP Requests
         ▼
┌─────────────────┐
│   FastAPI Backend│
│   (REST API)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQLite Database│
│   (SQLModel)    │
└─────────────────┘
```

### Database Schema

```python
# Describe your database model
class RoadProfile:
    id: int  # Primary key
    name: str  # Unique constraint
    x_coordinates: list[float]
    y_coordinates: list[float]
    created_at: datetime  # Optional
```

## Feature Breakdown

| Feature | Branch Name | Assignee | Est. Time | Status | Notes |
|---------|-------------|----------|-----------|--------|-------|
| Database models and setup | `feature/database-setup` | [Name] | 3-4 hours | ⏳ Pending | Create schema, connection, seed |
| CRUD operations | `feature/database-setup` | [Name] | 2-3 hours | ⏳ Pending | Create, Read, Update, Delete |
| Pydantic validation models | `feature/validation` | [Name] | 1-2 hours | ⏳ Pending | JSON schema validation |
| Dropdown selector (main page) | `feature/dropdown-selector` | [Name] | 3-4 hours | ⏳ Pending | UI component + callback |
| Upload page layout | `feature/upload-page` | [Name] | 2-3 hours | ⏳ Pending | File upload, rename, button |
| Upload preview functionality | `feature/upload-page` | [Name] | 2-3 hours | ⏳ Pending | Graph preview before save |
| FastAPI endpoints (if applicable) | `feature/api-endpoints` | [Name] | 4-5 hours | ⏳ Pending | GET/POST/DELETE routes |
| Unit tests (database) | `feature/tests-database` | [Name] | 2-3 hours | ⏳ Pending | 90%+ coverage |
| Unit tests (upload) | `feature/tests-upload` | [Name] | 2-3 hours | ⏳ Pending | 90%+ coverage |
| Integration testing | `feature/integration-tests` | [Name] | 2-3 hours | ⏳ Pending | End-to-end workflow |
| Documentation | All branches | All | Ongoing | ⏳ Pending | Code comments, docstrings |

**Status Legend:**
- ⏳ Pending - Not started
- 🔄 In Progress - Currently being worked on
- ✅ Complete - Merged to main
- ❌ Blocked - Waiting on dependencies

## Development Workflow

### 1. Sprint Planning (Week 1)

**Date:** [YYYY-MM-DD]

**Tasks:**
- [ ] Team kickoff meeting
- [ ] Review assignment requirements
- [ ] Decide on technical approach (FastAPI vs TinyDB)
- [ ] Create initial branch structure
- [ ] Set up development environment (all team members)
- [ ] Create this implementation plan

### 2. Development Sprints

#### Sprint 1: Database & Core Infrastructure (Days 1-3)
- [ ] Database schema design
- [ ] Pydantic models
- [ ] Seed script for default profile
- [ ] Basic CRUD operations
- [ ] Unit tests for database layer

#### Sprint 2: Frontend Features (Days 4-6)
- [ ] Dropdown selector implementation
- [ ] Upload page UI
- [ ] Navigation between pages
- [ ] Frontend validation

#### Sprint 3: Integration & Testing (Days 7-9)
- [ ] Connect frontend to backend/database
- [ ] Upload preview functionality
- [ ] End-to-end testing
- [ ] Achieve 90%+ coverage

#### Sprint 4: Polish & Documentation (Days 10-12)
- [ ] Code review and refactoring
- [ ] Fix bugs
- [ ] Complete documentation
- [ ] Final manual testing

### 3. Merge Strategy

**Branch Protection Rules:**
- All changes via Pull Requests
- Minimum 1 approval required
- All CI checks must pass
- No direct commits to `main`

**Merge Order:**
1. Database setup → main
2. Validation models → main
3. Dropdown selector → main
4. Upload page → main
5. API endpoints (if FastAPI) → main
6. Tests → main

## Testing Strategy

### Coverage Goal: 90%+ C1 Coverage

**Tools:**
- `pytest` for test execution
- `pytest-cov` for coverage measurement
- `pytest-mock` for mocking (if needed)

### Test Categories

#### 1. Unit Tests

**Database Operations:**
```python
# tests/test_database.py
- test_create_profile()
- test_read_profile_by_name()
- test_read_all_profiles()
- test_update_profile()
- test_delete_profile()
- test_duplicate_name_error()
```

**Pydantic Validation:**
```python
# tests/test_models.py
- test_valid_profile()
- test_invalid_name_too_short()
- test_invalid_name_too_long()
- test_coordinates_length_mismatch()
- test_coordinates_too_few_points()
- test_non_numeric_coordinates()
```

**FastAPI Endpoints (if applicable):**
```python
# tests/test_api.py
- test_get_all_profiles()
- test_get_profile_by_id()
- test_create_profile_success()
- test_create_profile_duplicate()
- test_create_profile_invalid_data()
```

#### 2. Integration Tests

```python
# tests/test_integration.py
- test_upload_workflow_end_to_end()
- test_dropdown_selection_updates_graph()
- test_database_persistence_after_restart()
```

#### 3. Manual Testing Checklist

- [ ] App starts without errors
- [ ] Dropdown shows all profiles
- [ ] Selecting profile updates visualization
- [ ] Upload page accessible
- [ ] Can upload valid JSON
- [ ] Preview shows correct graph
- [ ] Can rename profile before saving
- [ ] Invalid JSON shows error message
- [ ] Profile appears in dropdown after save
- [ ] Database persists after app restart
- [ ] Default profile exists on first run

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_database.py -v

# Check coverage report
open htmlcov/index.html  # or: start htmlcov/index.html on Windows
```

## Communication & Collaboration

### Meetings

| Type | Frequency | Duration | Participants |
|------|-----------|----------|--------------|
| Daily Standup | Daily | 15 min | All team members |
| Sprint Planning | Weekly | 1 hour | All team members |
| Code Review Sessions | As needed | 30 min | Author + Reviewer |
| Retrospective | End of project | 1 hour | All team members |

### Communication Channels

- **GitHub Issues:** Task tracking, bug reports
- **GitHub Discussions:** Technical questions, design decisions
- **[Team Chat Platform]:** Daily communication (Discord/Slack/WhatsApp)
- **Pull Request Comments:** Code-specific discussions

### LLM Usage Documentation

**If using LLMs (ChatGPT, Claude, etc.), document prompts in `docs/llm-prompts/`:**

**File naming convention:** `YYYY-MM-DD-feature-description.md`

**Template:**
```markdown
# [Feature Name] - LLM Conversation

**Date:** YYYY-MM-DD
**LLM Used:** ChatGPT 4 / Claude / etc.
**Author:** [Your Name]
**Purpose:** [Why you needed help]

## Prompt 1
[Your first prompt]

## Response 1
[Relevant parts of the response]

## Prompt 2
[Follow-up prompt]

## Response 2
[Response]

## Outcome
[What you learned / How you used this information]
```

## Risk Management

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Database schema changes break existing code | Medium | High | Comprehensive tests, migration scripts |
| Merge conflicts | High | Medium | Frequent pulls from main, small PRs |
| Coverage below 90% | Medium | High | Write tests alongside features, not after |
| FastAPI complexity (if chosen) | Medium | Medium | Start simple, iterate, use documentation |
| Time constraints | Medium | High | Prioritize core features, bonus features last |
| Team member unavailability | Low | High | Knowledge sharing, pair programming |

## Definition of Done

A feature is considered "done" when:

- [ ] Code is written and follows style guide (Ruff passes)
- [ ] Type hints added (Pyright passes)
- [ ] Unit tests written with 90%+ coverage
- [ ] Manual testing completed
- [ ] Code reviewed and approved by at least one team member
- [ ] Documentation updated (docstrings, comments)
- [ ] PR merged to main branch
- [ ] No regressions in existing functionality

## Success Criteria

**Minimum Viable Product (MVP):**
- [ ] Database stores and retrieves profiles
- [ ] Dropdown lists available profiles
- [ ] Selecting profile updates visualization
- [ ] Upload page accepts JSON files
- [ ] Preview shows uploaded profile
- [ ] Can save uploaded profile to database
- [ ] 90%+ test coverage
- [ ] All CI checks pass

**Stretch Goals:**
- [ ] FastAPI implementation (if time allows)
- [ ] Profile editing capability
- [ ] Profile deletion from UI
- [ ] Export profile as JSON
- [ ] Multiple upload formats (CSV, Excel)
- [ ] Profile thumbnails in dropdown

## Timeline

**Start Date:** [YYYY-MM-DD]
**Due Date:** [YYYY-MM-DD]
**Estimated Effort:** [X] hours total

**Milestones:**
- [ ] Week 1: Database and validation complete
- [ ] Week 2: Frontend features complete
- [ ] Week 3: Testing and polish complete
- [ ] Final: Project submitted

## Notes & Decisions

**Decision Log:**

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| YYYY-MM-DD | Chose [FastAPI/TinyDB] | [Reason] | [Impact on architecture] |
| YYYY-MM-DD | [Other decision] | [Reason] | [Impact] |

**Open Questions:**
- [ ] Question 1: [To be resolved]
- [ ] Question 2: [To be resolved]

**Lessons Learned:**
- [To be filled during/after development]

---

**Last Updated:** [YYYY-MM-DD]
**Version:** 1.0
