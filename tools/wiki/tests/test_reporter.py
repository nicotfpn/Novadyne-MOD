"""Testes do relatório (reporter.py)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from novadyne_wiki import reporter


class ReporterTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_ok_without_issues(self):
        self.assertTrue(reporter.Reporter().ok)

    def test_warning_ok_in_normal_mode(self):
        rep = reporter.Reporter()
        rep.warning("algo")
        self.assertTrue(rep.ok)

    def test_warning_fails_in_strict_mode(self):
        rep = reporter.Reporter(strict=True)
        rep.warning("algo")
        self.assertFalse(rep.ok)

    def test_error_always_fails(self):
        rep = reporter.Reporter()
        rep.error("fatal")
        self.assertFalse(rep.ok)

    def test_acknowledged_warning_does_not_fail_strict(self):
        """Aviso reconhecido não derruba --strict."""
        rep = reporter.Reporter(strict=True, acknowledged=["textura planejada"])
        rep.warning("textura planejada")
        self.assertTrue(rep.ok)

    def test_unacknowledged_warning_still_fails_strict(self):
        """Aviso NÃO reconhecido continua derrubando --strict."""
        rep = reporter.Reporter(strict=True, acknowledged=["textura planejada"])
        rep.warning("textura planejada")
        rep.warning("outro aviso qualquer")
        self.assertFalse(rep.ok)

    def test_write_report(self):
        rep = reporter.Reporter(strict=False)
        rep.warning("textura ausente", path="assets/x.png")
        rep.error("arquivo inválido", path="bad.json")
        rep.note_missing_texture("novadyne:x")
        rep.write_report(self.tmp)
        self.assertTrue((self.tmp / "report.json").exists())
        self.assertTrue((self.tmp / "report.md").exists())
        data = json.loads((self.tmp / "report.json").read_text(encoding="utf-8"))
        self.assertFalse(data["ok"])
        self.assertEqual(data["summary"]["warnings"], 1)
        self.assertEqual(data["summary"]["errors"], 1)
        self.assertIn("novadyne:x", data["stats"]["missing_textures"])


if __name__ == "__main__":
    unittest.main()
