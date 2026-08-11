"""Leitura e normalização estrutural de receitas JSON (data/*/recipe/**) — Fase 3.

Suporta os formatos realmente presentes no projeto (26.1.x):

- ``minecraft:crafting_shapeless`` — ingredientes como array de strings;
- ``minecraft:crafting_shaped`` — padrão + chaves;
- ``minecraft:smelting`` / ``blasting`` / ``smoking`` / ``campfire_cooking``;
- ``minecraft:stonecutting`` / ``smithing_transform`` (estrutural).

Ingredientes podem ser string (``#tag`` → tag, senão item), objeto
(``{"item": ...}`` / ``{"tag": ...}``) ou array (alternativas). Resultado
normalizado de ``{"id": ..., "count": n}``, ``{"item": ...}`` ou string.

Tipos desconhecidos não derrubam a geração: são marcados como não suportados,
com os campos preservados em ``raw`` e um warning no relatório.
"""

from __future__ import annotations

from pathlib import Path

from ..errors import Issue
from ..io_utils import iter_files
from .common import ScanResult, load_json_file, parse_resource_id, to_posix

_KNOWN_TOP_LEVEL = {
    "type", "group", "category", "pattern", "key", "ingredient", "ingredients",
    "result", "experience", "cookingtime", "process_time", "show_notification",
}

# Tipos estruturados: mapeiam para normalização.
_SHAPELESS = {"minecraft:crafting_shapeless"}
_SHAPED = {"minecraft:crafting_shaped"}
_SINGLE_INGREDIENT = {
    "minecraft:smelting", "minecraft:blasting", "minecraft:smoking",
    "minecraft:campfire_cooking", "minecraft:stonecutting",
}
_SMITHING = {"minecraft:smithing_transform", "minecraft:smithing_trim"}
_SPECIAL = ("minecraft:crafting_special_",)


def _ingredient_dict(value) -> dict | None:
    """Normaliza um ingrediente para {"item"|"tag"|"alternatives": ...}.

    Nunca inventa ids: retorna None quando o formato não é reconhecido.
    """
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("#"):
            tag = stripped[1:]
            if parse_resource_id(tag):
                return {"tag": tag}
            return None
        if parse_resource_id(stripped):
            return {"item": stripped}
        return None
    if isinstance(value, dict):
        if isinstance(value.get("item"), str) and parse_resource_id(value["item"]):
            return {"item": value["item"]}
        if isinstance(value.get("tag"), str) and parse_resource_id(value["tag"]):
            return {"tag": value["tag"]}
        inner = value.get("item")
        if isinstance(inner, dict) and isinstance(inner.get("id"), str):
            return {"item": inner["id"]}
        return None
    if isinstance(value, list):
        alternatives = [_ingredient_dict(item) for item in value]
        alternatives = [item for item in alternatives if item is not None]
        if not alternatives:
            return None
        if len(alternatives) == 1:
            return alternatives[0]
        return {"alternatives": alternatives}
    return None


def _result_dict(value) -> dict | None:
    """Normaliza um resultado para {"id", "count"}."""
    if isinstance(value, str):
        if parse_resource_id(value):
            return {"id": value, "count": 1}
        return None
    if isinstance(value, dict):
        item_id = None
        if isinstance(value.get("id"), str) and parse_resource_id(value["id"]):
            item_id = value["id"]
        elif isinstance(value.get("item"), str) and parse_resource_id(value["item"]):
            item_id = value["item"]
        if item_id is None:
            return None
        count = value.get("count")
        try:
            count_int = int(count) if count is not None else 1
        except (TypeError, ValueError):
            count_int = 1
        return {"id": item_id, "count": count_int}
    return None


def _ingredient_items_and_tags(ingredients: list[dict]) -> tuple[set[str], set[str]]:
    """Itens diretos e tags referenciados por uma lista de ingredientes."""
    items: set[str] = set()
    tags: set[str] = set()

    def walk(entry: dict) -> None:
        if "item" in entry:
            items.add(entry["item"])
        if "tag" in entry:
            tags.add(entry["tag"])
        for alt in entry.get("alternatives", []):
            walk(alt)

    for entry in ingredients:
        walk(entry)
    return items, tags


class RecipeScanner:
    """Varre data/*/recipe/** e normaliza cada receita JSON."""

    def __init__(self, *, data_root, project_root, reporter=None):
        self.data_root = Path(data_root)
        self.project_root = Path(project_root)
        self.reporter = reporter

    def scan(self) -> ScanResult:
        result = ScanResult()
        recipes: list[dict] = []
        unknown_types: list[str] = []
        source_files: list[str] = []
        files_scanned = 0

        for path in iter_files(self.data_root, suffixes=(".json",)):
            rel_path = path.relative_to(self.data_root)
            parts = rel_path.parts
            if len(parts) < 3 or parts[1] != "recipe":
                continue
            files_scanned += 1
            rel = to_posix(path.relative_to(self.project_root))
            namespace = parts[0]
            recipe_path = Path(*parts[2:]).with_suffix("").as_posix()
            source_files.append(rel)

            data, err = load_json_file(path)
            if err is not None:
                result.diagnostics.append(Issue("error", f"receita inválida: {err}", path=rel))
                continue
            if not isinstance(data, dict):
                result.diagnostics.append(Issue(
                    "error", "receita inválida: esperado um objeto JSON", path=rel))
                continue

            rtype = data.get("type")
            if not isinstance(rtype, str):
                result.diagnostics.append(Issue(
                    "error", "receita sem campo \"type\" válido", path=rel))
                continue

            category = data.get("category")
            group = data.get("group")

            recipe: dict = {
                "id": f"{namespace}:{recipe_path}",
                "namespace": namespace,
                "path": recipe_path,
                "type": rtype,
                "category": category if isinstance(category, str) else None,
                "group": group if isinstance(group, str) else None,
                "source_file": rel,
                "result_item": None,
                "result_count": 1,
                "pattern": None,
                "key": None,
                "ingredients": [],
                "ingredient": None,
                "experience": None,
                "cooking_time": None,
                "process_time": None,
                "supported": True,
                "unsupported_reason": None,
                "raw": {k: v for k, v in data.items() if k not in _KNOWN_TOP_LEVEL},
            }

            result_value = _result_dict(data.get("result"))
            if result_value:
                recipe["result_item"] = result_value["id"]
                recipe["result_count"] = result_value["count"]

            if rtype in _SHAPED:
                pattern = data.get("pattern")
                if isinstance(pattern, list) and all(isinstance(row, str) for row in pattern):
                    recipe["pattern"] = list(pattern)
                keys = data.get("key")
                if isinstance(keys, dict):
                    normalized = {}
                    for char, value in keys.items():
                        ing = _ingredient_dict(value)
                        if ing is not None:
                            normalized[char] = ing
                    recipe["key"] = dict(sorted(normalized.items()))
                recipe["ingredients"] = [
                    entry for entry in (recipe["key"] or {}).values()
                ]
            elif rtype in _SHAPELESS:
                raw_ingredients = data.get("ingredients")
                if isinstance(raw_ingredients, list):
                    recipe["ingredients"] = [
                        entry for entry in (_ingredient_dict(v) for v in raw_ingredients)
                        if entry is not None
                    ]
            elif rtype in _SINGLE_INGREDIENT:
                ingredient = _ingredient_dict(data.get("ingredient"))
                recipe["ingredient"] = ingredient
                if ingredient is not None:
                    recipe["ingredients"] = [ingredient]
                experience = data.get("experience")
                if isinstance(experience, (int, float)) and not isinstance(experience, bool):
                    recipe["experience"] = float(experience)
                cooking_time = data.get("cookingtime")
                if isinstance(cooking_time, int) and not isinstance(cooking_time, bool):
                    recipe["cooking_time"] = cooking_time
            elif rtype in _SMITHING:
                parts_list = []
                for field in ("template", "base", "addition"):
                    entry = _ingredient_dict(data.get(field))
                    if entry is not None:
                        parts_list.append(entry)
                recipe["ingredients"] = parts_list
            elif rtype.startswith(_SPECIAL):
                recipe["raw"]["note"] = "receita especial sem grade normalizável"
            else:
                recipe["supported"] = False
                recipe["unsupported_reason"] = f"tipo de receita não suportado: {rtype}"
                unknown_types.append(f"{rtype} ({rel})")
                result.diagnostics.append(Issue(
                    "warning", recipe["unsupported_reason"], path=rel))

            ingredient_items, ingredient_tags = _ingredient_items_and_tags(
                recipe["ingredients"] + ([recipe["ingredient"]] if recipe["ingredient"] else [])
            )
            references: set[str] = set()
            if recipe["result_item"]:
                references.add(recipe["result_item"])
            references |= ingredient_items
            references |= {f"#{tag}" for tag in ingredient_tags}
            recipe["ingredient_items"] = sorted(ingredient_items)
            recipe["ingredient_tags"] = sorted(ingredient_tags)
            recipe["references"] = sorted(references)

            recipes.append(recipe)

        result.data = {
            "recipes": sorted(recipes, key=lambda r: r["id"]),
            "source_files": sorted(source_files),
            "unknown_types": sorted(set(unknown_types)),
        }
        result.coverage = {
            "files_scanned": files_scanned,
            "recipes_found": len(recipes),
        }
        return result
