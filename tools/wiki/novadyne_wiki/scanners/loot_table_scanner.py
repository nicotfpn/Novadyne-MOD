"""Leitura conservadora de loot tables (data/*/loot_table/**/*.json) — Fase 3.

Registra arquivo, tipo, pools, referências diretas identificáveis (entries
``minecraft:item``), condições e construções não suportadas. Não simula
condições de loot. A associação a entradas do catálogo é feita pelo pipeline
somente por caminho (``blocks/<nome>``) ou referência explícita de item.
"""

from __future__ import annotations

from pathlib import Path

from ..errors import Issue
from ..io_utils import iter_files
from .common import ScanResult, load_json_file, to_posix


class LootTableScanner:
    """Varre data/*/loot_table/** e normaliza cada loot table encontrada."""

    def __init__(self, *, data_root, project_root, reporter=None):
        self.data_root = Path(data_root)
        self.project_root = Path(project_root)
        self.reporter = reporter

    def scan(self) -> ScanResult:
        result = ScanResult()
        loot_tables: list[dict] = []
        source_files: list[str] = []
        files_scanned = 0

        for path in iter_files(self.data_root, suffixes=(".json",)):
            rel_path = path.relative_to(self.data_root)
            parts = rel_path.parts
            if len(parts) < 3 or parts[1] != "loot_table":
                continue
            files_scanned += 1
            rel = to_posix(path.relative_to(self.project_root))
            namespace = parts[0]
            loot_path = Path(*parts[2:]).with_suffix("").as_posix()
            source_files.append(rel)

            data, err = load_json_file(path)
            if err is not None:
                result.diagnostics.append(Issue("error", f"loot table inválida: {err}", path=rel))
                continue
            if not isinstance(data, dict):
                result.diagnostics.append(Issue(
                    "error", "loot table inválida: esperado um objeto JSON", path=rel))
                continue

            item_refs: set[str] = set()
            conditions: set[str] = set()
            rolls: list[object] = []
            unsupported: list[dict] = []
            pool_count = 0

            pools = data.get("pools")
            if isinstance(pools, list):
                pool_count = len(pools)
                for pool in pools:
                    if not isinstance(pool, dict):
                        continue
                    rolls.append(pool.get("rolls"))
                    self._collect_conditions(pool.get("conditions"), conditions)
                    entries = pool.get("entries")
                    if not isinstance(entries, list):
                        continue
                    for entry in entries:
                        if not isinstance(entry, dict):
                            continue
                        self._collect_conditions(entry.get("conditions"), conditions)
                        entry_type = entry.get("type")
                        name = entry.get("name")
                        if isinstance(entry_type, str) and isinstance(name, str):
                            if entry_type == "minecraft:item":
                                item_refs.add(name)
                            else:
                                unsupported.append({"type": entry_type, "name": name})

            loot_type = data.get("type")
            loot_tables.append({
                "id": f"{namespace}:{loot_path}",
                "namespace": namespace,
                "path": loot_path,
                "type": loot_type if isinstance(loot_type, str) else None,
                "source_file": rel,
                "pools": pool_count,
                "rolls": rolls,
                "item_refs": sorted(item_refs),
                "conditions": sorted(conditions),
                "unsupported": unsupported,
                "raw": {k: v for k, v in data.items() if k != "pools"},
            })

        result.data = {
            "loot_tables": sorted(loot_tables, key=lambda l: l["id"]),
            "source_files": sorted(source_files),
        }
        result.coverage = {
            "files_scanned": files_scanned,
            "loot_tables_found": len(loot_tables),
        }
        return result

    @staticmethod
    def _collect_conditions(raw, conditions: set[str]) -> None:
        if not isinstance(raw, list):
            return
        for condition in raw:
            if isinstance(condition, dict) and isinstance(condition.get("condition"), str):
                conditions.add(condition["condition"])
