"""Índice de assets (texturas, definições de item) e diagnósticos — Fase 3.

Usa os resultados do ModelScanner e do BlockstateScanner para verificar:

- modelos referenciados por blockstates que não existem;
- texturas locais referenciadas por modelos que não existem;
- modelos órfãos (não referenciados por blockstate, definição de item,
  pai de outro modelo ou pelo conjunto esperado de entradas);
- texturas órfãs de item/bloco (provável conteúdo planejado);
- modelos sem textura (sem ``textures``, sem ``elements`` e sem pai).

Texturas de GUI, partículas, entidades etc. nunca são marcadas
automaticamente como órfãs: apenas as categorias item e bloco são avaliadas.
"""

from __future__ import annotations

from pathlib import Path

from ..errors import Issue
from ..io_utils import iter_files
from .common import ScanResult, load_json_file, parse_resource_id, to_posix

_ORPHAN_CANDIDATE_CATEGORIES = ("item", "block")


class AssetScanner:
    """Cruza modelos, blockstates, texturas e definições de item."""

    def __init__(self, *, assets_root, project_root, mod_id, models=None,
                 blockstates=None, expected_model_refs=None, reporter=None):
        self.assets_root = Path(assets_root)
        self.project_root = Path(project_root)
        self.mod_id = mod_id
        self.models: dict[str, dict] = models or {}
        self.blockstates: list[dict] = blockstates or []
        self.expected_model_refs: set[str] = set(expected_model_refs or [])
        self.reporter = reporter

    def scan(self) -> ScanResult:
        result = ScanResult()
        textures_dir = self.assets_root / self.mod_id / "textures"

        texture_files: dict[str, str] = {}  # path rel (repo) -> categoria
        for path in iter_files(textures_dir, suffixes=(".png", ".mcmeta")):
            rel = to_posix(path.relative_to(self.project_root))
            rel_textures = path.relative_to(textures_dir)
            category = rel_textures.parts[0] if rel_textures.parts else ""
            texture_files[rel] = category
        self._texture_category_map = dict(texture_files)

        item_definitions: dict[str, str] = {}
        item_definition_files: list[str] = []
        items_dir = self.assets_root / self.mod_id / "items"
        for path in iter_files(items_dir, suffixes=(".json",)):
            rel = to_posix(path.relative_to(self.project_root))
            item_definition_files.append(rel)
            data, err = load_json_file(path)
            if err is not None:
                result.diagnostics.append(Issue("error", f"definição de item inválida: {err}", path=rel))
                continue
            model = data.get("model") if isinstance(data, dict) else None
            if isinstance(model, dict) and isinstance(model.get("model"), str):
                item_definitions[path.stem] = model["model"]

        # Modelos referenciados por blockstates que não existem.
        missing_blockstate_models: list[str] = []
        for blockstate in self.blockstates:
            for ref in blockstate["model_refs"]:
                parsed = parse_resource_id(ref)
                if parsed and parsed[0] == self.mod_id:
                    model_file = self.assets_root / parsed[0] / "models" / f"{parsed[1]}.json"
                    if not model_file.exists():
                        missing_blockstate_models.append(ref)

        # Referências de textura quebradas (já sinalizadas pelo ModelScanner).
        broken_texture_refs: list[str] = []
        for model in self.models.values():
            broken_texture_refs.extend(model.get("missing_textures", []))
        broken_texture_refs = sorted(set(broken_texture_refs))

        # Modelos sem textura: sem textures, sem elements e sem pai.
        models_without_texture: list[str] = []
        for model_id, model in self.models.items():
            if (not model.get("textures") and not model.get("has_elements")
                    and not model.get("parent")):
                models_without_texture.append(model_id)

        result.data = {
            "texture_files": dict(sorted(texture_files.items())),
            "item_definitions": dict(sorted(item_definitions.items())),
            "item_definition_files": sorted(item_definition_files),
            "missing_blockstate_models": missing_blockstate_models,
            "broken_texture_refs": broken_texture_refs,
            "models_without_texture": sorted(models_without_texture),
            "orphan_models": [],
            "orphan_textures": [],
        }
        result.coverage = {
            "texture_files": len(texture_files),
            "item_definitions": len(item_definitions),
            "models_checked": len(self.models),
            "blockstates_checked": len(self.blockstates),
        }
        return result

    def find_orphans(self, expected_model_refs: set[str]) -> dict:
        """Detecta modelos e texturas órfãs.

        ``expected_model_refs`` é o conjunto de modelos usados pelas entradas
        do catálogo (computado pelo pipeline depois de montar as entradas).
        """
        used_models: set[str] = set(expected_model_refs)

        for blockstate in self.blockstates:
            for ref in blockstate["model_refs"]:
                parsed = parse_resource_id(ref)
                if parsed and parsed[0] == self.mod_id:
                    used_models.add(ref)

        for model in self.models.values():
            parent = model.get("parent")
            parsed = parse_resource_id(parent) if parent else None
            if parsed and parsed[0] == self.mod_id:
                used_models.add(parent)

        orphan_models = sorted(
            model_id for model_id in self.models if model_id not in used_models
        )

        used_textures: set[str] = set()
        for model in self.models.values():
            used_textures.update(model.get("texture_files", []))

        orphan_textures: list[str] = []
        for rel, category in self._texture_category_map.items():
            if category not in _ORPHAN_CANDIDATE_CATEGORIES:
                continue
            if rel not in used_textures:
                orphan_textures.append(rel)

        return {
            "orphan_models": orphan_models,
            "orphan_textures": sorted(orphan_textures),
        }

    def texture_categories(self) -> dict[str, str]:
        return dict(getattr(self, "_texture_category_map", {}))
