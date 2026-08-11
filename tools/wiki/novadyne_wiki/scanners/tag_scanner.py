"""Resolução de tags (data/*/tags/**/*.json) — Fase 3.

Cada tag mantém os valores declarados e, quando possível, os valores
resolvidos (expansão das referências ``#namespace:path``). A expansão é
protegida contra ciclos. Referências a tags do próprio escopo que não
existem são quebradas; referências externas (ex.: ``minecraft:``) são
apenas anotadas como não verificáveis.
"""

from __future__ import annotations

from pathlib import Path

from ..errors import Issue
from ..io_utils import iter_files
from .common import ScanResult, load_json_file, parse_resource_id, to_posix


class TagScanner:
    """Varre data/*/tags/** e normaliza cada tag encontrada."""

    def __init__(self, *, data_root, project_root, reporter=None):
        self.data_root = Path(data_root)
        self.project_root = Path(project_root)
        self.reporter = reporter

    def scan(self) -> ScanResult:
        result = ScanResult()
        tags: list[dict] = []
        source_files: list[str] = []
        files_scanned = 0

        for path in iter_files(self.data_root, suffixes=(".json",)):
            rel_path = path.relative_to(self.data_root)
            parts = rel_path.parts
            if len(parts) < 3 or parts[1] != "tags":
                continue
            files_scanned += 1
            rel = to_posix(path.relative_to(self.project_root))
            namespace = parts[0]
            registry = parts[2]
            tag_path = Path(*parts[3:]).with_suffix("").as_posix()
            source_files.append(rel)

            data, err = load_json_file(path)
            if err is not None:
                result.diagnostics.append(Issue("error", f"tag inválida: {err}", path=rel))
                continue
            if not isinstance(data, dict):
                result.diagnostics.append(Issue(
                    "error", "tag inválida: esperado um objeto JSON", path=rel))
                continue

            values_declared: list[str] = []
            tag_refs: list[str] = []
            raw_values = data.get("values")
            if isinstance(raw_values, list):
                for value in raw_values:
                    if not isinstance(value, str):
                        continue
                    stripped = value.strip()
                    if stripped.startswith("#"):
                        tag_id = stripped[1:]
                        if parse_resource_id(tag_id):
                            tag_refs.append(tag_id)
                    else:
                        values_declared.append(stripped)

            replace = data.get("replace")
            required = data.get("required")

            tags.append({
                "id": f"{namespace}:{tag_path}",
                "namespace": namespace,
                "registry": registry,
                "path": tag_path,
                "source_file": rel,
                "replace": replace if isinstance(replace, bool) else None,
                "required": required if isinstance(required, bool) else None,
                "values_declared": sorted(set(values_declared)),
                "tag_refs": sorted(set(tag_refs)),
                "missing_refs": [],
                "cycle": [],
                "values_resolved": [],
            })

        tags = sorted(tags, key=lambda t: t["id"])
        by_id = {t["id"]: t for t in tags}
        scanned_namespaces = {t["namespace"] for t in tags}

        # Referências ausentes (apenas dentro do escopo varrido).
        for tag in tags:
            missing = []
            for ref in tag["tag_refs"]:
                parsed = parse_resource_id(ref)
                if parsed is None:
                    continue
                ns, ref_path = parsed
                if ns in scanned_namespaces and f"{ns}:{ref_path}" not in by_id:
                    missing.append(ref)
            tag["missing_refs"] = sorted(set(missing))

        # Ciclos (DFS com proteção; um diagnóstico por ciclo único).
        seen_cycles: set[tuple[str, ...]] = set()
        for tag in tags:
            cycle = self._find_cycle(tag["id"], by_id)
            if not cycle:
                continue
            canonical = self._canonical_cycle(cycle)
            if canonical in seen_cycles:
                continue
            seen_cycles.add(canonical)
            for member_id in canonical:
                if member_id in by_id:
                    by_id[member_id]["cycle"] = list(canonical)
            result.diagnostics.append(Issue(
                "warning",
                f"ciclo de tags: {' -> '.join(canonical)}",
                path=tag["source_file"],
            ))

        # Valores resolvidos (expansão protegida contra ciclos).
        for tag in tags:
            tag["values_resolved"] = sorted(
                self._resolve(tag["id"], by_id, set()))

        result.data = {
            "tags": tags,
            "source_files": sorted(source_files),
            "cycles": sorted({tuple(cycle) for cycle in seen_cycles}),
        }
        result.coverage = {
            "files_scanned": files_scanned,
            "tags_found": len(tags),
        }
        return result

    def _resolve(self, tag_id: str, by_id: dict, stack: set[str]) -> set[str]:
        """Expande uma tag em valores diretos, sem revisitar ciclos."""
        if tag_id in stack:
            return set()
        tag = by_id.get(tag_id)
        if tag is None:
            return set()
        result = set(tag["values_declared"])
        for ref in tag["tag_refs"]:
            parsed = parse_resource_id(ref)
            if parsed is None:
                continue
            result |= self._resolve(f"{parsed[0]}:{parsed[1]}", by_id, stack | {tag_id})
        return result

    @staticmethod
    def _find_cycle(start_id: str, by_id: dict) -> list[str] | None:
        """Retorna o ciclo que passa por start_id, ou None."""
        visited: set[str] = set()

        def dfs(node: str, path: list[str]):
            if node in path:
                index = path.index(node)
                return path[index:] + [node]
            if node in visited:
                return None
            visited.add(node)
            tag = by_id.get(node)
            if not tag:
                return None
            for ref in tag["tag_refs"]:
                parsed = parse_resource_id(ref)
                if parsed is None:
                    continue
                cycle = dfs(f"{parsed[0]}:{parsed[1]}", path + [node])
                if cycle:
                    return cycle
            return None

        return dfs(start_id, [])

    @staticmethod
    def _canonical_cycle(cycle: list[str]) -> tuple[str, ...]:
        """Normaliza o ciclo (rotação para o menor elemento) para deduplicar."""
        if not cycle:
            return ()
        smallest = min(cycle)
        index = cycle.index(smallest)
        return tuple(cycle[index:-1] + cycle[:index] + [smallest])
