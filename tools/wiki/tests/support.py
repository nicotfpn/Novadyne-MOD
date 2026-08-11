"""Fixtures compartilhadas dos testes da Fase 3.

Cria árvores de projeto mínimas em diretórios temporários, sem tocar o
repositório real. Todos os caminhos são relativos à raiz da fixture.
"""

from __future__ import annotations

import json
from pathlib import Path


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_json(path: Path, data) -> Path:
    return write_text(path, json.dumps(data, ensure_ascii=False, indent=2))


class ModFixture:
    """Árvore de projeto mínima (Java + resources) para testes."""

    def __init__(self, root: Path, mod_id: str = "novadyne"):
        self.root = Path(root)
        self.mod_id = mod_id
        self.java = self.root / "src" / "main" / "java" / "com" / "novadyne"
        self.assets = self.root / "src" / "main" / "resources" / "assets"
        self.data = self.root / "src" / "main" / "resources" / "data"
        for directory in (self.java, self.assets, self.data):
            directory.mkdir(parents=True, exist_ok=True)
        write_text(
            self.root / "gradle.properties",
            "mod_id=" + mod_id + "\n"
            "mod_name=TestMod\n"
            "mod_version=1.0.0\n"
            "mod_license=Test\n"
            "mod_description=Mod de teste\n"
            "mod_authors=Tester\n"
            "minecraft_version=26.1.2\n"
            "neo_version=26.1.2.76\n",
        )

    def write_java(self, rel: str, content: str) -> Path:
        return write_text(self.java / rel, content)

    def write_asset(self, rel: str, content: str) -> Path:
        return write_text(self.assets / self.mod_id / rel, content)

    def write_asset_json(self, rel: str, data) -> Path:
        return write_json(self.assets / self.mod_id / rel, data)

    def write_data(self, rel: str, content: str) -> Path:
        return write_text(self.data / rel, content)

    def write_data_json(self, rel: str, data) -> Path:
        return write_json(self.data / rel, data)

    def write_png(self, rel: str) -> Path:
        return write_text(self.assets / self.mod_id / rel, "\x89PNG-fake")

    def run_catalog(self, reporter=None):
        """Executa o pipeline contra esta fixture."""
        from novadyne_wiki.pipeline import generate_catalog
        from novadyne_wiki.reporter import Reporter

        return generate_catalog(
            reporter or Reporter(),
            **self.catalog_kwargs(),
        )

    def catalog_kwargs(self) -> dict:
        """Argumentos para generate_catalog/run_generation apontando p/ a fixture."""
        return {
            "project_root": self.root,
            "java_root": self.java,
            "assets_root": self.assets,
            "data_root": self.data,
            "mod_id": self.mod_id,
        }

    # -- atalhos de conteúdo comum ----------------------------------------

    def add_simple_item(self, name: str, display: str | None = None):
        self.write_java(
            "ModItems.java",
            "package com.novadyne;\n"
            "import net.neoforged.neoforge.registries.DeferredRegister;\n"
            "import net.neoforged.neoforge.registries.DeferredItem;\n"
            "import net.minecraft.world.item.Item;\n"
            "public final class ModItems {\n"
            "    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(\"novadyne\");\n"
            f'    public static final DeferredItem<Item> {name.upper()} = ITEMS.registerSimpleItem("{name}");\n'
            "}\n",
        )
        self.add_lang(f"item.novadyne.{name}", display or name.replace("_", " ").title())

    def add_lang(self, key: str, value: str, locale: str = "en_us"):
        path = self.assets / self.mod_id / "lang" / f"{locale}.json"
        data = {}
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        data[key] = value
        write_json(path, data)

    def add_item_model(self, name: str):
        self.write_asset_json(
            f"models/item/{name}.json",
            {"parent": "minecraft:item/generated", "textures": {"layer0": f"novadyne:item/{name}"}},
        )
        self.write_asset_json(
            f"items/{name}.json",
            {"model": {"type": "minecraft:model", "model": f"novadyne:item/{name}"}},
        )
        self.write_png(f"textures/item/{name}.png")
