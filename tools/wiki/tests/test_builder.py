"""Testes do builder e idempotência (builder.py, catalog.py, validate.py)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from novadyne_wiki import builder
from novadyne_wiki.catalog import CatalogBuilder, write_catalog
from novadyne_wiki.reporter import Reporter
from novadyne_wiki.validate import validate_docs_links


class BuilderTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.content_dir = self.tmp / "content"
        self.docs_dir = self.tmp / "docs"
        self.theme_dir = self.tmp / "theme"
        self.custom = self.tmp / "mkdocs.custom.yml"
        self.config_path = self.tmp / "mkdocs.yml"
        self.theme_dir.mkdir(parents=True)
        (self.theme_dir / "css").mkdir()
        (self.theme_dir / "css" / "novadyne.css").write_text(":root {}", encoding="utf-8")
        (self.content_dir).mkdir(parents=True)
        (self.content_dir / "index.md").write_text(
            "---\ntitle: NovaDyne\norder: 0\n---\n# Home\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self._tmp.cleanup()

    def _build(self, reporter=None, clean=False):
        return builder.build_site(
            reporter or Reporter(),
            content_dir=self.content_dir,
            docs_dir=self.docs_dir,
            theme_dir=self.theme_dir,
            custom_config=self.custom,
            config_path=self.config_path,
            clean=clean,
        )

    def test_build_site_assembles_docs(self):
        self._build()
        self.assertTrue((self.docs_dir / "index.md").exists())
        body = (self.docs_dir / "index.md").read_text(encoding="utf-8")
        self.assertNotIn("---", body)
        self.assertIn("# Home", body)
        self.assertTrue((self.docs_dir / "assets" / "css" / "novadyne.css").exists())
        self.assertTrue(self.config_path.exists())
        config_text = self.config_path.read_text(encoding="utf-8")
        self.assertIn("Home", config_text)

    def test_build_site_removes_stale_files(self):
        self._build()
        stale = self.docs_dir / "stale.md"
        stale.write_text("velho", encoding="utf-8")
        self._build()
        self.assertFalse(stale.exists())

    def test_generation_is_idempotent(self):
        first = self._build()
        second = self._build()
        self.assertEqual(first, second)

    def test_build_site_reports_broken_link(self):
        (self.content_dir / "index.md").write_text(
            "---\ntitle: NovaDyne\n---\n# Home\n\n[quebrado](nao-existe.md)\n",
            encoding="utf-8",
        )
        reporter = Reporter()
        self._build(reporter)
        self.assertEqual(len(reporter.warnings), 1)
        self.assertIn("nao-existe.md", reporter.warnings[0].message)

    def test_validate_docs_links_ok(self):
        (self.docs_dir).mkdir(parents=True, exist_ok=True)
        (self.docs_dir / "a.md").write_text("[ok](b.md)\n", encoding="utf-8")
        (self.docs_dir / "b.md").write_text("b\n", encoding="utf-8")
        reporter = Reporter()
        validate_docs_links(self.docs_dir, reporter)
        self.assertEqual(reporter.warnings, [])


class CatalogBuilderTests(unittest.TestCase):
    def test_build_returns_schema(self):
        catalog = CatalogBuilder(Reporter()).build()
        self.assertEqual(catalog["schema"], 1)
        self.assertEqual(catalog["entries"], [])
        self.assertEqual(catalog["recipes"], [])

    def test_write_catalog_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            write_catalog({"a": [1, 2], "b": "x"}, path)
            write_catalog({"a": [1, 2], "b": "x"}, path)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data, {"a": [1, 2], "b": "x"})


if __name__ == "__main__":
    unittest.main()
