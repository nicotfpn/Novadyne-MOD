"""Geração de páginas a partir do catálogo (Fase 4).

Constrói uma página por entrada do catálogo em pastas por categoria
(docs/itens, docs/blocos, docs/maquinas, docs/misc), reaproveitando o
agrupamento por primeiro segmento do `build_nav()` para a navegação.

Máquinas (bloco com block_entity + menu) produzem uma página única em
docs/maquinas/; as entradas de block_entity, menu e item de bloco da mesma
máquina são fundidas nela em vez de gerar páginas separadas.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .config import BASE_CONFIG
from .paths import GENERATED_BANNER
from .scanners.common import parse_resource_id

_REPO_URL = str(BASE_CONFIG["repo_url"]).rstrip("/")
_DEFAULT_BRANCH = "main"

_MACHINE_LINKS = ("block_entity", "menu")

_CRAFTING_TYPES = {"minecraft:crafting_shapeless", "minecraft:crafting_shaped"}
_COOKING_TYPES = {
    "minecraft:smelting", "minecraft:blasting",
    "minecraft:smoking", "minecraft:campfire_cooking",
}

_TYPE_LABELS = {
    "minecraft:crafting_shapeless": "Crafting (shapeless)",
    "minecraft:crafting_shaped": "Crafting (grade)",
    "minecraft:smelting": "Forno",
    "minecraft:blasting": "Fundição",
    "minecraft:smoking": "Defumador",
    "minecraft:campfire_cooking": "Fogueira",
}


@dataclass
class GeneratedPage:
    """Uma página gerada a partir do catálogo (caminho relativo a docs_dir)."""

    dest_rel: str
    title: str
    nav_title: str | None = None
    order: int = 100
    body: str = ""


# -- utilidades ---------------------------------------------------------


def _rel_link(from_dest: str, to_dest: str) -> str:
    """Caminho relativo POSIX de uma página até outra (ambas docs-relativas)."""
    base_dir = os.path.dirname(from_dest)
    if not base_dir:
        return to_dest
    return os.path.relpath(to_dest, start=base_dir).replace("\\", "/")


def _texture_rel(texture_id: str | None, mod_id: str) -> str | None:
    """'novadyne:item/pure_silicon' -> 'assets/textures/item/pure_silicon.png'.

    Retorna None para namespaces que não são do mod (ex: minecraft:...),
    cujas texturas não são copiadas para a árvore docs.
    """
    if not texture_id:
        return None
    parsed = parse_resource_id(texture_id)
    if not parsed or parsed[0] != mod_id:
        return None
    return f"assets/textures/{parsed[1]}.png"


def _source_link(registration_source: str | None) -> str:
    """Link GitHub para 'arquivo:linha' (ou texto simples quando inválido)."""
    if not registration_source:
        return ""
    path, sep, line = registration_source.rpartition(":")
    if not sep:
        path, line = registration_source, ""
    url = f"{_REPO_URL}/blob/{_DEFAULT_BRANCH}/{path}"
    if line.isdigit():
        url += f"#L{line}"
    return f"[`{registration_source}`]({url})"


def _table(rows: list[tuple[str, str]]) -> str:
    lines = ["| Campo | Valor |", "|---|---|"]
    for key, value in rows:
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


# -- roteamento de destino ----------------------------------------------


def _dest_for_entry(entry: dict, machine_blocks: set[str]) -> str | None:
    """Destino (relativo a docs_dir) de uma entrada, ou None se fundida."""
    entry_type = entry.get("type")
    path = entry.get("path")
    if not path:
        return None
    if entry_type == "block":
        folder = "maquinas" if entry["id"] in machine_blocks else "blocos"
        return f"{folder}/{path}.md"
    if entry_type == "item":
        if entry.get("block") in machine_blocks:
            return None  # item de bloco de máquina: página única em maquinas/
        return f"itens/{path}.md"
    if entry_type in _MACHINE_LINKS:
        if entry.get("block") in machine_blocks:
            return None  # block_entity/menu fundidos na página da máquina
        return f"maquinas/{path}.md"
    if entry_type == "creative_tab":
        return f"misc/{path}.md"
    return None


def _related_entries(entry: dict, entries: list[dict]) -> list[dict]:
    """block_entity/menu da mesma máquina (mesmo id do bloco)."""
    if entry.get("type") != "block":
        return []
    return [
        other for other in entries
        if other["id"] == entry["id"] and other.get("type") in _MACHINE_LINKS
    ]


# -- seções de conteúdo -------------------------------------------------


def _render_identification(entry: dict) -> list[str]:
    rows = [
        ("ID", f"`{entry['id']}`"),
        ("Tipo", entry.get("type", "")),
    ]
    translations = entry.get("translations") or {}
    if translations:
        labels = ", ".join(
            f"`{locale}` — {value}" for locale, value in sorted(translations.items())
        )
        rows.append(("Tradução", labels))
    return ["## Identificação", "", _table(rows), ""]


def _render_image(entry: dict, dest: str, mod_id: str) -> list[str]:
    texture_rel = _texture_rel(entry.get("texture"), mod_id)
    if not texture_rel:
        return []
    alt = entry.get("display_name") or entry["id"]
    return [
        "## Imagem",
        "",
        f"![{alt}]({_rel_link(dest, texture_rel)})",
        "",
    ]


def _render_tags(entry: dict) -> list[str]:
    tags = entry.get("tags") or []
    if not tags:
        return []
    lines = ["## Tags", ""]
    lines.extend(f"- `{tag}`" for tag in tags)
    lines.append("")
    return lines


def _render_as_ingredient(recipe_ids: list[str], *, dest, dest_by_id, recipes_by_id, entries_by_id) -> list[str]:
    """Receitas nas quais esta entrada é ingrediente (links para o resultado)."""
    if not recipe_ids:
        return []
    lines = ["### Usado como ingrediente", ""]
    for rid in sorted(recipe_ids):
        recipe = recipes_by_id.get(rid)
        result = recipe.get("result_item") if recipe else None
        if result and result in dest_by_id:
            name = (entries_by_id[result].get("display_name") or result)
            lines.append(f"- [{name}]({_rel_link(dest, dest_by_id[result])}) — receita `{rid}`")
        else:
            lines.append(f"- `{rid}`")
    lines.append("")
    return lines


def _recipe_label(recipe: dict) -> str:
    return _TYPE_LABELS.get(recipe.get("type"), recipe.get("type", ""))


def _item_cell(item_id: str | None, *, dest, dest_by_id, entries_by_id, mod_id) -> str:
    """Célula de um item: imagem do mod com link para a página da entrada."""
    if not item_id:
        return ""
    entry = entries_by_id.get(item_id)
    label = entry.get("display_name") if entry else item_id
    link = _rel_link(dest, dest_by_id[item_id]) if item_id in dest_by_id else None
    texture_id = (entry or {}).get("texture") or item_id
    texture_rel = _texture_rel(texture_id, mod_id)
    if texture_rel:
        img = f'<img src="{_rel_link(dest, texture_rel)}" alt="{label}" class="recipe-icon">'
        return f'<a href="{link}">{img}</a>' if link else img
    if link:
        return f'<a href="{link}">{label}</a>'
    return f"<code>{item_id}</code>"


def _ingredient_cell(ing: dict | None, *, dest, dest_by_id, entries_by_id, mod_id) -> str:
    """Célula de um ingrediente (item, tag ou alternativas)."""
    if not ing:
        return ""
    if ing.get("alternatives"):
        cell = " ou ".join(
            _ingredient_cell(alt, dest=dest, dest_by_id=dest_by_id,
                             entries_by_id=entries_by_id, mod_id=mod_id)
            for alt in ing["alternatives"]
        )
    elif ing.get("item"):
        cell = _item_cell(ing["item"], dest=dest, dest_by_id=dest_by_id,
                          entries_by_id=entries_by_id, mod_id=mod_id)
    elif ing.get("tag"):
        cell = f'<code>{ing["tag"]}</code>'
    else:
        cell = ""
    count = ing.get("count", 1)
    if count and count > 1:
        cell = f'{cell} <span class="recipe-count">×{count}</span>'
    return cell


def _result_cell(recipe: dict, *, dest, dest_by_id, entries_by_id, mod_id) -> str:
    cell = _item_cell(recipe.get("result_item"), dest=dest, dest_by_id=dest_by_id,
                      entries_by_id=entries_by_id, mod_id=mod_id)
    count = recipe.get("result_count", 1)
    if count and count > 1:
        cell = f'{cell} <span class="recipe-count">×{count}</span>'
    return cell


def _render_crafting_visual(recipe: dict, *, dest, dest_by_id, entries_by_id, mod_id) -> str:
    """Grade 3×3 (shaped: posições do padrão; shapeless: slots neutros)."""
    cells: list[str] = []
    if recipe.get("type") == "minecraft:crafting_shaped":
        key = recipe.get("key") or {}
        for row in recipe.get("pattern") or []:
            for char in row:
                if char in key:
                    cells.append(_ingredient_cell(
                        key[char], dest=dest, dest_by_id=dest_by_id,
                        entries_by_id=entries_by_id, mod_id=mod_id))
                else:
                    cells.append("")
    else:
        cells = [
            _ingredient_cell(ing, dest=dest, dest_by_id=dest_by_id,
                             entries_by_id=entries_by_id, mod_id=mod_id)
            for ing in recipe.get("ingredients") or []
        ]
    cells = (cells + [""] * 9)[:9]

    grid_rows = [
        "".join(f'<td class="recipe-slot">{cells[i + j]}</td>' for j in range(3))
        for i in range(0, 9, 3)
    ]
    result = _result_cell(recipe, dest=dest, dest_by_id=dest_by_id,
                          entries_by_id=entries_by_id, mod_id=mod_id)
    title = f'<p class="recipe-title"><strong>{_recipe_label(recipe)}</strong> — <code>{recipe["id"]}</code></p>'
    return "\n".join([
        title,
        '<table class="recipe-grid">',
        f'<tr>{grid_rows[0]}<td class="recipe-arrow" rowspan="3">→</td>'
        f'<td class="recipe-slot recipe-result" rowspan="3">{result}</td></tr>',
        f"<tr>{grid_rows[1]}</tr>",
        f"<tr>{grid_rows[2]}</tr>",
        "</table>",
    ])


def _render_cooking_visual(recipe: dict, *, dest, dest_by_id, entries_by_id, mod_id) -> str:
    """Visual compacto de forno: entrada → seta → saída."""
    ingredient = recipe.get("ingredient")
    if ingredient is None and recipe.get("ingredients"):
        ingredient = recipe["ingredients"][0]
    input_cell = _ingredient_cell(ingredient, dest=dest, dest_by_id=dest_by_id,
                                  entries_by_id=entries_by_id, mod_id=mod_id)
    result = _result_cell(recipe, dest=dest, dest_by_id=dest_by_id,
                          entries_by_id=entries_by_id, mod_id=mod_id)
    details: list[str] = []
    if recipe.get("cooking_time"):
        details.append(f"{recipe['cooking_time']} ticks")
    if recipe.get("experience") is not None:
        details.append(f"{recipe['experience']:g} XP")
    suffix = " — " + " · ".join(details) if details else ""
    title = (f'<p class="recipe-title"><strong>{_recipe_label(recipe)}</strong>'
             f' — <code>{recipe["id"]}</code>{suffix}</p>')
    return "\n".join([
        title,
        '<table class="recipe-grid recipe-cooking">',
        "<tr>",
        f'<td class="recipe-slot">{input_cell}</td>',
        '<td class="recipe-arrow">→</td>',
        f'<td class="recipe-slot recipe-result">{result}</td>',
        "</tr>",
        "</table>",
    ])


def _render_recipe_visual(recipe: dict, *, dest, dest_by_id, entries_by_id, mod_id) -> str:
    rtype = recipe.get("type")
    if rtype in _CRAFTING_TYPES:
        return _render_crafting_visual(recipe, dest=dest, dest_by_id=dest_by_id,
                                       entries_by_id=entries_by_id, mod_id=mod_id)
    if rtype in _COOKING_TYPES:
        return _render_cooking_visual(recipe, dest=dest, dest_by_id=dest_by_id,
                                      entries_by_id=entries_by_id, mod_id=mod_id)
    return f'- `{recipe["id"]}` ({rtype})'


def _render_as_result(recipe_ids: list[str], *, dest, dest_by_id, recipes_by_id,
                      entries_by_id, mod_id) -> list[str]:
    """Receitas que produzem esta entrada, com visual (grid/forno)."""
    if not recipe_ids:
        return []
    lines = ["### Obtido por", ""]
    for rid in sorted(recipe_ids):
        recipe = recipes_by_id.get(rid)
        if recipe and recipe.get("supported"):
            lines.append(_render_recipe_visual(recipe, dest=dest, dest_by_id=dest_by_id,
                                               entries_by_id=entries_by_id, mod_id=mod_id))
            lines.append("")
        elif rid in dest_by_id:
            name = entries_by_id[rid].get("display_name") or rid
            lines.append(f"- [{name}]({_rel_link(dest, dest_by_id[rid])})")
        else:
            lines.append(f"- `{rid}`")
    return lines


def _render_machine_recipe_note(related: list[dict]) -> list[str]:
    """Nota de receita não documentada nas páginas de máquina."""
    lines = [
        "## Receitas",
        "",
        '!!! note "Receitas da máquina"',
        "",
        "    Receita definida em código, ainda não documentada automaticamente.",
    ]
    be = next((entry for entry in related if entry.get("type") == "block_entity"), None)
    if be and be.get("registration_source"):
        lines += ["", f"    Registro: {_source_link(be['registration_source'])}"]
    lines.append("")
    return lines


def _render_recipes(entry: dict, related: list[dict], *, dest, dest_by_id,
                    recipes_by_id, entries_by_id, mod_id) -> list[str]:
    as_ingredient = _render_as_ingredient(
        entry.get("recipes_as_ingredient") or [], dest=dest,
        dest_by_id=dest_by_id, recipes_by_id=recipes_by_id, entries_by_id=entries_by_id,
    )
    as_result = _render_as_result(
        entry.get("recipes_as_result") or [], dest=dest,
        dest_by_id=dest_by_id, recipes_by_id=recipes_by_id,
        entries_by_id=entries_by_id, mod_id=mod_id,
    )
    if as_result:
        return ["## Receitas", ""] + as_ingredient + as_result
    if as_ingredient:
        return ["## Receitas", ""] + as_ingredient
    if related:
        return _render_machine_recipe_note(related)
    return []


def _render_loot(entry: dict) -> list[str]:
    loot = entry.get("loot_tables") or []
    if not loot:
        return []
    lines = ["## Loot tables", ""]
    lines.extend(f"- `{item}`" for item in loot)
    lines.append("")
    return lines


def _render_registry(entry: dict, related: list[dict]) -> list[str]:
    rows: list[tuple[str, str]] = [("Fonte", _source_link(entry.get("registration_source")))]
    for other in related:
        label = "Block entity" if other.get("type") == "block_entity" else "Menu"
        rows.append((label, _source_link(other.get("registration_source"))))
    return ["## Registro", "", _table(rows), ""]


# -- montagem -----------------------------------------------------------


def _render_entry_page(entry: dict, related: list[dict], *, dest: str,
                       dest_by_id: dict, recipes_by_id: dict,
                       entries_by_id: dict, mod_id: str) -> str:
    lines = [GENERATED_BANNER, "", f"# {entry.get('display_name') or entry['id']}", ""]

    if entry.get("documentation_status") == "manual" and entry.get("manual_description"):
        lines.append(entry["manual_description"].strip())
        lines.append("")

    lines += _render_identification(entry)
    lines += _render_image(entry, dest, mod_id)
    lines += _render_tags(entry)
    lines += _render_recipes(entry, related, dest=dest, dest_by_id=dest_by_id,
                             recipes_by_id=recipes_by_id, entries_by_id=entries_by_id,
                             mod_id=mod_id)
    lines += _render_loot(entry)
    lines += _render_registry(entry, related)

    body = "\n".join(lines).rstrip() + "\n"
    return body


def generate_catalog_pages(catalog: dict) -> list[GeneratedPage]:
    """Gera uma página por entrada do catálogo (mais índices por categoria)."""
    entries = catalog.get("entries", [])
    entries_by_id: dict[str, dict] = {}
    for entry in entries:
        entries_by_id.setdefault(entry["id"], entry)
    recipes_by_id = {r["id"]: r for r in catalog.get("recipes", [])}
    mod_id = str((catalog.get("mod") or {}).get("id") or "novadyne")

    machine_blocks = {
        e["id"] for e in entries
        if e.get("type") == "block" and (e.get("menu") or e.get("block_entity"))
    }

    dest_by_id: dict[str, str] = {}
    for entry in entries:
        dest = _dest_for_entry(entry, machine_blocks)
        if dest:
            dest_by_id[entry["id"]] = dest

    pages: list[GeneratedPage] = []
    seen_dests: set[str] = set()
    for entry in entries:
        dest = _dest_for_entry(entry, machine_blocks)
        if not dest or dest in seen_dests:
            continue
        seen_dests.add(dest)
        related = _related_entries(entry, entries)
        title = entry.get("display_name") or entry["id"]
        body = _render_entry_page(
            entry, related, dest=dest, dest_by_id=dest_by_id,
            recipes_by_id=recipes_by_id, entries_by_id=entries_by_id, mod_id=mod_id,
        )
        pages.append(GeneratedPage(dest_rel=dest, title=title, nav_title=title, body=body))

    pages.sort(key=lambda page: page.dest_rel)
    return pages
