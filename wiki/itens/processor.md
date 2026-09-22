[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Processor

![Processor](../assets/generated/icon_processor.png)

`novadyne:processor`

## Operação

| Propriedade | Valor |
| --- | --- |
| Capacidade | 25.000 FE |
| Consumo | 50 FE/t |
| Duração | 150 ticks / 7.5 s |
| Energia por ciclo | 7.500 FE |

Tempos consideram 20 ticks por segundo. A extração externa de energia é bloqueada. Sem energia suficiente para o próximo tick, o progresso é zerado.

**Slots:** três entradas (Silicon Wafer, Copper Layer, Base Wafer), saída e valve. A valve ainda não aplica bônus nesta máquina.

## Como obter

### Processor — processor

![Grade ou processo para Processor](../assets/generated/processor.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 2 | Redstone |
| 1 | [Copper Layer](../itens/part_copper_layer.md) |
| 2 | [Silicon Wafer](../itens/part_silicon_wafer.md) |
| 1 | [Wafer Press](../itens/wafer_press.md) |
| 2 | Barra de ferro |
| 1 | Barra de ouro |

**Resultado:** 1 × [Processor](../itens/processor.md).

[Ver JSON da receita](../../src/main/resources/data/novadyne/recipe/processor.json)

## Onde usar

- Craft de [Lithography](../itens/litografia.md).

## Processos

### Montar circuito eletrônico

![Montar circuito eletrônico: entradas e saídas](../assets/generated/montar_circuito.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Silicon Wafer](../itens/part_silicon_wafer.md) |
| 1 | [Copper Layer](../itens/part_copper_layer.md) |
| 1 | [Base Wafer](../itens/part_base_wafer.md) |

**Resultado:** 1 × [Stacked Electronic Circuit](../itens/stacked_electronic_circuit.md).

Coloque **Silicon Wafer, Copper Layer e Base Wafer nos três slots de entrada, da esquerda para a direita**. Consome 1 de cada.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/ProcessorBlockEntity.java)



## Teste em criativo

```mcfunction
/give @s novadyne:processor
```
