"""Descoberta de blockstates (assets/<mod>/blockstates/*.json) — Fase 3.

Lê as variantes (``facing=north`` → modelo) e multiparts, coletando as
referências de modelo. A existência dos modelos referenciados é verificada
pelo AssetScanner (que tem o índice de modelos).
"""

from __future__ import annotations

from pathlib import Path

from ..errors import Issue
from ..io_utils import iter_files
from .common import ScanResult, load_json_file, to_posix


class BlockstateScanner:
    """Varre a pasta blockstates/ e normaliza cada blockstate encontrado."""

    def __init__(self, *, assets_root, project_root, mod_id, reporter=None):
        self.assets_root = Path(assets_root)
        self.project_root = Path(project_root)
        self.mod_id = mod_id
        self.reporter = reporter

    def scan(self) -> ScanResult:
        result = ScanResult()
        blockstates_dir = self.assets_root / self.mod_id / "blockstates"
        blockstates: list[dict] = []
        source_files: list[str] = []
        files_scanned = 0

        for path in iter_files(blockstates_dir, suffixes=(".json",)):
            files_scanned += 1
            rel = to_posix(path.relative_to(self.project_root))
            source_files.append(rel)
            data, err = load_json_file(path)
            if err is not None:
                result.diagnostics.append(Issue("error", f"blockstate inválido: {err}", path=rel))
                continue
            if not isinstance(data, dict):
                result.diagnostics.append(Issue(
                    "error", "blockstate inválido: esperado um objeto JSON", path=rel))
                continue

            model_refs: set[str] = set()
            variants: dict[str, dict] = {}
            multipart: list[dict] = []

            raw_variants = data.get("variants")
            if isinstance(raw_variants, dict):
                for state, variant in raw_variants.items():
                    if not isinstance(variant, dict):
                        continue
                    model = variant.get("model")
                    if isinstance(model, str):
                        model_refs.add(model)
                        variants[state] = {
                            key: variant[key]
                            for key in ("model", "x", "y", "uvlock")
                            if key in variant
                        }

            raw_multipart = data.get("multipart")
            if isinstance(raw_multipart, list):
                for part in raw_multipart:
                    if not isinstance(part, dict):
                        continue
                    apply_ = part.get("apply")
                    refs: list[str] = []
                    if isinstance(apply_, dict) and isinstance(apply_.get("model"), str):
                        refs.append(apply_["model"])
                    elif isinstance(apply_, list):
                        for entry in apply_:
                            if isinstance(entry, dict) and isinstance(entry.get("model"), str):
                                refs.append(entry["model"])
                    model_refs.update(refs)
                    multipart.append({"when": part.get("when"), "model_refs": sorted(set(refs))})

            blockstates.append({
                "id": f"{self.mod_id}:{path.stem}",
                "path": rel,
                "variants": dict(sorted(variants.items())),
                "multipart": multipart,
                "model_refs": sorted(model_refs),
            })

        result.data = {
            "blockstates": sorted(blockstates, key=lambda b: b["id"]),
            "source_files": sorted(source_files),
        }
        result.coverage = {
            "files_scanned": files_scanned,
            "blockstates_found": len(blockstates),
        }
        return result
