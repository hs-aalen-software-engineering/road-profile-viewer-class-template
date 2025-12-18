"""
Pytest Configuration and Traceability Hooks
============================================
Custom pytest hooks for requirement traceability reporting.

Features:
- Collects all @pytest.mark.requirement markers
- Generates JSON traceability data
- Integrates with pytest-html for enhanced reporting
- Supports allure for detailed reports
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pytest
from _pytest.config import Config
from _pytest.nodes import Item
from _pytest.terminal import TerminalReporter

# ============================================================================
# Allure integration (must be imported early for use in hooks)
# ============================================================================

try:
    import allure

    _ALLURE_AVAILABLE = True
except ImportError:
    allure = None  # type: ignore[assignment]
    _ALLURE_AVAILABLE = False


# Global storage for requirement data
_requirement_data: dict[str, list[dict[str, Any]]] = defaultdict(list)
_test_results: dict[str, dict[str, Any]] = {}


def pytest_configure(config: Config) -> None:
    """Configure pytest with traceability options."""
    # Add custom markers documentation
    config.addinivalue_line(
        "markers",
        "requirement(id): Mark test as verifying a specific requirement",
    )

    # Initialize traceability report path
    config._traceability_report_path = Path("reports/traceability")  # type: ignore[attr-defined]


def pytest_collection_modifyitems(session: pytest.Session, config: Config, items: list[Item]) -> None:
    """Collect requirement markers from all tests."""
    global _requirement_data
    _requirement_data.clear()

    for item in items:
        # Get all requirement markers
        for marker in item.iter_markers(name="requirement"):
            if marker.args:
                req_id = marker.args[0]
                _requirement_data[req_id].append({
                    "test_name": item.name,
                    "test_nodeid": item.nodeid,
                    "test_file": str(item.fspath) if item.fspath else "",
                    "test_class": item.parent.name
                    if item.parent and item.parent.name != item.fspath.basename
                    else None,  # type: ignore[union-attr]
                })


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """Track test results for traceability."""
    global _test_results

    if report.when == "call":
        _test_results[report.nodeid] = {
            "outcome": report.outcome,
            "duration": report.duration,
            "longrepr": str(report.longrepr) if report.longrepr else None,
        }


def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: int, config: Config) -> None:
    """Generate traceability summary at the end of test run."""
    global _requirement_data, _test_results

    if not _requirement_data:
        return

    # Create reports directory
    report_path = Path("reports/traceability")
    report_path.mkdir(parents=True, exist_ok=True)

    # Build full report data
    report_data = {
        "summary": {
            "total_requirements": len(_requirement_data),
            "total_tests": sum(len(tests) for tests in _requirement_data.values()),
            "passed": 0,
            "failed": 0,
            "skipped": 0,
        },
        "requirements": {},
    }

    for req_id, tests in sorted(_requirement_data.items()):
        req_tests = []
        for test in tests:
            result = _test_results.get(test["test_nodeid"], {"outcome": "unknown"})
            outcome = result.get("outcome", "unknown")

            if outcome == "passed":
                report_data["summary"]["passed"] += 1
            elif outcome == "failed":
                report_data["summary"]["failed"] += 1
            elif outcome == "skipped":
                report_data["summary"]["skipped"] += 1

            req_tests.append({
                **test,
                "outcome": outcome,
                "duration": result.get("duration", 0),
            })

        report_data["requirements"][req_id] = {
            "test_count": len(tests),
            "tests": req_tests,
            "status": "passed" if all(t["outcome"] == "passed" for t in req_tests) else "failed",
        }

    # Write JSON report
    json_path = report_path / "traceability.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    # Print summary
    terminalreporter.write_sep("=", "Requirement Traceability Summary")
    terminalreporter.write_line(f"Requirements covered: {len(_requirement_data)}")
    terminalreporter.write_line(f"Total requirement-test links: {report_data['summary']['total_tests']}")
    terminalreporter.write_line(f"Report saved to: {json_path}")


# ============================================================================
# pytest-html integration
# ============================================================================


def pytest_html_report_title(report: Any) -> None:
    """Set custom report title for pytest-html."""
    report.title = "Road Profile Viewer - Test Report with Requirement Traceability"


def pytest_html_results_table_header(cells: list[Any]) -> None:
    """Add Requirements column to pytest-html results table."""
    cells.insert(2, '<th class="sortable" data-column-type="requirements">Requirements</th>')


def pytest_html_results_table_row(report: Any, cells: list[Any]) -> None:
    """Add requirement IDs to each test row in pytest-html."""
    # Get requirements from test markers
    requirements = getattr(report, "_requirements", [])
    req_str = ", ".join(requirements) if requirements else "-"
    cells.insert(2, f'<td class="col-requirements">{req_str}</td>')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: Any) -> Any:
    """Attach requirement markers to test report for pytest-html and allure."""
    outcome = yield
    report = outcome.get_result()

    # Collect requirement markers
    requirements = []
    for marker in item.iter_markers(name="requirement"):
        if marker.args:
            requirements.append(marker.args[0])

    report._requirements = requirements  # type: ignore[attr-defined]

    # Add allure labels during call phase
    if call.when == "call" and _ALLURE_AVAILABLE and allure is not None:
        for req_id in requirements:
            allure.dynamic.label("requirement", req_id)
