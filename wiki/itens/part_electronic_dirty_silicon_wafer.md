[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Dirty Silicon Wafer

![Dirty Silicon Wafer](../assets/generated/icon_part_electronic_dirty_silicon_wafer.png)

`novadyne:part_electronic_dirty_silicon_wafer`

A gravação deu certo. Uma segunda passagem pela Lithography, com água, limpa o wafer.

## Como obter

### Gravar circuito

![Gravar circuito: entradas e saídas](../assets/generated/gravar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Stacked Electronic Circuit](../itens/stacked_electronic_circuit.md) |

**Resultados possíveis:** 1 × [Dirty Silicon Wafer](../itens/part_electronic_dirty_silicon_wafer.md) **ou** 1 × [Failed Silicon Wafer](../itens/part_electronic_failed_silicon_wafer.md).

A chance depende da Valve Tier (consulte o guia Valves na navegação). Sem valve equivale ao tier 1: 70% de sucesso. Tier 7: 95%. A saída precisa estar vazia. Não consome água neste estágio.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/LitografiaBlockEntity.java)

</details>

## Onde usar

- Limpar wafer com água, em [Lithography](../itens/litografia.md).

<details>
<summary>Pegar este item em criativo</summary>

```mcfunction
/give @s novadyne:part_electronic_dirty_silicon_wafer
```

</details>
