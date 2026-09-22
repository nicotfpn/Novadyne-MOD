[Início](../README.md) · [Receitas](../receitas.md) · [Máquinas](../maquinas.md) · [Materiais](../materiais.md) · [Valves](../valves.md) · [Progressão](../progressao.md) · [Como testar](../testar.md)

---

# Etched Silicon Wafer

![Etched Silicon Wafer](../assets/generated/icon_part_electronic_etched_silicon_wafer.png)

`novadyne:part_electronic_etched_silicon_wafer`

Wafer gravado e limpo. É o final da cadeia atual; ainda não possui uso em outro craft ou processo.

## Como obter

### Limpar wafer com água

![Limpar wafer com água: entradas e saídas](../assets/generated/limpar_wafer.png)

| Quantidade | Ingrediente |
| ---: | --- |
| 1 | [Dirty Silicon Wafer](../itens/part_electronic_dirty_silicon_wafer.md) |
| 1 | Balde de água |

**Resultado:** 1 × [Etched Silicon Wafer](../itens/part_electronic_etched_silicon_wafer.md) + 1 × Balde vazio.

O wafer gravado vai para o output. **O balde vazio volta ao slot do balde**. Retire-o para inserir outro balde de água. Processo sem RNG.

[Ver lógica da máquina](../../src/main/java/com/novadyne/common/blockentity/LitografiaBlockEntity.java)

## Onde usar

Sem consumo em outra receita implementada no momento.

## Teste em criativo

```mcfunction
/give @s novadyne:part_electronic_etched_silicon_wafer
```
