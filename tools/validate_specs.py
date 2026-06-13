"""Validate Biosiglib schemas, references, and algorithm specifications."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator


def find_repository_root() -> Path:
    """Find the repository root from this script location."""
    for candidate in Path(__file__).resolve().parents:
        if (
            (candidate / "AGENTS.md").is_file()
            and (candidate / "schemas").is_dir()
            and (candidate / "specs").is_dir()
        ):
            return candidate
    raise RuntimeError("Could not locate the Biosiglib repository root.")


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def json_path(path_parts: object) -> str:
    parts = list(path_parts)
    if not parts:
        return "$"

    result = "$"
    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += f".{part}"
    return result


def report_schema_errors(
    validator: Draft202012Validator,
    instance: object,
    path: Path,
    root: Path,
) -> list[str]:
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: item.path):
        errors.append(f"{path.relative_to(root)}: {json_path(error.path)}: {error.message}")
    return errors


def collect_reference_ids(reference_catalog: object) -> tuple[set[str], list[str]]:
    references = reference_catalog.get("references", [])
    ids = [entry.get("id") for entry in references if isinstance(entry, dict)]
    counts = Counter(ids)
    duplicate_errors = []

    for index, entry in enumerate(references):
        if not isinstance(entry, dict):
            continue
        reference_id = entry.get("id")
        if reference_id is not None and counts[reference_id] > 1:
            duplicate_errors.append(
                "references/references.json: "
                f"{json_path(['references', index, 'id'])}: duplicate reference id '{reference_id}'"
            )

    return {reference_id for reference_id in ids if isinstance(reference_id, str)}, duplicate_errors


def report_unresolved_references(
    spec: object,
    spec_path: Path,
    root: Path,
    known_reference_ids: set[str],
) -> list[str]:
    errors = []
    provenance_references = (
        spec.get("provenance", {}).get("references", [])
        if isinstance(spec, dict)
        else []
    )

    for index, reference in enumerate(provenance_references):
        if not isinstance(reference, dict):
            continue
        reference_id = reference.get("id")
        if isinstance(reference_id, str) and reference_id not in known_reference_ids:
            errors.append(
                f"{spec_path.relative_to(root)}: missing reference id '{reference_id}' "
                f"at {json_path(['provenance', 'references', index, 'id'])}"
            )

    return errors


def main() -> int:
    root = find_repository_root()
    errors: list[str] = []

    algorithm_schema_path = root / "schemas" / "algorithm-spec.schema.json"
    reference_schema_path = root / "schemas" / "reference-catalog.schema.json"
    references_path = root / "references" / "references.json"

    print(f"Validating {algorithm_schema_path.relative_to(root)}")
    algorithm_schema = load_json(algorithm_schema_path)
    try:
        Draft202012Validator.check_schema(algorithm_schema)
    except Exception as exc:  # jsonschema may raise several schema error types.
        errors.append(f"{algorithm_schema_path.relative_to(root)}: invalid schema: {exc}")

    print(f"Validating {reference_schema_path.relative_to(root)}")
    reference_schema = load_json(reference_schema_path)
    try:
        Draft202012Validator.check_schema(reference_schema)
    except Exception as exc:
        errors.append(f"{reference_schema_path.relative_to(root)}: invalid schema: {exc}")

    reference_validator = Draft202012Validator(
        reference_schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
    algorithm_validator = Draft202012Validator(
        algorithm_schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )

    print(f"Validating {references_path.relative_to(root)}")
    reference_catalog = load_json(references_path)
    errors.extend(report_schema_errors(reference_validator, reference_catalog, references_path, root))
    known_reference_ids, duplicate_reference_errors = collect_reference_ids(reference_catalog)
    errors.extend(duplicate_reference_errors)

    spec_paths = sorted((root / "specs").rglob("spec.json"))
    for spec_path in spec_paths:
        print(f"Validating {spec_path.relative_to(root)}")
        spec = load_json(spec_path)
        errors.extend(report_schema_errors(algorithm_validator, spec, spec_path, root))
        errors.extend(report_unresolved_references(spec, spec_path, root, known_reference_ids))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
