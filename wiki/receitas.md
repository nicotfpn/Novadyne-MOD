[Início](README.md) · [Receitas](receitas.md) · [Máquinas](maquinas.md) · [Materiais](materiais.md) · [Valves](valves.md) · [Progressão](progressao.md) · [Como testar](testar.md)

---

# Receitas e processos

As imagens mostram a disposição dos ingredientes e o resultado de cada operação. Na bancada, siga a grade quando houver posição fixa; nas máquinas, confira as entradas e deixe espaço na saída.

## Bancada e fornos

### Lithography

![Grade ou processo para Lithography](assets/generated/litografia.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 2 | Vidro |
| 1 | [Stacked Electronic Circuit](itens/stacked_electronic_circuit.md) |
| 2 | [Pure Silicon](itens/pure_silicon.md) |
| 1 | Balde de água |
| 2 | Barra de ferro |
| 1 | [Processor](itens/processor.md) |

**Resultado:** 1 × [Lithography](itens/litografia.md).

O balde vazio retorna após o craft.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/litografia.json)

</details>

### Macerator

![Grade ou processo para Macerator](assets/generated/macerator.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 5 | Barra de ferro |
| 1 | Fornalha |
| 2 | Barra de cobre |
| 1 | Redstone |

**Resultado:** 1 × [Macerator](itens/macerator.md).

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/macerator.json)

</details>

### Processor

![Grade ou processo para Processor](assets/generated/processor.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 2 | Redstone |
| 1 | [Copper Layer](itens/part_copper_layer.md) |
| 2 | [Silicon Wafer](itens/part_silicon_wafer.md) |
| 1 | [Wafer Press](itens/wafer_press.md) |
| 2 | Barra de ferro |
| 1 | Barra de ouro |

**Resultado:** 1 × [Processor](itens/processor.md).

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/processor.json)

</details>

### Pure Silicon · fornalha

![Grade ou processo para Pure Silicon](assets/generated/pure_silicon_from_quartz.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | Quartzo |

**Resultado:** 1 × [Pure Silicon](itens/pure_silicon.md).

A tag `c:gems/quartz` contém quartzo vanilla neste mod e pode receber outros itens por datapacks. O combustível não está incluído no ingrediente.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/pure_silicon_from_quartz.json)

</details>

### Pure Silicon · alto-forno

![Grade ou processo para Pure Silicon](assets/generated/pure_silicon_from_quartz_blasting.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | Quartzo |

**Resultado:** 1 × [Pure Silicon](itens/pure_silicon.md).

A tag `c:gems/quartz` contém quartzo vanilla neste mod e pode receber outros itens por datapacks. O combustível não está incluído no ingrediente.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/pure_silicon_from_quartz_blasting.json)

</details>

### Valve (Tier 1)

![Grade ou processo para Valve (Tier 1)](assets/generated/valve_tier_1.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 3 | Barra de ferro |
| 1 | Barra de cobre |

**Resultado:** 1 × [Valve (Tier 1)](itens/valve_tier_1.md).

**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/valve_tier_1.json)

</details>

### Valve (Tier 2)

![Grade ou processo para Valve (Tier 2)](assets/generated/valve_tier_2.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Valve (Tier 1)](itens/valve_tier_1.md) |
| 2 | Barra de ferro |
| 1 | Redstone |

**Resultado:** 1 × [Valve (Tier 2)](itens/valve_tier_2.md).

**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/valve_tier_2.json)

</details>

### Valve (Tier 3)

![Grade ou processo para Valve (Tier 3)](assets/generated/valve_tier_3.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Valve (Tier 2)](itens/valve_tier_2.md) |
| 2 | Barra de ouro |
| 2 | Redstone |

**Resultado:** 1 × [Valve (Tier 3)](itens/valve_tier_3.md).

**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/valve_tier_3.json)

</details>

### Valve (Tier 4)

![Grade ou processo para Valve (Tier 4)](assets/generated/valve_tier_4.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Valve (Tier 3)](itens/valve_tier_3.md) |
| 2 | Diamante |
| 4 | Redstone |

**Resultado:** 1 × [Valve (Tier 4)](itens/valve_tier_4.md).

**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/valve_tier_4.json)

</details>

### Valve (Tier 5)

![Grade ou processo para Valve (Tier 5)](assets/generated/valve_tier_5.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Valve (Tier 4)](itens/valve_tier_4.md) |
| 2 | Esmeralda |
| 4 | Bloco de redstone |

**Resultado:** 1 × [Valve (Tier 5)](itens/valve_tier_5.md).

**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/valve_tier_5.json)

</details>

### Valve (Tier 6)

![Grade ou processo para Valve (Tier 6)](assets/generated/valve_tier_6.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Valve (Tier 5)](itens/valve_tier_5.md) |
| 2 | Fragmento de netherita |
| 4 | Bloco de redstone |

**Resultado:** 1 × [Valve (Tier 6)](itens/valve_tier_6.md).

**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/valve_tier_6.json)

</details>

### Valve (Tier 7)

![Grade ou processo para Valve (Tier 7)](assets/generated/valve_tier_7.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Valve (Tier 6)](itens/valve_tier_6.md) |
| 2 | Barra de netherita |
| 6 | Bloco de redstone |

**Resultado:** 1 × [Valve (Tier 7)](itens/valve_tier_7.md).

**Sem posição fixa:** basta colocar esses ingredientes na bancada, em qualquer ordem.

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/valve_tier_7.json)

</details>

### Wafer Press

![Grade ou processo para Wafer Press](assets/generated/wafer_press.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 5 | Barra de ferro |
| 1 | [Ceramic Powder](itens/ceramic_powder.md) |
| 2 | Pistão |
| 1 | [Macerator](itens/macerator.md) |

**Resultado:** 1 × [Wafer Press](itens/wafer_press.md).

<details>
<summary>Ver no código</summary>

[Receita JSON](../src/main/resources/data/novadyne/recipe/wafer_press.json)

</details>

## Nas máquinas

### Moer argila

![Moer argila: entradas e saídas](assets/generated/macerar_argila.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | Bola de argila |

**Resultado:** 1 × [Ceramic Powder](itens/ceramic_powder.md).

Consome 1 bola de argila. Deixe espaço para Ceramic Powder na saída.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../src/main/java/com/novadyne/common/blockentity/MaceratorBlockEntity.java)

</details>

### Reciclar wafer com falha

![Reciclar wafer com falha: entradas e saídas](assets/generated/reciclar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Failed Silicon Wafer](itens/part_electronic_failed_silicon_wafer.md) |

**Resultados possíveis:** 1 × [Copper Layer](itens/part_copper_layer.md) **ou** 1 × [Base Wafer](itens/part_base_wafer.md).

**50% para cada resultado**, um item por ciclo. Retire o que estiver na saída antes de começar.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../src/main/java/com/novadyne/common/blockentity/MaceratorBlockEntity.java)

</details>

### Prensar silício

![Prensar silício: entradas e saídas](assets/generated/prensar_silicio.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Pure Silicon](itens/pure_silicon.md) |

**Resultado:** 1 × [Silicon Wafer](itens/part_silicon_wafer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

</details>

### Prensar cobre

![Prensar cobre: entradas e saídas](assets/generated/prensar_cobre.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | Barra de cobre |

**Resultado:** 1 × [Copper Layer](itens/part_copper_layer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

</details>

### Prensar cerâmica

![Prensar cerâmica: entradas e saídas](assets/generated/prensar_ceramica.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Ceramic Powder](itens/ceramic_powder.md) |

**Resultado:** 1 × [Base Wafer](itens/part_base_wafer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

</details>

### Montar circuito eletrônico

![Montar circuito eletrônico: entradas e saídas](assets/generated/montar_circuito.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Silicon Wafer](itens/part_silicon_wafer.md) |
| 1 | [Copper Layer](itens/part_copper_layer.md) |
| 1 | [Base Wafer](itens/part_base_wafer.md) |

**Resultado:** 1 × [Stacked Electronic Circuit](itens/stacked_electronic_circuit.md).

Coloque **Silicon Wafer, Copper Layer e Base Wafer nos três slots de entrada, da esquerda para a direita**. Consome 1 de cada.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../src/main/java/com/novadyne/common/blockentity/ProcessorBlockEntity.java)

</details>

### Gravar circuito

![Gravar circuito: entradas e saídas](assets/generated/gravar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Stacked Electronic Circuit](itens/stacked_electronic_circuit.md) |

**Resultados possíveis:** 1 × [Dirty Silicon Wafer](itens/part_electronic_dirty_silicon_wafer.md) **ou** 1 × [Failed Silicon Wafer](itens/part_electronic_failed_silicon_wafer.md).

A chance depende da Valve Tier (consulte o guia Valves na navegação). Sem valve equivale ao tier 1: 70% de sucesso. Tier 7: 95%. A saída precisa estar vazia. Não consome água neste estágio.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../src/main/java/com/novadyne/common/blockentity/LitografiaBlockEntity.java)

</details>

### Limpar wafer com água

![Limpar wafer com água: entradas e saídas](assets/generated/limpar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Dirty Silicon Wafer](itens/part_electronic_dirty_silicon_wafer.md) |
| 1 | Balde de água |

**Resultado:** 1 × [Etched Silicon Wafer](itens/part_electronic_etched_silicon_wafer.md) + 1 × Balde vazio.

O wafer gravado vai para o output. **O balde vazio volta ao slot do balde**. Retire-o para inserir outro balde de água. A limpeza sempre dá o mesmo resultado.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../src/main/java/com/novadyne/common/blockentity/LitografiaBlockEntity.java)

</details>
