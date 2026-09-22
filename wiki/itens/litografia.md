[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Lithography

![Lithography](../assets/generated/icon_litografia.png)

`novadyne:litografia`

## Operação

| Propriedade | Valor |
| --- | --- |
| Capacidade | 20.000 FE |
| Consumo | 40 FE/t |
| Duração | 120 ticks / 6 s |
| Energia por ciclo | 4.800 FE |

Tempos consideram 20 ticks por segundo. Recebe energia, mas não fornece energia a outros blocos. Se faltar energia durante o trabalho, o progresso volta a zero.

**Slots:** entrada, balde, valve e saída. A valve afeta apenas a chance da gravação. Na limpeza, o balde vazio permanece no slot do balde.

## Como obter

### Lithography

![Grade ou processo para Lithography](../assets/generated/litografia.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 2 | Vidro |
| 1 | [Stacked Electronic Circuit](../itens/stacked_electronic_circuit.md) |
| 2 | [Pure Silicon](../itens/pure_silicon.md) |
| 1 | Balde de água |
| 2 | Barra de ferro |
| 1 | [Processor](../itens/processor.md) |

**Resultado:** 1 × [Lithography](../itens/litografia.md).

Você recebe o balde vazio de volta ao fazer este craft.

<details>
<summary>Ver no código</summary>

[Receita JSON](../../src/main/resources/data/novadyne/recipe/litografia.json)

</details>

## Onde usar

Por enquanto, não entra em nenhuma outra receita.

## O que dá para fazer

### Gravar circuito

![Gravar circuito: entradas e saídas](../assets/generated/gravar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Stacked Electronic Circuit](../itens/stacked_electronic_circuit.md) |

**Você recebe um dos dois:** 1 × [Dirty Silicon Wafer](../itens/part_electronic_dirty_silicon_wafer.md) **ou** 1 × [Failed Silicon Wafer](../itens/part_electronic_failed_silicon_wafer.md).

A chance depende da Valve Tier (consulte o guia Valves na navegação). Sem valve equivale ao tier 1: 70% de sucesso. Tier 7: 95%. A saída precisa estar vazia. Não consome água neste estágio.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/LitografiaBlockEntity.java)

</details>

### Limpar wafer com água

![Limpar wafer com água: entradas e saídas](../assets/generated/limpar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Dirty Silicon Wafer](../itens/part_electronic_dirty_silicon_wafer.md) |
| 1 | Balde de água |

**Resultado:** 1 × [Etched Silicon Wafer](../itens/part_electronic_etched_silicon_wafer.md) + 1 × Balde vazio.

O wafer gravado vai para o output. **O balde vazio volta ao slot do balde**. Retire-o para inserir outro balde de água. A limpeza sempre dá o mesmo resultado.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/LitografiaBlockEntity.java)

</details>



<details>
<summary>Pegar este item em criativo</summary>

```mcfunction
/give @s novadyne:litografia
```

</details>
