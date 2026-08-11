"""Scanners das fontes do mod (Fase 3).

Cada scanner lê uma família de fontes comprováveis (Java, lang, modelos,
blockstates, receitas, tags, loot tables) e produz um ``ScanResult`` com
dados normalizados, diagnósticos e métricas de cobertura. Nenhum scanner
executa código do mod.
"""

from .common import ScanResult
from .registry_scanner import RegistryScanner
from .language_scanner import LanguageScanner
from .model_scanner import ModelScanner
from .blockstate_scanner import BlockstateScanner
from .asset_scanner import AssetScanner
from .recipe_scanner import RecipeScanner
from .tag_scanner import TagScanner
from .loot_table_scanner import LootTableScanner

__all__ = [
    "ScanResult",
    "RegistryScanner",
    "LanguageScanner",
    "ModelScanner",
    "BlockstateScanner",
    "AssetScanner",
    "RecipeScanner",
    "TagScanner",
    "LootTableScanner",
]
