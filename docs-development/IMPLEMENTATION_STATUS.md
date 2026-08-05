# Status de Implementação da Wiki — NovaDyne

> Atualizado em: 2026-08-05
> Próxima fase: **Fase 3 — Catálogo**

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
  `wiki/mkdocs.custom.yml` (merge profundo opcional) + nav calculado. O arquivo
  é ignorado no git e regenerado a cada execução.
- **`wiki/docs/` é descartável e reconstruído do zero** a cada geração;
  `wiki/theme/` é a fonte do tema (cópia para `docs/assets/`).
- **`build/wiki/` entrou em `DISPOSABLE_DIRS`** (apagável por `--clean`).
- **`wipe_dir` aceita `extra_allowed`** para permitir pastas alternativas
  (ex.: diretórios temporários dos testes) sem abrir mão da validação.
- **Catálogo determinístico**: schema `1`, sem timestamps; `build/wiki/`
  permanece descartável.
- **Item vanilla não mapeado** vira `None` quando o nome não é identificador
  válido; identificadores válidos seguem a heurística documentada
  (constante minúscula = id).
- **Erros e avisos separados**: avisos não falham por padrão; `--strict`
  eleva avisos a erro; `--check` valida também a idempotência.
- **Venv ignorado** em `tools/wiki/.venv/`; o build Gradle do mod continua
  independente da wiki.

### Testes executados

- `python -m unittest discover -s tools/wiki/tests -t tools/wiki` → **46 testes, OK**
  (I/O seguro, front matter, relatório, vanilla items, mkdocs.yml, builder,
  idempotência, caminhos).
- `python tools/wiki/generate.py --clean --verbose` → **OK** (0 avisos, 0 erros)
- `python tools/wiki/generate.py --check` → **OK** (idempotência confirmada)
- `python tools/wiki/generate.py --build` → **OK** (MkDocs Material compilou
  o site em `wiki/site/`: busca, 404, sitemap, tema claro/escuro)

### Limitações conhecidas

- Catálogo ainda vazio (`entries`/`recipes`); scanners chegam na Fase 3.
- Nav contém apenas a Home; seções de itens/blocos/receitas virão nas
  Fases 4–5.
- Validador de links cobre apenas páginas Markdown internas; validação de
  IDs/slugs/receitas entra na Fase 7.
- Tema ainda básico (CSS inicial); identidade visual completa na Fase 7.
- `wiki/content/` contém apenas `index.md`.
- Sem tarefas Gradle, CI de wiki ou GitHub Pages (Fase 8).

### Próxima fase

**Fase 3 — Catálogo**: implementar scanners (registros Java, receitas JSON e
de máquina, tags, modelos, texturas, traduções), preencher
`build/wiki/catalog.json`, produzir relatórios completos e testes dos
scanners. Não iniciada.
