[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Copper Layer

![Copper Layer](../assets/generated/icon_part_copper_layer.png)

`novadyne:part_copper_layer`

Camada de cobre para a montagem do circuito e o craft do Processor.

## Como obter

### Reciclar wafer com falha

![Reciclar wafer com falha: entradas e saídas](../assets/generated/reciclar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Failed Silicon Wafer](../itens/part_electronic_failed_silicon_wafer.md) |

**Resultado sorteado (um por ciclo):** 1 × [Copper Layer](../itens/part_copper_layer.md) **ou** 1 × [Base Wafer](../itens/part_base_wafer.md).

**50% para cada resultado**, um item por ciclo. A saída deve estar completamente vazia antes de iniciar.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/MaceratorBlockEntity.java)

### Prensar cobre

![Prensar cobre: entradas e saídas](../assets/generated/prensar_cobre.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | Barra de cobre |

**Resultado:** 1 × [Copper Layer](../itens/part_copper_layer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

## Onde usar

- Craft de [Processor](../itens/processor.md).
- Montar circuito eletrônico, em [Processor](../itens/processor.md).

## Teste em criativo

```mcfunction
/give @s novadyne:part_copper_layer
```
