"""Tests for build-time method documentation rendering."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "tools"))

import generate_docs  # noqa: E402


class MethodDocumentationRenderingTests(unittest.TestCase):
    def test_renders_practical_interface_from_contract_and_descriptions(self) -> None:
        rendered = generate_docs.render_method_interface("hrv.tdmetrics")

        self.assertIn("**Canonical ID:** `hrv.tdmetrics`", rendered)
        self.assertIn("| `dtk` |", rendered)
        self.assertIn("Clean beat-to-beat or pulse-to-pulse intervals", rendered)
        self.assertIn("| `mhr` |", rendered)

    def test_renders_references_and_technical_links_without_case_tables(self) -> None:
        rendered = generate_docs.render_method_resources("ecg.pantompkins")

        self.assertIn("## References", rendered)
        self.assertIn("Python source", rendered)
        self.assertIn("MATLAB source", rendered)
        self.assertIn("Normative JSON", rendered)
        self.assertIn("Validation cases", rendered)
        self.assertNotIn("Expected outputs", rendered)

    def test_renders_complete_method_catalog(self) -> None:
        rendered = generate_docs.render_method_catalog()
        specification_ids = generate_docs.repository_data()[0]

        for specification_id in specification_ids:
            with self.subTest(specification_id=specification_id):
                self.assertIn(f"({specification_id}.md)", rendered)

    def test_hook_replaces_markers_without_changing_source_file(self) -> None:
        source_path = REPOSITORY_ROOT / "docs" / "methods" / "hrv.tdmetrics.md"
        source = source_path.read_text(encoding="utf-8")
        page = SimpleNamespace(file=SimpleNamespace(src_uri="methods/hrv.tdmetrics.md"))

        rendered = generate_docs.on_page_markdown(source, page)

        self.assertNotIn(generate_docs.METHOD_INTERFACE_MARKER, rendered)
        self.assertNotIn(generate_docs.METHOD_RESOURCES_MARKER, rendered)
        self.assertEqual(source_path.read_text(encoding="utf-8"), source)


if __name__ == "__main__":
    unittest.main()
