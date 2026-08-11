"""Tests for generated specification documentation and navigation."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "tools"))

import generate_docs  # noqa: E402


class GeneratedSpecificationIndexTests(unittest.TestCase):
    def test_renders_index_and_navigation_from_specification_metadata(self) -> None:
        specs = [
            (
                Path("specs/ecg/example/spec.json"),
                {
                    "metadata": {"id": "ecg.example", "module": "ecg"},
                    "informative": {"summary": "Example ECG algorithm."},
                },
            ),
            (
                Path("specs/tools/helper/spec.json"),
                {
                    "metadata": {"id": "tools.helper", "module": "tools"},
                    "informative": {"summary": "Example helper."},
                },
            ),
        ]

        index = "\n".join(generate_docs.specification_index_lines(specs))
        navigation = "\n".join(generate_docs.specification_navigation_lines(specs))

        self.assertIn(
            "| [`ecg.example`](generated/specifications/ecg.example.md) | ECG | "
            "Example ECG algorithm. |",
            index,
        )
        self.assertIn(
            "| [`tools.helper`](generated/specifications/tools.helper.md) | Tools | "
            "Example helper. |",
            index,
        )
        self.assertEqual(
            navigation,
            "      - ecg.example: generated/specifications/ecg.example.md\n"
            "      - tools.helper: generated/specifications/tools.helper.md",
        )

    def test_replaces_only_the_delimited_generated_block(self) -> None:
        updated = generate_docs.replace_generated_block(
            "before\nSTART\nold\nEND\nafter\n",
            "START",
            "END",
            ["new", "content"],
            "example.md",
        )

        self.assertEqual(updated, "before\nSTART\nnew\ncontent\nEND\nafter\n")

    def test_repository_generated_documentation_is_current(self) -> None:
        generated = generate_docs.generated_documentation(REPOSITORY_ROOT)

        for path, expected in generated.items():
            with self.subTest(path=path):
                self.assertEqual(path.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
