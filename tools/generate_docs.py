"""Generate MkDocs specification pages from Biosiglib JSON specifications."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


GENERATED_SPEC_DIR = Path("docs") / "generated" / "specifications"
SPEC_GLOB = "specs/*/*/spec.json"
REPOSITORY_URL = "https://github.com/BSICoS/biosiglib"


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


def relative_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def markdown_escape_cell(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def inline_code(value: object) -> str:
    return f"`{value}`"


def json_scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def format_default(value: Any) -> str:
    if value is None:
        return ""
    return json.dumps(value, sort_keys=True)


def format_constraints(value: Any) -> str:
    if not isinstance(value, dict) or not value:
        return "None"

    parts = []
    for key in sorted(value):
        parts.append(f"{key}={json.dumps(value[key], sort_keys=True)}")
    return ", ".join(parts)


def table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape_cell(cell) for cell in row) + " |")
    return lines


def title_for_key(key: str) -> str:
    return key.replace("_", " ").capitalize()


def ordered_behavior_keys(behavior: dict[str, Any]) -> list[str]:
    preferred = [
        "nan_handling",
        "empty_input",
        "input_orientation",
        "insufficient_data",
    ]
    keys = [key for key in preferred if key in behavior]
    keys.extend(sorted(key for key in behavior if key not in set(preferred)))
    return keys


def discover_specs(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    specs = []
    for spec_path in sorted(root.glob(SPEC_GLOB)):
        spec = load_json(spec_path)
        if not isinstance(spec, dict):
            raise ValueError(f"{relative_path(spec_path, root)} did not contain a JSON object")
        specs.append((spec_path, spec))

    return sorted(
        specs,
        key=lambda item: (
            item[1].get("metadata", {}).get("id", ""),
            relative_path(item[0], root),
        ),
    )


def conformance_cases(root: Path, module: str, algorithm: str) -> list[tuple[Path, str]]:
    case_dir = root / "conformance" / module / algorithm
    cases = []
    for case_path in sorted(case_dir.glob("*.json")):
        case = load_json(case_path)
        case_id = case.get("id") if isinstance(case, dict) else case_path.stem
        cases.append((case_path, str(case_id)))
    return cases


def github_blob_url(root: Path, path: Path) -> str:
    return f"{REPOSITORY_URL}/blob/main/{relative_path(path, root)}"


def render_spec_page(root: Path, spec_path: Path, spec: dict[str, Any]) -> str:
    metadata = spec.get("metadata", {})
    informative = spec.get("informative", {})
    provenance = spec.get("provenance", {})
    normative = spec.get("normative", {})

    if not isinstance(metadata, dict):
        metadata = {}
    if not isinstance(informative, dict):
        informative = {}
    if not isinstance(provenance, dict):
        provenance = {}
    if not isinstance(normative, dict):
        normative = {}

    specification_id = str(metadata.get("id", spec_path.parent.name))
    module = str(metadata.get("module", ""))
    algorithm = spec_path.parent.name
    title = str(informative.get("title", specification_id))

    lines = [
        f"# {title}",
        "",
        "!!! warning \"Generated page\"",
        "    This page is generated from the Biosiglib JSON specification. Do not edit it manually; update the JSON source and run `python tools/generate_docs.py` instead.",
        "",
        "## Metadata",
        "",
    ]

    lines.extend(
        table(
            ["Field", "Value"],
            [
                ["Canonical specification ID", inline_code(specification_id)],
                ["Module", inline_code(module)],
                [
                    "Source JSON",
                    f"[{relative_path(spec_path, root)}]({github_blob_url(root, spec_path)})",
                ],
            ],
        )
    )

    summary = informative.get("summary")
    description = informative.get("description")
    if summary or description:
        lines.extend(["", "## Summary", ""])
        if summary:
            lines.extend([str(summary), ""])
        if description:
            lines.append(str(description))

    keywords = informative.get("keywords", [])
    if keywords:
        lines.extend(["", "## Keywords", ""])
        lines.append(", ".join(inline_code(keyword) for keyword in keywords))

    references = provenance.get("references", []) if isinstance(provenance, dict) else []
    lines.extend(["", "## Scientific References", ""])
    if references:
        rows = []
        for reference in references:
            if not isinstance(reference, dict):
                continue
            rows.append(
                [
                    inline_code(reference.get("id", "")),
                    reference.get("relation", ""),
                    reference.get("note", ""),
                ]
            )
        lines.extend(table(["ID", "Relation", "Note"], rows))
    else:
        lines.append("No scientific references are listed in this specification.")

    inputs = normative.get("inputs", []) if isinstance(normative, dict) else []
    lines.extend(["", "## Inputs", ""])
    lines.extend(
        table(
            ["id", "data_type", "shape", "unit", "allow_nan", "allow_inf", "constraints"],
            [
                [
                    inline_code(entry.get("id", "")),
                    entry.get("data_type", ""),
                    entry.get("shape", ""),
                    entry.get("unit", ""),
                    json_scalar(entry.get("allow_nan")),
                    json_scalar(entry.get("allow_inf")),
                    format_constraints(entry.get("constraints")),
                ]
                for entry in inputs
                if isinstance(entry, dict)
            ],
        )
    )

    parameters = normative.get("parameters", []) if isinstance(normative, dict) else []
    lines.extend(["", "## Parameters", ""])
    parameter_rows = [
        [
            inline_code(entry.get("id", "")),
            entry.get("data_type", ""),
            format_default(entry.get("default")),
            entry.get("unit", ""),
            format_constraints(entry.get("constraints")),
        ]
        for entry in parameters
        if isinstance(entry, dict)
    ]
    if parameter_rows:
        lines.extend(table(["id", "data_type", "default", "unit", "constraints"], parameter_rows))
    else:
        lines.append("No parameters.")

    outputs = normative.get("outputs", []) if isinstance(normative, dict) else []
    lines.extend(["", "## Outputs", ""])
    lines.extend(
        table(
            ["id", "data_type", "shape", "unit"],
            [
                [
                    inline_code(entry.get("id", "")),
                    entry.get("data_type", ""),
                    entry.get("shape", ""),
                    entry.get("unit", ""),
                ]
                for entry in outputs
                if isinstance(entry, dict)
            ],
        )
    )

    definitions = normative.get("definitions", []) if isinstance(normative, dict) else []
    lines.extend(["", "## Normative Definitions", ""])
    definition_rows = []
    for definition in definitions:
        if not isinstance(definition, dict):
            continue
        definition_rows.append(
            [
                inline_code(definition.get("target", "")),
                definition.get("text", ""),
                definition.get("latex", ""),
            ]
        )
    if definition_rows:
        lines.extend(table(["Target", "Definition", "Formula"], definition_rows))
    else:
        lines.append("No normative definitions are listed in this specification.")

    behavior = normative.get("behavior", {}) if isinstance(normative, dict) else {}
    lines.extend(["", "## Behavior", ""])
    if isinstance(behavior, dict) and behavior:
        for key in ordered_behavior_keys(behavior):
            lines.extend([f"### {title_for_key(key)}", "", str(behavior[key]), ""])
        lines.pop()
    else:
        lines.append("No behavior notes are listed in this specification.")

    notes = informative.get("notes", []) if isinstance(informative, dict) else []
    if notes:
        lines.extend(["", "## Informative Notes", ""])
        for note in notes:
            lines.append(f"* {note}")

    lines.extend(["", "## Conformance Cases", ""])
    cases = conformance_cases(root, module, algorithm)
    if cases:
        rows = []
        for case_path, case_id in cases:
            display = relative_path(case_path, root)
            rows.append(
                [
                    inline_code(case_id),
                    f"[{display}]({github_blob_url(root, case_path)})",
                ]
            )
        lines.extend(table(["Case ID", "File"], rows))
    else:
        lines.append(f"No conformance cases were found under `conformance/{module}/{algorithm}/`.")

    return "\n".join(lines).rstrip() + "\n"


def generated_pages(root: Path) -> dict[Path, str]:
    pages = {}
    for spec_path, spec in discover_specs(root):
        metadata = spec.get("metadata", {})
        if not isinstance(metadata, dict) or not isinstance(metadata.get("id"), str):
            raise ValueError(f"{relative_path(spec_path, root)} is missing metadata.id")
        output_path = root / GENERATED_SPEC_DIR / f"{metadata['id']}.md"
        pages[output_path] = render_spec_page(root, spec_path, spec)
    return pages


def check_generated(root: Path, pages: dict[Path, str]) -> int:
    expected_paths = set(pages)
    existing_paths = set((root / GENERATED_SPEC_DIR).glob("*.md"))
    stale_paths = sorted(expected_paths | existing_paths)

    failures = []
    for path in stale_paths:
        expected = pages.get(path)
        if expected is None:
            failures.append(f"stale generated file: {relative_path(path, root)}")
            continue
        if not path.exists():
            failures.append(f"missing generated file: {relative_path(path, root)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            failures.append(f"outdated generated file: {relative_path(path, root)}")

    if failures:
        print("Generated documentation is stale. Run `python tools/generate_docs.py`.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Generated documentation is up to date.")
    return 0


def write_generated(root: Path, pages: dict[Path, str]) -> int:
    output_dir = root / GENERATED_SPEC_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    expected_paths = set(pages)
    for path, content in sorted(pages.items()):
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"Wrote {relative_path(path, root)}")

    for path in sorted(output_dir.glob("*.md")):
        if path not in expected_paths:
            path.unlink()
            print(f"Removed stale {relative_path(path, root)}")

    return 0


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate MkDocs pages from Biosiglib JSON specifications.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that generated documentation is present and up to date.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    root = find_repository_root()

    try:
        pages = generated_pages(root)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Documentation generation failed: {exc}", file=sys.stderr)
        return 1

    if args.check:
        return check_generated(root, pages)
    return write_generated(root, pages)


if __name__ == "__main__":
    sys.exit(main())
