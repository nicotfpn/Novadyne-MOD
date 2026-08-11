"""Testes do TagScanner (Fase 3).

Cobre os casos 19 (tag referenciando outra tag) e 20 (ciclo de tags).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from .support import ModFixture


class TagScannerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.fixture = ModFixture(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def _scan_tags(self):
        from novadyne_wiki.scanners.tag_scanner import TagScanner

        return TagScanner(
            data_root=self.fixture.data,
            project_root=self.fixture.root,
        ).scan()

    def test_tag_references_another_tag(self):
        self.fixture.write_data_json(
            "c/tags/item/gems/quartz.json",
            {"replace": False, "values": ["minecraft:quartz"]},
        )
        self.fixture.write_data_json(
            "c/tags/item/dusts/silicon.json",
            {"replace": False, "values": ["novadyne:pure_silicon", "#c:gems/quartz"]},
        )
        result = self._scan_tags()
        tags = {t["id"]: t for t in result.data["tags"]}
        self.assertEqual(tags["c:gems/quartz"]["tag_refs"], [])
        silicon = tags["c:dusts/silicon"]
        self.assertEqual(silicon["tag_refs"], ["c:gems/quartz"])
        self.assertEqual(
            silicon["values_resolved"],
            ["minecraft:quartz", "novadyne:pure_silicon"],
        )
        self.assertEqual(silicon["missing_refs"], [])

    def test_tag_cycle_detected(self):
        self.fixture.write_data_json(
            "novadyne/tags/item/a.json",
            {"values": ["novadyne:coisa", "#novadyne:b"]},
        )
        self.fixture.write_data_json(
            "novadyne/tags/item/b.json",
            {"values": ["#novadyne:a"]},
        )
        result = self._scan_tags()
        tags = {t["id"]: t for t in result.data["tags"]}
        self.assertTrue(tags["novadyne:a"]["cycle"])
        self.assertTrue(tags["novadyne:b"]["cycle"])
        self.assertEqual(result.data["cycles"], [("novadyne:a", "novadyne:b", "novadyne:a")])
        messages = [d.message for d in result.diagnostics]
        self.assertTrue(any("ciclo de tags" in m for m in messages), messages)

    def test_tag_values_resolved_no_cycles(self):
        self.fixture.write_data_json(
            "novadyne/tags/item/pequeno.json",
            {"values": ["novadyne:coisa"]},
        )
        result = self._scan_tags()
        tag = result.data["tags"][0]
        self.assertEqual(tag["values_resolved"], ["novadyne:coisa"])


if __name__ == "__main__":
    unittest.main()
