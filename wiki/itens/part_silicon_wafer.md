[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Silicon Wafer

![Silicon Wafer](../assets/generated/icon_part_silicon_wafer.png)

`novadyne:part_silicon_wafer`

Sai da Wafer Press e entra na montagem do circuito. Você também vai precisar dele para construir o Processor.

## Como obter

### Prensar silício

![Prensar silício: entradas e saídas](../assets/generated/prensar_silicio.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Pure Silicon](../itens/pure_silicon.md) |

**Resultado:** 1 × [Silicon Wafer](../itens/part_silicon_wafer.md).

Conversão 1:1. A saída deve estar vazia ou conter o mesmo resultado com espaço.

<details>
<summary>Ver no código</summary>

[Lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/WaferPressBlockEntity.java)

</details>

## Onde usar

- Craft de [Processor](../itens/processor.md).
- Montar circuito eletrônico, em [Processor](../itens/processor.md).

<details>
<summary>Pegar este item em criativo</summary>

```mcfunction
/give @s novadyne:part_silicon_wafer
```

</details>
