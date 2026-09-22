[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Silicon Wafer

![Silicon Wafer](../assets/generated/icon_part_silicon_wafer.png)

`novadyne:part_silicon_wafer`

Wafer de silício prensado; componente do circuito eletrônico e do craft do Processor.

## Como obter

### Prensar silício

![Prensar silício: entradas e saídas](../assets/generated/prensar_silicio.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Pure Silicon](../itens/pure_silicon.md) |

**Resultado:** 1 × [Silicon Wafer](../itens/part_silicon_wafer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

## Onde usar

- Craft de [Processor](../itens/processor.md).
- Montar circuito eletrônico, em [Processor](../itens/processor.md).

## Teste em criativo

```mcfunction
/give @s novadyne:part_silicon_wafer
```
