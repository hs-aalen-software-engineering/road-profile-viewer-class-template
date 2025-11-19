# LLM Prompts Documentation

This folder contains documentation of Large Language Model (LLM) prompts used during the development of this project.

## Purpose

Documenting LLM interactions helps:
1. **Transparency**: Show how AI tools assisted development
2. **Learning**: Track what worked and what didn't
3. **Reproducibility**: Others can understand your problem-solving approach
4. **Academic Integrity**: Demonstrate proper attribution of AI-assisted work

## When to Document

Document LLM usage when you:
- Ask for help designing architecture or algorithms
- Request code examples or templates
- Seek explanations of errors or concepts
- Get assistance with debugging
- Ask for test case suggestions
- Request documentation writing help

## File Naming Convention

Use this format: `YYYY-MM-DD-feature-description.md`

**Examples:**
- `2025-11-20-database-schema-design.md`
- `2025-11-21-pydantic-validation-help.md`
- `2025-11-22-fastapi-endpoint-debugging.md`
- `2025-11-23-upload-component-implementation.md`

## Template

Create a new file for each significant LLM conversation using this template:

```markdown
# [Feature/Problem Title]

**Date:** YYYY-MM-DD
**LLM Used:** ChatGPT 4 / Claude 3 / GitHub Copilot / etc.
**Author:** [Your Name]
**Purpose:** [Brief description of why you needed help]
**Related Files:** [List files created/modified based on this conversation]

---

## Context

[Briefly describe what you were trying to accomplish and what challenges you faced]

---

## Conversation

### Prompt 1

\```
[Your exact prompt to the LLM]
\```

### Response 1 (Summary)

[Summarize or paste relevant parts of the LLM's response]

### Prompt 2

\```
[Your follow-up prompt]
\```

### Response 2 (Summary)

[Relevant parts of the response]

[Continue for additional prompts/responses...]

---

## Outcome

**What you learned:**
-
-

**How you used this information:**
-
-

**Code/concepts implemented:**
- [File:line reference or description]
-

**What you modified from the LLM suggestion:**
-
-

---

## Reflection

**What worked well:**
-

**What could be improved:**
-

**Alternative approaches considered:**
-
```

## Examples

### Example 1: Database Schema Design

**Filename:** `2025-11-20-database-schema-design.md`

```markdown
# SQLModel Database Schema for Road Profiles

**Date:** 2025-11-20
**LLM Used:** ChatGPT 4
**Author:** Jane Doe
**Purpose:** Design optimal database schema for storing road profile data
**Related Files:** `src/road_profile_viewer/database/models.py`

---

## Context

I needed to design a database schema that could store road profiles with varying
numbers of coordinate points efficiently. I wasn't sure whether to store coordinates
as JSON, separate tables, or pickled arrays.

---

## Conversation

### Prompt 1

\```
I'm building a SQLite database to store road profiles. Each profile has:
- A unique name
- A list of x coordinates (floats)
- A list of y coordinates (floats, same length as x)

What's the best way to structure this in SQLModel? Should I use JSON columns,
a separate table for coordinates, or something else?
\```

### Response 1 (Summary)

ChatGPT suggested three approaches:
1. JSON columns (simplest, good for our use case)
2. Separate coordinates table (normalized, more complex)
3. Array type (PostgreSQL only, not SQLite)

Recommended JSON for SQLite since:
- Simple to implement
- Good performance for our data size
- Easy to query all coordinates at once

---

## Outcome

**What you learned:**
- JSON columns are valid for moderate-sized lists in SQLite
- SQLModel can serialize Python lists to JSON automatically
- Trade-offs between normalization and simplicity

**How you used this information:**
- Implemented RoadProfile model with JSON columns for coordinates
- Added validation to ensure x and y lists have same length
- Used SQLModel's built-in JSON serialization

**Code implemented:**
- `src/road_profile_viewer/database/models.py:10-25`

**What you modified from the LLM suggestion:**
- Added Pydantic validators for coordinate length matching
- Added unique constraint on profile name
```

### Example 2: Debugging Upload Error

**Filename:** `2025-11-22-file-upload-base64-decoding.md`

```markdown
# Debugging Dash Upload Component Base64 Decoding

**Date:** 2025-11-22
**LLM Used:** Claude 3
**Author:** John Smith
**Purpose:** Fix error when decoding uploaded JSON file in Dash
**Related Files:** `src/road_profile_viewer/visualization.py`

---

## Context

Getting `UnicodeDecodeError` when trying to read uploaded JSON file from
Dash Upload component. The file contents seemed to be base64 encoded but
my decoding wasn't working.

---

## Conversation

### Prompt 1

\```
I'm using Dash's dcc.Upload component and getting this error when trying to decode:

UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 0

My code:
import base64
import json

def parse_uploaded_file(contents, filename):
    decoded = base64.b64decode(contents)
    return json.loads(decoded)

The contents parameter comes from the Upload component's contents property.
\```

### Response 1 (Summary)

Claude explained that Dash Upload component returns contents as a data URI string:
`data:application/json;base64,[base64-encoded-data]`

Need to split off the prefix before decoding.

Provided corrected code:
- Split on comma to remove prefix
- Then base64 decode
- Then JSON parse

---

## Outcome

**What you learned:**
- Dash Upload returns data URI, not raw base64
- Need to parse data URI format before decoding

**Code implemented:**
- `src/road_profile_viewer/visualization.py:156-162`

**What you modified:**
- Added error handling for invalid JSON
- Added validation using Pydantic before returning
```

## Best Practices

1. **Be Specific**: Document actual prompts, not summaries
2. **Include Context**: Explain what you tried before asking
3. **Show Your Work**: Note what you changed from suggestions
4. **Reflect**: Write what you learned and why it worked (or didn't)
5. **Link to Code**: Reference actual files/lines that resulted
6. **Be Honest**: Document both successful and unsuccessful attempts

## What NOT to Include

- Don't paste entire code files (use summaries or key excerpts)
- Don't include personally identifiable information
- Don't document trivial questions (e.g., "What does Python's `map` do?")
- Don't include prompts unrelated to this project

## Grading Considerations

Documenting LLM usage:
- ✅ **Shows initiative** in learning new technologies
- ✅ **Demonstrates critical thinking** (you modified suggestions)
- ✅ **Proves transparency** in your development process
- ✅ **Helps instructors** understand your learning journey

**Note:** Using LLMs is encouraged and allowed! We just ask that you document it
as part of your implementation plan.

---

**Remember:** The goal is not to prove you didn't use AI, but to show how you
used it effectively to learn and solve problems!
