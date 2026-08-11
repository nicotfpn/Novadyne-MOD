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


def _texture_rel(texture_id: str | None) -> str | None:
    """'novadyne:item/pure_silicon' -> 'assets/textures/item/pure_silicon.png'."""
    if not texture_id:
        return None
    parsed = parse_resource_id(texture_id)
    if not parsed:
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


def _render_image(entry: dict, dest: str) -> list[str]:
    texture_rel = _texture_rel(entry.get("texture"))
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


def _render_as_result(recipe_ids: list[str], *, dest, dest_by_id, recipes_by_id, entries_by_id) -> list[str]:
    """Receitas que produzem esta entrada (visual na Fase de receitas)."""
    if not recipe_ids:
        return []
    lines = ["### Obtido por", ""]
    for rid in sorted(recipe_ids):
        if rid in dest_by_id:
            name = entries_by_id[rid].get("display_name") or rid
            lines.append(f"- [{name}]({_rel_link(dest, dest_by_id[rid])})")
        else:
            lines.append(f"- `{rid}`")
    lines.append("")
    return lines


def _render_recipes(entry: dict, *, dest, dest_by_id, recipes_by_id, entries_by_id) -> list[str]:
    as_ingredient = _render_as_ingredient(
        entry.get("recipes_as_ingredient") or [], dest=dest,
        dest_by_id=dest_by_id, recipes_by_id=recipes_by_id, entries_by_id=entries_by_id,
    )
    as_result = _render_as_result(
        entry.get("recipes_as_result") or [], dest=dest,
        dest_by_id=dest_by_id, recipes_by_id=recipes_by_id, entries_by_id=entries_by_id,
    )
    if not as_ingredient and not as_result:
        return []
    return ["## Receitas", ""] + as_ingredient + as_result


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
                       entries_by_id: dict) -> str:
    lines = [GENERATED_BANNER, "", f"# {entry.get('display_name') or entry['id']}", ""]

    if entry.get("documentation_status") == "manual" and entry.get("manual_description"):
        lines.append(entry["manual_description"].strip())
        lines.append("")

    lines += _render_identification(entry)
    lines += _render_image(entry, dest)
    lines += _render_tags(entry)
    lines += _render_recipes(entry, dest=dest, dest_by_id=dest_by_id,
                             recipes_by_id=recipes_by_id, entries_by_id=entries_by_id)
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
            recipes_by_id=recipes_by_id, entries_by_id=entries_by_id,
        )
        pages.append(GeneratedPage(dest_rel=dest, title=title, nav_title=title, body=body))

    pages.sort(key=lambda page: page.dest_rel)
    return pages
