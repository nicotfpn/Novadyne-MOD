# Arquitetura da Wiki — NovaDyne

> Atualizado em: 2026-08-05 (Fase 2 — Fundação concluída)

Documento de referência da wiki gerada do NovaDyne. Descreve as camadas,
as pastas, os comandos e o que é manual ou gerado. O estado de implementação
por fase vive em `IMPLEMENTATION_STATUS.md`.

---

## 1. Objetivo

A wiki é gerada a partir das fontes reais do mod (registros Java, JSONs de
receitas, texturas, traduções), nunca de suposições. Ela é:

- **Pesquisável e navegável** (MkDocs Material, busca local, sem CDN);
- **Sustentável** (conteúdo novo vira página automaticamente);
- **Segura** (não altera código do mod, não sobrescreve textos manuais);
- **Determinística** (mesma entrada → mesma saída; idempotente).

## 2. Camadas

### Camada 1 — Fontes de verdade

Tudo o que existe no mod e pode ser lido sem executar código:

- `src/main/java/com/novadyne/**` (registros, block entities, receitas de máquina);
- `src/main/resources/assets/novadyne/**` (lang, modelos, blockstates, texturas);
- `src/main/resources/data/**` (receitas JSON, loot tables, tags);
- `gradle.properties` (versões, mod id).

### Camada 2 — Catálogo intermediário

`build/wiki/catalog.json` — dados normalizados e desacoplados dos formatos
brutos. Todo conteúdo vira uma entrada com `id`, `type`, `name`, `texture`,
`model`, `sources`, etc. As páginas são geradas **a partir do catálogo**, não
dos arquivos brutos.

Estado na Fase 2: catálogo criado com schema vazio (`entries: []`,
`recipes: []`). Os scanners da Fase 3 o preenchem.

### Camada 3 — Conteúdo manual

`wiki/content/` — Markdown com front matter YAML, mantido por humanos.
O gerador apenas o lê; **nunca** o sobrescreve.

Exemplo:

```yaml
---
title: NovaDyne
nav_title: Home
order: 0
---
```

### Camada 4 — Páginas geradas

`wiki/docs/` — árvore montada pelo gerador para o MkDocs. É **descartável**:
reconstruída do zero a cada execução. Páginas geradas por código carregarão o
marcador `<!-- AUTO-GENERATED: DO NOT EDIT DIRECTLY -->` (Fase 4+).

### Camada 5 — Site

MkDocs Material (tema local, modo claro/escuro, busca, 404, sitemap).
Tema próprio em `wiki/theme/`, copiado para `docs/assets/` na geração.

## 3. Estrutura de pastas

```
tools/wiki/
├── generate.py                  # ponto de entrada da CLI
├── requirements.txt             # dependências fixadas (mkdocs-material, PyYAML)
├── tests/                       # testes unittest da fundação
└── novadyne_wiki/               # pacote Python (stdlib + PyYAML)
    ├── paths.py                 # layout de pastas (única fonte de caminhos)
    ├── errors.py                # WikiError e Issue (warning/error)
    ├── io_utils.py              # I/O UTF-8, escrita atômica, caminhos seguros
    ├── reporter.py              # relatório build/wiki/report.{json,md}
    ├── model.py                 # modelos do catálogo (CatalogEntry, Recipe)
    ├── content.py               # carga de wiki/content/ (front matter)
    ├── catalog.py               # CatalogBuilder (schema do catálogo)
    ├── theme.py                 # cópia de wiki/theme -> docs/assets
    ├── config.py                # geração do mkdocs.yml + nav
    ├── validate.py              # validação de links internos
    ├── builder.py               # montagem da árvore docs
    ├── cli.py                   # argumentos e orquestração
    └── scanners/
        └── vanilla_items.py     # mapeamento conservador de itens vanilla

wiki/
├── content/                     # MANUAL — páginas mantidas por humanos
├── theme/                       # MANUAL — assets do tema (css, js)
├── docs/                        # GERADO — descartável, reconstruído
├── generated/                   # GERADO — descartável (Fase 4+)
├── mkdocs.yml                   # GERADO — escrito pelo gerador
├── mkdocs.custom.yml            # MANUAL — opcional, merge sobre o base
└── site/                        # SAÍDA do mkdocs build — descartável

build/wiki/                      # GERADO — catálogo + relatórios, descartável
docs-development/                # MANUAL — documentos de desenvolvimento
```

## 4. Comandos

Recomenda-se um venv em `tools/wiki/.venv` (ignorado pelo git):

```powershell
python -m venv tools/wiki/.venv
tools/wiki/.venv/Scripts/python -m pip install -r tools/wiki/requirements.txt
```

| Comando | Efeito |
|---|---|
| `python tools/wiki/generate.py` | Gera catálogo, árvore `docs/` e `mkdocs.yml` |
| `python tools/wiki/generate.py --check` | CI: falha se houver erros ou não-idempotência |
| `python tools/wiki/generate.py --strict` | Avisos passam a ser erros |
| `python tools/wiki/generate.py --clean` | Apaga pastas geradas antes de gerar |
| `python tools/wiki/generate.py --verbose` | Imprime detalhes |
| `python tools/wiki/generate.py --build` | Gera e executa `mkdocs build` |
| `python tools/wiki/generate.py --serve` | Gera e executa `mkdocs serve` (preview) |
| `python -m unittest discover -s tools/wiki/tests -t tools/wiki` | Testes |

O build padrão do mod (Gradle) **não** depende da wiki. Tarefas Gradle
convenientes e CI/Pages entram nas Fases 8–9.

## 5. O que é manual, gerado e descartável

| Pasta | Tipo | Pode apagar? |
|---|---|---|
| `wiki/content/` | Manual | Não |
| `wiki/theme/` | Manual | Não |
| `wiki/mkdocs.custom.yml` | Manual (opcional) | Não |
| `docs-development/` | Manual | Não |
| `wiki/docs/` | Gerado | Sim (só via `generate.py --clean` ou ferramenta) |
| `wiki/generated/` | Gerado | Sim |
| `wiki/mkdocs.yml` | Gerado | Sim (regenerado) |
| `wiki/site/` | Saída do MkDocs | Sim |
| `build/wiki/` | Gerado | Sim |

`io_utils.wipe_dir` só apaga diretórios declarados em
`paths.DISPOSABLE_DIRS` — proteção contra apagar pastas erradas.

## 6. Idempotência e relatório

- A geração é determinística: sem timestamps, ordenação estável, UTF-8
  explícito, escrita atômica (arquivo temporário + rename).
- O modo `--check` gera duas vezes e compara o manifesto de arquivos
  (SHA-256 por arquivo). Qualquer diferença é erro.
- `build/wiki/report.json` e `build/wiki/report.md` trazem conteúdos
  descobertos, páginas criadas/atualizadas/removidas, descrições, traduções e
  texturas ausentes, links quebrados e issues (avisos/erros).

## 7. Testes

Testes em `tools/wiki/tests/` (unittest, stdlib). Cobrem caminhos, I/O seguro,
front matter, relatório, mapeamento de itens vanilla, geração do mkdocs.yml e
idempotência do builder. Fixtures usam diretórios temporários — não tocam o
repositório real.

## 8. Segurança

- Não lê arquivos fora do repositório (`ensure_inside_root`).
- Não executa código do mod nem `eval`.
- Caminhos vindos de JSON são validados contra pastas permitidas.
- Não baixa recursos durante a geração; o site não depende de CDN.
- Não faz commit nem push automático.

## 9. Estado atual e próximas fases

Concluído: **Fase 1 (Auditoria)** e **Fase 2 (Fundação)**.

Próximas (não iniciadas):

1. **Fase 3 — Catálogo**: scanners (registros, receitas, tags, modelos),
   catálogo preenchido, relatório completo.
2. **Fase 4 — Itens e blocos**: geração de páginas, índices, links estáveis.
3. **Fase 5 — Receitas**: visual 3×3, “Como obter” e “Usado em”.
4. **Fase 6 — Veículos e armas**: templates especializados (conteúdo
   comprovado apenas).
5. **Fase 7 — Qualidade**: validadores completos, busca, acessibilidade.
6. **Fase 8 — Automação**: tarefas Gradle, CI, GitHub Pages.
7. **Fase 9 — Revisão final**.
