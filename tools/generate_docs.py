"""Render user-facing method data during the MkDocs build."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_URL = "https://github.com/BSICoS/biosiglib"
METHOD_INTERFACE_MARKER = "<!-- BIOSIGLIB METHOD INTERFACE -->"
METHOD_RESOURCES_MARKER = "<!-- BIOSIGLIB METHOD RESOURCES -->"
METHOD_CATALOG_MARKER = "<!-- BIOSIGLIB METHOD CATALOG -->"
DESCRIPTION_PATH = REPOSITORY_ROOT / "docs" / "methods" / "descriptions.json"
MATLAB_NAMES = {
    "tools.lpd_filter": "lpdfilter",
    "tools.medfilt_threshold": "medfiltThreshold",
    "tools.nan_filter": "nanfilter",
    "tools.nan_filtfilt": "nanfiltfilt",
    "tools.snap_to_peak": "snaptopeak",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def repository_data() -> tuple[
    dict[str, tuple[Path, dict[str, Any]]],
    dict[str, Any],
    dict[str, Any],
]:
    specs: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted((REPOSITORY_ROOT / "specs").rglob("spec.json")):
        spec = load_json(path)
        specification_id = spec["metadata"]["id"]
        specs[specification_id] = (path, spec)

    references = {
        reference["id"]: reference
        for reference in load_json(REPOSITORY_ROOT / "references" / "references.json")["references"]
    }
    descriptions = load_json(DESCRIPTION_PATH)
    return specs, references, descriptions


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend(
        "| " + " | ".join(markdown_escape(cell) for cell in row) + " |"
        for row in rows
    )
    return "\n".join(lines)


def format_value(value: Any) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if value is None:
        return "not applicable"
    if isinstance(value, (list, dict)):
        return f"`{json.dumps(value, sort_keys=True)}`"
    return f"`{value}`"


def format_requirements(entry: dict[str, Any]) -> str:
    parts = []
    constraints = entry.get("constraints", {})
    labels = {
        "minimum": "minimum",
        "exclusive_minimum": "greater than",
        "maximum": "maximum",
        "exclusive_maximum": "less than",
        "minimum_length": "minimum length",
    }
    for key, value in constraints.items():
        parts.append(f"{labels.get(key, key.replace('_', ' '))}: {value}")
    if entry.get("allow_nan") is True:
        parts.append("NaN allowed")
    elif entry.get("allow_nan") is False:
        parts.append("no NaN")
    if entry.get("allow_inf") is True:
        parts.append("Inf allowed")
    elif entry.get("allow_inf") is False:
        parts.append("finite")
    return "; ".join(parts) or "not specified"


def field_rows(
    specification_id: str,
    entries: list[dict[str, Any]],
    *,
    include_default: bool = False,
    include_requirements: bool = True,
) -> list[list[object]]:
    _, _, descriptions = repository_data()
    field_descriptions = descriptions[specification_id]
    rows = []
    for entry in entries:
        row: list[object] = [
            f"`{entry['id']}`",
            field_descriptions[entry["id"]],
            entry.get("data_type", "").replace("_", " "),
            entry.get("unit", "dimensionless"),
        ]
        if include_default:
            row.append(format_value(entry.get("default")))
        if include_requirements:
            row.append(format_requirements(entry))
        rows.append(row)
    return rows


def format_authors(reference: dict[str, Any]) -> str:
    names = []
    for author in reference.get("authors", []):
        if author.get("type") == "organization":
            names.append(author["name"])
        else:
            names.append(
                " ".join(
                    part
                    for part in (author.get("given_names", ""), author.get("family_name", ""))
                    if part
                )
            )
    if len(names) > 3:
        return f"{names[0]} et al."
    if len(names) == 2:
        return " and ".join(names)
    return ", ".join(names)


def format_reference(reference: dict[str, Any]) -> str:
    authors = format_authors(reference)
    year = reference.get("year", "")
    title = reference.get("title", "")
    journal = reference.get("journal")
    citation = f"{authors} ({year}). *{title}*."
    if journal:
        citation += f" {journal}."
    if doi := reference.get("doi"):
        citation += f" [doi:{doi}](https://doi.org/{doi})"
    elif pmid := reference.get("pmid"):
        citation += f" [PMID:{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)"
    return citation


def code_links(specification_id: str, module: str, algorithm: str) -> str:
    matlab_name = MATLAB_NAMES.get(specification_id, algorithm)
    python_path = f"src/biosigpy/{module}/{algorithm}.py"
    matlab_path = f"src/{module}/{matlab_name}.m"
    return (
        f"[Python source](https://github.com/BSICoS/biosigpy/blob/main/{python_path}) | "
        f"[MATLAB source](https://github.com/BSICoS/biosigmat/blob/main/{matlab_path})"
    )


def render_method_interface(specification_id: str) -> str:
    specs, _, _ = repository_data()
    _, spec = specs[specification_id]
    normative = spec["normative"]
    sections = [
        f"**Canonical ID:** `{specification_id}`",
        "",
        "## Inputs",
        "",
        table(
            ["Name", "Meaning", "Type", "Unit", "Requirements"],
            field_rows(specification_id, normative["inputs"]),
        ),
    ]

    parameters = normative.get("parameters", [])
    if parameters:
        sections.extend(
            [
                "",
                "## Parameters",
                "",
                table(
                    ["Name", "Meaning", "Type", "Unit", "Default", "Requirements"],
                    field_rows(specification_id, parameters, include_default=True),
                ),
            ]
        )

    sections.extend(
        [
            "",
            "## Outputs",
            "",
            table(
                ["Name", "Meaning", "Type", "Unit"],
                field_rows(
                    specification_id,
                    normative["outputs"],
                    include_requirements=False,
                ),
            ),
        ]
    )

    return "\n".join(sections)


def render_method_resources(specification_id: str) -> str:
    specs, references, _ = repository_data()
    spec_path, spec = specs[specification_id]
    metadata = spec["metadata"]
    module = metadata["module"]
    algorithm = spec_path.parent.name
    relative_spec_path = spec_path.relative_to(REPOSITORY_ROOT).as_posix()
    case_path = f"conformance/{module}/{algorithm}"

    sections = []
    reference_ids = []
    for relationship in spec.get("provenance", {}).get("references", []):
        reference_id = relationship["id"]
        if reference_id not in reference_ids:
            reference_ids.append(reference_id)
    if reference_ids:
        sections.extend(["## References", ""])
        sections.extend(
            f"- {format_reference(references[reference_id])}"
            for reference_id in reference_ids
        )
        sections.append("")

    sections.extend(
        [
            "## Implementations and technical resources",
            "",
            code_links(specification_id, module, algorithm),
            "",
            f"[Normative JSON]({REPOSITORY_URL}/blob/main/{relative_spec_path}) | "
            f"[Validation cases]({REPOSITORY_URL}/tree/main/{case_path})",
        ]
    )
    return "\n".join(sections)


def render_method_catalog() -> str:
    specs, _, _ = repository_data()
    rows = []
    for specification_id, (_, spec) in sorted(specs.items()):
        rows.append(
            [
                f"[{spec['informative']['title']}]({specification_id}.md)",
                spec["metadata"]["module"].upper(),
                spec["informative"]["summary"],
            ]
        )
    return table(["Method", "Area", "What it does"], rows)


def replace_marker(markdown: str, marker: str, rendered: str) -> str:
    if markdown.count(marker) != 1:
        raise ValueError(f"Expected exactly one {marker!r} marker")
    return markdown.replace(marker, rendered)


def on_page_markdown(markdown: str, page: Any, **_: Any) -> str:
    """MkDocs hook: inject generated data without changing source Markdown."""

    source_uri = page.file.src_uri.replace("\\", "/")
    if source_uri == "methods/index.md":
        return replace_marker(markdown, METHOD_CATALOG_MARKER, render_method_catalog())
    if source_uri.startswith("methods/") and source_uri.endswith(".md"):
        specification_id = Path(source_uri).stem
        if specification_id in repository_data()[0]:
            rendered = replace_marker(
                markdown,
                METHOD_INTERFACE_MARKER,
                render_method_interface(specification_id),
            )
            return replace_marker(
                rendered,
                METHOD_RESOURCES_MARKER,
                render_method_resources(specification_id),
            )
    return markdown
