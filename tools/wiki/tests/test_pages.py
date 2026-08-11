"""Testes de geração de páginas a partir do catálogo (pages.py)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from novadyne_wiki import builder
from novadyne_wiki.pages import generate_catalog_pages
from novadyne_wiki.reporter import Reporter


def _entry(**overrides) -> dict:
    base = {
        "id": "novadyne:pure_silicon",
        "namespace": "novadyne",
        "path": "pure_silicon",
        "type": "item",
        "display_name": "Pure Silicon",
        "translations": {"en_us": "Pure Silicon"},
        "texture": "novadyne:item/pure_silicon",
        "model": "novadyne:item/pure_silicon",
        "registration_source": "src/main/java/com/novadyne/ModItems.java:11",
        "tags": [],
        "recipes_as_result": [],
        "recipes_as_ingredient": [],
        "loot_tables": [],
        "documentation_status": "auto",
        "warnings": [],
        "properties": {},
    }
    base.update(overrides)
    return base


def _machine_entries() -> list[dict]:
    return [
        _entry(
            id="novadyne:macerator", path="macerator", type="block",
            display_name="Macerator", texture="novadyne:block/macerator_front",
            model="novadyne:block/macerator", blockstate="novadyne:macerator",
            item="novadyne:macerator", menu="novadyne:macerator",
            block_entity="novadyne:macerator", loot_tables=["novadyne:blocks/macerator"],
            registration_source="src/main/java/com/novadyne/ModBlocks.java:14",
            properties={"variants": 4},
        ),
        _entry(
            id="novadyne:macerator", path="macerator", type="item",
            display_name="Macerator", block="novadyne:macerator",
            texture="novadyne:block/macerator_front", model="novadyne:block/macerator",
            registration_source="src/main/java/com/novadyne/ModItems.java:23",
        ),
        _entry(
            id="novadyne:macerator", path="macerator", type="block_entity",
            block="novadyne:macerator",
            registration_source="src/main/java/com/novadyne/ModBlockEntities.java:17",
        ),
        _entry(
            id="novadyne:macerator", path="macerator", type="menu",
            block="novadyne:macerator",
            registration_source="src/main/java/com/novadyne/ModMenuTypes.java:18",
        ),
    ]


def _catalog(entries: list[dict]) -> dict:
    return {"entries": entries, "recipes": [], "tags": []}


class DestRelTests(unittest.TestCase):
    def _dests(self, entries: list[dict]) -> list[str]:
        return [p.dest_rel for p in generate_catalog_pages(_catalog(entries))
                if not p.dest_rel.endswith("/index.md")]

    def test_item_goes_to_itens(self):
        self.assertIn("itens/pure_silicon.md", self._dests([_entry()]))

    def test_plain_block_goes_to_blocos(self):
        block = _entry(type="block", path="caixa", id="novadyne:caixa")
        self.assertIn("blocos/caixa.md", self._dests([block]))

    def test_block_entity_and_menu_go_to_maquinas_when_orphan(self):
        be = _entry(type="block_entity", path="solo", id="novadyne:solo")
        menu = _entry(type="menu", path="solo", id="novadyne:solo")
        self.assertEqual(self._dests([be, menu]), ["maquinas/solo.md"])

    def test_creative_tab_goes_to_misc(self):
        tab = _entry(type="creative_tab", path="novadyne", id="novadyne:novadyne",
                     display_name="NovaDyne")
        self.assertIn("misc/novadyne.md", self._dests([tab]))


class EntryPageTests(unittest.TestCase):
    def _body(self, catalog, dest: str) -> str:
        if isinstance(catalog, list):
            catalog = _catalog(catalog)
        pages = generate_catalog_pages(catalog)
        return next(p.body for p in pages if p.dest_rel == dest)

    def test_simple_item_page_content(self):
        body = self._body([_entry()], "itens/pure_silicon.md")
        self.assertIn("# Pure Silicon", body)
        self.assertIn("novadyne:pure_silicon", body)
        self.assertIn("assets/textures/item/pure_silicon.png", body)
        self.assertIn("ModItems.java:11", body)

    def test_machine_merges_block_entity_and_menu_into_single_page(self):
        body = self._body(_machine_entries(), "maquinas/macerator.md")
        self.assertIn("# Macerator", body)
        self.assertIn("ModBlockEntities.java:17", body)
        self.assertIn("ModMenuTypes.java:18", body)
        self.assertIn("ModBlocks.java:14", body)
        self.assertIn("assets/textures/block/macerator_front.png", body)

    def test_recipe_links_resolve_to_entry_pages(self):
        recipes = [{
            "id": "novadyne:valve_tier_1",
            "type": "minecraft:crafting_shapeless",
            "result_item": "novadyne:valve_tier_1",
        }]
        valve_1 = _entry(id="novadyne:valve_tier_1", path="valve_tier_1",
                         display_name="Valve (Tier 1)", recipes_as_result=["novadyne:valve_tier_1"])
        valve_2 = _entry(id="novadyne:valve_tier_2", path="valve_tier_2",
                         display_name="Valve (Tier 2)", recipes_as_ingredient=["novadyne:valve_tier_1"])
        catalog = {"entries": [valve_1, valve_2], "recipes": recipes, "tags": []}
        body = self._body(catalog, "itens/valve_tier_2.md")
        self.assertIn("valve_tier_1.md", body)
        self.assertIn("Valve (Tier 1)", body)

    def test_manual_description_renders_before_auto_data(self):
        manual = _entry(
            documentation_status="manual",
            manual_description="Texto escrito à mão sobre o item.",
        )
        body = self._body([manual], "itens/pure_silicon.md")
        self.assertLess(body.index("Texto escrito à mão"),
                        body.index("## Identificação"))


class RecipeVisualTests(unittest.TestCase):
    def _body(self, catalog: dict, dest: str) -> str:
        pages = generate_catalog_pages(catalog)
        return next(p.body for p in pages if p.dest_rel == dest)

    def test_shapeless_recipe_renders_grid(self):
        recipe = {
            "id": "novadyne:valve_tier_1",
            "type": "minecraft:crafting_shapeless",
            "supported": True,
            "result_item": "novadyne:valve_tier_1",
            "result_count": 1,
            "ingredients": [
                {"item": "minecraft:iron_ingot"},
                {"item": "minecraft:iron_ingot"},
                {"item": "minecraft:iron_ingot"},
                {"item": "minecraft:copper_ingot"},
            ],
        }
        valve = _entry(id="novadyne:valve_tier_1", path="valve_tier_1",
                       display_name="Valve (Tier 1)", recipes_as_result=["novadyne:valve_tier_1"])
        catalog = {"entries": [valve], "recipes": [recipe], "tags": []}
        body = self._body(catalog, "itens/valve_tier_1.md")
        self.assertIn('class="recipe-grid"', body)
        self.assertIn("minecraft:iron_ingot", body)
        self.assertIn("valve_tier_1", body)

    def test_smelting_recipe_renders_compact_visual(self):
        recipe = {
            "id": "novadyne:pure_silicon_from_quartz",
            "type": "minecraft:smelting",
            "supported": True,
            "result_item": "novadyne:pure_silicon",
            "result_count": 1,
            "ingredient": {"tag": "c:gems/quartz"},
            "experience": 0.2,
            "cooking_time": 200,
        }
        silicon = _entry(recipes_as_result=["novadyne:pure_silicon_from_quartz"])
        catalog = {"entries": [silicon], "recipes": [recipe], "tags": []}
        body = self._body(catalog, "itens/pure_silicon.md")
        self.assertIn("recipe-cooking", body)
        self.assertIn("recipe-arrow", body)
        self.assertIn("<code>c:gems/quartz</code>", body)
        self.assertIn("200 ticks", body)

    def test_shaped_recipe_uses_pattern_positions(self):
        recipe = {
            "id": "novadyne:grade",
            "type": "minecraft:crafting_shaped",
            "supported": True,
            "result_item": "novadyne:coisa",
            "result_count": 1,
            "pattern": ["AA", "AA"],
            "key": {"A": {"item": "novadyne:pure_silicon"}},
        }
        coisa = _entry(id="novadyne:coisa", path="coisa",
                       display_name="Coisa", recipes_as_result=["novadyne:grade"])
        catalog = {"entries": [coisa], "recipes": [recipe], "tags": []}
        body = self._body(catalog, "itens/coisa.md")
        self.assertEqual(body.count('class="recipe-slot"'), 9)

    def test_machine_page_shows_recipe_note(self):
        body = self._body(_catalog(_machine_entries()), "maquinas/macerator.md")
        self.assertIn("ainda não documentada automaticamente", body)
        self.assertIn("ModBlockEntities.java:17", body)
        self.assertIn("## Receitas", body)


class IndexPageTests(unittest.TestCase):
    def _catalog_with_machine(self) -> dict:
        entries = [_entry()] + _machine_entries()
        return _catalog(entries)

    def test_section_index_pages_generated(self):
        pages = generate_catalog_pages(self._catalog_with_machine())
        dests = [p.dest_rel for p in pages]
        for index in ("itens/index.md", "blocos/index.md", "maquinas/index.md"):
            self.assertIn(index, dests)

    def test_index_uses_grid_cards_with_image_and_link(self):
        pages = generate_catalog_pages(self._catalog_with_machine())
        body = next(p.body for p in pages if p.dest_rel == "itens/index.md")
        self.assertIn('<div class="grid cards" markdown>', body)
        self.assertIn("[Pure Silicon](pure_silicon.md)", body)
        self.assertIn("assets/textures/item/pure_silicon.png", body)

    def test_machine_index_lists_only_machines(self):
        pages = generate_catalog_pages(self._catalog_with_machine())
        body = next(p.body for p in pages if p.dest_rel == "maquinas/index.md")
        self.assertIn("[Macerator](macerator.md)", body)
        self.assertNotIn("pure_silicon", body)

    def test_index_pages_are_deterministic(self):
        first = generate_catalog_pages(self._catalog_with_machine())
        second = generate_catalog_pages(self._catalog_with_machine())
        self.assertEqual([p.body for p in first], [p.body for p in second])


class BuilderIntegrationTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_build_site_writes_generated_pages(self):
        docs_dir = self.tmp / "docs"
        theme_dir = self.tmp / "theme"
        theme_dir.mkdir()
        content_dir = self.tmp / "content"
        content_dir.mkdir()
        (content_dir / "index.md").write_text(
            "---\ntitle: NovaDyne\norder: 0\n---\n# Home\n", encoding="utf-8",
        )
        textures_dir = self.tmp / "textures"
        (textures_dir / "item").mkdir(parents=True)
        (textures_dir / "item" / "pure_silicon.png").write_bytes(b"\x89PNG-fake")

        manifest = builder.build_site(
            Reporter(),
            catalog=_catalog([_entry()]),
            content_dir=content_dir,
            docs_dir=docs_dir,
            theme_dir=theme_dir,
            textures_dir=textures_dir,
            custom_config=self.tmp / "mkdocs.custom.yml",
            config_path=self.tmp / "mkdocs.yml",
        )
        self.assertTrue((docs_dir / "itens" / "pure_silicon.md").exists())
        self.assertIn("itens/pure_silicon.md", manifest)
        self.assertTrue((docs_dir / "assets" / "textures" / "item" / "pure_silicon.png").exists())

    def test_build_site_without_catalog_skips_generated_pages(self):
        docs_dir = self.tmp / "docs"
        theme_dir = self.tmp / "theme"
        theme_dir.mkdir()
        content_dir = self.tmp / "content"
        content_dir.mkdir()
        (content_dir / "index.md").write_text(
            "---\ntitle: NovaDyne\norder: 0\n---\n# Home\n", encoding="utf-8",
        )
        builder.build_site(
            Reporter(),
            content_dir=content_dir,
            docs_dir=docs_dir,
            theme_dir=theme_dir,
            custom_config=self.tmp / "mkdocs.custom.yml",
            config_path=self.tmp / "mkdocs.yml",
        )
        self.assertFalse((docs_dir / "itens").exists())


if __name__ == "__main__":
    unittest.main()
