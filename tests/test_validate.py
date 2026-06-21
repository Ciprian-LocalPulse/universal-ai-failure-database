"""
Unit tests for UAIFD tooling.
"""
import json
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from validate import validate_file, BASE_SCHEMA


# ── Fixtures ──────────────────────────────────────────────────────────────────

VALID_ENTRY = {
    "id": "UAIFD-HAL-TEST",
    "category": "hallucination",
    "subcategory": "fabricated_citation",
    "severity": "high",
    "model": {
        "name": "TestModel",
        "version": "test-1.0",
        "provider": "TestProvider",
        "api_date": "2024-01-01"
    },
    "prompt": "This is a test prompt of sufficient length to pass validation requirements.",
    "response": "This is a test response of sufficient length to pass validation requirements.",
    "failure_analysis": {
        "type": "fabricated_citation",
        "description": "This is a test failure description with sufficient length to pass the minimum character check.",
        "verified_by": "Manual verification by test suite",
        "reference_check": None
    },
    "impact": "Test impact statement.",
    "mitigation": "Test mitigation.",
    "tags": ["test", "hallucination"],
    "submitted_by": "test-user",
    "submission_date": "2024-01-01",
    "verified": False,
    "license": "CC0-1.0"
}


# ── Tests ──────────────────────────────────────────────────────────────────────

class TestValidateFile:

    def test_valid_entry(self, tmp_path):
        """A well-formed entry should pass validation."""
        f = tmp_path / "valid.json"
        f.write_text(json.dumps(VALID_ENTRY))
        is_valid, errors = validate_file(f)
        assert is_valid, f"Expected valid entry, got errors: {errors}"

    def test_missing_required_field(self, tmp_path):
        """Missing a required field should fail."""
        entry = {**VALID_ENTRY}
        del entry["severity"]
        f = tmp_path / "missing_field.json"
        f.write_text(json.dumps(entry))
        is_valid, errors = validate_file(f)
        assert not is_valid
        assert any("severity" in e for e in errors)

    def test_invalid_category(self, tmp_path):
        """An invalid category enum value should fail."""
        entry = {**VALID_ENTRY, "category": "not-a-real-category"}
        f = tmp_path / "bad_category.json"
        f.write_text(json.dumps(entry))
        is_valid, errors = validate_file(f)
        assert not is_valid

    def test_invalid_severity(self, tmp_path):
        """An invalid severity value should fail."""
        entry = {**VALID_ENTRY, "severity": "extreme"}
        f = tmp_path / "bad_severity.json"
        f.write_text(json.dumps(entry))
        is_valid, errors = validate_file(f)
        assert not is_valid

    def test_invalid_license(self, tmp_path):
        """Only CC0-1.0 is accepted."""
        entry = {**VALID_ENTRY, "license": "MIT"}
        f = tmp_path / "bad_license.json"
        f.write_text(json.dumps(entry))
        is_valid, errors = validate_file(f)
        assert not is_valid

    def test_invalid_json(self, tmp_path):
        """Malformed JSON should fail gracefully."""
        f = tmp_path / "bad.json"
        f.write_text("{invalid json{{")
        is_valid, errors = validate_file(f)
        assert not is_valid
        assert any("JSON" in e for e in errors)

    def test_verified_without_date(self, tmp_path):
        """verified: true without verified_date should produce a warning."""
        entry = {**VALID_ENTRY, "verified": True}
        f = tmp_path / "verified_no_date.json"
        f.write_text(json.dumps(entry))
        is_valid, errors = validate_file(f)
        assert not is_valid
        assert any("verified_date" in e for e in errors)

    def test_verified_with_date(self, tmp_path):
        """verified: true WITH verified_date should pass."""
        entry = {**VALID_ENTRY, "verified": True, "verified_date": "2024-06-01"}
        f = tmp_path / "verified_with_date.json"
        f.write_text(json.dumps(entry))
        is_valid, errors = validate_file(f)
        assert is_valid, f"Errors: {errors}"

    def test_invalid_date_format(self, tmp_path):
        """Date fields must be YYYY-MM-DD."""
        entry = {**VALID_ENTRY}
        entry["model"] = {**VALID_ENTRY["model"], "api_date": "01/01/2024"}
        f = tmp_path / "bad_date.json"
        f.write_text(json.dumps(entry))
        is_valid, errors = validate_file(f)
        assert not is_valid

    def test_all_severity_values(self, tmp_path):
        """All four severity levels should be valid."""
        for sev in ["critical", "high", "medium", "low"]:
            entry = {**VALID_ENTRY, "severity": sev}
            f = tmp_path / f"sev_{sev}.json"
            f.write_text(json.dumps(entry))
            is_valid, errors = validate_file(f)
            assert is_valid, f"Severity '{sev}' should be valid. Errors: {errors}"

    def test_all_category_values(self, tmp_path):
        """All five categories should be valid."""
        for cat in ["hallucination", "math-error", "logic-error", "legal-error", "vulnerability"]:
            entry = {**VALID_ENTRY, "category": cat}
            f = tmp_path / f"cat_{cat.replace('-','_')}.json"
            f.write_text(json.dumps(entry))
            is_valid, errors = validate_file(f)
            assert is_valid, f"Category '{cat}' should be valid. Errors: {errors}"


class TestExistingEntries:
    """Integration tests — validate all shipped entries."""

    DATA_DIR = Path(__file__).parent.parent / "data"

    def test_existing_entries_are_valid(self):
        """All entries in the data/ directory should pass validation."""
        json_files = list(self.DATA_DIR.rglob("*.json"))
        assert len(json_files) > 0, "No JSON entries found in data/ directory"

        failures = []
        for f in json_files:
            is_valid, errors = validate_file(f)
            if not is_valid:
                failures.append((f.name, errors))

        if failures:
            msg = "\n".join(f"{name}: {errs}" for name, errs in failures)
            pytest.fail(f"{len(failures)} existing entries failed validation:\n{msg}")
