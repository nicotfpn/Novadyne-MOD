# Status de Implementação da Wiki — NovaDyne

> Atualizado em: 2026-08-05
> Próxima fase: **Fase 4 — Itens e blocos**

Registro do progresso por fase. A fonte de verdade sobre o mod é
`REPOSITORY_AUDIT.md`; a arquitetura é descrita em `WIKI_ARCHITECTURE.md`.

---

## Fase 1 — Auditoria ✅ Concluída

Criado `docs-development/REPOSITORY_AUDIT.md`, baseado na leitura real do
repositório (registros Java, assets, dados, workflows). Nenhuma suposição.

## Fase 2 — Fundação ✅ Concluída

### Arquivos criados

**Pacote Python (`tools/wiki/novadyne_wiki/`):**
- `__init__.py`, `paths.py`, `errors.py`, `io_utils.py`, `reporter.py`,
  `model.py`, `content.py`, `catalog.py`, `theme.py`, `config.py`,
  `validate.py`, `builder.py`, `cli.py`
- `scanners/vanilla_items.py`

**Entrada e dependências:**
- `tools/wiki/generate.py` — CLI (`--check`, `--strict`, `--clean`,
  `--verbose`, `--build`, `--serve`)
- `tools/wiki/requirements.txt` — `mkdocs-material==9.5.50`,
  `PyYAML==6.0.2`

**Testes (`tools/wiki/tests/`):**
- `test_paths.py`, `test_io_utils.py`, `test_content.py`, `test_reporter.py`,
  `test_vanilla_items.py`, `test_config.py`, `test_builder.py`

**Site:**
- `wiki/content/index.md` — primeira página (manual)
- `wiki/theme/css/novadyne.css` — tema básico (variáveis CSS, claro/escuro,
  pixel art)

**Documentação:**
- `docs-development/WIKI_ARCHITECTURE.md` (novo)

### Arquivos alterados

- `.gitignore` — adicionados `wiki/docs/`, `wiki/generated/`, `wiki/mkdocs.yml`,
  `wiki/site/`, `tools/wiki/.venv/`

### Decisões tomadas

- **Padrão visual**: MkDocs Material com `font: false` (sem Google Fonts,
  sem CDN) e busca local; idioma do tema `pt-BR`.
- **`wiki/mkdocs.yml` é gerado** pelo gerador a partir de `BASE_CONFIG` +
  `wiki/mkdocs.custom.yml` (merge profundo opcional) + nav calculado.
- **`wiki/docs/` é descartável** e reconstruído do zero a cada geração.
- **Catálogo determinístico**: schema `1`, sem timestamps; `build/wiki/`
  permanece descartável.
- **Erros e avisos separados**: avisos não falham por padrão; `--strict`
  eleva avisos a erro; `--check` valida também a idempotência.

### Testes executados

- 46 testes, OK (Fase 2).

---

## Fase 3 — Catálogo intermediário e scanners ✅ Concluída

### Arquivos criados

**Scanners (`tools/wiki/novadyne_wiki/scanners/`):**
- `__init__.py`, `common.py` (ScanResult, ids de recurso, JSON com BOM)
- `registry_scanner.py` — registros NeoForge em Java (itens, blocos, BEs,
  menus, abas criativas, entidades)
- `language_scanner.py` — arquivos de idioma, `LanguageIndex` com fallback
  `pt_br` → `en_us` → demais
- `model_scanner.py` — modelos `models/**`, texturas e pais resolvidos
- `blockstate_scanner.py` — blockstates (variantes, multipart, refs)
- `asset_scanner.py` — texturas, definições de item, órfãos e refs quebradas
- `recipe_scanner.py` — receitas JSON normalizadas (shaped, shapeless,
  fornos, corte, ferraria; tipos desconhecidos preservados)
- `tag_scanner.py` — tags com valores declarados/resolvidos, refs e ciclos
- `loot_table_scanner.py` — loot tables (leitura conservadora)

**Catálogo e relatório:**
- `report_builder.py` — relatório derivado do catálogo
- `pipeline.py` — orquestração dos scanners, entradas e cruzamento de refs

**Testes (`tools/wiki/tests/`):**
- `support.py` (fixtures), `test_registry_scanner.py`,
  `test_language_scanner.py`, `test_model_scanner.py`,
  `test_recipe_scanner.py`, `test_tag_scanner.py`,
  `test_loot_table_scanner.py`, `test_catalog_phase3.py`

### Arquivos alterados

- `novadyne_wiki/model.py` — schema explícito (CatalogEntry/Recipe/IngredientRef)
- `novadyne_wiki/catalog.py` — `CatalogBuilder` completo (`schema_version`,
  `mod`, `entries`, `recipes`, `tags`, `diagnostics`, `generation`)
- `novadyne_wiki/reporter.py` — relatório do catálogo + `note_missing_model`
- `novadyne_wiki/cli.py` — pipeline integrado; `--check` cobre catálogo,
  relatórios, manifesto e config; `run_generation` aceita desvios p/ testes
- `docs-development/WIKI_ARCHITECTURE.md`, `docs-development/REPOSITORY_AUDIT.md`

### Scanners implementados

`RegistryScanner`, `LanguageScanner`, `ModelScanner`, `BlockstateScanner`,
`AssetScanner`, `RecipeScanner`, `TagScanner`, `LootTableScanner`,
`CatalogBuilder`, `ReportBuilder` (via `pipeline.py` + `report_builder.py`).

### Formatos suportados

- Registros NeoForge: `createItems`, `createBlocks`,
  `createDataComponents`, `create(Registries.X)`, `registerSimpleItem`,
  `registerSimpleBlockItem`, `registerBlock`, `register`
- Idiomas: `assets/<mod>/lang/*.json` (UTF-8, com/sem BOM)
- Modelos: `models/**/*.json` (parent, textures, elements)
- Blockstates: `variants` e `multipart`
- Definições de item: `items/*.json` (`minecraft:model`)
- Receitas: `crafting_shaped`, `crafting_shapeless`, `smelting`, `blasting`,
  `smoking`, `campfire_cooking`, `stonecutting`, `smithing_transform/trim`
  (ingrediente por item, tag e alternativas; resultado `{id, count}`)
- Tags: `data/*/tags/**` com refs `#ns:path`, `replace`, `required`
- Loot tables: `data/*/loot_table/**` (pools, entries `minecraft:item`,
  condições, construções não suportadas anotadas)

### Formatos não suportados (documentados, sem falha)

- Receitas de máquina definidas em Java (`*BlockEntity.java`) — comprovadas
  na auditoria, mas fora do escopo da Fase 3 (normalização prevista em fase
  futura de máquinas).
- Registros Java fora dos padrões acima → diagnóstico (sem suposição).
- Assets de GUI/partículas/entidades não são avaliados como órfãos.

### Testes executados

- `python -m unittest discover -s tools/wiki/tests -t tools/wiki` → **87
  testes, OK** (46 da Fase 2 preservados + 41 novos cobrindo os 30 casos
  obrigatórios da Fase 3: catálogo vazio, item/bloco/entidade registrados,
  traduções pt_br/en_us/ausente, modelos item/bloco, texturas, receitas
  shaped/shapeless/item/tag/quantidade/tipo desconhecido, tags com ref/ciclo,
  loot table, JSON inválido, ordem determinística, segunda geração idêntica,
  remoção de obsoleto, caminhos Windows/POSIX, Unicode, colisão de IDs,
  arquivo fora do namespace, relatório consistente com catálogo).
- `python tools/wiki/generate.py --clean --verbose` → **OK** (7 avisos,
  0 erros)
- `python tools/wiki/generate.py --check` → **OK** (idempotência confirmada;
  cobre catálogo, `report.json`, `report.md`, manifesto e `mkdocs.yml`)
- `python tools/wiki/generate.py --strict` → **FALHA (esperada)**: 7 avisos
  elevados a erro (assets órfãos conhecidos, ver abaixo)
- `python tools/wiki/generate.py --build` → **OK** (MkDocs Material compilou
  o site; Home apenas)
- Build Gradle do mod: **não executado** — o ambiente só tem Java 8 e o mod
  exige toolchain Java 25 (NeoForge 26.1.2); o fluxo da wiki é independente
  do build do mod (ver `WIKI_ARCHITECTURE.md`).

### Resultados reais encontrados (catálogo `build/wiki/catalog.json`)

- `mod`: NovaDyne 1.0.0 · Minecraft 26.1.2 · NeoForge 26.1.2.76 · id `novadyne`
- **33 entradas**: 20 itens, 4 blocos, 4 block entities, 4 menus,
  1 aba criativa
- **9 receitas**: 7 `crafting_shapeless`, 1 `smelting`, 1 `blasting`
- **1 tag**: `c:gems/quartz` (registry `item`)
- **4 loot tables**: `blocks/*`
- **1 idioma**: `en_us` (22 chaves)
- **24 modelos** (20 item + 4 bloco), **29 texturas** (23 item + 6 bloco),
  20 definições de item, 4 blockstates

### Warnings atuais (7)

1. `novadyne:item/macerator`, `wafer_press`, `processor`, `litografia` —
   modelos de item órfãos: as definições de item apontam para o modelo do
   bloco (`novadyne:block/<nome>`); os arquivos `models/item/<nome>.json`
   não são referenciados pelo sistema moderno de definições de item.
2. `textures/item/transistor.png`, `capacitor_tier_1.png`,
   `capacitor_tier_2.png` — texturas sem conteúdo registrado (conteúdo
   planejado, ver auditoria §11).

`--strict` falha enquanto esses assets pendentes existirem — comportamento
intencional da arquitetura (avisos viram erro em modo estrito).

### Novas descobertas comprovadas (registradas na auditoria)

- Os 9 JSONs de receita possuem BOM UTF-8 (lidos com `utf-8-sig`).
- Modelos `models/item/<nome>.json` dos itens de bloco são órfãos no sistema
  de definições de item do 26.1.x.

### Limitações conhecidas

- Receitas de máquina (Java) e estatísticas de máquina não entram no catálogo
  nesta fase; permanecem documentadas na auditoria.
- `documentation_status` é `auto` para todas as entradas (vínculo com páginas
  manuais chega na Fase 4).
- Páginas individuais, cards e visual de crafting ainda não existem (Fases
  4–5).
- O modo `--strict` falha com os 7 avisos de assets pendentes acima.
- Build do mod não verificado no ambiente (Java 8 disponível; exige Java 25).

### Próxima fase

**Fase 4 — Itens e blocos**: gerar páginas individuais e índices a partir do
catálogo, com links estáveis entre entradas, receitas e tags. Não iniciada.

**Fase 3 não iniciou a Fase 4**: nenhuma página de item/bloco, card, visual
de crafting, navegação por categorias, páginas de veículos/armas, CI ou
GitHub Pages foi implementada nesta fase.
