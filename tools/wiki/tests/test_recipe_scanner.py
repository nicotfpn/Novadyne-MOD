"""Testes do RecipeScanner (normalização estrutural — Fase 3).

Cobre os casos 13 (shaped), 14 (shapeless), 15 (ingrediente por item),
16 (ingrediente por tag), 17 (resultado com quantidade) e 18 (tipo de
receita desconhecido).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from .support import ModFixture


class RecipeScannerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.fixture = ModFixture(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def _scan_recipes(self):
        from novadyne_wiki.scanners.recipe_scanner import RecipeScanner

        return RecipeScanner(
            data_root=self.fixture.data,
            project_root=self.fixture.root,
        ).scan()

    def test_shapeless_recipe(self):
        self.fixture.write_data_json(
            "novadyne/recipe/coisa.json",
            {
                "type": "minecraft:crafting_shapeless",
                "category": "misc",
                "ingredients": ["minecraft:iron_ingot", "minecraft:copper_ingot"],
                "result": {"id": "novadyne:coisa", "count": 1},
            },
        )
        result = self._scan_recipes()
        recipe = result.data["recipes"][0]
        self.assertEqual(recipe["id"], "novadyne:coisa")
        self.assertEqual(recipe["type"], "minecraft:crafting_shapeless")
        self.assertEqual(recipe["result_item"], "novadyne:coisa")
        self.assertEqual(
            recipe["ingredients"],
            [{"item": "minecraft:iron_ingot"}, {"item": "minecraft:copper_ingot"}],
        )
        self.assertEqual(recipe["ingredient_items"], ["minecraft:copper_ingot", "minecraft:iron_ingot"])

    def test_shaped_recipe(self):
        self.fixture.write_data_json(
            "novadyne/recipe/placa.json",
            {
                "type": "minecraft:crafting_shaped",
                "category": "misc",
                "pattern": ["III", "ICI", "III"],
                "key": {
                    "I": {"item": "minecraft:iron_ingot"},
                    "C": "#c:gems/quartz",
                },
                "result": {"id": "novadyne:placa", "count": 4},
            },
        )
        result = self._scan_recipes()
        recipe = result.data["recipes"][0]
        self.assertEqual(recipe["pattern"], ["III", "ICI", "III"])
        self.assertEqual(recipe["key"]["I"], {"item": "minecraft:iron_ingot"})
        self.assertEqual(recipe["key"]["C"], {"tag": "c:gems/quartz"})
        self.assertEqual(recipe["result_count"], 4)

    def test_ingredient_by_tag(self):
        self.fixture.write_data_json(
            "novadyne/recipe/silicio.json",
            {
                "type": "minecraft:smelting",
                "ingredient": "#c:gems/quartz",
                "result": {"id": "novadyne:pure_silicon"},
                "experience": 0.2,
                "cookingtime": 200,
            },
        )
        result = self._scan_recipes()
        recipe = result.data["recipes"][0]
        self.assertEqual(recipe["ingredient"], {"tag": "c:gems/quartz"})
        self.assertEqual(recipe["ingredient_tags"], ["c:gems/quartz"])
        self.assertEqual(recipe["experience"], 0.2)
        self.assertEqual(recipe["cooking_time"], 200)

    def test_result_with_count(self):
        self.fixture.write_data_json(
            "novadyne/recipe/lote.json",
            {
                "type": "minecraft:crafting_shapeless",
                "ingredients": ["minecraft:iron_ingot"],
                "result": {"id": "novadyne:coisa", "count": 3},
            },
        )
        result = self._scan_recipes()
        recipe = result.data["recipes"][0]
        self.assertEqual(recipe["result_item"], "novadyne:coisa")
        self.assertEqual(recipe["result_count"], 3)

    def test_unknown_recipe_type(self):
        self.fixture.write_data_json(
            "novadyne/recipe/exotica.json",
            {
                "type": "novadyne:custom_reaction",
                "result": {"id": "novadyne:coisa", "count": 1},
                "campos_futuros": {"x": 1},
            },
        )
        result = self._scan_recipes()
        recipe = result.data["recipes"][0]
        self.assertFalse(recipe["supported"])
        self.assertIn("não suportado", recipe["unsupported_reason"])
        self.assertEqual(recipe["raw"], {"campos_futuros": {"x": 1}})
        self.assertTrue(
            any("novadyne:custom_reaction" in u for u in result.data["unknown_types"]),
            result.data["unknown_types"],
        )
        self.assertTrue(result.diagnostics)

    def test_alternatives_ingredient(self):
        self.fixture.write_data_json(
            "novadyne/recipe/alt.json",
            {
                "type": "minecraft:crafting_shapeless",
                "ingredients": [["minecraft:iron_ingot", "minecraft:copper_ingot"]],
                "result": {"id": "novadyne:coisa"},
            },
        )
        result = self._scan_recipes()
        recipe = result.data["recipes"][0]
        self.assertEqual(
            recipe["ingredients"],
            [{"alternatives": [{"item": "minecraft:iron_ingot"}, {"item": "minecraft:copper_ingot"}]}],
        )


if __name__ == "__main__":
    unittest.main()
