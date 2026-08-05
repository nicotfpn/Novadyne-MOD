"""Mapeamento conservador de constantes de itens vanilla (Java) para IDs.

Usado apenas para interpretar `Items.X` nas receitas de máquina definidas em
Java. A regra geral é: a constante enum minúscula vira o ID. Exceções
conhecidas são listadas explicitamente.
"""

from __future__ import annotations

_OVERRIDES: dict[str, str] = {
    "CLAY_BALL": "minecraft:clay_ball",
    "COPPER_INGOT": "minecraft:copper_ingot",
    "WATER_BUCKET": "minecraft:water_bucket",
    "BUCKET": "minecraft:bucket",
    "IRON_INGOT": "minecraft:iron_ingot",
    "GOLD_INGOT": "minecraft:gold_ingot",
    "REDSTONE": "minecraft:redstone",
    "REDSTONE_BLOCK": "minecraft:redstone_block",
    "DIAMOND": "minecraft:diamond",
    "EMERALD": "minecraft:emerald",
    "NETHERITE_SCRAP": "minecraft:netherite_scrap",
    "NETHERITE_INGOT": "minecraft:netherite_ingot",
    "QUARTZ": "minecraft:quartz",
}


def vanilla_item_id(constant_name: str) -> str | None:
    """Converte `Items.CLAY_BALL` → `minecraft:clay_ball`.

    Retorna None quando a constante não puder ser mapeada com segurança.
    """
    name = constant_name.strip()
    if name in _OVERRIDES:
        return _OVERRIDES[name]
    if not name.isidentifier():
        return None
    lowered = name.lower()
    if not lowered or not lowered.isascii():
        return None
    return f"minecraft:{lowered}"
