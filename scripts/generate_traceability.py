#!/usr/bin/env python3
"""
Traceability Report Generator
=============================
Generates requirement traceability reports from pytest runs.

Usage:
    python scripts/generate_traceability.py [OPTIONS]

Options:
    --format {json,html,markdown,all}   Output format (default: all)
    --output DIR                        Output directory (default: reports/traceability)
    --requirements FILE                 Requirements file to check coverage (default: docs/requirements.md)
    --verbose                           Show detailed output
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_requirements_from_docs(requirements_file: Path) -> dict[str, dict[str, str]]:
    """Parse requirement IDs and descriptions from requirements.md."""
    requirements: dict[str, dict[str, str]] = {}

    if not requirements_file.exists():
        print(f"Warning: Requirements file not found: {requirements_file}")
        return requirements

    content = requirements_file.read_text(encoding="utf-8")

    # Pattern to match requirement IDs like FR-001, NFR-001, REQ-GEOM-001
    # Format: | ID | Description | or **ID**: Description
    patterns = [
        # Table format: | FR-001 | Description |
        r"\|\s*((?:FR|NFR|REQ)-[\w-]+)\s*\|\s*([^|]+)\s*\|",
        # List format: - **FR-001**: Description
        r"-\s*\*\*\s*((?:FR|NFR|REQ)-[\w-]+)\s*\*\*\s*[:\-]\s*(.+)",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content):
            req_id = match.group(1).strip()
            description = match.group(2).strip()
            requirements[req_id] = {
                "id": req_id,
                "description": description,
                "type": "functional"
                if req_id.startswith("FR-")
                else ("non-functional" if req_id.startswith("NFR-") else "derived"),
            }

    return requirements


def load_traceability_data(report_path: Path) -> dict | None:
    """Load traceability data from JSON report."""
    json_file = report_path / "traceability.json"

    if not json_file.exists():
        print(f"Error: Traceability data not found at {json_file}")
        print("Run pytest first to generate the data.")
        return None

    with open(json_file, encoding="utf-8") as f:
        return json.load(f)


def generate_markdown_report(
    data: dict,
    requirements: dict[str, dict[str, str]],
    output_path: Path,
) -> None:
    """Generate markdown traceability report."""
    lines = [
        "# Requirement Traceability Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "",
        f"- **Total Requirements Tested:** {data['summary']['total_requirements']}",
        f"- **Total Test-Requirement Links:** {data['summary']['total_tests']}",
        f"- **Passed:** {data['summary']['passed']}",
        f"- **Failed:** {data['summary']['failed']}",
        f"- **Skipped:** {data['summary'].get('skipped', 0)}",
        "",
    ]

    # Coverage analysis
    tested_reqs = set(data["requirements"].keys())
    all_reqs = set(requirements.keys())
    untested = all_reqs - tested_reqs

    if all_reqs:
        coverage = len(tested_reqs & all_reqs) / len(all_reqs) * 100
        lines.extend([
            "## Coverage Analysis",
            "",
            f"- **Documented Requirements:** {len(all_reqs)}",
            f"- **Requirements with Tests:** {len(tested_reqs & all_reqs)}",
            f"- **Coverage:** {coverage:.1f}%",
            "",
        ])

        if untested:
            lines.extend([
                "### Untested Requirements",
                "",
                "| ID | Description | Type |",
                "|---|---|---|",
            ])
            for req_id in sorted(untested):
                req = requirements.get(req_id, {})
                desc = req.get("description", "No description")
                req_type = req.get("type", "unknown")
                lines.append(f"| {req_id} | {desc} | {req_type} |")
            lines.append("")

    # Traceability matrix
    lines.extend([
        "## Traceability Matrix",
        "",
        "| Requirement | Status | Tests | Description |",
        "|---|---|---|---|",
    ])

    for req_id, req_data in sorted(data["requirements"].items()):
        status_emoji = "✅" if req_data["status"] == "passed" else "❌"
        test_count = req_data["test_count"]
        description = requirements.get(req_id, {}).get("description", "-")
        # Truncate long descriptions
        if len(description) > 50:
            description = description[:47] + "..."
        lines.append(f"| {req_id} | {status_emoji} | {test_count} | {description} |")

    lines.append("")

    # Detailed test list per requirement
    lines.extend([
        "## Detailed Test Mapping",
        "",
    ])

    for req_id, req_data in sorted(data["requirements"].items()):
        lines.extend([
            f"### {req_id}",
            "",
            f"**Description:** {requirements.get(req_id, {}).get('description', 'Not documented')}",
            "",
            "| Test | Status | Duration |",
            "|---|---|---|",
        ])

        for test in req_data["tests"]:
            status = "✅" if test["outcome"] == "passed" else ("❌" if test["outcome"] == "failed" else "⏭️")
            duration = f"{test['duration']:.3f}s" if test.get("duration") else "-"
            test_name = test["test_name"]
            lines.append(f"| `{test_name}` | {status} | {duration} |")

        lines.append("")

    # Write file
    output_file = output_path / "traceability_report.md"
    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown report generated: {output_file}")


def generate_html_report(
    data: dict,
    requirements: dict[str, dict[str, str]],
    output_path: Path,
) -> None:
    """Generate HTML traceability report."""
    tested_reqs = set(data["requirements"].keys())
    all_reqs = set(requirements.keys())
    coverage = len(tested_reqs & all_reqs) / len(all_reqs) * 100 if all_reqs else 0

    untested = all_reqs - tested_reqs

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Requirement Traceability Report</title>
    <style>
        :root {{
            --passed: #28a745;
            --failed: #dc3545;
            --skipped: #ffc107;
            --untested: #6c757d;
            --bg: #f8f9fa;
            --border: #dee2e6;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: var(--bg);
        }}
        h1, h2, h3 {{ color: #333; }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .card-value {{
            font-size: 2em;
            font-weight: bold;
        }}
        .card-label {{ color: #666; }}
        .passed .card-value {{ color: var(--passed); }}
        .failed .card-value {{ color: var(--failed); }}
        .coverage .card-value {{ color: #007bff; }}
        .untested .card-value {{ color: var(--untested); }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{ background: #343a40; color: white; }}
        tr:hover {{ background: #f1f3f5; }}
        .status-passed {{ color: var(--passed); font-weight: bold; }}
        .status-failed {{ color: var(--failed); font-weight: bold; }}
        .status-skipped {{ color: var(--skipped); font-weight: bold; }}
        .untested-section {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .untested-section h3 {{
            color: #856404;
            margin-top: 0;
        }}
        .untested-table th {{
            background: #856404;
        }}
        .filter-input {{
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid var(--border);
            border-radius: 4px;
            font-size: 1em;
        }}
        .collapsible {{
            cursor: pointer;
            background: #e9ecef;
            padding: 10px;
            border-radius: 4px;
            margin: 5px 0;
        }}
        .collapsible:hover {{ background: #dee2e6; }}
        .content {{ display: none; padding: 10px; background: white; }}
        .content.active {{ display: block; }}
    </style>
</head>
<body>
    <h1>Requirement Traceability Report</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

    <div class="summary-cards">
        <div class="card coverage">
            <div class="card-value">{coverage:.1f}%</div>
            <div class="card-label">Coverage</div>
        </div>
        <div class="card">
            <div class="card-value">{data["summary"]["total_requirements"]}</div>
            <div class="card-label">Requirements</div>
        </div>
        <div class="card passed">
            <div class="card-value">{data["summary"]["passed"]}</div>
            <div class="card-label">Passed</div>
        </div>
        <div class="card failed">
            <div class="card-value">{data["summary"]["failed"]}</div>
            <div class="card-label">Failed</div>
        </div>
        <div class="card untested">
            <div class="card-value">{len(untested)}</div>
            <div class="card-label">Untested</div>
        </div>
    </div>
"""

    # Add untested requirements section if there are any
    if untested:
        html += """
    <div class="untested-section">
        <h3>Untested Requirements</h3>
        <p>The following documented requirements do not have any associated tests:</p>
        <table class="untested-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
"""
        for req_id in sorted(untested):
            req = requirements.get(req_id, {})
            desc = req.get("description", "No description")
            req_type = req.get("type", "unknown")
            html += f"""                <tr>
                    <td><strong>{req_id}</strong></td>
                    <td>{req_type}</td>
                    <td>{desc}</td>
                </tr>
"""
        html += """            </tbody>
        </table>
    </div>
"""

    html += """
    <h2>Traceability Matrix</h2>
    <input type="text" class="filter-input" id="filterInput" placeholder="Filter by requirement ID...">
    <table id="traceabilityTable">
        <thead>
            <tr>
                <th>Requirement</th>
                <th>Type</th>
                <th>Status</th>
                <th>Tests</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
"""

    for req_id, req_data in sorted(data["requirements"].items()):
        status = req_data["status"]
        status_class = f"status-{status}"
        test_count = req_data["test_count"]
        req_info = requirements.get(req_id, {})
        description = req_info.get("description", "-")
        req_type = req_info.get("type", "derived")

        html += f"""            <tr>
                <td><strong>{req_id}</strong></td>
                <td>{req_type}</td>
                <td class="{status_class}">{status.upper()}</td>
                <td>{test_count}</td>
                <td>{description}</td>
            </tr>
"""

    html += """        </tbody>
    </table>

    <h2>Detailed Test Mapping</h2>
"""

    for req_id, req_data in sorted(data["requirements"].items()):
        html += f"""    <div class="collapsible" onclick="this.nextElementSibling.classList.toggle('active')">
        <strong>{req_id}</strong> - {req_data["test_count"]} tests
    </div>
    <div class="content">
        <table>
            <thead>
                <tr><th>Test Name</th><th>Status</th><th>Duration</th></tr>
            </thead>
            <tbody>
"""
        for test in req_data["tests"]:
            status = test["outcome"]
            status_class = f"status-{status}"
            duration = f"{test['duration']:.3f}s" if test.get("duration") else "-"
            html += f"""                <tr>
                    <td><code>{test["test_name"]}</code></td>
                    <td class="{status_class}">{status.upper()}</td>
                    <td>{duration}</td>
                </tr>
"""
        html += """            </tbody>
        </table>
    </div>
"""

    html += """
    <script>
        document.getElementById('filterInput').addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll('#traceabilityTable tbody tr');
            rows.forEach(row => {
                const reqId = row.cells[0].textContent.toLowerCase();
                row.style.display = reqId.includes(filter) ? '' : 'none';
            });
        });
    </script>
</body>
</html>
"""

    output_file = output_path / "traceability_report.html"
    output_file.write_text(html, encoding="utf-8")
    print(f"HTML report generated: {output_file}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate requirement traceability reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--format",
        choices=["json", "html", "markdown", "all"],
        default="all",
        help="Output format (default: all)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/traceability"),
        help="Output directory (default: reports/traceability)",
    )
    parser.add_argument(
        "--requirements",
        type=Path,
        default=Path("docs/requirements.md"),
        help="Requirements file to check coverage",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output",
    )

    args = parser.parse_args()

    # Ensure output directory exists
    args.output.mkdir(parents=True, exist_ok=True)

    # Load data
    data = load_traceability_data(args.output)
    if data is None:
        return 1

    requirements = parse_requirements_from_docs(args.requirements)

    if args.verbose:
        print(f"Loaded {len(requirements)} documented requirements")
        print(f"Found {len(data['requirements'])} tested requirements")

    # Generate reports
    if args.format in ("markdown", "all"):
        generate_markdown_report(data, requirements, args.output)

    if args.format in ("html", "all"):
        generate_html_report(data, requirements, args.output)

    if args.format == "json":
        print(f"JSON report already exists: {args.output / 'traceability.json'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
