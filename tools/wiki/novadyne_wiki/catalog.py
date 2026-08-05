"""Construção do catálogo intermediário (build/wiki/catalog.json).

Na Fase 2 o catálogo nasce vazio (schema + estrutura). As Fases 3+ preenchem
`entries` e `recipes` a partir dos scanners. A saída é determinística:
nenhum timestamp ou dado dependente de ordem de sistema de arquivos.
"""

from __future__ import annotations

import json

from .io_utils import write_text_atomic


class CatalogBuilder:
    """Monta o dicionário normalizado do catálogo.

    O campo `sources` documenta a procedência de cada dado (adicionado por
    cada scanner nas fases seguintes).
    """

    SCHEMA_VERSION = 1

    def __init__(self, reporter):
        self.reporter = reporter

    def build(self) -> dict:
        return {
            "schema": self.SCHEMA_VERSION,
            "generator": "novadyne-wiki",
            "entries": [],
            "recipes": [],
        }


def write_catalog(catalog: dict, path) -> None:
    """Serializa o catálogo em UTF-8, ordenado e determinístico."""
    write_text_atomic(
        path,
        json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
