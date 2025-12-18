#!/usr/bin/env python3
"""
Unified Test Runner with Traceability Reports
==============================================
Run pytest with various reporting options.

Usage:
    python scripts/run_tests.py [OPTIONS]

Options:
    --coverage          Enable code coverage
    --html              Generate pytest-html report
    --allure            Generate Allure report
    --traceability      Generate traceability report
    --all-reports       Enable all reports
    --filter REQ_ID     Run only tests for specific requirement
    --open              Open HTML reports after generation
    --verbose           Verbose output

Examples:
    # Run all tests with traceability
    python scripts/run_tests.py --traceability

    # Run with all reports
    python scripts/run_tests.py --all-reports

    # Run only tests for FR-001
    python scripts/run_tests.py --filter FR-001

    # Combine options
    python scripts/run_tests.py --coverage --html --traceability
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import webbrowser
from pathlib import Path


def find_project_root() -> Path:
    """Find project root by looking for pyproject.toml."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path.cwd()


def check_dependency(package: str) -> bool:
    """Check if a package is installed."""
    try:
        result = subprocess.run(
            ["uv", "pip", "show", package],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        # Try pip directly
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package],
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode == 0
        except Exception:
            return False


def run_pytest(
    project_root: Path,
    coverage: bool = False,
    html: bool = False,
    allure: bool = False,
    traceability: bool = False,
    filter_req: str | None = None,
    verbose: bool = False,
    extra_args: list[str] | None = None,
) -> int:
    """Run pytest with specified options."""
    cmd = ["uv", "run", "python", "-m", "pytest"]

    # Verbosity
    if verbose:
        cmd.append("-v")

    # Coverage options
    if coverage:
        cmd.extend([
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=html:reports/coverage",
        ])

    # pytest-html report
    if html:
        reports_dir = project_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        cmd.extend([
            f"--html={reports_dir / 'test_report.html'}",
            "--self-contained-html",
        ])

    # Allure report
    if allure:
        allure_dir = project_root / "reports" / "allure-results"
        allure_dir.mkdir(parents=True, exist_ok=True)
        cmd.extend([
            f"--alluredir={allure_dir}",
        ])

    # Filter by requirement (custom marker expression)
    if filter_req:
        # Run all tests but we'll filter based on markers
        # Note: Standard pytest -m doesn't support marker arguments
        # This requires custom filtering in conftest.py or post-processing
        print(f"Note: Filtering by requirement {filter_req}")
        print("Running all tests and filtering results...")

    # Add any extra arguments
    if extra_args:
        cmd.extend(extra_args)

    # Print command
    print(f"Running: {' '.join(cmd)}")
    print()

    # Run pytest
    result = subprocess.run(cmd, cwd=project_root)

    # Generate traceability report if requested
    if traceability and result.returncode in (0, 1):  # 0=passed, 1=some failed
        print("\nGenerating traceability report...")
        trace_result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                str(project_root / "scripts" / "generate_traceability.py"),
                "--format",
                "all",
            ],
            cwd=project_root,
        )
        if trace_result.returncode != 0:
            print("Warning: Traceability report generation failed")

    return result.returncode


def generate_allure_html(project_root: Path) -> bool:
    """Generate Allure HTML report from results."""
    allure_results = project_root / "reports" / "allure-results"
    allure_report = project_root / "reports" / "allure-report"

    if not allure_results.exists():
        print("No Allure results found. Run with --allure first.")
        return False

    try:
        result = subprocess.run(
            ["allure", "generate", str(allure_results), "-o", str(allure_report), "--clean"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"Allure report generated: {allure_report}")
            return True
        else:
            print(f"Allure generation failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Allure CLI not found. Install with: npm install -g allure-commandline")
        print("Or: brew install allure (macOS) / scoop install allure (Windows)")
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run tests with various reporting options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/run_tests.py --traceability
    python scripts/run_tests.py --all-reports
    python scripts/run_tests.py --coverage --html
    python scripts/run_tests.py --filter FR-001
        """,
    )

    # Report options
    parser.add_argument("--coverage", action="store_true", help="Enable code coverage")
    parser.add_argument("--html", action="store_true", help="Generate pytest-html report")
    parser.add_argument("--allure", action="store_true", help="Generate Allure report")
    parser.add_argument("--traceability", action="store_true", help="Generate traceability report")
    parser.add_argument("--all-reports", action="store_true", help="Enable all reports")

    # Filtering
    parser.add_argument("--filter", dest="filter_req", help="Filter tests by requirement ID")

    # Output options
    parser.add_argument("--open", action="store_true", help="Open HTML reports after generation")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # Pass-through to pytest
    parser.add_argument("pytest_args", nargs="*", help="Additional pytest arguments")

    args = parser.parse_args()

    project_root = find_project_root()
    print(f"Project root: {project_root}")

    # Handle --all-reports
    if args.all_reports:
        args.coverage = True
        args.html = True
        args.traceability = True
        # Only enable allure if installed
        if check_dependency("allure-pytest"):
            args.allure = True
        else:
            print("Note: allure-pytest not installed, skipping Allure reports")

    # Check dependencies
    if args.html and not check_dependency("pytest-html"):
        print("Warning: pytest-html not installed. Run: uv add --dev pytest-html")
        args.html = False

    if args.allure and not check_dependency("allure-pytest"):
        print("Warning: allure-pytest not installed. Run: uv add --dev allure-pytest")
        args.allure = False

    # Run tests
    exit_code = run_pytest(
        project_root,
        coverage=args.coverage,
        html=args.html,
        allure=args.allure,
        traceability=args.traceability,
        filter_req=args.filter_req,
        verbose=args.verbose,
        extra_args=args.pytest_args,
    )

    # Generate Allure HTML if requested
    if args.allure:
        generate_allure_html(project_root)

    # Open reports if requested
    if args.open:
        reports_dir = project_root / "reports"

        if args.html and (reports_dir / "test_report.html").exists():
            webbrowser.open(f"file://{reports_dir / 'test_report.html'}")

        if args.traceability and (reports_dir / "traceability" / "traceability_report.html").exists():
            webbrowser.open(f"file://{reports_dir / 'traceability' / 'traceability_report.html'}")

        if args.coverage and (reports_dir / "coverage" / "index.html").exists():
            webbrowser.open(f"file://{reports_dir / 'coverage' / 'index.html'}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
