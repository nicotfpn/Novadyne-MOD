"""Testes do layout de pastas (paths.py)."""

from __future__ import annotations

import unittest

from novadyne_wiki import paths


class PathsTests(unittest.TestCase):
    def test_all_paths_inside_project_root(self):
        self.assertTrue((paths.PROJECT_ROOT / "src").exists())
        for name in (
            "MAIN_JAVA",
            "MAIN_RESOURCES",
            "ASSETS_DIR",
            "DATA_DIR",
            "BUILD_WIKI",
            "WIKI_DIR",
            "WIKI_CONTENT",
            "WIKI_GENERATED",
            "WIKI_DOCS",
            "WIKI_THEME",
            "WIKI_CONFIG",
            "WIKI_CUSTOM_CONFIG",
        ):
            with self.subTest(name=name):
                value = getattr(paths, name)
                value.resolve().relative_to(paths.PROJECT_ROOT.resolve())

    def test_disposable_dirs_are_inside_project_root(self):
        for directory in paths.DISPOSABLE_DIRS:
            directory.resolve().relative_to(paths.PROJECT_ROOT.resolve())

    def test_disposable_dirs_include_build_wiki(self):
        self.assertIn(paths.BUILD_WIKI, paths.DISPOSABLE_DIRS)

    def test_generated_banner(self):
        self.assertTrue(paths.GENERATED_BANNER.startswith("<!-- AUTO-GENERATED"))


if __name__ == "__main__":
    unittest.main()
