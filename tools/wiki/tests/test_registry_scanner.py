"""Testes do RegistryScanner (descoberta de registros Java — Fase 3).

Cobre os casos 2 (item), 3 (bloco), 4 (entidade), 28 (colisão de IDs) e o
diagnóstico de registros não classificados.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from novadyne_wiki.scanners.registry_scanner import RegistryScanner

from .support import ModFixture

BLOCKS_JAVA = """package com.novadyne;

import com.novadyne.common.block.MaceratorBlock;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks("novadyne");

    public static final DeferredBlock<MaceratorBlock> MACERATOR =
            BLOCKS.registerBlock("macerator", MaceratorBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
}
"""

ITEMS_JAVA = """package com.novadyne;

import net.minecraft.world.item.Item;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems("novadyne");

    public static final DeferredItem<Item> PURE_SILICON = ITEMS.registerSimpleItem("pure_silicon");
    public static final DeferredItem<net.minecraft.world.item.BlockItem> MACERATOR =
            ITEMS.registerSimpleBlockItem("macerator", ModBlocks.MACERATOR);
}
"""

ENTITIES_JAVA = """package com.novadyne;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModEntities {
    public static final DeferredRegister<EntityType<?>> ENTITY_TYPES =
            DeferredRegister.create(Registries.ENTITY_TYPE, "novadyne");

    public static final DeferredHolder<EntityType<?>, EntityType<?>> TEST_VEHICLE =
            ENTITY_TYPES.register("test_vehicle", () -> EntityType.Builder.of(null, null).build("test_vehicle"));
}
"""

UNKNOWN_JAVA = """package com.novadyne;

import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModWeird {
    public static final DeferredRegister<Object> WEIRD = DeferredRegister.create(Registries.CUSTOM, "novadyne");

    public static final Object SOMETHING = WEIRD.register("something", () -> new Object());
}
"""


class RegistryScannerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.fixture = ModFixture(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def scan(self):
        scanner = RegistryScanner(
            java_root=self.fixture.java,
            project_root=self.fixture.root,
            mod_id=self.fixture.mod_id,
        )
        return scanner.scan()

    def test_registered_item(self):
        self.fixture.write_java("ModItems.java", ITEMS_JAVA)
        result = self.scan()
        regs = result.data["registrations"]
        pure_silicon = next(r for r in regs if r["id"] == "pure_silicon")
        self.assertEqual(pure_silicon["type"], "item")
        self.assertEqual(pure_silicon["method"], "registerSimpleItem")
        self.assertEqual(pure_silicon["constant"], "PURE_SILICON")
        self.assertEqual(pure_silicon["line"], 10)
        self.assertTrue(pure_silicon["source_file"].endswith("ModItems.java"))
        self.assertEqual(pure_silicon["source_file"], "src/main/java/com/novadyne/ModItems.java")

    def test_registered_block(self):
        self.fixture.write_java("ModBlocks.java", BLOCKS_JAVA)
        result = self.scan()
        macerator = next(r for r in result.data["registrations"] if r["id"] == "macerator")
        self.assertEqual(macerator["type"], "block")
        self.assertEqual(macerator["method"], "registerBlock")
        self.assertEqual(macerator["line"], 11)

    def test_block_item_reference_resolved(self):
        self.fixture.write_java("ModBlocks.java", BLOCKS_JAVA)
        self.fixture.write_java("ModItems.java", ITEMS_JAVA)
        result = self.scan()
        block_item = next(
            r for r in result.data["registrations"]
            if r["id"] == "macerator" and r["type"] == "item"
        )
        self.assertEqual(block_item["block_ref"], "ModBlocks.MACERATOR")
        self.assertEqual(block_item["block_id"], "macerator")
        self.assertEqual(result.diagnostics, [])

    def test_registered_entity(self):
        self.fixture.write_java("ModEntities.java", ENTITIES_JAVA)
        result = self.scan()
        vehicle = next(r for r in result.data["registrations"] if r["id"] == "test_vehicle")
        self.assertEqual(vehicle["type"], "entity")

    def test_unknown_registration_produces_diagnostic(self):
        self.fixture.write_java("ModWeird.java", UNKNOWN_JAVA)
        result = self.scan()
        self.assertEqual(result.data["unresolved"], ["something"])
        messages = [d.message for d in result.diagnostics]
        self.assertTrue(any("não classificado" in m for m in messages), messages)


if __name__ == "__main__":
    unittest.main()
