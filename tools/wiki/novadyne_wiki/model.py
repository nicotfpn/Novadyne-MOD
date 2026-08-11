"""Modelos de dados normalizados do catálogo (Fase 3).

Todo conteúdo é representado por uma entrada (entry). O schema do catálogo
é versionado (``schema_version``) e contém somente campos comprováveis
pelas fontes do mod; campos não comprovados ficam ausentes (nunca inventados).

O serializador do catálogo produz dicionários JSON a partir destes modelos.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Tipos de entrada usados pelo catálogo.
ENTRY_TYPES = (
    "item", "block", "block_entity", "menu", "creative_tab",
    "entity", "data_component", "system",
)


@dataclass
class IngredientRef:
    """Uma entrada de ingrediente de receita normalizada.

    Exatamente um de ``item`` ou ``tag`` é preenchido; ``alternatives``
    representa escolhas (array no JSON de origem). ``count`` é a quantidade
    exigida pela receita quando comprovável.
    """

    item: str | None = None  # "minecraft:iron_ingot"
    tag: str | None = None  # "c:gems/quartz"
    count: int = 1
    alternatives: list["IngredientRef"] = field(default_factory=list)


@dataclass
class Recipe:
    """Uma receita normalizada (JSON ou estrutura comprovada)."""

    id: str  # "novadyne:valve_tier_1"
    type: str  # "minecraft:crafting_shapeless"
    category: str | None = None  # "misc"
    group: str | None = None
    result_item: str | None = None  # "novadyne:pure_silicon"
    result_count: int = 1
    pattern: list[str] | None = None  # shaped
    key: dict[str, IngredientRef] | None = None  # shaped
    ingredients: list[IngredientRef] = field(default_factory=list)
    ingredient: IngredientRef | None = None  # smelting/blasting etc.
    experience: float | None = None
    cooking_time: int | None = None  # ticks
    machine: str | None = None  # receitas de máquina (fases futuras)
    source_file: str | None = None
    supported: bool = True
    unsupported_reason: str | None = None
    raw: dict = field(default_factory=dict)  # campos desconhecidos preservados


@dataclass
class CatalogEntry:
    """Uma entrada do catálogo (item, bloco, entidade, menu, etc.)."""

    id: str  # "novadyne:pure_silicon"
    namespace: str  # "novadyne"
    path: str  # "pure_silicon"
    type: str  # ENTRY_TYPES
    translation_key: str | None = None
    display_name: str | None = None
    translations: dict = field(default_factory=dict)  # locale -> valor
    source_files: list[str] = field(default_factory=list)
    registration_source: str | None = None  # "ModItems.java:11"
    texture: str | None = None  # id de recurso, ex: "novadyne:item/pure_silicon"
    model: str | None = None  # id de recurso, ex: "novadyne:item/pure_silicon"
    blockstate: str | None = None  # id de recurso do blockstate
    tags: list[str] = field(default_factory=list)
    recipes_as_result: list[str] = field(default_factory=list)
    recipes_as_ingredient: list[str] = field(default_factory=list)
    loot_tables: list[str] = field(default_factory=list)
    properties: dict = field(default_factory=dict)  # dados comprovados
    documentation_status: str = "auto"  # auto | manual | missing
    warnings: list[str] = field(default_factory=list)
    block: str | None = None  # para itens de bloco
    item: str | None = None  # para blocos
    block_entity: str | None = None  # para blocos com BE
    menu: str | None = None  # para blocos com menu
    stats: dict = field(default_factory=dict)  # máquina/veículo/arma (futuro)
