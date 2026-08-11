"""Descoberta de arquivos de idioma (assets/<mod>/lang/*.json) — Fase 3.

Para cada chave, preserva os valores por locale. A apresentação resolve na
ordem: ``pt_br`` (preferido quando existe) → ``en_us`` (fallback secundário)
→ demais locales em ordem alfabética. Chave ausente nunca vira nome
inventado: o catálogo registra a ausência como warning.
"""

from __future__ import annotations

from pathlib import Path

from ..errors import Issue
from ..io_utils import iter_files
from .common import ScanResult, load_json_file, to_posix

# Ordem de preferência para o nome de apresentação.
_LOCALE_PREFERENCE = ("pt_br", "en_us")


class LanguageIndex:
    """Índice de traduções por chave e locale."""

    def __init__(self, keys: dict[str, dict[str, str]], locales: list[str]):
        self._keys = keys
        self._locales = sorted(locales)

    @property
    def locales(self) -> list[str]:
        return list(self._locales)

    def has(self, key: str) -> bool:
        return key in self._keys

    def values_for(self, key: str) -> dict[str, str]:
        """Valores por locale para uma chave (cópia ordenada)."""
        return dict(sorted(self._keys.get(key, {}).items()))

    def resolve(self, key: str) -> str | None:
        """Nome de apresentação previsível: pt_br → en_us → demais."""
        values = self._keys.get(key)
        if not values:
            return None
        for locale in _LOCALE_PREFERENCE:
            if locale in values:
                return values[locale]
        ordered = sorted(values)
        return values[ordered[0]] if ordered else None

    def to_data(self) -> dict:
        return {
            "locales": list(self._locales),
            "keys": {k: dict(sorted(v.items())) for k, v in sorted(self._keys.items())},
        }


class LanguageScanner:
    """Lê todos os arquivos de idioma existentes do mod."""

    def __init__(self, *, assets_root, project_root, mod_id, reporter=None):
        self.assets_root = Path(assets_root)
        self.project_root = Path(project_root)
        self.mod_id = mod_id
        self.reporter = reporter

    def scan(self) -> ScanResult:
        result = ScanResult()
        lang_dir = self.assets_root / self.mod_id / "lang"
        keys: dict[str, dict[str, str]] = {}
        locales: set[str] = set()
        source_files: list[str] = []
        files_by_locale: dict[str, str] = {}
        files_scanned = 0

        for path in iter_files(lang_dir, suffixes=(".json",)):
            files_scanned += 1
            rel = to_posix(path.relative_to(self.project_root))
            locale = path.stem
            data, err = load_json_file(path)
            if err is not None:
                result.diagnostics.append(Issue(
                    "error", f"arquivo de idioma inválido: {err}", path=rel))
                continue
            if not isinstance(data, dict):
                result.diagnostics.append(Issue(
                    "error", "arquivo de idioma inválido: esperado um objeto JSON",
                    path=rel))
                continue
            locales.add(locale)
            source_files.append(rel)
            files_by_locale[locale] = rel
            for key, value in data.items():
                if isinstance(key, str) and isinstance(value, str):
                    keys.setdefault(key, {})[locale] = value

        result.data = {
            "index": LanguageIndex(keys, sorted(locales)),
            "source_files": sorted(source_files),
            "files_by_locale": dict(sorted(files_by_locale.items())),
        }
        result.coverage = {
            "files_scanned": files_scanned,
            "keys_found": len(keys),
            "locales": sorted(locales),
        }
        return result
