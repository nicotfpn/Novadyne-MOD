"""Testes da configuração do MkDocs (config.py)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from novadyne_wiki import config
from novadyne_wiki.content import ManualPage


def _page(dest_rel: str, title: str, *, nav_title=None, order=100) -> ManualPage:
    return ManualPage(
        source=Path("/fake") / dest_rel,
        dest_rel=dest_rel,
        title=title,
        nav_title=nav_title,
        order=order,
    )


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_deep_merge(self):
        base = {"a": 1, "b": {"x": 1, "y": 2}, "c": [1, 2]}
        override = {"b": {"y": 99, "z": 3}, "c": [9]}
        merged = config.deep_merge(base, override)
        self.assertEqual(merged["a"], 1)
        self.assertEqual(merged["b"], {"x": 1, "y": 99, "z": 3})
        self.assertEqual(merged["c"], [9])
        self.assertEqual(base["b"], {"x": 1, "y": 2})

    def test_load_custom_config_missing(self):
        self.assertEqual(config.load_custom_config(self.tmp / "nope.yml"), {})

    def test_load_custom_config_invalid(self):
        path = self.tmp / "bad.yml"
        path.write_text(": inválido\n", encoding="utf-8")
        from novadyne_wiki.errors import WikiError

        with self.assertRaises(WikiError):
            config.load_custom_config(path)

    def test_build_nav_home_first(self):
        nav = config.build_nav([_page("guia.md", "Guia"), _page("index.md", "Início")])
        self.assertEqual(nav[0], {"Home": "index.md"})

    def test_build_nav_sections(self):
        pages = [
            _page("desenvolvimento/atualizar.md", "Atualizar", order=10),
            _page("desenvolvimento/arquitetura.md", "Arquitetura", order=20),
            _page("index.md", "Início", order=0),
        ]
        nav = config.build_nav(pages)
        self.assertEqual(nav[1], {"Desenvolvimento": [
            {"Atualizar": "desenvolvimento/atualizar.md"},
            {"Arquitetura": "desenvolvimento/arquitetura.md"},
        ]})

    def test_build_nav_stable_order(self):
        pages = [
            _page("b.md", "B"),
            _page("a.md", "A"),
            _page("c.md", "C"),
        ]
        nav = config.build_nav(pages)
        self.assertEqual([list(item)[0] for item in nav], ["A", "B", "C"])

    def test_assemble_config_includes_base_and_nav(self):
        cfg = config.assemble_config([{"Home": "index.md"}], custom_path=self.tmp / "nope.yml")
        self.assertEqual(cfg["site_name"], "NovaDyne")
        self.assertEqual(cfg["nav"], [{"Home": "index.md"}])
        self.assertIn("assets/css/novadyne.css", cfg["extra_css"])

    def test_write_mkdocs_config_roundtrip(self):
        target = self.tmp / "mkdocs.yml"
        config.write_mkdocs_config(target, config.assemble_config([], custom_path=self.tmp / "nope.yml"))
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
        self.assertEqual(data["docs_dir"], "docs")
        self.assertEqual(data["nav"], [])


if __name__ == "__main__":
    unittest.main()
