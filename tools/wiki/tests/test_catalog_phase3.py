"""Testes do catálogo e pipeline (Fase 3).

Cobre os casos 1 (catálogo vazio válido), 22 (JSON inválido), 23 (ordem
determinística), 24 (segunda geração sem alterações), 25 (remoção de
conteúdo obsoleto), 26 (caminhos Windows e POSIX), 28 (colisão de IDs),
29 (arquivo fora do namespace do mod) e 30 (relatório consistente com o
catálogo).
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from novadyne_wiki.catalog import write_catalog
from novadyne_wiki.reporter import Reporter
from novadyne_wiki.report_builder import build_catalog_report
from novadyne_wiki.scanners.common import to_posix

from .support import ModFixture, write_text

BLOCKS_JAVA = """package com.novadyne;

import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks("novadyne");

    public static final DeferredBlock<Object> CAIXA =
            BLOCKS.registerBlock("caixa", Object::new,
                    props -> props.strength(2.0F, 4.0F).requiresCorrectToolForDrops());
}
"""


def _serialize(catalog: dict) -> str:
    return json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True)


class CatalogPipelineTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.fixture = ModFixture(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_empty_catalog_valid(self):
        catalog, _ = self.fixture.run_catalog()
        self.assertEqual(catalog["schema"], 1)
        self.assertEqual(catalog["schema_version"], 1)
        self.assertEqual(catalog["entries"], [])
        self.assertEqual(catalog["recipes"], [])
        self.assertEqual(catalog["tags"], [])
        self.assertEqual(catalog["mod"]["id"], "novadyne")
        self.assertEqual(catalog["mod"]["version"], "1.0.0")
        self.assertEqual(catalog["diagnostics"], {"warnings": [], "errors": []})
        self.assertEqual(catalog["generation"]["counts"],
                         {"entries": 0, "recipes": 0, "tags": 0})

    def test_deterministic_order(self):
        self.fixture.add_simple_item("beta")
        self.fixture.add_simple_item("alpha")
        first, _ = self.fixture.run_catalog()
        second, _ = self.fixture.run_catalog()
        self.assertEqual(_serialize(first), _serialize(second))
        ids = [e["id"] for e in first["entries"]]
        self.assertEqual(ids, sorted(ids))

    def test_second_generation_no_changes(self):
        self.fixture.add_simple_item("coisa")
        first, _ = self.fixture.run_catalog()
        second, _ = self.fixture.run_catalog()
        self.assertEqual(_serialize(first), _serialize(second))

    def test_obsolete_content_removed_on_regeneration(self):
        self.fixture.add_simple_item("permanente")
        first, _ = self.fixture.run_catalog()
        self.assertEqual(len(first["entries"]), 1)
        # Remove o registro Java e regenera: a entrada obsoleta some.
        (self.fixture.java / "ModItems.java").unlink()
        second, _ = self.fixture.run_catalog()
        self.assertEqual(second["entries"], [])

    def test_stale_docs_removed_by_generation(self):
        from novadyne_wiki import cli

        build_dir = self.tmp / "build"
        docs_dir = self.tmp / "docs"
        content_dir = self.tmp / "content"
        theme_dir = self.tmp / "theme"
        theme_dir.mkdir(parents=True)
        content_dir.mkdir(parents=True)
        write_text(content_dir / "index.md",
                   "---\ntitle: NovaDyne\norder: 0\n---\n# Home\n")

        site_kwargs = {
            "content_dir": content_dir,
            "docs_dir": docs_dir,
            "theme_dir": theme_dir,
            "custom_config": self.tmp / "mkdocs.custom.yml",
            "config_path": self.tmp / "mkdocs.yml",
        }
        self.fixture.add_simple_item("coisa")
        cli.run_generation(Reporter(), build_dir=build_dir, site_kwargs=site_kwargs,
                           catalog_kwargs=self.fixture.catalog_kwargs())
        stale = docs_dir / "stale.md"
        stale.write_text("velho", encoding="utf-8")
        self.assertTrue(stale.exists())
        cli.run_generation(Reporter(), build_dir=build_dir, site_kwargs=site_kwargs,
                           catalog_kwargs=self.fixture.catalog_kwargs())
        self.assertFalse(stale.exists())

    def test_generation_idempotent_via_manifest(self):
        from novadyne_wiki import cli

        build_dir = self.tmp / "build"
        docs_dir = self.tmp / "docs"
        content_dir = self.tmp / "content"
        theme_dir = self.tmp / "theme"
        theme_dir.mkdir(parents=True)
        content_dir.mkdir(parents=True)
        write_text(content_dir / "index.md",
                   "---\ntitle: NovaDyne\norder: 0\n---\n# Home\n")

        site_kwargs = {
            "content_dir": content_dir,
            "docs_dir": docs_dir,
            "theme_dir": theme_dir,
            "custom_config": self.tmp / "mkdocs.custom.yml",
            "config_path": self.tmp / "mkdocs.yml",
        }
        self.fixture.add_simple_item("coisa")
        first = cli.run_generation(Reporter(), build_dir=build_dir, site_kwargs=site_kwargs,
                                   catalog_kwargs=self.fixture.catalog_kwargs())
        second = cli.run_generation(Reporter(), build_dir=build_dir, site_kwargs=site_kwargs,
                                    catalog_kwargs=self.fixture.catalog_kwargs())
        self.assertEqual(first, second)
        self.assertIn("catalog.json", first)
        self.assertIn("report.json", first)
        self.assertIn("report.md", first)

    def test_windows_and_posix_paths(self):
        self.assertEqual(to_posix("a\\b\\c.json"), "a/b/c.json")
        self.assertEqual(to_posix(Path("a") / "b" / "c.json"), "a/b/c.json")
        self.fixture.add_simple_item("coisa")
        catalog, _ = self.fixture.run_catalog()
        entry = catalog["entries"][0]
        for source in entry["source_files"]:
            self.assertNotIn("\\", source)
            self.assertNotIn("\\\\", source)
        self.assertTrue(all("/" in s for s in entry["source_files"]))

    def test_id_collision_detected(self):
        # Dois registros com o mesmo id e o mesmo tipo.
        self.fixture.write_java(
            "ModItems.java",
            "package com.novadyne;\n"
            "import net.neoforged.neoforge.registries.DeferredRegister;\n"
            "import net.neoforged.neoforge.registries.DeferredItem;\n"
            "import net.minecraft.world.item.Item;\n"
            "public final class ModItems {\n"
            "    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(\"novadyne\");\n"
            '    public static final DeferredItem<Item> A = ITEMS.registerSimpleItem("duplicado");\n'
            "    public static final DeferredItem<Item> B = ITEMS.registerSimpleItem(\"duplicado\");\n"
            "}\n",
        )
        reporter = Reporter()
        self.fixture.run_catalog(reporter)
        self.assertTrue(
            any("colisão de IDs" in e.message for e in reporter.errors),
            [e.render() for e in reporter.errors],
        )

    def test_block_and_block_item_same_id_is_not_collision(self):
        # Bloco e item de bloco compartilham o id: é o caso normal no Minecraft.
        self.fixture.write_java("ModBlocks.java", BLOCKS_JAVA)
        self.fixture.write_java(
            "ModItems.java",
            "package com.novadyne;\n"
            "import net.neoforged.neoforge.registries.DeferredRegister;\n"
            "import net.neoforged.neoforge.registries.DeferredItem;\n"
            "public final class ModItems {\n"
            "    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(\"novadyne\");\n"
            '    public static final DeferredItem<Object> CAIXA =\n'
            '            ITEMS.registerSimpleBlockItem("caixa", ModBlocks.CAIXA);\n'
            "}\n",
        )
        reporter = Reporter()
        catalog, _ = self.fixture.run_catalog(reporter)
        self.assertEqual([e for e in reporter.errors], [])
        same_id = [e["type"] for e in catalog["entries"] if e["path"] == "caixa"]
        self.assertIn("block", same_id)
        self.assertIn("item", same_id)

    def test_file_outside_mod_namespace_ignored(self):
        (self.fixture.assets / "outromod").mkdir(parents=True, exist_ok=True)
        write_text(self.fixture.assets / "outromod" / "models" / "x.json", "{}")
        self.fixture.add_simple_item("coisa")
        catalog, summary = self.fixture.run_catalog()
        ignored_paths = [item["path"] for item in summary["ignored_files"]]
        self.assertTrue(
            any("outromod" in p for p in ignored_paths),
            ignored_paths,
        )
        reasons = {item["reason"] for item in summary["ignored_files"]}
        self.assertIn("arquivo fora do namespace do mod", reasons)

    def test_invalid_json_produces_error_and_continues(self):
        self.fixture.write_data(
            "novadyne/recipe/quebrada.json",
            '{"type": "minecraft:crafting_shapeless", "ingredients": [',
        )
        self.fixture.write_data_json(
            "novadyne/recipe/ok.json",
            {
                "type": "minecraft:crafting_shapeless",
                "ingredients": ["minecraft:iron_ingot"],
                "result": {"id": "novadyne:coisa"},
            },
        )
        reporter = Reporter()
        catalog, _ = self.fixture.run_catalog(reporter)
        self.assertEqual(len(catalog["recipes"]), 1)
        self.assertTrue(
            any("JSON inválido" in e.message for e in reporter.errors),
            [e.render() for e in reporter.errors],
        )
        self.assertTrue(catalog["diagnostics"]["errors"])

    def test_report_consistent_with_catalog(self):
        self.fixture.add_simple_item("coisa")
        self.fixture.write_data_json(
            "novadyne/recipe/coisa.json",
            {
                "type": "minecraft:crafting_shapeless",
                "ingredients": ["minecraft:iron_ingot"],
                "result": {"id": "novadyne:coisa", "count": 1},
            },
        )
        catalog, summary = self.fixture.run_catalog()
        report = build_catalog_report(catalog, summary)
        self.assertEqual(
            sum(report["entries_by_type"].values()), len(catalog["entries"]),
        )
        self.assertEqual(
            sum(report["recipes_by_type"].values()), len(catalog["recipes"]),
        )
        self.assertEqual(report["entries_total"], len(catalog["entries"]))
        self.assertEqual(report["recipes_total"], len(catalog["recipes"]))

    def test_write_catalog_deterministic(self):
        catalog, _ = self.fixture.run_catalog()
        target = self.tmp / "catalog.json"
        write_catalog(catalog, target)
        data = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["generation"]["counts"], catalog["generation"]["counts"])

    # -- documentação manual (Fase 4) -------------------------------------

    def _write_manual_description(self, entry_id: str, body: str = "descrição manual"):
        write_text(
            self.fixture.root / "wiki" / "content" / "entries" / f"{entry_id.split(':')[1]}.md",
            f"---\nid: {entry_id}\ntitle: Teste\n---\n\n{body}\n",
        )

    def test_entry_with_manual_description_is_manual(self):
        self.fixture.add_simple_item("pure_silicon")
        self._write_manual_description("novadyne:pure_silicon")
        catalog, _ = self.fixture.run_catalog()
        entry = catalog["entries"][0]
        self.assertEqual(entry["documentation_status"], "manual")
        self.assertEqual(entry["manual_description"], "descrição manual")

    def test_entry_with_warning_and_no_description_is_missing(self):
        self.fixture.add_simple_item("sem_descricao")
        catalog, _ = self.fixture.run_catalog()
        entry = catalog["entries"][0]
        self.assertTrue(entry["warnings"])
        self.assertEqual(entry["documentation_status"], "missing")
        self.assertNotIn("manual_description", entry)

    def test_normal_entry_stays_auto(self):
        self.fixture.add_simple_item("coisa")
        self.fixture.add_item_model("coisa")
        catalog, _ = self.fixture.run_catalog()
        entry = catalog["entries"][0]
        self.assertEqual(entry["warnings"], [])
        self.assertEqual(entry["documentation_status"], "auto")

    def test_manual_description_survives_second_generation(self):
        self.fixture.add_simple_item("pure_silicon")
        self._write_manual_description("novadyne:pure_silicon")
        first, _ = self.fixture.run_catalog()
        second, _ = self.fixture.run_catalog()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
