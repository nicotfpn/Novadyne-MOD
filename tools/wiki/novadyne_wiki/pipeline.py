"""Orquestração dos scanners e construção do catálogo (Fase 3).

O pipeline:

1. lê ``gradle.properties`` para os metadados do mod;
2. executa todos os scanners (Java, idiomas, modelos, blockstates, assets,
   receitas, tags, loot tables);
3. monta as entradas do catálogo e cruza referências (receitas, tags, loot);
4. verifica modelos/texturas por entrada e detecta assets órfãos;
5. produz o catálogo determinístico e o resumo usado pelo relatório.

Nenhum código do mod é executado; nenhum caminho absoluto entra no catálogo.
"""

from __future__ import annotations

from pathlib import Path

from .catalog import CatalogBuilder
from .io_utils import iter_files
from .paths import ASSETS_DIR, DATA_DIR, MAIN_JAVA, PROJECT_ROOT
from .scanners import (
    AssetScanner,
    BlockstateScanner,
    LanguageScanner,
    LootTableScanner,
    ModelScanner,
    RecipeScanner,
    RegistryScanner,
    TagScanner,
)
from .scanners.common import parse_resource_id, to_posix

# Tipos de entrada que possuem chave de tradução esperada.
_TRANSLATED_TYPES = ("item", "block", "entity")
# Subpastas de data/ reconhecidas nesta fase.
_KNOWN_DATA_DOMAINS = ("recipe", "tags", "loot_table")


def read_gradle_properties(path: Path) -> dict:
    """Lê gradle.properties (chave=valor simples, ignorando comentários)."""
    props: dict[str, str] = {}
    if not Path(path).exists():
        return props
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        props[key.strip()] = value.strip()
    return props


def build_mod_info(properties: dict, mod_id: str) -> dict:
    """Metadados do mod comprováveis em gradle.properties."""
    mapping = {
        "mod_id": "id",
        "mod_name": "name",
        "mod_version": "version",
        "mod_license": "license",
        "mod_description": "description",
        "mod_authors": "authors",
        "minecraft_version": "minecraft_version",
        "neo_version": "neo_version",
    }
    info: dict = {}
    for source_key, out_key in mapping.items():
        if properties.get(source_key):
            info[out_key] = properties[source_key]
    info["id"] = mod_id
    return info


def _merge_diagnostics(reporter, scan_results) -> None:
    """Encaminha os diagnósticos de todos os scanners ao Reporter."""
    for result in scan_results:
        for issue in result.diagnostics:
            if issue.severity == "error":
                reporter.error(issue.message, path=issue.path, context=issue.context)
            else:
                reporter.warning(issue.message, path=issue.path, context=issue.context)


def _translation_key(entry_type: str, namespace: str, path: str) -> str | None:
    if entry_type == "item":
        return f"item.{namespace}.{path}"
    if entry_type == "block":
        return f"block.{namespace}.{path}"
    if entry_type == "entity":
        return f"entity.{namespace}.{path}"
    if entry_type == "creative_tab":
        return f"itemGroup.{namespace}.{path}"
    return None


def _primary_texture(model_id: str | None, models: dict) -> str | None:
    """Textura principal de um modelo (layer0 → front → primeira)."""
    if not model_id:
        return None
    return _primary_texture_rec(model_id, models, set())


def _primary_texture_rec(model_id: str, models: dict, seen: set[str]) -> str | None:
    if model_id in seen:
        return None
    seen.add(model_id)
    record = models.get(model_id)
    if not record:
        return None
    textures = record.get("textures") or {}
    for key in ("layer0", "front"):
        if key in textures:
            return textures[key]
    if textures:
        return textures[sorted(textures)[0]]
    parent = record.get("parent")
    if parent:
        parsed = parse_resource_id(parent)
        if parsed:
            return _primary_texture_rec(parent, models, seen)
    return None


def _collect_ignored_files(project_root: Path, mod_id: str,
                           assets_root: Path, data_root: Path) -> list[dict]:
    """Arquivos deliberadamente ignorados nesta fase e o motivo."""
    ignored: list[dict] = []

    if assets_root.exists():
        for namespace_dir in sorted(p for p in assets_root.iterdir() if p.is_dir()):
            if namespace_dir.name == mod_id:
                continue
            for path in iter_files(namespace_dir):
                ignored.append({
                    "path": to_posix(path.relative_to(project_root)),
                    "reason": "arquivo fora do namespace do mod",
                })

    if data_root.exists():
        for path in iter_files(data_root, suffixes=(".json", ".bbmodel")):
            rel_path = path.relative_to(data_root)
            parts = rel_path.parts
            if len(parts) < 2 or parts[1] not in _KNOWN_DATA_DOMAINS:
                if path.suffix == ".bbmodel":
                    reason = "arquivo de projeto BlockBench excluído do build"
                else:
                    reason = "formato de dados não suportado nesta fase"
                ignored.append({
                    "path": to_posix(path.relative_to(project_root)),
                    "reason": reason,
                })

    return ignored


def _base_entry(reg: dict) -> dict:
    return {
        "id": f"{reg['namespace']}:{reg['path']}",
        "namespace": reg["namespace"],
        "path": reg["path"],
        "type": reg["type"],
        "registration_source": f"{reg['source_file']}:{reg['line']}",
        "source_files": [reg["source_file"]],
        "tags": [],
        "recipes_as_result": [],
        "recipes_as_ingredient": [],
        "loot_tables": [],
        "properties": {},
        "documentation_status": "auto",
        "warnings": [],
    }


def generate_catalog(
    reporter,
    *,
    project_root=PROJECT_ROOT,
    java_root=MAIN_JAVA,
    assets_root=ASSETS_DIR,
    data_root=DATA_DIR,
    mod_id: str | None = None,
) -> tuple[dict, dict]:
    """Executa o pipeline completo e retorna (catálogo, resumo para relatório)."""
    project_root = Path(project_root)
    assets_root = Path(assets_root)
    data_root = Path(data_root)

    properties = read_gradle_properties(project_root / "gradle.properties")
    if mod_id is None:
        mod_id = properties.get("mod_id") or "novadyne"
    mod_info = build_mod_info(properties, mod_id)

    # -- scanners ---------------------------------------------------------
    reg_result = RegistryScanner(java_root=java_root, project_root=project_root,
                                 mod_id=mod_id).scan()
    lang_result = LanguageScanner(assets_root=assets_root, project_root=project_root,
                                  mod_id=mod_id).scan()
    model_result = ModelScanner(assets_root=assets_root, project_root=project_root,
                                mod_id=mod_id).scan()
    bs_result = BlockstateScanner(assets_root=assets_root, project_root=project_root,
                                  mod_id=mod_id).scan()
    recipe_result = RecipeScanner(data_root=data_root, project_root=project_root).scan()
    tag_result = TagScanner(data_root=data_root, project_root=project_root).scan()
    loot_result = LootTableScanner(data_root=data_root, project_root=project_root).scan()

    models = model_result.data.get("models", {})
    blockstates = bs_result.data.get("blockstates", [])
    language_index = lang_result.data.get("index")
    item_definitions = {}

    asset_scanner = AssetScanner(
        assets_root=assets_root, project_root=project_root, mod_id=mod_id,
        models=models, blockstates=blockstates,
    )
    asset_result = asset_scanner.scan()
    item_definitions = asset_result.data.get("item_definitions", {})
    lang_files_by_locale = lang_result.data.get("files_by_locale", {})

    # -- entradas ---------------------------------------------------------
    registrations = reg_result.data.get("registrations", [])
    blocks_by_path = {
        r["path"]: r for r in registrations
        if r["type"] == "block" and r["method"] == "registerBlock"
    }
    block_items_by_path = {
        r["path"]: r for r in registrations
        if r["type"] == "item" and r["method"] == "registerSimpleBlockItem"
    }
    block_entities_by_path = {
        r["path"]: r for r in registrations if r["type"] == "block_entity"
    }
    menus_by_path = {r["path"]: r for r in registrations if r["type"] == "menu"}

    # Colisões reais de id: mesmo id E mesmo tipo a partir de fontes distintas.
    seen: dict[tuple[str, str], str] = {}
    for reg in registrations:
        if reg["type"] == "unknown":
            continue
        key = (reg["id"], reg["type"])
        if key in seen:
            reporter.error(
                f"colisão de IDs: {reg['id']} ({reg['type']}) registrado em "
                f"{seen[key]} e {reg['source_file']}:{reg['line']}",
            )
        else:
            seen[key] = f"{reg['source_file']}:{reg['line']}"

    entries: list[dict] = []
    for reg in registrations:
        if reg["type"] == "unknown":
            continue
        entry = _base_entry(reg)
        entry_type = reg["type"]

        if entry_type in ("item", "block", "entity", "creative_tab"):
            if entry_type == "item" and reg["method"] == "registerSimpleBlockItem":
                key = f"block.{reg['namespace']}.{reg['path']}"
            else:
                key = _translation_key(entry_type, reg["namespace"], reg["path"])
            entry["translation_key"] = key
            entry["translations"] = {}
            if key and language_index.has(key):
                entry["translations"] = language_index.values_for(key)
                entry["display_name"] = language_index.resolve(key)
                for locale in entry["translations"]:
                    lang_file = lang_files_by_locale.get(locale)
                    if lang_file:
                        entry["source_files"].append(lang_file)
            else:
                entry["warnings"].append(f"tradução ausente: {key or 'chave desconhecida'}")
                reporter.warning(
                    f"tradução ausente para entrada: {entry['id']}",
                    path=entry["id"],
                )
                reporter.note_missing_translation(entry["id"])

        if entry_type == "item":
            model_id = item_definitions.get(reg["path"]) or f"{mod_id}:item/{reg['path']}"
            entry["model"] = model_id
            entry["texture"] = _primary_texture(model_id, models)
            if reg["method"] == "registerSimpleBlockItem":
                block_id = reg.get("block_id")
                if block_id:
                    entry["block"] = f"{mod_id}:{block_id}"
                else:
                    entry["warnings"].append("referência de bloco não resolvida")
            if reg["path"] in item_definitions:
                entry["properties"]["item_definition"] = (
                    f"assets/{mod_id}/items/{reg['path']}.json"
                )

        elif entry_type == "block":
            blockstate_id = f"{mod_id}:{reg['path']}"
            entry["blockstate"] = blockstate_id
            bs_record = next((b for b in blockstates if b["id"] == blockstate_id), None)
            if bs_record and bs_record["model_refs"]:
                entry["model"] = sorted(bs_record["model_refs"])[0]
                entry["properties"]["variants"] = len(bs_record.get("variants", {}))
            else:
                entry["model"] = f"{mod_id}:block/{reg['path']}"
            entry["texture"] = _primary_texture(entry["model"], models)
            if reg["path"] in block_items_by_path:
                entry["item"] = f"{mod_id}:{reg['path']}"
            if reg["path"] in block_entities_by_path:
                entry["block_entity"] = f"{mod_id}:{reg['path']}"
            if reg["path"] in menus_by_path:
                entry["menu"] = f"{mod_id}:{reg['path']}"

        elif entry_type == "block_entity":
            if reg["path"] in blocks_by_path:
                entry["block"] = f"{mod_id}:{reg['path']}"

        elif entry_type == "menu":
            if reg["path"] in blocks_by_path:
                entry["block"] = f"{mod_id}:{reg['path']}"

        # Metadados do modelo associado.
        model_id = entry.get("model")
        if model_id and model_id in models:
            record = models[model_id]
            entry["properties"]["textures"] = record.get("textures", {})
            entry["properties"]["texture_files"] = record.get("texture_files", [])
            entry["properties"]["model_file"] = record.get("path")
            if record.get("parent"):
                entry["properties"]["parent"] = record["parent"]
            entry["source_files"].append(record["path"])
            entry["source_files"].extend(record.get("texture_files", []))

        entry["source_files"] = sorted(set(entry["source_files"]))
        entries.append(entry)

    # -- verificação de modelo/textura por entrada -------------------------
    for entry in entries:
        if entry["type"] not in ("item", "block"):
            continue
        model_id = entry.get("model")
        if not model_id:
            entry["warnings"].append("registro sem modelo")
            reporter.warning("registro sem modelo", path=entry["id"])
            reporter.note_missing_model(entry["id"])
            continue
        parsed_model = parse_resource_id(model_id)
        if parsed_model and parsed_model[0] == mod_id:
            model_file = assets_root / parsed_model[0] / "models" / f"{parsed_model[1]}.json"
            if not model_file.exists():
                entry["warnings"].append(f"modelo ausente: {model_id}")
                reporter.warning(f"modelo ausente: {model_id}", path=entry["id"])
                reporter.note_missing_model(entry["id"])
        texture_id = entry.get("texture")
        if texture_id:
            parsed_texture = parse_resource_id(texture_id)
            if parsed_texture and parsed_texture[0] == mod_id:
                texture_file = assets_root / parsed_texture[0] / "textures" / f"{parsed_texture[1]}.png"
                if not texture_file.exists():
                    entry["warnings"].append(f"textura ausente: {texture_id}")
                    reporter.warning(f"textura ausente: {texture_id}", path=entry["id"])
                    reporter.note_missing_texture(entry["id"])

    # -- cruzamento de referências -----------------------------------------
    recipes = recipe_result.data.get("recipes", [])
    tags = tag_result.data.get("tags", [])
    loot_tables = loot_result.data.get("loot_tables", [])
    for entry in entries:
        entry["recipes_as_result"] = sorted(
            r["id"] for r in recipes if r.get("result_item") == entry["id"]
        )
        entry["recipes_as_ingredient"] = sorted(
            r["id"] for r in recipes if entry["id"] in r.get("ingredient_items", [])
        )
        entry["tags"] = sorted(
            t["id"] for t in tags
            if entry["id"] in t.get("values_declared", [])
            or entry["id"] in t.get("values_resolved", [])
        )
        loot_ids = (
            [l["id"] for l in loot_tables if entry["id"] in l.get("item_refs", [])]
            if entry["type"] in ("item", "block") else []
        )
        if entry["type"] == "block":
            loot_ids.extend(
                l["id"] for l in loot_tables
                if l["namespace"] == entry["namespace"]
                and l.get("path") == f"blocks/{entry['path']}"
            )
        entry["loot_tables"] = sorted(set(loot_ids))

    # -- assets órfãos ------------------------------------------------------
    expected_model_refs = {
        e["model"] for e in entries if e.get("model")
    }
    orphans = asset_scanner.find_orphans(expected_model_refs)
    for model_id in orphans["orphan_models"]:
        reporter.warning(f"modelo órfão: {model_id}")
    for texture_rel in orphans["orphan_textures"]:
        reporter.warning(f"textura sem conteúdo registrado: {texture_rel}")
    for model_id in asset_result.data.get("models_without_texture", []):
        reporter.warning(f"modelo sem textura: {model_id}")

    missing_blockstate_models = asset_result.data.get("missing_blockstate_models", [])
    for ref in missing_blockstate_models:
        reporter.warning(f"modelo referenciado por blockstate não encontrado: {ref}")

    broken_texture_refs = asset_result.data.get("broken_texture_refs", [])
    for ref in broken_texture_refs:
        reporter.warning(f"referência de textura quebrada: {ref}")

    # -- dados de geração e diagnóstico do catálogo -------------------------
    _merge_diagnostics(reporter, (
        reg_result, lang_result, model_result, bs_result, asset_result,
        recipe_result, tag_result, loot_result,
    ))

    warnings_list: list[dict] = []
    errors_list: list[dict] = []
    for issue in reporter.issues:
        item = {
            "severity": issue.severity,
            "message": issue.message,
            "path": issue.path,
            "context": issue.context,
        }
        if issue.severity == "error":
            errors_list.append(item)
        else:
            warnings_list.append(item)

    ignored_files = _collect_ignored_files(project_root, mod_id, assets_root, data_root)

    languages = lang_result.coverage.get("locales", [])
    broken_references = sorted(set(
        broken_texture_refs + missing_blockstate_models
        + model_result.data.get("missing_parents", [])
    ))
    orphan_assets = sorted(set(orphans["orphan_models"]) | set(orphans["orphan_textures"]))

    scanner_coverage = {
        "registry": reg_result.coverage,
        "language": lang_result.coverage,
        "model": model_result.coverage,
        "blockstate": bs_result.coverage,
        "asset": asset_result.coverage,
        "recipe": recipe_result.coverage,
        "tag": tag_result.coverage,
        "loot_table": loot_result.coverage,
    }

    generation = {
        "generator": "novadyne-wiki",
        "schema_version": CatalogBuilder.SCHEMA_VERSION,
        "mod_version": mod_info.get("version"),
        "languages": languages,
        "counts": {
            "entries": len(entries),
            "recipes": len(recipes),
            "tags": len(tags),
        },
        "scanners": scanner_coverage,
        "broken_references": broken_references,
        "orphan_assets": orphan_assets,
        "unknown_recipe_types": recipe_result.data.get("unknown_types", []),
    }

    catalog = CatalogBuilder().build(
        mod=mod_info,
        entries=entries,
        recipes=recipes,
        tags=tags,
        diagnostics={"warnings": warnings_list, "errors": errors_list},
        generation=generation,
    )

    scan_summary = {
        "scanner_coverage": scanner_coverage,
        "ignored_files": ignored_files,
        "unresolved_registrations": reg_result.data.get("unresolved", []),
    }
    return catalog, scan_summary
