"""Testes do mapeamento de itens vanilla (scanners/vanilla_items.py)."""

from __future__ import annotations

import unittest

from novadyne_wiki.scanners import vanilla_items


class VanillaItemsTests(unittest.TestCase):
    def test_known_overrides(self):
        self.assertEqual(vanilla_items.vanilla_item_id("CLAY_BALL"), "minecraft:clay_ball")
        self.assertEqual(vanilla_items.vanilla_item_id("COPPER_INGOT"), "minecraft:copper_ingot")
        self.assertEqual(vanilla_items.vanilla_item_id("WATER_BUCKET"), "minecraft:water_bucket")
        self.assertEqual(vanilla_items.vanilla_item_id("BUCKET"), "minecraft:bucket")

    def test_generic_lowercasing(self):
        self.assertEqual(vanilla_items.vanilla_item_id("IRON_INGOT"), "minecraft:iron_ingot")
        self.assertEqual(vanilla_items.vanilla_item_id("DIAMOND"), "minecraft:diamond")

    def test_heuristic_lowercases_valid_identifier(self):
        self.assertEqual(
            vanilla_items.vanilla_item_id("NOT_A_REAL_ITEM_XYZ"),
            "minecraft:not_a_real_item_xyz",
        )

    def test_unknown_returns_none(self):
        self.assertIsNone(vanilla_items.vanilla_item_id(""))
        self.assertIsNone(vanilla_items.vanilla_item_id("has space"))
        self.assertIsNone(vanilla_items.vanilla_item_id("123_num"))

    def test_idempotent(self):
        self.assertEqual(
            vanilla_items.vanilla_item_id("CLAY_BALL"),
            vanilla_items.vanilla_item_id("clay_ball"),
        )


if __name__ == "__main__":
    unittest.main()
