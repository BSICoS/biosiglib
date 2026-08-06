"""Negative and regression tests for the Biosiglib validator."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "tools"))

import validate_specs  # noqa: E402


class ConformanceCaseSchemaTests(unittest.TestCase):
    def test_accepts_literal_vector_expected_output(self) -> None:
        schema = validate_specs.load_json(
            REPOSITORY_ROOT / "schemas" / "conformance-case.schema.json"
        )
        validator = validate_specs.Draft202012Validator(schema)
        case = {
            "$schema": "../../../schemas/conformance-case.schema.json",
            "id": "hrv.example.literal_vector",
            "specification_id": "hrv.example",
            "description": "Exercise a literal vector output without a fixture.",
            "inputs": [{"id": "tk", "value": [0, 1, 2]}],
            "parameters": {},
            "expected_outputs": [
                {
                    "id": "tn",
                    "value": [0, 1, "NaN"],
                    "absolute_tolerance": 0,
                }
            ],
            "nan_equal": True,
            "oracle": {
                "type": "analytical",
                "description": "Literal vector schema regression case.",
            },
        }

        self.assertEqual(list(validator.iter_errors(case)), [])

    def test_accepts_requested_outputs_and_invalid_numerical_result(self) -> None:
        schema = validate_specs.load_json(
            REPOSITORY_ROOT / "schemas" / "conformance-case.schema.json"
        )
        validator = validate_specs.Draft202012Validator(schema)
        case = {
            "$schema": "../../../schemas/conformance-case.schema.json",
            "id": "hrv.example.invalid_numerical_result",
            "specification_id": "hrv.example",
            "description": "Request an optional output that fails numerically.",
            "inputs": [{"id": "tk", "value": [0, 1, 2]}],
            "parameters": {},
            "requested_outputs": ["signal", "modulation"],
            "expected_error": {"category": "invalid_numerical_result"},
            "oracle": {
                "type": "analytical",
                "description": "Schema regression case for output-dependent errors.",
            },
        }

        self.assertEqual(list(validator.iter_errors(case)), [])

    def test_accepts_aggregated_expected_warning(self) -> None:
        schema = validate_specs.load_json(
            REPOSITORY_ROOT / "schemas" / "conformance-case.schema.json"
        )
        validator = validate_specs.Draft202012Validator(schema)
        case = {
            "$schema": "../../../schemas/conformance-case.schema.json",
            "id": "hrv.example.warning",
            "specification_id": "hrv.example",
            "description": "Exercise an aggregated warning expectation.",
            "inputs": [{"id": "pxx", "value": [0, 1, 2]}],
            "parameters": {},
            "expected_outputs": [
                {"id": "lf", "value": 1, "absolute_tolerance": 0}
            ],
            "expected_warnings": [
                {"id": "zero_required_power", "affected_ids": ["lf", "hf"]}
            ],
            "nan_equal": True,
            "oracle": {
                "type": "analytical",
                "description": "Expected-warning schema regression case.",
            },
        }

        self.assertEqual(list(validator.iter_errors(case)), [])

    def test_rejects_expected_warning_on_error_case(self) -> None:
        schema = validate_specs.load_json(
            REPOSITORY_ROOT / "schemas" / "conformance-case.schema.json"
        )
        validator = validate_specs.Draft202012Validator(schema)
        case = {
            "$schema": "../../../schemas/conformance-case.schema.json",
            "id": "hrv.example.error_warning",
            "specification_id": "hrv.example",
            "description": "Warnings are observable only for successful calls.",
            "inputs": [{"id": "pxx", "value": []}],
            "parameters": {},
            "expected_error": {"category": "invalid_value"},
            "expected_warnings": [
                {"id": "zero_required_power", "affected_ids": ["lf"]}
            ],
            "oracle": {
                "type": "analytical",
                "description": "Error/warning exclusivity regression case.",
            },
        }

        self.assertNotEqual(list(validator.iter_errors(case)), [])


class SpecificationDocumentationValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.specification_id = "tools.example"
        self.documentation_reference = (
            f"generated/specifications/{self.specification_id}.md"
        )
        self.documentation_path = (
            self.root / "docs" / "generated" / "specifications"
            / f"{self.specification_id}.md"
        )
        self.documentation_path.parent.mkdir(parents=True)
        self.documentation_path.write_text("# Example\n", encoding="utf-8")
        (self.root / "docs" / "specifications.md").write_text(
            f"[Example]({self.documentation_reference})\n",
            encoding="utf-8",
        )
        (self.root / "mkdocs.yml").write_text(
            f"nav:\n  - Example: {self.documentation_reference}\n",
            encoding="utf-8",
        )
        self.specs_by_id = {self.specification_id: {}}

    def validate(self) -> list[str]:
        return validate_specs.validate_specification_documentation(
            self.root,
            self.specs_by_id,
        )

    def test_accepts_generated_indexed_and_navigable_specification(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_rejects_missing_generated_specification_page(self) -> None:
        self.documentation_path.unlink()

        errors = self.validate()

        self.assertTrue(
            any("generated page" in error and "is missing" in error for error in errors)
        )

    def test_rejects_specification_missing_from_index(self) -> None:
        (self.root / "docs" / "specifications.md").write_text(
            "# Specifications\n",
            encoding="utf-8",
        )

        errors = self.validate()

        self.assertTrue(any("is not listed" in error for error in errors))

    def test_rejects_specification_missing_from_navigation(self) -> None:
        (self.root / "mkdocs.yml").write_text("nav: []\n", encoding="utf-8")

        errors = self.validate()

        self.assertTrue(
            any("is not listed in navigation" in error for error in errors)
        )


class ExistingNegativeValidationTests(unittest.TestCase):
    def test_rejects_unknown_warning_and_affected_id(self) -> None:
        root = Path("repository").resolve()
        case_path = root / "conformance" / "hrv" / "example" / "unknown_warning.json"
        cases = [
            (
                case_path,
                {
                    "specification_id": "hrv.example",
                    "inputs": [],
                    "parameters": {},
                    "expected_outputs": [],
                    "expected_warnings": [
                        {"id": "unknown_warning", "affected_ids": ["unknown_id"]}
                    ],
                },
            )
        ]
        specs_by_id = {
            "hrv.example": {
                "input_ids": {"pxx"},
                "parameter_ids": set(),
                "output_ids": {"lf"},
                "warning_ids": {"zero_required_power"},
            }
        }

        errors = validate_specs.validate_conformance_references(
            root,
            cases,
            specs_by_id=specs_by_id,
            fixtures_by_id={},
            known_reference_ids=set(),
        )

        self.assertTrue(
            any("unknown specification warning id 'unknown_warning'" in error for error in errors)
        )
        self.assertTrue(
            any("unknown specification input or output id 'unknown_id'" in error for error in errors)
        )

    def test_rejects_unknown_requested_output(self) -> None:
        root = Path("repository").resolve()
        case_path = root / "conformance" / "hrv" / "example" / "unknown_output.json"
        cases = [
            (
                case_path,
                {
                    "specification_id": "hrv.example",
                    "inputs": [],
                    "parameters": {},
                    "requested_outputs": ["unknown_output"],
                    "expected_error": {"category": "invalid_value"},
                    "oracle": {
                        "type": "analytical",
                        "description": "Validator cross-reference regression case.",
                    },
                },
            )
        ]
        specs_by_id = {
            "hrv.example": {
                "input_ids": set(),
                "parameter_ids": set(),
                "output_ids": {"ihr"},
            }
        }

        errors = validate_specs.validate_conformance_references(
            root,
            cases,
            specs_by_id=specs_by_id,
            fixtures_by_id={},
            known_reference_ids=set(),
        )

        self.assertTrue(
            any("unknown specification output id 'unknown_output'" in error for error in errors)
        )

    def test_rejects_unknown_conformance_specification(self) -> None:
        root = Path("repository").resolve()
        case_path = root / "conformance" / "tools" / "example" / "unknown.json"
        cases = [
            (
                case_path,
                {
                    "specification_id": "tools.unknown",
                    "inputs": [],
                    "parameters": {},
                    "expected_outputs": [],
                },
            )
        ]

        errors = validate_specs.validate_conformance_references(
            root,
            cases,
            specs_by_id={},
            fixtures_by_id={},
            known_reference_ids=set(),
        )

        self.assertTrue(any("unknown specification id" in error for error in errors))

    def test_rejects_manifest_commit_mismatch(self) -> None:
        errors = validate_specs.validate_manifest_commit(
            {"biosiglib": {"commit": "old-commit"}},
            Path("conformance.json"),
            "current-commit",
        )

        self.assertEqual(len(errors), 1)
        self.assertIn("does not match current Biosiglib commit", errors[0])


if __name__ == "__main__":
    unittest.main()
