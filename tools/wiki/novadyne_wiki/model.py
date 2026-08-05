"""Modelos de dados normalizados do catálogo.

Todo conteúdo é representado por CatalogEntry. Receitas por Recipe.
Os campos seguem o que é comprovável pelas fontes; campos não comprovados
ficam ausentes (nunca inventados).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class IngredientRef:
    """Uma entrada de ingrediente de receita.

    Exatamente um de `item` ou `tag` é preenchido.
    `count` é o número de slots/quantidade exigida pela receita.
    """

    item: str | None = None  # "minecraft:iron_ingot"
    tag: str | None = None  # "c:gems/quartz"
    count: int = 1


@dataclass
class Recipe:
    id: str  # id da receita, ex: "novadyne:valve_tier_1"
    type: str  # "minecraft:crafting_shapeless", "machine", ...
    category: str | None = None  # "misc", "smelting", ...
    result_item: str | None = None  # "novadyne:pure_silicon"
    result_count: int = 1
    pattern: list[str] | None = None  # shaped
    key: dict[str, IngredientRef] | None = None  # shaped
    ingredients: list[IngredientRef] = field(default_factory=list)  # shapeless / list
    experience: float | None = None  # smelting/blasting
    cooking_time: int | None = None  # ticks
    machine: str | None = None  # para receitas de máquina: "novadyne:macerator"
    source_file: str | None = None  # arquivo que comprova a receita
    probability_note: str | None = None  # nota real (ex: 50/50 da Litografia)
    unsupported: bool = False
    unsupported_reason: str | None = None


@dataclass
class CatalogEntry:
    id: str  # "novadyne:pure_silicon" ("" para entradas sem registro, ex: tags)
    type: str  # item | block | vehicle | weapon | ammunition | component | entity | system | recipe | tag | machine
    name: str  # nome localizado (fallback: id legível)
    translation_key: str | None = None
    texture: str | None = None  # caminho de textura relativo a assets/, ex: "novadyne:textures/item/x.png"
    model: str | None = None  # caminho de modelo relativo a assets/, ex: "novadyne:models/item/x.json"
    source_classes: list[str] = field(default_factory=list)  # arquivos Java
    source_files: list[str] = field(default_factory=list)  # arquivos de recursos
    category: str | None = None  # categoria editorial
    stack_size: int | None = None
    block: str | None = None  # para itens de bloco: id do bloco
    item: str | None = None  # para blocos: id do item correspondente
    block_entity: str | None = None  # para blocos com BE
    menu: str | None = None  # para blocos com menu
    tags: list[str] = field(default_factory=list)  # ids de tags das quais participa
    loot_drops: list[str] = field(default_factory=list)  # itens dropados
    stats: dict = field(default_factory=dict)  # dados de máquina/veículo/arma comprovados
    relations: list[str] = field(default_factory=list)  # ids relacionados (documentação)
    doc_status: str = "auto"  # auto | manual | missing
    warnings: list[str] = field(default_factory=list)
    planned: bool = False
