# Auditoria do Repositório — NovaDyne

> Data da auditoria: 2026-08-05
> Versão do mod: `1.0.0` (de `gradle.properties`)
> Minecraft: `26.1.2` · NeoForge: `26.1.2.76` · Java: `25`
> Mod ID: `novadyne` · Grupo: `com.novadyne`

Esta auditoria foi gerada manualmente, lendo o conteúdo real do repositório.
Nenhuma suposição sobre conteúdo foi incluída. Cada seção indica as fontes
usadas para as descobertas.

---

## 1. Estrutura relevante de pastas

```
src/main/java/com/novadyne/
├── NovaDyneMod.java                  # Ponto de entrada; registra todos os DeferredRegisters
├── ModItems.java                     # Registro de itens (20 itens)
├── ModBlocks.java                    # Registro de blocos (4 blocos)
├── ModBlockEntities.java             # Registro de block entities (4)
├── ModMenuTypes.java                 # Registro de menus (4)
├── ModDataComponents.java            # Registro de data components (vazio)
├── ModCreativeTabs.java              # Aba criativa (1)
├── api/
│   ├── energy/                       # API de energia (IStrictEnergyHandler, IEnergyContainer, Action, AutomationType, IContentsListener)
│   └── machine/IUpgradeableMachine.java
├── client/
│   ├── ClientModEvents.java          # Registro de telas (4)
│   └── screen/                       # Telas de máquinas (4)
├── common/
│   ├── block/                        # AbstractMachineBlock + 4 máquinas
│   ├── blockentity/                  # AbstractMachineBlockEntity + 4 BEs (receitas de máquina vivem aqui)
│   ├── menu/                         # AbstractMachineMenu + 4 menus
│   ├── capabilities/energy/          # BasicEnergyContainer, MachineEnergyContainer
│   ├── integration/energy/           # EnergyCompat, adapters Forge Energy
│   └── util/                         # NBTUtils, SerializationConstants

src/main/resources/
├── assets/novadyne/
│   ├── lang/en_us.json               # Único arquivo de idioma (en_us)
│   ├── models/item/                  # 20 modelos de item
│   ├── models/block/                 # 4 modelos de bloco
│   ├── blockstates/                  # 4 blockstates
│   ├── items/                        # 20 definições de item (client item definitions)
│   ├── textures/item/                # 23 texturas de item
│   ├── textures/block/               # 6 texturas de bloco
│   └── textures/gui/                 # 4 texturas de GUI
└── data/
    ├── novadyne/recipe/              # 9 receitas JSON
    ├── novadyne/loot_table/blocks/   # 4 loot tables
    └── c/tags/item/gems/quartz.json  # 1 tag

.github/workflows/build.yml           # Build existente (push + PR)
```

Fonte: listagem real do diretório (`src/main/java`, `src/main/resources`).

---

## 2. Registros encontrados

| Registro | Quantidade | Arquivo |
|---|---|---|
| Itens | 20 | `ModItems.java` |
| Blocos | 4 | `ModBlocks.java` |
| Block entities | 4 | `ModBlockEntities.java` |
| Menus | 4 | `ModMenuTypes.java` |
| Telas (client) | 4 | `ClientModEvents.java` |
| Abas criativas | 1 | `ModCreativeTabs.java` |
| Data components | 0 (registro vazio) | `ModDataComponents.java` |
| Entidades | 0 | — |
| Veículos | 0 | — |
| Armas | 0 (Plasma Cannon *planejada* no README) | `README.md` |

---

## 3. Itens existentes (20)

### 3.1 Materiais (9)

| ID | Nome (en_us) |
|---|---|
| `novadyne:pure_silicon` | Pure Silicon |
| `novadyne:part_silicon_wafer` | Silicon Wafer |
| `novadyne:ceramic_powder` | Ceramic Powder |
| `novadyne:part_copper_layer` | Copper Layer |
| `novadyne:part_base_wafer` | Base Wafer |
| `novadyne:stacked_electronic_circuit` | Stacked Electronic Circuit |
| `novadyne:part_electronic_dirty_silicon_wafer` | Dirty Silicon Wafer |
| `novadyne:part_electronic_failed_silicon_wafer` | Failed Silicon Wafer |
| `novadyne:part_electronic_etched_silicon_wafer` | Etched Silicon Wafer |

### 3.2 Itens de bloco (4)

| ID | Bloco |
|---|---|
| `novadyne:macerator` | `novadyne:macerator` |
| `novadyne:wafer_press` | `novadyne:wafer_press` |
| `novadyne:processor` | `novadyne:processor` |
| `novadyne:litografia` | `novadyne:litografia` |

### 3.3 Válvulas de upgrade (7)

`novadyne:valve_tier_1` … `novadyne:valve_tier_7` (Valve (Tier 1) … Valve (Tier 7)).

Fonte: `ModItems.java` (todas via `registerSimpleItem` / `registerSimpleBlockItem`).

---

## 4. Blocos existentes (4)

| ID | Classe | Propriedades |
|---|---|---|
| `novadyne:macerator` | `MaceratorBlock` | strength 3.5/6.0, `requiresCorrectToolForDrops` |
| `novadyne:wafer_press` | `WaferPressBlock` | idem |
| `novadyne:processor` | `ProcessorBlock` | idem |
| `novadyne:litografia` | `LitografiaBlock` | idem |

Todos herdam `AbstractMachineBlock` (bloco com `facing` horizontal, abre menu,
tem sinal de comparador e ticker de servidor).

Fonte: `ModBlocks.java`, `AbstractMachineBlock.java`.

---

## 5. Block entities (4) e estatísticas de máquina

| Máquina | Capacidade (FE) | Consumo (FE/t) | Progresso (t) | Slots |
|---|---|---|---|---|
| Macerator | 10 000 | 20 | 120 | 3 (entrada, saída, válvula) |
| Wafer Press | 15 000 | 30 | 100 | 3 (entrada, saída, válvula) |
| Processor | 25 000 | 50 | 150 | 5 (3 entradas, saída, válvula) |
| Litografia | 20 000 | 40 | 120 | 4 (entrada, balde, válvula, saída) |

Fonte: constantes `MAX_ENERGY`, `ENERGY_PER_TICK`, `MAX_PROGRESS` e `INVENTORY_SIZE`
em `MaceratorBlockEntity.java`, `WaferPressBlockEntity.java`,
`ProcessorBlockEntity.java`, `LitografiaBlockEntity.java`.

---

## 6. Receitas existentes (formato JSON, 9 arquivos)

Todos em `src/main/resources/data/novadyne/recipe/`.

| Arquivo | Tipo | Resultado |
|---|---|---|
| `valve_tier_1.json` | `minecraft:crafting_shapeless` | `novadyne:valve_tier_1` |
| `valve_tier_2.json` | `minecraft:crafting_shapeless` | `novadyne:valve_tier_2` |
| `valve_tier_3.json` | `minecraft:crafting_shapeless` | `novadyne:valve_tier_3` |
| `valve_tier_4.json` | `minecraft:crafting_shapeless` | `novadyne:valve_tier_4` |
| `valve_tier_5.json` | `minecraft:crafting_shapeless` | `novadyne:valve_tier_5` |
| `valve_tier_6.json` | `minecraft:crafting_shapeless` | `novadyne:valve_tier_6` |
| `valve_tier_7.json` | `minecraft:crafting_shapeless` | `novadyne:valve_tier_7` |
| `pure_silicon_from_quartz.json` | `minecraft:smelting` | `novadyne:pure_silicon` |
| `pure_silicon_from_quartz_blasting.json` | `minecraft:blasting` | `novadyne:pure_silicon` |

### 6.1 Formatos observados (importante para o gerador)

1. **Shapeless simplificado (26.1.x)**: `ingredients` é um **array de strings**
   (`"minecraft:iron_ingot"`), `result` é objeto `{ "id": "...", "count": n }`.
   *Não* usa o formato antigo `{ "item": ... }` por objeto.
   Fonte: `valve_tier_1.json` … `valve_tier_7.json`.
2. **Forno simplificado**: `ingredient` é string com prefixo `#` para tag
   (`"#c:gems/quartz"`), `result` é `{ "id": "..." }` (sem `count`), com
   `experience` e `cookingtime`.
   Fonte: `pure_silicon_from_quartz.json`, `pure_silicon_from_quartz_blasting.json`.

Não existem receitas `crafting_shaped`, `smoking`, `campfire_cooking`,
`stonecutting` ou `smithing_transform` no projeto até esta data.

### 6.2 Receitas de máquina (definidas em Java, não em JSON)

As máquinas não usam o Recipe Manager; definem receitas fixas em código.
Fonte: classes `*BlockEntity.java`.

| Máquina | Entrada | Saída | Observações |
|---|---|---|---|
| Macerator | `minecraft:clay_ball` | `novadyne:ceramic_powder` ×1 | determinística |
| Macerator | `novadyne:part_electronic_failed_silicon_wafer` | `novadyne:part_copper_layer` ×1 **ou** `novadyne:part_base_wafer` ×1 | 50/50 aleatório por item |
| Wafer Press | `novadyne:pure_silicon` | `novadyne:part_silicon_wafer` ×1 | determinística |
| Wafer Press | `minecraft:copper_ingot` | `novadyne:part_copper_layer` ×1 | determinística |
| Wafer Press | `novadyne:ceramic_powder` | `novadyne:part_base_wafer` ×1 | determinística |
| Processor | `novadyne:part_silicon_wafer` + `novadyne:part_copper_layer` + `novadyne:part_base_wafer` | `novadyne:stacked_electronic_circuit` ×1 | 3 entradas fixas |
| Litografia | `novadyne:stacked_electronic_circuit` | `novadyne:part_electronic_dirty_silicon_wafer` ×1 (sucesso) ou `novadyne:part_electronic_failed_silicon_wafer` ×1 (falha) | chance de falha: 30% (tier 1) → 5% (tier 7), linear |
| Litografia | `novadyne:part_electronic_dirty_silicon_wafer` + `minecraft:water_bucket` | `novadyne:part_electronic_etched_silicon_wafer` ×1 + `minecraft:bucket` ×1 | consome o balde |

Nota de precisão: a chance de falha da Litografia é calculada como
`0.30 − (tier−1) × (0.25/6.0)`, limitada entre 0.05 e 0.30, com `tier` mínimo 1.
Fonte: `LitografiaBlockEntity.processEngraving()`.

---

## 7. Tags existentes

| Tag | Valores |
|---|---|
| `c:gems/quartz` | `minecraft:quartz` |

Fonte: `src/main/resources/data/c/tags/item/gems/quartz.json`.

---

## 8. Loot tables existentes (4)

`macerator`, `wafer_press`, `processor`, `litografia` — todas `minecraft:block`,
com um pool de 1 roll, entry `minecraft:item` apontando para o próprio bloco,
condicionado a `minecraft:survives_explosion`.

Fonte: `src/main/resources/data/novadyne/loot_table/blocks/*.json`.

---

## 9. Idiomas existentes

| Arquivo | Chaves |
|---|---|
| `assets/novadyne/lang/en_us.json` | 22 (1 aba criativa + 4 blocos + 9 materiais + 7 válvulas + 1 tooltip de energia) |

Não existe `pt_br`. O site usará pt-BR como idioma editorial e os nomes de
itens virão de `en_us.json` (única fonte real).

---

## 10. Texturas e modelos

### 10.1 Texturas de item (23 PNGs)

20 correspondem a itens registrados + **3 sem registro**:

| Textura sem registro | Status |
|---|---|
| `textures/item/transistor.png` | sem item, sem modelo → conteúdo aparentemente planejado |
| `textures/item/capacitor_tier_1.png` | idem |
| `textures/item/capacitor_tier_2.png` | idem |

Fonte: listagem de `assets/novadyne/textures/item/`.

### 10.2 Texturas de bloco (6 PNGs)

`macerator_front`, `wafer_press_front`, `processor_front`, `litografia_front`,
`machine_side`, `machine_top` — todas referenciadas pelos 4 modelos de bloco
(`minecraft:block/orientable`).

### 10.3 Texturas de GUI (4 PNGs)

`macerator`, `wafer_press`, `processor`, `litografia` — usadas pelas telas.

### 10.4 Modelos

- `models/item/`: 20 arquivos — um para cada item registrado (itens simples usam
  `minecraft:item/generated` com `layer0`; itens de bloco apontam para
  `novadyne:block/<nome>`).
- `models/block/`: 4 arquivos (`orientable` com front/side/top).
- `blockstates/`: 4 arquivos (variante `facing`).
- `items/` (client item definitions): 20 arquivos, `{ "model": { "type":
  "minecraft:model", "model": "novadyne:..." } }`.

Fonte: listagem de `assets/novadyne/{models,blockstates,items}`.

---

## 11. Inconsistências e pontos de atenção

1. **Texturas sem registro**: `transistor`, `capacitor_tier_1`,
   `capacitor_tier_2` → provável conteúdo planejado (eletrônicos). Não documentar
   como conteúdo disponível.
2. **README desatualizado/minimalista**: lista apenas "Plasma Cannon (planned)"
   e não menciona as máquinas, materiais ou válvulas existentes.
3. **`src/generated/resources`** é declarado em `build.gradle`, mas a pasta não
   existe; nada foi gerado por datagen até esta data.
4. **Receitas em formato simplificado** (strings em vez de objetos): o gerador
   deve suportar esse formato; formatos antigos podem não ser válidos em 26.1.2.
5. **Sem testes automatizados** (`src/test` inexistente).
6. **`ModDataComponents` vazio**: registro criado, sem componentes.
7. **Sem entidades, veículos ou armas** registrados, apesar da descrição do mod
   ("Aerospace and combat vehicles mod").
8. **Litografia**: usa `tier = max(1, valveTier)`, ou seja, sem válvula a
   chance de falha é a do tier 1 (30%).
9. **`.github/workflows/build.yml`** existente: roda `./gradlew build` em push/PR.
   A wiki deve integrar-se sem quebrá-lo.

---

## 12. Conteúdo aparentemente planejado

| Item | Evidência |
|---|---|
| Plasma Cannon (arma de energia) | `README.md` ("Plasma Cannon *(planned)* — Energy weapon") |
| Transistor | textura sem registro |
| Capacitor Tier 1 / Tier 2 | texturas sem registro |
| Dobro de minérios por tag (`c:ores/*` → `c:dusts/*`) | comentário FUTURE em `MaceratorBlockEntity.java` |

Nada disso deve ser documentado como disponível.

---

## 13. Fontes consultadas

- `AGENTS.md`, `gradle.properties`, `build.gradle`, `settings.gradle`, `README.md`
- `src/main/java/com/novadyne/*.java` (todos os registros)
- `src/main/java/com/novadyne/**/*.java` (blocos, BEs, menus, telas, energia, API)
- `src/main/resources/assets/novadyne/**` (lang, models, blockstates, items, textures)
- `src/main/resources/data/novadyne/**` (recipes, loot tables)
- `src/main/resources/data/c/**` (tags)
- `.github/workflows/build.yml`, `.gitignore`

---

## 14. Arquitetura final proposta (resumo)

Baseada no conteúdo real encontrado, a wiki usará:

- **Camada 1 (fontes)**: `gradle.properties`, registros Java, `lang/en_us.json`,
  modelos, blockstates, texturas, receitas JSON, loot tables, tags, receitas de
  máquina em Java, constantes de máquina em Java.
- **Camada 2 (catálogo)**: `build/wiki/catalog.json` normalizado, gerado por
  scanners Python conservadores (sem execução de código do mod).
- **Camada 3 (manual)**: `wiki/content/` (YAML/Markdown com front matter).
- **Camada 4 (gerado)**: `wiki/generated/` (descartável) + `wiki/docs/`
  (montado pelo gerador para o MkDocs).
- **Camada 5 (site)**: MkDocs Material com tema próprio, pt-BR, receitas em
  HTML/CSS com texturas reais, busca e navegação geradas.

A próxima fase (Fase 2) implementa a fundação do gerador e do site.
