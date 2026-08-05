"""Testes de I/O seguro (io_utils.py)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from novadyne_wiki import io_utils
from novadyne_wiki.errors import WikiError


class IoUtilsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_write_text_atomic_roundtrip_unicode(self):
        target = self.tmp / "sub" / "x.md"
        io_utils.write_text_atomic(target, "olá — conteúdo\n")
        self.assertEqual(io_utils.read_text(target), "olá — conteúdo\n")

    def test_write_text_atomic_normalizes_newlines(self):
        target = self.tmp / "x.md"
        io_utils.write_text_atomic(target, "a\r\nb\n")
        self.assertEqual(io_utils.read_text(target), "a\nb\n")

    def test_write_bytes_atomic(self):
        target = self.tmp / "img.png"
        io_utils.write_bytes_atomic(target, b"\x89PNG\r\n")
        self.assertEqual(target.read_bytes(), b"\x89PNG\r\n")

    def test_ensure_inside_root_ok(self):
        inside = self.tmp / "a" / "b.txt"
        inside.parent.mkdir(parents=True)
        inside.write_text("x", encoding="utf-8")
        self.assertEqual(io_utils.ensure_inside_root(inside, self.tmp), inside.resolve())

    def test_ensure_inside_root_rejects_escape(self):
        outside = self.tmp.parent / "escape.txt"
        outside.write_text("x", encoding="utf-8")
        with self.assertRaises(WikiError):
            io_utils.ensure_inside_root(outside, self.tmp)

    def test_safe_relative(self):
        root_a = self.tmp / "a"
        root_b = self.tmp / "b"
        root_a.mkdir()
        root_b.mkdir()
        file = root_b / "x" / "y.png"
        file.parent.mkdir(parents=True)
        file.write_bytes(b"x")
        self.assertEqual(io_utils.safe_relative(file, (root_a, root_b)), "x/y.png")

    def test_safe_relative_rejects_outside(self):
        with self.assertRaises(WikiError):
            io_utils.safe_relative(self.tmp / "nope.txt", (self.tmp / "a",))

    def test_slugify(self):
        self.assertEqual(io_utils.slugify("Hello, World!"), "hello-world")
        self.assertEqual(io_utils.slugify("  Led  "), "led")
        self.assertEqual(io_utils.slugify("café"), "caf")

    def test_iter_files_stable_order(self):
        for name in ("b.txt", "a.txt", "c.txt"):
            (self.tmp / name).write_text("x", encoding="utf-8")
        result = io_utils.iter_files(self.tmp, suffixes=(".txt",))
        self.assertEqual([p.name for p in result], ["a.txt", "b.txt", "c.txt"])

    def test_file_digest_stable(self):
        path = self.tmp / "f.txt"
        path.write_text("conteúdo", encoding="utf-8")
        self.assertEqual(io_utils.file_digest(path), io_utils.file_digest(path))

    def test_wipe_dir_refuses_non_disposable(self):
        with self.assertRaises(WikiError):
            io_utils.wipe_dir(self.tmp)

    def test_wipe_dir_with_extra_allowed(self):
        target = self.tmp / "sub"
        target.mkdir()
        (target / "keep.txt").write_text("x", encoding="utf-8")
        (target / "nested").mkdir()
        (target / "nested" / "y.txt").write_text("y", encoding="utf-8")
        io_utils.wipe_dir(target, extra_allowed=(target,))
        self.assertTrue(target.exists())
        self.assertEqual(list(target.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
