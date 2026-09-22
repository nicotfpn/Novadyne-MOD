[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Base Wafer

![Base Wafer](../assets/generated/icon_part_base_wafer.png)

`novadyne:part_base_wafer`

A base cerâmica do circuito. É feita prensando Ceramic Powder.

## Como obter

### Reciclar wafer com falha

![Reciclar wafer com falha: entradas e saídas](../assets/generated/reciclar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Failed Silicon Wafer](../itens/part_electronic_failed_silicon_wafer.md) |

**Resultados possíveis:** 1 × [Copper Layer](../itens/part_copper_layer.md) **ou** 1 × [Base Wafer](../itens/part_base_wafer.md).

**50% para cada resultado**, um item por ciclo. Retire o que estiver na saída antes de começar.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/MaceratorBlockEntity.java)

</details>

### Prensar cerâmica

![Prensar cerâmica: entradas e saídas](../assets/generated/prensar_ceramica.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Ceramic Powder](../itens/ceramic_powder.md) |

**Resultado:** 1 × [Base Wafer](../itens/part_base_wafer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

</details>

## Onde usar

- Montar circuito eletrônico, em [Processor](../itens/processor.md).

<details>
<summary>Pegar este item em criativo</summary>

```mcfunction
/give @s novadyne:part_base_wafer
```

</details>
