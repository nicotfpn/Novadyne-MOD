"""Testes de ModelScanner/AssetScanner e verificação de assets (Fase 3).

Cobre os casos 8 (modelo de item), 9 (modelo de bloco), 10 (referência de
textura), 11 (textura ausente) e 12 (modelo ausente).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from novadyne_wiki.reporter import Reporter

from .support import ModFixture


class ModelAssetTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.fixture = ModFixture(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def _scan_models(self):
        from novadyne_wiki.scanners.model_scanner import ModelScanner

        return ModelScanner(
            assets_root=self.fixture.assets,
            project_root=self.fixture.root,
            mod_id=self.fixture.mod_id,
        ).scan()

    def test_item_model(self):
        self.fixture.write_asset_json(
            "models/item/coisa.json",
            {"parent": "minecraft:item/generated", "textures": {"layer0": "novadyne:item/coisa"}},
        )
        result = self._scan_models()
        record = result.data["models"]["novadyne:item/coisa"]
        self.assertEqual(record["parent"], "minecraft:item/generated")
        self.assertEqual(record["textures"], {"layer0": "novadyne:item/coisa"})
        self.assertIn("novadyne:item/coisa", record["texture_refs"])

    def test_block_model(self):
        self.fixture.write_asset_json(
            "models/block/macerator.json",
            {
                "parent": "minecraft:block/orientable",
                "textures": {
                    "front": "novadyne:block/macerator_front",
                    "side": "novadyne:block/machine_side",
                    "top": "novadyne:block/machine_top",
                },
            },
        )
        self.fixture.write_png("textures/block/macerator_front.png")
        self.fixture.write_png("textures/block/machine_side.png")
        self.fixture.write_png("textures/block/machine_top.png")
        result = self._scan_models()
        record = result.data["models"]["novadyne:block/macerator"]
        self.assertEqual(len(record["texture_files"]), 3)
        self.assertEqual(record["missing_textures"], [])

    def test_texture_reference_resolved(self):
        self.fixture.write_asset_json(
            "models/item/coisa.json",
            {"parent": "minecraft:item/generated", "textures": {"layer0": "novadyne:item/coisa"}},
        )
        self.fixture.write_png("textures/item/coisa.png")
        result = self._scan_models()
        record = result.data["models"]["novadyne:item/coisa"]
        self.assertEqual(
            record["texture_files"],
            ["src/main/resources/assets/novadyne/textures/item/coisa.png"],
        )

    def test_missing_texture_detected(self):
        self.fixture.write_asset_json(
            "models/item/coisa.json",
            {"parent": "minecraft:item/generated", "textures": {"layer0": "novadyne:item/coisa"}},
        )
        result = self._scan_models()
        record = result.data["models"]["novadyne:item/coisa"]
        self.assertEqual(record["texture_files"], [])
        self.assertEqual(record["missing_textures"], ["novadyne:item/coisa"])
        self.assertEqual(result.data["missing_textures"], ["novadyne:item/coisa"])

    def test_missing_model_warning_for_registered_item(self):
        # Item registrado, com lang e item definition, mas sem models/item/*.json.
        self.fixture.add_simple_item("sem_modelo", "Sem Modelo")
        self.fixture.write_asset_json(
            "items/sem_modelo.json",
            {"model": {"type": "minecraft:model", "model": "novadyne:item/sem_modelo"}},
        )
        reporter = Reporter()
        catalog, _ = self.fixture.run_catalog(reporter)
        entry = next(e for e in catalog["entries"] if e["path"] == "sem_modelo")
        self.assertTrue(
            any("modelo ausente" in w for w in entry.get("warnings", [])),
            entry.get("warnings"),
        )
        self.assertTrue(any("modelo ausente" in w.message for w in reporter.warnings))

    def test_missing_texture_warning_for_registered_item(self):
        # Item registrado, modelo existe, mas a textura referenciada não existe.
        self.fixture.add_simple_item("sem_textura", "Sem Textura")
        self.fixture.write_asset_json(
            "models/item/sem_textura.json",
            {"parent": "minecraft:item/generated", "textures": {"layer0": "novadyne:item/sem_textura"}},
        )
        self.fixture.write_asset_json(
            "items/sem_textura.json",
            {"model": {"type": "minecraft:model", "model": "novadyne:item/sem_textura"}},
        )
        reporter = Reporter()
        catalog, _ = self.fixture.run_catalog(reporter)
        entry = next(e for e in catalog["entries"] if e["path"] == "sem_textura")
        self.assertTrue(
            any("textura ausente" in w for w in entry.get("warnings", [])),
            entry.get("warnings"),
        )
        self.assertTrue(any("textura ausente" in w.message for w in reporter.warnings))


if __name__ == "__main__":
    unittest.main()
