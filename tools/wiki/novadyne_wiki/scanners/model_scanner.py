"""Descoberta de modelos (assets/<mod>/models/**/*.json) — Fase 3.

Lê cada modelo JSON, identifica o pai, as texturas declaradas e resolve as
referências locais de textura (``novadyne:item/x`` → ``textures/item/x.png``).
Referências ao namespace ``minecraft`` não são verificáveis aqui e são
marcadas como externas (não geram warning).
"""

from __future__ import annotations

from pathlib import Path

from ..errors import Issue
from ..io_utils import iter_files
from .common import ScanResult, load_json_file, parse_resource_id, to_posix


class ModelScanner:
    """Varre a pasta models/ e normaliza cada modelo encontrado."""

    def __init__(self, *, assets_root, project_root, mod_id, reporter=None):
        self.assets_root = Path(assets_root)
        self.project_root = Path(project_root)
        self.mod_id = mod_id
        self.reporter = reporter

    def scan(self) -> ScanResult:
        result = ScanResult()
        models_dir = self.assets_root / self.mod_id / "models"
        models: dict[str, dict] = {}
        missing_textures: set[str] = set()
        missing_parents: set[str] = set()
        source_files: list[str] = []
        files_scanned = 0

        for path in iter_files(models_dir, suffixes=(".json",)):
            files_scanned += 1
            rel = to_posix(path.relative_to(self.project_root))
            source_files.append(rel)
            rel_models = path.relative_to(models_dir)
            model_id = f"{self.mod_id}:{rel_models.with_suffix('').as_posix()}"

            data, err = load_json_file(path)
            if err is not None:
                result.diagnostics.append(Issue("error", f"modelo inválido: {err}", path=rel))
                continue
            if not isinstance(data, dict):
                result.diagnostics.append(Issue(
                    "error", "modelo inválido: esperado um objeto JSON", path=rel))
                continue

            raw_textures = data.get("textures")
            textures: dict[str, str] = {}
            if isinstance(raw_textures, dict):
                for var, ref in raw_textures.items():
                    if isinstance(var, str) and isinstance(ref, str):
                        textures[var] = ref

            parent = data.get("parent")
            if not isinstance(parent, str):
                parent = None

            elements = data.get("elements")
            has_elements = isinstance(elements, list) and len(elements) > 0

            record: dict = {
                "id": model_id,
                "path": rel,
                "parent": parent,
                "textures": textures,
                "has_elements": has_elements,
                "texture_refs": [],
                "texture_files": [],
                "external_textures": [],
                "missing_textures": [],
                "missing_parents": [],
            }

            for _var, ref in sorted(textures.items()):
                parsed = parse_resource_id(ref)
                if parsed is None:
                    continue
                ns, tex_path = parsed
                if ns != self.mod_id:
                    record["external_textures"].append(ref)
                    continue
                record["texture_refs"].append(ref)
                tex_file = self.assets_root / ns / "textures" / f"{tex_path}.png"
                if tex_file.exists():
                    record["texture_files"].append(to_posix(tex_file.relative_to(self.project_root)))
                else:
                    record["missing_textures"].append(ref)
                    missing_textures.add(ref)

            if parent:
                parsed_parent = parse_resource_id(parent)
                if parsed_parent and parsed_parent[0] == self.mod_id:
                    ns, parent_path = parsed_parent
                    parent_file = self.assets_root / ns / "models" / f"{parent_path}.json"
                    if not parent_file.exists():
                        record["missing_parents"].append(parent)
                        missing_parents.add(parent)

            models[model_id] = record

        result.data = {
            "models": dict(sorted(models.items())),
            "missing_textures": sorted(missing_textures),
            "missing_parents": sorted(missing_parents),
            "source_files": sorted(source_files),
        }
        result.coverage = {
            "files_scanned": files_scanned,
            "models_found": len(models),
        }
        return result
