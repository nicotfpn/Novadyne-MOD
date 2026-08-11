"""Testes do LootTableScanner (leitura conservadora — Fase 3).

Cobre o caso 21 (loot table básica) e a associação por caminho no pipeline.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from .support import ModFixture


class LootTableScannerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.fixture = ModFixture(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_basic_loot_table(self):
        self.fixture.write_data_json(
            "novadyne/loot_table/blocks/macerator.json",
            {
                "type": "minecraft:block",
                "pools": [
                    {
                        "rolls": 1,
                        "entries": [
                            {"type": "minecraft:item", "name": "novadyne:macerator"}
                        ],
                        "conditions": [{"condition": "minecraft:survives_explosion"}],
                    }
                ],
            },
        )
        from novadyne_wiki.scanners.loot_table_scanner import LootTableScanner

        result = LootTableScanner(
            data_root=self.fixture.data,
            project_root=self.fixture.root,
        ).scan()
        loot = result.data["loot_tables"][0]
        self.assertEqual(loot["id"], "novadyne:blocks/macerator")
        self.assertEqual(loot["type"], "minecraft:block")
        self.assertEqual(loot["pools"], 1)
        self.assertEqual(loot["item_refs"], ["novadyne:macerator"])
        self.assertEqual(loot["conditions"], ["minecraft:survives_explosion"])
        self.assertEqual(loot["unsupported"], [])

    def test_unsupported_entry_recorded(self):
        self.fixture.write_data_json(
            "novadyne/loot_table/blocks/caixa.json",
            {
                "type": "minecraft:block",
                "pools": [
                    {
                        "rolls": 1,
                        "entries": [
                            {"type": "minecraft:loot_table", "name": "novadyne:other"}
                        ],
                    }
                ],
            },
        )
        from novadyne_wiki.scanners.loot_table_scanner import LootTableScanner

        result = LootTableScanner(
            data_root=self.fixture.data,
            project_root=self.fixture.root,
        ).scan()
        loot = result.data["loot_tables"][0]
        self.assertEqual(loot["item_refs"], [])
        self.assertEqual(
            loot["unsupported"],
            [{"type": "minecraft:loot_table", "name": "novadyne:other"}],
        )

    def test_block_entry_linked_by_path(self):
        # Bloco registrado + loot table em loot_table/blocks/<nome>.json
        self.fixture.write_java(
            "ModBlocks.java",
            "package com.novadyne;\n"
            "import net.neoforged.neoforge.registries.DeferredRegister;\n"
            "import net.neoforged.neoforge.registries.DeferredBlock;\n"
            "public final class ModBlocks {\n"
            "    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(\"novadyne\");\n"
            '    public static final DeferredBlock<Object> CAIXA =\n'
            '            BLOCKS.registerBlock("caixa", Object::new);\n'
            "}\n",
        )
        self.fixture.write_data_json(
            "novadyne/loot_table/blocks/caixa.json",
            {
                "type": "minecraft:block",
                "pools": [
                    {
                        "rolls": 1,
                        "entries": [{"type": "minecraft:item", "name": "novadyne:caixa"}],
                    }
                ],
            },
        )
        catalog, _ = self.fixture.run_catalog()
        entry = next(e for e in catalog["entries"] if e["path"] == "caixa" and e["type"] == "block")
        self.assertEqual(entry["loot_tables"], ["novadyne:blocks/caixa"])


if __name__ == "__main__":
    unittest.main()
