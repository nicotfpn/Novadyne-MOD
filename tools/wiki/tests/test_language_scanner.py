"""Testes do LanguageScanner e resolução de nomes (Fase 3).

Cobre os casos 5 (pt_br preferido), 6 (fallback en_us), 7 (tradução
ausente) e 27 (Unicode preservado).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from novadyne_wiki.reporter import Reporter

from .support import ModFixture


class LanguageScannerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.fixture = ModFixture(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def _scan_languages(self):
        from novadyne_wiki.scanners.language_scanner import LanguageScanner

        scan = LanguageScanner(
            assets_root=self.fixture.assets,
            project_root=self.fixture.root,
            mod_id=self.fixture.mod_id,
        ).scan()
        return scan.data["index"]

    def test_pt_br_preferred_over_en_us(self):
        self.fixture.add_lang("item.novadyne.coisa", "Thing", locale="en_us")
        self.fixture.add_lang("item.novadyne.coisa", "Coisa", locale="pt_br")
        index = self._scan_languages()
        self.assertEqual(index.resolve("item.novadyne.coisa"), "Coisa")
        self.assertEqual(
            index.values_for("item.novadyne.coisa"),
            {"en_us": "Thing", "pt_br": "Coisa"},
        )

    def test_en_us_fallback(self):
        self.fixture.add_simple_item("pure_silicon", "Pure Silicon")
        catalog, _ = self.fixture.run_catalog()
        entry = next(e for e in catalog["entries"] if e["path"] == "pure_silicon")
        self.assertEqual(entry["display_name"], "Pure Silicon")
        self.assertEqual(entry["translations"], {"en_us": "Pure Silicon"})

    def test_missing_translation_is_warning(self):
        self.fixture.add_simple_item("orphan_item")
        (self.fixture.assets / self.fixture.mod_id / "lang" / "en_us.json").unlink()
        reporter = Reporter()
        catalog, _ = self.fixture.run_catalog(reporter)
        entry = next(e for e in catalog["entries"] if e["path"] == "orphan_item")
        self.assertIsNone(entry.get("display_name"))
        self.assertEqual(entry.get("translations"), {})
        self.assertTrue(
            any("tradução ausente" in w for w in entry.get("warnings", [])),
            entry.get("warnings"),
        )
        self.assertTrue(
            any("tradução ausente" in w.message for w in reporter.warnings)
        )

    def test_unicode_preserved(self):
        self.fixture.add_simple_item("maquina", "Máquina — ünïcödé")
        catalog, _ = self.fixture.run_catalog()
        from novadyne_wiki.catalog import write_catalog

        target = self.tmp / "catalog.json"
        write_catalog(catalog, target)
        raw = target.read_text(encoding="utf-8")
        self.assertIn("Máquina — ünïcödé", raw)

    def test_locales_listed(self):
        self.fixture.add_lang("a", "A", locale="en_us")
        self.fixture.add_lang("a", "A", locale="pt_br")
        catalog, _ = self.fixture.run_catalog()
        self.assertEqual(catalog["generation"]["languages"], ["en_us", "pt_br"])


if __name__ == "__main__":
    unittest.main()
