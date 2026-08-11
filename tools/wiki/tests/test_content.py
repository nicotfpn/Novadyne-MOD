"""Testes de carregamento de conteúdo manual (content.py)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from novadyne_wiki import content
from novadyne_wiki.errors import WikiError


class ContentTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, rel: str, text: str) -> Path:
        path = self.tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_load_manual_pages_with_front_matter(self):
        self._write(
            "index.md",
            "---\ntitle: NovaDyne\nnav_title: Home\norder: 0\n---\n\n# Título\n",
        )
        pages = content.load_manual_pages(self.tmp)
        self.assertEqual(len(pages), 1)
        page = pages[0]
        self.assertEqual(page.title, "NovaDyne")
        self.assertEqual(page.nav_title, "Home")
        self.assertEqual(page.order, 0)
        self.assertEqual(page.body, "# Título")

    def test_load_manual_pages_without_front_matter(self):
        self._write("pagina.md", "sem front matter\n")
        pages = content.load_manual_pages(self.tmp)
        self.assertEqual(len(pages), 1)
        self.assertTrue(pages[0].title.endswith("Pagina"))

    def test_invalid_front_matter_raises(self):
        self._write("bad.md", "---\n: inválido\n---\ncorpo\n")
        with self.assertRaises(WikiError):
            content.load_manual_pages(self.tmp)

    def test_load_entry_description(self):
        self._write(
            "entries/pure_silicon.md",
            "---\nid: novadyne:pure_silicon\ntitle: Pure Silicon\n---\n\ndescrição manual\n",
        )
        page = content.load_entry_description(self.tmp, "novadyne:pure_silicon")
        self.assertIsNotNone(page)
        self.assertEqual(page.body, "descrição manual")
        self.assertIsNone(content.load_entry_description(self.tmp, "novadyne:missing"))

    def test_empty_dir(self):
        self.assertEqual(content.load_manual_pages(self.tmp), [])

    def test_entries_subdir_not_loaded_as_manual_page(self):
        self._write("index.md", "---\ntitle: NovaDyne\norder: 0\n---\n# Home\n")
        self._write(
            "entries/pure_silicon.md",
            "---\nid: novadyne:pure_silicon\ntitle: Pure Silicon\n---\ndescrição\n",
        )
        pages = content.load_manual_pages(self.tmp)
        self.assertEqual([p.dest_rel for p in pages], ["index.md"])


if __name__ == "__main__":
    unittest.main()
