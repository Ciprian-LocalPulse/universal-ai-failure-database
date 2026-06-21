#!/usr/bin/env python3
"""
Universal AI Failure Database — Entry Validator
================================================
Validates a single entry or all entries against the UAIFD JSON schema.

Usage:
    python tools/validate.py data/hallucinations/my-entry.json
    python tools/validate_all.py  # validate everything
"""

import json
import sys
from pathlib import Path
import jsonschema
from rich.console import Console
from rich import print as rprint

console = Console()

SCHEMAS_DIR = Path(__file__).parent.parent / "docs" / "schemas" / "json"

BASE_SCHEMA = {
    "type": "object",
    "required": [
        "id", "category", "subcategory", "severity",
        "model", "prompt", "response", "failure_analysis",
        "tags", "submitted_by", "submission_date", "verified", "license"
    ],
    "properties": {
        "id": {"type": "string"},
        "category": {
            "type": "string",
            "enum": ["hallucination", "math-error", "logic-error", "legal-error", "vulnerability"]
        },
        "subcategory": {"type": "string", "minLength": 1},
        "severity": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low"]
        },
        "model": {
            "type": "object",
            "required": ["name", "provider", "api_date"],
            "properties": {
                "name": {"type": "string"},
                "version": {"type": "string"},
                "provider": {"type": "string"},
                "api_date": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"}
            }
        },
        "prompt": {"type": "string", "minLength": 10},
        "response": {"type": "string", "minLength": 10},
        "failure_analysis": {
            "type": "object",
            "required": ["type", "description", "verified_by"],
            "properties": {
                "type": {"type": "string"},
                "description": {"type": "string", "minLength": 20},
                "verified_by": {"type": "string"},
                "reference_check": {}
            }
        },
        "impact": {"type": "string"},
        "mitigation": {"type": "string"},
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        },
        "submitted_by": {"type": "string"},
        "submission_date": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}$"
        },
        "verified": {"type": "boolean"},
        "verified_date": {"type": "string"},
        "license": {
            "type": "string",
            "enum": ["CC0-1.0"]
        }
    },
    "additionalProperties": True
}


def validate_file(filepath: Path) -> tuple[bool, list[str]]:
    """Validate a single entry file. Returns (is_valid, list_of_errors)."""
    errors = []

    # Load JSON
    try:
        with open(filepath, encoding="utf-8") as f:
            entry = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON parse error: {e}"]
    except OSError as e:
        return False, [f"File read error: {e}"]

    # Schema validation
    validator = jsonschema.Draft7Validator(BASE_SCHEMA)
    for error in validator.iter_errors(entry):
        errors.append(f"Schema error at '{'.'.join(str(p) for p in error.path)}': {error.message}")

    # Additional logical checks
    if entry.get("verified") and not entry.get("verified_date"):
        errors.append("Entry is marked 'verified: true' but has no 'verified_date'.")

    prompt = entry.get("prompt", "")
    if len(prompt) > 10000:
        errors.append("Prompt exceeds 10,000 characters. Consider summarising or truncating.")

    pii_hints = ["@", "phone:", "ssn:", "date of birth", "passport"]
    full_text = json.dumps(entry).lower()
    for hint in pii_hints:
        if hint in full_text and hint == "@":
            # Email check — rough heuristic
            if any(word in full_text for word in ["gmail.com", "hotmail", "yahoo.com"]):
                errors.append("Possible PII detected (email address). Please remove.")

    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 2:
        console.print("[red]Usage: python tools/validate.py <path-to-entry.json>[/red]")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        console.print(f"[red]File not found: {filepath}[/red]")
        sys.exit(1)

    console.print(f"Validating [bold]{filepath}[/bold]...")

    is_valid, errors = validate_file(filepath)

    if is_valid:
        console.print(f"[green]✓ Entry is valid.[/green]")
        sys.exit(0)
    else:
        console.print(f"[red]✗ Entry has {len(errors)} error(s):[/red]")
        for i, err in enumerate(errors, 1):
            console.print(f"  [red]{i}.[/red] {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
