[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Macerator

![Macerator](../assets/generated/icon_macerator.png)

`novadyne:macerator`

## Operação

| Propriedade | Valor |
| --- | --- |
| Capacidade | 10.000 FE |
| Consumo | 20 FE/t |
| Duração | 120 ticks / 6 s |
| Energia por ciclo | 2.400 FE |

Tempos consideram 20 ticks por segundo. A extração externa de energia é bloqueada. Sem energia suficiente para o próximo tick, o progresso é zerado.

**Slots:** entrada, saída e valve. A valve ainda não aplica bônus nesta máquina. A reciclagem exige output vazio.

## Como obter

### Macerator — macerator

![Grade ou processo para Macerator](../assets/generated/macerator.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 5 | Barra de ferro |
| 1 | Fornalha |
| 2 | Barra de cobre |
| 1 | Redstone |

**Resultado:** 1 × [Macerator](../itens/macerator.md).

[Ver JSON da receita](../../src/main/resources/data/novadyne/recipe/macerator.json)

## Onde usar

- Craft de [Wafer Press](../itens/wafer_press.md).

## Processos

### Moer argila

![Moer argila: entradas e saídas](../assets/generated/macerar_argila.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | Bola de argila |

**Resultado:** 1 × [Ceramic Powder](../itens/ceramic_powder.md).

Consome 1 bola de argila. Output deve aceitar Ceramic Powder.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/MaceratorBlockEntity.java)

### Reciclar wafer com falha

![Reciclar wafer com falha: entradas e saídas](../assets/generated/reciclar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Failed Silicon Wafer](../itens/part_electronic_failed_silicon_wafer.md) |

**Resultado sorteado (um por ciclo):** 1 × [Copper Layer](../itens/part_copper_layer.md) **ou** 1 × [Base Wafer](../itens/part_base_wafer.md).

**50% para cada resultado**, um item por ciclo. A saída deve estar completamente vazia antes de iniciar.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/MaceratorBlockEntity.java)



## Teste em criativo

```mcfunction
/give @s novadyne:macerator
```
