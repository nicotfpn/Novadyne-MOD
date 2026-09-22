[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Wafer Press

![Wafer Press](../assets/generated/icon_wafer_press.png)

`novadyne:wafer_press`

## Operação

| Propriedade | Valor |
| --- | --- |
| Capacidade | 15.000 FE |
| Consumo | 30 FE/t |
| Duração | 100 ticks / 5 s |
| Energia por ciclo | 3.000 FE |

Tempos consideram 20 ticks por segundo. A extração externa de energia é bloqueada. Sem energia suficiente para o próximo tick, o progresso é zerado.

**Slots:** entrada, saída e valve. A valve ainda não aplica bônus nesta máquina.

## Como obter

### Wafer Press — wafer_press

![Grade ou processo para Wafer Press](../assets/generated/wafer_press.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 5 | Barra de ferro |
| 1 | [Ceramic Powder](../itens/ceramic_powder.md) |
| 2 | Pistão |
| 1 | [Macerator](../itens/macerator.md) |

**Resultado:** 1 × [Wafer Press](../itens/wafer_press.md).

[Ver JSON da receita](../../src/main/resources/data/novadyne/recipe/wafer_press.json)

## Onde usar

- Craft de [Processor](../itens/processor.md).

## Processos

### Prensar silício

![Prensar silício: entradas e saídas](../assets/generated/prensar_silicio.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Pure Silicon](../itens/pure_silicon.md) |

**Resultado:** 1 × [Silicon Wafer](../itens/part_silicon_wafer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

### Prensar cobre

![Prensar cobre: entradas e saídas](../assets/generated/prensar_cobre.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | Barra de cobre |

**Resultado:** 1 × [Copper Layer](../itens/part_copper_layer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

### Prensar cerâmica

![Prensar cerâmica: entradas e saídas](../assets/generated/prensar_ceramica.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Ceramic Powder](../itens/ceramic_powder.md) |

**Resultado:** 1 × [Base Wafer](../itens/part_base_wafer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)



## Teste em criativo

```mcfunction
/give @s novadyne:wafer_press
```
