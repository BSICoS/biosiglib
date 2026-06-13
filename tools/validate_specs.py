"""Validate Biosiglib schemas, catalogs, specifications, fixtures, and cases."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from json import JSONDecodeError
from pathlib import Path
from typing import Any

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


def load_json(path: Path) -> Any:
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


def relative_name(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def display_path(path: Path) -> str:
    return str(path)


def report_schema_errors(
    validator: Draft202012Validator,
    instance: Any,
    path: Path,
    root: Path,
) -> list[str]:
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: item.path):
        errors.append(f"{relative_name(path, root)}: {json_path(error.path)}: {error.message}")
    return errors


def check_schema(schema: Any, path: Path, root: Path) -> list[str]:
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema may raise several schema error types.
        return [f"{relative_name(path, root)}: invalid schema: {exc}"]
    return []


def make_validator(schema: Any) -> Draft202012Validator:
    return Draft202012Validator(
        schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Biosiglib specifications and optional implementation manifests.",
    )
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        metavar="PATH",
        help="Validate an external implementation manifest.",
    )
    return parser


def collect_reference_ids(reference_catalog: Any) -> tuple[set[str], list[str]]:
    references = reference_catalog.get("references", []) if isinstance(reference_catalog, dict) else []
    ids = [entry.get("id") for entry in references if isinstance(entry, dict)]
    counts = Counter(ids)
    duplicate_errors = []

    for index, entry in enumerate(references):
        if not isinstance(entry, dict):
            continue
        reference_id = entry.get("id")
        if isinstance(reference_id, str) and counts[reference_id] > 1:
            duplicate_errors.append(
                "references/references.json: "
                f"{json_path(['references', index, 'id'])}: duplicate reference id '{reference_id}'"
            )

    return {reference_id for reference_id in ids if isinstance(reference_id, str)}, duplicate_errors


def load_algorithm_specs(
    root: Path,
    validator: Draft202012Validator,
    known_reference_ids: set[str],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    errors = []
    specs_by_id: dict[str, dict[str, Any]] = {}

    for spec_path in sorted((root / "specs").rglob("spec.json")):
        print(f"Validating {relative_name(spec_path, root)}")
        spec = load_json(spec_path)
        errors.extend(report_schema_errors(validator, spec, spec_path, root))

        if not isinstance(spec, dict):
            continue

        metadata = spec.get("metadata", {})
        specification_id = metadata.get("id") if isinstance(metadata, dict) else None
        normative = spec.get("normative", {})
        inputs = normative.get("inputs", []) if isinstance(normative, dict) else []
        parameters = normative.get("parameters", []) if isinstance(normative, dict) else []
        outputs = normative.get("outputs", []) if isinstance(normative, dict) else []

        if isinstance(specification_id, str):
            specs_by_id[specification_id] = {
                "path": spec_path,
                "input_ids": {
                    entry.get("id") for entry in inputs if isinstance(entry, dict)
                },
                "parameter_ids": {
                    entry.get("id") for entry in parameters if isinstance(entry, dict)
                },
                "output_ids": {
                    entry.get("id") for entry in outputs if isinstance(entry, dict)
                },
            }

        provenance_references = (
            spec.get("provenance", {}).get("references", [])
            if isinstance(spec.get("provenance"), dict)
            else []
        )
        for index, reference in enumerate(provenance_references):
            if not isinstance(reference, dict):
                continue
            reference_id = reference.get("id")
            if isinstance(reference_id, str) and reference_id not in known_reference_ids:
                errors.append(
                    f"{relative_name(spec_path, root)}: missing reference id '{reference_id}' "
                    f"at {json_path(['provenance', 'references', index, 'id'])}"
                )

    return specs_by_id, errors


def collect_fixture_ids(fixture_catalog: Any) -> tuple[set[str], list[str]]:
    fixtures = fixture_catalog.get("fixtures", []) if isinstance(fixture_catalog, dict) else []
    ids = [entry.get("id") for entry in fixtures if isinstance(entry, dict)]
    counts = Counter(ids)
    duplicate_errors = []

    for index, fixture in enumerate(fixtures):
        if not isinstance(fixture, dict):
            continue
        fixture_id = fixture.get("id")
        if isinstance(fixture_id, str) and counts[fixture_id] > 1:
            duplicate_errors.append(
                "fixtures/catalog.json: "
                f"{json_path(['fixtures', index, 'id'])}: duplicate fixture id '{fixture_id}'"
            )

    return {fixture_id for fixture_id in ids if isinstance(fixture_id, str)}, duplicate_errors


def resolve_fixture_path(root: Path, declared_path: str) -> Path | None:
    candidate = Path(declared_path)
    if candidate.is_absolute():
        return None
    return (root / candidate).resolve()


def is_inside_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False
    return True


def read_csv_header(path: Path) -> list[str] | None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return next(reader, None)


def load_fixtures(
    root: Path,
    fixture_catalog: Any,
    known_fixture_ids: set[str],
    known_reference_ids: set[str],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    errors = []
    fixtures_by_id: dict[str, dict[str, Any]] = {}
    fixtures = fixture_catalog.get("fixtures", []) if isinstance(fixture_catalog, dict) else []

    for fixture_index, fixture in enumerate(fixtures):
        if not isinstance(fixture, dict):
            continue

        fixture_id = fixture.get("id")
        if not isinstance(fixture_id, str):
            continue

        source = fixture.get("source", {})
        if isinstance(source, dict):
            for ref_index, parent_id in enumerate(source.get("parent_fixture_ids", [])):
                if isinstance(parent_id, str) and parent_id not in known_fixture_ids:
                    errors.append(
                        "fixtures/catalog.json: "
                        f"{json_path(['fixtures', fixture_index, 'source', 'parent_fixture_ids', ref_index])}: "
                        f"unknown parent fixture id '{parent_id}'"
                    )
            for ref_index, reference_id in enumerate(source.get("reference_ids", [])):
                if isinstance(reference_id, str) and reference_id not in known_reference_ids:
                    errors.append(
                        "fixtures/catalog.json: "
                        f"{json_path(['fixtures', fixture_index, 'source', 'reference_ids', ref_index])}: "
                        f"unknown reference id '{reference_id}'"
                    )

        files_by_role: dict[str, dict[str, Any]] = {}
        files = fixture.get("files", [])
        for file_index, file_entry in enumerate(files):
            if not isinstance(file_entry, dict):
                continue

            role = file_entry.get("role")
            declared_path = file_entry.get("path")
            declared_format = file_entry.get("format")
            path_json = ["fixtures", fixture_index, "files", file_index, "path"]
            format_json = ["fixtures", fixture_index, "files", file_index, "format"]

            if not isinstance(role, str) or not isinstance(declared_path, str):
                continue

            fixture_file = {
                "format": declared_format,
                "header": None,
                "path": None,
            }
            files_by_role[role] = fixture_file

            print(f"Validating {declared_path}")
            resolved_path = resolve_fixture_path(root, declared_path)
            if resolved_path is None:
                errors.append(
                    "fixtures/catalog.json: "
                    f"{json_path(path_json)}: fixture path '{declared_path}' must be relative"
                )
                continue

            fixture_file["path"] = resolved_path
            if not is_inside_root(resolved_path, root):
                errors.append(
                    "fixtures/catalog.json: "
                    f"{json_path(path_json)}: fixture path '{declared_path}' resolves outside the repository"
                )
                continue

            if isinstance(declared_format, str):
                expected_suffix = f".{declared_format}"
                if resolved_path.suffix.lower() != expected_suffix:
                    errors.append(
                        "fixtures/catalog.json: "
                        f"{json_path(format_json)}: fixture file '{declared_path}' does not match "
                        f"declared format '{declared_format}'"
                    )

            if not resolved_path.is_file():
                errors.append(
                    "fixtures/catalog.json: "
                    f"{json_path(path_json)}: fixture file '{declared_path}' does not exist"
                )
                continue

            if declared_format == "csv":
                try:
                    fixture_file["header"] = read_csv_header(resolved_path)
                except OSError as exc:
                    errors.append(
                        "fixtures/catalog.json: "
                        f"{json_path(path_json)}: could not read CSV file '{declared_path}': {exc}"
                    )

        fixtures_by_id[fixture_id] = {
            "files_by_role": files_by_role,
        }

    return fixtures_by_id, errors


def load_conformance_cases(
    root: Path,
    validator: Draft202012Validator,
) -> tuple[list[tuple[Path, Any]], list[str]]:
    errors = []
    cases = []

    for case_path in sorted((root / "conformance").rglob("*.json")):
        print(f"Validating {relative_name(case_path, root)}")
        case = load_json(case_path)
        errors.extend(report_schema_errors(validator, case, case_path, root))
        cases.append((case_path, case))

    ids = [
        case.get("id")
        for _, case in cases
        if isinstance(case, dict) and isinstance(case.get("id"), str)
    ]
    counts = Counter(ids)
    for case_path, case in cases:
        if not isinstance(case, dict):
            continue
        case_id = case.get("id")
        if isinstance(case_id, str) and counts[case_id] > 1:
            errors.append(
                f"{relative_name(case_path, root)}: $.id: duplicate conformance-case id '{case_id}'"
            )

    return cases, errors


def report_duplicate_case_entries(
    case_path: Path,
    root: Path,
    case: dict[str, Any],
    field_name: str,
    label: str,
) -> list[str]:
    errors = []
    entries = case.get(field_name, [])
    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    counts = Counter(ids)

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        entry_id = entry.get("id")
        if isinstance(entry_id, str) and counts[entry_id] > 1:
            errors.append(
                f"{relative_name(case_path, root)}: "
                f"{json_path([field_name, index, 'id'])}: duplicate {label} id '{entry_id}'"
            )

    return errors


def validate_conformance_references(
    root: Path,
    cases: list[tuple[Path, Any]],
    specs_by_id: dict[str, dict[str, Any]],
    fixtures_by_id: dict[str, dict[str, Any]],
    known_reference_ids: set[str],
) -> list[str]:
    errors = []

    for case_path, case in cases:
        if not isinstance(case, dict):
            continue

        specification_id = case.get("specification_id")
        spec_info = specs_by_id.get(specification_id) if isinstance(specification_id, str) else None
        if isinstance(specification_id, str) and spec_info is None:
            errors.append(
                f"{relative_name(case_path, root)}: $.specification_id: "
                f"unknown specification id '{specification_id}'"
            )

        errors.extend(report_duplicate_case_entries(case_path, root, case, "inputs", "input"))
        errors.extend(
            report_duplicate_case_entries(case_path, root, case, "expected_outputs", "expected output")
        )

        for input_index, input_mapping in enumerate(case.get("inputs", [])):
            if not isinstance(input_mapping, dict):
                continue

            input_id = input_mapping.get("id")
            if spec_info is not None and isinstance(input_id, str):
                if input_id not in spec_info["input_ids"]:
                    errors.append(
                        f"{relative_name(case_path, root)}: "
                        f"{json_path(['inputs', input_index, 'id'])}: unknown specification input id "
                        f"'{input_id}'"
                    )

            fixture_id = input_mapping.get("fixture_id")
            fixture_info = fixtures_by_id.get(fixture_id) if isinstance(fixture_id, str) else None
            if isinstance(fixture_id, str) and fixture_info is None:
                errors.append(
                    f"{relative_name(case_path, root)}: "
                    f"{json_path(['inputs', input_index, 'fixture_id'])}: unknown fixture id "
                    f"'{fixture_id}'"
                )
                continue

            file_role = input_mapping.get("file_role")
            fixture_file = None
            if fixture_info is not None and isinstance(file_role, str):
                fixture_file = fixture_info["files_by_role"].get(file_role)
                if fixture_file is None:
                    errors.append(
                        f"{relative_name(case_path, root)}: "
                        f"{json_path(['inputs', input_index, 'file_role'])}: unknown fixture file role "
                        f"'{file_role}'"
                    )
                    continue

            if fixture_file is not None:
                if fixture_file.get("format") != "csv":
                    errors.append(
                        f"{relative_name(case_path, root)}: "
                        f"{json_path(['inputs', input_index, 'file_role'])}: fixture file role "
                        f"'{file_role}' is not CSV"
                    )
                    continue

                column = input_mapping.get("column")
                header = fixture_file.get("header")
                if isinstance(column, str) and isinstance(header, list) and column not in header:
                    errors.append(
                        f"{relative_name(case_path, root)}: "
                        f"{json_path(['inputs', input_index, 'column'])}: missing CSV column "
                        f"'{column}'"
                    )

        parameters = case.get("parameters", {})
        if spec_info is not None and isinstance(parameters, dict):
            for parameter_id in parameters:
                if parameter_id not in spec_info["parameter_ids"]:
                    errors.append(
                        f"{relative_name(case_path, root)}: "
                        f"{json_path(['parameters', parameter_id])}: unknown specification parameter id "
                        f"'{parameter_id}'"
                    )

        for output_index, expected_output in enumerate(case.get("expected_outputs", [])):
            if not isinstance(expected_output, dict):
                continue
            output_id = expected_output.get("id")
            if spec_info is not None and isinstance(output_id, str):
                if output_id not in spec_info["output_ids"]:
                    errors.append(
                        f"{relative_name(case_path, root)}: "
                        f"{json_path(['expected_outputs', output_index, 'id'])}: unknown specification output id "
                        f"'{output_id}'"
                    )

        oracle = case.get("oracle", {})
        if isinstance(oracle, dict):
            for ref_index, reference_id in enumerate(oracle.get("reference_ids", [])):
                if isinstance(reference_id, str) and reference_id not in known_reference_ids:
                    errors.append(
                        f"{relative_name(case_path, root)}: "
                        f"{json_path(['oracle', 'reference_ids', ref_index])}: unknown reference id "
                        f"'{reference_id}'"
                    )

    return errors


def get_current_git_commit(
    root: Path,
    git_command: str = "git",
) -> tuple[str | None, str | None]:
    try:
        result = subprocess.run(
            [git_command, "-C", str(root), "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return None, f"could not run git to determine the Biosiglib commit: {exc}"

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git rev-parse failed"
        return None, f"could not determine the Biosiglib commit: {message}"

    commit = result.stdout.strip()
    if not commit:
        return None, "could not determine the Biosiglib commit: git returned an empty commit"

    return commit, None


def load_external_manifest(path_argument: str) -> tuple[Path, Any | None, list[str]]:
    manifest_path = Path(path_argument).expanduser()
    if not manifest_path.is_absolute():
        manifest_path = (Path.cwd() / manifest_path).resolve()
    else:
        manifest_path = manifest_path.resolve()

    if not manifest_path.exists():
        return manifest_path, None, [f"{display_path(manifest_path)}: manifest file does not exist"]
    if not manifest_path.is_file():
        return manifest_path, None, [f"{display_path(manifest_path)}: manifest path is not a regular file"]

    try:
        return manifest_path, load_json(manifest_path), []
    except JSONDecodeError as exc:
        return manifest_path, None, [
            f"{display_path(manifest_path)}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ]
    except OSError as exc:
        return manifest_path, None, [f"{display_path(manifest_path)}: could not read manifest: {exc}"]


def report_external_schema_errors(
    validator: Draft202012Validator,
    manifest: Any,
    manifest_path: Path,
) -> list[str]:
    errors = []
    for error in sorted(validator.iter_errors(manifest), key=lambda item: item.path):
        errors.append(f"{display_path(manifest_path)}: {json_path(error.path)}: {error.message}")
    return errors


def validate_manifest_specification_ids(
    manifest: Any,
    manifest_path: Path,
    specs_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    if not isinstance(manifest, dict):
        return []

    specifications = manifest.get("specifications", {})
    if not isinstance(specifications, dict):
        return []

    errors = []
    for specification_id in specifications:
        if specification_id not in specs_by_id:
            errors.append(
                f"{display_path(manifest_path)}: "
                f"{json_path(['specifications', specification_id])}: unknown specification id "
                f"'{specification_id}'"
            )
    return errors


def validate_manifest_commit(
    manifest: Any,
    manifest_path: Path,
    current_commit: str | None,
) -> list[str]:
    if current_commit is None or not isinstance(manifest, dict):
        return []

    biosiglib = manifest.get("biosiglib", {})
    if not isinstance(biosiglib, dict):
        return []

    declared_commit = biosiglib.get("commit")
    if isinstance(declared_commit, str) and declared_commit != current_commit:
        return [
            f"{display_path(manifest_path)}: $.biosiglib.commit: declared commit "
            f"'{declared_commit}' does not match current Biosiglib commit '{current_commit}'"
        ]

    return []


def validate_external_manifest(
    path_argument: str,
    validator: Draft202012Validator,
    specs_by_id: dict[str, dict[str, Any]],
    current_commit: str | None,
) -> list[str]:
    manifest_path, manifest, errors = load_external_manifest(path_argument)
    print(f"Validating {display_path(manifest_path)}")
    if manifest is None:
        return errors

    errors.extend(report_external_schema_errors(validator, manifest, manifest_path))
    errors.extend(validate_manifest_specification_ids(manifest, manifest_path, specs_by_id))
    errors.extend(validate_manifest_commit(manifest, manifest_path, current_commit))
    return errors


def validate_repository(root: Path) -> tuple[list[str], dict[str, dict[str, Any]], dict[str, Draft202012Validator]]:
    errors: list[str] = []

    schema_paths = {
        "algorithm": root / "schemas" / "algorithm-spec.schema.json",
        "reference": root / "schemas" / "reference-catalog.schema.json",
        "fixture": root / "schemas" / "fixture-catalog.schema.json",
        "conformance": root / "schemas" / "conformance-case.schema.json",
        "implementation_manifest": root / "schemas" / "implementation-manifest.schema.json",
    }

    schemas: dict[str, Any] = {}
    for name, schema_path in schema_paths.items():
        print(f"Validating {relative_name(schema_path, root)}")
        schema = load_json(schema_path)
        schemas[name] = schema
        errors.extend(check_schema(schema, schema_path, root))

    validators = {
        name: make_validator(schema)
        for name, schema in schemas.items()
    }

    references_path = root / "references" / "references.json"
    print(f"Validating {relative_name(references_path, root)}")
    reference_catalog = load_json(references_path)
    errors.extend(
        report_schema_errors(validators["reference"], reference_catalog, references_path, root)
    )
    known_reference_ids, duplicate_reference_errors = collect_reference_ids(reference_catalog)
    errors.extend(duplicate_reference_errors)

    specs_by_id, spec_errors = load_algorithm_specs(
        root,
        validators["algorithm"],
        known_reference_ids,
    )
    errors.extend(spec_errors)

    fixture_catalog_path = root / "fixtures" / "catalog.json"
    print(f"Validating {relative_name(fixture_catalog_path, root)}")
    fixture_catalog = load_json(fixture_catalog_path)
    errors.extend(
        report_schema_errors(validators["fixture"], fixture_catalog, fixture_catalog_path, root)
    )
    known_fixture_ids, duplicate_fixture_errors = collect_fixture_ids(fixture_catalog)
    errors.extend(duplicate_fixture_errors)

    fixtures_by_id, fixture_errors = load_fixtures(
        root,
        fixture_catalog,
        known_fixture_ids,
        known_reference_ids,
    )
    errors.extend(fixture_errors)

    cases, case_errors = load_conformance_cases(root, validators["conformance"])
    errors.extend(case_errors)
    errors.extend(
        validate_conformance_references(
            root,
            cases,
            specs_by_id,
            fixtures_by_id,
            known_reference_ids,
        )
    )

    return errors, specs_by_id, validators


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    root = find_repository_root()
    errors, specs_by_id, validators = validate_repository(root)

    current_commit = None
    if args.manifest:
        current_commit, commit_error = get_current_git_commit(root)
        if commit_error is not None:
            errors.append(f"Biosiglib checkout: {commit_error}")

        for manifest_path in args.manifest:
            errors.extend(
                validate_external_manifest(
                    manifest_path,
                    validators["implementation_manifest"],
                    specs_by_id,
                    current_commit,
                )
            )

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
