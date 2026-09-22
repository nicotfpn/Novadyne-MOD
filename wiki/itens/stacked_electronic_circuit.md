[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Stacked Electronic Circuit

![Stacked Electronic Circuit](../assets/generated/icon_stacked_electronic_circuit.png)

`novadyne:stacked_electronic_circuit`

Circuito montado no Processor; pode ser gravado e é ingrediente da Lithography.

## Como obter

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

## Onde usar

- Craft de [Lithography](../itens/litografia.md).
- Gravar circuito, em [Lithography](../itens/litografia.md).

## Teste em criativo

```mcfunction
/give @s novadyne:stacked_electronic_circuit
```
