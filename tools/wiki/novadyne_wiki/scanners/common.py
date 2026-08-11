"""Utilitários compartilhados entre os scanners (Fase 3).

Centraliza a carga segura de JSON, a normalização de caminhos POSIX e o
resultado padrão de um scanner (dados + diagnósticos + arquivos ignorados +
cobertura). Nenhum caminho absoluto é produzido: tudo é relativo às raízes
de varredura informadas.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from ..errors import Issue

# "novadyne:item/pure_silicon" ou "minecraft:iron_ingot"
_RESOURCE_ID_RE = re.compile(r"^([a-z0-9_.-]+):([a-z0-9_./-]+)$")


@dataclass
class ScanResult:
    """Resultado de um scanner: dados normalizados, diagnósticos e cobertura.

    - ``data``: dicionário com o conteúdo descoberto (determinístico).
    - ``diagnostics``: avisos/erros (Issue) associados a arquivos.
    - ``ignored``: arquivos deliberadamente ignorados e o motivo.
    - ``coverage``: métricas aproximadas (arquivos varridos, itens achados).
    """

    data: dict = field(default_factory=dict)
    diagnostics: list[Issue] = field(default_factory=list)
    ignored: list[dict] = field(default_factory=list)
    coverage: dict = field(default_factory=dict)


def to_posix(value: str | Path) -> str:
    """Converte um caminho para separadores POSIX ('/').

    Garante a mesma saída em Windows e Linux.
    """
    if isinstance(value, Path):
        return value.as_posix()
    return str(value).replace("\\", "/")


def parse_resource_id(value: str) -> tuple[str, str] | None:
    """Divide 'novadyne:item/pure_silicon' em (namespace, path).

    Retorna None para valores que não são IDs de recurso válidos.
    """
    match = _RESOURCE_ID_RE.match(value.strip())
    if not match:
        return None
    return match.group(1), match.group(2)


def load_json_file(path: Path) -> tuple[object | None, str | None]:
    """Carrega um JSON UTF-8 (aceita e remove BOM quando presente).

    Retorna (dados, None) em caso de sucesso ou (None, mensagem) em erro.
    Nunca levanta exceção para JSON inválido — o scanner decide o que fazer.
    """
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return None, f"não foi possível ler o arquivo: {exc}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"JSON inválido (linha {exc.lineno}, coluna {exc.colno}): {exc.msg}"
