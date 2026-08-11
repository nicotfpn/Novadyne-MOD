"""Descoberta conservadora de registros NeoForge em Java (Fase 3).

Detecta apenas os padrões reais encontrados no projeto:

- ``DeferredRegister.createItems / createBlocks / createDataComponents``
- ``DeferredRegister.create(Registries.X, ...)``
- ``ITEMS.registerSimpleItem("id")``
- ``ITEMS.registerSimpleBlockItem("id", ModBlocks.X)``
- ``BLOCKS.registerBlock("id", Clazz::new, ...)``
- ``REGISTRY.register("id", ...)``

Não é um parser completo de Java: padrões fora desta lista geram diagnóstico
em vez de suposição. A variável de registro é validada contra a declaração
``DeferredRegister`` do próprio arquivo — nome de variável sozinho não é
prova de tipo.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..errors import Issue
from ..io_utils import iter_files
from .common import ScanResult, to_posix

# Registro simples: VAR.registerSimpleItem("id") ou VAR.register("id")
_CALL_RE = re.compile(
    r"([A-Z][A-Z0-9_]*)\s*\.\s*(registerSimpleItem|registerBlock|register)"
    r"\s*\(\s*\"([^\"]+)\""
)

# Item de bloco: VAR.registerSimpleBlockItem("id", ModBlocks.CONST)
_BLOCK_ITEM_RE = re.compile(
    r"([A-Z][A-Z0-9_]*)\s*\.\s*registerSimpleBlockItem\s*\(\s*\"([^\"]+)\"\s*,"
    r"\s*([A-Z]\w*(?:\.[A-Z][A-Z0-9_]*)?)\s*\)"
)

# Declaração de constante: "final ... NOME = ..." (pode continuar na linha seguinte)
_DECL_RE = re.compile(r"\bfinal\s+[\w?<>,.\s]*\s+([A-Z][A-Z0-9_]*)\s*=\s*(.*)$")

# Tipo de registro por declaração DeferredRegister (var -> tipo)
_REGISTRY_DECL_RES = [
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.createItems\b"), "item"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.createBlocks\b"), "block"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.createDataComponents\b"), "data_component"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.create\s*\(\s*Registries\.BLOCK_ENTITY_TYPE\b"), "block_entity"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.create\s*\(\s*Registries\.MENU\b"), "menu"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.create\s*\(\s*Registries\.CREATIVE_MODE_TAB\b"), "creative_tab"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.create\s*\(\s*Registries\.ENTITY_TYPE\b"), "entity"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.create\s*\(\s*Registries\.ITEM\b"), "item"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.create\s*\(\s*Registries\.BLOCK\b"), "block"),
    (re.compile(r"(\w+)\s*=\s*DeferredRegister\.create\s*\(\s*Registries\.DATA_COMPONENT_TYPE\b"), "data_component"),
]

# Forma tipada: DeferredRegister.Items ITEMS = ...
_TYPED_DECL_RES = [
    (re.compile(r"DeferredRegister\.Items\s+([A-Z][A-Z0-9_]*)\s*="), "item"),
    (re.compile(r"DeferredRegister\.Blocks\s+([A-Z][A-Z0-9_]*)\s*="), "block"),
    (re.compile(r"DeferredRegister\.DataComponents\s+([A-Z][A-Z0-9_]*)\s*="), "data_component"),
]

_QUALIFIED_REF_RE = re.compile(r"([A-Z]\w*)\.([A-Z][A-Z0-9_]*)")


def _registry_types(text: str) -> dict[str, str]:
    """Mapeia a variável do DeferredRegister para o tipo de registro no arquivo."""
    mapping: dict[str, str] = {}
    for pattern, reg_type in _REGISTRY_DECL_RES:
        for match in pattern.finditer(text):
            mapping[match.group(1)] = reg_type
    for pattern, reg_type in _TYPED_DECL_RES:
        for match in pattern.finditer(text):
            mapping[match.group(1)] = reg_type
    return mapping


class RegistryScanner:
    """Varre arquivos Java por registros NeoForge comprováveis."""

    def __init__(self, *, java_root, project_root, mod_id, reporter=None):
        self.java_root = Path(java_root)
        self.project_root = Path(project_root)
        self.mod_id = mod_id
        self.reporter = reporter

    def scan(self) -> ScanResult:
        result = ScanResult()
        registrations: list[dict] = []
        constants_by_file: dict[str, dict[str, str]] = {}
        files_scanned = 0
        unresolved: list[str] = []

        for path in iter_files(self.java_root, suffixes=(".java",)):
            files_scanned += 1
            rel = to_posix(path.relative_to(self.project_root))
            text = path.read_text(encoding="utf-8", errors="replace")
            var_types = _registry_types(text)

            constants: dict[str, str] = {}
            pending: str | None = None
            for lineno, line in enumerate(text.splitlines(), 1):
                decl = _DECL_RE.search(line)
                if decl:
                    pending = decl.group(1)
                    scan_text = decl.group(2)
                else:
                    scan_text = line

                for match in _CALL_RE.finditer(scan_text):
                    var, method, reg_id = match.group(1), match.group(2), match.group(3)
                    reg_type = var_types.get(var, "unknown")
                    self._append(reg_id, reg_type, var, method, pending, block_ref=None,
                                 rel=rel, lineno=lineno, constants=constants,
                                 registrations=registrations, unresolved=unresolved,
                                 diagnostics=result.diagnostics)
                    pending = None

                for match in _BLOCK_ITEM_RE.finditer(scan_text):
                    var, reg_id, block_ref = match.group(1), match.group(2), match.group(3)
                    reg_type = var_types.get(var, "unknown")
                    self._append(reg_id, reg_type, var, "registerSimpleBlockItem", pending,
                                 block_ref=block_ref, rel=rel, lineno=lineno,
                                 constants=constants, registrations=registrations,
                                 unresolved=unresolved, diagnostics=result.diagnostics)
                    pending = None

                if not decl and line.rstrip().endswith(";"):
                    pending = None

            constants_by_file[Path(rel).stem] = constants

        for reg in registrations:
            if reg["method"] != "registerSimpleBlockItem":
                continue
            block_id = self._resolve_block_ref(reg["block_ref"], constants_by_file)
            reg["block_id"] = block_id
            if block_id is None:
                result.diagnostics.append(Issue(
                    "warning",
                    f"referência de bloco não resolvida para item de bloco: {reg['block_ref']}",
                    path=reg["source_file"],
                    context=f"linha {reg['line']}",
                ))

        result.data = {
            "mod_id": self.mod_id,
            "registrations": sorted(registrations, key=lambda r: (r["id"], r["type"])),
            "constants_by_file": constants_by_file,
            "unresolved": sorted(set(unresolved)),
        }
        result.coverage = {
            "files_scanned": files_scanned,
            "registrations_found": len(registrations),
        }
        return result

    def _append(self, reg_id, reg_type, var, method, constant, *, block_ref,
                rel, lineno, constants, registrations, unresolved, diagnostics):
        if reg_type == "unknown":
            unresolved.append(reg_id)
            diagnostics.append(Issue(
                "warning",
                f"registro não classificado (variável de registro desconhecida: {var})",
                path=rel,
                context=f"linha {lineno}",
            ))
        if constant is not None:
            constants[constant] = reg_id
        registrations.append({
            "id": reg_id,
            "namespace": self.mod_id,
            "path": reg_id,
            "type": reg_type,
            "method": method,
            "constant": constant,
            "source_file": rel,
            "line": lineno,
            "block_ref": block_ref,
            "block_id": None,
        })

    @staticmethod
    def _resolve_block_ref(ref: str | None, constants_by_file: dict[str, dict[str, str]]) -> str | None:
        if not ref:
            return None
        match = _QUALIFIED_REF_RE.match(ref)
        if not match:
            return None
        stem, const = match.group(1), match.group(2)
        return constants_by_file.get(stem, {}).get(const)
