"""Construção do catálogo intermediário (build/wiki/catalog.json) — Fase 3.

O catálogo é um documento determinístico (sem timestamps) com schema
versionado:

- ``schema`` / ``schema_version``: versão do schema (1);
- ``mod``: metadados do mod (gradle.properties);
- ``entries``: entradas normalizadas (itens, blocos, BEs, menus, abas...);
- ``recipes``: receitas normalizadas;
- ``tags``: tags com valores declarados e resolvidos;
- ``diagnostics``: avisos/erros dos scanners;
- ``generation``: cobertura aproximada por scanner e contagens.

Toda saída é ordenada de forma estável e serializada em UTF-8.
"""

from __future__ import annotations

import json

from .io_utils import write_text_atomic


def _sorted_entries(entries: list[dict]) -> list[dict]:
    return sorted(entries, key=lambda e: (e.get("id", ""), e.get("type", "")))


def _sorted_recipes(recipes: list[dict]) -> list[dict]:
    return sorted(recipes, key=lambda r: r.get("id", ""))


def _sorted_tags(tags: list[dict]) -> list[dict]:
    return sorted(tags, key=lambda t: t.get("id", ""))


def _sorted_issues(issues: list[dict]) -> list[dict]:
    return sorted(issues, key=lambda i: (i.get("path") or "", i.get("message", "")))


class CatalogBuilder:
    """Monta o dicionário normalizado do catálogo."""

    SCHEMA_VERSION = 1

    def __init__(self, reporter=None):
        self.reporter = reporter

    def build(
        self,
        *,
        mod: dict | None = None,
        entries: list[dict] | None = None,
        recipes: list[dict] | None = None,
        tags: list[dict] | None = None,
        diagnostics: dict | None = None,
        generation: dict | None = None,
    ) -> dict:
        diagnostics = diagnostics or {"warnings": [], "errors": []}
        return {
            "schema": self.SCHEMA_VERSION,
            "schema_version": self.SCHEMA_VERSION,
            "generator": "novadyne-wiki",
            "mod": dict(mod or {}),
            "entries": _sorted_entries(list(entries or [])),
            "recipes": _sorted_recipes(list(recipes or [])),
            "tags": _sorted_tags(list(tags or [])),
            "diagnostics": {
                "warnings": _sorted_issues(list(diagnostics.get("warnings", []))),
                "errors": _sorted_issues(list(diagnostics.get("errors", []))),
            },
            "generation": dict(generation or {}),
        }


def write_catalog(catalog: dict, path) -> None:
    """Serializa o catálogo em UTF-8, ordenado e determinístico."""
    write_text_atomic(
        path,
        json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
