# BLUEPRINT - NovaDyne

Documento de referência rápida do projeto `novadyne` para NeoForge 26.1.2.

## Estrutura de diretórios

```text
novadynemod/
├─ build.gradle
├─ gradle.properties
├─ settings.gradle
├─ geckolib-neoforge-26.1.2-5.5.1.jar
├─ src/
│  └─ main/
│     ├─ java/
│     │  └─ com/novadyne/
│     │     ├─ NovaDyneMod.java
│     │     ├─ ModItems.java
│     │     ├─ ModCreativeTabs.java
│     │     ├─ items/
│     │     │  └─ ExosuitTier1Item.java
│     │     └─ client/
│     │        ├─ model/
│     │        │  └─ ExosuitTier1ArmorModel.java
│     │        └─ renderer/
│     │           └─ ExosuitTier1ArmorRenderer.java
│     ├─ resources/
│     │  └─ assets/novadyne/
│     │     ├─ geckolib/models/
│     │     │  └─ exosuit_tier1.geo.json
│     │     ├─ lang/
│     │     │  └─ en_us.json
│     │     ├─ models/item/
│     │     │  └─ exosuit_tier1.json
│     │     └─ textures/armor/
│     │        └─ exosuit_tier1.png
│     └─ templates/
│        └─ META-INF/
│           └─ neoforge.mods.toml
```

## Classe principal

### `com.novadyne.NovaDyneMod`

Arquivo: `src/main/java/com/novadyne/NovaDyneMod.java`

- Anotação principal: `@Mod(NovaDyneMod.MODID)`
- `MODID`: `novadyne`
- Logger: `LogUtils.getLogger()`
- Construtor recebe `IEventBus modEventBus`
- Registra no mod event bus:
  - `ModItems.ITEMS.register(modEventBus)`
  - `ModCreativeTabs.CREATIVE_MODE_TABS.register(modEventBus)`

## Registros de conteúdo

### Itens

Classe: `com.novadyne.ModItems`

Registry:

```java
public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(NovaDyneMod.MODID);
```

Itens registrados:

| Campo Java | Nome de registro | Tipo | Observações |
|---|---|---|---|
| `PLASMA_CANNON` | `plasma_cannon` | `Item` | Item simples registrado com `ITEMS.registerSimpleItem("plasma_cannon")`, garantindo `Item.Properties#setId` automaticamente. |
| `EXOSUIT_TIER1` | `exosuit_tier1` | `ExosuitTier1Item` | Item de armadura GeckoLib registrado com `ITEMS.registerItem("exosuit_tier1", ExosuitTier1Item::new)`. Implementa `GeoItem` e renderiza via `GeoArmorRenderer`. |

### Item customizado (GeckoLib)

Classe: `com.novadyne.items.ExosuitTier1Item`

- Estende `net.minecraft.world.item.Item` e implementa `com.geckolib.animatable.GeoItem`
- No construtor aplica `properties.humanoidArmor(ArmorMaterials.IRON, ArmorType.CHESTPLATE)`
- Implementa `createGeoRenderer()` para registrar `GeoRenderProvider` com `ExosuitTier1ArmorRenderer`
- Implementa `registerControllers()` (sem controllers de animação por enquanto)
- Usa `AnimatableInstanceCache` via `GeckoLibUtil.createInstanceCache(this)`

### Modelo GeckoLib (Client)

Classe: `com.novadyne.client.model.ExosuitTier1ArmorModel`

- Estende `GeoModel<ExosuitTier1Item>`
- Aponta para:
  - Model: `novadyne:exosuit_tier1` (arquivo em `geckolib/models/exosuit_tier1.geo.json`)
  - Texture: `novadyne:armor/exosuit_tier1` (arquivo em `textures/armor/exosuit_tier1.png`)
  - Animation: `null` (nenhuma animação registrada)

### Renderer GeckoLib (Client)

Classe: `com.novadyne.client.renderer.ExosuitTier1ArmorRenderer`

- Estende `GeoArmorRenderer<ExosuitTier1Item, HumanoidRenderState>`
- Usa `ExosuitTier1ArmorModel` como modelo

### Creative Tabs

Classe: `com.novadyne.ModCreativeTabs`

Registry:

```java
public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS =
        DeferredRegister.create(Registries.CREATIVE_MODE_TAB, NovaDyneMod.MODID);
```

Tabs registradas:

| Campo Java | Nome de registro | Título | Ícone | Conteúdo |
|---|---|---|---|---|
| `NOVADYNE_TAB` | `novadyne` | `NovaDyne` | `PLASMA_CANNON` | `PLASMA_CANNON`, `EXOSUIT_TIER1` |

### Blocos

Nenhuma classe de registro de blocos encontrada.

### Entidades

Nenhuma classe de registro de entidades encontrada.

### Menus, block entities, receitas por código, componentes ou outros registries

Nenhum registro encontrado além de itens e creative tabs.

## Recursos

Base de assets encontrada:

```text
src/main/resources/assets/novadyne/
```

### `models/`

Arquivos JSON: 1

- `models/item/exosuit_tier1.json`
  - Modelo de item para inventário/hotbar: `{"parent": "builtin/entity"}`.

### `geckolib/models/`

Arquivos: 1

- `exosuit_tier1.geo.json`
  - Modelo geométrico no formato Blockbench/Bedrock com `format_version`: `1.12.0`
  - Identificador: `geometry.exosuit_tier1`
  - Textura declarada: 64×128 (PNG real é 64×64; UVs podem estar desalinhadas verticalmente)
  - NÃO possui rotação [0,180,0] nos bones — modelo foi reconstruído já orientado para frente
  - Bones padrão do Minecraft (vazios ou com cubes):
    - `bipedHead`, `armorHead` (10 cubes — capacete/antenas)
    - `bipedBody`, `armorBody` (14 cubes — peitoral frente + costas)
    - `bipedRightArm`, `armorRightArm` (0 cubes)
    - `bipedLeftArm`, `armorLeftArm` (0 cubes)
    - `bipedLeftLeg`, `armorLeftLeg`, `armorLeftBoot` (0 cubes)
    - `bipedRightLeg`, `armorRightLeg`, `armorRightBoot` (0 cubes)

### `textures/`

Arquivos PNG: 1

- `textures/armor/exosuit_tier1.png` (64×64 — conteúdo visível apenas nas linhas 16, 20, 27, 29)

### `lang/`

Arquivos: 1

- `en_us.json`

Chaves atuais:

```json
{
  "itemGroup.examplemod": "Example Mod Tab",
  "block.examplemod.example_block": "Example Block",
  "item.examplemod.example_item": "Example Item",
  "examplemod.configuration.title": "Example Mod Configs",
  "examplemod.configuration.section.examplemod.common.toml": "Example Mod Configs",
  "examplemod.configuration.section.examplemod.common.toml.title": "Example Mod Configs",
  "examplemod.configuration.items": "Item List",
  "examplemod.configuration.logDirtBlock": "Log Dirt Block",
  "examplemod.configuration.magicNumberIntroduction": "Magic Number Text",
  "examplemod.configuration.magicNumber": "Magic Number"
}
```

Observação: as traduções ainda usam o namespace `examplemod`, não `novadyne`.

### `data/novadyne/`

Nenhuma pasta `src/main/resources/data/novadyne/` encontrada.

### Blockstates, modelos de item/bloco, receitas, loot tables e tags

Não encontrados no estado atual do projeto.

## Configurações do projeto

### `gradle.properties`

| Propriedade | Valor |
|---|---|
| `minecraft_version` | `26.1.2` |
| `minecraft_version_range` | `[26.1.2,)` |
| `neo_version` | `26.1.2.76` |
| `mod_id` | `novadyne` |
| `mod_name` | `NovaDyne` |
| `mod_license` | `All Rights Reserved` |
| `mod_version` | `1.0.0` |
| `mod_group_id` | `com.novadyne` |
| `mod_authors` | `SeuNick` |
| `mod_description` | `Aerospace and combat vehicles mod` |

Gradle:

- `org.gradle.jvmargs=-Xmx1G`
- Daemon habilitado
- Parallel habilitado
- Build cache habilitado
- Configuration cache habilitado

### `build.gradle`

Plugins:

- `java-library`
- `maven-publish`
- `net.neoforged.moddev` versão `2.0.141`
- `idea`

Configuração NeoForge:

- `neoForge.version = project.neo_version`
- Runs configurados:
  - `client`
  - `server`
  - `gameTestServer`
  - `data`
- Namespace de GameTests usa `project.mod_id`
- Geração de metadata via task `generateModMetadata`
- Recursos gerados incluídos por `sourceSets.main.resources.srcDir generateModMetadata`
- Datagen output: `src/generated/resources/`

Java:

- Toolchain configurada para Java 25
- Encoding de compilação: UTF-8

Dependências:

- `modImplementation files('geckolib-neoforge-26.1.2-5.5.1.jar')`

Repositórios:

- Maven GeckoLib: `https://dl.cloudsmith.io/public/geckolib3/geckolib/maven/`

### `settings.gradle`

- Usa plugin `org.gradle.toolchains.foojay-resolver-convention` versão `1.0.0`

### `src/main/templates/META-INF/neoforge.mods.toml`

Arquivo template usado por `generateModMetadata`.

Campos principais gerados por placeholders:

- `license="${mod_license}"`
- `modId="${mod_id}"`
- `version="${mod_version}"`
- `displayName="${mod_name}"`
- `description=${mod_description}`

Dependências declaradas:

- `neoforge`
  - tipo: `required`
  - versionRange: `[${neo_version},)`
  - side: `BOTH`
- `minecraft`
  - tipo: `required`
  - versionRange: `${minecraft_version_range}`
  - side: `BOTH`

## Observações e sugestões

- `en_us.json` ainda contém traduções de exemplo com namespace `examplemod`; ideal trocar para `novadyne`.
- A creative tab usa `Component.literal("NovaDyne")`; se quiser localização, criar chave `itemGroup.novadyne.novadyne` ou similar.
- `PLASMA_CANNON` não possui textura, modelo de item nem tradução própria.
- `EXOSUIT_TIER1` possui textura em `textures/armor/exosuit_tier1.png`, geo model em `geckolib/models/exosuit_tier1.geo.json`, modelo de item em `models/item/exosuit_tier1.json` e renderização GeckoLib ativa via `ExosuitTier1Item` → `ExosuitTier1ArmorRenderer` → `ExosuitTier1ArmorModel`.
- **Diagnóstico 2026-07-01 (15h)**: Havia 2 geo.json conflitantes — `models/exosuit_tier1.geo.json` (correto, 14 cubes front+back, sem rotação) e `geckolib/models/exosuit_tier1.geo.json` (incompleto, 6 cubes só frente, com rotação [0,180,0]). O GeckoLib carregava o de `geckolib/models/` (incompleto). Correção: o modelo correto de `models/` foi copiado para `geckolib/models/` (substituindo o antigo) e `models/exosuit_tier1.geo.json` foi deletado. O modelo não usa mais rotação [0,180,0] pois foi exportado já orientado para frente. Atenção: o modelo declara `texture_height: 128` mas o PNG é 64×64 — UVs podem estar desalinhadas.
- **Bones com cubes**: `armorHead` (10 cubes), `armorBody` (14 cubes — frente + costas)
- **Bones sem cubes (aguardando decisão)**:
  - `armorRightArm` (vazio — child de `bipedRightArm`)
  - `armorLeftArm` (vazio — child de `bipedLeftArm`)
  - `armorLeftLeg`, `armorLeftBoot` (vazios — children de `bipedLeftLeg`)
  - `armorRightLeg`, `armorRightBoot` (vazios — children de `bipedRightLeg`)
- Não há blocos, entidades, menus, block entities, receitas, loot tables ou tags registrados.
- Não há pasta `data/novadyne`; necessária futuramente para receitas, loot tables, tags e dados server-side.
- O arquivo `neoforge.mods.toml` está em `src/main/templates`, não diretamente em `src/main/resources/META-INF`; isso é esperado porque `build.gradle` gera metadata em build time.
- O projeto inclui GeckoLib 5.5.1 como jar local para NeoForge 26.1.2.
- API NeoForge 26.1.x: `Identifier.fromNamespaceAndPath(namespace, path)` para criar resource locations.
